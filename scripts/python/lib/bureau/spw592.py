"""UOB SPW592 — "ช้อปซูเปอร์ ยิ่งจ่าย ยิ่งคุ้ม" (SuperHypermarket H2), 1 Jul – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read on 2026-10-01 from
https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/super-spw592-1226.page
(rendered from `…/super-spw592-1226.json`; ref 26UC15). Pooled monthly
full-amount spend at the named supermarkets (MCC 5411/5499) pays one amount
for the band reached: ฿50 from ฿4,000, ฿150 from ฿10,000. At most ฿150 a month
and ฿900 for the campaign (6 × ฿150), per cardholder, every UOB card and
supplement pooled — except UOB Makro, which the cashback part excludes.

Makro isn't among the stores, and e-wallet payments (`TMN LOTUS HYPER`) don't
count. The household's UOB supermarket spend from July to September was a few
hundred baht, far under ฿4,000. Not registered (user, 2026-10-01): the class is
ready, but no Bureau row exists, so nothing links to it.

An overlay like EPW538: UOB One rows keep their own `% cb`, and the ฿50/฿150
lives in the trackers (`marks_rows = False`). The bank pays only the best of
overlapping promotions in one merchant category; whether it counts UOB One's own
cashback as one is unknown (see docs/promotions/uob-epw538.md).
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .ladder import LadderPromotion, Tranche

BANDS = ((Decimal(10_000), Decimal(150)), (Decimal(4_000), Decimal(50)))

# In store and the listed online shops. GO Wholesale posts as `CFW-<branch> …`.
_STORES = re.compile(r"BIG ?C\b|BIGC|DON ?DON ?DONKI|\bDONKI\b|FOODLAND|GOURMET|GO ?WHOLESALE|\bCFW-|"
                     r"HOME ?FRESH|LOTUS'?S|LOTUS GO ?FRESH|MITSUKOSHI|DEPACHIKA|NO ?BRAND|RIMPING|"
                     r"\bTOPS\b|VILLA|FRESHKET")
_WALLET = r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*|SHOPEEPAY|RABBIT"


class SPW592Promotion(LadderPromotion):
    code = "SPW592"
    icon = "🛒"
    title = "ช้อปซูเปอร์ ยิ่งจ่าย ยิ่งคุ้ม"
    cards = ("UOB One", "UOB World", "UOB Premier")
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 12, 31))
    source_url = ("https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/"
                  "super-spw592-1226.page")
    headline = "฿50/150"
    marks_rows = False   # an overlay on each card's own cashback; `% cb` stays the card's

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        for reach, pay in BANDS:
            if pooled >= reach:
                return [Tranche(Decimal(0), reach, pay)]
        return []

    def qualifies(self, tx: Tx) -> bool:
        return bool(_STORES.search(tx.merchant))

    ladder_rows: ClassVar = (
        ("under ฿4,000", "nothing"),
        ("฿4,000 – 9,999", "฿50"),
        ("฿10,000 or more", "฿150 — the monthly cap"),
    )
    examples: ClassVar = ((3_999, 0), (4_000, 50), (9_999, 50), (10_000, 150), (60_000, 150))
    inclusions: ClassVar = (
        "Full-amount spend at supermarkets and hypermarkets (MCC 5411, 5499) in store: Big C, Big C "
        "Mini, Don Don Donki, Foodland, Gourmet Market, GO Wholesale, Home Fresh Mart, Lotus's, Lotus's "
        "PRIVÉ, Lotus's go fresh, Mitsukoshi Depachika, No Brand, Rimping, Tops Food Hall, Tops, Tops "
        "Daily, Tops Care, Villa Market.",
        "Online only through Big C online, Freshket, GO Wholesale, Lotus's Shop Online, Tops Online and "
        "Villa Market Online, paid by card on their own site or app.",
        "Slips add up: one amount for the month's highest band, pooled across every UOB card Takumi "
        "holds and every supplement on them — except UOB Makro.",
        "Register once before spending, within the month you join: SMS \"SH <last 12 digits>\" to "
        "4545111, or Rewards+ in UOB TMRW. Dated by the transaction (approval) date.",
    )
    rules: ClassVar = (
        Rule("Paid through an e-wallet (TrueMoney, Rabbit LINE Pay, ShopeePay …)", _WALLET),
        Rule("Makro (not a participating store)", r"MAKRO"),
        Rule("Shops renting space inside the store; cash on delivery; bill payments"),
        Rule("Gift cards and vouchers, top-ups of any card, investment, utilities, financial "
             "transactions and insurance", r"GIFT ?CARD|VOUCHER|TOP ?UP"),
        Rule("UOB i-Plan installments", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Charges cancelled later"),
    )
    crediting: ClassVar = (
        "Within 60 days after the last day of the month registered for, to a primary card the bank "
        "picks.",
        "Not combinable with other promotions.",
    )
