"""AEON World Mastercard cashback — 5% at partner supermarkets, 1 Apr 2026 – 31 Jan 2027.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.aeon.co.th/aeon/cards/aeon-world-mastercard on
2026-09-29: 5% at Big C (and Big C Online), Lotus's (and its online shop),
Foodland, Villa Market, Tops, Gourmet Market & Home Fresh Mart, Central Food
Hall and Makro Pro; at most ฿500 per primary card per statement cycle
(11th – 10th), supplements included (so ฿10,000 of spend fills it). Credited
within 90 days of the statement date.

AEON keeps `% cb` unset on these rows (Baiboon's `[บัตรหลัก] WWW.MAKRO.PRO`
rows), so this writes the Bureau and the trackers only.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import UNCERTAIN, Rule, Tx
from .capped import CreditCapPromotion

RATE = Decimal("0.05")
_STORES = re.compile(r"BIG ?C\b|BIGC|LOTUS|FOODLAND|VILLA|\bTOPS\b|GOURMET|HOME FRESH|CENTRAL FOOD ?HALL|"
                     r"MAKRO")


class AEONWorldCashback(CreditCapPromotion):
    code = "AEON WM"
    name_pattern = r"\bAEON WM cb 5%"
    title = "AEON World Mastercard เครดิตเงินคืน 5% ซูเปอร์มาร์เก็ต"
    cards = ("AEON World Mastercard",)
    campaign = (dt.date(2026, 4, 1), dt.date(2027, 1, 31))
    source_url = "https://www.aeon.co.th/aeon/cards/aeon-world-mastercard"
    headline = "5%"
    period_basis = "bill_cycle"
    cap = Decimal(500)
    marks_rows = False   # AEON World rows keep `% cb` unset; the money is in the trackers

    def rate(self, tx: Tx) -> Decimal | None:
        if not _STORES.search(tx.merchant) or promotions.is_installment(tx.name):
            return None
        return RATE

    ladder_title = "Cashback"
    ladder_header = ("Where", "Cashback")
    ladder_rows: ClassVar = (
        ("Big C, Big C Online, Lotus's, Lotus's shop online, Foodland, Villa Market, Tops, Gourmet "
         "Market & Home Fresh Mart, Central Food Hall, Makro Pro", "5%"),
        ("Cap", "฿500 a statement cycle per primary card, supplements included (฿10,000 of spend)"),
    )
    inclusions: ClassVar = (
        "Counted per statement cycle, the 11th to the 10th: rows whose Bill Cycle Date is the "
        "cycle's close. The base is the baht amount after conversion.",
        "No registration.",
    )
    rules: ClassVar = (
        Rule("Makro in store (the page names Makro Pro)", r"^MAKRO_", level=UNCERTAIN,
             hint="only Makro Pro is named"),
        Rule("Installments, loans and hire purchase", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Funds and insurance (MCC 6211, 6300), foreign exchange (6051, 4829), cash advances, "
             "interest, fees, penalties, taxes; cancelled or refunded charges"),
    )
    crediting: ClassVar = (
        "Within 90 days of the statement date (the 10th), to the primary card.",
        "Spend counted here can't count toward another AEON promotion, by the page's terms — the "
        "household counts it toward Everyday with AEON too, as its trackers do.",
    )
