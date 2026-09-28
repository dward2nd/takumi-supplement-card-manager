"""Krungsri Card PTT2 — "ยิ่งเติมยิ่งคุ้ม ที่พีทีที สเตชั่น", per PTT slip, 1 Jul – 31 Oct 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.krungsricard.com/th/promotion/ptt on 2026-09-29.
Each slip at a participating PTT Station earns on its own: ฿900–1,199 pays
฿30, ฿1,200 or more pays ฿60, capped at ฿90 a month per primary card account
(฿60 + ฿30, or three ฿30s).

Per card account (lib/bureau/accounts.py): Krungsri VISA, JCB, Lady and NOW
each have their own ฿90. The household fills up mostly at Bangchak, which
doesn't count.
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

_PTT = re.compile(r"\bPTT|PTTST|PTTOR")
_NOT_FUEL = re.compile(r"AMAZON|7-?ELEVEN|JIFFY")


class PTT2Promotion(SlipCreditPromotion):
    code = "PTT2"
    title = "ยิ่งเติมยิ่งคุ้ม ที่พีทีที สเตชั่น"
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 10, 31))
    source_url = "https://www.krungsricard.com/th/promotion/ptt"
    headline = "5%"
    cap = Decimal(90)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _PTT.search(tx.merchant) or tx.amount < 900:
            return None
        return Decimal(60) if tx.amount >= 1_200 else Decimal(30)

    ladder_title = "Cashback per slip"
    ladder_header = ("PTT Station slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿900", "nothing"),
        ("฿900 – 1,199", "฿30"),
        ("฿1,200 or more", "฿60"),
        ("Cap", "฿90 a month per primary card account"),
    )
    inclusions: ClassVar = (
        "Full-amount spend at participating PTT Stations in Thailand.",
        "Per slip: slips never add up.",
        "Each primary card account has its own ฿90 a month: Krungsri VISA, JCB, Lady and NOW. "
        "Supplements count; the bank credits the primary account.",
        "Register once in UCHOOSE (\"PTT2\"), before or on the transaction date.",
    )
    rules: ClassVar = (
        Rule("The station's shops (Café Amazon, 7-Eleven, Jiffy …)", _NOT_FUEL.pattern, level=UNCERTAIN,
             hint="the page names PTT Stations only; purchases other than fuel may not count"),
        Rule("Paid through an e-wallet", r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*"),
        Rule("Krungsri Consumer Installment Plan", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Foreign currency; interest, fees and penalties; charges cancelled or refunded",
             test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
    )
    crediting: ClassVar = (
        "Within 30 days after each month-end, to the primary card account.",
        "Not combinable with other promotions.",
    )


class PTT2KrungsriVISA(CardAccount, PTT2Promotion):
    cards = ("Krungsri VISA",)


class PTT2KrungsriJCB(CardAccount, PTT2Promotion):
    cards = ("Krungsri JCB",)


class PTT2KrungsriLady(CardAccount, PTT2Promotion):
    cards = ("Krungsri Lady",)


class PTT2KrungsriNOW(CardAccount, PTT2Promotion):
    cards = ("Krungsri NOW",)


ACCOUNTS = (PTT2KrungsriVISA, PTT2KrungsriJCB, PTT2KrungsriLady, PTT2KrungsriNOW)
