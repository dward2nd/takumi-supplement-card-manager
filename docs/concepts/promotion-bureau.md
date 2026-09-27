---
tags: [concept, rewards, promotion]
---

# Promotion Bureau — pooled campaigns and the FCFS split

Some bank campaigns pay on the **primary account's pooled spend**, not per row. NW3 on First Choice pays ฿200 per whole ฿10,000 the household spends in a month, across Takumi's principal card and Baiboon's and Nuta's supplements. No single holder's ledger can tell what the bank will pay, or who earned it. The [[../databases/promotion-bureau|Promotion Bureau]] DB exists for these: one row per campaign period, linked to every holder's qualifying transactions. Added by Takumi 2026-09-26.

This sits beside, not inside, the per-row [[promotions|promotion model]] (`% cb` from `scripts/repositories/promotions/*.yaml`). The YAML model answers "what rate does this row earn?". The Bureau answers "what does the bank pay the account, and whose spend earned it?".

## One class per campaign

Campaign terms don't share a shape (stepped ladders, flat bonuses, merchant-specific tiers, points), so each is a `BasePromotion` subclass in `scripts/python/lib/bureau/`, declaring the bank's terms in code: card, dates, `tranches()` (the ladder), `rules` (exclusions, each with a merchant-string test where one exists), and the page text. Screening, the split and the Bureau page summary are shared and read those declarations, so the page and the screening can't drift apart. [[../../.claude/skills/sync-promotion/SKILL.md|/sync-promotion]] drives it.

## Who gets how much: first come, first served

Decided by the user 2026-09-28:

1. Walk the linked rows in `Transaction Datetime` order. Only the spend inside a **paying step** earns; it earns at the step's rate and goes to whoever spent it. Spend past the last whole step earns nothing, whoever it belongs to.
2. Rows with the **same `Transaction Datetime`** count as simultaneous. That covers a shared bill (a `[บัตรหลัก]` row plus Takumi's remainder of the same charge, given the same time) and date-only rows, whose order within the day is unknown. When such a group straddles a step, the part inside the step is shared **pro rata by amount**.
   Only the day the last step ends on needs exact order. Store it as times in `Transaction Datetime` on that day's rows. Apps (UCHOOSE included) show dates only, so the user has to dig the times out of notification logs; ask for that one day's times, nothing more. A boundary day that mixes timed and date-only rows draws a warning.
3. Each holder's total is rounded to the satang, and the leftover satang go to the largest remainders, so the shares add up to the credit exactly.

Worked case, September 2026 (reconciled): pooled ฿36,803.92 → 3 steps → ฿600 on the first ฿30,000. The step ends on 2026-09-24 with ฿176.08 of room left. By the times the user looked up, `TMN*PROMPTPAY30` ฿35 (10:56) and `DUMPLINGS` ฿10 (18:47) come first. Hai Di Lao (21:21; Takumi ฿1,562.67 + Baiboon `[บัตรหลัก]` ฿781.33, one charge) takes the last ฿131.08, pro rata: Takumi ฿87.39, Baiboon ฿43.69.

This replaced the July/August convention, in which each friend got a flat 2% of their own spend and Takumi kept the remainder (see the note on Takumi's `เครดิตเงินคืน NW3_1JUL26-31JUL26` row).

## Bureau vs. bank

Krungsri-family apps (UCHOOSE, which covers First Choice) list the transactions the bank counts toward a campaign, with their total; that list is the reference for what to link. Whether other issuers' apps do the same is unknown. When it differs from the Bureau's `ยอดจ่ายรวม` (total spend), the linked data is wrong somewhere: a row double-counted, mis-split, or linked when the bank excludes it. `/sync-promotion` with `bank_spend` lays out the gap: per-date totals to read against the app's list, dates whose total equals the gap, and repeated rows. The fix comes from the app's list or the statement, never from editing numbers to match.
