---
tags: [database, takumi, cards]
owner: takumi
role: cards
---

# Takumi — Cards (`สรุปบัตรและสินเชื่อของเว็บ`)

The catalogue of every credit card and loan product that lists [[../people/takumi|Takumi]] as the primary holder.

- **Notion URL**: https://www.notion.so/dward2nd/1aacb755f0f181f1bcfedc4a42ab6f27
- **Collection ID**: `1aacb755-f0f1-818a-a284-000b17d155de`
- **Parent page**: `💳 รายการใช้จ่ายผ่านบัตรของเว็บ` → `Personal Monetary Policy`
- **Last schema-verified**: 2026-05-19

## Properties

| Name (Notion)             | Type     | Notes |
|---------------------------|----------|-------|
| `Name`                    | title    | Card product name (e.g. `UOB Premier`) |
| `Card Network`            | select   | `JCB` / `Mastercard` / `VISA` / `UnionPay` / `Unspecified` — see [[../concepts/card-network]] |
| `ความพรีเมียม`              | select   | `สูง (Signature)` / `ธรรมดา (Platinum)` / `ไม่มี` — see [[../concepts/premium-tier]] |
| `Date`                    | date     | Card open/issue date (sparse) |
| `Note`                    | text     | Free-form notes |
| `บาทต่อ 1 คะแนน`            | number   | Baht spent per 1 reward point. Drives [[../formulas/points-realized]] via rollup. |
| `ให้คะแนนตามรอบบิล`         | checkbox | If true, points are awarded per billing cycle rather than per transaction |
| `วงเงินที่ได้`               | number (baht) | Credit limit assigned to this card (the user's share, since supplement holders share it) |
| `รายการใช้จ่ายผ่านบัตรของเว็บ` | relation → Transactions | The two-way relation to [[takumi-transactions]] |

### Rollups (from Transactions)

| Name                 | Aggregation     | Source field on Transactions |
|----------------------|-----------------|------------------------------|
| `คะแนนสะสม`           | sum             | `คะแนนที่ได้จริง` (formula)        |
| `ยอดค้างชำระ rollup`   | sum             | `ยอดชำระ` (when unpaid)         |
| `วันครบกำหนดชำระ`      | latest_date     | `Due Date`                    |
| `วันตัดรอบบิล`          | latest_date     | `Bill Cycle Date`              |

### Formulas

- `ยอดค้างชำระ` — outstanding balance. Decoded in [[../formulas/outstanding-balance]].

## What's NOT here (vs supplement holders)

- **No `ธนาคาร/บริษัท`** select. Baiboon's and Nuta's Cards DBs do have an issuer column. See [[../concepts/known-divergences]].
- No `% cb` or cashback model. (Nuta has these.)

## Views

A single sortable table view (`ตาราง`) and a timeline view by `วันตัดรอบบิล`. No board view in this database.

## Relations diagram

```
[Cards]  ⟷ relation ⟷  [Transactions]
   ▲                       │
   └── rollups ─────────────┘
```
