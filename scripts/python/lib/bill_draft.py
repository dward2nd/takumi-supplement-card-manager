"""Draft a Bills row from a cycle's transactions.

deterministic + idempotent — re-running for the same (holder, card,
bill_cycle) refuses to create a duplicate. A Bills row uniquely
identifies on (Card, วันตัดรอบบิล); `draft_bill` aborts when one already
exists for that pair (draft or final).

This is the core behind /prepare-bill. It lives in `lib/` rather than in
`scripts/python/prepare-bill/` because /update-bill also needs it: when a
payment slip arrives for a cycle whose Bills row doesn't exist yet, that
skill drafts the bill first so the slip has somewhere to attach (the
script directory name `prepare-bill` is not a valid Python identifier, so
sharing by import from there isn't possible).

Sums `ยอดชำระ` across every transaction whose `Bill Cycle Date` equals the
cycle's BC date for the named card, **excluding bill-payment rows** —
`ยอดชำระ` is the amount *due*, not the balance remaining. Cashback offsets
are expected to already exist in the cycle as negative-amount rows, so the
sum is the "balance including cashback".
"""

from __future__ import annotations

import datetime as _dt

from . import card_repo, installments, notion_client
from . import notion_blocks as nb
from .bill_cycle import (PatternNotFoundError, active_cycle, cycle_for_month, due_date_for,
                         most_recent_closed_cycle, pattern_for_card)
from .bill_estimate import BillEstimateError, estimate, previous_bill_warning
from .bills import DRAFT_PREFIX, bills_for, card_relation, explain_cycle, require_bills_ds
from .cards import CardAmbiguousError, CardNotFoundError, card_title_text, card_titles_by_id, find_card
from .holders import HOLDERS, resolve_holder
from .ledger import PRIMARY_PREFIX, amount_due, cycle_pages, cycle_rows, title_text
from .transaction_read import project_transaction



class BillDraftError(RuntimeError):
    pass


def bill_title_card(card_page: dict) -> str:
    """The card as bill titles spell it (`<Card> <YYYY-MM>`): its card YAML `name`,
    which is what the bills have always carried and what /record-statement titles
    with (`Krungsri Visa`, where the Cards page says `Krungsri VISA`), else the
    Cards page title. Bill naming stays as it was (user, 2026-09-30)."""
    title = card_title_text(card_page)
    repo = card_repo.get(title)
    return repo.name if repo else title


class BillExistsError(BillDraftError):
    """A Bills row already exists for the (Card, วันตัดรอบบิล) pair."""

    def __init__(self, page: dict, holder_key: str, card: str, bill_cycle: str):
        self.page = page
        super().__init__(
            f"a bill row already exists for {holder_key}/{card} cycle "
            f"{bill_cycle} (id={page['id']}). Refusing to create a duplicate."
        )


def reject_statement_bills(holder) -> None:
    """Refuse to sum one holder's own rows into a bill whose total comes from the statement.

    Takumi's bill is the bank's per-card total — his primary charges plus
    Baiboon's and Nuta's supplement and `[บัตรหลัก]` rows — so his rows alone
    would understate it. His drafts go through `draft_primary_bill`, which
    adds up all three ledgers.
    """
    if holder.statement_bills:
        raise BillDraftError(
            f"{holder.key!r} bills are the bank statement's per-card totals "
            f"(principal + supplement sections), not a sum of {holder.key}'s own "
            f"rows — draft them with draft_primary_bill"
        )


def _on_pattern(card: str, bill_cycle: str) -> None:
    bc = _dt.date.fromisoformat(bill_cycle)
    try:
        on_pattern = cycle_for_month(pattern_for_card(card), bc.year, bc.month)[0] == bc
    except PatternNotFoundError as e:
        raise BillDraftError(str(e)) from e
    if not on_pattern:
        raise BillDraftError(f"{bill_cycle} isn't a cycle date of {card!r}'s bank pattern")


