"""Reward points per ledger row — the `คะแนนที่ได้จริง` formula, in code.

deterministic + idempotent — pure functions.

Notion computes a row's points as floor(ยอดชำระ / บาทต่อ 1 คะแนน) × multiplier
× คะแนนต่อ 1 หน่วย, the multiplier being the first ticked box in the order ×0,
÷4, ×2, ×3, ×4, ×5, ×6 (none ticked = ×1); the supplements' copy wraps the
first two factors in an outer floor for ÷4 (docs/formulas/points-realized.md).
`คะแนนต่อ 1 หน่วย` (points per unit, a Cards field; empty = 1) is applied after
that floor, so a card can earn fractions: Lotus's Beyond pays 0.25 coin a ฿50
block, and ×6 at Lotus's (2026-10-05). UOB's statements agree line by line
(Aug/Sep 2026), so a statement line split across several ledger rows can lose
points to rounding — /record-statement adds those back on the principal
holder's ledger.
"""

from __future__ import annotations

import math
from decimal import Decimal

# Formula precedence: the first ticked box wins.
MULTIPLIER_FACTORS: dict[str, Decimal] = {
    "×0": Decimal(0), "÷4": Decimal("0.25"), "×2": Decimal(2), "×3": Decimal(3), "×4": Decimal(4), "×5": Decimal(5),
    "×6": Decimal(6),
}

# Cards field: points one `บาทต่อ 1 คะแนน` block earns at ×1. Empty (or 0) = 1.
PER_UNIT = "คะแนนต่อ 1 หน่วย"


def checked_multiplier(props: dict) -> str | None:
    """The multiplier box a Transactions page has ticked (formula precedence), or None for ×1."""
    return next((m for m in MULTIPLIER_FACTORS if (props.get(m) or {}).get("checkbox")), None)


def per_unit(card_props: dict) -> Decimal:
    """A card page's `คะแนนต่อ 1 หน่วย`, as the formula reads it: anything not above 0 is 1."""
    v = (card_props.get(PER_UNIT) or {}).get("number")
    return Decimal(str(v)) if v and v > 0 else Decimal(1)


def as_points(value) -> int | float:
    """A points figure as a plain number: whole numbers stay int, coins keep their fraction."""
    d = Decimal(str(value or 0)).quantize(Decimal("0.01"))
    return int(d) if d == d.to_integral_value() else float(d)


def row_points(amount, baht_per_point, multiplier: str | None, unit=1) -> int | float:
    """Points a row earns: floor(floor(amount / baht per point) × multiplier) × points per unit."""
    if not baht_per_point or amount is None or Decimal(str(amount)) <= 0:
        return 0
    base = math.floor(Decimal(str(amount)) / Decimal(str(baht_per_point)))
    return as_points(math.floor(base * MULTIPLIER_FACTORS.get(multiplier, Decimal(1))) * Decimal(str(unit)))
