---
tags: [formula]
---

# `คะแนน unrealized` — expected-but-not-yet-banked points

A formula property on every Transactions DB. Likely captures points that *will* be earned once a condition is met (e.g. `Processed = true`, or end-of-cycle for cards with `ให้คะแนนตามรอบบิล = true`).

The complementary formula is [[points-realized]] (`คะแนนที่ได้จริง`). Together they cover the full "earnable points" surface per transaction.

## Where to find the body

- Takumi: `formulaCode://1aacb755-f0f1-81dc-8e9f-000b20891025/YW93ZA`
- Baiboon: `formulaCode://181cb755-f0f1-8167-b5b6-000bc6d47469/PGBrQw`
- Nuta: `formulaCode://2a1cb755-f0f1-8110-9795-000bf7d48b4f/PGBrQw`

Note: Takumi's URL suffix differs (`YW93ZA` vs `PGBrQw` for the supplements). The formulas may not be identical even where the column names match. Decode before quoting.

## Decoded body

_TBD — fetch from Notion when the user wants formula-level reasoning._

## Likely interaction with realized

For a typical card (per-transaction points):

```
unrealized = if Processed then 0 else <expected points>
realized   = if Processed then <expected points> else 0
```

For a `ให้คะแนนตามรอบบิล = true` card, the bank only awards points at cycle close, so `realized` stays 0 until then and `unrealized` is non-zero through the cycle.

Verify by fetching the formula body.
