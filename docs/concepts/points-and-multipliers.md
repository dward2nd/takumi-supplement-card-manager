---
tags: [concept, rewards]
---

# Point multipliers (`×0` `×2` `×3` `×4` `×5` `÷4`)

Reward points are modelled as **independent boolean multiplier columns**, not as a single number. Each transaction carries several checkbox flags that indicate which promotional rate applies, and the [[../formulas/points-realized|`คะแนนที่ได้จริง`]] formula combines them with the card's `บาทต่อ 1 คะแนน` rate to produce actual points earned.

## The set of multipliers, by person

| Multiplier | [[../people/takumi\|Takumi]] | [[../people/baiboon\|Baiboon]] | [[../people/nuta\|Nuta]] |
|------------|---------|---------|------|
| `×0`       | ✓        | ✓        | ✓     |
| `×2`       | ✓        | ✓        | ✓     |
| `×3`       | ✓        |          |       |
| `×4`       | ✓        | ✓        | ✓     |
| `×5`       | ✓        | ✓        | ✓     |
| `÷4`       |          | ✓        | ✓     |

So Takumi's transactions support `×3` but not `÷4`; supplement holders' transactions support `÷4` but not `×3`.

## Why boolean columns instead of one multiplier number

Two reasons inferred from the structure:

1. **Promo identity is preserved**. A `×5` is conceptually different from "five times the base rate" — it's a specific promo campaign. If you stored the resolved multiplier as `5.0`, you'd lose the trace.
2. **Multiple multipliers can co-apply** (or be considered independently for reconciliation). The schema permits more than one checkbox to be true on the same row; the formula must encode priority/combination rules. Decode in [[../formulas/points-realized]] when needed.

## Related fields on the transaction

- `ใช้คะแนน` — points *redeemed* against this transaction (separate axis from points earned).
- `คะแนนที่ได้จริง` (formula) — actual points earned this row.
- `คะแนน unrealized` (formula) — potential/expected points before some condition resolves (likely tied to `Processed` or `Credit Return`).

## On the Cards side

- `บาทต่อ 1 คะแนน` (baht per point) is the per-card base rate, rolled up into each transaction.
- `คะแนนสะสม` rolls up `คะแนนที่ได้จริง` across transactions.
- `ให้คะแนนตามรอบบิล` is a per-card checkbox: true if the bank awards points per billing cycle rather than per transaction (changes when "realized" happens).
