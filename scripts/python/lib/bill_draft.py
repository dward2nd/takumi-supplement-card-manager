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

from . import installments, notion_client, promotions
from .bill_cycle import PatternNotFoundError, active_cycle, cycle_for_month, pattern_for_card
from .bills import explain_cycle, require_bills_ds
from .cards import CardAmbiguousError, CardNotFoundError, card_title_text, card_titles_by_id, find_card
from .holders import resolve_holder
from .payments import is_bill_payment_row
from .transaction_read import project_transaction

DRAFT_PREFIX = "[DRAFT] "


class BillDraftError(RuntimeError):
    pass


class BillExistsError(BillDraftError):
    """A Bills row already exists for the (Card, วันตัดรอบบิล) pair."""

    def __init__(self, page: dict, holder_key: str, card: str, bill_cycle: str):
        self.page = page
        super().__init__(
            f"a bill row already exists for {holder_key}/{card} cycle "
            f"{bill_cycle} (id={page['id']}). Refusing to create a duplicate."
        )


def reject_statement_bills(holder) -> None:
    """Refuse to draft a bill for a holder whose bills come from the statement.

    A draft sums one holder's own Transactions rows. Takumi's bill is the
    bank's per-card total — his primary charges plus Baiboon's and Nuta's
    supplement and `[บัตรหลัก]` rows — so that sum would understate it.
    """
    if holder.statement_bills:
        raise BillDraftError(
            f"{holder.key!r} bills are the bank statement's per-card totals "
            f"(principal + supplement sections), not a sum of {holder.key}'s own "
            f"rows — create them from the statement, not /prepare-bill"
        )


def resolve_bill_card_name(
    options: list[str], card_name: str, cards_title: str
) -> tuple[str, bool]:
    """Map a card onto the Bills `Card` SELECT spelling → (name, is_new).

    Exact match first, then case-insensitive: the Cards DS title and the
    SELECT option can disagree on case (known-divergences #11, `Krungsri
    VISA` vs `Krungsri Visa`), and minting a second option that differs only
    in case would split the card's bill history in two.

    No match at all means the card has never been billed. The name is then
    the Cards DS title verbatim and `is_new` is True — Notion adds the
    option when the first bill is created with it.
    """
    if card_name in options:
        return card_name, False
    folded = [o for o in options if o.casefold() == card_name.strip().casefold()]
    if len(folded) == 1:
        return folded[0], False
    if len(folded) > 1:
        raise BillDraftError(
            f"card {card_name!r} matches several Bills SELECT options by case: {folded}"
        )
    return cards_title.strip(), True


def cards_with_crediting() -> frozenset[str]:
    """Cards whose cashback comes back as credit rows (a class in lib.crediting).

    Such cards need explicit `*CASHBACK*` credit rows in the cycle before
    the bill is drafted, otherwise the flat sum overstates the balance.
    """
    from .crediting import CREDITINGS   # late: crediting reaches back into bills-side modules
    return frozenset(CREDITINGS)


def select_options(ds_id: str) -> list[str]:
    """SELECT options on a Bills DS's `Card` property (verbatim strings)."""
    client = notion_client.get_client()
    ds = client.data_sources.retrieve(data_source_id=ds_id)
    card_prop = ds.get("properties", {}).get("Card", {})
    if card_prop.get("type") != "select":
        raise BillDraftError("Bills DS `Card` is not a SELECT — schema drift?")
    return [opt.get("name") for opt in card_prop.get("select", {}).get("options", [])]


def existing_bill(ds_id: str, card: str, bill_cycle: str) -> dict | None:
    pages = notion_client.query_all(
        ds_id,
        filter={
            "and": [
                {"property": "Card", "select": {"equals": card}},
                {"property": "วันตัดรอบบิล", "date": {"equals": bill_cycle}},
            ]
        },
    )
    return pages[0] if pages else None


