---
tags: [database, baiboon, cards]
owner: baiboon
role: cards
---

# Baiboon — Cards (`สรุปบัตรและสินเชื่อที่ใบบุญถือ`)

The catalogue of supplement cards held by [[../people/baiboon|Baiboon]] on [[../people/takumi|Takumi]]'s accounts.

- **Notion URL**: https://www.notion.so/dward2nd/181cb755f0f180078c70c5bfe8e86c74
- **Collection ID**: `99bb5ba6-79b1-47e2-9b8f-fa3102d5b294`
- **Parent page**: `💳 รายการใช้จ่ายผ่านบัตรของใบบุญ` → `Personal Monetary Policy`
- **Last schema-verified**: 2026-05-19

## Properties

| Name (Notion)             | Type     | Notes |
|---------------------------|----------|-------|
| `Name`                    | title    | Card product name |
| `Card Network`            | select   | `JCB` / `Mastercard` / `VISA` / `UnionPay` / `Unspecified` |
| `ความพรีเมียม`              | select   | `สูง (Signature)` / `ธรรมดา (Platinum)` / `ไม่มี` |
| `ธนาคาร/บริษัท`             | select   | **Issuer**: `UOB` / `Shopee` / `บัตรกรุงศรี` / `KTC`. **Not present in [[takumi-cards]]**. |
| `Date`                    | date     |  |
| `Note`                    | text     |  |
| `บาทต่อ 1 คะแนน`            | number (baht) | Baht spent per 1 reward point |
| `ให้คะแนนตามรอบบิล`         | checkbox |  |
| `วงเงินที่ได้`               | number (baht) | Credit limit |
| `รายการใช้จ่ายผ่านบัตรของใบบุญ` | relation → [[baiboon-transactions]] |  |

### Rollups (from Transactions)

| Name                 | Aggregation     |
|----------------------|-----------------|
| `คะแนนสะสม`           | sum of `คะแนนที่ได้จริง` |
| `ยอดค้างชำระ rollup`   | sum of `ยอดชำระ`     |
| `วันครบกำหนดชำระ`      | latest `Due Date`  |
| `วันตัดรอบบิล`          | latest `Bill Cycle Date` |

### Formulas

- `ยอดค้างชำระ` — see [[../formulas/outstanding-balance]].

## Views

`ตาราง` (table), `บอร์ด` (board grouped by `ธนาคาร/บริษัท`), `การ์ต` (gallery grouped by issuer), and `ไทม์ไลน์วันตัดรอบบิลและวันครบกำหนดชำระ` (timeline by bill cycle → due date).

## Note on the supplement model

Each row here represents a *supplement card* on a Takumi-owned account. The credit limit (`วงเงินที่ได้`) is the share allocated to Baiboon, not the underlying account's total. See [[../concepts/supplement-card-model]].
