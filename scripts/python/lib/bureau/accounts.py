"""CardAccount / CardNumber — a campaign whose quota is per card account or card number, not per person.

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

`CardNumber` does the same per card number, for two holders' cards with one
title (KTC UnionPay …1346 and …2310).
"""

from __future__ import annotations

import datetime as dt
import re
from typing import ClassVar

from ..holders import primary
from ..points_account import PrincipalCardAccount, SupplementCardAccount
from .base import CASHBACK, BasePromotion, Tx, cycle_billed_on


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


class CardNumber(BasePromotion):
    """A quota per card number, for cards the Cards DBs title alike.

    A card network counts its limits per card number, and two holders' cards can
    share a title: Takumi's KTC UnionPay …1346 and Baiboon's own …2310 are both
    "KTC UnionPay", each with its own limits (user, 2026-09-30). Which ledger rows
    sit on a number is the statement's rule (`lib.points_account`): the
    principal's number carries his rows and the friends' `[บัตรหลัก]` shares, a
    supplement's number that holder's other rows. The number goes into the
    Bureau Name: `2026M9 — UnionPay QR …1346 cb 6%`.

    Mix in before the payout shape: `class UnionPayQR1346(CardNumber, UnionPayQR)`.
    """

    number: ClassVar[str]   # the last four digits, as the statement prints them
    holder: ClassVar[str]   # whose number it is

    @classmethod
    def account(cls) -> str:
        return f"…{cls.number}"

    @classmethod
    def on_card(cls, tx: Tx) -> bool:
        kind = PrincipalCardAccount if cls.holder == primary().key else SupplementCardAccount
        return kind(cls.cards[0], cls.holder).counts(tx.holder, tx.name)

    @classmethod
    def matches(cls, bureau_name: str, start: dt.date, end: dt.date) -> bool:
        pattern = rf"\b{re.escape(cls.code)} {re.escape(cls.account())}(?= cb | |$)"
        return bool(re.search(pattern, bureau_name)) and cls.within_campaign(start, end)

    def covers(self, start: dt.date, end: dt.date, tx: Tx) -> bool:
        return self.on_card(tx) and super().covers(start, end, tx)

    def period_for(self, tx: Tx) -> tuple[dt.date, dt.date] | None:
        return super().period_for(tx) if self.on_card(tx) else None

    def row_name(self, start: dt.date, end: dt.date) -> str:
        month = cycle_billed_on(end) if self.period_basis == "bill_cycle" else start
        kind = " cb" if self.reward == CASHBACK else ""
        return f"{month.year}M{month.month} — {self.code} {self.account()}{kind} {self.headline}"

    def tracker_title(self, start: dt.date, end: dt.date) -> str:
        return super().tracker_title(start, end).replace(f"{self.code} ", f"{self.code} {self.account()} ", 1)