def _primary_estimate(bills_ds: str, card_page: dict, bill_cycle: str, unmonitored: float | None):
    try:
        est = estimate(bill_title_card(card_page), bill_cycle, unmonitored=unmonitored)
    except BillEstimateError as e:
        raise BillDraftError(str(e)) from e
    if (warning := previous_bill_warning(bills_ds, card_page["id"], bill_cycle)):
        est.warnings.append(warning)
    return est


def reestimate_primary_bill(holder, card: str, bill_cycle: str, *, unmonitored: float | None = None):
    """A fresh ledger estimate for an existing `[DRAFT]` statement bill (/update-bill's
    `refresh_from_transactions` on Takumi's drafts): rows added after the draft
    (a late-entered charge, a moved installment term) are picked up."""
    try:
        card_page = find_card(holder.cards_ds, card)
    except (CardNotFoundError, CardAmbiguousError) as e:
        raise BillDraftError(str(e)) from e
    return _primary_estimate(require_bills_ds(holder), card_page, bill_cycle, unmonitored)


def draft_primary_bill(spec: dict, *, dry_run: bool = False) -> dict:
    """`[DRAFT] <Card> <YYYY-MM>` on a statement-driven Bills DB, at the ledgers' estimate.

    Before the statement arrives, Takumi's bill is estimated from all three
    ledgers (`lib.bill_estimate`): his rows, each friend's statement-line rows
    (their subtotals go in the Note), and an `unmonitored` supplement's total
    the user supplies. /record-statement later completes the row with the
    printed total, title and Note, and reports how far the estimate was off.

    Spec keys: `holder` (the primary), `card` (required); `bill_cycle`
    (optional, default the card's most recently closed cycle); `unmonitored`
    (the untracked supplement's total, required for a card that has one).
    """
    for key in ("holder", "card"):
        if not spec.get(key):
            raise BillDraftError(f"missing required field: {key!r}")
    holder = resolve_holder(spec["holder"])
    if not holder.statement_bills:
        raise BillDraftError(f"{holder.key!r} bills are drafted from their own rows — use draft_bill")
    bills_ds = require_bills_ds(holder)
    try:
        card_page = find_card(holder.cards_ds, spec["card"])
    except (CardNotFoundError, CardAmbiguousError) as e:
        raise BillDraftError(str(e)) from e
    name = bill_title_card(card_page)
    if (bill_cycle := spec.get("bill_cycle")):
        _on_pattern(name, bill_cycle)
    else:
        bill_cycle = most_recent_closed_cycle(name, _dt.date.today())[0].isoformat()
    if (page := existing_bill(bills_ds, card_page["id"], bill_cycle)) is not None:
        raise BillExistsError(page, holder.key, name, bill_cycle)
    est = _primary_estimate(bills_ds, card_page, bill_cycle, spec.get("unmonitored"))
    if not est.lines and not est.split.get("unmonitored"):
        raise BillDraftError(f"no statement lines for {name} cycle {bill_cycle} in any ledger — nothing to bill")

    title = f"{DRAFT_PREFIX}{name} {bill_cycle[:7]}"
    out = {"holder": holder.key, "card": name, "bill_cycle": bill_cycle, "title": title,
           "ยอดชำระ": est.total, "split": est.split, "tx_count": est.lines, "note": est.note()}
    if est.warnings:
        out["warnings"] = est.warnings
    if dry_run:
        return {**out, "dry_run": True}
    page = notion_client.create_page(bills_ds, {
        "title": {"title": [{"text": {"content": title}}]},
        "Card": card_relation(card_page["id"]),
        "วันตัดรอบบิล": {"date": {"start": bill_cycle}},
        "ยอดชำระ": {"number": est.total},
        "จ่ายแล้ว": {"checkbox": False},
        "Note": {"rich_text": nb.text(est.note())},
    })
    return {"id": page["id"], "url": page.get("url"), **out}


