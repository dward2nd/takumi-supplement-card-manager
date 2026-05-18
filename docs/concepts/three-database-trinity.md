---
tags: [concept, structural]
---

# The three-database trinity

Each supplement holder gets three databases that together model their card universe:

```
       ┌────────────────────────┐
       │       Cards (DB)       │     one row per card product
       │  e.g. UOB Premier      │     (with limit, network, points rate)
       └─────────┬──────────────┘
                 │
            two-way relation
                 │
       ┌─────────▼──────────────┐
       │  Transactions (DB)     │     one row per swipe
       │  -- merchant, amount,  │
       │     dates, points      │
       └────────────────────────┘

       ┌────────────────────────┐
       │       Bills (DB)       │     one row per monthly statement
       │  -- Card (SELECT!)     │     (with PDF attachments,
       │     amount, จ่ายแล้ว    │      payment evidence)
       └────────────────────────┘
```

## Cards ⟷ Transactions

A proper Notion relation, two-way. The Cards DB rolls up totals (`คะแนนสะสม`, `ยอดค้างชำระ rollup`) from related transactions. This is the workhorse axis.

## Bills

Standalone. Its `Card` field is a **`select`** (a hardcoded text list), not a relation to Cards. This is a deliberate denormalization with practical downsides — see [[known-divergences]]. The future app should make this a foreign key.

## Variants

- [[../people/takumi|Takumi]] doesn't have a Bills DB at all — only Cards + Transactions.
- All three holders have Cards + Transactions with the same overall shape, modulo person-specific extras: `หมวดหมู่` (Takumi), `% cb` + `cashback` formula (Nuta).

## Why a trinity and not one big DB?

Different rows live at different cadences and have different attachment surfaces:

- **Cards** change rarely (you open/close a card maybe yearly).
- **Transactions** are high-volume, fine-grained, point-aware.
- **Bills** are monthly, document-bearing (PDFs + payment receipts), and the natural unit of "have I paid this month yet?".

Squashing them into one DB would make views and rollups much harder.
