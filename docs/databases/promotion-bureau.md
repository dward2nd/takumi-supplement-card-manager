---
tags: [database, household, promotion]
owner: household
role: promotions
---

# Promotion Bureau

One row per **campaign period** (e.g. `2026M9 — NW3 cb 2%`), linking every holder's transactions that count toward it. Created by Takumi 2026-09-26; shared with the scripts' integration 2026-09-28. Concept: [[../concepts/promotion-bureau]].

- **Collection ID**: `3e7cb755-f0f1-80f0-8c78-000b1d9f44cb` (data source; its database is `3e7cb755-f0f1-80ac-8556-dd408bc65947`). `PROMOTION_BUREAU_DS` in `scripts/python/lib/holders.py`.
- **Last schema-verified**: 2026-09-28

## Schema

| Property | Type | Meaning |
|---|---|---|
| `Name` | title | `<YYYY>M<m> — <code> <headline>`; the code picks the `BasePromotion` class |
| `Start Date` / `End Date` | date | the period (a calendar month for NW3) |
| `รายการใช้จ่ายจาก<name>` | relation (two-way) | the holder's linked Transactions rows; the synced side is `Promotion` on each Transactions DS |
| `ยอดจาก<name>` | rollup | Σ `ยอดชำระ` (amount paid) of those rows |
| `ยอดจ่ายรวม` | formula | `ยอดจากเว็บ + ยอดจากนุตา + ยอดจากใบบุญ` — pooled spend |
| `เงินคืนรวม` | number (baht) | total credit (cashback returned). `/sync-promotion` fills it when empty and never overwrites it |
| `เงินคืนส่วน<name>` | number (baht) | the holder's share; written by `/sync-promotion` (FCFS split) |

`<name>` is the holder's Thai name (`เว็บ`, `ใบบุญ`, `นุตา`), so the scripts derive every per-holder column name from `Holder.thai_name`.

The page **body** carries the campaign summary: ladder, what counts, exclusions, crediting and the household split. `/sync-promotion` renders it from the campaign class when the body is empty.

## Rows

| Row | Class | Notes |
|---|---|---|
| `2026M9 — NW3 cb 2%` | `NW3Promotion` | [[../promotions/first-choice-nw3]]; synced 2026-09-28 |
| `2026M9 — UOB World ×5` | — | points campaign; no class yet, so `/sync-promotion` refuses it |

## Quirks

- A page's relation list is cut off at **25** in the API response. Count linked rows from the Transactions side (`Promotion` contains the row) instead.
- Each holder has a tracker row per credit in [[cashback-trackers]], linked back through `Promotion`.
