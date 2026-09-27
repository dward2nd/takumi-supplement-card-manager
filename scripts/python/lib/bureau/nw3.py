"""Krungsri First Choice NW3 — "แมตช์ทุกยอด คุ้มทุกการใช้", 1 Jul – 30 Sep 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.firstchoice.co.th/promotion/cashback-firstchoice
on 2026-09-28. The ladder pays per *whole* ฿10,000 of pooled monthly spend,
so ฿36,908.92 earns ฿600, the same as ฿30,000. The bank's ฿7,500 campaign
cap is exactly 3 × the ฿2,500 monthly cap, so it can never bind on its own
and isn't modelled.

The Bureau keeps one row per month (`2026M9 — NW3 cb 2%`). This class covers
all three months: the terms don't change between them.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import BasePromotion, Rule, Tranche

STEP = Decimal(10_000)
RATE = Decimal("0.02")
STEP_CAP = Decimal(100_000)    # 10 steps × ฿200 = the ฿2,000 ladder cap
BONUS_AT = Decimal(200_000)
BONUS = Decimal(500)

# Foreign-registered sites that bill in baht — the bank names these outright.
_FOREIGN_SITES = re.compile(r"AMAZON|GOOGLE|FACEBOOK|FACEBK|\bMETA\b")


def _foreign(tx) -> bool:
    return promotions.looks_foreign_in_thb(tx.merchant) or bool(_FOREIGN_SITES.search(tx.merchant))


class NW3Promotion(BasePromotion):
    code = "NW3"
    title = "แมตช์ทุกยอด คุ้มทุกการใช้"
    card = "First Choice"
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))
    source_url = "https://www.firstchoice.co.th/promotion/cashback-firstchoice"
    headline = "2%"

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        if pooled < 5_000:
            return []
        if pooled < STEP:
            return [Tranche(Decimal(0), Decimal(5_000), Decimal(50))]
        counted = min(pooled // STEP * STEP, STEP_CAP)
        bands = [Tranche(Decimal(0), counted, counted * RATE)]
        if pooled >= BONUS_AT:
            # The bonus rewards the spend the capped ladder no longer pays for.
            bands.append(Tranche(STEP_CAP, BONUS_AT, BONUS))
        return bands

    ladder_rows: ClassVar = (
        ("under ฿5,000", "nothing"),
        ("฿5,000 – 9,999", "฿50 flat"),
        ("every whole ฿10,000", "฿200 (2%) — up to ฿2,000, reached at ฿100,000"),
        ("฿200,000 or more", "+฿500 bonus → ฿2,500, the monthly cap"),
    )
    examples: ClassVar = (
        (4_900, 0), (5_000, 50), (8_000, 50), (10_000, 200), (30_000, 600),
        (120_000, 2_000), (200_000, 2_500),
    )
    inclusions: ClassVar = (
        "Full-amount (รูดเต็มจำนวน) purchases on the Krungsri First Choice Visa Platinum, "
        "pooled per calendar month on the primary account (Takumi's). The bank credits the "
        "primary account only.",
        "Steps, not a smooth 2%: ฿39,999 earns the same ฿600 as ฿30,000.",
        "Dated by the statement's transaction date, net of discounts. A charge the merchant "
        "hasn't settled within 30 days of month-end doesn't count.",
        "Counts only from the moment registration is confirmed: UCHOOSE app → search \"NW3\", "
        "or SMS \"NW3 <16-digit card no.>\" to 081-256-3333. NW2 members who spent over "
        "฿10,000 in both Apr and May 2026 were enrolled automatically.",
        "Everyday categories qualify: fuel, restaurants, home & furniture, supermarkets, "
        "department stores, fashion, skincare, hospitals, beauty clinics, sports, phones & "
        "computers.",
    )
    rules: ClassVar = (
        Rule("Installments (ผ่อน) — including 0% merchant plans on the personal-loan line",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Marketplaces: Shopee, Lazada, TikTok (the bank's ON3 campaign covers them)",
             r"SHOPEE(?! ?FOOD)|LAZADA|TIKTOK"),
        Rule("Food delivery: LINE MAN, ShopeeFood, Robinhood, Bolt, and everything in the Grab "
             "app (DLV2)", r"LINE ?MAN|SHOPEE ?FOOD|ROBINHOOD|\bBOLT\b|GRAB"),
        Rule("Travel: flights, hotels, travel agencies, car booking & rental, duty-free (TR2)",
             r"AGODA|BOOKING\.COM|EXPEDIA|TRAVELOKA|TRIP\.COM|CTRIP|AIR ?ASIA|AIRWAYS|AIRLINES|"
             r"NOK ?AIR|VIETJET|LION AIR|HOTEL|RESORT|AIRBNB|KING ?POWER|DUTY ?FREE|HERTZ|\bAVIS\b"),
        Rule("Insurance of any kind (IS3)", r"INSURANCE|ASSURANCE|\bAIA\b|\bFWD\b|ALLIANZ|ประกัน"),
        Rule("Supermarket charges of ฿10,001 or more each — Big C, Lotus's, Tops, Villa Market, "
             "Gourmet Market, Home Fresh Mart, MaxValu, Foodland, Makro, online stores included",
             r"BIG ?C\b|LOTUS|TOPS\b|VILLA|GOURMET|HOME FRESH|MAX ?VALU|FOODLAND|MAKRO|CP AXTRA",
             over=Decimal(10_000)),
        Rule("Fuel charges of ฿3,001 or more each", over=Decimal(3_000),
             test=lambda tx: promotions.looks_petrol(tx.merchant)),
        Rule("Utilities: electricity, water, landline (MCC 4900, 9402)",
             r"\b(MEA|PEA|MWA|PWA)\b|ELECTRICITY|WATERWORKS|การไฟฟ้า|การประปา"),
        Rule("Government bodies — taxes, state fees, some public hospitals (MCC 9399, 9405, "
             "7800) — and public organizations (องค์การมหาชน) such as Museum Siam",
             r"MUSEUM SIAM|REVENUE DEP|GOVERNMENT|MINISTRY|DEPARTMENT OF|กรม|องค์การ"),
        Rule("Gold and jewellery shops, e-wallet payments there included", r"\bGOLD\b|JEWEL|ทอง"),
        Rule("Financial services: funds (RMF/SSF), brokers, currency exchange, crypto & "
             "digital assets", r"\bFUND\b|\bRMF\b|\bSSF\b|SECURITIES|ASSET MANAGEMENT|BITKUB|"
             r"BINANCE|CRYPTO|SUPER ?RICH"),
        Rule("Spending abroad or in foreign currency, and baht charges from foreign-registered "
             "sites (Amazon, Google, Facebook, Agoda, Booking.com …)",
             test=_foreign),
        Rule("Recurring monthly or yearly auto-debits (subscriptions)",
             r"NETFLIX|SPOTIFY|YOUTUBE|DISNEY|\bHBO\b|ITUNES|APPLE\.COM|OPENAI|CHATGPT|CANVA|ADOBE"),
        Rule("Interest, fees and penalties; charges later cancelled or refunded",
             r"\bFEE\b|INTEREST|LATE CHARGE|PENALTY"),
        # Page-only: no merchant test. The app's NW3 eligible list for Sep 2026 counted
        # the household's TMN* card payments (฿6,465 of them, against a ฿105 gap), so
        # TrueMoney-routed payments are not what the bank means by a top-up.
        Rule("E-wallet top-ups (TrueMoney, Rabbit LINE Pay, ShopeePay …). Card payments made "
             "through TrueMoney (TMN*…) still count: the app's eligible list includes them"),
    )
    crediting: ClassVar = (
        "Within 30 business days after each month-end, as a statement line like "
        "เครดิตเงินคืน NW3_1JUL26-31JUL26.",
        "Taken back if a counted charge is later cancelled or refunded.",
        "Caps: ฿2,500 a month and ฿7,500 for the campaign, per primary account.",
    )
