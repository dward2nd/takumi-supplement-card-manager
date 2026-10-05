"""Krungsri-family statement text → Statement.

deterministic + idempotent — pure function of the extracted text.

One PDF per card account (First Choice, Krungsri NOW / Visa / JCB / Lady,
Central The 1 Redz, Lotus's Beyond — layouts seen on the 5 Sep 2026
statements), bundling the primary and every supplement. The blocks, anchored
on their English captions:

  ยอดเรียกเก็บของรอบบัญชีที่แล้ว <prev>     previous balance
  <dated payment lines>                   … Total Payments <sum>
  <number> (<NAME>)                       one section per card that spent
  <dated purchase lines>                  … SUBTOTAL FOR <number> (<NAME>) <sum>
                                          … Transaction Amount <sum>
  <dated adjustment lines>                cashback / campaign credits, fees
                                          … Adjustment Amount <sum>
  Total Payment Due For Credit Card <total>

First Choice appends a personal-loan block (its second credit line) closing
with `Total Payment Due For Personal Loan <total>`; it becomes its own account
with section number `LOAN`.

A charge re-split into installments on the card line (PLAN ON DEMAND, the
household's U PLAN) stays in its card's section, followed by its reversal
`REV-FC PLAN ON DEMAND: <merchant>` under the heading of conversions to
installments. Its terms print after `Transaction Amount`, grouped by card under
headers without the space (`4784 48XX XXXX 1064(BAIBOON BOONMAPA)`):

  <charge posted> <billed> FIRST CHOICE PLAN ON DEMAND <principal left> 001/003 <term>
  <merchant, cut to 26 characters>
  ค่างวดต่อเดือน = <term>

A term goes to its card's section, dated the day it's billed (as the household
dates terms) and named `<merchant> 01/03`; the charge, the reversal and the
term are tagged with their `conversion` part.

Payments and adjustments belong to no card section; they're attached to the
account's own card number — the first masked number in the text. Lines read
`TRANS POSTING DESCRIPTION AMOUNT`, dated `DD/MM/YY` in either the Christian
(`26`) or the Buddhist (`69` = 2569) era. A foreign charge carries its original
amount in the description — `… CA (21.40 USD) 730.42` — which moves to the note.
"""

from __future__ import annotations

import re
from dataclasses import replace

from .. import installments
from .model import CardAccount, CardSection, RewardSummary, Statement, StatementLine, StatementParseError, parse_amount
from .parser import StatementParser

_AMT = r"(-?[\d,]+\.\d\d)"
_JOB_DATE = re.compile(r"_(\d\d)(\d\d)(\d{4})_\d+ \(U\)")
_THAI_MONTHS = "มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม".split()
_THAI_DATE = re.compile(r"(\d\d) (" + "|".join(_THAI_MONTHS) + r") (25\d\d)")
_TAIL_DATE = re.compile(r"(\d\d)/(\d\d)/(\d\d)$")
_CARD_ANYWHERE = re.compile(r"\b\d{4} \d\dXX XXXX (\d{4})\b")
_SECTION = re.compile(r"^\d{4} \d\dXX XXXX (\d{4}) \((.+)\)$")
_PREV = re.compile(r"ยอดเรียกเก็บของรอบบัญชีที่แล้ว " + _AMT + "$")
_LINE = re.compile(r"^(\d\d)/(\d\d)/(\d\d) \d\d/\d\d/\d\d (.+?) " + _AMT + "$")
_FOREIGN = re.compile(r"^(.*?) \(([\d,]+\.\d\d) ([A-Z]{3})\)$")
_TOTAL_PAYMENTS = re.compile(r"Total Payments " + _AMT + "$")
_TX_AMOUNT = re.compile(r"Transaction Amount " + _AMT + "$")
_ADJ_AMOUNT = re.compile(r"Adjustment Amount " + _AMT + "$")
_CARD_TOTAL = re.compile(r"Total Payment Due For Credit Card " + _AMT + "$")
_LOAN_TOTAL = re.compile(r"Total Payment Due For Personal Loan " + _AMT + "$")
_JOB_CODE = re.compile(r"_([A-Z]{3})_\d{8}_")
_PLAN_SECTION = re.compile(r"^\d{4} \d\dXX XXXX (\d{4}) ?\(.+\)$")
_PLAN_TERM = re.compile(r"^(\d\d)/(\d\d)/(\d\d) (\d\d)/(\d\d)/(\d\d) (.+? PLAN ON DEMAND) ([\d,]+\.\d\d) "
                        r"(\d{1,3})/(\d{1,3}) " + _AMT + "$")
