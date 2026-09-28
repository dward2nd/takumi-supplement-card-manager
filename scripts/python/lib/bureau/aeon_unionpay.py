"""AEON UnionPay Platinum cashback — 3% in China, Hong Kong, Macau and Taiwan currencies.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.aeon.co.th/aeon/cards/aeon-unionpay-platinum-card on
2026-09-29 (a standing card benefit): 3% on spend in CNY, HKD, MOP or TWD only,
on the baht amount after conversion; at most ฿2,500 per primary card per
statement cycle (฿30,000 a year), supplements included. Credited within 90 days
of the statement date (the 10th).

The household marks these rows `% cb` 3% by hand (Nuta's Alipay rows); the
original currency sits in the Note (`Original charge 600 CNY.`). This adds the
cap.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .capped import CreditCapPromotion

RATE = Decimal("0.03")
_CURRENCY = re.compile(r"\b(CNY|RMB|HKD|MOP|TWD|NTD)\b")
_COUNTRY = re.compile(r"\b(CHN|HKG|MAC|TWN)$")


class AEONUnionPayCashback(CreditCapPromotion):
    code = "AEON UnionPay"
    name_pattern = r"\bAEON UnionPay cb 3%"
    title = "AEON-UnionPay Platinum เครดิตเงินคืน 3% จีน ฮ่องกง มาเก๊า ไต้หวัน"
    cards = ("AEON UnionPay",)
    campaign = (dt.date(2025, 1, 1), None)   # a standing card benefit
    source_url = "https://www.aeon.co.th/aeon/cards/aeon-unionpay-platinum-card"
    headline = "3%"
    period_basis = "bill_cycle"
    cap = Decimal(2_500)

    def rate(self, tx: Tx) -> Decimal | None:
        if promotions.is_installment(tx.name):
            return None
        return RATE if _CURRENCY.search(tx.note.upper()) or _COUNTRY.search(tx.merchant) else None

    ladder_title = "Cashback"
    ladder_header = ("Spend", "Cashback")
    ladder_rows: ClassVar = (
        ("In CNY (China), HKD (Hong Kong), MOP (Macau) or TWD (Taiwan)", "3%"),
        ("Cap", "฿2,500 a statement cycle per primary card (฿30,000 a year), supplements included"),
    )
    inclusions: ClassVar = (
        "Counted per statement cycle (the 10th): rows whose Bill Cycle Date is the cycle's close.",
        "The base is the baht amount after conversion. No registration.",
        "A row counts when its Note gives one of the four currencies, or its merchant string ends in "
        "CHN, HKG, MAC or TWN.",
    )
    rules: ClassVar = (
        Rule("Installments, loans and hire purchase", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Funds and insurance (MCC 6211, 6300), foreign exchange (6051, 4829), cash advances, "
             "interest, fees, penalties, taxes; cancelled or refunded charges"),
    )
    crediting: ClassVar = (
        "Within 90 days of the statement date (the 10th), to the primary card, as "
        "`CASH BACK - CREDIT CARD PROMOTION`.",
        "Can't combine with other promotions.",
    )