def draft_statement_bill(holder, card: str, bill_cycle: str, *, dry_run: bool = False) -> dict:
    """A placeholder `[DRAFT] <Card> <YYYY-MM>` row on a statement-driven Bills DB.

    Takumi often pays the bank before the statement PDF arrives (user,
    2026-09-28: "put the payment slips to new drafted bills; I'll bring the
    statements later"), so the slip needs a row to attach to. The row carries
    no `ยอดชำระ` — only the statement knows the card total — and
    /record-statement completes it later: `ยอดชำระ`, `Note` and the title.

    Guards against typos: the card must be in the holder's Cards DS and
    `bill_cycle` must be one of its bank pattern's cycle dates.
    """
    if not holder.statement_bills:
        raise BillDraftError(f"{holder.key!r} bills are drafted from transactions — use draft_bill")
    try:
        card_page = find_card(holder.cards_ds, card)
    except (CardNotFoundError, CardAmbiguousError) as e:
        raise BillDraftError(str(e)) from e
    _on_pattern(card, bill_cycle)
    ds = require_bills_ds(holder)
    name = bill_title_card(card_page)
    if (page := existing_bill(ds, card_page["id"], bill_cycle)) is not None:
        raise BillExistsError(page, holder.key, name, bill_cycle)
    title = f"{DRAFT_PREFIX}{name} {bill_cycle[:7]}"
    note = ("Drafted from the payment slip before the statement arrived. "
            "ยอดชำระ and the split come from the statement (/record-statement completes this row).")
    out = {"holder": holder.key, "card": name, "bill_cycle": bill_cycle, "title": title,
           "statement_pending": True}
    if dry_run:
        return {**out, "id": None, "dry_run": True}
    page = notion_client.create_page(ds, {
        "title": {"title": [{"text": {"content": title}}]},
        "Card": card_relation(card_page["id"]),
        "วันตัดรอบบิล": {"date": {"start": bill_cycle}},
        "จ่ายแล้ว": {"checkbox": False},
        "Note": {"rich_text": nb.text(note)},
    })
    return {**out, "id": page["id"]}


def cards_with_crediting() -> frozenset[str]:
    """Cards whose cashback comes back as credit rows (a class in lib.crediting).

    Such cards need explicit `*CASHBACK*` credit rows in the cycle before
    the bill is drafted, otherwise the flat sum overstates the balance.
    """
    from .crediting import CREDITINGS   # late: crediting reaches back into bills-side modules
    return frozenset(CREDITINGS)


def existing_bill(ds_id: str, card_page_id: str, bill_cycle: str) -> dict | None:
    """The Bills row for (card page, วันตัดรอบบิล), if one exists."""
    pages = bills_for(ds_id, card_page_id, bill_cycle)
    return pages[0] if pages else None


def sum_cycle(
    transactions_ds: str, card_page_id: str, bill_cycle: str
) -> tuple[float, int, list[dict]]:
    rows = cycle_pages(transactions_ds, card_page_id, bill_cycle)
    # Bill-payment rows (`ชำระ…` / `จ่าย…`) are excluded: `ยอดชำระ` is the
    # cycle's *amount due*, not its remaining balance. Including them would
    # net the payment into the total and make the result order-dependent — a
    # cycle drafted before its payment was recorded would read differently
    # from the same cycle drafted after. Cashback credits, refunds and
    # `[…]`-prefixed adjustments DO count; they change what is owed.
    # See lib.ledger.is_bill_payment_row.
    return amount_due([project_transaction(r) for r in rows]), len(rows), rows


def has_cashback_credit_rows(rows: list[dict]) -> bool:
    """Heuristic: at least one row whose `Name` mentions CASHBACK."""
    return any("CASHBACK" in title_text(r).upper() for r in rows)


