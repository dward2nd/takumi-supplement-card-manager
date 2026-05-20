---
tags: [concept, rewards, nuta-only]
---

# Cashback model (Nuta-only)

Only [[../people/nuta|Nuta]]'s transactions track cashback. Two fields are involved:

| Field      | Type                       | Where |
|------------|----------------------------|-------|
| `% cb`     | number (percent, 1 decimal) | [[../databases/nuta-transactions]] |
| `cashback` | formula                    | [[../databases/nuta-transactions]] |

The formula body lives in Notion at a `formulaCode://` URL; decode in [[../formulas/cashback]] when you need it.

## Likely semantics (to be verified)

`% cb × ยอดชำระ ÷ 100` — the baht cashback for the row, possibly gated on `Processed = true` and/or `Credit Return = false`. Don't assume; read the formula.

## Why only Nuta has this

Inferred: one or more of Nuta's cards is a cashback-style card (rather than points-style), and tracking cashback alongside points-rewards in the same row was cleaner than splitting into separate databases.

If Baiboon ever picks up a cashback card, the schema can be cloned from Nuta — both columns are additive (don't affect existing rows when added).

## Migration consideration

In the [[../future-app/data-model-target|future app]], cashback and points should likely be modelled as polymorphic "rewards" per transaction rather than as parallel column families.

## Phase 2 model (resolved 2026-05-21)

Confirmed in [[../future-app/product-shape]]:

- Cashback is **no longer Nuta-only** — it joins multipliers inside `Transaction.rewardRules` (a JSON array on `Transaction`). Any holder's transaction can carry `{type: "cashback", percent: 5}` alongside or instead of a multiplier.
- The cashback `formula` field disappears — the new app **computes** the cashback baht in code on read, replacing the Notion formula (see [[../formulas/cashback]] for the historical formula body).
- **Auto-classify with override** — per-card cashback-tier rules (e.g. UOB One's 10% / 5% / 1%) get applied automatically when a transaction is added, based on the merchant string. The user can override per row when the auto-tier is wrong.
