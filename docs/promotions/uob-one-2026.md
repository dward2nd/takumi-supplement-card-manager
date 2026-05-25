---
tags: [promotion, uob-one]
---

# UOB One 2026 cashback promotion

The UOB One Account spend-and-save tiered-cashback promotion as it applies to UOB One supplement transactions in 2026. Carried over from 2025; the issuer has extended the same shape year-over-year, so the tier table and carve-outs below are stable across the 2025 → 2026 renewal.

> **Structured source of truth**: `scripts/repositories/promotions/uob-one-2026.yaml`.
> This page is the *narrative* — effective dates, tiers, exclusions, installment rule, and the crediting schedule all live in the repo YAML, which is what `lib.promotions` and the skills read. Don't duplicate the structured fields here. If the issuer changes anything, update the YAML via [[../../.claude/skills/update-promotion/SKILL.md|/update-promotion]] and only re-summarise here when the *story* changes.

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

## Cashback crediting schedule

Per the YAML's `crediting_schedule`:

- **1%** tier credited on the cycle's BC date.
- **5%** / **10%** tiers credited on the first weekday of the following calendar month.

[[../../.claude/skills/post-cashback-credits/SKILL.md|/post-cashback-credits]] reads this schedule and materializes the cashback as negative-amount transactions whose `Bill Cycle Date` / `Due Date` are aligned to the current cycle (the explicit date-rule exception). `[[../../.claude/skills/prepare-bill/SKILL.md|/prepare-bill]]` then sums the cycle flat.

## Points

UOB One earns no points — `×0` multiplier on every transaction. This is a **card-level** rule (`scripts/repositories/cards/uob-one.yaml` → `points_default: "×0"`), not a promo-driven one. The promo's `points_default` echoes the card-level value for convenience.

## History

- **2025**: original promotion ran with the same tier table.
- **2026**: extended through `2026-12-31`. Tier table, carve-outs, exclusions, and installment rule unchanged.

If the issuer renews for 2027 with different terms, **branch** a fresh `scripts/repositories/promotions/uob-one-2027.yaml` via [[../../.claude/skills/add-promotion/SKILL.md|/add-promotion]] and set this promo's `effective_end` (if it isn't already past) via [[../../.claude/skills/update-promotion/SKILL.md|/update-promotion]]. Don't mutate the 2026 YAML's effective dates after the fact — preserve the historical reading.

## Open questions

- Monthly cashback cap (account-level or card-level?) — not yet surfaced from the issuer T&Cs.
- Does Takumi's primary UOB One get the same supplement-side tier treatment, or do primary-card swipes count differently? Phase-1 data hasn't given a clean answer.

## See also

- `scripts/repositories/promotions/uob-one-2026.yaml` — the structured source of truth.
- [[../cards/uob-one]] — the card description and account-level facts.
- [[../concepts/promotions]] — the cross-cutting promotion concept.
- [[../concepts/cashback]] — the per-transaction `% cb` field.
- [[../../.claude/skills/post-cashback-credits/SKILL.md|/post-cashback-credits]] — the credit-row writer for this promo.
