---
tags: [promotion, uob-one]
---

# UOB One 2026 cashback promotion

The UOB One Account spend-and-save tiered-cashback promotion as it applies to UOB One supplement transactions in 2026. Carried over from 2025; the issuer has extended the same shape year-over-year, so the tier table and carve-outs below are stable across the 2025 → 2026 renewal.

> **Structured source of truth**: `scripts/repositories/promotions/uob-one-2026.yaml`.
> This page is the *narrative* — effective dates, tiers, exclusions and installment rule all live in the repo YAML, which is what `lib.promotions` and the skills read. Don't duplicate the structured fields here. If the issuer changes anything, update the YAML via [[../../.claude/skills/update-promotion/SKILL.md|/update-promotion]] and only re-summarise here when the *story* changes.

- **Effective**: `2026-01-01` → `2026-12-31`.
- **Card**: [[../cards/uob-one]] (Takumi primary; Baiboon and Nuta supplements).
- **Source**: the issuer's annual T&Cs; per-row patterns confirmed against Baiboon's and Nuta's 2026 statements.

## Tier story

Two **bonus** tiers stacked on a **base** rate:

- **10%** on transit + Café Amazon merchants (BTS / MRT / AMZ-named rows). Transit means BTS and MRT only: the SRT Red Line (`SRT RED LINE …`) earns the base 1% (user, 2026-10-07). Two 2025 Red Line rows carry Notes that disagree (10% and 1%); the 1% one stands.
- **5%** on convenience + grooming + Thailand-side ride-hail (`7-11`, `WATSON`, `WWW.GRAB.COM`, `GRABTAXI`) — but *not* `TMN 7-11`, which is a TrueMoney top-up at 7-Eleven that falls through to the base rate.
- **1%** on everything else not excluded.

Why the carve-outs: `TMN 7-11` is a TrueMoney top-up the user wanted treated as a TrueMoney transaction; `WWW.GRAB.COM` / `GRABTAXI` are Thailand-only because cross-border Grab purchases drop out of the bonus tier.

## Installment rule

Installment transactions earn **1% per installment row**, regardless of which tier the underlying purchase would have hit. The 1% accrues per installment as each row posts — it is *not* credited as one lump-sum on the purchase date.

This is the convention that makes UOB One's installments different from First Choice (where installment cashback typically arrives in a one-shot at purchase time).

A full charge converted later through **UOB PayLater** ends up the same way. UOB takes back the original charge's cashback on approval and pays it on each term instead ("…จะได้รับคะแนนสะสมหรือเครดิตเงินคืนตามยอดการชำระในแต่ละงวดแทน", [UOB PayLater page](https://www.uob.co.th/personal/cards/credit/uob-paylater.page), read 2026-10-05). The household hasn't had a PayLater conversion on UOB One yet. Whether the 1% counts a term's interest too is unconfirmed. See [[../concepts/installment-conversion-rates]].

## Exclusions

The promo does **not** override the project-wide exclusions:

- Foreign merchant billed in THB → no cashback / no points (set `×0`).
- Petrol stations on UOB cards → no cashback / no points.

When such a row is left at `% cb` unset, write a `Note` per [[../../.claude/skills/add-transaction/SKILL.md|/add-transaction]]'s exclusion-note rule.

## Cashback crediting

The household's agreement (user, 2026-05-25, kept 2026-09-28): the ledger credits UOB One **per bill cycle**, even though UOB counts 10%/5% per calendar month. [[../../.claude/skills/post-cashback-credits/SKILL.md|/post-cashback-credits]] (`scripts/python/lib/crediting/uob_one.py`) sums the cycle's rows per `% cb` tier and writes:

- **1%**: `UOB ONE CASHBACK 1%`, dated the cycle's BC date.
- **5%** / **10%**: `UOB ONE CASHBACK 5%` / `10%`, dated the first weekday of the following calendar month.

All are billed on the cycle itself (the explicit date-rule exception), and `[[../../.claude/skills/prepare-bill/SKILL.md|/prepare-bill]]` then sums the cycle flat. The [[../concepts/promotion-bureau|Promotion Bureau]] keeps the bank's view (calendar months, pooled caps) separately; it matters once the account nears the ฿500 cap, which is a separate question from what the friends pay.

