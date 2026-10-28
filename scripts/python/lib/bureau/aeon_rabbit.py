"""AEON Rabbit Platinum cashback — 5% Rabbit/LINE Pay, 1% MRT Purple; ฿1,000 a statement cycle.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.aeon.co.th/aeon/cards/aeon-rabbit-platinum-card on
2026-09-29 (a standing card benefit): 5% on Rabbit Auto Top-up and on payments
through LINE Pay, 1% on MRT Purple Line card top-ups; at most ฿50 per
transaction, and ฿1,000 per primary card per statement cycle (11th – 10th),
supplements included. Credited within two cycles as `CASH BACK - CREDIT CARD
PROMOTION`.

Counted by transaction date, like NTW1 (`AEONTransactionDated`): the 2 Oct
2026 credit of ฿100.25 is 5% of the ฿2,005 dated 11 Aug – 10 Sep, not of the
฿2,015 billed on the 10 Sep statement (user, 2026-10-29). Its 2 Sep credit agrees:
฿75.96 for 11 Jul – 10 Aug, where the 10 Aug statement gives ฿73.20 (checked
2026-10-29 against every AEON statement on file). Each transaction's cashback is
rounded to the satang before it's summed (`line_credit`).

Which rows earn which rate comes from the card's promotion YAML
(`scripts/repositories/promotions/aeon-rabbit-cashback.yaml`); this adds the
two caps, which the YAML notes but can't enforce.
"""

from __future__ import annotations

import datetime as dt
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, ClassVar

from .. import promotions
from .aeon_cycle import AEONTransactionDated
from .base import SATANG, Rule, Tx, TxCredit
from .capped import CreditCapPromotion

PER_TX_CAP = Decimal(50)


class AEONRabbitCashback(AEONTransactionDated, CreditCapPromotion):
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
        # AEON rounds each transaction's cashback: its 2 Sep 2026 credit (฿75.96) holds two
        # ฿7.50 slips at ฿0.38 each, a satang over 5% of the period's total (2026-10-29).
        return min(rate * tx.amount, PER_TX_CAP).quantize(SATANG, rounding=ROUND_HALF_UP)

    def expected(self, r: TxCredit) -> dict[str, Any]:
        # `% cb` is the row's rate (or less, under the ฿50 cap), not its satang-rounded credit
        # over the amount, which reads 5.01% on a ฿40.50 slip.
        out = super().expected(r)
        if out.get("cashback_percent"):
            out["cashback_percent"] = (min(self.rate(r.tx) * r.tx.amount, PER_TX_CAP) / r.tx.amount).quantize(Decimal("0.0001"))
        return out

    ladder_title = "Cashback"
    ladder_header = ("Where", "Cashback")
    ladder_rows: ClassVar = (
        ("Rabbit Auto Top-up (฿300 a day); any payment through LINE Pay", "5%, at most ฿50 a transaction"),
        ("MRT Purple Line card top-up (Khlong Bang Phai – Tao Poon)", "1%, at most ฿50 a transaction"),
        ("Cap", "฿1,000 a statement cycle per primary card, supplements included"),
    )
    inclusions: ClassVar = (
        "Counted by transaction date, 11th – 10th, whatever statement the row bills on: the "
        "2 Oct 2026 credit (฿100.25) matches this to the satang.",
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
