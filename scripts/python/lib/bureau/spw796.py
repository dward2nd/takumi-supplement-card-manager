"""UOB SPW796 — "ช้อปออนไลน์ คุ้มทุกคลิก" (e-Commerce & e-Wallet), 1 Oct – 31 Dec 2026.

deterministic + idempotent — declarations only.

Terms read on 2026-10-01 from
https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/shopping-online-spw796-1226.page
(rendered from `…/shopping-online-spw796-1226.json`; ref 26UA303): EPW538 for
Q4 2026. The same ladder (฿100 per whole ฿5,000 pooled in the month, at most
฿200 a month and ฿600 for the campaign, per cardholder), the same nine apps
and the same exclusions. Registration (SMS `EC`, or Rewards+) must come before
the spend, within the campaign.
"""

from __future__ import annotations

import datetime as dt
from typing import ClassVar

from .epw538 import EPW538Promotion


class SPW796Promotion(EPW538Promotion):
    code = "SPW796"
    campaign = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
    source_url = ("https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/"
                  "shopping-online-spw796-1226.page")

    inclusions: ClassVar = (
        *EPW538Promotion.inclusions[:4],
        "Register once, before the spend and between 1 Oct and 31 Dec 2026: SMS \"EC <last 12 digits of "
        "the card>\" to 4545111, or Rewards+ in UOB TMRW. UOB Reserve and Infinite don't need to register.",
    )
    crediting: ClassVar = (
        "Within 60 days after 31 Dec 2026, into one of the primary cardholder's UOB cards; the bank "
        "picks which.",
        "Not combinable with other promotions; when promotions in the same merchant category overlap, "
        "the bank pays only the best one.",
    )
