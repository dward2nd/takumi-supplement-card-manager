"""UnionPay at the MRT — 15% off Blue and Purple Line fares, 16 Mar – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms verbatim in docs/sources/unionpay-mrt-terms-2026-10-09.txt (UnionPay's
page, promotion code 260309111895; BEM's page pid=9550): 15% off the normal
fare of every Blue or Purple Line trip paid by tapping a participating
UnionPay credit card at the gate, no minimum; at most ฿550 of discount per
card a month (pre-authorisations included); 86,000 discounts a month
nationwide, first come first served. No registration.

The statement shows the fare after the discount (user, 2026-10-09: "the
cashback is combined in the transaction (if eligible), not separated"), so
the shape is `InstantDiscountPromotion`. Fares are whole baht, so a
discounted settlement is 85% of a whole number: ฿50.15 is a ฿59 fare less
฿8.85. A whole-baht amount could be a multiple of ฿20 with 15% off (฿17 =
฿20 less ฿3, confirmed by the user for 11 Oct 2026).

Tracked from October 2026 on Takumi's AEON UnionPay …2918 (user, 2026-11-01),
the household's card that taps at the gate: the ฿550 is per card number,
and friends' `[บัตรหลัก]` taps on …2918 share it. Takumi and Baiboon pay with
KTC UnionPay by QR only, and a payment takes one UnionPay offer, so KTC
UnionPay isn't tracked here.

The terms count a trip by the date the bank posts the settlement, and one
settlement can bundle several trips. The ledger dates a row by the app's
transaction date, which is the period used here: the two differ only for a
settlement posting across a month end.

UnionPay's pool isn't in the offer API the QR offer uses (checked
2026-11-01), so `Quotas Exceeded Date` is set by hand from UnionPay's
announcements (`/sync-promotion` spec `quota_gone`).
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .accounts import CardNumber
from .base import Rule, Tx
from .instant import InstantDiscountPromotion
from .quota import AnnouncedPool

PAGE = "https://m.unionpayintl.com/cardholderServ/serviceCenter/merchant/1134436148216?type=1"
_MRT = re.compile(r"^MRT-BEM\b")
_COUNTER = r"TOP ?UP|TOPUP|เติมเงิน"


class UnionPayMRT(InstantDiscountPromotion):
    code = "UnionPay MRT"
    icon = "🚇"
    title = "UnionPay — 15% off MRT Blue and Purple Line fares by contactless tap"
    cards = ("AEON UnionPay",)
    campaign = (dt.date(2026, 3, 16), dt.date(2026, 12, 31))
    source_url = PAGE
    headline = "15%"

    rate = Decimal("0.15")
    cap = Decimal(550)
    per_slip = cap      # no limit per trip; the month's ฿550 is the only one
    per_day = 1_000     # nor per day
    quota = AnnouncedPool(url=PAGE)
    missed_causes = ("an undiscounted fare: a top-up or ticket at the counter, a card not tapped at the gate, "
                     "or the pool gone before Quotas Exceeded Date says")

    @property
    def authoritative_period(self) -> bool:
        # The discount is taken at the gate, so the month is the row's own date.
        return True

    def qualifies(self, tx: Tx) -> bool:
        return bool(_MRT.search(tx.merchant)) and not promotions.is_installment(tx.name)

    ladder_title = "Discount per trip"
    ladder_header = ("Trip", "Discount")
    ladder_rows: ClassVar = (
        ("Blue or Purple Line, UnionPay credit card tapped at the gate", "15% off the normal fare, no minimum"),
        ("Per card", "฿550 a month, pre-authorisations included"),
        ("UnionPay's pool", "86,000 discounts a month nationwide (860,000 over the campaign), first come first "
                            "served"),
    )
    inclusions: ClassVar = (
        "Per calendar month and per card number: Takumi's AEON UnionPay …2918, with any [บัตรหลัก] taps on it.",
        "No registration.",
        "The discount is in the charge: ยอดชำระ is the fare less 15%. ฿50.15 was a ฿59 fare with ฿8.85 off; "
        "฿17 a ฿20 fare with ฿3 off.",
    )
    rules: ClassVar = (
        Rule("Tickets bought or cards topped up at the counter", _COUNTER),
        Rule("A payment another UnionPay offer takes: one UnionPay offer per payment, the best one"),
        Rule("Refunds: only the amount paid is refunded, and the discount counts as used"),
    )
    crediting: ClassVar = (
        "None: UnionPay takes the discount off at the gate and AEON charges the rest. No % cb, no tracker "
        "rows, no credit rows.",
        "Quotas Exceeded Date is the day UnionPay's monthly pool ran out, set by hand from UnionPay's "
        "announcement. From that day nothing is discounted.",
    )
    split_text: ClassVar = (
        "Each discount belongs to whoever's trip it was, first come first served by Transaction Datetime, "
        "until the card's ฿550 or the pool runs out.",
        "A fare's net amount shows whether the discount was taken: ฿38.25 (85% of ฿45) was; ฿16 wasn't. A "
        "multiple of ฿17 reads as discounted (85% of a multiple of ฿20).",
    )


class UnionPayMRT2918(CardNumber, UnionPayMRT):
    number, holder = "2918", "takumi"


ACCOUNTS = (UnionPayMRT2918,)
