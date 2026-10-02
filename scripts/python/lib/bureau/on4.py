"""Krungsri First Choice ON4 — "เซฟทุกการช้อปออนไลน์ ได้คืนคุ้ม", Shopee / Lazada / TikTok, 1 Oct – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.firstchoice.co.th/promotion/online-shopping on
2026-10-01. ON3's successor with a lower entry step and a new top:

  ฿2,000–3,999 pooled in the month → ฿25; every whole ฿4,000 under ฿15,000 →
  ฿60 (at most 3, ฿180); from ฿15,000, ฿270 per whole ฿15,000 instead (at most
  7, ฿1,890); ฿150,000 adds ฿610, making the ฿2,500 monthly cap. The bank's
  examples fix the joins: ฿17,500 → ฿270, ฿120,000 → ฿1,890, ฿150,000 → ฿2,500.
  The ฿7,500 campaign cap is 3 × ฿2,500.

Travel agents and airlines sold through the apps now belong to TR3.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule
from .ladder import Tranche
from .on3 import ON3Promotion

ENTRY_FROM, ENTRY_PAY = Decimal(2_000), Decimal(25)
LOW_STEP, LOW_PAY, LOW_STEPS = Decimal(4_000), Decimal(60), 3
HIGH_FROM = HIGH_STEP = Decimal(15_000)
HIGH_PAY, HIGH_STEPS = Decimal(270), 7
BONUS_AT, BONUS = Decimal(150_000), Decimal(610)


class ON4Promotion(ON3Promotion):
    code = "ON4"
    title = "เซฟทุกการช้อปออนไลน์ ได้คืนคุ้ม"
    campaign = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
    source_url = "https://www.firstchoice.co.th/promotion/online-shopping"
    headline = "1.25–1.8%"

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        if pooled < ENTRY_FROM:
            return []
        if pooled < LOW_STEP:
            return [Tranche(Decimal(0), ENTRY_FROM, ENTRY_PAY)]
        if pooled < HIGH_FROM:
            steps = min(int(pooled // LOW_STEP), LOW_STEPS)
            return [Tranche(Decimal(0), steps * LOW_STEP, steps * LOW_PAY)]
        steps = min(int(pooled // HIGH_STEP), HIGH_STEPS)
        bands = [Tranche(Decimal(0), steps * HIGH_STEP, steps * HIGH_PAY)]
        if pooled >= BONUS_AT:
            # The bonus rewards the spend the capped ladder no longer pays for.
            bands.append(Tranche(steps * HIGH_STEP, BONUS_AT, BONUS))
        return bands

    ladder_rows: ClassVar = (
        ("under ฿2,000", "nothing"),
        ("฿2,000 – 3,999", "฿25 (1.25%)"),
        ("every whole ฿4,000, while under ฿15,000", "฿60 (1.5%) — up to ฿180"),
        ("every whole ฿15,000, from ฿15,000", "฿270 (1.8%) instead — up to ฿1,890, reached at ฿105,000"),
        ("฿150,000 or more", "+฿610 → ฿2,500, the monthly cap"),
    )
    examples: ClassVar = (
        (2_800, 25), (4_000, 60), (8_000, 120), (12_000, 180), (17_500, 270), (30_000, 540),
        (57_000, 810), (60_000, 1_080), (75_000, 1_350), (90_000, 1_620), (105_000, 1_890),
        (120_000, 1_890), (150_000, 2_500), (200_000, 2_500),
    )
    inclusions: ClassVar = (
        "Full-amount baht purchases through Shopee, Lazada and TikTok on the Krungsri First Choice Visa "
        "Platinum, pooled per calendar month on the primary account (Takumi's); supplements count, and "
        "the bank credits the primary account only.",
        "Steps, not a smooth rate: ฿17,500 earns ฿270, the same as ฿15,000, and the ฿4,000 steps stop "
        "counting once the ฿15,000 ladder takes over.",
        "Counts from the day registration is confirmed: UCHOOSE → \"ON4\", or SMS \"ON4 <16-digit card "
        "no.>\" to 081-256-3333. Once for the whole campaign.",
        "The bank classifies by the card network's merchant data (Visa).",
    )
    rules: ClassVar = (
        Rule("ShopeeFood (the DLV3 delivery campaign covers it)", r"SHOPEE ?FOOD"),
        Rule("Top-ups into ShopeePay or Lazada Wallet",
             test=lambda tx: promotions.looks_wallet_top_up(tx.merchant)),
        Rule("Installments: only full-amount spend counts",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Utility payments through the apps (MCC 4814, 4900, 9402)", r"\bBILL|TOPUP|MOBILE|INTERNET PAY"),
        Rule("Travel agents and airlines through the apps (TR3 covers them)",
             r"AIR ?ASIA|AIRWAYS|AIRLINES|NOK ?AIR|VIETJET|TRAVEL|AGODA|TRIP\.COM|TICKET"),
        Rule("Foreign-currency spend; interest, fees and penalties; charges cancelled later",
             test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
    )
    crediting: ClassVar = (
        "Within 30 business days after each month-end, to the primary account.",
        "A charge the merchant hasn't settled within 30 days of month-end doesn't count; a charge "
        "cancelled later is clawed back.",
        "Caps: ฿2,500 a month and ฿7,500 for the campaign, per primary account.",
    )
