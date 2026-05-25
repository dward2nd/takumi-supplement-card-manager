---
tags: [database, takumi, transactions]
owner: takumi
role: transactions
---

# Takumi — Transactions (`รายการใช้จ่ายผ่านบัตรของเว็บ`)

Every individual purchase Takumi makes on his own cards.

- **Notion URL**: https://www.notion.so/dward2nd/1aacb755f0f18144b50dd2477403fc7d
- **Collection ID**: `1aacb755-f0f1-81dc-8e9f-000b20891025`
- **Parent page**: `💳 รายการใช้จ่ายผ่านบัตรของเว็บ` → `Personal Monetary Policy`
- **Last schema-verified**: 2026-05-19

## Properties

| Name (Notion)       | Type      | Notes |
|---------------------|-----------|-------|
| `Name`              | title     | Merchant or short description |
| `Card`              | relation → [[takumi-cards]] | The card used |
| `หมวดหมู่`            | relation → Categories DB    | **Takumi-only**: expense category. The Categories DB isn't yet documented here. |
| `ยอดชำระ`            | number (baht) | Transaction amount |
| `ใช้คะแนน`           | number (int)  | Points redeemed against this transaction |
| `Transaction Datetime` | datetime  | When the swipe / authorisation happened |
| `Process Date`      | date          | When the bank posted it. See [[../concepts/billing-cycle]] |
| `Bill Cycle Date`   | date          | Which billing cycle this lands on |
| `Due Date`          | date          | When payment is owed |
| `Note`              | text          |  |

### Status checkboxes (the [[../concepts/payment-lifecycle|payment lifecycle]])

- `Processed` — bank has posted the charge
- `ชำระแล้ว` — Takumi has paid the resulting bill
- `Credit Return` — this transaction was refunded/charged back

### Point multiplier checkboxes — see [[../concepts/points-and-multipliers]]

- `×0`, `×2`, **`×3`** (Takumi-only), `×4`, `×5`

Notably absent: `÷4` (which Baiboon and Nuta both have).

### Formulas

- `คะแนนที่ได้จริง` — actual points earned. See [[../formulas/points-realized]].
- `คะแนน unrealized` — unrealized points. See [[../formulas/points-unrealized]].

### Rollup

- `บาทต่อ 1 คะแนน` — from the related Card.

## Views

Five views: by transaction datetime, by process date, by card (relation grouping), by bill cycle date, and a donut chart aggregating `ยอดชำระ` by `หมวดหมู่` (the only chart view in the eight databases).

## Notable absences

- No `% cb` / `cashback` formula — both Baiboon and Nuta have them; Takumi does not.
- No `÷4` multiplier.
