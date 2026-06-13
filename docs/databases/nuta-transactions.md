---
tags: [database, nuta, transactions]
owner: nuta
role: transactions
---

# Nuta — Transactions (`รายการใช้จ่ายผ่านบัตรของนุตา`)

Every purchase Nuta makes on her supplement cards. Schema mirrors Baiboon's — both track cashback via `% cb` + `cashback` formula. Takumi's DS has neither.

- **Notion URL**: https://www.notion.so/dward2nd/2a1cb755f0f181ea95d2e8fbec394921
- **Collection ID**: `2a1cb755-f0f1-8110-9795-000bf7d48b4f`
- **Parent page**: `💳 รายการใช้จ่ายผ่านบัตรของนุตา` → `Personal Monetary Policy`
- **Last schema-verified**: 2026-05-19

## Properties

| Name (Notion)          | Type                        | Notes                                                                                                                           |
| ---------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `Name`                 | title                       |                                                                                                                                 |
| `Card`                 | relation → [[nuta-cards]]   |                                                                                                                                 |
| `ยอดชำระ`              | number (baht)               |                                                                                                                                 |
| `ใช้คะแนน`             | number (int)                |                                                                                                                                 |
| `Transaction Datetime` | datetime                    |                                                                                                                                 |
| `Process Date`         | date                        |                                                                                                                                 |
| `Bill Cycle Date`      | date                        |                                                                                                                                 |
| `Due Date`             | date                        |                                                                                                                                 |
| `Note`                 | text                        |                                                                                                                                 |
| **`% cb`**             | number (percent, 1 decimal) | Cashback percentage applied to this transaction. Also exists on Baiboon's DS; absent on Takumi's. See [[../concepts/cashback]]. |

### Status checkboxes — see [[../concepts/payment-lifecycle]]

- `Processed`, `ชำระแล้ว`, `Credit Return`

### Point multiplier checkboxes — see [[../concepts/points-and-multipliers]]

- `×0`, `×2`, `×4`, `×5`, `÷4`

(No `×3` — that's Takumi-only.)

### Formulas

- `คะแนนที่ได้จริง` — [[../formulas/points-realized]]
- `คะแนน unrealized` — [[../formulas/points-unrealized]]
- **`cashback`** — also on Baiboon's DS; absent on Takumi's. See [[../formulas/cashback]].

### Rollup

- `บาทต่อ 1 คะแนน` — from the related Card.

## Cashback parity with Baiboon

The `% cb` × `cashback` pair lets Nuta track baht-cashback alongside point-rewards in the same row. Baiboon's DS now mirrors this (added 2026-05-25 from this template). Only Takumi's DS still lacks cashback.

## Views

Same four "axis" views (by transaction time, process time, card, bill cycle) plus an unfiltered "ไม่จำแนกเลย" table.
