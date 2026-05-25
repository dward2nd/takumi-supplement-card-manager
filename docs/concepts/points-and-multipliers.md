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

## Approximation caveat

The `×0/×2/×3/×4/×5/÷4` set is **not** the issuer's real earning rule — it's a **convenience approximation** chosen to be fast to click in Notion's fixed-checkbox UI and to cover the common Thai-credit-card promotional shapes. Real earning rules can be richer:

- **Fractional points** (a transaction earns `0.25 pts` per 50 ฿, not an integer multiple of a base rate). The Notion checkbox enum literally cannot express this. See [[../cards/lotuss-beyond]].
- **Per-merchant bonus tiers within a card** — the issuer awards different rates depending on the merchant string, not just on whether a promo checkbox is set. See [[../cards/lotuss-beyond]] (general vs at-Lotus) and [[../cards/uob-makro]] (general vs in-store Makro, with the `÷4` checkbox standing in for "this was an in-store-Makro swipe").
- **Conditional fall-back via the merchant string** — UOB Makro's `÷4` only applies when the transaction was physically read by Makro's in-store reader. TrueMoney intermediation (`TMN*…`) breaks that condition and reverts to the base rate. The checkbox alone doesn't encode the "TrueMoney breaks it" rule; the human entering the row has to know.

So the multiplier set is a **lossy projection** of the underlying rules. Where the gap matters, the per-card narrative note is the source of truth (`docs/cards/<card>.md`), not the Notion checkbox. The phase-2 app models the underlying rules directly as `RewardRule` JSON entries on `Transaction` — see [[../future-app/data-model-target]] and [[promotions]].