def draft_bill(spec: dict, *, dry_run: bool = False) -> dict:
    """Create the `[DRAFT] <Card> <YYYY-MM>` Bills row for a cycle.

    Spec keys: `holder`, `card` (required); `bill_cycle` (optional, inferred
    from the card's bank pattern); `skip_populate_installments`,
    `skip_cashback_check`, `skip_auto_note` (all optional, default False).
    """
    if not isinstance(spec, dict):
        raise BillDraftError("spec must be a JSON object")
    for key in ("holder", "card"):
        if not spec.get(key):
            raise BillDraftError(f"missing required field: {key!r}")

    holder = resolve_holder(spec["holder"])
    if holder.statement_bills:
        return draft_primary_bill(spec, dry_run=dry_run)
    bills_ds = require_bills_ds(holder)

    # The Cards DB is the authority on whether the card exists — a typo
    # raises here with substring candidates. The bill links to that page.
    card = find_card(holder.cards_ds, spec["card"])
    card_name = card_title_text(card)

    if (bc := spec.get("bill_cycle")):
        # Validate ISO format eagerly so we fail loud.
        _dt.date.fromisoformat(bc)
        bill_cycle = bc
    else:
        bc_date, _ = active_cycle(card_name, _dt.date.today())
        bill_cycle = bc_date.isoformat()

    existing = existing_bill(bills_ds, card["id"], bill_cycle)
    if existing is not None:
        raise BillExistsError(existing, holder.key, card_name, bill_cycle)

    # Auto-populate in-progress installments into this cycle before summing.
    # Without this, a 10-month plan whose next term hasn't been written yet
    # would silently shrink the bill total. The populate call is idempotent —
    # plans whose next term already lives in this cycle are skipped — and
    # uses the same library function /populate-installment calls, so the two
    # skills can't disagree. The user can disable this for back-fills where
    # they're recreating a historical bill snapshot.
    installments_summary: dict | None = None
    if not spec.get("skip_populate_installments"):
        # Derive the cycle's due date from the card's bank pattern so
        # appended rows carry the correct DD without depending on the
        # Bills DB which doesn't store DD on its own.
        cand_dd = due_date_for(card_name, _dt.date.fromisoformat(bill_cycle))
        installments_summary = installments.populate_for_cycle(
            holder_key=holder.key,
            transactions_ds=holder.transactions_ds,
            card_name=card_name,
            card_page_id=card["id"],
            bill_cycle=bill_cycle,
            due_date=cand_dd.isoformat(),
            auto_classify=True,
            exclude=set(),
            dry_run=dry_run,
        )

    total, tx_count, rows = sum_cycle(holder.transactions_ds, card["id"], bill_cycle)
    if tx_count == 0:
        raise BillDraftError(
            f"no transactions found for {holder.key}/{card_name} cycle {bill_cycle} "
            f"— nothing to bill. Did you mean a different cycle date?"
        )

    if card_name in cards_with_crediting() and not spec.get("skip_cashback_check"):
        if not has_cashback_credit_rows(rows):
            raise BillDraftError(
                f"{card_name} requires cashback credit rows before drafting the bill — "
                f"its cashback comes back as credit rows (lib.crediting) but the cycle has no "
                f"`*CASHBACK*` transactions, so the sum would overstate the balance owed. "
                f"Run /post-cashback-credits first (or pass "
                f'`"skip_cashback_check": true` in the spec to override).'
            )

    bc_date = _dt.date.fromisoformat(bill_cycle)
    title = f"{DRAFT_PREFIX}{bill_title_card(card)} {bc_date.strftime('%Y-%m')}"

    # Auto-generate the Note explaining special rows in this cycle (cashback
    # credits, manual adjustments, installment terms). Skip when the user
    # passes `skip_auto_note: true` — they may want to leave Note blank or
    # supply their own text via /update-bill afterwards.
    auto_note: str | None = None
    if not spec.get("skip_auto_note"):
        projected = [project_transaction(r) for r in rows]
        auto_note = explain_cycle(projected)

    properties = {
        "title": {"title": [{"text": {"content": title}}]},
        "Card": card_relation(card["id"]),
        "วันตัดรอบบิล": {"date": {"start": bill_cycle}},
        "ยอดชำระ": {"number": total},
        "จ่ายแล้ว": {"checkbox": False},
    }
    if auto_note:
        properties["Note"] = {"rich_text": nb.text(auto_note)}

    if dry_run:
        out: dict = {"dry_run": True}
    else:
        page = notion_client.create_page(bills_ds, properties)
        out = {"id": page["id"], "url": page.get("url")}
    out.update({
        "holder": holder.key,
        "card": card_name,
        "bill_cycle": bill_cycle,
        "title": title,
        "ยอดชำระ": total,
        "tx_count": tx_count,
    })
    if installments_summary is not None:
        out["installments"] = installments_summary
    if auto_note:
        out["auto_note"] = auto_note
    return out


