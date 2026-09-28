"""Decide which holder's ledger each statement line belongs in.

deterministic + idempotent — pure function of the statement, the card-number
map and the Notion rows handed in. No I/O; `record` fetches and writes.

The rule (see docs/databases/takumi-bills.md): every statement line lives in
exactly one ledger.

- A line on a **supplement** card number belongs to that supplement holder,
  recorded under its plain name. The statement only checks it — a line the
  holder hasn't recorded is reported, never written for them.
- A line on the **primary** card number belongs to whichever friend already
  recorded it (that row must carry the `[บัตรหลัก] ` prefix — added if
  missing), else to Takumi, who gets a new row unless he has one already.
  A friend's `[บัตรหลัก]` row for part of a line (their share of a split
  bill) claims that part; Takumi gets the remainder. Credits split the same
  way: a friend's row for part of a bank credit (First Choice's
  `เครดิตเงินคืน …` is shared out by holder) claims that part.
- Payments are never recorded here: they settle the previous bill.

Matching is by transaction date and amount, exact first, then the same amount
within NEAR_DAYS; a matching merchant stem breaks ties. Re-running over a
statement already recorded finds every line and plans nothing.
"""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field
from typing import Callable

from .. import ledger
from ..ledger import is_bill_payment_row, is_cashback_row
from .model import CardAccount, Statement, StatementLine

PRIMARY_PREFIX = ledger.PRIMARY_PREFIX + " "   # as written into a friend's row name
UNMONITORED = "unmonitored"  # a real supplement no one tracks: billed, never recorded
# Bracketed rows that are household bookkeeping, not statement lines: carry-forwards
# (both spellings are in use) and debt takeovers.
HOUSEHOLD_BRACKETS = ("[ยอดยกมา", "[ยกยอดมา", "[เว็บรับหนี้")
NEAR_DAYS = 3
_TOL = 0.005

# (issuer, last four digits) → (card title, holder slug), or None if unmapped.
NumberLookup = Callable[[str, str], "tuple[str, str] | None"]


@dataclass
class AccountPlan:
    product: str
    total: float
    card: str | None = None
    status: str = "ready"  # ready | skipped | blocked
    reason: str | None = None
    renames: list[dict] = field(default_factory=list)  # friend rows gaining the [บัตรหลัก] prefix
    creates: list[StatementLine] = field(default_factory=list)  # new Takumi rows
    recorded: int = 0  # lines already present in the right ledger
    near_matches: list[dict] = field(default_factory=list)  # matched on amount with the date off by ≤ NEAR_DAYS
    shares: list[dict] = field(default_factory=list)  # primary lines split between a friend's share and Takumi
    missing: list[dict] = field(default_factory=list)  # supplement lines absent from the holder's DB
    not_on_statement: list[dict] = field(default_factory=list)  # rows no statement line accounts for
    payments: list[StatementLine] = field(default_factory=list)
    split: dict[str, float] = field(default_factory=dict)  # holder → attributed amount
    carried: float = 0.0  # previous balance left after this statement's payments
    warnings: list[str] = field(default_factory=list)

    def drift(self) -> float:
        """Notion minus statement, over the lines this plan accounts for."""
        extra = sum(r["amount"] or 0 for r in self.not_on_statement)
        missing = sum(m["amount"] for m in self.missing)
        return round(extra - missing, 2)


def is_statement_line_row(row: dict, holder: str) -> bool:
    """Could this Notion row stand for a line on the bank statement?

    Excludes household bookkeeping: payments, transfers, ledger resets,
    carry-forwards and debt takeovers. Other bracketed rows stay in — a
    `[ยกเลิก] …` row is the statement's refund line, a `[บัตรหลัก] …` row a
    primary-card charge — since leaving one out would plan a duplicate for
    Takumi. A friend's cashback row is the household's own computed credit —
    the bank's cashback lands on Takumi's primary card — so it is excluded for
    friends only.
    """
    name = (row.get("name") or "").strip()
    if not name or row.get("amount") is None or not row.get("transaction_date"):
        return False
    if name.startswith(("Reset ", "โอนยอด")) or is_bill_payment_row(row):
        return False
    if name.startswith(HOUSEHOLD_BRACKETS):
        return False
    if holder != "takumi" and is_cashback_row(row):
        return False
    return True


