"""Record a statement: fetch the cycle's rows, apply the attribution plan,
and file Takumi's bill.

deterministic + idempotent — every write is skipped when its result already
exists: a renamed row already carries the prefix, Takumi's line is matched
rather than re-created, the bill is found by (Card, วันตัดรอบบิล), and the PDF
is attached only when no file of that name is on the bill.

Writes, per account the plan marks `ready`:
  1. rename friends' primary-card rows to `[บัตรหลัก] …`
  2. create Takumi's rows (statement BC + printed due date; points multiplier
     and `% cb` from `lib.promotions.classify` for charges, `×0` and no
     cashback for credits and fees)
  3. create Takumi's Bills row at the printed total, with the split in `Note`
  4. attach the statement PDF to it
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path

from .. import card_repo, notion_client, notion_files, promotions
from ..bill_cycle import PatternNotFoundError, cycle_for_month, pattern_for_card
from ..bill_draft import existing_bill, resolve_bill_card_name, select_options
from ..cards import CardNotFoundError, find_card
from ..bills import STATEMENT_PDF
from ..holders import HOLDERS
from ..ledger import cycle_rows
from ..transaction_write import build_transaction_properties
from .attribution import AccountPlan, plan_statement
from .model import Statement, StatementLine

THAI_NAMES = {"takumi": "เว็บ", "baiboon": "ใบบุญ", "nuta": "นุตา", "unmonitored": "unmonitored supplement(s)"}


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


def bill_note(statement: Statement, plan: AccountPlan) -> str:
    parts = []
    for holder in ("takumi", "baiboon", "nuta", "unmonitored"):
        if holder in plan.split:
            parts.append(f"{THAI_NAMES[holder]} ฿{plan.split[holder]:,.2f}")
    if abs(plan.carried) > 0.005:
        parts.append(f"balance carried from the previous statement ฿{plan.carried:,.2f}")
    note = (
        f"{statement.issuer} statement dated {statement.statement_date}, due {statement.due_date}. "
        f"฿{plan.total:,.2f} = " + " + ".join(parts) + "."
    )
    if plan.not_on_statement or plan.missing:
        note += f" Notion differs from the statement by ฿{plan.drift():+,.2f} — see /record-statement's report."
    return note


def record(statement: Statement, *, pdf: str | Path | None = None, dry_run: bool = False) -> dict:
    rows, card_ids = fetch_rows(statement)
    plans = plan_statement(statement, number_lookup, rows)
    takumi = HOLDERS["takumi"]
    out_accounts, warnings = [], []
    counts = {"renamed": 0, "created": 0, "bills_created": 0, "pdfs_attached": 0}

    for plan in plans:
        entry = _report(plan)
        out_accounts.append(entry)
        if plan.status != "ready":
            continue
        warnings.extend(w for w in cycle_warnings(statement, plan.card) if w not in warnings)
        warnings.extend(plan.warnings)
        takumi_card = card_ids.get(("takumi", plan.card))
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

        if dry_run:
            entry["creates"] = [_create_report(l, m, n, cb) for l, m, n, cb in creates]
            continue

        for r in plan.renames:
            notion_client.update_page_properties(r["id"], {"Name": {"title": [{"text": {"content": r["new"]}}]}})
            counts["renamed"] += 1
        created = []
        for line, mult, note, cb in creates:
            props = build_transaction_properties(
                name=line.name, amount=line.amount, transaction_date=line.date,
                bill_cycle_date=statement.statement_date, due_date=statement.due_date,
                card_page_id=takumi_card, note=note, multiplier=mult, cashback_percent=cb,
            )
            page = notion_client.create_page(takumi.transactions_ds, props)
            created.append({**_create_report(line, mult, note, cb), "id": page["id"]})
        counts["created"] += len(created)
        entry["creates"] = created

        if bill is None:
            bill = notion_client.create_page(takumi.bills_ds, {
                "title": {"title": [{"text": {"content": f"{bill_name} {statement.statement_date[:7]}"}}]},
                "Card": {"select": {"name": bill_name}},
                "วันตัดรอบบิล": {"date": {"start": statement.statement_date}},
                "ยอดชำระ": {"number": plan.total},
                "จ่ายแล้ว": {"checkbox": False},
                "Note": {"rich_text": [{"text": {"content": bill_note(statement, plan)}}]},
            })
            counts["bills_created"] += 1
            entry["bill"] = {"status": "created", "id": bill["id"], "ยอดชำระ": plan.total}
        if pdf is not None:
            names = {f.get("name") for f in bill["properties"].get(STATEMENT_PDF, {}).get("files", [])} if "properties" in bill else set()
            if Path(pdf).name not in names:
                notion_files.append_files_to_page(bill["id"], STATEMENT_PDF, [pdf])
                counts["pdfs_attached"] += 1
                entry["bill"]["pdf"] = "attached"
            else:
                entry["bill"]["pdf"] = "already attached"

    return {
        "statement": {"issuer": statement.issuer, "statement_date": statement.statement_date, "due_date": statement.due_date},
        "dry_run": dry_run,
        "counts": counts,
        "warnings": warnings,
        "accounts": out_accounts,
    }


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


def _bill_report(bill: dict, plan: AccountPlan) -> dict:
    amount = bill["properties"].get("ยอดชำระ", {}).get("number")
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