**Past the ฿500 cap** (user, 2026-09-28): the rest of the month's 10%/5% spend earns 1%. `/sync-promotion` on the month's `UOB One cb 10%/5%` row asks for `% cb` 1% on those rows (the row the cap runs out on stays unset), and the 1% quota and the per-cycle credit then count them at 1%.

## Points

UOB One earns no points — `×0` multiplier on every transaction. This is a **card-level** rule (`scripts/repositories/cards/uob-one.yaml` → `points_default: "×0"`), not a promo-driven one. The promo's `points_default` echoes the card-level value for convenience.

## History

- **2025**: original promotion ran with the same tier table.
- **2026**: extended through `2026-12-31`. Tier table, carve-outs, exclusions, and installment rule unchanged.

If the issuer renews for 2027 with different terms, **branch** a fresh `scripts/repositories/promotions/uob-one-2027.yaml` via [[../../.claude/skills/add-promotion/SKILL.md|/add-promotion]] and set this promo's `effective_end` (if it isn't already past) via [[../../.claude/skills/update-promotion/SKILL.md|/update-promotion]]. Don't mutate the 2026 YAML's effective dates after the fact — preserve the historical reading.

## Caps, and the Promotion Bureau

The bank caps the cashback, and the two caps count over **different periods** (bank page, read 2026-09-28):

| Tiers | Cap | Counted per | Credited |
|---|---|---|---|
| 10% + 5% together | ฿500 | **calendar month**, by post date | last day of the month |
| 1% | ฿2,000 | **statement cycle** | within the cycle |

The caps are shared by everyone on the account and split first come, first served (user, 2026-09-28), so each has its own [[../concepts/promotion-bureau|Promotion Bureau]] row per period: `2026M9 — UOB One cb 10%/5%` (1–30 Sep) and `2026M9 — UOB One cb 1%` (25 Aug–24 Sep, the cycle billed 25 Sep). The tiers themselves still come from `uob-one-2026.yaml` through `lib.promotions.classify`; the Bureau classes (`scripts/python/lib/bureau/uob_one.py`) add only the caps. One exception the YAML doesn't know: **Makro in-store** (`MAKRO_…`) earns nothing, while its catch-all tier would give 1%.

September 2026, before Takumi's UOB statement (2026-09-28):

| Row | Pooled | Credit | Nuta | Baiboon |
|---|---|---|---|---|
| 10%/5% (1–30 Sep) | ฿2,417.50 | ฿132.63 | ฿120.80 | ฿11.83 |
| 1% (25 Aug–24 Sep) | ฿13,029.40 | ฿130.29 | ฿128.49 | ฿1.80 |

