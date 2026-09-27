"""Promotion Bureau: household-wide tracking of bank promotions.

deterministic + idempotent — the registry is static; see each module.

The Bureau (a Notion DB) keeps one row per promotion period and links every
holder's qualifying transactions to it. Each bank campaign is its own
`BasePromotion` subclass, because campaigns don't share a shape.

Modules:
  base   — BasePromotion (the contract), rule screening, FCFS allocation,
           the page summary
  nw3    — Krungsri First Choice NW3, Jul–Sep 2026
  store  — Notion reads/writes for Bureau rows, linked transactions, trackers

To add a campaign: subclass BasePromotion in a new module, then list it in
PROMOTIONS below.
"""

from __future__ import annotations

import datetime as dt

from .base import ELIGIBLE, EXCLUDED, UNCERTAIN, Allocation, BasePromotion, Rule, Tranche, Tx
from .nw3 import NW3Promotion

PROMOTIONS: tuple[type[BasePromotion], ...] = (NW3Promotion,)


def promotion_for(bureau_name: str, start: dt.date, end: dt.date) -> BasePromotion:
    """The campaign a Bureau row belongs to, by the code in its Name and its period."""
    hits = [cls for cls in PROMOTIONS if cls.matches(bureau_name, start, end)]
    if len(hits) != 1:
        known = ", ".join(f"{c.code} {c.campaign[0]}→{c.campaign[1]}" for c in PROMOTIONS)
        raise LookupError(
            f"{len(hits)} registered promotions match {bureau_name!r} ({start}→{end}); "
            f"known: {known}. Add a BasePromotion subclass in lib/bureau/ for a new campaign.")
    return hits[0]()


__all__ = ["ELIGIBLE", "EXCLUDED", "UNCERTAIN", "Allocation", "BasePromotion", "NW3Promotion",
           "PROMOTIONS", "Rule", "Tranche", "Tx", "promotion_for"]
