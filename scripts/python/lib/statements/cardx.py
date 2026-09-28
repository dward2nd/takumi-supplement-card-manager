"""CardX statement text → Statement.

deterministic + idempotent — pure function of the extracted text.

Layout (seen on Nuta's CardX JCB statements, Feb–Sep 2026): one PDF per card
number, locked with that cardholder's own date of birth. The header prints
`NNNN NNXX XXXX NNNN <PRODUCT> <limit> <total limit>` and then one line with
the closing date, the total due, the minimum payment and the due date:
`05/09/26 1,103.45 798.25 25/09/26` (`DD/MM/YY`). Lines sit between
`PREVIOUS BALANCE <amount>` and `TOTAL BALANCE <amount>`, reading
`POSTING TRANSACTION DESCRIPTION AMOUNT` with `DD/MM` dates.

The text extraction renders hyphens as a soft hyphen (U+00AD). Before an amount
it's the minus sign (`PAYMENT RECEIVED,THK YOU \xad1,600.00`); inside a
description it's a plain hyphen (`AGODA.COM FD SGN\xadDMK`), written back as `-`.

The points block prints six figures under `… OUTSTANDING POINTS`: brought
forward, regular earned, bonus earned, adjusted, redeemed, outstanding
(`55 15 0 0 0 70`; a refund can turn earned negative, `227 -376 0 0 0 -149`).

Read by /audit-rewards and /sync-points-balance (2026-09-29). All eight of
Nuta's statements reproduce their printed totals. /record-statement has never
been run on a CardX PDF: it files Takumi's bills, and this one is Nuta's own card.
"""

from __future__ import annotations

import re

from .model import CardAccount, CardSection, RewardSummary, Statement, StatementLine, StatementParseError, parse_amount
from .parser import StatementParser

_SOFT_HYPHEN = "­"
_MINUS = f"[{_SOFT_HYPHEN}-]"
_CARD = re.compile(r"^\d{4} \d\dXX XXXX (\d{4}) (.+?) [\d,]+ [\d,]+$", re.M)
_CLOSING = re.compile(rf"^(\d\d)/(\d\d)/(\d\d) ({_MINUS}?[\d,]+\.\d\d) [\d,]+\.\d\d (\d\d)/(\d\d)/(\d\d)$", re.M)
_PREV = re.compile(rf"^PREVIOUS BALANCE ({_MINUS}?[\d,]+\.\d\d)$")
_LINE = re.compile(rf"^(\d\d)/(\d\d) (\d\d)/(\d\d) (.+?) ({_MINUS}?)([\d,]+\.\d\d)$")
_TOTAL = re.compile(rf"^TOTAL BALANCE ({_MINUS}?[\d,]+\.\d\d)$")
_POINTS_HEADER = "OUTSTANDING POINTS"
_POINTS = re.compile(rf"^({_MINUS}?[\d,]+) ({_MINUS}?[\d,]+) ({_MINUS}?[\d,]+) ({_MINUS}?[\d,]+) ({_MINUS}?[\d,]+) ({_MINUS}?[\d,]+)$")


def _signed(text: str) -> float:
    return -parse_amount(text[1:]) if text[:1] in (_SOFT_HYPHEN, "-") else parse_amount(text)


def _date(day: str, month: str, closing: tuple[int, int]) -> str:
    """A `DD/MM` line date in the year that puts it on or before the closing date."""
    year, closing_month = closing
    return f"{year - 1 if int(month) > closing_month else year}-{month}-{day}"


def _kind(name: str, amount: float) -> str:
    if name.upper().startswith("PAYMENT"):
        return "payment"
    if amount < 0:
        return "credit"
    return "fee" if re.search(r"\bFEE\b", name, re.I) else "charge"


def parse(text: str) -> Statement:
    card, closing, total = _CARD.search(text), _CLOSING.search(text), None
    if not (card and closing):
        raise StatementParseError("CardX: card number or closing-date line not found")
    year = 2000 + int(closing.group(3))
    closing_ym = (year, int(closing.group(2)))

    prev = 0.0
    lines: list[StatementLine] = []
    inside = False
    for ln in (l.strip() for l in text.splitlines()):
        if (m := _PREV.match(ln)):
            prev, inside = _signed(m.group(1)), True
            continue
        if (m := _TOTAL.match(ln)):
            total = _signed(m.group(1))
            break
        if inside and (m := _LINE.match(ln)):
            name = m.group(5).replace(_SOFT_HYPHEN, "-")
            amount = parse_amount(m.group(7)) * (-1 if m.group(6) else 1)
            lines.append(StatementLine(date=_date(m.group(3), m.group(4), closing_ym), name=name, amount=amount,
                                       kind=_kind(name, amount), posted=_date(m.group(1), m.group(2), closing_ym)))
    if total is None:
        raise StatementParseError("CardX: no TOTAL BALANCE line")

    due_year = 2000 + int(closing.group(7))
    return Statement(
        issuer="CardX",
        statement_date=f"{year}-{closing.group(2)}-{closing.group(1)}",
        due_date=f"{due_year}-{closing.group(6)}-{closing.group(5)}",
        accounts=(CardAccount(product=card.group(2).strip(), total=total,
                              sections=(CardSection(card.group(1), prev, tuple(lines)),)),),
    )


class CardXParser(StatementParser):
    key = issuer = "CardX"
    signature = "CARDX CREDIT CARD STATEMENT"
    # CardX bills the principal and each supplement separately, one PDF per card
    # number, each with its own points (user, 2026-09-27; Nuta's own PDF, 2026-09-29).
    separate_card_statements = True
    # Points round per line, like the ledger formula: Sep 2026 printed 15 earned,
    # the rows give 15 one by one and 16 rounded once on the cycle's spend.
    # Credited per cycle (the default timing): Jun, Aug and Sep 2026 all reconcile.
    points_rounding = "line"

    def rewards(self, text: str, statement: Statement) -> tuple[RewardSummary, ...]:
        number = statement.accounts[0].sections[0].number
        lines = [l.strip() for l in text.splitlines()]
        for i, ln in enumerate(lines):
            if _POINTS_HEADER in ln and i + 1 < len(lines) and (m := _POINTS.match(lines[i + 1])):
                n = [_signed(g) for g in m.groups()]
                return (RewardSummary(number=number, program="CardX points", earned=n[1], bonus=n[2],
                                      adjusted=n[3], redeemed=n[4], outstanding=n[5]),)
        return ()

    def parse_text(self, text: str) -> Statement:
        return parse(text)
