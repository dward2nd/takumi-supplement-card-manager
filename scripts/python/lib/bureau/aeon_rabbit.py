"""AEON Rabbit Platinum cashback — 5% Rabbit/LINE Pay, 1% MRT Purple; ฿1,000 a statement cycle.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.aeon.co.th/aeon/cards/aeon-rabbit-platinum-card on
2026-09-29 (a standing card benefit): 5% on Rabbit Auto Top-up and on payments
through LINE Pay, 1% on MRT Purple Line card top-ups; at most ฿50 per
transaction, and ฿1,000 per primary card per statement cycle (11th – 10th),
supplements included. Credited within two cycles as `CASH BACK - CREDIT CARD
PROMOTION`.

Which rows earn which rate comes from the card's promotion YAML
(`scripts/repositories/promotions/aeon-rabbit-cashback.yaml`); this adds the
two caps, which the YAML notes but can't enforce.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .capped import CreditCapPromotion

PER_TX_CAP = Decimal(50)


class AEONRabbitCashback(CreditCapPromotion):
    code = "AEON Rabbit"
    icon = "🚆"
    name_pattern = r"\bAEON Rabbit cb 5%"
    title = "AEON Rabbit Platinum เครดิตเงินคืน"
    cards = ("AEON Rabbit",)
    campaign = (dt.date(2025, 1, 1), None)   # aeon-rabbit-cashback.yaml: standing
    source_url = "https://www.aeon.co.th/aeon/cards/aeon-rabbit-platinum-card"
    headline = "5%"
    period_basis = "bill_cycle"
    cap = Decimal(1_000)

    def rate(self, tx: Tx) -> Decimal | None:
        if promotions.looks_wallet_top_up(tx.merchant):
            return None
        c = promotions.classify(self.cards[0], tx.day, tx.name)
        return Decimal(str(c.cashback_percent)) if c.cashback_percent else None

    def line_credit(self, tx: Tx, rate: Decimal) -> Decimal:
        return min(rate * tx.amount, PER_TX_CAP)

    ladder_title = "Cashback"
    ladder_header = ("Where", "Cashback")
    ladder_rows: ClassVar = (
        ("Rabbit Auto Top-up (฿300 a day); any payment through LINE Pay", "5%, at most ฿50 a transaction"),
        ("MRT Purple Line card top-up (Khlong Bang Phai – Tao Poon)", "1%, at most ฿50 a transaction"),
        ("Cap", "฿1,000 a statement cycle per primary card, supplements included"),
    )
    inclusions: ClassVar = (
        "Counted per statement cycle, the 11th to the 10th: rows whose Bill Cycle Date is the "
        "cycle's close.",
        "No registration; the card must be activated before the spend.",
    )
    rules: ClassVar = (
        Rule("Top-ups into any digital wallet (easyBills, TrueMoney, ShopeePay …); vouchers and gift "
             "cards; digital assets", test=lambda tx: promotions.looks_wallet_top_up(tx.merchant)),
        Rule("Funds (MCC 6211), insurance (5960, 6300, 9223), utilities and recurring bills (4900), "
             "installments and loans, foreign exchange (6051, 4829), cash advances, interest, fees, "
             "penalties, taxes; cancelled or refunded charges; tax refunds are netted out"),
    )
    crediting: ClassVar = (
        "Within two statement cycles of the spend, to the primary card, as "
        "`CASH BACK - CREDIT CARD PROMOTION`.",
    )
