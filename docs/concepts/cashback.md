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
