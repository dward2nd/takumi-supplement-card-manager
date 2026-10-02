"""ttb credit-card shopping campaigns, Oct–Dec 2026: MUJI (MUJC) and the hypermarket (BGO).

deterministic + idempotent — declarations and pure functions only.

Terms read on 2026-10-01 from
https://www.ttbbank.com/th/promotion/credit-card/shopping/muji-oct26 and
https://www.ttbbank.com/th/promotion/credit-card/shopping/hypermarket-oct26.
Every ttb card counts, primary and supplement pooled into the primary
cardholder's account (Takumi's …7368, Baiboon's …0864). Both cap the whole
campaign per person, not a month, so each keeps one Bureau row for the
campaign (`2026M10`), as BMG did. Slips are read as each earning its own tier,
summed up to the cap, as the household read BMG (`ttb_campaigns.py`).

  MUJC — MUJI, 1 Oct – 31 Dec 2026: ฿40 per whole ฿1,200 of a slip (at most
         ฿160), ฿200 for a ฿6,000–9,999 slip, ฿500 from ฿10,000; ฿1,500 per
         person for the campaign.
  BGO  — BMG's successor, 1 Oct – 31 Dec 2026: the same tiers (฿50 / 100 /
         450 / 1,500 from ฿3,000 / 5,000 / 20,000 / 100,000 a slip), but only at
         Big C and GO Wholesale, in store and online. Makro PRO is no longer in
         it. ฿1,500 per person for the campaign.

ttb's "Joy of Shopping" (joyofshopping-jan26) redeems ttb rewards plus points
at participating malls; ttb so smart earns no points, so it isn't modelled.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .slips import SlipCreditPromotion
from .ttb_campaigns import _TIERS, _WALLET, TTBHypermarketPromotion

CAMPAIGN = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
_MUJI = re.compile(r"\bMUJI\b")
# GO Wholesale posts as `CFW-<branch> …` (Central Food Wholesale).
_BIGC_GO = re.compile(r"BIG ?C\b|BIGC|GO ?WHOLESALE|\bCFW-")


class _WholeCampaign(SlipCreditPromotion):
    """One quota for the whole campaign: the Bureau row runs from its first day to its last."""

    def period_for(self, tx: Tx) -> tuple[dt.date, dt.date] | None:
        first, last = self.campaign
        return (first, last) if first <= tx.day <= last else None


class TTBMujiPromotion(_WholeCampaign):
    code = "MUJC"
    icon = "🛍️"
    title = "ttb — ช้อปคุ้มที่ MUJI"
    cards = ("ttb so smart",)
    campaign = CAMPAIGN
    source_url = "https://www.ttbbank.com/th/promotion/credit-card/shopping/muji-oct26"
    headline = "฿40–500"
    cap = Decimal(1_500)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _MUJI.search(tx.merchant) or tx.amount < 1_200:
            return None
        if tx.amount >= 10_000:
            return Decimal(500)
        if tx.amount >= 6_000:
            return Decimal(200)
        return tx.amount // 1_200 * Decimal(40)

    ladder_title = "Cashback per slip"
    ladder_header = ("MUJI slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿1,200", "nothing"),
        ("every whole ฿1,200, under ฿6,000", "฿40 — up to ฿160"),
        ("฿6,000 – 9,999", "฿200"),
        ("฿10,000 or more", "฿500"),
        ("Cap", "฿1,500 per person for the whole campaign, every card together"),
    )
    inclusions: ClassVar = (
        "Full-amount spend at MUJI, on every ttb card; primary and supplements pooled.",
        "Read as each slip earning its own tier, summed up to the ฿1,500 (as for BMG).",
        "Register once, before or on the transaction date: ttb touch, or SMS \"MUJC <last 12 digits>\" "
        "to 4899777.",
    )
    rules: ClassVar = (
        Rule("Converted to ttb so goood (which also loses so smart's 1%)",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Business spend; charges cancelled or returned later"),
    )
    crediting: ClassVar = (
        "Within 60 days after the campaign ends (by about 1 Mar 2027), to the primary card with the "
        "most spend.",
        "The points half (10% for ttb rewards plus points) doesn't apply: ttb so smart earns no points.",
    )


class TTBBigCGoPromotion(TTBHypermarketPromotion):
    code = "BGO"
    title = "ttb — ช้อปไฮเปอร์มาร์เก็ตสุดคุ้ม ที่ Big C และ Go Wholesale"
    campaign = CAMPAIGN
    source_url = "https://www.ttbbank.com/th/promotion/credit-card/shopping/hypermarket-oct26"

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _BIGC_GO.search(tx.merchant):
            return None
        return next((pay for reach, pay in _TIERS if tx.amount >= reach), None)

    inclusions: ClassVar = (
        "Full-amount spend at Big C and GO Wholesale in store, and Big C Online and GO Wholesale Online "
        "— not Makro (in store or PRO), Lotus's or Tops.",
        "Register once, before or on the transaction date: ttb touch, or SMS \"BGO <last 12 digits>\" "
        "to 4899777.",
        "Read as each slip earning its own tier, summed up to the ฿1,500 (the household's reading of "
        "BMG); the page's boilerplate could also mean only the single highest slip pays.",
    )
    rules: ClassVar = (
        Rule("Paid through an e-wallet", _WALLET),
        Rule("Converted to ttb so goood (which also loses so smart's 1%)",
             test=lambda tx: promotions.is_installment(tx.name)),
    )
    crediting: ClassVar = (
        "Within 60 days after the campaign ends (by about 1 Mar 2027), to the primary card with the "
        "most spend.",
    )
