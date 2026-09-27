"""AEON statement text → Statement.

deterministic + idempotent — pure function of the extracted text.

Layout (seen on the 10 Sep 2026 e-statement): one PDF, one or more pages per
card. Every page opens with the statement date, the product name, the due date
(`DD / MM / YYYY`) and the masked card number; a card's first page then prints
the minimum payment and the total balance as `<amount> Baht`. The opening block
lists single-dated payments and cashback (printed unsigned, but credits) until
`BALANCE BROUGHT FORWARD`; purchases follow as `TRANS POSTING DESCRIPTION
AMOUNT [FOREIGN CCY]`. Fees print undated (`ANNUAL FEE 1,605.00 VAT 7% 105.00
THB`) and are dated at the statement date.
"""

from __future__ import annotations

import re

from .model import CardAccount, CardSection, Statement, StatementLine, StatementParseError, parse_amount

_DATE = re.compile(r"^(\d\d)/(\d\d)/(\d{4})$")
_DUE = re.compile(r"^(\d\d) / (\d\d) / (\d{4})$")
_CARD = re.compile(r"^\d{4} - \d\d\*\* - \*\*\*\* - (\d{4})$")
_BAHT = re.compile(r"^(-?[\d,]+\.\d\d) Baht$")
_OPENING = re.compile(r"^OPENING BALANCE (-?[\d,]+\.\d\d)$")
_BROUGHT_FORWARD = re.compile(r"^BALANCE BROUGHT FORWARD\b")
_SINGLE = re.compile(r"^(\d\d)/(\d\d)/(\d{4}) (.+?) ([\d,]+\.\d\d)$")
_LINE = re.compile(
    r"^(\d\d)/(\d\d)/(\d{4}) \d\d/\d\d/\d{4} (.+?) (-?[\d,]+\.\d\d)(?: ([\d,]+\.\d\d) ([A-Z]{3}))?$"
)
_FEE = re.compile(r"^([A-Z][A-Z ]*\bFEE) ([\d,]+\.\d\d)(?: VAT 7% ([\d,]+\.\d\d) THB)?$")


def parse(text: str) -> Statement:
    lines = [l.strip() for l in text.splitlines()]
    st = next((m for l in lines if (m := _DATE.match(l))), None)
    due = next((m for l in lines if (m := _DUE.match(l))), None)
    if not (st and due):
        raise StatementParseError("AEON: statement date / due date not found")
    statement_date = f"{st.group(3)}-{st.group(2)}-{st.group(1)}"

    cards: dict[str, dict] = {}  # number → {product, total, prev, lines, open}
    order: list[str] = []
    cur: dict | None = None
    product: str | None = None
    baht_seen = 0
    for i, ln in enumerate(lines):
        if _DATE.match(ln) and i + 2 < len(lines) and _DUE.match(lines[i + 2]):
            product = lines[i + 1]  # page header: date / product / due / card number
            continue
        if (m := _CARD.match(ln)):
            num = m.group(1)
            if num not in cards:
                cards[num] = {"product": product, "total": None, "prev": 0.0, "lines": [], "open": True}
                order.append(num)
            cur, baht_seen = cards[num], 0
            continue
        if cur is None:
            continue
        if (m := _BAHT.match(ln)) and cur["total"] is None:
            baht_seen += 1
            if baht_seen == 2:  # first is the minimum payment, second the total balance
                cur["total"] = parse_amount(m.group(1))
            continue
        if (m := _OPENING.match(ln)):
            cur["prev"] = parse_amount(m.group(1))
            continue
        if _BROUGHT_FORWARD.match(ln):
            cur["open"] = False
            continue
        if (m := _LINE.match(ln)):
            note = f"Original amount {m.group(6)} {m.group(7)}." if m.group(6) else None
            amount = parse_amount(m.group(5))
            cur["lines"].append(
                StatementLine(
                    date=f"{m.group(3)}-{m.group(2)}-{m.group(1)}",
                    name=m.group(4),
                    amount=amount,
                    kind="credit" if amount < 0 else "charge",
                    note=note,
                )
            )
            continue
        if cur["open"] and (m := _SINGLE.match(ln)):
            # Opening block: payments and cashback, printed unsigned.
            name = m.group(4)
            cur["lines"].append(
                StatementLine(
                    date=f"{m.group(3)}-{m.group(2)}-{m.group(1)}",
                    name=name,
                    amount=-parse_amount(m.group(5)),
                    kind="payment" if name.startswith("PAYMENT") else "credit",
                )
            )
            continue
        if (m := _FEE.match(ln)):
            vat = f" Includes VAT 7% ฿{m.group(3)}." if m.group(3) else ""
            cur["lines"].append(
                StatementLine(
                    date=statement_date,
                    name=m.group(1),
                    amount=parse_amount(m.group(2)),
                    kind="fee",
                    note=f"The statement prints this line undated; dated at the statement date.{vat}",
                )
            )

    accounts = []
    for num in order:
        c = cards[num]
        if c["total"] is None:
            raise StatementParseError(f"AEON: no total balance found for card {num}")
        accounts.append(
            CardAccount(
                product=c["product"],
                total=c["total"],
                sections=(CardSection(num, c["prev"], tuple(c["lines"])),),
            )
        )
    return Statement(
        issuer="AEON",
        statement_date=statement_date,
        due_date=f"{due.group(3)}-{due.group(2)}-{due.group(1)}",
        accounts=tuple(accounts),
    )
