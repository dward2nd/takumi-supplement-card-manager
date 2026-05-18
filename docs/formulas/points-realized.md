---
tags: [formula]
---

# `คะแนนที่ได้จริง` — actual points earned (per transaction)

A formula property on every Transactions DB. Computes how many reward points this transaction actually earns, factoring in:

- `ยอดชำระ` (transaction amount in baht)
- `บาทต่อ 1 คะแนน` (rolled-up from the related Card)
- Multiplier checkboxes — see [[../concepts/points-and-multipliers]]
- Possibly status flags from [[../concepts/payment-lifecycle]] (e.g. zero out if `Credit Return = true` or `Processed = false`)

## Where to find the body

Each Transactions DB stores its own copy of this formula at a `formulaCode://` URL:

- Takumi: `formulaCode://1aacb755-f0f1-81dc-8e9f-000b20891025/aGRceg`
- Baiboon: `formulaCode://181cb755-f0f1-8167-b5b6-000bc6d47469/aGRceg`
- Nuta: `formulaCode://2a1cb755-f0f1-8110-9795-000bf7d48b4f/aGRceg`

Fetch via `mcp__notion__notion-fetch` against the parent DB and inspect the schema's `formulaCode://` link, then resolve.

## Decoded body

_TBD — fetch from Notion when the user wants formula-level reasoning._

## Likely shape (hypothesis, verify before quoting)

```
if Credit Return then 0
else if Processed = false then 0
else floor(ยอดชำระ / บาทต่อ 1 คะแนน) × <effective multiplier>
```

where `<effective multiplier>` resolves the checkbox family (`×0`/`×2`/`×3`/`×4`/`×5`/`÷4`). The three copies may not be identical — Takumi has `×3` but no `÷4`; supplements have `÷4` but no `×3`.

## Why three copies

Notion formula properties are per-database. There's no way to share a formula across collections, so each Transactions DB has its own. This is a phase-2 consolidation candidate.
