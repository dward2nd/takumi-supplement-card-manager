"""Reward points per ledger row — the `คะแนนที่ได้จริง` formula, in code.

deterministic + idempotent — pure functions.

Notion computes a row's points as floor(ยอดชำระ / บาทต่อ 1 คะแนน) × multiplier,
the multiplier being the first ticked box in the order ×0, ÷4, ×2, ×3, ×4, ×5
(none ticked = ×1); the supplements' copy wraps it in an outer floor for ÷4
(docs/formulas/points-realized.md). UOB's statements agree line by line (Aug/Sep
2026), so a statement line split across several ledger rows can lose points to
rounding — /record-statement adds those back on the principal holder's ledger.
"""

from __future__ import annotations

import math
from decimal import Decimal

# Formula precedence: the first ticked box wins.
MULTIPLIER_FACTORS: dict[str, Decimal] = {
    "×0": Decimal(0), "÷4": Decimal("0.25"), "×2": Decimal(2), "×3": Decimal(3), "×4": Decimal(4), "×5": Decimal(5),
}


def checked_multiplier(props: dict) -> str | None:
    """The multiplier box a Transactions page has ticked (formula precedence), or None for ×1."""
    return next((m for m in MULTIPLIER_FACTORS if (props.get(m) or {}).get("checkbox")), None)


def row_points(amount, baht_per_point, multiplier: str | None) -> int:
    """Points a row earns: floor(floor(amount / baht per point) × multiplier)."""
    if not baht_per_point or amount is None or Decimal(str(amount)) <= 0:
        return 0
    base = math.floor(Decimal(str(amount)) / Decimal(str(baht_per_point)))
    return math.floor(base * MULTIPLIER_FACTORS.get(multiplier, Decimal(1)))
