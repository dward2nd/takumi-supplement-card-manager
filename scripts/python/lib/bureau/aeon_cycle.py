"""AEONTransactionDated — an AEON statement-cycle quota counted by transaction date, 11th – 10th.

deterministic + idempotent — pure functions of the transactions handed in.

AEON counts a row in the period it was made in, strictly 11th – 10th, whatever
statement it bills on (AEON's call centre, 2026-10-24, for NTW1). AEON posts
purchases one to four days late, so a row dated the 9th or 10th often bills a
cycle later but still counts in the earlier period. AEON Rabbit's 5% follows
the same rule: its 2 Oct 2026 credit (฿100.25) matches it to the satang, and
reading the Bill Cycle Date (฿100.75) doesn't (user, 2026-10-29).

Mix in before the payout shape: `class NTW1Promotion(AEONTransactionDated, LadderPromotion)`.
The Bureau row carries the period AEON counts: Start = the day after the
previous closing date, End = the closing date itself (`2026M10` runs 11 Sep –
10 Oct), and the tracker reads `11 Sep—10 Oct` (user, 2026-10-29). Other cycle
rows end the day before their BC date (`cycle_billed_on`); here End is the BC
date, so `billed_on` returns it unchanged and the Name and tracker date stay
as they were.
"""

from __future__ import annotations

import datetime as dt

from ..bill_cycle import pattern_for_card
from .base import BasePromotion, Tx

_DAY = dt.timedelta(days=1)


class AEONTransactionDated(BasePromotion):
    # A row belongs to the period closing on the first AEON closing date (the 10th)
    # on or after its transaction date, not the one its Bill Cycle Date names.
    def _closing(self, tx: Tx) -> dt.date:
        return pattern_for_card(tx.card or self.cards[0]).active(tx.day)[0]

    def billed_on(self, end: dt.date) -> dt.date:
        return end

    def covers(self, start: dt.date, end: dt.date, tx: Tx) -> bool:
        first, last = self.campaign
        return self._closing(tx) == end and first <= tx.day and (last is None or tx.day <= last)

    def candidate_filter(self, start: dt.date, end: dt.date) -> list[dict]:
        # A superset, a day wide each side (timed rows read back as datetimes); `covers` decides.
        return [{"property": "Transaction Datetime", "date": {"on_or_after": (start - _DAY).isoformat()}},
                {"property": "Transaction Datetime", "date": {"on_or_before": (end + _DAY).isoformat()}}]

    def period_for(self, tx: Tx) -> tuple[dt.date, dt.date] | None:
        first, last = self.campaign
        if tx.day < first or (last is not None and tx.day > last):
            return None
        closing = self._closing(tx)
        previous, _ = pattern_for_card(tx.card or self.cards[0]).closed(closing)
        return self._clip_cycle(previous + _DAY, closing)
