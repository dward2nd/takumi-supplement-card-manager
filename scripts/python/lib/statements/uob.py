"""UOB statement text → Statement.

deterministic + idempotent — pure function of the extracted text.

Layout (seen on the 25 Aug 2026 statement): one PDF per customer; each product
opens with its heading (`UOB ONE`) on the line before its primary card number,
and each further card number under it opens a supplement section. Lines read
`POST TRANS DESCRIPTION AMOUNT [CR]`, dated `DD MON` without a year;
installment lines repeat the amount (`373.00 373.00`). The product closes with
`TOTAL BALANCE - <PRODUCT> <amount>`.
"""

from __future__ import annotations

import re

from .model import CardAccount, CardSection, Statement, StatementLine, StatementParseError, parse_amount
from .parser import StatementParser

_MONTHS = {m: i for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(), 1)}
_DATE = r"(\d\d) ([A-Z]{3}) (\d{4})"
_CARD = re.compile(r"^\d{4} \d\dXX XXXX (\d{4})$")
_HEADING = re.compile(r"^UOB [A-Z ]+$")
_PREV = re.compile(r"^PREVIOUS BALANCE (-?[\d,]+\.\d\d)( CR)?$")
_LINE = re.compile(
    r"^\d\d [A-Z]{3} (\d\d) ([A-Z]{3}) (.+?) ([\d,]+\.\d\d)(?: (CR)| [\d,]+\.\d\d)?$"
)
_TOTAL = re.compile(r"^TOTAL BALANCE - (.+?) (-?[\d,]+\.\d\d)( CR)?$")


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
            name, credit = m.group(3), bool(m.group(5))
            amount = parse_amount(m.group(4))
            sections[-1]["lines"].append(
                StatementLine(
                    date=_iso(m.group(1), m.group(2), year_for(m.group(2))),
                    name=name,
                    amount=-amount if credit else amount,
                    kind=_kind(name, credit),
                )
            )

    return Statement(
        issuer="UOB",
        statement_date=_iso(sd.group(1), sd.group(2), st_year),
        due_date=_iso(dd.group(1), dd.group(2), int(dd.group(3))),
        accounts=tuple(accounts),
    )


class UOBParser(StatementParser):
    key = issuer = "UOB"
    signature = "UOB"

    def parse_text(self, text: str) -> Statement:
        return parse(text)
