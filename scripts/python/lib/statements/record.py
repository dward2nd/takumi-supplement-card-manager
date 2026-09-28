"""Record a statement: fetch the cycle's rows, apply the attribution plan,
and file Takumi's bill.

deterministic + idempotent — every write is skipped when its result already
exists: a renamed row already carries the prefix, Takumi's line is matched
rather than re-created, the bill is found by (Card, วันตัดรอบบิล), and the PDF
is attached only when no file of that name is on the bill.

Dates: the ledger files every row and bill under the card's own cycle
(`ledger_cycle`). A bank sometimes prints a statement date a few days off it —
UOB printed 27 Sep / due 19 Oct 2026 for the cycle that closed 25 Sep, due
15 Oct — "they just shifted BC/DD on paper" (user, 2026-09-28). Then the
card's cycle dates are used and the printed ones go into the bill's Note.
When the printed date *is* a cycle date, the printed due date is kept.

Writes, per account the plan marks `ready`:
  1. rename friends' primary-card rows to `[บัตรหลัก] …`
  2. create Takumi's rows (statement BC + printed due date; points multiplier
     and `% cb` from `lib.promotions.classify` for charges, `×0` and no
     cashback for credits and fees)
  3. create Takumi's Bills row at the printed total, with the split in `Note`
  4. attach the statement PDF to it
  4a. stamp `Process Date` (the statement's posting date, where it prints one)
      on every row a line accounts for — new rows get it at creation
  4c. for a bank that rounds points once per cycle (KBank, KTC, Krungsri), add
      a `[ปรับคะแนน] ปัดเศษคะแนนรอบบิล YYYY-MM` row with what the ledger's per-row
      rounding loses on each printed points summary (`rounding_adjustments`;
      user, 2026-09-28) — on the account holder's ledger: Takumi's for a pooled
      account, the card's holder on a one-PDF-per-card issuer
  4b. for a line split between friends' shares and Takumi's remainder, add a
      `[ปรับคะแนน] <line>` row to Takumi's ledger with the points the per-row
      rounding lost (`split_adjustments`; user, 2026-09-28: the principal
      holder carries the adjustment)
  5. re-sync the Promotion Bureau rows the created and renamed rows count
     toward, fixing `% cb` / multiplier to the split (`lib.bureau.follow`)
"""

from __future__ import annotations

import dataclasses
import datetime as _dt
from pathlib import Path

from .. import card_repo, notion_client, notion_files, points_account, promotions
from .. import notion_blocks as nb
from ..bill_cycle import PatternNotFoundError, cycle_for_month, pattern_for_card
from ..bill_draft import DRAFT_PREFIX, existing_bill, resolve_bill_card_name, select_options
from ..cards import CardNotFoundError, find_card
from ..bills import STATEMENT_PDF
from .. import holders
from ..bureau import follow
from ..holders import HOLDERS
from ..ledger import cycle_rows
from ..points import row_points
from ..transaction_write import build_transaction_properties
from .attribution import AccountPlan, plan_statement
from .model import Statement, StatementLine

THAI_NAMES = {h.key: h.thai_name for h in HOLDERS.values()} | {"unmonitored": "unmonitored supplement(s)"}
PRIMARY_KEY = holders.primary().key


def number_lookup(issuer: str, number: str) -> tuple[str, str] | None:
    for c in card_repo.load_all():
        if c.issuer == issuer and number in c.statement_numbers:
            return c.name, c.statement_numbers[number]
    return None


def fetch_rows(statement: Statement) -> tuple[dict, dict]:
    """({(holder, card): [projected rows in this BC]}, {(holder, card): card page id})."""
    cards = {
        o[0]
        for a in statement.accounts
        for s in a.sections
        if (o := number_lookup(statement.issuer, s.number))
    }
    rows: dict[tuple[str, str], list[dict]] = {}
    card_ids: dict[tuple[str, str], str] = {}
    for key, holder in HOLDERS.items():
        for card in cards:
            try:
                page = find_card(holder.cards_ds, card)
            except CardNotFoundError:
                continue
            card_ids[(key, card)] = page["id"]
            rows[(key, card)] = cycle_rows(holder.transactions_ds, page["id"], statement.statement_date)
    return rows, card_ids


def fetch_later_rows(statement: Statement, card_ids: dict) -> dict:
    """{(friend, card): projected rows in the cycle after this one} — where a
    friend books a bank credit that landed after their bill was settled."""
    bc = _dt.date.fromisoformat(statement.statement_date)
    later: dict[tuple[str, str], list[dict]] = {}
    for (key, card), page_id in card_ids.items():
        if key == holders.primary().key:
            continue
        try:
            next_bc = pattern_for_card(card).active(bc + _dt.timedelta(days=1))[0]
        except PatternNotFoundError:
            continue
        later[(key, card)] = cycle_rows(HOLDERS[key].transactions_ds, page_id, next_bc.isoformat())
    return later


