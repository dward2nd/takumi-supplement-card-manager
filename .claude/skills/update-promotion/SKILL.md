---
name: update-promotion
description: Patch an existing promotion YAML in `scripts/repositories/promotions/<id>.yaml` — adjust effective dates, status, tiers, foreign-in-THB policy, installment rule, or crediting schedule. Use when the user says "extend the UOB One promo to 2027", "mark this promotion superseded", "add Agoda to the foreign-in-THB overrides", or otherwise wants to change an active or historical promo.
---

# update-promotion

Patches **one** promotion file in `scripts/repositories/promotions/`. Loads the existing YAML, merges the spec's `set` patch at the top level (list-valued fields are *replaced* whole, not merged element-by-element), validates the merged result against the schema, and writes it back.

## Primary execution path — the deterministic script

```sh
echo '<JSON-spec>' | uv run scripts/python/update-promotion/cli.py
# --dry-run to preview the merged result without writing
```

Spec:

```json
{
  "id":  "uob-one-2026",
  "set": {
    "effective_end": "2026-12-31",
    "status":        "active"
  }
}
```

Patchable fields (everything except `id`):

`name`, `card`, `effective_start`, `effective_end`, `status`, `points_default`, `foreign_in_thb_policy`, `tiers`, `installment_rule`, `crediting_schedule`.

## Hard rules

### 1. `id` is not patchable

To rename a promotion, delete the file and use [[../add-promotion/SKILL.md|/add-promotion]] to create a fresh one (then audit any references). Renames are rare enough that hands-on is fine.

### 2. List-valued fields replace, not merge

Sending `set: { tiers: [...] }` **replaces the entire tiers list**. If you want to add one tier, copy the existing list, add yours, and send the full result. The CLI does not infer "insert" / "remove" semantics.

The same applies to `foreign_in_thb_policy.overrides` — you replace the whole policy block when you patch it.

### 3. Status transitions

`status` moves through: `active` → `superseded` (when a new promo for the same card takes over) or `active` → `expired` (when the issuer ends the promo with no successor). When marking a promo `superseded`, also set its `effective_end` to the last day it applied.

The classification lib only considers `status: active` promos within their effective window.

### 4. Schema validation runs on the merged result

If the patch produces an invalid promo (e.g. unknown `foreign_in_thb_policy.default` value, malformed tier), the CLI aborts before writing.

### 5. Don't silently invalidate historical classifications

If a promo has been used to classify transactions and you change its tier rates, those transactions' `% cb` values won't auto-update. After the patch, either:
- Audit the affected transactions and re-classify with [[../update-transaction/SKILL.md|/update-transaction]] (with `cashback_percent` per row), or
- Leave history alone and document the change in `docs/promotions/<id>.md`.

## Common patches

| User said... | `set` body |
|---|---|
| "Extend UOB One to 2027" | `{ "effective_end": "2027-12-31" }` |
| "Mark this superseded as of today" | `{ "status": "superseded", "effective_end": "2026-05-25" }` |
| "Add Agoda override at 1.5%" | `{ "foreign_in_thb_policy": { "default": "exclude", "overrides": [{ "merchant_substring": "AGODA", "rate": 0.015, "keeps_points_exclusion": true }] } }` |
| "Drop the installment rule" | `{ "installment_rule": null }` |
| "Change 5% tier to 7%" | `{ "tiers": [ ... full tiers list with the 5% one changed to 7% ... ] }` |

## Procedure

1. **Confirm which promo** the user means; identify by `id` (or look up by card + period in `scripts/repositories/promotions/`).
2. **Build the smallest `set` block** that captures the change. Include full lists for list-valued fields.
3. **Run `--dry-run` first** for list replacements (`tiers`, `overrides`) — they're the easy way to accidentally drop rules.
4. **Run the script.** Read the envelope, surface `{id, path, fields, previous}` back to the user.
5. **Flag downstream impact** if the change affects already-classified transactions; offer to re-run [[../update-transaction/SKILL.md|/update-transaction]].

## What this skill does NOT do

- Does **not** create new promotions. Use [[../add-promotion/SKILL.md|/add-promotion]].
- Does **not** rename promotions (id is the filename — delete + recreate by hand).
- Does **not** mutate cards or transactions.
- Does **not** translate Thai or rename fields.
