"""A campaign's shared pool, as the bank publishes it — and the day it ran out.

deterministic + idempotent — reads the bank's page; writes the Bureau row's
`Quotas Exceeded Date` only when it's empty (or set to what the caller passes), so a second
run writes nothing.

Some campaigns stop for everyone once a nationwide pool is spent: UnionPay QR
gives 12,000 discounts a month, and September 2026's were gone on 12 Sep. The
ledger can't show that, so the day goes on the Bureau row as `Quotas Exceeded
Date`, and the campaign's walk discounts nothing from it (`InstantDiscountPromotion`).

It gets there two ways:
  - a sync that finds the bank's page saying the pool is used up, inside the
    period, with nothing stored yet, writes today (Asia/Bangkok). That's when it
    was first seen, not when it ran out: a sync only runs when rows are written;
  - the user reads it off the bank's announcement (UnionPay's Facebook post)
    and it's passed in (`/sync-promotion` spec `quota_gone`), replacing a
    later sighting.

A campaign opts in with a `quota` source on its class (a `QuotaSource`).
"""

from __future__ import annotations

import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

from . import store
from .base import BasePromotion
from .store import QUOTA_GONE, BureauRow

BANGKOK = ZoneInfo("Asia/Bangkok")
LIVE, USED_UP, NOT_STARTED, UNLISTED = "live", "used up", "not started", "not listed"


@dataclass(frozen=True)
class QuotaStatus:
    state: str                 # LIVE, USED_UP, NOT_STARTED or UNLISTED
    left: Decimal | None       # the share of the pool left, when the page shows it
    ref: str | None            # the bank's own reference for the period (an offer number)
    url: str | None            # where a person can look
    checked: dt.datetime


class QuotaSource(ABC):
    name: str

    @abstractmethod
    def status(self, start: dt.date, end: dt.date) -> QuotaStatus:
        """The pool for the period `start`–`end`, as the bank's page shows it now."""


def observe(row: BureauRow, promo: BasePromotion, write, *, given: str | None = None
            ) -> tuple[dict[str, Any] | None, list[str]]:
    """Read the campaign's pool, record the day it ran out, and hand it to the campaign.

    Returns (the envelope's `quota` block, warnings); (None, []) for a campaign
    without a quota source.
    """
    source: QuotaSource | None = getattr(promo, "quota", None)
    if source is None:
        return None, []
    warnings: list[str] = []
    gone = row.quota_gone
    if given:
        day = dt.date.fromisoformat(given)
        if day != gone:
            write(f"Bureau {QUOTA_GONE}={day}", store.write_date, row.id, QUOTA_GONE, day)
            gone = day

    status = None
    try:
        status = source.status(row.start, row.end)
    except (OSError, ValueError, KeyError) as e:
        warnings.append(f"couldn't read {source.name}: {type(e).__name__}: {e} — {QUOTA_GONE} left as it is")

    if status is not None:
        today = status.checked.astimezone(BANGKOK).date()
        if status.state == USED_UP and gone is None:
            if row.start <= today <= row.end:
                write(f"Bureau {QUOTA_GONE}={today} (first seen used up on {source.name})",
                      store.write_date, row.id, QUOTA_GONE, today)
                gone = today
            else:
                warnings.append(f"{source.name} shows the pool used up, but the period is over and "
                                f"{QUOTA_GONE} is empty — set it from the bank's announcement "
                                f"(/sync-promotion `quota_gone`)")
        elif status.state == LIVE and gone is not None and gone <= today:
            warnings.append(f"{QUOTA_GONE} says {gone}, but {source.name} shows {status.left:.0%} of the "
                            f"pool left — check the date")

    promo.quota_gone = gone
    out: dict[str, Any] = {QUOTA_GONE: gone.isoformat() if gone else None}
    if status is not None:
        out |= {"page": status.state, "left": None if status.left is None else float(status.left),
                "checked": status.checked.astimezone(BANGKOK).isoformat(timespec="minutes"),
                "ref": status.ref, "url": status.url}
    return out, warnings
