---
tags: [formula]
---

# `ยอดค้างชำระ` — outstanding balance (per card)

A formula property on every Cards DB. Computes the unpaid balance on this card, aggregated across the card's related transactions.

There's also a `ยอดค้างชำระ rollup` property on each Cards DB that simply `sum`s `ยอดชำระ` from related transactions. The *formula* version likely refines that by subtracting paid amounts or excluding `Credit Return` rows.

> **Phase 2**: this Notion formula is replaced by application code in the new app — see [[../future-app/product-shape#Rewards & computation]]. The body below is retained for reference and as a one-time decode target during phase-2 setup of the outstanding-balance engine.

## Where to find the body

- Takumi: `formulaCode://1aacb755-f0f1-818a-a284-000b17d155de/OjtEcQ`
- Baiboon: `formulaCode://99bb5ba6-79b1-47e2-9b8f-fa3102d5b294/OjtEcQ`
- Nuta: `formulaCode://2a1cb755-f0f1-8188-9b00-000b5fa448b8/OjtEcQ`

All three share the same suffix `OjtEcQ` — the formula bodies may genuinely be identical (this would be the cleanest case). Verify.

## Decoded body

_TBD — fetch from Notion when reconciling against bank statements._

## Likely shape (hypothesis)

```
sum(ยอดชำระ where ชำระแล้ว = false AND Credit Return = false)
```

i.e. only count transactions that are still owed by the holder and haven't been refunded. The Cards DB rollup `ยอดค้างชำระ rollup` lacks the `ชำระแล้ว` filter (rollups can't apply per-row filters easily) — so the formula likely fetches the rollup and adjusts, or iterates the relation.

## Used by views

The Cards DB tables sort by `ยอดค้างชำระ` descending — "what's the biggest open balance right now?" is the primary at-a-glance question.
