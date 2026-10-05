---
tags: [database, household, promotion]
owner: household
role: promotions
---

# Promotion Bureau

One row per **quota period** (e.g. `2026M9 — NW3 cb 2%`), linking every holder's transactions that count toward it. Created by Takumi 2026-09-26; shared with the scripts' integration 2026-09-28. Concept: [[../concepts/promotion-bureau]].

- **Collection ID**: `3e7cb755-f0f1-80f0-8c78-000b1d9f44cb` (data source; its database is `3e7cb755-f0f1-80ac-8556-dd408bc65947`). `PROMOTION_BUREAU_DS` in `scripts/python/lib/holders.py`.
- **Last schema-verified**: 2026-10-01 (`Issuer`'s `Krungsri` split into four brands; `Issuer` added 2026-09-30; `Quotas Exceeded Date` added by the user; `สิทธิ์ลุ้นรางวัล` 2026-09-29)

## Schema

| Property | Type | Meaning |
|---|---|---|
| `Name` | title | `<YYYY>M<m> — <campaign>`; the month rule is in [[../concepts/promotion-bureau]]. The name picks the `BasePromotion` class |
| `Issuer` | select | who issues the campaign's cards: the cards' `brand` in `scripts/repositories/cards/` (`BasePromotion.issuer`), which is their `issuer` except inside the Krungsri family. That family is one issuer to the scripts (one statement format) but four brands here (user, 2026-10-01): `Krungsri Card` (Krungsri VISA/JCB/Lady/NOW), `First Choice`, `Lotus's Money` (Lotus's Beyond) and `Central The 1`. The other options are `UOB`, `AEON`, `ttb` and `KTC` (UnionPay QR: UnionPay's offer, on KTC cards). Added and filled 2026-09-30 (user). Every new row gets it, and a sync corrects it |
| `Start Date` / `End Date` | date | the period: a calendar month, or a statement cycle — the previous BC date to the day before the BC date, since spend on the BC date lands on the next statement (user, 2026-09-28) |
| `รายการใช้จ่ายจาก<name>` | relation (two-way) | the holder's linked Transactions rows; the synced side is `Promotion` on each Transactions DS |
| `ยอดจาก<name>` | rollup | Σ `ยอดชำระ` (amount paid) of those rows |
| `ยอดจ่ายรวม` | formula | `ยอดจากเว็บ + ยอดจากนุตา + ยอดจากใบบุญ` — pooled spend |
| `เงินคืนรวม` | number (baht) | total credit (cashback returned). Follows the split while it equals Σ `เงินคืนส่วน…`; a figure typed by hand is never overwritten |
| `เงินคืนส่วน<name>` | number (baht) | the holder's share; written by `/sync-promotion` (FCFS split) |
| `สิทธิ์ลุ้นรางวัล` | number | lucky-draw rights the period earned, on a `RIGHTS` campaign's row (BTS); added 2026-09-29 |
| `Quotas Exceeded Date` | date | the day the campaign's nationwide pool ran out (UnionPay QR): first seen used up on the bank's page by a sync, or set from the bank's announcement. Added by the user 2026-09-30 |

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
| `2026M8`–`2026M10 — BTS First Choice 10 rights`, `— BTS Krungsri Card 10 rights` | `BTSFirstChoice`, `BTSKrungsriCard` | created 2026-09-29 (one pool at first, split per company the same day); draw rights; [[../promotions/first-choice-2026h2]] |
| `2026M9 — ON3 …`, `— DLV3 …`, `— IS3 …` | `ON3Promotion`, `DLV3Promotion`, `IS3Promotion` | created 2026-09-29; First Choice |
| `2026M9`/`2026M10 — ONQ3/SUP1/PTT2/EAT/BC3P/J Dining/NOW <card> cb …`, `— Bangchak <card> cb 1%` (per cycle) | one `CardAccount` subclass per Krungsri card | created 2026-09-29; per card account; [[../promotions/krungsri-card-2026]] |
| `2026M9`/`2026M10 — CTG cb 3%`, `— BCG cb 3%`; `2026M7 — BMG cb ฿50–1,500` (whole campaign) | `TTBCaltexPromotion`, `TTBBangchakPromotion`, `TTBHypermarketPromotion` | created 2026-09-29; [[../promotions/ttb-2026]] |
| `2026M9`–`2026M11 — AEON UnionPay cb 3%` | `AEONUnionPayCashback` | created 2026-09-29; per AEON cycle |
| `2026M9 — LBS3 cb 1.6%` | `LBS3Promotion` | created 2026-09-29; Lotus's Beyond; [[../promotions/lotuss-lbs3]] |
| `2026M9`/`2026M10 — ttb so smart cb 1%` | `TTBSoSmartCashback` | created 2026-09-29; per ttb cycle; [[../promotions/ttb-2026]] |
| `2026M9`/`2026M10 — AEON Rabbit cb 5%`, `— AEON WM cb 5%`, `— NTW1 cb ฿120/340` | `AEONRabbitCashback`, `AEONWorldCashback`, `NTW1Promotion` | created 2026-09-29; per AEON cycle; [[../promotions/aeon-2026]] |
| `2026M9`/`2026M10 — UnionPay QR …1346 cb 6%`, `— UnionPay QR …2310 cb 6%` | `UnionPayQR1346`, `UnionPayQR2310` | created 2026-09-30; per card number, calendar month; September's `Quotas Exceeded Date` 12 Sep (UnionPay's Facebook post); [[../promotions/unionpay-qr]] |
| `2026M10 — NW4 cb 2%`, `— ON4 cb 1.25–1.8%`, `— IS4 cb 0.8–1%` | `NW4Promotion`, `ON4Promotion`, `IS4Promotion` | created 2026-10-01; First Choice Q4; [[../promotions/first-choice-2026h2]] |
| `2026M10 — BXP/LOTA/UNQ <card> cb …`; `2026M10`/`2026M11 — Bangchak700 <card> cb 1%` (per cycle; M10 is the partial 1–4 Oct cycle) | `CardAccount` subclasses in `bxp.py`, `lotus_exclusive.py`, `uniqlo.py` | created 2026-10-01; [[../promotions/krungsri-card-2026]], [[../promotions/uniqlo-2026]] |
| `2026M10 — SPW796 cb 2%`, `— UNO cb ฿150–800` | `SPW796Promotion`, `UOBUniqloPromotion` | created 2026-10-01; every UOB card; [[../promotions/uob-epw538]], [[../promotions/uniqlo-2026]] |
| `2026M10 — BGO cb ฿50–1,500`, `— MUJC cb ฿40–500` (whole campaign, 1 Oct – 31 Dec); `2026M10 — UQCB cb ฿150–800` | `TTBBigCGoPromotion`, `TTBMujiPromotion`, `TTBUniqloPromotion` | created 2026-10-01; [[../promotions/ttb-2026]], [[../promotions/uniqlo-2026]] |
| `2026M10 — MKR <KBank card> cb ฿100/240` (JCB, LINE Points, PLUSTINUM, Shopee) | `MKRKBank…` (`CardAccount`) | created 2026-10-01; one row per KBank card; [[../promotions/kbank-makro]] |
| `2026M10 — UMK26-1 cb ฿150/800/2,500` · `2026M10 — UMK26-2 cb ฿150/500/1,200` (1 Oct – 31 Dec) · `2026M10 — UMK26-3 cb ฿300` | `UOBMakroStoreMission` · `UOBMakroProMission` · `UOBMakroOtherMission` | created 2026-10-03 after Takumi registered; UOB Makro, principal and supplement pooled; [[../promotions/uob-makro-gold-mission]] |
| `2026M10 — UQN <KBank card> cb ฿100–600` (JCB, LINE Points, PLUSTINUM, Shopee) | `UQNKBank…` (`CardAccount`) | created 2026-10-01 (the JCB row first by an accidental live run, kept once the user registered); [[../promotions/uniqlo-2026]] |
| `2026M10 — HY1 cb ฿40/200/720` | `CardXHypermarketPromotion` | created 2026-10-01; Nuta's CardX JCB; [[../promotions/cardx-hypermarket]] |
| `2026M10 — UQC cb ฿120–700` | `CardXUniqloPromotion` | created 2026-10-05 (user); Nuta's CardX JCB, not registered yet; [[../promotions/uniqlo-2026]] |
| `2026M10 — SMP1 cb 2%` · `2026M10 — SMT2 cb ฿200` | `SMP1Promotion` · `SMT2Promotion` | created 2026-10-05 (user: "SMT1 / SMT2"); Lotus's Beyond, registered before the 1 Oct AIS bill; [[../promotions/lotuss-smp1]] |

Every campaign still running in October 2026 got its rows for the periods that overlap October on 2026-09-29, so the writers' follow-up keeps them filled. Campaigns ending 30 Sep (NW3, EPW538, ON3, IS3, BMG, J Dining, Krungsri Bangchak) got none: a successor (NW4 …) is a new campaign class once the user brings its terms. Their successors (NW4, ON4, IS4, SPW796, BGO, BXP/Bangchak700) and the new registered campaigns (LOTA, UNQ, UNO, UQCB, MUJC) got their October rows on 2026-10-01. LOTB and SPW592 have classes but no rows: the household isn't registered for them (user, 2026-10-01). UQN was registered later that day and has its rows.

## Quirks

- A page's relation list is cut off at **25** in the API response. Count linked rows from the Transactions side (`Promotion` contains the row) instead.
- Each holder has a tracker row per credit in [[cashback-trackers]], linked back through `Promotion`.
