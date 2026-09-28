---
tags: [database, household, promotion]
owner: household
role: promotions
---

# Promotion Bureau

One row per **quota period** (e.g. `2026M9 — NW3 cb 2%`), linking every holder's transactions that count toward it. Created by Takumi 2026-09-26; shared with the scripts' integration 2026-09-28. Concept: [[../concepts/promotion-bureau]].

- **Collection ID**: `3e7cb755-f0f1-80f0-8c78-000b1d9f44cb` (data source; its database is `3e7cb755-f0f1-80ac-8556-dd408bc65947`). `PROMOTION_BUREAU_DS` in `scripts/python/lib/holders.py`.
- **Last schema-verified**: 2026-09-28

## Schema

| Property | Type | Meaning |
|---|---|---|
| `Name` | title | `<YYYY>M<m> — <campaign>`; the month rule is in [[../concepts/promotion-bureau]]. The name picks the `BasePromotion` class |
| `Start Date` / `End Date` | date | the period: a calendar month, or a statement cycle — the previous BC date to the day before the BC date, since spend on the BC date lands on the next statement (user, 2026-09-28) |
| `รายการใช้จ่ายจาก<name>` | relation (two-way) | the holder's linked Transactions rows; the synced side is `Promotion` on each Transactions DS |
| `ยอดจาก<name>` | rollup | Σ `ยอดชำระ` (amount paid) of those rows |
| `ยอดจ่ายรวม` | formula | `ยอดจากเว็บ + ยอดจากนุตา + ยอดจากใบบุญ` — pooled spend |
| `เงินคืนรวม` | number (baht) | total credit (cashback returned). Follows the split while it equals Σ `เงินคืนส่วน…`; a figure typed by hand is never overwritten |
| `เงินคืนส่วน<name>` | number (baht) | the holder's share; written by `/sync-promotion` (FCFS split) |

`<name>` is the holder's Thai name (`เว็บ`, `ใบบุญ`, `นุตา`), so the scripts derive every per-holder column name from `Holder.thai_name`.

The page **body** carries the campaign summary: ladder, what counts, exclusions, crediting and the household split. `/sync-promotion` renders it from the campaign class when the body is empty.

## Rows

| Row | Class | Notes |
|---|---|---|
| `2026M9 — NW3 cb 2%` | `NW3Promotion` | [[../promotions/first-choice-nw3]]; synced 2026-09-28 |
| `2026M9 — UOB World ×5` | `UOBWorldBonus` | points quota, cycle 25 Aug–24 Sep (billed 25 Sep); [[../promotions/uob-world-points]] |
| `2026M9 — UOB One cb 10%/5%` | `UOBOneBonus` | created 2026-09-28; ฿500 cap, calendar Sep; [[../promotions/uob-one-2026]] |
| `2026M9 — UOB One cb 1%` | `UOBOneBase` | created 2026-09-28; ฿2,000 cap, cycle 25 Aug–24 Sep (billed 25 Sep) |
| `2026M9 — EPW538 cb 2%` | `EPW538Promotion` | created 2026-09-28; every UOB card; [[../promotions/uob-epw538]] |

## Quirks

- A page's relation list is cut off at **25** in the API response. Count linked rows from the Transactions side (`Promotion` contains the row) instead.
- Each holder has a tracker row per credit in [[cashback-trackers]], linked back through `Promotion`.