def _stem(name: str) -> tuple[str, ...]:
    bare = re.sub(r"^(\[[^\]]*\]\s*)+", "", name or "").upper().split()
    return tuple(bare[:2])


def _days(a: str, b: str) -> int:
    return abs((_dt.date.fromisoformat(a) - _dt.date.fromisoformat(b)).days)


def _take(pool: list[dict], line_date: str, amount: float, name: str, *, near: bool) -> dict | None:
    """Remove and return the best row in `pool` for this date/amount, or None."""
    best, best_key = None, None
    for r in pool:
        if abs((r["amount"] or 0) - amount) > _TOL:
            continue
        d = _days(r["transaction_date"], line_date)
        if d > (NEAR_DAYS if near else 0):
            continue
        key = (d, _stem(r["name"]) != _stem(name))
        if best_key is None or key < best_key:
            best, best_key = r, key
    if best is not None:
        pool.remove(best)
    return best


def plan_account(
    statement: Statement,
    account: CardAccount,
    lookup: NumberLookup,
    rows: dict[tuple[str, str], list[dict]],
) -> AccountPlan:
    """Plan one card account. `rows[(holder, card)]` are that holder's rows on
    the card in this statement's bill cycle (projected; absent = none)."""
    plan = AccountPlan(product=account.product, total=account.total)
    if not account.has_activity():
        plan.status, plan.reason = "skipped", "no activity and nothing due"
        return plan

    owners = {s.number: lookup(statement.issuer, s.number) for s in account.sections}
    cards = {o[0] for o in owners.values() if o}
    if len(cards) > 1:
        plan.status, plan.reason = "blocked", f"card numbers map to different cards: {sorted(cards)}"
        return plan
    plan.card = next(iter(cards), None)
    unknown = [n for n, o in owners.items() if o is None]
    if unknown:
        plan.status = "blocked"
        plan.reason = (
            f"card number(s) {unknown} under {account.product!r} aren't in any "
            f"{statement.issuer} card's statement_numbers (scripts/repositories/cards/)"
        )
        if plan.card:
            plan.reason += "; " + _guess_owners(account, unknown, plan.card, rows)
        return plan

    card = plan.card
    pools = {
        h: [r for r in rows.get((h, card), []) if is_statement_line_row(r, h)]
        for h in ("takumi", "baiboon", "nuta")
    }
    friends = ("baiboon", "nuta")
    # One statement per card number (StatementParser.separate_card_statements):
    # a friend with no section here has only their [บัตรหลัก] rows to find on
    # it; their own card's rows belong to their own statement.
    from . import separate_card_statements   # late: the package imports this module
    if separate_card_statements(statement.issuer):
        on_statement = {o[1] for o in owners.values() if o}
        for h in friends:
            if h not in on_statement:
                pools[h] = [r for r in pools[h] if r["name"].startswith(PRIMARY_PREFIX.strip())]

    def credit(holder: str, amount: float) -> None:
        plan.split[holder] = round(plan.split.get(holder, 0.0) + amount, 2)

    primary_lines: list[StatementLine] = []
    for section in account.sections:
        holder = owners[section.number][1]
        plan.carried += section.previous_balance
        for line in section.lines:
            if line.kind == "payment":
                plan.payments.append(line)
                plan.carried += line.amount
                continue
            if holder == "takumi":
                primary_lines.append(line)
                continue
            credit(holder, line.amount)
            if holder == UNMONITORED:
                continue  # on the bill, in no ledger — nothing to check it against
            row = _take(pools[holder], line.date, line.amount, line.name, near=False) or _take(
                pools[holder], line.date, line.amount, line.name, near=True
            )
            if row is None:
                plan.missing.append({"holder": holder, "number": section.number, **_line(line)})
                continue
            plan.recorded += 1
            if row["transaction_date"] != line.date:
                plan.near_matches.append({"holder": holder, "row_id": row["id"], "row_date": row["transaction_date"], **_line(line)})
            if row["name"].startswith(PRIMARY_PREFIX.strip()):
                plan.warnings.append(
                    f"{holder}'s {row['name']!r} ({row['transaction_date']}, ฿{row['amount']:,.2f}) is "
                    f"on their own supplement card {section.number} but carries the [บัตรหลัก] prefix"
                )
    plan.carried = round(plan.carried, 2)

    # Primary lines: exact matches first across everyone, then near-date, then shares.
    remaining: list[StatementLine] = []
    for near in (False, True):
        remaining = []
        for line in primary_lines:
            owner, row = None, None
            for h in ("takumi", *friends):
                row = _take(pools[h], line.date, line.amount, line.name, near=near)
                if row is not None:
                    owner = h
                    break
            if row is None:
                remaining.append(line)
                continue
            credit(owner, line.amount)
            plan.recorded += 1
            if near:
                plan.near_matches.append({"holder": owner, "row_id": row["id"], "row_date": row["transaction_date"], **_line(line)})
            if owner != "takumi" and not row["name"].startswith(PRIMARY_PREFIX.strip()):
                plan.renames.append(
                    {"holder": owner, "id": row["id"], "old": row["name"], "new": PRIMARY_PREFIX + row["name"], **_line(line)}
                )
        primary_lines = remaining

    for line in remaining:
        claimed = _claim_shares(line, {h: pools[h] for h in friends})
        for h, r in claimed:
            credit(h, r["amount"])
        rest = round(line.amount - sum(r["amount"] for _, r in claimed), 2)
        if claimed:
            plan.shares.append(
                {**_line(line), "friends": {h: r["amount"] for h, r in claimed}, "takumi": rest}
            )
        if abs(rest) <= _TOL:
            continue
        credit("takumi", rest)
        if claimed:
            existing = _take(pools["takumi"], line.date, rest, line.name, near=True)
            if existing is not None:
                plan.recorded += 1
                continue
            shares = ", ".join(f"{h} ฿{r['amount']:,.2f}" for h, r in claimed)
            line = StatementLine(
                date=line.date, name=line.name, amount=rest, kind=line.kind,
                note=f"Takumi's remainder of the ฿{line.amount:,.2f} statement line; friends' share(s): {shares}."
                + (f" {line.note}" if line.note else ""),
            )
        plan.creates.append(line)

    for h, pool in pools.items():
        for r in pool:
            plan.not_on_statement.append(
                {"holder": h, "id": r["id"], "date": r["transaction_date"], "name": r["name"], "amount": r["amount"]}
            )
    return plan


