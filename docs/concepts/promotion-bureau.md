---
tags: [concept, rewards, promotion]
---

# Promotion Bureau — pooled campaigns and the FCFS split

Some bank campaigns pay on the **primary account's pooled spend**, not per row. NW3 on First Choice pays ฿200 per whole ฿10,000 the household spends in a month, across Takumi's principal card and Baiboon's and Nuta's supplements. No single holder's ledger can tell what the bank will pay, or who earned it. The [[../databases/promotion-bureau|Promotion Bureau]] DB exists for these: one row per **quota period**, linked to every holder's qualifying transactions. Added by Takumi 2026-09-26.

This sits beside, not inside, the per-row [[promotions|promotion model]] (`% cb` from `scripts/repositories/promotions/*.yaml`). The YAML model answers "what rate does this row earn?". The Bureau answers "what does the bank pay the account, and whose spend earned it?".

## One row per quota period

A quota period is the window a bank counts a limit over (user, 2026-09-28). Even a campaign that runs a quarter or a year usually counts per month (`สะสมยอดใช้จ่ายต่อเดือน` "spend accumulated per month", `จำกัดสูงสุด…ต่อเดือน` "capped at … a month"), and its `จำกัด…ตลอดรายการ` (whole-campaign cap) is usually just the months added up. So each Bureau row is one period, named `<year>M<month> — <campaign>`:

| The bank counts per… | `<month>` is… | Example |
|---|---|---|
| calendar month | that month | `2026M9 — NW3 cb 2%` (1–30 Sep) |
| statement cycle | the month of the cycle's closing (BC) date | `2026M9 — UOB One cb 1%` (25 Aug–24 Sep, billed 25 Sep) |
| the whole campaign | the campaign's first month | — |

