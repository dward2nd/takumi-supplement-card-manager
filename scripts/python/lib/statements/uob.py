"""UOB statement text → Statement.

deterministic + idempotent — pure function of the extracted text.

Layout (seen on the 25 Aug 2026 statement): one PDF per customer; each product
opens with its heading (`UOB ONE`) on the line before its primary card number,
and each further card number under it opens a supplement section. Lines read
`POST TRANS DESCRIPTION AMOUNT [CR]`, dated `DD MON` without a year;
installment lines repeat the amount (`373.00 373.00`). The product closes with
`TOTAL BALANCE - <PRODUCT> <amount>`. The POST date is kept (`posted`): UOB
One's cashback periods count by it. A foreign charge's original amount is
glued to its description (`… SAN FRANCISCO USD107.00`); it moves to the note.

The printed STATEMENT DATE can sit off the cycle (27 Sep 2026 for the cycle
that closed 25 Sep): the parser keeps what's printed, and /record-statement
maps it onto the card's cycle (`lib.statements.record.ledger_cycle`).
"""

from __future__ import annotations

import re

from .model import CardAccount, CardSection, RewardSummary, Statement, StatementLine, StatementParseError, parse_amount
from .parser import StatementParser

_MONTHS = {m: i for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(), 1)}
_DATE = r"(\d\d) ([A-Z]{3}) (\d{4})"
_CARD = re.compile(r"^\d{4} \d\dXX XXXX (\d{4})$")
_HEADING = re.compile(r"^UOB [A-Z ]+$")
_PREV = re.compile(r"^PREVIOUS BALANCE (-?[\d,]+\.\d\d)( CR)?$")
_LINE = re.compile(
    r"^(\d\d) ([A-Z]{3}) (\d\d) ([A-Z]{3}) (.+?) ([\d,]+\.\d\d)(?: (CR)| [\d,]+\.\d\d)?$"
)
_TOTAL = re.compile(r"^TOTAL BALANCE - (.+?) (-?[\d,]+\.\d\d)( CR)?$")
# A foreign charge prints its original amount glued to the description:
# `ANTHROPIC* CLAUDE SUB SAN FRANCISCO USD107.00 3,669.72` (seen 27 Sep 2026).
_FOREIGN = re.compile(r"^(.*?) ((?:USD|EUR|GBP|JPY|CNY|HKD|MOP|TWD|KRW|SGD|MYR|VND|AUD|NZD|CAD|CHF|INR|IDR|PHP))"
                      r"([\d,]+\.\d\d)$")


def _iso(day: str, mon: str, year: int) -> str:
    return f"{year:04d}-{_MONTHS[mon]:02d}-{int(day):02d}"


def _kind(name: str, credit: bool) -> str:
    if credit:
        return "payment" if name.startswith("PAYMENT") else "credit"
    return "fee" if re.search(r"\bFEE\b", name) else "charge"


def parse(text: str) -> Statement:
    sd = re.search(r"STATEMENT DATE " + _DATE, text)
    dd = re.search(r"PAYMENT DUE DATE " + _DATE, text)
    if not (sd and dd):
        raise StatementParseError("UOB: statement date / payment due date not found")
    st_year, st_month = int(sd.group(3)), _MONTHS[sd.group(2)]

    def year_for(mon: str) -> int:
        # Lines carry no year; a month later than the statement's belongs to last year.
        return st_year - 1 if _MONTHS[mon] > st_month else st_year

    lines = [l.strip() for l in text.splitlines()]
    accounts: list[CardAccount] = []
    product: str | None = None
    sections: list[dict] = []

    def close_section_list() -> tuple[CardSection, ...]:
        return tuple(
            CardSection(number=s["number"], previous_balance=s["prev"], lines=tuple(s["lines"]))
            for s in sections
        )

    for i, ln in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if _HEADING.match(ln) and _CARD.match(nxt):
            product, sections = ln, []
            continue
        if product is None:
            continue
        if (m := _CARD.match(ln)):
            sections.append({"number": m.group(1), "prev": 0.0, "lines": []})
            continue
        if (m := _PREV.match(ln)) and sections:
            v = parse_amount(m.group(1))
            sections[-1]["prev"] = -v if m.group(2) else v
            continue
        if (m := _TOTAL.match(ln)):
            if m.group(1) != product:
                raise StatementParseError(f"UOB: total for {m.group(1)!r} inside {product!r}")
            total = parse_amount(m.group(2)) * (-1 if m.group(3) else 1)
            accounts.append(CardAccount(product=product, total=total, sections=close_section_list()))
            product, sections = None, []
            continue
        if (m := _LINE.match(ln)) and sections:
            name, credit, note = m.group(5), bool(m.group(7)), None
            if (f := _FOREIGN.match(name)):
                name, note = f.group(1), f"Original amount {f.group(3)} {f.group(2)}."
            amount = parse_amount(m.group(6))
            sections[-1]["lines"].append(
                StatementLine(
                    date=_iso(m.group(3), m.group(4), year_for(m.group(4))),
                    name=name,
                    amount=-amount if credit else amount,
                    kind=_kind(name, credit),
                    note=note,
                    posted=_iso(m.group(1), m.group(2), year_for(m.group(2))),
                )
            )

    return Statement(
        issuer="UOB",
        statement_date=_iso(sd.group(1), sd.group(2), st_year),
        due_date=_iso(dd.group(1), dd.group(2), int(dd.group(3))),
        accounts=tuple(accounts),
    )


# `UOB REWARDS POINT SUMMARY`, one row per primary card:
# `5432 15XX XXXX 9310 1,334 0 1,598 17,618 0 30 SEP 26`
# = earned, adjustment, redeemed, outstanding balance, expiring points, expiring date.
_POINTS = re.compile(r"^\d{4} \d\dXX XXXX (\d{4}) ([\d,]+) (-?[\d,]+) ([\d,]+) ([\d,]+) [\d,]+ \d\d [A-Z]{3} \d\d$")


class UOBParser(StatementParser):
    key = issuer = "UOB"
    signature = "UOB"
    points_timing = "posting"   # points are credited as each charge posts (user, 2026-09-28)
    points_rounding = "line"    # per statement line, like the ledger formula (Aug/Sep 2026)

    def rewards(self, text: str, statement: Statement) -> tuple[RewardSummary, ...]:
        out = []
        for ln in text.splitlines():
            if (m := _POINTS.match(ln.strip())):
                n = [parse_amount(g) for g in m.groups()[1:]]
                out.append(RewardSummary(number=m.group(1), program="UOB Rewards", earned=n[0], adjusted=n[1],
                                         redeemed=n[2], outstanding=n[3]))
        return tuple(out)

    def parse_text(self, text: str) -> Statement:
        return parse(text)
