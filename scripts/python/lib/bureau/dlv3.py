"""Krungsri First Choice DLV3 — "สั่งเดลิเวอรี่คุ้ม", delivery apps, 1 Sep – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.firstchoice.co.th/promotion/delivery-cashback on
2026-09-29. Pooled monthly spend in Grab, LINE MAN, Bolt, ShopeeFood and
Robinhood pays in steps; the bank's examples fix how the ladders meet: under
฿10,000 it pays ฿30 per whole ฿2,000 (at most 4, ฿120), from ฿10,000 it pays
฿200 per whole ฿10,000 instead (at most 2, ฿400). ฿8,800 earns ฿120 and
฿11,000 earns ฿200. The ฿1,600 campaign cap is 4 × ฿400, so it never binds on
its own. The page's points (1 per ฿25) and points-to-cashback offers aren't
tracked: the household keeps no First Choice points.

NW3 leaves delivery out because this campaign covers it.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import UNCERTAIN, Rule, Tx
from .ladder import LadderPromotion, Tranche

LOW_STEP, LOW_PAY, LOW_STEPS = Decimal(2_000), Decimal(30), 4
HIGH_FROM = HIGH_STEP = Decimal(10_000)
HIGH_PAY, HIGH_STEPS = Decimal(200), 2

# Everything in the Grab app counts (food, rides, mart, express), as do the other four.
_APPS = re.compile(r"GRAB|LINE ?MAN|LINEMAN|_LM_|\bLM\b|\bBOLT\b|SHOPEE ?FOOD|ROBINHOOD")


class DLV3Promotion(LadderPromotion):
    code = "DLV3"
    icon = "🛵"
    title = "สั่งเดลิเวอรี่คุ้ม"
    cards = ("First Choice",)
    campaign = (dt.date(2026, 9, 1), dt.date(2026, 12, 31))
    source_url = "https://www.firstchoice.co.th/promotion/delivery-cashback"
    headline = "1.5–2%"

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        if pooled < HIGH_FROM:
            steps = min(int(pooled // LOW_STEP), LOW_STEPS)
            return [Tranche(Decimal(0), steps * LOW_STEP, steps * LOW_PAY)] if steps else []
        steps = min(int(pooled // HIGH_STEP), HIGH_STEPS)
        return [Tranche(Decimal(0), steps * HIGH_STEP, steps * HIGH_PAY)]

    def qualifies(self, tx: Tx) -> bool:
        return bool(_APPS.search(tx.merchant))

    ladder_rows: ClassVar = (
        ("under ฿2,000", "nothing"),
        ("every whole ฿2,000, while under ฿10,000", "฿30 (1.5%) — up to ฿120"),
        ("every whole ฿10,000, from ฿10,000", "฿200 (2%) instead — up to ฿400, the monthly cap"),
    )
    examples: ClassVar = ((2_200, 30), (8_800, 120), (11_000, 200), (33_000, 400))
    inclusions: ClassVar = (
        "Full-amount baht spend in the Grab, LINE MAN, Bolt, ShopeeFood and Robinhood apps: food "
        "delivery, supermarket orders in the apps' marts, rides, parcels and messengers.",
        "Pooled per calendar month on the primary account (Takumi's); supplements count, and the "
        "bank credits the primary account only.",
        "The bank goes by the card network's MCC (Visa); spend outside the listed merchants' MCCs "
        "doesn't count.",
        "Counts from the day registration is confirmed (before or on the transaction date): UCHOOSE "
        "→ \"DLV3\", or SMS \"DLV3 <16-digit card no.>\" to 081-256-3333. Once for the campaign.",
    )
    rules: ClassVar = (
        Rule("Paid through a wallet (LINE Pay, TrueMoney …): the charge carries the wallet's MCC, "
             "not the app's", r"^LINEPAY\*|^LPTH\*|^TMN", level=UNCERTAIN,
             hint="the bank matches on the app's MCC; a wallet-routed charge may not carry it"),
        Rule("Installments: only full-amount spend counts",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Foreign-currency spend; interest, fees and penalties; charges cancelled later; spend "
             "on an overpaid balance or a temporary limit; digital assets",
             test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
    )
    crediting: ClassVar = (
        "Within 30 business days after each month-end, to the primary account.",
        "Caps: ฿400 a month and ฿1,600 for the campaign, per primary account.",
    )