# How far a printed statement date may sit from the card's cycle date and still
# be taken as that cycle (a paper shift); further than this is a real question.
MAX_PAPER_SHIFT_DAYS = 5


def ledger_cycle(statement: Statement) -> tuple[Statement, list[str]]:
    """The statement re-dated to the ledger's cycle, and why (warnings).

    Every mapped card's cycle rule is asked for the cycle nearest the printed
    date. The printed date on a cycle date → unchanged (printed due date kept).
    A few days off → the card's cycle BC and due date. Off by more, or cards
    that disagree → refuse: that's a changed cycle, not paper.
    """
    printed = _dt.date.fromisoformat(statement.statement_date)
    cards = sorted({o[0] for a in statement.accounts for s in a.sections
                    if (o := number_lookup(statement.issuer, s.number))})
    found: dict[tuple[_dt.date, _dt.date], list[str]] = {}
    for card in cards:
        try:
            pattern = pattern_for_card(card)
        except PatternNotFoundError:
            continue
        hit = pattern.nearest(printed, MAX_PAPER_SHIFT_DAYS)
        if hit is None:
            raise ValueError(
                f"{statement.issuer} statement dated {printed}: no {card} cycle date within "
                f"{MAX_PAPER_SHIFT_DAYS} days — check the statement, or the card's cycle rule in lib/bill_cycle.py")
        found.setdefault(hit, []).append(card)
    if len({bc for bc, _ in found}) > 1:
        raise ValueError(f"{statement.issuer} statement dated {printed}: its cards' cycles disagree: "
                         + "; ".join(f"{', '.join(c)} → {bc}" for (bc, _), c in found.items()))
    if not found or next(iter(found))[0] == printed:
        return statement, []
    bc, dd = next(iter(found))
    ledger = dataclasses.replace(statement, statement_date=bc.isoformat(), due_date=dd.isoformat())
    return ledger, [f"{statement.issuer} printed statement date {statement.statement_date} / due "
                    f"{statement.due_date}, but the cycle closed {bc}: recorded under {bc} / due {dd} "
                    f"(the card's cycle); the printed dates are in the bill Note"]


def cycle_warnings(statement: Statement, card: str) -> list[str]:
    """Compare the printed dates with the card's bank pattern (report only)."""
    try:
        pattern = pattern_for_card(card)
    except PatternNotFoundError as e:
        return [str(e)]
    d = _dt.date.fromisoformat(statement.statement_date)
    bc, dd = cycle_for_month(pattern, d.year, d.month)
    out = []
    if bc.isoformat() != statement.statement_date:
        out.append(f"{card}: statement date {statement.statement_date}, but the card's pattern gives {bc}")
    if dd.isoformat() != statement.due_date:
        out.append(
            f"{card}: printed due date {statement.due_date}, but the card's pattern gives {dd}; "
            f"Takumi's rows use the printed date"
        )
    return out


def _classify(card: str, line: StatementLine) -> tuple[str | None, str | None, float | None]:
    """(multiplier, note, cashback_percent) for a new Takumi row. A 0% rate stays
    unset, per the household convention for rows that earn no cashback."""
    if line.kind != "charge":
        return "×0", None, None
    c = promotions.classify(card, _dt.date.fromisoformat(line.date), line.name)
    return c.points_override, c.note, c.cashback_percent or None


POINTS_ADJUSTMENT = "[ปรับคะแนน] "


def _baht_per_point(holder: str, card: str) -> float | None:
    try:
        page = find_card(HOLDERS[holder].cards_ds, card)
    except CardNotFoundError:
        return None
    return (page["properties"].get("บาทต่อ 1 คะแนน") or {}).get("number")


