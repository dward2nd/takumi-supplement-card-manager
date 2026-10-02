"""Krungsri Card at Bangchak, 1 Oct 2026 – 31 May 2027 — the card's 1% (per cycle) and BXP (per slip), from ฿700 a slip.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.krungsricard.com/th/promotion/bangchak on
2026-10-01, which replaced the Jun–Sep terms (`bangchak.py`) that day. Same two
parts on Krungsri Visa Platinum, JCB Platinum and Lady Titanium (Krungsri NOW
is still excluded), now in steps of ฿700 a slip:

  ต่อ 1 — the card's own benefit, no registration: "1%", read as ฿7 per whole
          ฿700 of each slip, at most ฿21 per primary card account per statement
          cycle (the bank counts at most ฿2,100 of fuel a cycle), credited within
          the cycle. The old terms' ฿8 per whole ฿800 was confirmed by the bank's
          `BANGCHAK SPECIAL DISCOUNT OF 1 %` lines; this reading follows it, and
          October's lines will confirm it. `Bangchak700CardBenefit`, code
          "Bangchak700" so its cycle rows never share a name with the old
          `Bangchak` rows (the cycle billed 5 Oct 2026 straddles both).
  ต่อ 2 — BXP, registered in UCHOOSE per round (round 1: 1 Oct 2026 – 31 Jan
          2027; round 2: 1 Feb – 31 May 2027): ฿17.50 per whole ฿700 on each slip,
          at most ฿52.50 per primary card account per calendar month, credited
          within 30 days after the month. `BXPPromotion`. (BXS, 2% for the
          Signature tier, isn't on any household card.)

Both withhold the card's normal points, as `KrungsriPetrolCampaign` already
does. Gas (LPG/NGV) stations and e-wallet payments don't count.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import ClassVar

from .accounts import CardAccount
from .bangchak import _RULES, _fuel
from .base import Tx
from .slips import SlipCreditPromotion

STEP = Decimal(700)
CAMPAIGN = (dt.date(2026, 10, 1), dt.date(2027, 5, 31))
SOURCE = "https://www.krungsricard.com/th/promotion/bangchak"
_ROUNDS = "round 1: 1 Oct 2026 – 31 Jan 2027; round 2: 1 Feb – 31 May 2027"


def _steps(tx: Tx) -> int:
    return int(tx.amount // STEP) if _fuel(tx) else 0


class Bangchak700CardBenefit(SlipCreditPromotion):
    code = "Bangchak700"
    icon = "⛽"
    title = "เติมคืนคุ้ม ง่ายขึ้นได้ทุกวัน ที่ปั๊มบางจาก — ต่อ 1 (สิทธิประโยชน์บัตร)"
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "1%"
    period_basis = "bill_cycle"
    cap = Decimal(21)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        steps = _steps(tx)
        return steps * Decimal(7) if steps else None

    ladder_title = "Cashback per slip"
    ladder_header = ("Bangchak fuel slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿700", "nothing"),
        ("every whole ฿700 on the slip, no registration", "฿7 (1%)"),
        ("Cap", "฿21 a statement cycle per primary card account (฿2,100 of fuel)"),
    )
    inclusions: ClassVar = (
        "Krungsri Visa Platinum, JCB Platinum and Lady Titanium; Krungsri NOW is excluded.",
        "Counted per statement cycle (Bill Cycle Date), supplements included; credited within the "
        "cycle as `BANGCHAK SPECIAL DISCOUNT OF 1 %`.",
        "Read as ฿7 per whole ฿700 of each slip, as the Jun–Sep terms' ฿8 per ฿800 were paid; "
        "October's statement lines will confirm it.",
        "The card's normal points are withheld on the same spend.",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = ("Within the statement cycle, to the primary card account.",)


class BXPPromotion(SlipCreditPromotion):
    code = "BXP"
    icon = "⛽"
    title = "เติมคืนคุ้ม ง่ายขึ้นได้ทุกวัน ที่ปั๊มบางจาก — ต่อ 2 พิเศษรับเพิ่ม"
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "2.5%"
    cap = Decimal("52.5")

    def slip_credit(self, tx: Tx) -> Decimal | None:
        steps = _steps(tx)
        return steps * Decimal("17.5") if steps else None

    ladder_title = "Cashback per slip"
    ladder_header = ("Bangchak fuel slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿700", "nothing"),
        ("every whole ฿700 on the slip", "฿17.50 (2.5%)"),
        ("Cap", "฿52.50 a calendar month per primary card account"),
    )
    inclusions: ClassVar = (
        "Krungsri Visa Platinum, JCB Platinum and Lady Titanium; Krungsri NOW is excluded.",
        "Per slip: ฿1,399 earns ฿17.50, the same as ฿700. Slips never add up.",
        f"Per calendar month, supplements included. Register in UCHOOSE (\"BXP\") before or on the "
        f"transaction date, once per round ({_ROUNDS}).",
        "The card's normal points are withheld on the same spend.",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = (
        "Within 30 days after each month-end, to the primary card account.",
        "Not combinable with other promotions.",
    )


class Bangchak700KrungsriVISA(CardAccount, Bangchak700CardBenefit):
    cards = ("Krungsri VISA",)


class Bangchak700KrungsriJCB(CardAccount, Bangchak700CardBenefit):
    cards = ("Krungsri JCB",)


class Bangchak700KrungsriLady(CardAccount, Bangchak700CardBenefit):
    cards = ("Krungsri Lady",)


class BXPKrungsriVISA(CardAccount, BXPPromotion):
    cards = ("Krungsri VISA",)


class BXPKrungsriJCB(CardAccount, BXPPromotion):
    cards = ("Krungsri JCB",)


class BXPKrungsriLady(CardAccount, BXPPromotion):
    cards = ("Krungsri Lady",)


ACCOUNTS = (Bangchak700KrungsriVISA, Bangchak700KrungsriJCB, Bangchak700KrungsriLady,
            BXPKrungsriVISA, BXPKrungsriJCB, BXPKrungsriLady)
