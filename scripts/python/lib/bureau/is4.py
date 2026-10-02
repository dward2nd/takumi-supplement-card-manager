"""Krungsri First Choice IS4 — insurance premiums, per slip, 1 Oct – 31 Dec 2026.

deterministic + idempotent — declarations only.

Terms read from https://www.firstchoice.co.th/promotion/insurance-creditcard
on 2026-10-01: IS3 again, for Oct–Dec. Each insurance slip earns on its own
(฿80 per whole ฿10,000 from ฿10,000, ฿100 per ฿10,000 from ฿100,000, ฿1,000 per
฿100,000 from ฿200,000), capped at ฿5,000 a month per primary account
(฿15,000 for the campaign, 3 × that). AIA, unit-linked, KGIB/LGIB/LLAB and
foreign-registered insurers are out, and IS4 spend can't also count toward NW4.
"""

from __future__ import annotations

import datetime as dt
from typing import ClassVar

from .is3 import IS3Promotion


class IS4Promotion(IS3Promotion):
    code = "IS4"
    campaign = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
    source_url = "https://www.firstchoice.co.th/promotion/insurance-creditcard"

    inclusions: ClassVar = (
        "Full-amount baht premiums of any kind — life (savings or pension), health, accident, car, "
        "home, travel, pet — first year or renewal, on the Krungsri First Choice Visa Platinum.",
        "Per slip: slips never add up. Dated by the transaction date.",
        "Supplements count toward the primary account (Takumi's), which the bank credits.",
        "Counts only after registration is confirmed, strictly before the spend: UCHOOSE → \"IS4\", "
        "or SMS \"IS4 <16-digit card no.>\" to 081-256-3333.",
        "IS4 spend never also counts toward NW4.",
    )
    crediting: ClassVar = (
        "Within 5 business days of the transaction, to the primary account; it shows on the monthly "
        "statement.",
    )
