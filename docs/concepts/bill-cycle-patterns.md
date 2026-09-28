---
tags: [concept, temporal, billing]
---

# Bill-cycle patterns by issuer

Every card has a fixed monthly **billing pattern**: which calendar day is the cycle cut-off, and how many days later the bill is due. The patterns are consistent within an issuer family (and, in the user's experience, stable enough to encode in code).

This note is the source of truth for those patterns. The [bill_cycle library](../../scripts/python/lib/bill_cycle.py) implements them; [[../../.claude/skills/add-transaction/SKILL|add-transaction]] uses the library to auto-fill the `Bill Cycle Date` and `Due Date` on new transactions when the caller doesn't supply them explicitly.

## Which cycle is "active"?

Rule, applied per card:

> The active cycle is the one whose **bill-cycle date is the next one on or after today** — i.e., the upcoming cut-off the bill is currently accumulating toward.

A transaction posted today lands on that bill. The cut-off day itself already belongs to *its own* cycle (so on day-5 of the month, the cycle closing day-5 is still the active one — it closes at end-of-day).

Concretely, to find the active cycle:

1. Compute this month's bill-cycle date for the card.
2. If today **≤** that date → it's the active cycle.
3. Otherwise → roll forward one month and use that.

For UOB this comparison uses the *shifted* bill-cycle date (see UOB below), not the nominal day 25.

## The patterns

| Issuer family             | Bill cycle day  | Due date                          | Notes                          |
|---------------------------|-----------------|-----------------------------------|--------------------------------|
| Krungsri / First Choice / CardX / Lotus's | day **5**   | bill cycle **+ 20 days**          | consistent, no shifts; Lotus's joined 2026-08-08 |
| KTC                       | day **27**      | bill cycle **+ 15 days**          | consistent, no shifts          |
| ttb                       | day **27**      | bill cycle **+ 20 days**          | same BC day as KTC, longer grace |
| AEON                      | day **10**      | day **2** of the **next** month   | consistent, no shifts; fixed-day due |
| KBank                     | day **25**      | day **10** of the **next** month  | consistent, no shifts; fixed-day due |
| ~~Lotus~~ *(historical)*  | day **28**      | bill cycle **+ 20 days**          | **retired 2026-08-08** — see below |
| SPayLater                 | day **15**      | bill cycle **+ 10 days**          | consistent, no shifts          |
| Grab                      | day **1**       | bill cycle **+ 6 days** (⇒ day 7) | Takumi-only; labelled a day *after* the bank's cut — see below |
| UOB                       | day **25**      | bill cycle **+ 20 days**          | see *UOB exceptions* below     |

### Card → pattern mapping (by name prefix, case-insensitive)

| Card name prefix     | Pattern        |
|----------------------|----------------|
| `Krungsri …`         | Krungsri/etc   |
| `First Choice`       | Krungsri/etc   |
| `CardX …`            | Krungsri/etc   |
| `KTC …`              | KTC            |
| `ttb …`              | ttb            |
| `AEON …`             | AEON           |
| `KBank …`            | KBank          |
| `Lotus's Beyond`     | Krungsri/etc   |
| `SPayLater`          | SPayLater      |
| `Grab PayLater`      | Grab           |
| `UOB …`              | UOB            |

### Grab PayLater is labelled a day after the bank's cut

Grab's statement actually cuts at the turn of the month — the bank's own period ends on the 30th/31st — and is due on the 7th. The pattern nonetheless anchors **BC day 1**, one day later than the cut.

That's deliberate, and it's the house same-day convention doing the work. `active_cycle` assigns a transaction to the cycle whose BC is the next date **≥** the transaction date, so a purchase dated *on* the BC day falls into the cycle closing that day. Label the cycle `09-30` and a purchase made on the 30th lands in the cycle that just closed; label it `10-01` and it lands in the cycle due 10-07, which is where Grab actually bills it.

Deciding this by relabelling rather than by special-casing the comparison keeps one rule for all nine patterns. Set by the user 2026-09-23.

The 29 pre-2025-07 rows on the card still carry the old labelling (BC day 31, or day 28 in February) and now sit one day off the pattern. They are history on a reset ledger and were left as-is; `/audit-transaction-dates` will flag them.

### KTC: Takumi's history predates the current cycle

Every dated KTC row in [[../databases/takumi-transactions]] through 2025-06 sits at **BC day 2 / due +15**, not the day 27 above. All four of his KTC products agree, across 48 rows.

The `ktc` pattern is nonetheless correct today: Baiboon's KTC UnionPay is a supplement on Takumi's KTC account — necessarily the same billing cycle — and it currently bills BC day 27 / due day 12. So KTC moved the cycle sometime after 2025-06 and the day-2 rows are history.

His four KTC cards are registered against `ktc` on that basis, each with the caveat in its YAML. If a fresh KTC statement ever shows day 2, add a `ktc_day2` pattern rather than editing `ktc` — Baiboon's and Nuta's live cards depend on it.

### Matching

The match is on the card's title in the Cards DB. Looking up the `ธนาคาร/บริษัท` (bank/company) select is unreliable — many rows have it blank — so we key off the card name itself. See [[known-divergences#9. Takumi's Cards DB omits ธนาคาร/บริษัท]].

