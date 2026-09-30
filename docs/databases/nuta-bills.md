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
- **Last schema-verified**: 2026-09-30

## Properties

Schema is identical to [[baiboon-bills]], except that `Card` relates to Nuta's own Cards DB and the legacy `Card (old select)` has a different option list.

| Name (Notion)       | Type     | Notes |
|---------------------|----------|-------|
| (title, blank name) | title    |  |
| `Card`              | relation → [[nuta-cards]] | One-way (no back-link column on Cards). A relation since 2026-09-30; before that a SELECT. See [[../concepts/known-divergences]] #1. |
| `Card (old select)` | select   | **Legacy.** The former `Card` SELECT, renamed and kept so existing views grouped/filtered by it still work. To be deleted once the views move to the relation. Scripts ignore it. |
| `วันตัดรอบบิล`        | date     |  |
| `ยอดชำระ`            | number (baht) |  |
| `จ่ายแล้ว`            | checkbox |  |
| `ใบแจ้งยอด (PDF)`     | files    |  |
| `หลักฐานการชำระ`      | files    |  |
| `Note`              | text     |  |

### Legacy: `Card (old select)` options (verbatim)

`AEON Next Gen`, `AEON Primo`, **`AEON UnionPay`**, **`CardX JCB`**, `First Choice`, `Krungsri JCB`, `Krungsri Visa`, `KTC UnionPay`, `SPayLater`, `UOB Makro`, `UOB One`, `UOB Premier`, `UOB World`.

Differences vs [[baiboon-bills]]: includes `AEON UnionPay` and `CardX JCB`; excludes `Krungsri NOW`, `Lotus's Beyond`, `ttb so smart`. That divergence (#8) no longer matters: since 2026-09-30 a bill links a page in Nuta's own Cards DB, and nothing adds options to the old select.

All 35 of Nuta's existing bills were linked on 2026-09-30, each to the Cards page its old select named. Bill titles keep their `<Card> <YYYY-MM>` naming. See [[../concepts/known-divergences]] #1, #8 and #11.

## Views

A single table view filtered to `จ่ายแล้ว = false`, sorted by `วันตัดรอบบิล` (asc) then `ยอดชำระ` (desc).

> Note: Baiboon's Bills view sorts `วันตัดรอบบิล` **desc**; Nuta's sorts **asc**. A minor UI inconsistency.
