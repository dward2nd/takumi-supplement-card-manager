---
tags: [database, baiboon, transactions]
owner: baiboon
role: transactions
---

# Baiboon — Transactions (`รายการใช้จ่ายผ่านบัตรของใบบุญ`)

Every purchase Baiboon makes on his/her supplement cards.

- **Notion URL**: https://www.notion.so/dward2nd/181cb755f0f18120a062d01ab54728b4
- **Collection ID**: `181cb755-f0f1-8167-b5b6-000bc6d47469`
- **Parent page**: `💳 รายการใช้จ่ายผ่านบัตรของใบบุญ` → `Personal Monetary Policy`
- **Last schema-verified**: 2026-05-19

## Properties

| Name (Notion)       | Type      | Notes |
|---------------------|-----------|-------|
| `Name`              | title     | Merchant or short description |
| `Card`              | relation → [[baiboon-cards]] |  |
| `ยอดชำระ`            | number (baht) | Transaction amount |
| `ใช้คะแนน`           | number (int)  | Points redeemed |
| `Transaction Datetime` | datetime  |  |
| `Process Date`      | date          |  |
| `Bill Cycle Date`   | date          |  |
| `Due Date`          | date          |  |
| `Note`              | text          |  |
| `% cb`              | number (percent) | Cashback percentage applied to this transaction. Added 2026-05-25 — Baiboon's DS now mirrors Nuta's cashback setup. See [[../concepts/cashback]]. |

### Status checkboxes — see [[../concepts/payment-lifecycle]]

- `Processed`, `ชำระแล้ว`, `Credit Return`

### Point multiplier checkboxes — see [[../concepts/points-and-multipliers]]

- `×0`, `×2`, `×4`, `×5`, `÷4`

Notably absent: `×3` (Takumi-only).

### Formulas

- `คะแนนที่ได้จริง` — [[../formulas/points-realized]]
- `คะแนน unrealized` — [[../formulas/points-unrealized]]
- `cashback` — `% cb` × `ยอดชำระ`. Added 2026-05-25; see [[../formulas/cashback]].

### Rollup

- `บาทต่อ 1 คะแนน` — from the related Card.

## Notable absences

- **No `หมวดหมู่` (category)** — that's Takumi-only.

## Views

Five views: by `Transaction Datetime`, by `Process Date`, by Card (relation grouping), by `Bill Cycle Date`, and a "no grouping" view filtered to `ชำระแล้ว`.
