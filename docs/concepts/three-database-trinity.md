---
tags: [concept, structural]
---

# The three-database trinity

Each supplement holder gets three databases that together model their card universe:

```
         ┌──────────────────────────────┐
         │          Cards (DB)          │   one row per card product
         │  e.g. UOB Premier            │   (with limit, network, points rate)
         └────┬────────────────────▲────┘
              │                    │
       two-way relation     one-way relation
              │              (Bills → Cards)
              │                    │
┌─────────────▼──────────┐ ┌───────┴────────────────┐
│  Transactions (DB)     │ │       Bills (DB)       │
│  one row per swipe     │ │  one row per statement │
│  -- merchant, amount,  │ │  -- Card (relation)    │
│     dates, points      │ │     amount, จ่ายแล้ว,    │
│                        │ │     PDFs, slips        │
└────────────────────────┘ └────────────────────────┘
```

## Cards ⟷ Transactions

A proper Notion relation, two-way. The Cards DB rolls up totals (`คะแนนสะสม`, `ยอดค้างชำระ rollup`) from related transactions. This is the workhorse axis.

## Bills

Its `Card` field is a **one-way relation** to the holder's own Cards DB (since 2026-09-30), so there is no back-link column on Cards and no rollup from bills. Until then it was a **`select`** (a hardcoded text list). That SELECT survives as the legacy `Card (old select)` until the household's views move over. See [[known-divergences]] #1.

A bill still isn't linked to its transactions: the two meet on (card, `วันตัดรอบบิล` = `Bill Cycle Date`). See [[billing-cycle#Relation to Bills]].

## Variants

- [[../people/takumi|Takumi]] has had a Bills DB since 2026-09-27, but his bills are statement-driven (the bank's per-card total), not a sum of his own rows. See [[../databases/takumi-bills]].
- All three holders have Cards + Transactions with the same overall shape, modulo person-specific extras: `หมวดหมู่` (Takumi-only), `×3` (Takumi-only). `% cb` + `cashback` formula are on all three since Takumi's were added on 2026-09-28.

## Why a trinity and not one big DB?

Different rows live at different cadences and have different attachment surfaces:

- **Cards** change rarely (you open/close a card maybe yearly).
- **Transactions** are high-volume, fine-grained, point-aware.
- **Bills** are monthly, document-bearing (PDFs + payment receipts), and the natural unit of "have I paid this month yet?".

Squashing them into one DB would make views and rollups much harder.
