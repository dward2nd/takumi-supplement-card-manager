"""UOB Makro 26th anniversary "Gold Mission" (MPW823, SMS `UMK26`), 1 Oct – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read on 2026-10-03 from the rendered
https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/makro-26th-mpw823-1226.page
(no `.json` twin). UOB Makro cardholders only, registered once by SMS `UMK26 <last 12 digits>`
to 4545111 or Rewards+ in UOB TMRW (Takumi registered on 2026-10-03). Every
cap is per cardholder, principal and supplements together, so Takumi's and
Baiboon's UOB Makro rows pool. Three quotas, one Bureau row each:

  UMK26-1 — Makro stores, every branch: the month's total pays one band,
            ฿150 from ฿50,000, ฿800 from ฿150,000, ฿2,500 from ฿400,000.
            ฿7,500 for the campaign (3 × ฿2,500, never binding alone).
            `UOBMakroStoreMission`, one row per month.
  UMK26-2 — Makro PRO, in the app only, per slip: ฿150 for ฿10,000–29,999,
            ฿500 for ฿30,000–59,999, ฿1,200 from ฿60,000; ฿3,600 for the
            whole campaign. `UOBMakroProMission`, one row for the campaign.
  UMK26-3 — other spend ("หมวดอื่นๆ"): ฿300 for a month of ฿10,000 or more,
            ฿900 for the campaign (never binding alone). `UOBMakroOtherMission`,
            one row per month.

Doing all three at least once during the campaign adds a ฿1,000 Makro voucher,
and every ฿1,000 on the card is a right in a gold-bar draw: neither is money in
the card account, so neither is tracked here. Credited within 60 days after
31 Dec. Not combinable with other promotions.

UOB lists hypermarkets and supermarkets (MCC 5411) among the spend it doesn't
count, in a list shared by all three missions and the draw. Missions 1 and 2
name Makro and Makro PRO outright, so the exclusion is read as applying to
mission 3 and the draw (a reading; `HTTPS://WWW.MAKRO.PRO/` posts as 5411).
Mission 2 counts the Makro PRO *app*; the statement string can't tell app from
web, and the household orders in the app, so every Makro PRO row counts.

Fixed amounts, not a rate: UOB Makro rows carry no `% cb` from this
(`marks_rows = False`); the money lives in the Bureau and the trackers.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import UNCERTAIN, Rule, Tx
from .ladder import LadderPromotion, Tranche
from .slips import SlipCreditPromotion

CAMPAIGN = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
SOURCE = ("https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/"
          "makro-26th-mpw823-1226.page")
TITLE = "ฉลองบัตรเครดิตยูโอบี แม็คโคร 26 ปี — Gold Mission"
CARDS = ("UOB Makro",)

STORE_BANDS = ((Decimal(400_000), Decimal(2_500)), (Decimal(150_000), Decimal(800)),
               (Decimal(50_000), Decimal(150)))
PRO_TIERS = ((Decimal(60_000), Decimal(1_200)), (Decimal(30_000), Decimal(500)),
             (Decimal(10_000), Decimal(150)))
OTHER_REACH, OTHER_PAY = Decimal(10_000), Decimal(300)

_MAKRO = re.compile(r"MAKRO")
_MAKRO_PRO = re.compile(r"MAKRO\.PRO")
_WALLET = r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*|SHOPEEPAY|RABBIT"
# Supermarkets the merchant string shows (MCC 5411); GO Wholesale posts as `CFW-<branch>`.
_GROCERS = re.compile(r"BIG ?C\b|BIGC|GO ?WHOLESALE|\bCFW-|DON ?DON ?DONKI|FOODLAND|GOURMET|HOME ?FRESH|"
                      r"RIMPING|VILLA|MAX ?VALU|FRESHKET|SAVEMART|CP FRESH")

_COMMON_RULES = (
    Rule("Paid through an e-wallet (TrueMoney, Rabbit LINE Pay …)", _WALLET),
    Rule("Gift cards and top-ups of any card", r"GIFT ?CARD|VOUCHER|\(TOP\b|\bTOP ?-?UP\b"),
    Rule("Installments: UOB excludes the not-yet-billed balance; whether each billed term counts "
         "isn't stated", test=lambda tx: promotions.is_installment(tx.name), level=UNCERTAIN),
    Rule("Annual fees, interest, cash advances, transfers, UOB Pay Anything, tax refunds",
         r"MEMBERSHIP FEE|ANNUAL FEE|INTEREST|LATE CHARGE|CASH ADVANCE|PAY ?ANYTHING"),
    Rule("Cigarettes, alcohol, infant formula, medicines; charges cancelled later"),
)
_REGISTER = ("Register once: SMS \"UMK26 <last 12 digits>\" to 4545111, or Rewards+ in UOB TMRW "
             "(Takumi registered on 3 Oct 2026).")
_POOLED = ("UOB Makro cardholders only; principal and supplements count as one cardholder, so "
           "Takumi's and Baiboon's UOB Makro rows pool.")
_CREDITING = (
    "Within 60 days after the campaign ends (31 Dec 2026), to the principal card's account.",
    "All three missions at least once during the campaign → a ฿1,000 Makro voucher on top, mailed "
    "to the principal (not tracked here). Every ฿1,000 on the card is a right in a gold-bar draw "
    "(not tracked).",
    "The three missions pay at most ฿12,000 together. Not combinable with other promotions.",
)


def _band(pooled: Decimal, bands: tuple[tuple[Decimal, Decimal], ...]) -> list[Tranche]:
    for reach, pay in bands:
        if pooled >= reach:
            return [Tranche(Decimal(0), reach, pay)]
    return []


class UOBMakroStoreMission(LadderPromotion):
    code = "UMK26-1"
    icon = "🛒"
    title = f"{TITLE} · ภารกิจที่ 1 (หน้าร้านแม็คโคร)"
    cards = CARDS
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "฿150/800/2,500"
    marks_rows = False

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        return _band(pooled, STORE_BANDS)

    def qualifies(self, tx: Tx) -> bool:
        return bool(_MAKRO.search(tx.merchant)) and not _MAKRO_PRO.search(tx.merchant)

    ladder_rows: ClassVar = (
        ("under ฿50,000", "nothing"),
        ("฿50,000 – 149,999", "฿150"),
        ("฿150,000 – 399,999", "฿800"),
        ("฿400,000 or more", "฿2,500 — the monthly maximum"),
        ("Cap", "฿7,500 for the campaign"),
    )
    examples: ClassVar = ((49_999, 0), (50_000, 150), (149_999, 150), (150_000, 800),
                          (399_999, 800), (400_000, 2_500), (900_000, 2_500))
    inclusions: ClassVar = (
        "Spend on the UOB Makro card at every Makro branch, added up over the calendar month; the "
        "month's total pays one band. Makro PRO is mission 2.",
        _POOLED,
        _REGISTER,
    )
    rules: ClassVar = (
        Rule("Paid through TrueMoney at the till (TMN MAKRO)", _WALLET),
        *_COMMON_RULES[1:],
    )
    crediting: ClassVar = _CREDITING


class UOBMakroProMission(SlipCreditPromotion):
    code = "UMK26-2"
    icon = "🛒"
    title = f"{TITLE} · ภารกิจที่ 2 (Makro PRO)"
    cards = CARDS
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "฿150/500/1,200"
    cap = Decimal(3_600)

    # One quota for the whole campaign: the Bureau row runs 1 Oct – 31 Dec (`2026M10`).
    def period_for(self, tx: Tx) -> tuple[dt.date, dt.date] | None:
        first, last = self.campaign
        return (first, last) if first <= tx.day <= last else None

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _MAKRO_PRO.search(tx.merchant):
            return None
        return next((pay for reach, pay in PRO_TIERS if tx.amount >= reach), None)

    ladder_title = "Cashback per slip"
    ladder_header = ("Makro PRO slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿10,000", "nothing"),
        ("฿10,000 – 29,999", "฿150"),
        ("฿30,000 – 59,999", "฿500"),
        ("฿60,000 or more", "฿1,200"),
        ("Cap", "฿3,600 for the whole campaign"),
    )
    inclusions: ClassVar = (
        "Card payments in the Makro PRO app, per slip: slips never add up. The statement string "
        "(`HTTPS://WWW.MAKRO.PRO/`, `WWW.MAKRO.PRO`) can't tell app from web; the household orders "
        "in the app.",
        "One quota for the whole campaign (1 Oct – 31 Dec 2026).",
        _POOLED,
        _REGISTER,
    )
    rules: ClassVar = _COMMON_RULES
    crediting: ClassVar = _CREDITING


class UOBMakroOtherMission(LadderPromotion):
    code = "UMK26-3"
    icon = "🛒"
    title = f"{TITLE} · ภารกิจที่ 3 (หมวดอื่นๆ)"
    cards = CARDS
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "฿300"
    marks_rows = False

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        return _band(pooled, ((OTHER_REACH, OTHER_PAY),))

    def qualifies(self, tx: Tx) -> bool:
        return not _MAKRO.search(tx.merchant)

    ladder_rows: ClassVar = (
        ("under ฿10,000", "nothing"),
        ("฿10,000 or more", "฿300 — the monthly maximum"),
        ("Cap", "฿900 for the campaign"),
    )
    examples: ClassVar = ((9_999, 0), (10_000, 300), (50_000, 300))
    inclusions: ClassVar = (
        "Spend on the UOB Makro card outside Makro (\"หมวดอื่นๆ ตามที่ธนาคารกำหนด\", other categories "
        "as the bank defines them), added up over the calendar month.",
        _POOLED,
        _REGISTER,
    )
    rules: ClassVar = (
        Rule("Hypermarkets and supermarkets (MCC 5411)",
             test=lambda tx: bool(_GROCERS.search(tx.merchant)) or promotions.looks_supermarket(tx.merchant)),
        Rule("Fuel stations", test=lambda tx: promotions.looks_petrol(tx.merchant)),
        Rule("Utilities (MCC 4900), insurance and unit-linked policies, funds (MCC 6211), EasyBills "
             "(MCC 5999)", r"EASY ?BILL|\bPEA\b|\bMEA\b|\bPWA\b|WATERWORKS|INSURANCE|ASSURANCE|\bFUND\b"),
        *_COMMON_RULES,
    )
    crediting: ClassVar = _CREDITING


PROMOTIONS = (UOBMakroStoreMission, UOBMakroProMission, UOBMakroOtherMission)
