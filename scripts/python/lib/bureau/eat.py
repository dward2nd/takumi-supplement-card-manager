"""Krungsri Card EAT — "อิ่มคุ้มฟิน เปิดโหมดพร้อมกิน", participating restaurants, 1 Jul – 31 Oct 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.krungsricard.com/th/promotion/dining-cashback-deal
(and its restaurant list, dining-benefit-2.pdf) on 2026-09-29. Registered in
UCHOOSE under "EAT"; the household calls it "DN 10%", after the statement line
`CB22_EAT_10MASS DN 1JUL26-31OCT26`. Per primary card account and calendar
month: the first slip of ฿1,000 or more at a participating restaurant earns
฿100, and a third such slip earns another ฿100 — ฿200 at most. Each part is
capped at ฿400 for the campaign (4 months × ฿100), so it never binds alone.

Per card account (lib/bureau/accounts.py): Krungsri VISA, JCB, Lady and NOW.
Only the best-known names on the 137-restaurant list are linked automatically;
a slip at another listed restaurant, linked by hand, counts too. The page's
"DN" points redemption (1,000 points → ฿100) isn't tracked.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .accounts import CardAccount
from .base import Rule, Tx
from .slip_count import SlipCountPromotion

MIN_SLIP = Decimal(1_000)

_LISTED = re.compile(
    r"SUSHIRO|\bMK\b|OISHI|PEPPER LUNCH|\bS ?& ?P\b|SHABUSHI|SIZZLER|SUSHI ?EXPRESS|SUSHI ?PLUS|PIZZA COMPANY|"
    r"YAYOI|YOSHINOYA|AFTER YOU|DIN TAI FUNG|GREYHOUND|COCO ICHIBANYA|OOTOYA|SANTOUKA|KATSUYA|TONKATSU|"
    r"SALAD FACTORY|SOMBOON|LONG JOHN|CHEESECAKE FACTORY|WINE CONNECTION|JUMBO SEAFOOD|SUKI MASA|SUSHI MASA|"
    r"MARUMOMO|KIWAMIYA|BINCHO|TSUDOI|DAISEN|CANTON PARADISE|BOON TONG KEE|SONGFA|GINGER FARM|DIMM\b|"
    r"HOUSE OF EMILY|PIZZA MARU|HITORI|CYU\b|SABOTEN|SEKI\b|SMIZZLE|NAM NAM|PHED PHED|SALAD STOP|"
    r"MAGURO|KATSUSHIN|KATSU MIDORI|TOMITA|OZAWA|AKIMITSU|DOMO YAKINIKU|GIANTS YAKINIKU|GRILL YAMAYA|"
    r"TEMPURA YAMAYA|BOTTOMLESS|WOLFGANG|YUANYEE|CHOKDEE|KAM'?S ROAST|BANANA LEAF|HONG BAO|BA HAO")
_EXCLUDED = re.compile(r"FOODPANDA|GRAB|LINE ?MAN|_LM_|ROBINHOOD|SHOPEE ?FOOD|^TMN[ *]|TRUE ?MONEY|"
                       r"^LINEPAY\*|^LPTH\*|SHOPEEPAY|GB ?PRIME")


class EATPromotion(SlipCountPromotion):
    code = "EAT"
    icon = "🍽️"
    title = "อิ่มคุ้มฟิน เปิดโหมดพร้อมกิน"
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 10, 31))
    source_url = "https://www.krungsricard.com/th/promotion/dining-cashback-deal"
    headline = "฿100+100"
    milestones: ClassVar = {1: Decimal(100), 3: Decimal(100)}

    def qualifies(self, tx: Tx) -> bool:
        return tx.amount >= MIN_SLIP and bool(_LISTED.search(tx.merchant)) and not _EXCLUDED.search(tx.merchant)

    def counts_linked(self, tx: Tx) -> bool:
        return tx.amount >= MIN_SLIP   # a listed restaurant the household linked by hand counts

    ladder_title = "Cashback per month"
    ladder_header = ("Slips of ฿1,000+ at participating restaurants", "Cashback")
    ladder_rows: ClassVar = (
        ("the month's first", "฿100"),
        ("the month's third", "+฿100"),
        ("Cap", "฿200 a month per primary card account; ฿400 per part for the campaign"),
    )
    inclusions: ClassVar = (
        "Participating restaurants only (137 on the bank's list: Sushiro, MK, Oishi, Shabushi, Sizzler, "
        "Pepper Lunch, S&P, Yayoi, Yoshinoya, The Pizza Company …), restaurant MCCs 5811, 5812, 5813, "
        "5814, 5462, 5820, 5460, 5841.",
        "Per primary card account and calendar month: Krungsri VISA, JCB, Lady and NOW each count "
        "their own slips. Supplements count; the bank credits the primary account.",
        "Register in UCHOOSE (\"EAT\"), before or on the transaction date.",
        "Only well-known names are linked automatically; link a slip at another listed restaurant "
        "by hand and it counts.",
    )
    rules: ClassVar = (
        Rule("Orders through Foodpanda, GrabFood, LINE MAN, Robinhood or ShopeeFood, and payments "
             "through any e-wallet (TrueMoney, LINE Pay, ShopeePay, GB Prime Pay)", _EXCLUDED.pattern),
    )
    crediting: ClassVar = (
        "Within 30 days after each month-end, to the primary card account, as "
        "`CB22_EAT_10MASS DN 1JUL26-31OCT26`.",
    )


class EATKrungsriVISA(CardAccount, EATPromotion):
    cards = ("Krungsri VISA",)


class EATKrungsriJCB(CardAccount, EATPromotion):
    cards = ("Krungsri JCB",)


class EATKrungsriLady(CardAccount, EATPromotion):
    cards = ("Krungsri Lady",)


class EATKrungsriNOW(CardAccount, EATPromotion):
    cards = ("Krungsri NOW",)


ACCOUNTS = (EATKrungsriVISA, EATKrungsriJCB, EATKrungsriLady, EATKrungsriNOW)
