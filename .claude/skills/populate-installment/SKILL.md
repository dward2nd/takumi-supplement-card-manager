---
name: populate-installment
description: For every in-progress installment plan on a holder + card, append the next term (`NN+1`) to the target bill cycle. Use when the user says "populate installments on Nuta's UOB One", or when /prepare-bill calls in to fill out a cycle before summing. Idempotent — re-runs against the same cycle skip plans whose next term already lives there. The companion skill [[../add-installment/SKILL.md|/add-installment]] starts new plans.
---

# populate-installment

For each in-progress installment plan on the named holder + card, writes one Notion transaction row representing the next term (`NN+1` of the plan's total) into the **target cycle**. The companion of [[../add-installment/SKILL.md|/add-installment]] — that skill seeds plans, this one continues them.

This is the only sanctioned write path for continuing installments. Together they replace the old workflow of typing every `NN/NN` row by hand via [[../add-transaction/SKILL.md|/add-transaction]].

## Primary execution path — the deterministic script

Backed by `scripts/python/populate-installment/cli.py`. Pulls every transaction tied to the card, filters to those whose merchant name carries the `NN/NN` installment suffix, groups them by **(base merchant, total terms, per-term amount)**, then for each group decides what to do.

The per-term amount is what distinguishes parallel plans with the same bank-side merchant string (the user often runs several `2C2P *SHOPEE 10`-term plans concurrently, each at a different baht/term). Within a `(base, total)` group, rows are clustered greedily by amount with a 2% tolerance — enough to absorb the small per-term rounding the bank sometimes applies (375.30 → 373.00 across consecutive terms, ~0.6%), yet tight enough to keep genuinely-distinct plans apart (e.g. two Shopee plans at 1,032.60 and 1,079.20 per term, only 4.3% apart, must not merge). Tightened from 5% on 2026-07-26.

Per-cluster decisions:

| Condition | `action` | What happens |
|---|---|---|
| `base` listed in `exclude` | `skipped-excluded` | No write. Use when the user has cancelled / closed a plan early. |
| `max_term >= total_terms` | `skipped-complete` | No write. Plan finished. |
| Any row in cluster already sits on the target cycle | `skipped-already-in-cycle` | No write. Idempotency guard — covers /add-installment writing `01/N` in this cycle and /populate-installment then being run on the same cycle. |
| Otherwise | `appended` | Writes a new row with `term = max_term + 1`, same base, **previous term's amount**, target BC/DD. Transaction date == BC. |

Invocation:

```sh
echo '<JSON-spec>' | uv run scripts/python/populate-installment/cli.py
# add --dry-run to preview without writing
```

JSON spec — `holder` and `card` are required, everything else optional:

```json
{
  "holder":         "nuta",
  "card":           "UOB One",
  "bill_cycle":     "2026-05-25",         // optional; defaults to most-recently-closed cycle
  "exclude":        ["2C2P *SHOPEE"],     // optional list of base names to skip
  "auto_classify":  true                   // optional, default true
}
```

Output envelope:

```json
{
  "holder": "nuta", "card": "UOB One",
  "bill_cycle": "2026-05-25", "due_date": "2026-06-15",
  "in_progress": [
    {
      "base": "2C2P *SHOPEE", "total_terms": 10, "max_term": 2,
      "per_term_amount": 1079.20,
      "action": "appended",
      "next_term": 3, "next_name": "2C2P *SHOPEE 03/10",
      "amount": 1079.20,
      "classification": { "promotion_id": "uob-one-2026", "reason": "installment", ... },
      "created": { "id": "...", "url": "...", "name": "2C2P *SHOPEE 03/10", "amount": 1079.20, "date": "2026-05-25" }
    },
    { "base": "...", "action": "skipped-complete", ... },
    { "base": "...", "action": "skipped-already-in-cycle", ... }
  ],
  "count_appended": <int>,
  "count_skipped":  <int>
}
```

## What the user supplies

1. **Holder + card** — the scope. The skill runs against one (holder, card) at a time. No "do every card on every holder" mode by design — bills are per-card and the user usually populates as they prepare each bill.
2. **Optional `bill_cycle`** — the target cycle. Defaults to most-recently-closed.
3. **Optional `exclude`** — base merchant names to skip when the user has cancelled or closed a plan early.

## Idempotency & continuity

The user said: *installments should be continuous unless I say otherwise — e.g. I close one earlier, or I cancelled the payment*. So:

- The skill **does not stop** at any plan by default. Running it monthly is the steady-state expectation.
- Stopping a plan is the user's action: archive the latest row, or pass `exclude: ["<base>"]` for that run.
- Re-running the skill on the same cycle is a no-op — the `skipped-already-in-cycle` branch makes this safe.

## When this skill runs

- **Manually** — the user invokes `/populate-installment` for a card after a cycle closes, or before drafting a bill.
- **Automatically from /prepare-bill** — the bill-drafting skill calls this first, so the cycle's sum already includes all installment terms (see [[../prepare-bill/SKILL.md|/prepare-bill]]).

## Hard rules

### 1. Same routing rules as /add-transaction

Holder → DS, exact card-title match. The script uses `lib.holders.resolve_holder` and `lib.cards.find_card`; cross-writes are impossible.

### 2. Parallel plans are clustered by per-term amount

Two rows in the same `(base, total)` group belong to the same plan when their amounts match within 2%. Bank rounding (a few baht across terms) is absorbed; genuinely separate plans (e.g. one at 1,032.60 baht/term and another at 1,079.20 — 4.3% apart) sit in distinct clusters and advance independently.

If the user wants stricter separation (e.g. two plans at very close amounts) they should disambiguate by adding a unique qualifier to the base name when starting the second plan via [[../add-installment/SKILL.md|/add-installment]].

### 3. Next term inherits the previous term's amount

For a 10-month plan whose last posted term was 02/10 at 1079.20, the next term written is 03/10 at 1079.20 — the bank typically holds the per-term amount constant. If the bank statement reveals a different figure, patch the row with [[../update-transaction/SKILL.md|/update-transaction]] after the fact.

### 4. Auto-classify by default

The new row is classified via `lib.promotions.classify` with `is_installment_override=True`. On UOB One that hits the promo's `installment_rule` → 1% cashback + `×0`. Pass `auto_classify: false` to leave `% cb` and the multiplier unset (e.g. for First Choice plans where the user wants to leave classification manual).

## Procedure

1. **Confirm holder + card.** If the user says "populate Nuta's UOB One", that's the scope; no extra clarification needed.
2. **Confirm the target cycle.** Default is most-recently-closed.
3. **Run dry-run first** when the data is unfamiliar — surfaces the plan list and the proposed actions so the user can flag anomalies before writing.
4. **Run for real**, surface a compact list per plan: base name, per-term amount, action, and the new term's row if appended.
5. **Anomalies to mention** when reporting:
   - More than one cluster within the same `(base, total)` → confirms parallel plans (usually fine, worth a one-liner so the user knows the skill saw both).
   - A plan whose previous term's amount looks different from the bank-statement figure for this cycle → the user may want to `/update-transaction` after populate.

## What this skill does NOT do

- Does **not** start new plans — use [[../add-installment/SKILL.md|/add-installment]].
- Does **not** edit existing terms — use [[../update-transaction/SKILL.md|/update-transaction]].
- Does **not** create bills or finalize cycles — that's [[../prepare-bill/SKILL.md|/prepare-bill]] and [[../update-bill/SKILL.md|/update-bill]].
- Does **not** detect cancelled plans automatically. The user signals cancellation by either archiving the rows or passing `exclude`.
