"""ttb so smart 1% — a card benefit capped at ฿2,000 a statement cycle per card account.

deterministic + idempotent — declarations and pure functions only.

Terms from the bank (user, 2026-09-29; https://www.ttbbank.com/th/personal/credit-cards/card-type/ttb-so-smart):
1% on every card purchase, credited into a ttb no fixed savings account, "สูงสุด
2,000 บาท/บัญชีบัตร/รอบบัญชี". Takumi's primary (…7368) and Baiboon's
supplement (…0864) are one card account, so they share the ฿2,000.

Which rows earn 1% comes from the card's promotion YAML
(`scripts/repositories/promotions/ttb-so-smart-cashback.yaml`, through
`lib.promotions.classify`), as /add-transaction writes it; the bank's
exclusions the YAML can't see are rules here. This adds the cap.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import Any, ClassVar

from .. import promotions
from .base import Rule, Tx, TxCredit
from .capped import CreditCapPromotion

RATE = Decimal("0.01")

_EXCLUDED = re.compile(
    r"^TMN[ *]|TRUE ?MONEY|7-?ELEVEN|7-11|INSURANCE|ASSURANCE|\bAIA\b|\bFWD\b|ประกัน|\bFUND\b|"
    r"\bRMF\b|\bSSF\b|\bTAX\b|REVENUE|\b(MEA|PEA|MWA|PWA)\b|ELECTRICITY|WATERWORKS|SUPER ?RICH|"
    r"EXCHANGE|\bFEE\b|INTEREST|CASH ADVANCE|PENALTY")
_CHINA_EEA = re.compile(r"\b(CHN|CN|DEU|DE|FRA|FR|ITA|IT|ESP|ES|NLD|NL|BEL|BE|AUT|AT|IRL|IE|PRT|PT|"
                        r"GRC|GR|FIN|FI|SWE|SE|DNK|DK|POL|PL|CZE|CZ|HUN|HU|ROU|RO|BGR|BG|HRV|HR|SVK|SK|"
                        r"SVN|SI|LTU|LT|LVA|LV|EST|EE|LUX|LU|MLT|MT|CYP|CY|NOR|NO|ISL|IS|LIE|LI|GBR|GB)$")


class TTBSoSmartCashback(CreditCapPromotion):
    code = "ttb so smart"
    name_pattern = r"\bttb so smart cb 1%"
    title = "ttb so smart เครดิตเงินคืน 1%"
    cards = ("ttb so smart",)
    campaign = (dt.date(2026, 1, 1), None)   # ttb-so-smart-cashback.yaml: standing
    source_url = "https://www.ttbbank.com/th/personal/credit-cards/card-type/ttb-so-smart"
    headline = "1%"
    period_basis = "bill_cycle"
    cap = Decimal(2_000)

    def rate(self, tx: Tx) -> Decimal | None:
        if _EXCLUDED.search(tx.merchant) or _CHINA_EEA.search(tx.merchant) \
                or promotions.looks_petrol(tx.merchant) or promotions.looks_transport_or_toll(tx.merchant):
            return None
        c = promotions.classify(self.cards[0], tx.day, tx.name)
        return RATE if c.cashback_percent and Decimal(str(c.cashback_percent)) == RATE else None

    def expected(self, r: TxCredit) -> dict[str, Any]:
        """Inside the ฿2,000: 1%. The row the cap runs out on, and every row past it, unset."""
        return {"cashback_percent": RATE if r.counted == r.tx.amount and r.credit > 0 else None}

    ladder_title = "Cashback"
    ladder_header = ("Spend in the statement cycle", "Cashback")
    ladder_rows: ClassVar = (
        ("Every card purchase that isn't excluded", "1%"),
        ("Cap", "฿2,000 a statement cycle per card account (Takumi's card and Baiboon's supplement together)"),
    )
    inclusions: ClassVar = (
        "Counted per statement cycle: rows whose Bill Cycle Date is the cycle's close (the 27th).",
        "Credited into a ttb no fixed savings account, not onto the card.",
    )
    rules: ClassVar = (
        Rule("7-Eleven and TrueMoney Wallet", r"^TMN[ *]|TRUE ?MONEY|7-?ELEVEN|7-11"),
        Rule("Petrol stations of every kind", test=lambda tx: promotions.looks_petrol(tx.merchant)),
        Rule("Public transport of every kind", test=lambda tx: promotions.looks_transport_or_toll(tx.merchant)),
        Rule("Utilities (MCC 4900, since 15 Jan 2026) and taxes",
             r"\b(MEA|PEA|MWA|PWA)\b|ELECTRICITY|WATERWORKS|\bTAX\b|REVENUE"),
        Rule("Insurance premiums of every kind, unit-linked life insurance, funds of every kind",
             r"INSURANCE|ASSURANCE|\bAIA\b|\bFWD\b|ประกัน|\bFUND\b|\bRMF\b|\bSSF\b"),
        Rule("Merchants registered in China (not Hong Kong or Macau) or the EEA and the UK, in any "
             "currency", _CHINA_EEA.pattern),
        Rule("Foreign-registered merchants charging in baht",
             test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
        Rule("ttb so goood split payments, pay plan installments at the merchant, cash chill chill",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Cash advances, cash transfers, currency exchange, interest, penalties and fees, "
             "cancelled charges, business spend", r"SUPER ?RICH|EXCHANGE|\bFEE\b|INTEREST|CASH ADVANCE|PENALTY"),
    )
    crediting: ClassVar = (
        "Into the ttb no fixed account linked to the card, per statement cycle.",
    )
