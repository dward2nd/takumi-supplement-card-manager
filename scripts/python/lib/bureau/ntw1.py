"""AEON NTW1 — "ใช้ทุกวัน รับทุกเดือน" (Everyday with AEON), 11 Jul 2026 – 10 Mar 2027.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.aeon.co.th/aeon/promotions/happy-monthly-with-aeon-2026
on 2026-09-29. Pooled spend per statement cycle (11th – 10th) across six
categories pays one fixed amount: ฿120 from ฿10,000, ฿340 from ฿30,000 — the
higher replaces the lower. At most ฿340 per person (national ID) per cycle;
the ฿2,720 campaign cap is 8 cycles × ฿340.

One registration per person counts, on one card: Takumi registered AEON World
Mastercard only, so no other AEON card's spend counts (user, 2026-09-29).
Supplements under it (Baiboon's) pool in. AEON keeps `% cb` unset, so this
writes the Bureau and the trackers only.

Restaurants (MCC 5812, dine-in or take-away, not fast food or food courts)
can't be told from the merchant string, so they're never linked
automatically: link a restaurant row by hand and it counts.

Spend counts by transaction date, strictly 11th – 10th, whatever statement
the row bills on (AEON's call centre, 2026-10-24). AEON posts purchases one
to four days late, so a row dated the 9th or 10th often bills a cycle later
but still counts in the period it was made in.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from ..bill_cycle import pattern_for_card
from .base import Rule, Tx, cycle_billed_on
from .ladder import LadderPromotion, Tranche

_DAY = dt.timedelta(days=1)

BANDS = ((Decimal(30_000), Decimal(340)), (Decimal(10_000), Decimal(120)))

_SUPERMARKETS = r"BIG ?C\b|BIGC|\bTOPS\b|GOURMET|FOODLAND|GO WHOLESALE|\bCFW-|MAKRO"  # CFW-: GO Wholesale's statement name
_DELIVERY = r"GRAB|LINE ?MAN|_LM_|PF_LM"
_TRAVEL = r"AGODA|BOOKING\.COM|GOTHER|KLOOK|TRAVELOKA|TRIP\.COM|CTRIP"
_BEAUTY = r"BEAUTRIUM|BOOTS|EVEANDBOY|EVE ?AND ?BOY|SEPHORA|WATSON"
_FASHION = (r"SUPERSPORTS|REV RUNNR|HOKA|H ?& ?M\b|ARMANI|CALVIN KLEIN|CROCS|FITFLOP|G2000|GUESS|HUSH PUPPIES|"
            r"JOHN HENRY|\bLEE\b|\bMLB\b|PAUL SMITH|RALPH LAUREN|SKECHERS|TOMMY HILFIGER|WRANGLER|BERSHKA|"
            r"MASSIMO DUTTI|OYSHO|PULL ?& ?BEAR|\bZARA\b")
_CATEGORIES = re.compile("|".join((_SUPERMARKETS, _DELIVERY, _TRAVEL, _BEAUTY, _FASHION)))
_WALLET = re.compile(r"^LINEPAY\*|^LPTH\*|^TMN[ *]|TRUE ?MONEY|SHOPEEPAY|GRABPAY")


class NTW1Promotion(LadderPromotion):
    code = "NTW1"
    title = "ใช้ทุกวัน รับทุกเดือน กับบัตรเครดิตอิออน (Everyday with AEON)"
    cards = ("AEON World Mastercard",)
    campaign = (dt.date(2026, 7, 11), dt.date(2027, 3, 10))
    source_url = "https://www.aeon.co.th/aeon/promotions/happy-monthly-with-aeon-2026"
    headline = "฿120/340"
    period_basis = "bill_cycle"
    marks_rows = False   # AEON World rows keep `% cb` unset; the money is in the trackers

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        for reach, pay in BANDS:
            if pooled >= reach:
                return [Tranche(Decimal(0), reach, pay)]
        return []

    def qualifies(self, tx: Tx) -> bool:
        return bool(_CATEGORIES.search(tx.merchant))

    # A row belongs to the period closing on the first AEON closing date (the 10th)
    # on or after its transaction date, not the one its Bill Cycle Date names. The
    # Bureau row keeps a cycle row's dates (Start = the previous closing date,
    # End = the day before this one), so names and links stay as they were.
    def _closing(self, tx: Tx) -> dt.date:
        return pattern_for_card(tx.card or self.cards[0]).active(tx.day)[0]

    def covers(self, start: dt.date, end: dt.date, tx: Tx) -> bool:
        first, last = self.campaign
        return self._closing(tx) == cycle_billed_on(end) and first <= tx.day and (last is None or tx.day <= last)

    def candidate_filter(self, start: dt.date, end: dt.date) -> list[dict]:
        # A superset, a day wide each side (timed rows read back as datetimes); `covers` decides.
        return [{"property": "Transaction Datetime", "date": {"on_or_after": start.isoformat()}},
                {"property": "Transaction Datetime", "date": {"on_or_before": (cycle_billed_on(end) + _DAY).isoformat()}}]

    def period_for(self, tx: Tx) -> tuple[dt.date, dt.date] | None:
        first, last = self.campaign
        if tx.day < first or (last is not None and tx.day > last):
            return None
        closing = self._closing(tx)
        previous, _ = pattern_for_card(tx.card or self.cards[0]).closed(closing)
        return self._clip_cycle(previous, closing - _DAY)

    ladder_title = "Cashback per statement cycle"
    ladder_header = ("Pooled spend in the cycle", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿10,000", "nothing"),
        ("฿10,000 – 29,999", "฿120"),
        ("฿30,000 or more", "฿340 — the cap per person per cycle"),
    )
    examples: ClassVar = ((9_999, 0), (10_000, 120), (29_999, 120), (30_000, 340), (80_000, 340))
    inclusions: ClassVar = (
        "Full-amount baht spend at merchants in Thailand, in store or on the merchant's own site or "
        "app, summed across: restaurants (MCC 5812, dine-in or take-away, not fast food or food "
        "courts); food ordered in Grab and LINE MAN; Big C, Tops (Food Hall, daily), Gourmet Market, "
        "Foodland, Go Wholesale and Makro PRO; Agoda, Booking.com, Gother, Klook, Traveloka and "
        "Trip.com; Beautrium, Boots, EVEANDBOY, Sephora and Watsons; and the listed fashion and "
        "sports brands in department-store plazas.",
        "Counted by transaction date, 11th – 10th, whatever statement the row bills on (AEON's "
        "call centre, 2026-10-24).",
        "Only on the registered card — AEON World Mastercard — and the supplements under it.",
        "Only spend from the day registration completes counts (AEON THAI MOBILE or aeon.co.th, "
        "once for the campaign).",
        "Restaurants aren't linked automatically; link one by hand and it counts.",
        "A cycle whose spend runs past twice the credit limit earns nothing.",
    )
    rules: ClassVar = (
        Rule("Paid through an e-wallet", _WALLET.pattern),
        Rule("Installments", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Spending abroad or charged in a foreign currency",
             test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
        Rule("Top-up cards, cash coupons, vouchers and gift cards; part-paid deposits; cancelled or "
             "refunded charges", r"GIFT ?CARD|VOUCHER|COUPON"),
    )
    crediting: ClassVar = (
        "Within 120 days after each cycle ends, to the primary card.",
        "Caps: ฿340 a cycle and ฿2,720 for the campaign, per person.",
    )