MAX_WINDOW_DAYS = 31


def discover_cycles(
    transactions_ds: str, bill_cycle_from: str, bill_cycle_to: str
) -> tuple[dict[tuple[str, str], int], int]:
    """Every (card page id, BC) with rows whose `Bill Cycle Date` is in the window.

    Returns ({(card_id, bill_cycle): row_count}, unassigned_row_count). Rows
    with no `Card` relation can't belong to any bill; they are counted so the
    caller can surface them rather than silently dropping them.
    """
    rows = notion_client.query_all(
        transactions_ds,
        filter={
            "and": [
                {"property": "Bill Cycle Date", "date": {"on_or_after": bill_cycle_from}},
                {"property": "Bill Cycle Date", "date": {"on_or_before": bill_cycle_to}},
            ]
        },
    )
    cycles: dict[tuple[str, str], int] = {}
    unassigned = 0
    for r in rows:
        p = project_transaction(r)
        if not p["card_ids"]:
            unassigned += 1
            continue
        for card_id in p["card_ids"]:
            key = (card_id, p["bill_cycle_date"])
            cycles[key] = cycles.get(key, 0) + 1
    return cycles, unassigned


def pattern_bill_cycle(card_name: str, bill_cycle: str) -> str | None:
    """The card pattern's BC for `bill_cycle`'s month, or None if unregistered."""
    try:
        pattern = pattern_for_card(card_name)
    except PatternNotFoundError:
        return None
    bc = _dt.date.fromisoformat(bill_cycle)
    return cycle_for_month(pattern, bc.year, bc.month)[0].isoformat()


def _cycle_rows_by_name(holder, card: str, bill_cycle: str) -> list[dict]:
    try:
        page = find_card(holder.cards_ds, card)
    except CardNotFoundError:
        return []
    return cycle_rows(holder.transactions_ds, page["id"], bill_cycle)


