---
tags: [concept, rewards]
---

# Cashback promotions

Cashback (`% cb` on Baiboon's and Nuta's Transactions DSes — see [[../databases/baiboon-transactions]] / [[../databases/nuta-transactions]]) is the *output* of applying an active **promotion** to a transaction. The agent treats the per-row `% cb` value as the resolved rate; the *why* (which promotion granted it, why exclusions applied) lives in `Note`.

**Structured source of truth**: `scripts/repositories/promotions/<id>.yaml`. One YAML file per promotion. See `scripts/repositories/README.md` for the schema and `scripts/python/lib/promotions.py` for the classification logic. The narrative pages under [[../promotions/|docs/promotions/]] tell the story; the YAML drives the scripts.

## Why promotions, not card policies

Issuers run cashback as time-bound promotions, even when they look permanent:

- **UOB One**'s tier system has been a stable promotion year-over-year (currently extended through `2026-12-31`), but it *could* change at the next renewal. Treating it as a dated promotion makes that renewal a doc-level edit, not a model change.
- **First Choice** runs short-duration promos (e.g. the May 2026 2% campaign with an explicit Agoda inclusion). These come and go.
- Some cards may have **no** active promotion at a given time — those transactions earn nothing.

Treating cashback as "promotion + dates" instead of "card-level rate" makes year-over-year changes, historical reconciliation, and cross-card comparisons cleaner.

## Active promotions

| Card           | Promotion                                       | Effective                       |
|----------------|-------------------------------------------------|---------------------------------|
| UOB One        | [[../promotions/uob-one-2026]]                  | `2026-01-01` → `2026-12-31`     |
| First Choice   | ad-hoc — not yet documented at promotion level  | the user updates rows manually  |

When a new promotion arrives, add it under [[../promotions/]] and link from the card's note.

## General rules that interact with promotions

### Foreign merchant billed in THB

**Default**: foreign-merchant-in-THB earns **neither cashback nor points** on any Thai-issued card. The country suffix in the merchant string (`US`, `USA`, `JP`, `SG`, etc.) flags this.

**Promotion overrides for cashback**: a promo can grant cashback to foreign-in-THB transactions if it *explicitly* names them. Document the override in the promotion's note.

**Promotion overrides for points**: almost never. Cashback promos typically say nothing about points, so the foreign-in-THB rule still excludes points even when cashback is granted. **Set `×0`** on the row to encode "no points".

**Example**: First Choice's May 2026 2% promo explicitly grants **1.5%** cashback on Agoda (foreign, SG, billed in THB). The Agoda row receives 1.5% `% cb` and `×0` (no points). The `Note` explains both — the cashback came from the promo's explicit inclusion; the points exclusion came from the default rule the promo did not override.

### Petrol stations on UOB cards

UOB cards (One, World, Premier, Makro) earn nothing at petrol stations. No promotion has been seen to override this. Watch for merchant strings containing `PT`, `BCP`, `ESSO`, `SHELL`, `CALTEX`, `PTT`.

### Installment transactions

Installment cashback varies per issuer; document the rule on the relevant **promotion** note, not the card note:

- **UOB One** (per [[../promotions/uob-one-2026#installment-rule]]): 1% per installment row, regardless of merchant tier. Credited per installment, not all at once.
- **First Choice**: installment promotion treatment varies by promo — ask the user; never reflexively apply the same rate as on the non-installment rows.

## How to classify a transaction

**Easiest**: let the script do it via `/add-transaction` with `auto_classify: true`. The CLI calls `lib.promotions.classify(card, date, merchant)` for each row, applies the active promo's rules (including the foreign-in-THB and petrol exclusions and the installment override), and fills `% cb` / multiplier / Note accordingly. Per-row spec values still win over auto-classified values, so the user can override anytime.

**Manually** (agent procedure, when not using auto_classify):

1. Identify the card and the transaction date.
2. Look up the active promotion(s) for that card on that date (`scripts/repositories/promotions/`; or check the narrative under [[../promotions/]]).
3. Apply the promo's tier rules / exclusions / installment treatment to the merchant string.
4. Cross-check the general rules above (foreign-in-THB, UOB petrol). If they exclude the row, the promo doesn't grant cashback unless it explicitly overrides.
5. Write `% cb` per row. Leave unset on excluded rows. Add a `Note` whenever a row is excluded for a reason beyond the card/promo's headline.

## Adding or updating a promotion

- [[../../.claude/skills/add-promotion/SKILL.md|/add-promotion]] — writes a new `scripts/repositories/promotions/<id>.yaml`.
- [[../../.claude/skills/update-promotion/SKILL.md|/update-promotion]] — patches an existing one (effective dates, status, tiers, etc.).

After adding or updating, the change is immediately visible to `lib.promotions` — no Python edit required.

## See also

- [[cashback]] — the per-transaction cashback field/formula.
- [[../promotions/uob-one-2026]] — the currently-active UOB One promo.
- [[../../.claude/skills/add-transaction/SKILL|/add-transaction]] — the write skill's policy section pulls from this doc.
