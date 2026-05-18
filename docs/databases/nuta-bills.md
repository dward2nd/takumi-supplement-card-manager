---
tags: [database, nuta, bills]
owner: nuta
role: bills
---

# Nuta — Bills (`บิลเรียกเก็บค่าบัตรเครดิตของนุตา`)

One row per monthly statement for Nuta's supplement cards.

- **Notion URL**: https://www.notion.so/dward2nd/2a1cb755f0f1819fa870d11f243531b4
- **Collection ID**: `2a1cb755-f0f1-8193-982d-000bd4e3156c`
- **Parent page**: `💳 รายการใช้จ่ายผ่านบัตรของนุตา` → `Personal Monetary Policy`
- **Last schema-verified**: 2026-05-19

## Properties

Schema is identical to [[baiboon-bills]] except for the `Card` select option list.

| Name (Notion)       | Type     | Notes |
|---------------------|----------|-------|
| (title, blank name) | title    |  |
| `Card`              | **select** | **NOT a relation** — see [[../concepts/known-divergences]] |
| `วันตัดรอบบิล`        | date     |  |
| `ยอดชำระ`            | number (baht) |  |
| `จ่ายแล้ว`            | checkbox |  |
| `ใบแจ้งยอด (PDF)`     | files    |  |
| `หลักฐานการชำระ`      | files    |  |
| `Note`              | text     |  |

### `Card` select options (verbatim)

`AEON Next Gen`, `AEON Primo`, **`AEON UnionPay`**, **`CardX JCB`**, `First Choice`, `Krungsri JCB`, `Krungsri Visa`, `KTC UnionPay`, `SPayLater`, `UOB Makro`, `UOB One`, `UOB Premier`, `UOB World`.

Differences vs [[baiboon-bills]]: includes `AEON UnionPay` and `CardX JCB`; excludes `Krungsri NOW`, `Lotus's Beyond`, `ttb so smart`.

## Views

A single table view filtered to `จ่ายแล้ว = false`, sorted by `วันตัดรอบบิล` (asc) then `ยอดชำระ` (desc).

> Note: Baiboon's Bills view sorts `วันตัดรอบบิล` **desc**; Nuta's sorts **asc**. A minor UI inconsistency.
