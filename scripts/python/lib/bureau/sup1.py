"""Krungsri Card SUP1 — "ช้อปซูเปอร์มาร์ชั้นนำ", per supermarket slip, 1 Aug – 31 Oct 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.krungsricard.com/th/promotion/supermarket-shopping
on 2026-09-29. Each supermarket slip earns on its own: ฿1,500–3,999 pays ฿35,
฿4,000 or more pays ฿120, capped at ฿120 a month per primary card account; so
one slip of ฿4,000 fills the month. The household calls it "SUP1 3%"
(฿120 / ฿4,000).

Per card account (lib/bureau/accounts.py): Krungsri VISA, JCB, Lady and NOW
each have their own ฿120. September 2026 shows it: Baiboon's Makro PRO slips
of ฿4,045.50 (JCB), ฿4,064 (VISA), ฿4,159 (NOW) and ฿4,425 (Lady) each brought
a `CB15_ SUP1 CAMPAIGN 1SEP26-30SEP26` of ฿120. SUP2 (฿700 at ฿60,000 a
month) is a separate registration the household doesn't hold (user, 2026-09-29).
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .accounts import CardAccount
from .base import UNCERTAIN, Rule, Tx
from .slips import SlipCreditPromotion

# GO Wholesale posts as `CFW-<branch> …` (Central Food Wholesale), e.g. `CFW-CHIANGMAI 1 CHIANGMAI TH`.
_STORES = re.compile(r"BIG ?C\b|BIGC|\bTOPS\b|GOURMET|GO WHOLESALE|\bCFW-|MAKRO")
_MAKRO_IN_STORE = re.compile(r"^MAKRO_")


class SUP1Promotion(SlipCreditPromotion):
    code = "SUP1"
    icon = "🛒"
    title = "ช้อปซูเปอร์มาร์ชั้นนำ รับเครดิตเงินคืนสูงสุด 3%"
    campaign = (dt.date(2026, 8, 1), dt.date(2026, 10, 31))
    source_url = "https://www.krungsricard.com/th/promotion/supermarket-shopping"
    headline = "3%"
    cap = Decimal(120)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _STORES.search(tx.merchant) or tx.amount < 1_500:
            return None
        return Decimal(120) if tx.amount >= 4_000 else Decimal(35)

    ladder_title = "Cashback per slip"
    ladder_header = ("Supermarket slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿1,500", "nothing"),
        ("฿1,500 – 3,999", "฿35"),
        ("฿4,000 or more", "฿120"),
        ("Cap", "฿120 a month per primary card account"),
    )
    inclusions: ClassVar = (
        "Full-amount spend at Big C (every format, bigc.co.th), Tops (Food Hall, daily, online), "
        "Gourmet Market, Go Wholesale, Makro PRO, and Makro in store when paid by scanning with "
        "UCHOOSE — card, tap, QR or online.",
        "Per slip: slips never add up.",
        "Each primary card account has its own ฿120 a month: Krungsri VISA, JCB, Lady and NOW. "
        "Supplements count; the bank credits the primary account.",
        "Register once in UCHOOSE (\"SUP1\"), before or on the transaction date.",
    )
    rules: ClassVar = (
        Rule("Makro in store paid other than by UCHOOSE scan", _MAKRO_IN_STORE.pattern, level=UNCERTAIN,
             hint="in-store Makro counts only when paid through UCHOOSE; the merchant string can't show it"),
        Rule("Paid through an e-wallet (TMN …)", r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*|SHOPEEPAY"),
        Rule("Krungsri Consumer Installment Plan", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Foreign currency and foreign exchange; interest, fees and penalties; charges cancelled, "
             "refunded or never billed", test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
    )
    crediting: ClassVar = (
        "Within 30 days after the month-end — in practice within days of the slip, as "
        "`CB15_ SUP1 CAMPAIGN 1SEP26-30SEP26`.",
        "Combinable with other promotions.",
    )


class SUP1KrungsriVISA(CardAccount, SUP1Promotion):
    cards = ("Krungsri VISA",)


class SUP1KrungsriJCB(CardAccount, SUP1Promotion):
    cards = ("Krungsri JCB",)


class SUP1KrungsriLady(CardAccount, SUP1Promotion):
    cards = ("Krungsri Lady",)


class SUP1KrungsriNOW(CardAccount, SUP1Promotion):
    cards = ("Krungsri NOW",)


ACCOUNTS = (SUP1KrungsriVISA, SUP1KrungsriJCB, SUP1KrungsriLady, SUP1KrungsriNOW)
