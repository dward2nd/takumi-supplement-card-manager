---
tags: [database, household, promotion]
owner: household
role: cashback-tracker
---

# Cashback trackers (`รายการติดตามเครดิตเงินคืนของ<name>`)

Three identical DBs, one per holder. Each row is one promotion credit the holder expects to get back, such as `NW3 2% 1—31 Aug` or `ttb so smart 1% Sep bill`. It stays open until the credit reaches them.

| Holder | Collection ID |
|---|---|
| Takumi | `96bcb755-f0f1-83ef-a5b9-079f9ba3ae98` |
| Baiboon | `374cb755-f0f1-80b2-97cc-000b0105e43e` |
| Nuta | `2e4cb755-f0f1-838a-9317-877c67577916` |

`Holder.cashback_tracker_ds` in `scripts/python/lib/holders.py`. **Last schema-verified**: 2026-09-30.

## Schema

| Property | Type | Meaning |
|---|---|---|
| `Name` | title | `<code> <rate> <period>`, e.g. `NW3 2% 1—30 Sep` |
| `Transaction Date` | date | the period start for a Bureau-driven row (the household's precedent) |
| `Card` | relation → the holder's own Cards DS | the card earning the credit |
| `Promotion` | relation → [[promotion-bureau]] (one-way) | set on Bureau-driven rows |
| `Expected Cashback` | number (baht) | the holder's share |
| *(unnamed)* | checkbox | ticked once the credit has reached the holder (named `""` in the API) |
| `Note` | rich_text | the household's own status note, e.g. `รวมไปในบิลของรอบบิล 5 ตุลาคม` ("included in the 5 Oct bill") |
| `Slip` | files | a transfer slip, when the credit was paid out in cash |
| `Slip Transaction` | relation → the holder's own Transactions DS (one-way) | the ledger row that *is* the credit, when the bank paid it onto the card (added 2026-09-30) |

## How a row is settled

Either way, the unnamed checkbox is ticked once the credit has reached the holder:

- **Paid out by transfer.** Takumi transfers the money and attaches the slip to `Slip`.
- **Paid by the bank onto the card.** The credit is already a row in the holder's own ledger. It might be the bank's line (`BANGCHAK SPECIAL DISCOUNT OF 1 %`, `CB15_ SUP1 …`) or the household's credit row (`UOB ONE CASHBACK 1%`). That row goes in `Slip Transaction` (user, 2026-09-30). Before this column existed, the row was written into `Note` as `บันทึกในบัญชีแล้ว: <name> ฿<amt> · <card> ของ<ชื่อ> <date>`, with a link. The four trackers settled that way on 2026-09-29 keep their Note, and were linked through `Slip Transaction` on 2026-09-30.

The relation only reaches the holder's own ledger. A friend's credit that landed on Takumi's primary card is in his ledger, not theirs, so their tracker is settled by his transfer slip. Example: Baiboon's `Everyday with AEON 10 Aug` (฿120), settled 2026-10-09 by his PromptPay slip after her `[บัตรหลัก] CASH BACK - CREDIT CARD PROMOTION` row was archived ([[../promotions/aeon-2026#NTW1 for the cycle billed 10 Aug, paid by transfer|aeon-2026]]).

**A pooled bank credit settles Takumi's share.** When the bank credits a whole pooled campaign onto his card, as with `UOB One Cashback 10% 5%` −฿420.95 on 30 Sep 2026, his tracker links that one row and is ticked, even though the row is the whole pool and not his share. The Note gives both figures (user, 2026-10-06).

**UOB One 10%/5%: a month tracker settles against cycle credits** (user, 2026-10-06). The Bureau counts 10%/5% per calendar month, the bank's view. Baiboon and Nuta are paid per bill cycle, through the `UOB ONE CASHBACK 10%` / `5%` rows that [[../../.claude/skills/post-cashback-credits/SKILL|/post-cashback-credits]] puts on their bills. A month overlaps **two** cycles: September runs over the cycle closing 25 Sep and the one closing 22 Oct, which covers 25–29 Sep. So the month's tracker links the 10%/5% credit rows of **both** cycles in `Slip Transaction`, and is ticked once both are linked. The amounts won't match `Expected Cashback`, since a cycle isn't a month. First case: September 2026. Nuta's is linked to her 25 Sep rows (−฿17.50, −฿156.20) and Baiboon's to hers (−฿5.83). Both stay unticked until the 22 Oct cycle's credits are posted. This replaces the earlier rule that a cycle credit never ticks a month tracker.

## History

- Baiboon's tracker predates the Bureau (rows from 2026-06). Its 31 earlier rows have no `Promotion` link; leave them as they are.
- Takumi's and Nuta's were created 2026-09-28 as copies of Baiboon's. The copies had no `Promotion` column, and their `Card` relation still pointed at **Baiboon's** Cards DS. Both were fixed that day while the tables were empty: `Promotion` was added, and `Card` was retargeted to each holder's own Cards DS.
- 2026-09-29: 26 unlinked rows backfill UOB's e-Wallet & e-Commerce campaign for Oct 2025 – Aug 2026 (`EPW913 …`, `EPW144 …`, `EPW243 …`, `EPW538 2% 1—31 Aug`), split in proportion to each holder's eligible spend on the bundled statements. Takumi's are ticked where the bank credit has posted. See [[../promotions/uob-epw538#The quarterly series]].
- `/sync-promotion` writes Bureau-driven rows. It never touches a ticked row or one without a `Promotion` link.
