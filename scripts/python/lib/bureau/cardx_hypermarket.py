"""CardX HY1 / HYP — "คุ้มยกแพ็ก รับคืนแรง ที่ไฮเปอร์มาร์เก็ต", 1 Oct – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read on 2026-10-01 from the rendered
https://www.cardx.co.th/credit-card/promotion/top-hypermarket-oct26-usc02 (the
user's copy: CardX's content server refuses this machine, whose traffic leaves
through Hong Kong). Full-amount spend at the named hypermarkets, in store and
online, on every CardX credit card:

  HY1 — per slip: ฿40 for ฿3,000–9,999, ฿200 for ฿10,000–29,999, ฿720 from
        ฿30,000; at most ฿1,440 a month per person, every CardX card together,
        and ฿4,320 for the campaign (3 × ฿1,440, never binding alone).
        `CardXHypermarketPromotion`, one row per month.
  HYP — ฿3,000 once, for ฿300,000 of such spend over the whole campaign; one right
        per person, and only the first 150 nationwide. `CardXHypermarketBonus`, one
        quota for the campaign. The household's CardX spend is nowhere near it, so
        it has no Bureau rows.

The third part (HY2) swaps POINTX points for 12% (Mon–Thu) or 14% (Fri–Sun) back,
by SMS on every slip: a redemption, not tracked. The only household CardX card
is Nuta's CardX JCB; CardX bills each card number on its own, so its quota is
simply that card's. CardX rows carry no `% cb` here (a fixed amount per slip).
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
SOURCE = "https://www.cardx.co.th/credit-card/promotion/top-hypermarket-oct26-usc02"
TITLE = "คุ้มยกแพ็ก รับคืนแรง ที่ไฮเปอร์มาร์เก็ต"
TIERS = ((Decimal(30_000), Decimal(720)), (Decimal(10_000), Decimal(200)), (Decimal(3_000), Decimal(40)))

# In store: Big C (food place, market, mini), GO WHOLESALE (`CFW-…`), Lotus's (PRIVE,
# go fresh), Makro. Online: Big C Online, Freshket, GO WHOLESALE app, Lotus's online, Makro PRO.
_STORES = re.compile(r"BIG ?C\b|BIGC|GO ?WHOLESALE|\bCFW-|LOTUS'?S|LOTUS GO ?FRESH|MAKRO|FRESHKET")
_RULES = (
    Rule("Paid through ShopeePay or Rabbit LINE Pay", r"SHOPEEPAY|^LINEPAY\*|^LPTH\*|RABBIT"),
    Rule("Paid through TrueMoney (TMN MAKRO, TMN LOTUS …)", r"^TMN[ *]|TRUE ?MONEY", level=UNCERTAIN,
         hint="the page excludes only ShopeePay and Rabbit LINE Pay; whether a TrueMoney payment carries "
              "the store's category is unknown"),
    Rule("Installments of every kind: ดีจังแบ่งชำระ 0%, plans set up through CardX or SCB EASY",
         test=lambda tx: promotions.is_installment(tx.name)),
    Rule("Business use; charges cancelled later"),
)
_INCLUSIONS = (
    "Full-amount spend at Big C (food place, market, mini Big C), GO WHOLESALE, Lotus's (PRIVE, go "
    "fresh) and Makro in store, and Big C Online, Freshket, the GO WHOLESALE app, Lotus's online and "
    "Makro PRO, on every CardX and SCB WEALTH by CardX credit card.",
    "One quota per person, every CardX card together; the household's only CardX card is Nuta's "
    "CardX JCB.",
)


def _store(tx: Tx) -> bool:
    return bool(_STORES.search(tx.merchant))


class CardXHypermarketPromotion(SlipCreditPromotion):
    code = "HY1"
    icon = "🛒"
    title = f"{TITLE} — คุ้มที่ 1"
    cards = ("CardX JCB",)
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "฿40/200/720"
    cap = Decimal(1_440)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _store(tx):
            return None
        return next((pay for reach, pay in TIERS if tx.amount >= reach), None)

    ladder_title = "Cashback per slip"
    ladder_header = ("Hypermarket slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿3,000", "nothing"),
        ("฿3,000 – 9,999", "฿40"),
        ("฿10,000 – 29,999", "฿200"),
        ("฿30,000 or more", "฿720"),
        ("Cap", "฿1,440 a month and ฿4,320 for the campaign, per person"),
    )
    inclusions: ClassVar = (
        *_INCLUSIONS,
        "Per slip: slips never add up.",
        "Register every card once: the CardX app or website, or SMS \"HY1 <last 12 digits>\" to 4545777 "
        "(CardX FLEX: \"FHY\").",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = (
        "Within 60 days after the campaign ends (31 Dec 2026), to the card the slip was paid with; it "
        "shows on the next statement.",
    )


class CardXHypermarketBonus(LadderPromotion):
    code = "HYP"
    icon = "🛒"
    title = f"{TITLE} — รับเพิ่ม"
    cards = ("CardX JCB",)
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "฿3,000"
    marks_rows = False

    # One quota for the whole campaign: the Bureau row runs 1 Oct – 31 Dec (`2026M10`).
    def period_for(self, tx: Tx) -> tuple[dt.date, dt.date] | None:
        first, last = self.campaign
        return (first, last) if first <= tx.day <= last else None

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        return [Tranche(Decimal(0), Decimal(300_000), Decimal(3_000))] if pooled >= 300_000 else []

    def qualifies(self, tx: Tx) -> bool:
        return _store(tx)

    ladder_title = "Cashback for the campaign"
    ladder_header = ("Spend over the whole campaign", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿300,000", "nothing"),
        ("฿300,000 or more", "฿3,000, once per person; the first 150 people only"),
    )
    examples: ClassVar = ((299_999, 0), (300_000, 3_000), (900_000, 3_000))
    inclusions: ClassVar = (
        *_INCLUSIONS,
        "Slips add up over the whole campaign (1 Oct – 31 Dec 2026); CardX FLEX doesn't count.",
        "Register every card once: the CardX app or website, or SMS \"HYP <last 12 digits>\" to 4545777.",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = ("Within 60 days after the campaign ends, to the card used.",)
