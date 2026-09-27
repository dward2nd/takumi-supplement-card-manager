"""Promotion Bureau: household-wide tracking of bank promotions.

deterministic + idempotent — the registry is static; see each module.

The Bureau (a Notion DB) keeps one row per **quota period**: the window a
bank counts a limit over (a calendar month, a statement cycle, or the whole
campaign). The row is named `<year>M<month> — <campaign>`, where the month is
the calendar month, the month of the cycle's closing date, or the campaign's
first month. Every holder's qualifying transactions link to it.

Modules:
  base       BasePromotion (identity, matching, screening, FCFS walk, page)
             and CashbackPromotion (baht shares, trackers, the `% cb` rule)
  ladder     LadderPromotion: steps of pooled spend
  capped     CreditCapPromotion: a per-row rate until a pooled credit cap
  nw3        Krungsri First Choice NW3 (ladder), Jul–Sep 2026
  store      Notion reads/writes for Bureau rows, linked transactions, trackers

To add a campaign: subclass the shape that fits (or BasePromotion for a new
shape) in a new module, then list it in PROMOTIONS below.
"""

from __future__ import annotations

import datetime as dt

from .base import (CASHBACK, ELIGIBLE, EXCLUDED, POINTS, UNCERTAIN, Allocation, BasePromotion,
                   CashbackPromotion, Rule, Tx, TxCredit)
from .capped import CreditCapPromotion
from .ladder import LadderPromotion, Tranche
from .nw3 import NW3Promotion

PROMOTIONS: tuple[type[BasePromotion], ...] = (NW3Promotion,)


def promotion_for(bureau_name: str, start: dt.date, end: dt.date) -> BasePromotion:
    """The campaign a Bureau row belongs to, by its Name and its period."""
    hits = [cls for cls in PROMOTIONS if cls.matches(bureau_name, start, end)]
    if len(hits) != 1:
        known = ", ".join(f"{c.__name__} ({c.name_pattern or c.code})" for c in PROMOTIONS)
        raise LookupError(
            f"{len(hits)} registered promotions match {bureau_name!r} ({start}→{end}); "
            f"known: {known}. Add a BasePromotion subclass in lib/bureau/ for a new campaign.")
    return hits[0]()


__all__ = ["CASHBACK", "ELIGIBLE", "EXCLUDED", "POINTS", "UNCERTAIN", "Allocation", "BasePromotion",
           "CashbackPromotion", "CreditCapPromotion", "LadderPromotion", "NW3Promotion",
           "PROMOTIONS", "Rule", "Tranche", "Tx", "TxCredit", "promotion_for"]