_PLAN_END = re.compile(r"^SUBTOTAL OF |PLAN ON DEMAND / Total")
_PLAN_REVERSAL = re.compile(r"^REV-\w+ PLAN ON DEMAND\b")


def _year(yy: str) -> int:
    n = int(yy)
    return 2500 + n - 543 if n >= 50 else 2000 + n  # `69` → 2569 BE → 2026


def _iso(d: str, m: str, yy: str) -> str:
    return f"{_year(yy):04d}-{m}-{d}"


def _dates(lines: list[str], text: str) -> tuple[str, str]:
    m = _JOB_DATE.search(text)
    if not m:
        raise StatementParseError("Krungsri: statement date (job id `_DDMMYYYY_`) not found")
    statement_date = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    thai = _THAI_DATE.findall(text)
    if len(thai) >= 2:  # First Choice prints both dates in Thai: statement, then due
        d, mon, be = thai[1]
        return statement_date, f"{int(be) - 543:04d}-{_THAI_MONTHS.index(mon) + 1:02d}-{d}"
    for ln in lines:
        if _PREV.search(ln):
            break
        if (t := _TAIL_DATE.search(ln)) and (due := _iso(*t.groups())) > statement_date:
            return statement_date, due
    raise StatementParseError("Krungsri: payment due date not found")


def _line(m: re.Match, kind: str | None = None) -> StatementLine:
    name, amount, note = m.group(4), parse_amount(m.group(5)), None
    if (f := _FOREIGN.match(name)):
        name, note = f.group(1), f"Original amount {f.group(2)} {f.group(3)}."
    if kind is None:
        kind = "credit" if amount < 0 else ("fee" if re.search(r"\bFEE\b", name) else "charge")
    return StatementLine(date=_iso(m.group(1), m.group(2), m.group(3)), name=name, amount=amount, kind=kind, note=note)


def _term(m: re.Match, merchant: str) -> StatementLine:
    n, total = int(m.group(9)), int(m.group(10))
    return StatementLine(
        date=_iso(m.group(4), m.group(5), m.group(6)),
        name=installments.format_name(merchant or m.group(7), n, total),
        amount=parse_amount(m.group(11)),
        kind="charge",
        note=f"{m.group(7)} {n}/{total}, plan dated {_iso(m.group(1), m.group(2), m.group(3))}: "
             f"฿{m.group(8)} of principal before this term.",
        conversion="term",
    )


def _mark_conversions(lines: list[StatementLine]) -> list[StatementLine]:
    """Tag each reversal, and the charge of the same date and amount it takes back."""
    out = list(lines)
    for i, r in enumerate(out):
        if r.amount >= 0 or not _PLAN_REVERSAL.match(r.name):
            continue
        out[i] = replace(r, conversion="reversal")
        for j, c in enumerate(out):
            if c.conversion is None and c.kind == "charge" and c.date == r.date and abs(c.amount + r.amount) < 0.005:
                out[j] = replace(c, conversion="charge")
                break
    return out