**Where this differs from the ledger's credit rows, on purpose.** The ledger credits per bill cycle (the household's agreement, above), the Bureau per calendar month (the bank's view), so Nuta's September 10%/5% is ฿120.80 in the Bureau against ฿173.60 in her cycle credit rows. The 1% share differs by ฿2.31, which is timing: Nuta's `TMN 7-11 ฿231` got its 1% in August's credit, but UOB pays it in September. Her `[ยอดยกมาจากรอบ 2026-08]` −฿231 leg (carrying `% cb` 1%) nets it out of September's ledger credit (฿126.18), and her tracker nets it the same way, while the Bureau share keeps the bank's ฿128.49.

**The bank's 1% vs the Bureau's, September 2026** (worked out 2026-09-28 from the 27 Sep statement, once Takumi's lines were recorded):

- The statement's 1%-tier lines (all three holders) total ฿12,892.40. That's ฿128.92, exactly the Bureau's figure, so the ledger and the statement agree line for line.
- UOB credited `UOB One Cashback 1%` ฿124.53. That's reproduced to the satang by two rules:
  - **Spend posted on the statement date counts toward the next cycle's 1%**, even though it's printed on this statement (UOB's terms say so too). Four purchases were posted 25 Sep: Nuta's `SHOPEE` ฿167, `SHOPEE *SHOPEE` ฿102, `TMN 7-11` ฿57 and `LINEPAY*PF_LINE MAN` ฿111.61, ฿437.61 in all. The installment terms posted that day roll forward too; September's base carries August's terms instead of its own (same amounts), see below.
  - **1% is rounded per line**, half up.
- Prediction: October's 1% credit includes those four lines (฿4.38).
- **Applied since 2026-09-28** (user: "use that to determine 1%/5%/10% cashback … even if using the household's rule, we follow the same rules as UOB"). `/record-statement` stamps `Process Date`, and the Bureau's `UOBOneBase` / `UOBOneBonus` count by it and round per line. The household's per-cycle credit rows (`lib.crediting.uob_one`) take a cycle's rows by the same statement-cycle rule. After re-stamping the Aug and Sep statements, `2026M9 — UOB One cb 1%` reads **฿124.53, the bank's credit to the satang**. Nuta's 25 Sep cycle credits became 1% −฿120.42 and 5% −฿156.20.
- **10%/5% follows the same rule, one level up:** spend posted on the **last day of the month** counts toward the next month. August's `UOB One Cashback 10% 5%` ฿188.40 (posted 31 Aug) is exactly 10%/5% of the lines posted 31 Jul–30 Aug, rounded per line (checked 2026-09-28 against both statements). That window includes July's last-day postings (Nuta's Grab ฿130) and leaves out 31 Aug's (five Nuta Grabs, ฿496). The Bureau's 10%/5% row counts by transaction date, 1–30 Sep, so it drifts at both edges. Lines posted 31 Aug–25 Sep already give ฿317.25 toward September's credit; lines posted 26–29 Sep will add to it on the October statement.
- **July reproduces exactly too:** ฿92.15 by the rules and ฿92.15 from UOB (June's statement, from Nuta's bill, supplied the roll-ins). July's statement was also paper-shifted: printed 26 Jul, but its last posting and its 1% credit were on 24 Jul.
- **August explained: installment terms roll forward too** (user's catch, 2026-09-28). A term posts on the statement date, so its 1% counts in the *next* cycle like anything else posted that day. The old rule counted each term in the cycle it's billed on:
  - August's terms included a new plan's first term, `2C2P *SHOPEE 01/10` ฿1,032.60, which July's terms didn't have. Under the old rule August came to ฿117.21, ฿10.33 more than UOB paid, and ฿10.33 is exactly 1% of that term.
  - Rolling terms forward, **July, August and September all reproduce to the satang**: ฿92.15, ฿106.88 and ฿124.53. July and September hid the mistake because the terms rolling out matched the terms rolling in.
  - August also rolled in a ฿26 `SHOPEEPAY*SHOPEE` posted on July's 24 Jul close. July's statement was paper-shifted too: printed 26 Jul, closed 24 Jul. `AIATH AUTO PAYMENT` earns 1%.

## Open questions

- ~~10%/5% by month or by cycle?~~ Settled 2026-09-28: the ledger stays per cycle (the household's agreement); the Bureau shows the bank's months.
- ~~Carry-forward rows with `% cb`?~~ Settled 2026-09-28: a timing difference. The Bureau share keeps the bank's view; the tracker nets the carry-forward leg, like the per-cycle ledger credit does.
- ~~August 2026's 1% shortfall~~ Explained 2026-09-28: installment terms roll forward like any statement-date posting (see above).
- ~~Count by posting date?~~ Done 2026-09-28: see above.
- Does Takumi's primary UOB One get the same supplement-side tier treatment, or do primary-card swipes count differently? Phase-1 data hasn't given a clean answer.

## See also

- `scripts/repositories/promotions/uob-one-2026.yaml` — the structured source of truth.
- [[../cards/uob-one]] — the card description and account-level facts.
- [[../concepts/promotions]] — the cross-cutting promotion concept.
- [[../concepts/cashback]] — the per-transaction `% cb` field.
- [[../../.claude/skills/post-cashback-credits/SKILL.md|/post-cashback-credits]] — the credit-row writer for this promo.