def _claim_shares(line: StatementLine, pools: dict[str, list[dict]]) -> list[tuple[str, dict]]:
    """Friends' rows that are parts of this line: same merchant stem, same sign,
    within NEAR_DAYS, each smaller than the line, together no more than it.

    A share of a charge must carry the `[บัตรหลัก]` prefix — an unprefixed
    smaller row is more likely a purchase of its own. A share of a credit
    needn't: the household splits bank credits under the bank's own name."""
    sign = 1 if line.amount > 0 else -1
    size = abs(line.amount)
    cands = [
        (h, r)
        for h, pool in pools.items()
        for r in pool
        if (sign < 0 or r["name"].startswith(PRIMARY_PREFIX.strip()))
        and _stem(r["name"]) == _stem(line.name)
        and _days(r["transaction_date"], line.date) <= NEAR_DAYS
        and 0 < sign * (r["amount"] or 0) < size - _TOL
    ]
    cands.sort(key=lambda hr: _days(hr[1]["transaction_date"], line.date))
    claimed, total = [], 0.0
    for h, r in cands:
        if total + abs(r["amount"]) <= size + _TOL:
            claimed.append((h, r))
            total += abs(r["amount"])
    for h, r in claimed:
        pools[h].remove(r)
    return claimed


def _guess_owners(account: CardAccount, unknown: list[str], card: str, rows: dict) -> str:
    """Hint for an unmapped number: whose rows its lines match best."""
    hints = []
    for num in unknown:
        lines = [l for s in account.sections if s.number == num for l in s.lines if l.kind != "payment"]
        best = []
        for h in ("baiboon", "nuta", "takumi"):
            pool = [r for r in rows.get((h, card), []) if is_statement_line_row(r, h)]
            hits = sum(1 for l in lines if _take(pool, l.date, l.amount, l.name, near=False))
            if hits:
                best.append(f"{h} {hits}/{len(lines)}")
        hints.append(f"{num} matches " + (", ".join(best) if best else "no one's rows"))
    return "; ".join(hints)


def _line(line: StatementLine) -> dict:
    return {"date": line.date, "name": line.name, "amount": line.amount}


def plan_statement(statement: Statement, lookup: NumberLookup, rows: dict) -> list[AccountPlan]:
    return [plan_account(statement, a, lookup, rows) for a in statement.accounts]
