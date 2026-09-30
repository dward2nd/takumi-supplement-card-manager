"""Krungsri Card at Bangchak — the card's 1% (per cycle) and BC3P (per slip), 1 Jun – 30 Sep 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.krungsricard.com/th/promotion/bangchak on
2026-09-29, for Krungsri Visa Platinum, JCB Platinum and Lady Titanium
(Krungsri NOW is excluded). Two parts, both at Bangchak stations in Thailand
(BSRC-branded ones included: August's `CB12_BC3P` ฿24 on Baiboon's JCB came
from `BSRC-PHAAPOOM` ฿800):

  ต่อ 1 — the card's own benefit, no registration: "1%", paid as ฿8 per whole
          ฿800 of each slip, at most ฿32 per primary card account per statement
          cycle, credited within the cycle as `BANGCHAK SPECIAL DISCOUNT OF 1 %`.
          The bank's lines fix the per-slip reading: ฿800 → −฿8 (31 Aug) and
          ฿970 → −฿8, not ฿9.70 (14 Sep), on Baiboon's JCB. `BangchakCardBenefit`.
  ต่อ 2 — BC3P, registered in UCHOOSE: ฿24 per whole ฿800 on each slip, at
          most ฿48 per primary card account per calendar month, credited within
          30 days after the month as `CB12_BC3P CAMPAIGN 1AUG26-31AUG26`. `BC3PPromotion`.

Both withhold the card's normal points (as `KrungsriPetrolCampaign` already
does). Gas (LPG/NGV) stations and e-wallet payments don't count.
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

_BANGCHAK = re.compile(r"BANGCHAK|\bBSRC\b|BSRC-|บางจาก")
_NOT_FUEL = re.compile(r"\bGAS\b|LPG|NGV|INTHANIN|AMAZON")
_WALLET = r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*"
CAMPAIGN = (dt.date(2026, 6, 1), dt.date(2026, 9, 30))
SOURCE = "https://www.krungsricard.com/th/promotion/bangchak"


def _fuel(tx: Tx) -> bool:
    return bool(_BANGCHAK.search(tx.merchant)) and not _NOT_FUEL.search(tx.merchant)


_RULES = (
    Rule("Gas (LPG/NGV) stations; the station's shops", _NOT_FUEL.pattern),
    Rule("Paid through an e-wallet", _WALLET),
    Rule("Krungsri Consumer Installment Plan", test=lambda tx: promotions.is_installment(tx.name)),
)


class BangchakCardBenefit(SlipCreditPromotion):
    code = "Bangchak"
    icon = "⛽"
    title = "เติมเซฟกว่าเคย ตั้งแต่สลิปแรก ที่ปั๊มบางจาก — ต่อ 1 (สิทธิประโยชน์บัตร)"
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "1%"
    period_basis = "bill_cycle"
    cap = Decimal(32)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        steps = tx.amount // 800
        return steps * 8 if steps and _fuel(tx) and not promotions.is_installment(tx.name) else None

    ladder_title = "Cashback per slip"
    ladder_header = ("Bangchak fuel slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿800", "nothing"),
        ("every whole ฿800 on the slip, no registration", "฿8 (1%)"),
        ("Cap", "฿32 a statement cycle per primary card account"),
    )
    inclusions: ClassVar = (
        "Krungsri Visa Platinum, JCB Platinum and Lady Titanium; Krungsri NOW is excluded.",
        "Counted per statement cycle (Bill Cycle Date), supplements included; credited within the cycle.",
        "The card's normal points are withheld on the same spend.",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = ("Within the statement cycle, to the primary card account, as "
                           "`BANGCHAK SPECIAL DISCOUNT OF 1 %`.",)


class BC3PPromotion(SlipCreditPromotion):
    code = "BC3P"
    icon = "⛽"
    title = "เติมเซฟกว่าเคย ตั้งแต่สลิปแรก ที่ปั๊มบางจาก — ต่อ 2 พิเศษรับเพิ่ม"
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "3%"
    cap = Decimal(48)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        steps = tx.amount // 800
        return steps * 24 if steps and _fuel(tx) else None

    ladder_title = "Cashback per slip"
    ladder_header = ("Bangchak fuel slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿800", "nothing"),
        ("every whole ฿800 on the slip", "฿24 (3%)"),
        ("Cap", "฿48 a calendar month per primary card account"),
    )
    inclusions: ClassVar = (
        "Krungsri Visa Platinum, JCB Platinum and Lady Titanium; Krungsri NOW is excluded.",
        "Per slip: ฿1,599 earns ฿24, the same as ฿800. Slips never add up.",
        "Per calendar month, supplements included; register in UCHOOSE (\"BC3P\") before or on the "
        "transaction date.",
        "The card's normal points are withheld on the same spend.",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = (
        "Within 30 days after each month-end, to the primary card account, as "
        "`CB12_BC3P CAMPAIGN 1AUG26-31AUG26`.",
        "Not combinable with other promotions.",
    )


class BangchakKrungsriVISA(CardAccount, BangchakCardBenefit):
    cards = ("Krungsri VISA",)


class BangchakKrungsriJCB(CardAccount, BangchakCardBenefit):
    cards = ("Krungsri JCB",)


class BangchakKrungsriLady(CardAccount, BangchakCardBenefit):
    cards = ("Krungsri Lady",)


class BC3PKrungsriVISA(CardAccount, BC3PPromotion):
    cards = ("Krungsri VISA",)


class BC3PKrungsriJCB(CardAccount, BC3PPromotion):
    cards = ("Krungsri JCB",)


class BC3PKrungsriLady(CardAccount, BC3PPromotion):
    cards = ("Krungsri Lady",)


ACCOUNTS = (BangchakKrungsriVISA, BangchakKrungsriJCB, BangchakKrungsriLady,
            BC3PKrungsriVISA, BC3PKrungsriJCB, BC3PKrungsriLady)
