"""KTC (Krungthai Card) statement text → Statement.

deterministic + idempotent — pure function of the extracted text.

Layout (seen on the 27 Aug 2026 statements for KTC UnionPay, KTC Digital VISA
and KTC JCB): one PDF per card number, one cardholder block each. The header
carries `TYPE OF CARD : <PRODUCT>`, the masked number `NNNN-NNXX-XXXX-NNNN`,
the closing date after `วันสรุปยอดบัญชี`, the due date after `วันครบกำหนดชำระ`
and the total due after `ยอดที่ต้องชำระ/ชำระเกิน (-)`. Lines sit between
`ยอดเรียกเก็บรอบที่แล้ว <previous balance>` and
`สรุปยอดรอบนี้ <NAME> <section total>`, reading
`TRANS POSTING DESCRIPTION AMOUNT` with `DD/MM/YY` dates. Credits and payments
print a detached minus: `Payment-KBANK Mobile - 25,101.00`.

KTC bills the principal and each supplement card separately (user,
2026-09-27): each card number gets its own statement and is paid on its own. So
a PDF holds exactly one cardholder block, and more than one `สรุปยอดรอบนี้`
refuses the parse. The extracted Thai decomposes sara am (`ชำาระ`), so Thai
labels are matched loosely.
"""

from __future__ import annotations

import re

from .model import CardAccount, CardSection, Statement, StatementLine, StatementParseError, parse_amount
from .parser import StatementParser

_PRODUCT = re.compile(r"TYPE OF CARD : (.+)")
_NUMBER = re.compile(r"\b\d{4}-\d\dXX-XXXX-(\d{4})\b")
_DATE = re.compile(r"(\d\d)/(\d\d)/(\d\d)")
_TOTAL = re.compile(r"ยอดที่ต้องช\S*ระ/ช\S*ระเกิน \(-\) (-?[\d,]+\.\d\d)(-?)")
_PREV = re.compile(r"^ยอดเรียกเก็บรอบที่แล้ว (-?[\d,]+\.\d\d)$")
_LINE = re.compile(r"^(\d\d)/(\d\d)/(\d\d) \d\d/\d\d/\d\d (.+?) (- )?([\d,]+\.\d\d)$")
_SUMMARY = re.compile(r"^สรุปยอดรอบนี้ .+ (-?[\d,]+\.\d\d)$")


def _iso(m: re.Match) -> str:
    return f"20{m.group(3)}-{m.group(2)}-{m.group(1)}"


def _date_after(text: str, label: str) -> str:
    i = text.find(label)
    m = _DATE.search(text, i) if i >= 0 else None
    if not m:
        raise StatementParseError(f"KTC: no date after {label!r}")
    return _iso(m)


def _kind(name: str, amount: float) -> str:
    if name.upper().startswith("PAYMENT"):
        return "payment"
    if amount < 0:
        return "credit"
    return "fee" if re.search(r"\bFEE\b", name, re.I) else "charge"


def parse(text: str) -> Statement:
    product = _PRODUCT.search(text)
    number = _NUMBER.search(text)
    total = _TOTAL.search(text)
    if not (product and number and total):
        raise StatementParseError("KTC: product, card number or total due not found")
    summaries = [l for l in (s.strip() for s in text.splitlines()) if _SUMMARY.match(l)]
    if len(summaries) != 1:
        raise StatementParseError(
            f"KTC: expected one cardholder block, found {len(summaries)} — supplement layout not seen yet"
        )

    prev = 0.0
    lines: list[StatementLine] = []
    inside = False
    for ln in (l.strip() for l in text.splitlines()):
        if (m := _PREV.match(ln)):
            prev, inside = parse_amount(m.group(1)), True
            continue
        if _SUMMARY.match(ln):
            break
        if inside and (m := _LINE.match(ln)):
            amount = parse_amount(m.group(6)) * (-1 if m.group(5) else 1)
            lines.append(StatementLine(date=_iso(m), name=m.group(4), amount=amount, kind=_kind(m.group(4), amount)))

    due = parse_amount(total.group(1)) * (-1 if total.group(2) else 1)
    return Statement(
        issuer="KTC",
        statement_date=_date_after(text, "วันสรุปยอดบัญชี"),
        due_date=_date_after(text, "วันครบก"),
        accounts=(
            CardAccount(
                product=product.group(1).strip(),
                total=due,
                sections=(CardSection(number.group(1), prev, tuple(lines)),),
            ),
        ),
    )


class KTCParser(StatementParser):
    key = issuer = "KTC"
    signature = "KRUNGTHAI CARD"
    separate_card_statements = True

    def parse_text(self, text: str) -> Statement:
        return parse(text)
