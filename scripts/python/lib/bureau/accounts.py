"""CardAccount — a campaign whose quota is per primary card account, not per person.

deterministic + idempotent — naming only.

Krungsri caps its card campaigns per "หมายเลขบัญชีบัตรหลัก" (primary card
account number): each card product is its own account, with its own
registration and its own cap. September 2026 shows it: SUP1 paid ฿120 on
Krungsri JCB, NOW and Lady alike (`CB15_ SUP1 CAMPAIGN 1SEP26-30SEP26`), and
every Krungsri card is registered for every campaign, tracked per card (user,
2026-09-29).

So the Bureau keeps one row per card per period — `2026M9 — SUP1 Krungsri JCB
cb 3%` — and each card is a subclass naming its one card. The card goes into
the Bureau Name, the tracker titles and the matching, so four cards' rows never
collide.
"""

from __future__ import annotations

import datetime as dt
import re

from .base import CASHBACK, BasePromotion, cycle_billed_on


class CardAccount(BasePromotion):
    """Mix in before the payout shape: `class SUP1KrungsriJCB(CardAccount, SUP1Promotion)`."""

    @classmethod
    def account(cls) -> str:
        return cls.cards[0]

    @classmethod
    def matches(cls, bureau_name: str, start: dt.date, end: dt.date) -> bool:
        pattern = rf"\b{re.escape(cls.code)} {re.escape(cls.account())}(?= cb | |$)"
        return bool(re.search(pattern, bureau_name)) and cls.within_campaign(start, end)

    def row_name(self, start: dt.date, end: dt.date) -> str:
        month = cycle_billed_on(end) if self.period_basis == "bill_cycle" else start
        kind = " cb" if self.reward == CASHBACK else ""
        return f"{month.year}M{month.month} — {self.code} {self.account()}{kind} {self.headline}"

    def tracker_title(self, start: dt.date, end: dt.date) -> str:
        return super().tracker_title(start, end).replace(f"{self.code} ", f"{self.code} {self.account()} ", 1)
