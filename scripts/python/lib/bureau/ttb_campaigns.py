"""ttb credit-card campaigns: Caltex (CTG) and Bangchak (BCG) fuel, and the hypermarket (BMG).

deterministic + idempotent — declarations and pure functions only.

Terms read on 2026-09-29 from
https://www.ttbbank.com/th/promotion/credit-card/auto/caltex-jul26,
https://www.ttbbank.com/th/promotion/credit-card/auto/bangchak-jul26 and
https://www.ttbbank.com/th/promotion/credit-card/shopping/hypermarket-jul26.
Every ttb card counts, primary and supplement pooled into the primary
cardholder's account (Takumi's …7368, Baiboon's …0864).

Fuel (1 Jul – 31 Dec 2026): 3% of each slip of ฿600 or more, at most ฿18 a slip
— so every qualifying slip pays ฿18 — for at most 4 slips (฿72) per person per
calendar month. (5%, ฿30 a slip, needs a ttb car or home loan; the household
takes the 3%.) Baiboon's `ttb Bangchak 3% Aug 2026` ฿54 is 3 × ฿18.

Hypermarket (1 Jul – 30 Sep 2026): each slip of ฿3,000 or more at Big C, Go
Wholesale, Big C Online or Makro PRO earns by its size — ฿50, ฿100, ฿450 or
฿1,500 — up to ฿1,500 per person for the whole campaign, so the Bureau keeps one
row for the campaign (`2026M7`). The page's boilerplate also speaks of "the
highest slip per round"; the household's own tracker (฿500 for 1 Jul – 30 Sep)
reads the slips as adding up, and so does this class.
"""

from __future__ import annotations

import datetime as dt
import math
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .slips import SlipCreditPromotion

_WALLET = r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*|SHOPEEPAY"


class _TTBFuel(SlipCreditPromotion):
    icon = "⛽"
    cards = ("ttb so smart",)
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 12, 31))
    headline = "3%"
    cap = Decimal(72)
    station: ClassVar[re.Pattern]

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if tx.amount < 600 or not self.station.search(tx.merchant):
            return None
        return min(Decimal(math.floor(tx.amount * Decimal("0.03"))), Decimal(18))

    ladder_title = "Cashback per slip"
    ladder_header = ("Fuel slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿600", "nothing"),
        ("฿600 or more", "3%, at most ฿18 — so ฿18"),
        ("Cap", "4 slips (฿72) a calendar month per person"),
    )
    rules: ClassVar = (
        Rule("Paid through an e-wallet", _WALLET),
        Rule("Business spend; charges cancelled or refunded later"),
    )
    crediting: ClassVar = (
        "Within 60 days after the end of the month, to the primary cardholder.",
        "The slip must post before the statement date.",
    )


class TTBCaltexPromotion(_TTBFuel):
    code = "CTG"
    title = "ttb — เติมคุ้มขึ้นที่ปั๊มคาลเท็กซ์"
    source_url = "https://www.ttbbank.com/th/promotion/credit-card/auto/caltex-jul26"
    station = re.compile(r"CALTEX|คาลเท็กซ์")
    inclusions: ClassVar = (
        "Fuel of ฿600 or more a slip at any Caltex station in Thailand, on any ttb card (supplements "
        "pooled into the primary).",
        "Register once: ttb touch, or SMS \"CTG <last 12 digits>\" to 4899777.",
    )


class TTBBangchakPromotion(_TTBFuel):
    code = "BCG"
    title = "ttb — เติมน้ำมันสุดคุ้มที่ปั๊มบางจาก"
    source_url = "https://www.ttbbank.com/th/promotion/credit-card/auto/bangchak-jul26"
    station = re.compile(r"BANGCHAK|\bBSRC\b|BSRC-|บางจาก")
    inclusions: ClassVar = (
        "Fuel of ฿600 or more a slip at any Bangchak station in Thailand, on any ttb card (supplements "
        "pooled into the primary).",
        "Register once: ttb touch, or SMS \"BCG <last 12 digits>\" to 4899777.",
    )


_HYPERMARKETS = re.compile(r"BIG ?C\b|BIGC|GO ?WHOLESALE|MAKRO ?PRO|WWW\.MAKRO\.PRO|MAKRO\.PRO")
_TIERS = ((Decimal(100_000), Decimal(1_500)), (Decimal(20_000), Decimal(450)),
          (Decimal(5_000), Decimal(100)), (Decimal(3_000), Decimal(50)))


class TTBHypermarketPromotion(SlipCreditPromotion):
    code = "BMG"
    icon = "🛒"
    title = "ttb — ช้อป Big C, Go Wholesale และ Makro Pro ที่สาขาและออนไลน์"
    cards = ("ttb so smart",)
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))
    source_url = "https://www.ttbbank.com/th/promotion/credit-card/shopping/hypermarket-jul26"
    headline = "฿50–1,500"
    cap = Decimal(1_500)

    # One quota for the whole campaign: the Bureau row runs 1 Jul – 30 Sep (`2026M7`).
    def period_for(self, tx: Tx) -> tuple[dt.date, dt.date] | None:
        first, last = self.campaign
        return (first, last) if first <= tx.day <= last else None

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _HYPERMARKETS.search(tx.merchant):
            return None
        return next((pay for reach, pay in _TIERS if tx.amount >= reach), None)

    ladder_title = "Cashback per slip"
    ladder_header = ("Slip", "Cashback")
    ladder_rows: ClassVar = (
        ("฿3,000 – 4,999", "฿50"),
        ("฿5,000 – 19,999", "฿100"),
        ("฿20,000 – 99,999", "฿450"),
        ("฿100,000 or more", "฿1,500"),
        ("Cap", "฿1,500 per person for the whole campaign, every card together"),
    )
    inclusions: ClassVar = (
        "Full-amount spend at Big C (every format) and Go Wholesale in store, and Big C Online, Makro "
        "PRO and Go Wholesale Online — not Makro in store, not Lotus's or Tops.",
        "Register once, before or on the transaction date: ttb touch, or SMS \"BMG <last 12 digits>\" "
        "to 4899777.",
        "Read as each slip earning its own tier, summed up to the ฿1,500 (the household's tracker); "
        "the page's boilerplate could also mean only the single highest slip pays.",
    )
    rules: ClassVar = (
        Rule("Makro in store (only Makro PRO online is listed)", r"^MAKRO_"),
        Rule("Paid through an e-wallet", _WALLET),
        Rule("Converted to ttb so goood (which also loses so smart's 1%)",
             test=lambda tx: promotions.is_installment(tx.name)),
    )
    crediting: ClassVar = (
        "Within 60 days after the campaign ends (by about 29 Nov 2026), to the primary card with the "
        "most spend.",
    )