Which rows belong to a period is each campaign class's call (`covers`, `candidate_filter`, `period_for` on `BasePromotion`). The defaults read the transaction date (calendar month) or the `Bill Cycle Date` (cycle). **UOB One overrides them with the bank's posting-date rules** (see [[../promotions/uob-one-2026]]): 1% by posting date within the cycle, 10%/5% by posting date within the month, each with the closing day rolling forward (installment terms included). Posting dates come from `Process Date`, or are inferred until the statement comes ([[billing-cycle#Posting dates (`Process Date`)]]).

A cycle row runs from the previous BC date to the **day before** its BC date. Spend on the BC date itself lands on the next statement (user, 2026-09-28). UOB's terms say the same, and every BC-day UOB purchase in the ledger since 2025 was billed to the next cycle. Rows are still sorted into a cycle row by the `Bill Cycle Date` they carry (End Date + 1 day), so late postings count where the bank billed them.

One campaign can have two quotas with different periods: UOB One caps its 10%/5% tiers per calendar month and its 1% per statement cycle, so it has two rows a month.

## One class per campaign, one class per payout shape

Campaign terms don't share a shape, so the shape is a class and each campaign subclasses it (`scripts/python/lib/bureau/`):

| Shape | How the reward is paid | Campaigns |
|---|---|---|
| `LadderPromotion` | steps of pooled spend: ฿200 per whole ฿10,000, ฿100 per ฿5,000 … | NW3, EPW538 |
| `CreditCapPromotion` | each row earns its own rate until the period's pooled credit hits a cap | UOB One 10%/5%, UOB One 1% |
| `UOBWorldBonus` (its own shape) | points: ×5 on bonus categories inside the first ฿20,000 of a cycle | UOB World ×5 |

A campaign class states the bank's terms in code: cards, dates, what counts (`qualifies`, `rules`), the payout, and the page text. Screening, the split and the Bureau page summary read those declarations, so the page and the screening can't drift apart. [[../../.claude/skills/sync-promotion/SKILL.md|/sync-promotion]] drives it.

## One row, several campaigns — same bank only

A transaction can count toward more than one campaign of its own bank (user, 2026-09-28). Nuta's `TMN 7-11` on UOB One earns UOB One's 1% **and** counts toward EPW538. Each campaign gets its own Bureau row and tracker rows. The row's single `% cb`, though, shows only the card's own cashback (UOB One's tier, First Choice's NW3); an overlay paid as a lump sum on top (EPW538) sets `marks_rows = False` and lives in the trackers alone.

## Who gets how much: first come, first served

Decided by the user 2026-09-28:

1. Walk the linked rows in `Transaction Datetime` order. Only the spend inside a **paying step** earns; it earns at the step's rate and goes to whoever spent it. Spend past the last whole step earns nothing, whoever it belongs to.
2. Rows with the **same `Transaction Datetime`** count as simultaneous. That covers a shared bill (a `[บัตรหลัก]` row plus Takumi's remainder of the same charge, given the same time) and date-only rows, whose order within the day is unknown. When such a group straddles a step, the part inside the step is shared **pro rata by amount**.
   Only the day the last step ends on needs exact order. Store it as times in `Transaction Datetime` on that day's rows. Apps (UCHOOSE included) show dates only, so the user has to dig the times out of notification logs; ask for that one day's times, nothing more. A boundary day that mixes timed and date-only rows draws a warning.
3. **Per-row fields follow the split** (user, 2026-09-28). For cashback, the `% cb`: A row wholly inside the paying steps carries the full rate (`0.02` for NW3). The row, or same-time group, that straddles the last step is left **unset**, even though part of it earns; so is every row after it. The share fields and trackers carry the exact money. September 2026: 81 rows at 2% and 12 unset (Hai Di Lao's two shares, and everything after). For points (UOB World), the multiplier: ×5 inside the quota, ×2 past it, and the row the quota ends in keeps ×5 and gives back the over-quota part through `ใช้คะแนน`. `/sync-promotion` checks these on every run (`field_mismatches`), since a newly linked row can move the boundary to another day.
4. Each holder's total is rounded to the satang, and the leftover satang go to the largest remainders, so the shares add up to the credit exactly.
5. `เงินคืนรวม` (total cashback) follows the split while it equals the sum of the share fields. Once someone types a different figure there (the bank's actual credit), it's never overwritten, and a split that disagrees with it is held back with a warning.

Worked case, September 2026 (reconciled): pooled ฿36,803.92 → 3 steps → ฿600 on the first ฿30,000. The step ends on 2026-09-24 with ฿176.08 of room left. By the times the user looked up, `TMN*PROMPTPAY30` ฿35 (10:56) and `DUMPLINGS` ฿10 (18:47) come first. Hai Di Lao (21:21; Takumi ฿1,562.67 + Baiboon `[บัตรหลัก]` ฿781.33, one charge) takes the last ฿131.08, pro rata: Takumi ฿87.39, Baiboon ฿43.69.

This replaced the July/August convention, in which each friend got a flat 2% of their own spend and Takumi kept the remainder (see the note on Takumi's `เครดิตเงินคืน NW3_1JUL26-31JUL26` row).

## Kept in step with the ledger

Every write to a ledger re-syncs the Bureau (user, 2026-09-28). [[../../.claude/skills/add-transaction/SKILL|/add-transaction]], [[../../.claude/skills/update-transaction/SKILL|/update-transaction]] and [[../../.claude/skills/record-statement/SKILL|/record-statement]] hand the rows they wrote to `lib.bureau.follow`, which:

1. **Places each row.** For every campaign on the row's card, it finds the quota period the row falls in (`BasePromotion.period_for`: the calendar month of the transaction date, or the cycle billed on the row's `Bill Cycle Date`) and that period's Bureau row. It also takes the Bureau rows the row is already linked to, so an edit that moves a row re-syncs where it was counted.
2. **Re-syncs** each of those rows the way [[../../.claude/skills/sync-promotion/SKILL|/sync-promotion]] does, with `link_candidates`. Eligible rows in the period are linked, the credit is split again, and `เงินคืนรวม` / `เงินคืนส่วน<name>` and the trackers are updated.
3. **Applies the split to the rows.** Every linked row's `% cb`, multiplier and `ใช้คะแนน` is set to what the split expects, including rows the writer didn't touch. A backdated row can push someone else's row past a cap, and that row's `% cb` has to follow, because it feeds the other quota. A UOB One 10%/5% row past the month's ฿500 is marked 1%, which is what makes the cycle's 1% quota count it. So the rows it fixes are followed again, until a pass fixes nothing. If two quotas want different values for one row (possible only when both UOB One caps are exceeded), it stops after one reversal and warns instead of flipping the value back and forth.

An edit that moves a row onto another statement cycle, or onto another card, **unlinks** it from the Bureau row it no longer belongs to, and that row is re-synced without it. The `Bill Cycle Date` is where the bank billed it. A calendar-month row that's dated outside its month is only warned about, because the bank counts those by posting date, and a link across a month boundary can be deliberate. Example, 2026-09-28: Nuta's `TMN 7-11` ฿137 dated 25 Sep was moved to the 22 Oct cycle. It left `2026M9 — UOB One cb 1%` but stayed in EPW538 and the 10%/5% month, which both count by transaction date.

What it doesn't do:

- **Create Bureau rows.** A period with no row is reported under `missing`, with the name and dates to pass to `/sync-promotion` (the name is the class's: `<year>M<month> — <code> cb <headline>`, or without `cb` for points). Periods before a campaign's first Bureau row are untracked and aren't reported.
- **Honour hand edits of `% cb` on linked rows.** The split owns those fields, and the next sync puts them back. An exception that should last goes into the campaign class as a `Rule`. A deliberate unlink doesn't last either: the next sync re-links an eligible row.

A Bureau row's dates must match its period. The follow-up finds a cycle row by End Date + 1 day = the row's `Bill Cycle Date`. A row whose dates are off, but whose name has the right `<year>M<month>`, is still re-synced for its linked rows, with a warning that new rows can't be linked to it.

## Bureau vs. bank

Krungsri-family apps (UCHOOSE, which covers First Choice) list the transactions the bank counts toward a campaign, with their total; that list is the reference for what to link. Whether other issuers' apps do the same is unknown. When it differs from the Bureau's `ยอดจ่ายรวม` (total spend), the linked data is wrong somewhere: a row double-counted, mis-split, or linked when the bank excludes it. `/sync-promotion` with `bank_spend` lays out the gap: per-date totals to read against the app's list, dates whose total equals the gap, and repeated rows. The fix comes from the app's list or the statement, never from editing numbers to match.
