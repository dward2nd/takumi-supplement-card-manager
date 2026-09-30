"""Krungsri Card ONQ3 — "สายช้อปออนไลน์ ช้อปคุ้มมีคืน", online shops and wallets, 7 Aug – 30 Nov 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.krungsricard.com/th/promotion/online-shopping-cashback
on 2026-09-29. Pooled monthly spend at Lazada, Shopee, TikTok Shop, LINE
SHOPPING and through TrueMoney, LINE Pay and ShopeePay pays one fixed amount
for the highest band reached: ฿40 from ฿3,000, ฿170 from ฿15,000, ฿350 from
฿30,000. The bands replace each other; nothing repeats. Capped at ฿350 a month
and ฿1,400 for the campaign (4 × ฿350) per primary card account.

Per card account (lib/bureau/accounts.py): Krungsri VISA, JCB and Lady each
have their own quota. Krungsri NOW is excluded by the bank. Krungsri keeps
`% cb` unset on its rows, so this campaign writes the Bureau and the trackers
only.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .accounts import CardAccount
from .base import UNCERTAIN, Rule, Tx
from .ladder import LadderPromotion, Tranche

BANDS = ((Decimal(30_000), Decimal(350)), (Decimal(15_000), Decimal(170)), (Decimal(3_000), Decimal(40)))

_ONLINE = re.compile(r"LAZADA|SHOPEE|TIKTOK|LINE SHOPPING|^TMN[ *]|TRUE ?MONEY|LINE ?PAY|^LPTH\*")
_DELIVERY = re.compile(r"GRAB|LINE ?MAN|_LM_|PF_LM|SHOPEE ?FOOD|ROBINHOOD|\bBOLT\b")


class ONQ3Promotion(LadderPromotion):
    code = "ONQ3"
    icon = "🛍️"
    title = "สายช้อปออนไลน์ ช้อปคุ้มมีคืน"
    campaign = (dt.date(2026, 8, 7), dt.date(2026, 11, 30))
    source_url = "https://www.krungsricard.com/th/promotion/online-shopping-cashback"
    headline = "฿40/170/350"
    marks_rows = False   # Krungsri rows keep `% cb` unset; the money is in the trackers

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        for reach, pay in BANDS:
            if pooled >= reach:
                return [Tranche(Decimal(0), reach, pay)]
        return []

    def qualifies(self, tx: Tx) -> bool:
        return bool(_ONLINE.search(tx.merchant)) and not _DELIVERY.search(tx.merchant)

    ladder_rows: ClassVar = (
        ("under ฿3,000", "nothing"),
        ("฿3,000 – 14,999", "฿40"),
        ("฿15,000 – 29,999", "฿170"),
        ("฿30,000 or more", "฿350 — the monthly cap"),
    )
    examples: ClassVar = ((2_999, 0), (3_000, 40), (14_999, 40), (15_000, 170), (29_999, 170),
                          (30_000, 350), (90_000, 350))
    inclusions: ClassVar = (
        "Full-amount baht spend at Lazada, Shopee, TikTok Shop and LINE SHOPPING, and card payments "
        "through TrueMoney, LINE Pay and ShopeePay.",
        "One amount for the month's highest band; the bands replace each other and never repeat.",
        "Pooled per calendar month (transaction date on the statement) on each primary card account: "
        "Krungsri VISA, JCB and Lady are three separate quotas. Supplements count; the bank credits "
        "the primary account.",
        "Counts from the day registration is confirmed, before or on the transaction date: UCHOOSE "
        "→ \"ONQ3\", once for the campaign.",
    )
    rules: ClassVar = (
        Rule("Delivery apps paid through a wallet: Grab, LINE MAN, ShopeeFood …", _DELIVERY.pattern),
        Rule("Public transport and tolls (MCC 4111, 4112, 4131, 4784): BTS, MRT, expressways, "
             "EASY PASS top-ups, Nakhonchai Air, LALAMOVE; cash on delivery",
             test=lambda tx: promotions.looks_transport_or_toll(tx.merchant)),
        Rule("Utilities (MCC 4900); easyBills, easyBills+, Samsung Pay", r"EASY ?BILLS|SAMSUNG ?PAY|"
             r"\b(MEA|PEA|MWA|PWA)\b"),
        Rule("Top-ups into a wallet", test=lambda tx: promotions.looks_wallet_top_up(tx.merchant),
             level=UNCERTAIN, hint="the page counts card payments through the wallets; a top-up is unclear"),
        Rule("Krungsri Consumer Installment Plan", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Foreign currency and foreign exchange; digital assets; interest, fees and penalties; "
             "charges cancelled, refunded or never billed",
             test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
    )
    crediting: ClassVar = (
        "Within 90 days after each month-end, to the primary card account.",
        "Caps: ฿350 a month and ฿1,400 for the campaign, per primary card account.",
        "Not combinable with other promotions.",
    )


class ONQ3KrungsriVISA(CardAccount, ONQ3Promotion):
    cards = ("Krungsri VISA",)


class ONQ3KrungsriJCB(CardAccount, ONQ3Promotion):
    cards = ("Krungsri JCB",)


class ONQ3KrungsriLady(CardAccount, ONQ3Promotion):
    cards = ("Krungsri Lady",)


ACCOUNTS = (ONQ3KrungsriVISA, ONQ3KrungsriJCB, ONQ3KrungsriLady)
