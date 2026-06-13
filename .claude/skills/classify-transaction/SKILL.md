---
name: classify-transaction
description: Preview the cashback / points classification a promotion would assign to one or more transactions — `% cb`, multiplier, the tier/exclusion reason, and the suggested Note — WITHOUT writing anything. Read-only. Use when the user asks "what cashback would this merchant earn?", "how would this be classified?", "is this 5% or 1%?", or wants to eyeball the auto-classification before committing it via /add-transaction.
---

# classify-transaction

Read-only preview of how the active promotion(s) would classify a transaction. It is the **inspectable front-end** to `lib.promotions.classify` — the exact logic that [[../add-transaction/SKILL.md|/add-transaction]], [[../add-installment/SKILL.md|/add-installment]] and [[../populate-installment/SKILL.md|/populate-installment]] run behind `auto_classify: true`. The difference is that this skill **never writes**: it shows you the `% cb`, the multiplier, the reason it landed in that tier (or got excluded), and the suggested `Note`, so you can review — and override — before any row is created.

It touches **neither Notion nor any repo file**. Classification is pure: it reads the card repo (`scripts/repositories/cards/`) and the promotion YAML (`scripts/repositories/promotions/`) only. That's why it's safe to run freely.

## Primary execution path — the deterministic script

Backed by `scripts/python/classify-transaction/cli.py` (a thin wrapper over `lib.promotions.classify`).

```sh
echo '<JSON-spec>' | uv run scripts/python/classify-transaction/cli.py
```

JSON spec:

```json
{
  "card": "UOB One",
  "transactions": [
    { "date": "2026-05-29", "name": "WWW.GRAB.COM BANGKOK TH", "amount": 250 },
    { "date": "2026-05-29", "name": "2C2P *SHOPEE 03/10",      "amount": 1079.2 }
  ]
}
```

- **`card`** is required — the verbatim card name (same string the promotions key on). A single transaction may be passed inline at the top level (`{card, date, name, amount}`) instead of via `transactions`.
- **`date`** matters: promotions are dated, so a transaction outside a promo's effective window classifies differently. Pass the real transaction date.
- **`name`** is the verbatim merchant string — the matcher keys on it (tier tokens, `NN/NN` installment suffix, foreign country suffix, petrol tokens). Don't clean it.
- **`amount`** is optional. When present, the preview also reports the baht cashback (`% cb` × amount) so you can sanity-check the payout.

## Reading the output

Each row reports:

- **`reason`** — the tag explaining the verdict: `tier` (matched a cashback tier), `installment` (`NN/NN` row → promo's installment rate), `foreign-override` / `foreign-default-exclude` (foreign-merchant-in-THB handling), `petrol-exclusion` (UOB fuel), `no-tier-match` (promo active but merchant fell through), `no-promo` (no active promotion on this card+date).
- **`cashback_percent`** (raw fraction, e.g. `0.05`) + **`cashback_display`** (`"5%"`). `null` = leave `% cb` unset (the row earns no cashback — see [[../add-transaction/SKILL.md|/add-transaction]] rule 4b: never write an explicit `0`).
- **`multiplier`** — the points multiplier the promo/card implies (`"×0"` for UOB One; `null` = default ×1 earning).
- **`note`** — the suggested exclusion/explanation Note (e.g. petrol, installment), or `null`.
- **`card_known`** (top level) — `false` means the card name isn't in `scripts/repositories/cards/`, i.e. almost certainly a **typo** (e.g. `UOB ONE` vs `UOB One`); the classification then degrades to `no-promo`. Always check this before trusting a `no-promo` result.

## What the user typically asks

- "What cashback would Nuta's UOB One give on GRAB / Café Amazon / 7-11?" → tiers (10 / 10 / 5%, or 1% for `TMN 7-11`).
- "Is this Shopee installment row earning cashback?" → `installment`, 1% per row.
- "Would a PTT charge on UOB One earn anything?" → `petrol-exclusion`, none.
- "Show me how this whole batch classifies before I add it." → pass the batch, eyeball, then hand explicit values to [[../add-transaction/SKILL.md|/add-transaction]].

## Hard rules

### 1. Read-only — never writes

No Notion calls, no repo writes. If the user wants the classification *applied*, hand the previewed `cashback_percent` / `multiplier` / `note` to [[../add-transaction/SKILL.md|/add-transaction]] (per-row), or run it there with `auto_classify: true`.

### 2. Verbatim merchant names

Pass the merchant string exactly as supplied — the tier/installment/foreign/petrol detection all key off it. Cleaning the name changes the verdict.

### 3. Classification ≠ guarantee

These are the promo's *rules as encoded*. Genuinely ambiguous merchants (aggregators that could span tiers) still need a human eyeball — that's the whole point of previewing. Surface ambiguity rather than trusting the tag blindly.

## What this skill does NOT do

- Does **not** write transactions — see [[../add-transaction/SKILL.md|/add-transaction]].
- Does **not** read or reconcile against Notion — it's a pure repo-driven preview. For what's actually *in* Notion, see [[../fetch-transactions/SKILL.md|/fetch-transactions]].
- Does **not** declare or edit promotions — see [[../add-promotion/SKILL.md|/add-promotion]] / [[../update-promotion/SKILL.md|/update-promotion]].
- Does **not** apply to Takumi's cashback (Takumi's Transactions DS has no `% cb`); a classification preview is still informational, but the value can't be stored there.
- Does **not** translate Thai labels.
