"""KBank statement text → Statement.

deterministic + idempotent — pure function of the extracted text.

Layout (seen on the 25 Aug 2026 statement): one PDF bundles every KBank product
under the primary holder, each opening with
`/ ACCOUNT DETAILS <PRODUCT> <card number> <name>` and closing with
`***** TOTAL BALANCE ***** <amount>`. Lines read
`TRANS POSTING DESCRIPTION AMOUNT` with `DD/MM/YY` dates; credits and payments
carry a leading minus. The back pages print a *sample* statement (dated 2020)
whose lines must be ignored — they fall outside any open account.
"""

from __future__ import annotations

import re

from .model import CardAccount, CardSection, Statement, StatementLine, StatementParseError, parse_amount

_HEADER = re.compile(r"^/ ACCOUNT DETAILS (.+?) \d{4} \d\dXX XXXX (\d{4})\b")
_PREV = re.compile(r"^PREVIOUS BALANCE (-?[\d,]+\.\d\d)$")
_LINE = re.compile(r"^(\d\d)/(\d\d)/(\d\d) \d\d/\d\d/\d\d (.+?) (-?[\d,]+\.\d\d)$")
_TOTAL = re.compile(r"^\*+ ?TOTAL BALANCE ?\*+ (-?[\d,]+\.\d\d)$")


def _kind(name: str, amount: float) -> str:
    if name.startswith("PAYMENT"):
        return "payment"
    if amount < 0:
        return "credit"
    return "fee" if re.search(r"\bFEE\b", name) else "charge"


def parse(text: str) -> Statement:
    sd = re.search(r"STATEMENT DATE (\d\d)/(\d\d)/(\d{4})", text)
    dd = re.search(r"DUE DATE (\d\d)/(\d\d)/(\d{4})", text)
    if not (sd and dd):
        raise StatementParseError("KBank: statement date / due date not found")

    accounts: list[CardAccount] = []
    cur: dict | None = None
    for ln in (l.strip() for l in text.splitlines()):
        if (m := _HEADER.match(ln)):
            cur = {"product": m.group(1), "number": m.group(2), "prev": 0.0, "lines": []}
            continue
        if cur is None:
            continue
        if (m := _PREV.match(ln)):
            cur["prev"] = parse_amount(m.group(1))
            continue
        if (m := _TOTAL.match(ln)):
            accounts.append(
                CardAccount(
                    product=cur["product"],
                    total=parse_amount(m.group(1)),
                    sections=(CardSection(cur["number"], cur["prev"], tuple(cur["lines"])),),
                )
            )
            cur = None
            continue
        if (m := _LINE.match(ln)):
            amount = parse_amount(m.group(5))
            cur["lines"].append(
                StatementLine(
                    date=f"20{m.group(3)}-{m.group(2)}-{m.group(1)}",
                    name=m.group(4),
                    amount=amount,
                    kind=_kind(m.group(4), amount),
                )
            )

    return Statement(
        issuer="KBank",
        statement_date=f"{sd.group(3)}-{sd.group(2)}-{sd.group(1)}",
        due_date=f"{dd.group(3)}-{dd.group(2)}-{dd.group(1)}",
        accounts=tuple(accounts),
    )