def sum_cycle(
    transactions_ds: str, card_page_id: str, bill_cycle: str
) -> tuple[float, int, list[dict]]:
    rows = notion_client.query_all(
        transactions_ds,
        filter={
            "and": [
                {"property": "Card", "relation": {"contains": card_page_id}},
                {"property": "Bill Cycle Date", "date": {"equals": bill_cycle}},
            ]
        },
    )
    # Bill-payment rows (`ชำระ…` / `จ่าย…`) are excluded: `ยอดชำระ` is the
    # cycle's *amount due*, not its remaining balance. Including them would
    # net the payment into the total and make the result order-dependent — a
    # cycle drafted before its payment was recorded would read differently
    # from the same cycle drafted after. Cashback credits, refunds and
    # `[…]`-prefixed adjustments DO count; they change what is owed.
    # See lib.payments.is_bill_payment_row.
    total = 0.0
    for r in rows:
        projected = project_transaction(r)
        if is_bill_payment_row(projected):
            continue
        amt = projected.get("amount")
        if amt is not None:
            total += amt
    return round(total, 2), len(rows), rows


def has_cashback_credit_rows(rows: list[dict]) -> bool:
    """Heuristic: at least one row whose `Name` mentions CASHBACK."""
    for r in rows:
        props = r.get("properties", {})
        title = props.get("Name") or {}
        text = "".join(t.get("plain_text", "") for t in title.get("title", []) or [])
        if "CASHBACK" in text.upper():
            return True
    return False


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
    bills_ds = require_bills_ds(holder)
    reject_statement_bills(holder)

    # The Cards DB is the authority on whether the card exists — a typo
    # raises here with substring candidates. Only then is the name mapped
    # onto the Bills SELECT, so a card that has never been billed is a
    # first bill, not an error.
    card = find_card(holder.cards_ds, spec["card"])
    card_name, new_select_option = resolve_bill_card_name(
        select_options(bills_ds), spec["card"], card_title_text(card)
    )

    if (bc := spec.get("bill_cycle")):
        # Validate ISO format eagerly so we fail loud.
        _dt.date.fromisoformat(bc)
        bill_cycle = bc
    else:
        bc_date, _ = active_cycle(card_name, _dt.date.today())
        bill_cycle = bc_date.isoformat()

    # A SELECT option that doesn't exist yet can't have a bill behind it —
    # and querying on it is a 400, not an empty result.
    existing = None if new_select_option else existing_bill(bills_ds, card_name, bill_cycle)
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
        bc_date = _dt.date.fromisoformat(bill_cycle)
        pattern = pattern_for_card(card_name)
        cand_bc, cand_dd = cycle_for_month(pattern, bc_date.year, bc_date.month)
        if cand_bc != bc_date:
            cand_dd = pattern.due_date_shift(pattern.due_from_nominal_bc(bc_date))
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
    title = f"{DRAFT_PREFIX}{card_name} {bc_date.strftime('%Y-%m')}"

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
        "Card": {"select": {"name": card_name}},
        "วันตัดรอบบิล": {"date": {"start": bill_cycle}},
        "ยอดชำระ": {"number": total},
        "จ่ายแล้ว": {"checkbox": False},
    }
    if auto_note:
        properties["Note"] = {"rich_text": [{"text": {"content": auto_note}}]}

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
    if new_select_option:
        out["new_select_option"] = True
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


def draft_bills_in_window(spec: dict, *, dry_run: bool = False) -> dict:
    """Draft a bill for every cycle whose BC falls in [from, to], across cards.

    Spec keys: `bill_cycle_from`, `bill_cycle_to` (required, ISO, inclusive,
    at most MAX_WINDOW_DAYS apart); `holders` (list) or `holder` (default:
    both supplement holders); `cards` (optional list filter, matched
    case-insensitively); `skip_populate_installments`, `skip_cashback_check`,
    `skip_auto_note` (passed through to every draft).

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
    `reason` says which).
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
        reject_statement_bills(h)

    card_filter = {c.strip().casefold() for c in spec.get("cards") or []}
    passthrough = {
        k: spec[k]
        for k in ("skip_populate_installments", "skip_cashback_check", "skip_auto_note")
        if k in spec
    }

    results: list[dict] = []
    unassigned_rows: dict[str, int] = {}
    for holder in holders:
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
            if out.get("new_select_option"):
                entry["new_select_option"] = True
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