def parse(text: str) -> Statement:
    lines = [l.strip() for l in text.splitlines()]
    statement_date, due_date = _dates(lines, text)
    head = _CARD_ANYWHERE.search(text)
    if not head:
        raise StatementParseError("Krungsri: no masked card number found")
    account_number = head.group(1)
    code = (_JOB_CODE.search(text) or [None, "CARD"])[1]

    accounts: list[CardAccount] = []
    sections: dict[str, dict] = {}
    order: list[str] = []
    state, current, loan = "start", None, False
    plan_owner: str | None = None   # whose installment terms are being listed

    def section(num: str) -> dict:
        if num not in sections:
            sections[num] = {"prev": 0.0, "lines": []}
            order.append(num)
        return sections[num]

    def close(product: str, total: float) -> None:
        nonlocal sections, order
        accounts.append(
            CardAccount(
                product=product,
                total=total,
                sections=tuple(CardSection(n, sections[n]["prev"], tuple(_mark_conversions(sections[n]["lines"])))
                               for n in order),
            )
        )
        sections, order = {}, []

    for i, ln in enumerate(lines):
        if (m := _PREV.search(ln)):
            state = "payments"
            section("LOAN" if loan else account_number)["prev"] = parse_amount(m.group(1))
            continue
        if state == "start":
            continue
        if _TOTAL_PAYMENTS.search(ln):
            state = "purchases"
            continue
        if _TX_AMOUNT.search(ln):
            state, current = "adjustments", None
            continue
        if _ADJ_AMOUNT.search(ln):
            state = "after"
            continue
        if (m := _CARD_TOTAL.search(ln)):
            close(f"KRUNGSRI {code} {account_number}", parse_amount(m.group(1)))
            state, loan = "start", True  # anything further is the personal-loan block
            continue
        if (m := _LOAN_TOTAL.search(ln)):
            close(f"KRUNGSRI {code} {account_number} PERSONAL LOAN", parse_amount(m.group(1)))
            state = "start"
            continue
        if (m := _SECTION.match(ln)) and state == "purchases":
            current = section(m.group(1))
            continue
        if state == "adjustments":
            if (m := _PLAN_SECTION.match(ln)):
                plan_owner = m.group(1)
                continue
            if _PLAN_END.search(ln):
                plan_owner = None
                continue
            if (m := _PLAN_TERM.match(ln)):
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                merchant = "" if _LINE.match(nxt) or re.match(r"[฀-๿]", nxt) else nxt
                section(plan_owner or account_number)["lines"].append(_term(m, merchant))
                continue
        if not (m := _LINE.match(ln)):
            continue
        owner = "LOAN" if loan else account_number
        if state == "payments":
            section(owner)["lines"].append(_line(m, "payment"))
        elif state == "purchases":
            (current if current is not None else section(owner))["lines"].append(_line(m))
        elif state == "adjustments":
            section(owner)["lines"].append(_line(m))

    return Statement(issuer="Krungsri", statement_date=statement_date, due_date=due_date, accounts=tuple(accounts))


# `Credit Card Point Summary`, then `previous +earned -used outstanding` (First Choice
# and Central The 1 print none). Lotus's prints coins instead:
# `+normal +special ±adjusted +outstanding +expiring old-points`.
_POINTS = re.compile(r"^([\d,]+) \+([\d,]+) -([\d,]+) ([\d,]+)$")
_COINS = re.compile(r"^\+([\d,]+\.\d\d) \+([\d,]+\.\d\d) ([+-][\d,]+\.\d\d) \+([\d,]+\.\d\d) \+[\d,]+\.\d\d [\d,]+$")


def _primary(statement: Statement) -> str | None:
    return statement.accounts[0].sections[0].number if statement.accounts and statement.accounts[0].sections else None


class KrungsriParser(StatementParser):
    key = issuer = "Krungsri"
    signature = "TOTAL PAYMENT DUE FOR CREDIT CARD"

    def rewards(self, text: str, statement: Statement) -> tuple[RewardSummary, ...]:
        lines = [l.strip() for l in text.splitlines()]
        start = next((i for i, l in enumerate(lines) if "Credit Card Point Summary" in l), None)
        number = _primary(statement)
        if start is None or not number:
            return ()
        for ln in lines[start + 1:start + 6]:
            if (m := _POINTS.match(ln)):
                n = [parse_amount(g) for g in m.groups()]
                return (RewardSummary(number=number, program="Krungsri points", earned=n[1],
                                      redeemed=n[2], outstanding=n[3]),)
        return ()

    def parse_text(self, text: str) -> Statement:
        return parse(text)


class LotusParser(KrungsriParser):
    """Lotus's Money Services is a Krungsri company: same layout, same PDF
    password, and Lotus's Beyond carries `issuer: Krungsri` in the card repo.
    Only the name and the signature differ."""

    key = "Lotus"
    signature = "LOTUS"
    # Coins per statement line: floor(amount / 50) blocks × 0.25, +1.25 at Lotus's
    # (5 Sep 2026 statement, 2026-10-05) — the ledger formula's own shape.
    points_rounding = "line"

    def rewards(self, text: str, statement: Statement) -> tuple[RewardSummary, ...]:
        number = _primary(statement)
        for ln in text.splitlines():
            if number and (m := _COINS.match(ln.strip())):
                n = [parse_amount(g.lstrip("+")) for g in m.groups()]
                return (RewardSummary(number=number, program="Lotus's coins", earned=n[0], bonus=n[1],
                                      adjusted=n[2], outstanding=n[3]),)
        return ()
