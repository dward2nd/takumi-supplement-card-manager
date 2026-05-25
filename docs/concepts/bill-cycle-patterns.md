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
| Krungsri / First Choice / CardX | day **5**   | bill cycle **+ 20 days**          | consistent, no shifts          |
| KTC                       | day **27**      | bill cycle **+ 15 days**          | consistent, no shifts          |
| ttb                       | day **27**      | bill cycle **+ 20 days**          | same BC day as KTC, longer grace |
| AEON                      | day **10**      | day **2** of the **next** month   | consistent, no shifts          |
| Lotus                     | day **28**      | bill cycle **+ 20 days**          | consistent, no shifts          |
| SPayLater                 | day **15**      | bill cycle **+ 10 days**          | consistent, no shifts          |
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
| `Lotus …`            | Lotus          |
| `SPayLater`          | SPayLater      |
| `UOB …`              | UOB            |

The match is on the card's title in the Cards DB. Looking up the `ธนาคาร/บริษัท` (bank/company) select is unreliable — many rows have it blank — so we key off the card name itself. See [[known-divergences#9. Takumi's Cards DB omits ธนาคาร/บริษัท]].

## UOB exceptions — weekend / Thai public holiday shifts

The nominal cycle is **day 25** with a due date **20 days later**. Both dates are then shifted independently if they land on a non-working day:

- If **day 25** falls on a Saturday, Sunday, or Thai public holiday → bill cycle date is shifted **earlier** to the closest preceding workday.
- If the **due date** falls on a Saturday, Sunday, or Thai public holiday → due date is shifted **later** to the closest following workday.

The shifts are independent — a shifted bill cycle date does **not** change how the due date is computed (the due date still starts from the nominal day 25 + 20 days = day 14 of the next month, then gets its own shift if needed).

The "active cycle" comparison from the top of this note uses the *shifted* bill cycle date for UOB. So if day 25 has been pulled back to day 22 (because 23–25 are all non-working), then on day 22 onwards we're already in the next cycle.

Thai public holidays are sourced from the [`holidays`](https://pypi.org/project/holidays/) Python package, country code `TH`, official public-holiday set. The Bank of Thailand calendar can occasionally diverge by a day around substitution holidays — if a real-world bank statement disagrees with what the library computed, the script's output is overridable: pass `bill_cycle` / `due_date` explicitly in the add-transaction spec and the library is bypassed for that batch.

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