def split_adjustments(plan: AccountPlan, takumi_rows: list[dict]) -> list[dict]:
    """Points a split line loses to rounding, per split, to add back on Takumi's ledger.

    The bank awards a line's points once: floor(amount / baht per point) ×
    multiplier. Split into a friend's `[บัตรหลัก]` share and Takumi's remainder,
    each row rounds down on its own (TMN 7-11 ฿51 = 10 points at ×5; ฿27.50 +
    ฿23.50 = 5). The difference goes on a `[ปรับคะแนน] <line>` row in Takumi's
    ledger (user, 2026-09-28). A row already there (same name and date) is kept.
    """
    bpp = _baht_per_point(PRIMARY_KEY, plan.card)
    if not bpp:
        return []
    out = []
    for s in plan.splits:
        line, (kind, rem) = s["line"], s["remainder"] or (None, None)
        if kind == "new":
            mult = _classify(plan.card, rem)[0]
            rem_pts = row_points(rem.amount, bpp, mult)
        elif kind == "row":
            mult, rem_pts = rem.get("multiplier"), row_points(rem["amount"], bpp, rem.get("multiplier"))
        else:
            mult, rem_pts = s["rows"][0][1].get("multiplier"), 0
        # A holder can own several shares of one line (Baiboon's ฿47 + ฿12 of a ฿59 TMN): sum per row.
        shares = [(h, row_points(r["amount"], _baht_per_point(h, plan.card), r.get("multiplier"))) for h, r in s["rows"]]
        bank = row_points(line.amount, bpp, mult)
        lost = bank - sum(p for _, p in shares) - rem_pts
        name = POINTS_ADJUSTMENT + line.name
        if lost == 0 or any(r["name"] == name and (r["transaction_date"] or "")[:10] == line.date for r in takumi_rows):
            continue
        parts = " + ".join(f"{h} {p}" for h, p in shares) + f" + takumi {rem_pts}"
        out.append({"line": line, "points": lost, "name": name,
                    "note": (f"Points lost to rounding when the ฿{line.amount:,.2f} statement line of {line.date} "
                             f"was split: the bank gives {bank} ({mult or '×1'}), the rows give {parts}. "
                             f"{lost:+} points {'added back' if lost > 0 else 'taken off'} here "
                             f"(ใช้คะแนน {-lost}); the principal holder carries split-line adjustments.")})
    return out


ROUNDING_ADJUSTMENT = "[ปรับคะแนน] ปัดเศษคะแนนรอบบิล "


def rounding_adjustments(statement: Statement) -> list[dict]:
    """Per printed points summary on a bank that rounds once per cycle: the points
    the ledger's per-row flooring loses, less any rounding row already there."""
    from .. import rewards_audit   # late: rewards_audit reads the statements package
    from . import PARSERS
    parser = next((p for p in PARSERS.values() if p.issuer == statement.issuer), None)
    if parser is None or parser.points_rounding != "cycle":
        return []
    bc = _dt.date.fromisoformat(statement.statement_date)
    out = []
    for s in statement.rewards:
        owner = number_lookup(statement.issuer, s.number)
        if owner is None or "coins" in s.program.lower():
            continue
        card, holder = owner
        t = rewards_audit.tally(s, card, holder, parser, bc)
        lost = rewards_audit.rounding_lost(t) - t.rounding_adjustments
        if lost <= 0:
            continue
        account_holder = points_account.account_for(parser, card, holder).account_holder
        out.append({"card": card, "holder": account_holder, "points": lost, "number": s.number,
                    "name": ROUNDING_ADJUSTMENT + statement.statement_date[:7],
                    "note": (f"{card} …{s.number}, cycle {statement.statement_date}: the bank rounds points once on the "
                             f"cycle's spend at each rate (floor(Σ ÷ baht per point) × multiplier) = "
                             f"{t.earned + rewards_audit.rounding_lost(t)}; the ledger's rows round each one and give "
                             f"{t.earned}. +{lost} added back here (ใช้คะแนน {-lost}).")})
    return out


def bill_note(statement: Statement, plan: AccountPlan, printed: Statement | None = None) -> str:
    parts = []
    for holder in (*HOLDERS, "unmonitored"):
        if holder in plan.split:
            parts.append(f"{THAI_NAMES[holder]} ฿{plan.split[holder]:,.2f}")
    if abs(plan.carried) > 0.005:
        parts.append(f"balance carried from the previous statement ฿{plan.carried:,.2f}")
    shown = printed or statement
    note = f"{statement.issuer} statement dated {shown.statement_date}, due {shown.due_date}. "
    if printed and printed.statement_date != statement.statement_date:
        note += (f"The cycle closed {statement.statement_date} (filed there, due {statement.due_date}); "
                 f"the printed dates are shifted on paper. ")
    note += f"฿{plan.total:,.2f} = " + " + ".join(parts) + "."
    if plan.not_on_statement or plan.missing:
        note += f" Notion differs from the statement by ฿{plan.drift():+,.2f} — see /record-statement's report."
    return note


