---
name: add-promotion
description: Declare a new cashback promotion in the repository at `scripts/repositories/promotions/<id>.yaml`. Use when the user describes a new cashback campaign — its card, effective dates, tier rules, optional foreign-in-THB overrides and installment treatment. The promotion immediately becomes available to `lib.promotions.classify` and downstream skills (/add-transaction auto-classify, /classify-transaction). How the bank pays the cashback back is not YAML — a Crediting class in `scripts/python/lib/crediting/`.
---

# add-promotion

Creates **one** promotion YAML file at `scripts/repositories/promotions/<id>.yaml`. The schema and downstream consumers are documented in `scripts/repositories/README.md`.

## Primary execution path — the deterministic script

```sh
echo '<JSON-spec>' | uv run scripts/python/add-promotion/cli.py
# --dry-run to validate + serialize without touching disk
# --force to overwrite an existing file (refuses by default)
```

Minimum spec:

```json
{
  "id": "first-choice-2026-q3",
  "name": "First Choice Q3 2026 promo",
  "card": "First Choice",
  "effective_start": "2026-07-01",
  "effective_end": "2026-09-30",
  "status": "active",
  "tiers": [
    { "rate": 0.02, "label": "base", "patterns": ["*"] }
  ]
}
```

Full spec (every optional block):

```json
{
  "id":              "uob-one-2027",
  "name":            "UOB One 2027 cashback promotion",
  "card":            "UOB One",
  "effective_start": "2027-01-01",
  "effective_end":   "2027-12-31",
  "status":          "active",
  "points_default":  "×0",
  "foreign_in_thb_policy": {
    "default": "exclude",
    "overrides": [
      { "merchant_substring": "AGODA", "rate": 0.015, "keeps_points_exclusion": true }
    ]
  },
  "tiers": [
    { "rate": 0.10, "label": "bonus", "patterns": ["BTS", "MRT", "AMZ"] },
    { "rate": 0.05, "label": "bonus", "patterns": ["7-11", "WATSON"], "exclude_patterns": ["TMN 7-11"] },
    { "rate": 0.01, "label": "base",  "patterns": ["*"] }
  ],
  "installment_rule": { "rate": 0.01, "credited": "per_installment" }
}
```

## Hard rules

### 1. Card must already exist in the repo

The `card` field must match an existing `scripts/repositories/cards/<slug>.yaml` (`name:` field, exact match). Add the card YAML first if it doesn't exist.

### 2. `id` is the filename — keep it stable

The promo's `id` is its filename slug. Once a promotion is active and referenced by transactions, **don't rename it**. Use /update-promotion for everything except renames; a rename is delete + recreate by hand.

### 3. Each promo's effective dates don't overlap on the same card

Two active promotions on the same card with overlapping effective ranges create ambiguous classifications. The lib resolves ties by `effective_start` descending (most recent wins), but **prefer non-overlapping ranges**. When the issuer renews a year-over-year promo, set the old one's `effective_end` (via /update-promotion → `set: { effective_end: "2026-12-31" }`) before adding the new one.

### 4. Don't change the card-level points default here

`points_default` on a promotion is a convenience override; the card's own `points_default` (in `scripts/repositories/cards/<slug>.yaml`) is the canonical source. Set the promo's only when the promo itself changes the default (rare — happens when a card normally earns points but the promo's terms suspend them).

### 5. Crediting is code, not YAML

How the issuer pays the cashback back (periods, dates, caps) is a `Crediting` class per card in `scripts/python/lib/crediting/`; `crediting_schedule` was retired 2026-09-28. A new card for [[../post-cashback-credits/SKILL.md|/post-cashback-credits]] needs a class there, not a YAML key.

## Procedure

1. **Clarify what the user is telling you.** Effective dates? Tier rules? Carve-outs? Installment treatment? Crediting schedule? If any of these is unclear, ask before writing.
2. **Verify the card exists** in `scripts/repositories/cards/`. If not, create it first (small YAML — see the existing examples).
3. **Build the JSON spec.** Skip optional blocks if the user hasn't specified them; better to leave defaults than to invent rules.
4. **Run `--dry-run` first** for any non-trivial promo so the user can see the resolved YAML before disk write.
5. **Run the script.** Read the envelope, surface `{id, path, status}` back to the user.
6. **Reciprocal-link the narrative doc.** If a `docs/promotions/<id>.md` exists or should exist, point at the repo file as the source of truth (don't duplicate structured data into the narrative).

## What this skill does NOT do

- Does **not** patch existing files. Use [[../update-promotion/SKILL.md|/update-promotion]].
- Does **not** delete promotions. Remove the file by hand (and audit transactions that referenced it).
- Does **not** mutate cards. Edit `scripts/repositories/cards/<slug>.yaml` directly.
- Does **not** mutate transactions. Use [[../update-transaction/SKILL.md|/update-transaction]] to re-classify rows when a promo changes.
- Does **not** translate Thai. Property names, tier patterns, and merchant strings stay verbatim per project convention.
