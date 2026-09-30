"""Krungsri JCB J Dining — 3% per whole ฿1,000 on restaurant slips worldwide, 1 Jan – 30 Sep 2026.

deterministic + idempotent — declarations and pure functions only.

Terms (user, 2026-09-29; https://www.krungsricard.com/th/product/creditcard/krungsri-jcb):
"รับเครดิตเงินคืน 3% เมื่อมียอดใช้จ่ายครบทุก 1,000 บาท/เซลล์สลิป ณ ร้านอาหารทั่วโลก" —
per slip, ฿30 for every whole ฿1,000, at restaurants anywhere in the world
(MCC 5811, 5812, 5813, 5814, 5462, 5820; not hotel restaurants), at most ฿150
a month per primary card account. Supplements count; credited within 60 days —
in practice a `CB <restaurant>` line days later (Baiboon's SUSHIRO ฿1,342 →
`CB SUSHIRO GH(TH)C.CHIANGMAI BANGKOK` −฿30, Sep 2026).

Restaurants can't always be told from the merchant string, so only the names
below are linked automatically; a row linked by hand counts too.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .accounts import CardAccount
from .base import Rule, Tx
from .slips import SlipCreditPromotion

STEP, PER_STEP = Decimal(1_000), Decimal(30)

_RESTAURANT = re.compile(
    r"SUSHI|SHABU|HAI ?DI ?LAO|\bMK\b|BAR ?B ?Q|RESTAURANT|RESTAURAN\b|KITCHEN|GRILL|BISTRO|PIZZA|BURGER|"
    r"STEAK|DIM ?SUM|DUMPLING|NOODLE|RAMEN|YAKINIKU|IZAKAYA|BUFFET|EATERY|DINING|BAKERY|CAFE\b|COFFEE|"
    r"STARBUCKS|AMAZON|SWENSEN|MCDONALD|\bKFC\b|BURGER KING|PIZZA|FUJI|ZEN\b|OISHI|SIZZLER|YAYOI|"
    r"AFTER YOU|TIM HORTONS|KRISPY|DAIRY QUEEN|MOOYIM|หมูกระทะ|ร้านอาหาร|ภัตตาคาร")
_NOT_RESTAURANT = re.compile(r"GRAB|LINE ?MAN|_LM_|SHOPEE ?FOOD|FOODLAND|FOOD ?HALL|HOTEL|RESORT")


class JDiningPromotion(SlipCreditPromotion):
    code = "J Dining"
    icon = "🍽️"
    title = "Krungsri JCB — เครดิตเงินคืน 3% ร้านอาหารทั่วโลก"
    campaign = (dt.date(2026, 1, 1), dt.date(2026, 9, 30))
    source_url = "https://www.krungsricard.com/th/product/creditcard/krungsri-jcb"
    headline = "3%"
    cap = Decimal(150)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        steps = tx.amount // STEP
        return steps * PER_STEP if steps else None

    def qualifies(self, tx: Tx) -> bool:
        return self.slip_credit(tx) is not None and bool(_RESTAURANT.search(tx.merchant)) \
            and not _NOT_RESTAURANT.search(tx.merchant)

    def counts_linked(self, tx: Tx) -> bool:
        return self.slip_credit(tx) is not None   # a restaurant the household linked by hand counts

    ladder_title = "Cashback per slip"
    ladder_header = ("Restaurant slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿1,000", "nothing"),
        ("every whole ฿1,000 on the slip", "฿30 (3%)"),
        ("Cap", "฿150 a month per primary card account"),
    )
    inclusions: ClassVar = (
        "Restaurants anywhere in the world (MCC 5811, 5812, 5813, 5814, 5462, 5820), hotel "
        "restaurants excepted, on the Krungsri JCB Platinum.",
        "Per slip: ฿1,999 earns ฿30, the same as ฿1,000. Slips never add up.",
        "Supplements count toward the primary account (Takumi's), which the bank credits.",
        "No registration.",
        "Only well-known restaurant names are linked automatically; link any other restaurant slip "
        "by hand and it counts.",
    )
    rules: ClassVar = (
        Rule("Restaurants inside hotels", r"HOTEL|RESORT"),
        Rule("Delivery apps (their MCC isn't a restaurant's)", r"GRAB|LINE ?MAN|_LM_|SHOPEE ?FOOD"),
        Rule("Installments", test=lambda tx: promotions.is_installment(tx.name)),
    )
    crediting: ClassVar = (
        "Within 60 days of the transaction, to the primary account — in practice a `CB <restaurant>` "
        "line a few days later.",
    )


class JDiningKrungsriJCB(CardAccount, JDiningPromotion):
    cards = ("Krungsri JCB",)


ACCOUNTS = (JDiningKrungsriJCB,)
