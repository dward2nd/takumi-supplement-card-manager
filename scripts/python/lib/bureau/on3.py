"""Krungsri First Choice ON3 — "ช้อปออนไลน์ได้คืนคุ้ม", Shopee / Lazada / TikTok, 1 Jul – 30 Sep 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.firstchoice.co.th/promotion/shopping-online on
2026-09-29. Pooled monthly spend on the three marketplaces pays in steps, and
the bank's own examples fix how the two ladders meet: under ฿15,000 it pays
฿60 per whole ฿4,000 (at most 3); from ฿15,000 it pays ฿270 per whole ฿15,000
instead (at most 8), so ฿17,500 earns ฿270, not ฿270 + ฿60; ฿150,000 adds
฿340, making the ฿2,500 monthly cap. The ฿7,500 campaign cap is 3 × ฿2,500,
so it never binds on its own.

NW3 leaves these marketplaces out because ON3 covers them, so a First Choice
row is claimed by one campaign or the other, never both.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .ladder import LadderPromotion, Tranche

LOW_STEP, LOW_PAY, LOW_STEPS = Decimal(4_000), Decimal(60), 3
HIGH_FROM = HIGH_STEP = Decimal(15_000)
HIGH_PAY, HIGH_STEPS = Decimal(270), 8
BONUS_AT, BONUS = Decimal(150_000), Decimal(340)

_MARKETPLACE = re.compile(r"SHOPEE|LAZADA|TIKTOK")
_SHOPEE_FOOD = re.compile(r"SHOPEE ?FOOD")


class ON3Promotion(LadderPromotion):
    code = "ON3"
    title = "ช้อปออนไลน์ได้คืนคุ้ม"
    cards = ("First Choice",)
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))
    source_url = "https://www.firstchoice.co.th/promotion/shopping-online"
    headline = "1.5–1.8%"

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        if pooled < HIGH_FROM:
            steps = min(int(pooled // LOW_STEP), LOW_STEPS)
            return [Tranche(Decimal(0), steps * LOW_STEP, steps * LOW_PAY)] if steps else []
        steps = min(int(pooled // HIGH_STEP), HIGH_STEPS)
        bands = [Tranche(Decimal(0), steps * HIGH_STEP, steps * HIGH_PAY)]
        if pooled >= BONUS_AT:
            # The bonus rewards the spend the capped ladder no longer pays for.
            bands.append(Tranche(steps * HIGH_STEP, BONUS_AT, BONUS))
        return bands

    def qualifies(self, tx: Tx) -> bool:
        return bool(_MARKETPLACE.search(tx.merchant)) and not _SHOPEE_FOOD.search(tx.merchant)

    ladder_rows: ClassVar = (
        ("under ฿4,000", "nothing"),
        ("every whole ฿4,000, while under ฿15,000", "฿60 (1.5%) — up to ฿180"),
        ("every whole ฿15,000, from ฿15,000", "฿270 (1.8%) instead — up to ฿2,160, reached at ฿120,000"),
        ("฿150,000 or more", "+฿340 → ฿2,500, the monthly cap"),
    )
    examples: ClassVar = (
        (4_000, 60), (8_000, 120), (12_000, 180), (17_500, 270), (30_000, 540), (57_000, 810),
        (60_000, 1_080), (75_000, 1_350), (90_000, 1_620), (105_000, 1_890), (120_000, 2_160),
        (139_000, 2_160), (150_000, 2_500), (200_000, 2_500),
    )
    inclusions: ClassVar = (
        "Full-amount baht purchases through Shopee, Lazada and TikTok on the Krungsri First Choice "
        "Visa Platinum, pooled per calendar month on the primary account (Takumi's); supplements "
        "count, and the bank credits the primary account only.",
        "Steps, not a smooth rate: ฿17,500 earns ฿270, the same as ฿15,000, and the ฿4,000 steps "
        "stop counting once the ฿15,000 ladder takes over.",
        "Counts from the day registration is confirmed: UCHOOSE → \"ON3\", or SMS "
        "\"ON3 <16-digit card no.>\" to 081-256-3333. Once for the whole campaign.",
        "The bank classifies by the card network's merchant data (Visa).",
    )
    rules: ClassVar = (
        Rule("ShopeeFood (the DLV3 delivery campaign covers it)", r"SHOPEE ?FOOD"),
        Rule("Top-ups into ShopeePay or Lazada Wallet",
             test=lambda tx: promotions.looks_wallet_top_up(tx.merchant)),
        Rule("Installments: only full-amount spend counts",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Utility payments through the apps (MCC 4814, 4900, 9402)", r"\bBILL|TOPUP|MOBILE|INTERNET PAY"),
        Rule("Foreign-currency spend; interest, fees and penalties; charges cancelled later",
             test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
    )
    crediting: ClassVar = (
        "Within 30 business days after each month-end, to the primary account.",
        "A charge the merchant hasn't settled within 30 days of month-end doesn't count; a charge "
        "cancelled later is clawed back.",
        "Caps: ฿2,500 a month and ฿7,500 for the campaign, per primary account.",
    )
