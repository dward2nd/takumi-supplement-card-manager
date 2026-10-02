"""Krungsri Card LOTA / LOTB — "ช้อปโลตัสเซฟ ง่ายขึ้น คุ้ม 3 ต่อ", per Lotus's slip, 1 Aug – 31 Oct 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.krungsricard.com/th/promotion/lotus-exclusive on
2026-10-01. Two registrations, both per slip at Lotus's, Lotus's Go Fresh and
lotuss.com, on every Krungsri card (NOW included):

  LOTA — ฿35 for a ฿1,500–4,999 slip, ฿150 for ฿5,000 or more; at most ฿150 a
         month per primary card account. Register before or on the day.
  LOTB — ฿450 for a single slip of ฿40,000 or more; at most ฿450 a month per
         primary card account, and only the first 1,800 qualifying accounts
         nationwide each month (UCHOOSE shows what's left). Register *before*
         the transaction.

They stack: a ฿40,000 slip earns ฿150 + ฿450. Combinable with other promotions.
Per card account (lib/bureau/accounts.py), like SUP1. The household's Lotus's
spend has gone on Lotus's Beyond, KTC and UOB cards, never Krungsri, so the
Bureau tracks LOTA from October 2026. LOTB isn't registered (user, 2026-10-01):
its classes have no Bureau rows.

Lotus's posts as `LOTUS'S <branch> …`; `TMN*LOTUS` / `TMN LOTUS HYPER` are
TrueMoney payments, which the bank excludes as e-wallet spend.
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

_LOTUSS = re.compile(r"LOTUS'?S|LOTUSS\.COM|LOTUS GO ?FRESH")
_WALLET = r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*|SHOPEEPAY"
CAMPAIGN = (dt.date(2026, 8, 1), dt.date(2026, 10, 31))
SOURCE = "https://www.krungsricard.com/th/promotion/lotus-exclusive"
TITLE = "ช้อปโลตัสเซฟ ง่ายขึ้น คุ้ม 3 ต่อ"

_RULES = (
    Rule("Paid through an e-wallet (TMN*LOTUS, TMN LOTUS HYPER …)", _WALLET),
    Rule("Krungsri Consumer Installment Plan", test=lambda tx: promotions.is_installment(tx.name)),
    Rule("Foreign currency and foreign exchange; interest, fees and penalties; charges cancelled, "
         "refunded or never billed", test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
)


def _lotuss(tx: Tx) -> bool:
    return bool(_LOTUSS.search(tx.merchant))


class LOTAPromotion(SlipCreditPromotion):
    code = "LOTA"
    icon = "🛒"
    title = f"{TITLE} — ต่อ 1"
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "3%"
    cap = Decimal(150)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _lotuss(tx) or tx.amount < 1_500:
            return None
        return Decimal(150) if tx.amount >= 5_000 else Decimal(35)

    ladder_title = "Cashback per slip"
    ladder_header = ("Lotus's slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿1,500", "nothing"),
        ("฿1,500 – 4,999", "฿35"),
        ("฿5,000 or more", "฿150"),
        ("Cap", "฿150 a month per primary card account"),
    )
    inclusions: ClassVar = (
        "Full-amount spend at every Lotus's and Lotus's Go Fresh and at lotuss.com, on every Krungsri "
        "card (Visa, Mastercard, JCB; NOW included).",
        "Per slip: slips never add up.",
        "Each primary card account has its own ฿150 a month: Krungsri VISA, JCB, Lady and NOW. "
        "Supplements count; the bank credits the primary account.",
        "Register once in UCHOOSE (\"LOTA\"), before or on the transaction date.",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = (
        "Within 30 days after each month-end, to the primary card account.",
        "Combinable with other promotions (LOTB, SUP1 …).",
    )


class LOTBPromotion(SlipCreditPromotion):
    code = "LOTB"
    icon = "🛒"
    title = f"{TITLE} — ต่อ 2 โบนัส"
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "฿450"
    cap = Decimal(450)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        return Decimal(450) if _lotuss(tx) and tx.amount >= 40_000 else None

    ladder_title = "Cashback per slip"
    ladder_header = ("Lotus's slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿40,000", "nothing"),
        ("฿40,000 or more", "฿450"),
        ("Cap", "฿450 a month per primary card account; the first 1,800 accounts nationwide each month"),
    )
    inclusions: ClassVar = (
        "Full-amount spend at every Lotus's and Lotus's Go Fresh and at lotuss.com, on every Krungsri "
        "card (NOW included).",
        "One slip of ฿40,000 or more; slips never add up.",
        "Only the first 1,800 qualifying accounts each month, first come, first served nationwide: check "
        "what's left in UCHOOSE before the purchase.",
        "Register once in UCHOOSE (\"LOTB\"), strictly before the transaction.",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = (
        "Within 30 days after each month-end, to the primary card account.",
        "Stacks with LOTA on the same slip.",
    )


class LOTAKrungsriVISA(CardAccount, LOTAPromotion):
    cards = ("Krungsri VISA",)


class LOTAKrungsriJCB(CardAccount, LOTAPromotion):
    cards = ("Krungsri JCB",)


class LOTAKrungsriLady(CardAccount, LOTAPromotion):
    cards = ("Krungsri Lady",)


class LOTAKrungsriNOW(CardAccount, LOTAPromotion):
    cards = ("Krungsri NOW",)


class LOTBKrungsriVISA(CardAccount, LOTBPromotion):
    cards = ("Krungsri VISA",)


class LOTBKrungsriJCB(CardAccount, LOTBPromotion):
    cards = ("Krungsri JCB",)


class LOTBKrungsriLady(CardAccount, LOTBPromotion):
    cards = ("Krungsri Lady",)


class LOTBKrungsriNOW(CardAccount, LOTBPromotion):
    cards = ("Krungsri NOW",)


ACCOUNTS = (LOTAKrungsriVISA, LOTAKrungsriJCB, LOTAKrungsriLady, LOTAKrungsriNOW,
            LOTBKrungsriVISA, LOTBKrungsriJCB, LOTBKrungsriLady, LOTBKrungsriNOW)
