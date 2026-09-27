---
tags: [formula]
---

# `คะแนน unrealized` — gross points before the `Processed` gate

A formula property on every Transactions DB. The complementary formula is [[points-realized]] (`คะแนนที่ได้จริง`).

Unlike realized points, this one feeds **no rollup** — no Cards DB property sums it. It exists for eyeballing a row in the table view.

> **Phase 2**: this Notion formula is replaced by application code in the new app — see [[../future-app/product-shape#Rewards & computation]]. The body below is retained for reference and as a one-time decode target during phase-2 setup of the points engine.

## Where to find the body

- Takumi: `formulaCode://1aacb755-f0f1-81dc-8e9f-000b20891025/YW93ZA`
- Baiboon: `formulaCode://181cb755-f0f1-8167-b5b6-000bc6d47469/PGBrQw`
- Nuta: `formulaCode://2a1cb755-f0f1-8110-9795-000bf7d48b4f/PGBrQw`

Read them through the Notion HTTP API instead — `GET /v1/data_sources/{id}` returns every formula's `expression` inline.

## Decoded body

**Verified 2026-09-22.** As with [[points-realized]], the supplements carry an extra outer `floor` (for `÷4` = 0.25) and Takumi does not.

Takumi:

```
if(prop("ยอดชำระ") > 0,
   floor(prop("ยอดชำระ") / sum(prop("บาทต่อ 1 คะแนน")))
     * ifs(prop("×0"), 0, prop("×2"), 2, prop("×3"), 3, prop("×4"), 4, prop("×5"), 5, 1),
   0)
+ if(prop("Credit Return"), prop("คะแนนที่ได้จริง"), 0)
```

Baiboon and Nuta (identical to each other):

```
if(prop("ยอดชำระ") > 0,
   floor(floor(prop("ยอดชำระ") / sum(prop("บาทต่อ 1 คะแนน")))
     * ifs(prop("×0"), 0, prop("÷4"), 0.25, prop("×2"), 2, prop("×4"), 4, prop("×5"), 5, 1)),
   0)
+ if(prop("Credit Return"), prop("คะแนนที่ได้จริง"), 0)
```

## The name is misleading

The first term is **identical** to the earning term in [[points-realized]] except that it omits `* if(Processed, 1, 0)` and the `- ใช้คะแนน` subtraction.

So this property does **not** mean "points still pending". It does not drop to zero once `Processed` is ticked — a posted row shows the same number in both columns (absent redemptions). Read it as **gross points this row is worth**, and read `คะแนนที่ได้จริง` as gross × posted − redeemed.

The earlier hypothesis in this note — an `if Processed then 0 else expected` split, and a `ให้คะแนนตามรอบบิล` interaction — is wrong on both counts. `ให้คะแนนตามรอบบิล` appears nowhere in either formula; it's a human-facing flag on the Cards DB only.

## The `Credit Return` term is unexplained

On a refunded row the formula *adds* that row's realized points on top of its gross points, roughly doubling the figure. It is not an offset — there's no negation. Intent unclear; it may be a half-finished clawback idea.

Since nothing rolls this property up, the quirk is cosmetic today. Don't replicate it in phase 2 without asking Takumi what it was for.