def record(statement: Statement, *, pdf: str | Path | None = None, dry_run: bool = False,
           sync_promotions: bool = True) -> dict:
    printed = statement
    statement, shift_warnings = ledger_cycle(printed)
    rows, card_ids = fetch_rows(statement)
    plans = plan_statement(statement, number_lookup, rows, fetch_later_rows(statement, card_ids))
    takumi = holders.primary()
    out_accounts, warnings = [], list(shift_warnings)
    counts = {"renamed": 0, "created": 0, "bills_created": 0, "bills_completed": 0, "pdfs_attached": 0,
              "process_dates": 0, "points_adjustments": 0}
    written: list[follow.Written] = []

    for plan in plans:
        entry = _report(plan)
        out_accounts.append(entry)
        if plan.status != "ready":
            continue
        warnings.extend(w for w in cycle_warnings(statement, plan.card) if w not in warnings)
        warnings.extend(plan.warnings)
        takumi_card = card_ids.get((takumi.key, plan.card))
        if takumi_card is None and plan.creates:
            entry["status"] = "blocked"
            entry["reason"] = f"{plan.card!r} isn't in Takumi's Cards DB — add it, then re-run"
            continue

        creates = []
        for line in plan.creates:
            mult, cnote, cb = _classify(plan.card, line)
            note = " ".join(n for n in (line.note, cnote) if n) or None
            creates.append((line, mult, note, cb))

        bill_name, new_option = resolve_bill_card_name(
            select_options(takumi.bills_ds), plan.card, plan.card
        )
        bill = None if new_option else existing_bill(takumi.bills_ds, bill_name, statement.statement_date)
        entry["bill"] = _bill_report(bill, plan) if bill else {"status": "would-create" if dry_run else "created"}

        bc = statement.statement_date
        # Renamed and re-dated rows are followed; a row both renamed and stamped once.
        touched = {r["id"]: {"holder": r["holder"], "date": r["date"], "name": r["new"], "posted": None,
                             "links": r["links"]} for r in plan.renames}
        for s in plan.stamps:
            touched.setdefault(s["id"], {"holder": s["holder"], "date": s["date"], "name": s["name"],
                                         "links": s["links"]})["posted"] = s["posted"]
        written += [follow.Written.of(i, t["holder"], card_ids.get((t["holder"], plan.card), ""), t["date"], bc,
                                      links=tuple(t["links"]), name=t["name"], posted=t["posted"])
                    for i, t in touched.items()]
        if plan.stamps:
            entry["process_dates"] = len(plan.stamps)
        adjustments = split_adjustments(plan, rows.get((takumi.key, plan.card), [])) if takumi_card else []
        if adjustments:
            entry["points_adjustments"] = [{"date": a["line"].date, "line": a["line"].name,
                                            "amount": a["line"].amount, "points": a["points"]} for a in adjustments]
        if dry_run:
            entry["creates"] = [_create_report(l, m, n, cb) for l, m, n, cb in creates]
            written += [follow.Written.of(None, takumi.key, takumi_card, l.date, bc, name=l.name, posted=l.posted)
                        for l, *_ in creates]
            continue

        for r in plan.renames:
            notion_client.update_page_properties(r["id"], {"Name": {"title": [{"text": {"content": r["new"]}}]}})
            counts["renamed"] += 1
        for s in plan.stamps:
            notion_client.update_page_properties(s["id"], {"Process Date": {"date": {"start": s["posted"]}}})
            counts["process_dates"] += 1
        created = []
        for line, mult, note, cb in creates:
            props = build_transaction_properties(
                name=line.name, amount=line.amount, transaction_date=line.date,
                bill_cycle_date=statement.statement_date, due_date=statement.due_date,
                card_page_id=takumi_card, note=note, multiplier=mult, cashback_percent=cb,
                process_date=line.posted,
            )
            page = notion_client.create_page(takumi.transactions_ds, props)
            created.append({**_create_report(line, mult, note, cb), "id": page["id"]})
            written.append(follow.Written.of(page["id"], takumi.key, takumi_card, line.date, bc,
                                             name=line.name, posted=line.posted))
        counts["created"] += len(created)
        entry["creates"] = created
        for a in adjustments:
            notion_client.create_page(takumi.transactions_ds, build_transaction_properties(
                name=a["name"], amount=0, transaction_date=a["line"].date,
                bill_cycle_date=statement.statement_date, due_date=statement.due_date,
                card_page_id=takumi_card, note=a["note"], multiplier="×0", points_redeemed=-a["points"]))
            counts["points_adjustments"] += 1

        if bill is None:
            bill = notion_client.create_page(takumi.bills_ds, {
                "title": {"title": [{"text": {"content": f"{bill_name} {statement.statement_date[:7]}"}}]},
                "Card": {"select": {"name": bill_name}},
                "วันตัดรอบบิล": {"date": {"start": statement.statement_date}},
                "ยอดชำระ": {"number": plan.total},
                "จ่ายแล้ว": {"checkbox": False},
                "Note": {"rich_text": nb.text(bill_note(statement, plan, printed))},
            })
            counts["bills_created"] += 1
            entry["bill"] = {"status": "created", "id": bill["id"], "ยอดชำระ": plan.total}
        elif _pending_draft(bill):
            # Drafted from a payment slip before the statement arrived
            # (lib.bill_draft.draft_statement_bill): the statement completes it.
            notion_client.update_page_properties(bill["id"], {
                "title": {"title": [{"text": {"content": f"{bill_name} {statement.statement_date[:7]}"}}]},
                "ยอดชำระ": {"number": plan.total},
                "Note": {"rich_text": nb.text(bill_note(statement, plan, printed))},
            })
            counts["bills_completed"] += 1
            entry["bill"] = {"status": "draft completed", "id": bill["id"], "ยอดชำระ": plan.total}
        if pdf is not None:
            names = {f.get("name") for f in bill["properties"].get(STATEMENT_PDF, {}).get("files", [])} if "properties" in bill else set()
            if Path(pdf).name not in names:
                notion_files.append_files_to_page(bill["id"], STATEMENT_PDF, [pdf])
                counts["pdfs_attached"] += 1
                entry["bill"]["pdf"] = "attached"
            else:
                entry["bill"]["pdf"] = "already attached"

    out = {
        "statement": {"issuer": statement.issuer, "statement_date": statement.statement_date, "due_date": statement.due_date,
                      **({"printed": {"statement_date": printed.statement_date, "due_date": printed.due_date}}
                         if printed is not statement else {})},
        "dry_run": dry_run,
        "counts": counts,
        "warnings": warnings,
        "accounts": out_accounts,
    }
    rounding = rounding_adjustments(statement)
    if rounding:
        out["rounding_adjustments"] = [{k: r[k] for k in ("card", "holder", "number", "points")} for r in rounding]
    if not dry_run:
        for r in rounding:
            h = HOLDERS[r["holder"]]
            notion_client.create_page(h.transactions_ds, build_transaction_properties(
                name=r["name"], amount=0, transaction_date=statement.statement_date,
                bill_cycle_date=statement.statement_date, due_date=statement.due_date,
                card_page_id=find_card(h.cards_ds, r["card"])["id"], note=r["note"], multiplier="×0",
                points_redeemed=-r["points"]))
            counts["points_adjustments"] += 1
    if sync_promotions and written:
        out["promotions"] = follow.follow_safely(written, dry_run=dry_run)
    return out


