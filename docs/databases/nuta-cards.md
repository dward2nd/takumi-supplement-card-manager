---
tags: [database, nuta, cards]
owner: nuta
role: cards
---

# Nuta — Cards (`สรุปบัตรและสินเชื่อที่นุตาถือ`)

The catalogue of supplement cards held by [[../people/nuta|Nuta]] on [[../people/takumi|Takumi]]'s accounts.

- **Notion URL**: https://www.notion.so/dward2nd/2a1cb755f0f18112a5a8d1c482c68f67
- **Collection ID**: `2a1cb755-f0f1-8188-9b00-000b5fa448b8`
- **Parent page**: `💳 รายการใช้จ่ายผ่านบัตรของนุตา` → `Personal Monetary Policy`
- **Last schema-verified**: 2026-05-19

## Properties

Schema is identical to [[baiboon-cards]] (modulo the relation target pointing at [[nuta-transactions]] instead).

| Name (Notion)             | Type     | Notes |
|---------------------------|----------|-------|
| `Name`                    | title    |  |
| `Card Network`            | select   | `JCB` / `Mastercard` / `VISA` / `UnionPay` / `Unspecified` |
| `ความพรีเมียม`              | select   | `สูง (Signature)` / `ธรรมดา (Platinum)` / `ไม่มี` |
| `ธนาคาร/บริษัท`             | select   | `UOB` / `Shopee` / `บัตรกรุงศรี` / `KTC` |
| `Date`                    | date     |  |
| `Note`                    | text     |  |
| `บาทต่อ 1 คะแนน`            | number (baht) |  |
| `ให้คะแนนตามรอบบิล`         | checkbox |  |
| `วงเงินที่ได้`               | number (baht) |  |
| `รายการใช้จ่ายผ่านบัตรของใบบุญ` *(internal label, points at Nuta's transactions)* | relation → [[nuta-transactions]] | Note the property label still says "ใบบุญ" — likely a copy-paste artefact in Notion. |

### Rollups

Same shape as Baiboon's: `คะแนนสะสม` (sum of `คะแนนที่ได้จริง`), `ยอดค้างชำระ rollup` (sum of `ยอดชำระ`), `วันครบกำหนดชำระ` (latest `Due Date`), `วันตัดรอบบิล` (latest `Bill Cycle Date`).

### Formulas

- `ยอดค้างชำระ` — [[../formulas/outstanding-balance]]

## Card products observed (vs Baiboon)

Nuta-only: `AEON UnionPay`, `CardX JCB`. Baiboon-only: `Krungsri NOW`, `Lotus's Beyond`, `ttb so smart`. See [[../cards/_stubs]] for the full union.

## Views

Same four as Baiboon: `ตาราง`, `บอร์ด` (by `ธนาคาร/บริษัท`), `การ์ต` (gallery), `ไทม์ไลน์วันตัดรอบบิลและวันครบกำหนดชำระ`.
