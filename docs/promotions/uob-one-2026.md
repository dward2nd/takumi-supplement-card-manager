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

- **10%** on transit + Café Amazon merchants (BTS / MRT / AMZ-named rows).
- **5%** on convenience + grooming + Thailand-side ride-hail (`7-11`, `WATSON`, `WWW.GRAB.COM`, `GRABTAXI`) — but *not* `TMN 7-11`, which is a TrueMoney top-up at 7-Eleven that falls through to the base rate.
- **1%** on everything else not excluded.

Why the carve-outs: `TMN 7-11` is a TrueMoney top-up the user wanted treated as a TrueMoney transaction; `WWW.GRAB.COM` / `GRABTAXI` are Thailand-only because cross-border Grab purchases drop out of the bonus tier.

## Installment rule

Installment transactions earn **1% per installment row**, regardless of which tier the underlying purchase would have hit. The 1% accrues per installment as each row posts — it is *not* credited as one lump-sum on the purchase date.

This is the convention that makes UOB One's installments different from First Choice (where installment cashback typically arrives in a one-shot at purchase time).

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

The caps are shared by everyone on the account and split first come, first served (user, 2026-09-28), so each has its own [[../concepts/promotion-bureau|Promotion Bureau]] row per period: `2026M9 — UOB One cb 10%/5%` (1–30 Sep) and `2026M9 — UOB One cb 1%` (26 Aug–25 Sep). The tiers themselves still come from `uob-one-2026.yaml` through `lib.promotions.classify`; the Bureau classes (`scripts/python/lib/bureau/uob_one.py`) add only the caps. One exception the YAML doesn't know: **Makro in-store** (`MAKRO_…`) earns nothing, while its catch-all tier would give 1%.

September 2026, before Takumi's UOB statement (2026-09-28):

| Row | Pooled | Credit | Nuta | Baiboon |
|---|---|---|---|---|
| 10%/5% (1–30 Sep) | ฿2,417.50 | ฿132.63 | ฿120.80 | ฿11.83 |
| 1% (26 Aug–25 Sep) | ฿13,029.40 | ฿130.29 | ฿128.49 | ฿1.80 |

**Where this differs from the ledger's credit rows, on purpose.** The ledger credits per bill cycle (the household's agreement, above), the Bureau per calendar month (the bank's view), so Nuta's September 10%/5% is ฿120.80 in the Bureau against ฿173.60 in her cycle credit rows. The 1% share differs by ฿2.31, which is timing: Nuta's `TMN 7-11 ฿231` got its 1% in August's credit, but UOB pays it in September. Her `[ยอดยกมาจากรอบ 2026-08]` −฿231 leg (carrying `% cb` 1%) nets it out of September's ledger credit (฿126.18), and her tracker nets it the same way, while the Bureau share keeps the bank's ฿128.49.

## Open questions

- ~~10%/5% by month or by cycle?~~ Settled 2026-09-28: the ledger stays per cycle (the household's agreement); the Bureau shows the bank's months.
- ~~Carry-forward rows with `% cb`?~~ Settled 2026-09-28: a timing difference. The Bureau share keeps the bank's view; the tracker nets the carry-forward leg, like the per-cycle ledger credit does.
- Does Takumi's primary UOB One get the same supplement-side tier treatment, or do primary-card swipes count differently? Phase-1 data hasn't given a clean answer.

## See also

- `scripts/repositories/promotions/uob-one-2026.yaml` — the structured source of truth.
- [[../cards/uob-one]] — the card description and account-level facts.
- [[../concepts/promotions]] — the cross-cutting promotion concept.
- [[../concepts/cashback]] — the per-transaction `% cb` field.
- [[../../.claude/skills/post-cashback-credits/SKILL.md|/post-cashback-credits]] — the credit-row writer for this promo.