def _report(plan: AccountPlan) -> dict:
    e = {"product": plan.product, "card": plan.card, "status": plan.status, "total": plan.total}
    if plan.reason:
        e["reason"] = plan.reason
    if plan.status != "ready":
        return e
    e.update(
        split=plan.split,
        recorded=plan.recorded,
        renames=[{k: r[k] for k in ("holder", "id", "date", "amount", "new")} for r in plan.renames],
        payments_skipped=[{"date": l.date, "name": l.name, "amount": l.amount} for l in plan.payments],
        drift=plan.drift(),
    )
    for key in ("near_matches", "shares", "missing", "not_on_statement"):
        if getattr(plan, key):
            e[key] = getattr(plan, key)
    if abs(plan.carried) > 0.005:
        e["carried"] = plan.carried
    return e


def _pending_draft(bill: dict) -> bool:
    """A slip-first placeholder: `[DRAFT] …` title and no `ยอดชำระ` yet."""
    title = "".join(t.get("plain_text", "") for p in bill["properties"].values()
                    if p.get("type") == "title" for t in p.get("title", []))
    return title.startswith(DRAFT_PREFIX) and bill["properties"].get("ยอดชำระ", {}).get("number") is None


def _bill_report(bill: dict, plan: AccountPlan) -> dict:
    amount = bill["properties"].get("ยอดชำระ", {}).get("number")
    if _pending_draft(bill):
        return {"status": "draft to complete", "id": bill["id"], "ยอดชำระ": plan.total}
    r = {"status": "exists", "id": bill["id"], "ยอดชำระ": amount}
    if amount is None or abs(amount - plan.total) > 0.005:
        r["warning"] = f"existing bill says {amount}, statement prints {plan.total:,.2f} — left unchanged"
    return r


def _create_report(line: StatementLine, mult: str | None, note: str | None, cb: float | None = None) -> dict:
    r = {"date": line.date, "name": line.name, "amount": line.amount}
    if mult:
        r["multiplier"] = mult
    if cb:
        r["cashback_percent"] = cb
    if note:
        r["note"] = note
    return r
