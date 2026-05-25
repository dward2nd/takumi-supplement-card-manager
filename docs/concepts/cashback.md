---
tags: [concept, rewards]
---

# Cashback model

[[../people/baiboon|Baiboon]]'s and [[../people/nuta|Nuta]]'s transactions track cashback. Two fields are involved:

| Field      | Type                       | Where |
|------------|----------------------------|-------|
| `% cb`     | number (percent) | [[../databases/baiboon-transactions]], [[../databases/nuta-transactions]] |
| `cashback` | formula = `% cb` × `ยอดชำระ` | [[../databases/baiboon-transactions]], [[../databases/nuta-transactions]] |

[[../people/takumi|Takumi]]'s Transactions DS does not have these fields. The decoded formula body lives in [[../formulas/cashback]].

## Cashback values come from promotions

The `% cb` value on a transaction is the *output* of applying an active **promotion** to that transaction — not a permanent property of the card. The card's note links to the currently-active promo, which defines tier rules, merchant exclusions, installment treatment, and the cashback-crediting workflow. See [[promotions]] for the cross-cutting model and per-card promotion notes under [[../promotions/]].

When a row earns no cashback (no active promo, or the active promo excludes the row), **leave `% cb` unset** — never write an explicit `0`. Use `Note` to record the reason when it's beyond the card/promo's headline rule (foreign-in-THB, petrol-on-UOB, primary-card-swipe, etc.).

## Why Takumi doesn't have this (yet)

Takumi's setup predates the supplement-card model. Nuta's DS introduced cashback tracking; Baiboon's DS was extended to match on 2026-05-25. Takumi's can be cloned the same way if it ever needs it — both columns are additive (don't affect existing rows when added).

## Migration consideration

In the [[../future-app/data-model-target|future app]], cashback and points should likely be modelled as polymorphic "rewards" per transaction rather than as parallel column families.

## Phase 2 model (resolved 2026-05-21)

Confirmed in [[../future-app/product-shape]]:

- Cashback becomes universal — it joins multipliers inside `Transaction.rewardRules` (a JSON array on `Transaction`). Any holder's transaction (including Takumi's) can carry `{type: "cashback", percent: 5}` alongside or instead of a multiplier. (Baiboon and Nuta already track cashback in Notion as of 2026-05-25; phase 2 closes the gap for Takumi.)
- The cashback `formula` field disappears — the new app **computes** the cashback baht in code on read, replacing the Notion formula (see [[../formulas/cashback]] for the historical formula body).
- **Auto-classify with override** — per-card cashback-tier rules (e.g. UOB One's 10% / 5% / 1%) get applied automatically when a transaction is added, based on the merchant string. The user can override per row when the auto-tier is wrong.