def _primary_window(holder, lo: str, hi: str, card_filter: set[str], unmonitored: dict,
                    *, dry_run: bool) -> list[dict]:
    """Window mode for the primary: one estimate draft per (card, BC) any ledger has.

    Cycles come from all three Transactions DBs, since a card Takumi didn't use
    can still carry a friend's lines. `unmonitored` maps card → the untracked
    supplement's total. Status `skipped` is a cycle with no line on the
    principal's statement (a friend's own KTC/CardX card, a ledger reset).
    """
    found: dict[tuple[str, str], int] = {}
    for h in HOLDERS.values():
        titles = card_titles_by_id(h.cards_ds)
        for (card_id, bc), n in discover_cycles(h.transactions_ds, lo, hi)[0].items():
            if (title := titles.get(card_id)) is None:
                continue
            repo = card_repo.get(title)
            key = (repo.name if repo else title, bc)
            found[key] = found.get(key, 0) + n
    amounts = {k.strip().casefold(): v for k, v in unmonitored.items()}

    results = []
    for (card, bc), n in sorted(found.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if card_filter and card.casefold() not in card_filter:
            continue
        entry: dict = {"holder": holder.key, "card": card, "bill_cycle": bc, "rows": n}
        results.append(entry)
        expected = pattern_bill_cycle(card, bc)
        if expected is not None and expected != bc:
            entry.update(status="off-pattern", reason=f"card pattern puts this month's BC on {expected}; "
                                                      f"check the rows with /audit-transaction-dates")
            continue
        try:
            find_card(holder.cards_ds, card)
        except CardNotFoundError:
            # A friend's own card (Nuta's CardX JCB) with no principal in Takumi's
            # Cards DB. Only a [บัตรหลัก] row would put it on his statement.
            shares = [h.key for h in HOLDERS.values() if h is not holder
                      and any(r["name"].startswith(PRIMARY_PREFIX) for r in _cycle_rows_by_name(h, card, bc))]
            entry.update(status="blocked" if shares else "skipped",
                         reason=(f"{card} isn't in {holder.key}'s Cards DB"
                                 + (f", but {', '.join(shares)} have [บัตรหลัก] rows on it — add the card"
                                    if shares else " — not his bill")))
            continue
        spec = {"holder": holder.key, "card": card, "bill_cycle": bc}
        if card.casefold() in amounts:
            spec["unmonitored"] = amounts[card.casefold()]
        try:
            out = draft_primary_bill(spec, dry_run=dry_run)
        except BillExistsError as e:
            entry.update(status="exists", bill_id=e.page["id"],
                         **{"ยอดชำระ": e.page["properties"].get("ยอดชำระ", {}).get("number")})
            continue
        except BillDraftError as e:
            nothing = str(e).startswith("no statement lines")
            entry.update(status="skipped" if nothing else "blocked", reason=str(e))
            continue
        entry.update({"status": "would-create" if dry_run else "created",
                      **{k: out[k] for k in ("title", "ยอดชำระ", "split", "tx_count", "note")}})
        if out.get("warnings"):
            entry["warnings"] = out["warnings"]
        if not dry_run:
            entry["bill_id"] = out["id"]
    return results


def draft_bills_in_window(spec: dict, *, dry_run: bool = False) -> dict:
    """Draft a bill for every cycle whose BC falls in [from, to], across cards.

    Spec keys: `bill_cycle_from`, `bill_cycle_to` (required, ISO, inclusive,
    at most MAX_WINDOW_DAYS apart); `holders` (list) or `holder` (default:
    both supplement holders); `cards` (optional list filter, matched
    case-insensitively); `skip_populate_installments`, `skip_cashback_check`,
    `skip_auto_note` (passed through to every draft). Naming the primary
    (`takumi`) drafts his statement bills at the ledgers' estimate instead
    (`_primary_window`); `unmonitored` maps a card to its untracked
    supplement's total for those.

    Cycles are discovered from the Transactions DBs, not predicted from the
    card patterns — a card with no rows in the window has nothing to bill.
    Each cycle is drafted through `draft_bill`, so every single-card guard
    still applies; a guard that refuses becomes that cycle's `blocked`
    status instead of aborting the rest of the window. Idempotent: a re-run
    reports the cycles drafted last time as `exists`.

    Statuses: `created` / `would-create`, `exists`, `off-pattern` (the rows'
    BC isn't the card's bank-pattern BC for that month — misdated rows, or a
    bank-side shift the holiday library missed; draft it in single mode with
    an explicit `bill_cycle` if it's genuine), `blocked` (a guard refused;
    `reason` says which), and for the primary `skipped` (nothing on the
    principal's statement).
    """
    if not isinstance(spec, dict):
        raise BillDraftError("spec must be a JSON object")
    if spec.get("card") or spec.get("bill_cycle"):
        raise BillDraftError(
            "window mode takes `cards` (a list filter) and `bill_cycle_from`/"
            "`bill_cycle_to`, not `card`/`bill_cycle`"
        )
    try:
        lo = _dt.date.fromisoformat(spec["bill_cycle_from"])
        hi = _dt.date.fromisoformat(spec["bill_cycle_to"])
    except KeyError as e:
        raise BillDraftError(f"window mode needs both bill_cycle_from and bill_cycle_to (missing {e})") from None
    if lo > hi:
        raise BillDraftError(f"bill_cycle_from {lo} is after bill_cycle_to {hi}")
    # A wide window over history would mass-draft every old cycle that never
    # got a Bills row. Keep it to about one statement's worth.
    if (hi - lo).days >= MAX_WINDOW_DAYS:
        raise BillDraftError(
            f"window {lo}..{hi} spans {(hi - lo).days + 1} days; the limit is "
            f"{MAX_WINDOW_DAYS}. Run it as several windows."
        )

    if spec.get("holders"):
        holder_keys = list(spec["holders"])
    elif spec.get("holder"):
        holder_keys = [spec["holder"]]
    else:
        holder_keys = ["baiboon", "nuta"]
    holders = [resolve_holder(h) for h in holder_keys]
    for h in holders:
        require_bills_ds(h)

    card_filter = {c.strip().casefold() for c in spec.get("cards") or []}
    passthrough = {
        k: spec[k]
        for k in ("skip_populate_installments", "skip_cashback_check", "skip_auto_note")
        if k in spec
    }

    results: list[dict] = []
    unassigned_rows: dict[str, int] = {}
    for holder in holders:
        if holder.statement_bills:
            results += _primary_window(holder, lo.isoformat(), hi.isoformat(), card_filter,
                                       spec.get("unmonitored") or {}, dry_run=dry_run)
            continue
        titles = card_titles_by_id(holder.cards_ds)
        cycles, unassigned = discover_cycles(holder.transactions_ds, lo.isoformat(), hi.isoformat())
        if unassigned:
            unassigned_rows[holder.key] = unassigned

        for (card_id, bill_cycle), n in sorted(
            cycles.items(), key=lambda kv: (kv[0][1], titles.get(kv[0][0], ""))
        ):
            card_name = titles.get(card_id)
            if card_filter and (card_name or "").casefold() not in card_filter:
                continue
            entry: dict = {
                "holder": holder.key,
                "card": card_name or card_id,
                "bill_cycle": bill_cycle,
                "rows": n,
            }
            results.append(entry)
            if card_name is None:
                entry.update(status="blocked", reason="Card relation points outside this holder's Cards DB")
                continue

            expected = pattern_bill_cycle(card_name, bill_cycle)
            if expected is not None and expected != bill_cycle:
                entry.update(
                    status="off-pattern",
                    reason=f"card pattern puts this month's BC on {expected}; "
                    f"check the rows with /audit-transaction-dates",
                )
                continue

            try:
                out = draft_bill(
                    {"holder": holder.key, "card": card_name, "bill_cycle": bill_cycle, **passthrough},
                    dry_run=dry_run,
                )
            except BillExistsError as e:
                entry.update(status="exists", bill_id=e.page["id"])
                continue
            except (BillDraftError, CardNotFoundError, CardAmbiguousError, PatternNotFoundError) as e:
                entry.update(status="blocked", reason=str(e))
                continue

            # String keys, not keyword arguments: Python NFKC-normalizes
            # identifiers, which rewrites the Thai ำ (U+0E33) in `ยอดชำระ`
            # into ํ + า — a key that no longer matches the property name.
            entry.update({
                "status": "would-create" if dry_run else "created",
                "title": out["title"],
                "ยอดชำระ": out["ยอดชำระ"],
                "tx_count": out["tx_count"],
            })
            if not dry_run:
                entry["bill_id"] = out["id"]
            appended = (out.get("installments") or {}).get("count_appended")
            if appended:
                entry["installments_appended"] = appended

    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    out = {
        "mode": "window",
        "bill_cycle_from": lo.isoformat(),
        "bill_cycle_to": hi.isoformat(),
        "holders": [h.key for h in holders],
        "counts": counts,
        "results": results,
    }
    if dry_run:
        out["dry_run"] = True
    if unassigned_rows:
        out["unassigned_rows"] = unassigned_rows
    return out
