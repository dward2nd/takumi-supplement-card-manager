"""How much of each tracked campaign the household has used in a month — the plan's "ใช้ไปแล้ว" lines.

deterministic + idempotent — reads the Promotion Bureau only.

A catalogue's spending plan ranks cards by what they still return this month,
so it needs each campaign's pooled spend, credit so far and cap. Every Bureau
row whose period overlaps the month is reported, with its campaign's cap where
the payout shape has one (`cap` on a credit-cap or discount campaign).
"""

from __future__ import annotations

import calendar
import datetime as dt
from decimal import Decimal

from ..bureau import promotion_for, store


def month_bounds(month: str) -> tuple[dt.date, dt.date]:
    """`2026-10` → (1 Oct, 31 Oct)."""
    y, m = (int(x) for x in month.split("-"))
    return dt.date(y, m, 1), dt.date(y, m, calendar.monthrange(y, m)[1])


def usage(month: str) -> list[dict]:
    first, last = month_bounds(month)
    out = []
    for row in sorted(store.all_rows(), key=lambda r: r.name):
        if row.end < first or row.start > last:
            continue
        try:
            promo = promotion_for(row.name, row.start, row.end)
        except LookupError:
            continue
        cap = getattr(promo, "cap", None)
        credit = row.total or Decimal(0)
        out.append({
            "bureau": row.name,
            "issuer": row.issuer or promo.issuer(),
            "cards": list(promo.cards),
            "period": [row.start.isoformat(), row.end.isoformat()],
            "pooled_spend": float(sum(row.rollups.values(), Decimal(0))),
            "credit": float(credit),
            "cap": None if cap is None else float(cap),
            "left": None if cap is None else float(max(Decimal(cap) - credit, Decimal(0))),
            "shares": {k: float(v) for k, v in row.shares.items() if v},
            **({"quota_gone": row.quota_gone.isoformat()} if row.quota_gone else {}),
        })
    return out