**Apostrophes: use ASCII `'`.** It is the preferred spelling in both Notion titles and the card YAMLs. Notion's editor inserts the typographic `’` (U+2019) readily and it is visually identical, so a mismatch is silent — `Lotus's Beyond` was mis-titled in Notion for months, and `card_repo` returned `None` for it, meaning the card had *no* bill-cycle pattern and *no* exclusion flags. `lib.card_repo.by_name` now folds curly→ASCII as a safety net, but the titles themselves should stay ASCII. If a card reports "no registered pattern", check the apostrophe first.

### Lotus's Beyond changed pattern on 2026-08-08

The card moved from the retired `lotus` pattern (day 28, +20d) onto `krungsri` (day 5, +20d), matching the rest of the Krungsri family.

- **Pre-switch rows keep their old dates and were deliberately not migrated** (user instruction). The card's two existing rows stay on BC `2026-05-28` / DD `2026-06-17`.
- The `lotus` key (`LotusCycle`) is retained in `lib.bill_cycle.PATTERNS` purely so that history reads correctly; no card points at it.
- Inference has no notion of a dated pattern change, so it now answers with day-5 for *every* date. **Backdating a row into a pre-switch cycle must pass explicit `bill_cycle` + `due_date`.**
- The shared pattern key does **not** make this a Krungsri-family card for reward purposes — it stays exempt from the 7-11 / TrueMoney points exclusion. See [[krungsri-truemoney-711-exclusion]].

## UOB exceptions — weekend / Thai public holiday shifts

The nominal cycle is **day 25** with a due date **20 days later**. Both dates are then shifted independently if they land on a non-working day:

- If **day 25** falls on a Saturday, Sunday, or Thai public holiday → bill cycle date is shifted **earlier** to the closest preceding workday.
- If the **due date** falls on a Saturday, Sunday, or Thai public holiday → due date is shifted **later** to the closest following workday.

The shifts are independent — a shifted bill cycle date does **not** change how the due date is computed (the due date still starts from the nominal day 25 + 20 days = day 14 of the next month, then gets its own shift if needed).

The "active cycle" comparison from the top of this note uses the *shifted* bill cycle date for UOB. So if day 25 has been pulled back to day 22 (because 23–25 are all non-working), then on day 22 onwards we're already in the next cycle.

Thai public holidays are sourced from the [`holidays`](https://pypi.org/project/holidays/) Python package, country code `TH`, official public-holiday set. The Bank of Thailand calendar can occasionally diverge by a day around substitution holidays — if a real-world bank statement disagrees with what the library computed, the script's output is overridable: pass `bill_cycle` / `due_date` explicitly in the add-transaction spec and the library is bypassed for that batch.

### Observed exception — cycle 2026-08-25 due 18 Sep

The UOB statement dated 25 Aug 2026 printed a due date of **18 Sep 2026** — 24 days after the bill cycle, where the pattern gives 14 Sep (+20; a Monday, not a holiday). Every UOB row in that cycle, across all three holders, was set to 18 Sep on 2026-09-27 at Takumi's request. One statement isn't enough to change the pattern, so it still says +20 and `/audit-transaction-dates` will flag these rows. If later UOB statements also print +24, change the pattern instead.

## Worked examples

Today is **2026-05-21** (the date this note was written). Active cycle by pattern:

| Pattern        | Day | This month's date | Today vs. that date | Active bill cycle | Active due date |
|----------------|----:|-------------------|---------------------|-------------------|-----------------|
| Krungsri/etc   |   5 | 2026-05-05        | after → advance     | 2026-06-05        | 2026-06-25      |
| KTC            |  27 | 2026-05-27        | before → keep       | 2026-05-27        | 2026-06-11      |
| ttb            |  27 | 2026-05-27        | before → keep       | 2026-05-27        | 2026-06-16      |
| AEON           |  10 | 2026-05-10        | after → advance     | 2026-06-10        | 2026-07-02      |
| Lotus          |  28 | 2026-05-28        | before → keep       | 2026-05-28        | 2026-06-17      |
| SPayLater      |  15 | 2026-05-15        | after → advance     | 2026-06-15        | 2026-06-25      |
| UOB            |  25 | 2026-05-25 (Mon)  | before → keep       | 2026-05-25        | 2026-06-14 (Sun) → **2026-06-15** |

The UOB row shows the right-side shift: 2026-06-14 is a Sunday, so the due date is pushed to Monday 2026-06-15.

## See also

- [[billing-cycle]] — the four date axes on every transaction (this note is about how *bill cycle* and *due date* are computed; the other two are bank-driven).
- [[../../.claude/skills/add-transaction/SKILL]] — the write skill that consumes these patterns.
- [[known-divergences#9. Takumi's Cards DB omits ธนาคาร/บริษัท]] — why we key off card name, not issuer field.
