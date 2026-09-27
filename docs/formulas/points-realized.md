---
tags: [formula]
---

# `คะแนนที่ได้จริง` — actual points earned (per transaction)

A formula property on every Transactions DB. Computes how many reward points this transaction actually earns, factoring in:

- `ยอดชำระ` (transaction amount in baht)
- `บาทต่อ 1 คะแนน` (baht per 1 point, rolled up from the related Card)
- Multiplier checkboxes — see [[../concepts/points-and-multipliers]]
- `Processed` — points don't count until the bank posts the charge
- `ใช้คะแนน` (points redeemed against this transaction)

The Cards DB rollup `คะแนนสะสม` is a plain `sum` of this property across the card's related transactions, so **this formula is the card's entire point balance**. Nothing else feeds it.

> **Phase 2**: this Notion formula is replaced by application code in the new app — see [[../future-app/product-shape#Rewards & computation]]. The body below is retained for reference and as a one-time decode target during phase-2 setup of the points engine.

## Where to find the body

Each Transactions DB stores its own copy at a `formulaCode://` URL:

- Takumi: `formulaCode://1aacb755-f0f1-81dc-8e9f-000b20891025/aGRceg`
- Baiboon: `formulaCode://181cb755-f0f1-8167-b5b6-000bc6d47469/aGRceg`
- Nuta: `formulaCode://2a1cb755-f0f1-8110-9795-000bf7d48b4f/aGRceg`

Read them through the Notion HTTP API instead — `GET /v1/data_sources/{id}` returns every formula's `expression` inline, no `formulaCode://` resolution needed.

## Decoded body

**Verified 2026-09-22** against all three data sources. The three copies are *not* identical — the supplements carry an extra outer `floor`.

Takumi:

```
if(prop("ยอดชำระ") > 0,
   floor(prop("ยอดชำระ") / sum(prop("บาทต่อ 1 คะแนน")))
     * ifs(prop("×0"), 0, prop("×2"), 2, prop("×3"), 3, prop("×4"), 4, prop("×5"), 5, 1)
     * if(prop("Processed"), 1, 0),
   0)
- if(empty(prop("ใช้คะแนน")), 0, prop("ใช้คะแนน"))
```

Baiboon and Nuta (identical to each other):

```
if(prop("ยอดชำระ") > 0,
   floor(floor(prop("ยอดชำระ") / sum(prop("บาทต่อ 1 คะแนน")))
     * ifs(prop("×0"), 0, prop("÷4"), 0.25, prop("×2"), 2, prop("×4"), 4, prop("×5"), 5, 1))
     * if(prop("Processed"), 1, 0),
   0)
- if(empty(prop("ใช้คะแนน")), 0, prop("ใช้คะแนน"))
```

## What the body actually says

1. **Only positive amounts earn.** `ยอดชำระ > 0` gates the whole earning term. Payment rows, cashback credits, and refunds — all entered as negative amounts — earn nothing. They still pass through the `ใช้คะแนน` subtraction below.
2. **Integer division first.** `floor(ยอดชำระ / บาทต่อ 1 คะแนน)` — points are floored *before* the multiplier applies, so a `×5` card multiplies the already-floored base, not the exact quotient.
3. **The multiplier is an `ifs` chain, so checkbox order is precedence.** `×0` wins over everything; then (supplements) `÷4`, then `×2`, `×4`, `×5`. Takumi's chain is `×0 → ×2 → ×3 → ×4 → ×5`. Ticking two boxes doesn't compound — the first match in that order wins. Unticked everywhere ⇒ `1`.
4. **The supplements' outer `floor` exists because of `÷4`.** `0.25` is the only fractional multiplier in the household, and it's the only reason an outer `floor` is needed. Takumi has no `÷4`, so his copy doesn't have one. This is why a `÷4` row earning 3 base points yields `floor(0.75)` = **0**, not 1.
5. **`Processed` gates earning, `Credit Return` does not.** The old hypothesis in this note guessed that a refunded row zeroes out. It doesn't — `Credit Return` appears only in [[points-unrealized]]. A refunded row keeps its realized points unless the user also unticks `Processed` or ticks `×0`.
6. **`ใช้คะแนน` is subtracted unconditionally**, outside the `ยอดชำระ > 0` gate. It is the only lever that can push a row's realized points negative, and it works on a row of any amount — including zero or negative. See [[../concepts/ledger-reset]], which exploits exactly this.

## Why three copies

Notion formula properties are per-database. There's no way to share a formula across collections, so each Transactions DB has its own — and, as the `÷4` divergence shows, they drift. This is a phase-2 consolidation candidate. See [[../concepts/known-divergences#4. Point multipliers diverge]].
