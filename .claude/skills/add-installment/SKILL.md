---
name: add-installment
description: Write the first term (`01/NN`) of a new installment plan to one cardholder's Notion Transactions database. Use when the user announces a new installment purchase — e.g. "2C2P *SHOPEE in 10 months, 449.10 baht/term on Nuta's UOB One". The bill cycle defaults to the most recently closed cycle; transaction date == bill cycle date. The companion skill [[../populate-installment/SKILL.md|/populate-installment]] adds the subsequent terms.
---

# add-installment

Writes one Notion transaction row — the first term, labelled `01/NN` — of a new installment plan on one of a holder's supplement cards.

This is the only sanctioned write path for the *first* term of an installment. Subsequent terms come from [[../populate-installment/SKILL.md|/populate-installment]]. Together they replace the old workflow of typing each `NN/NN` row by hand via [[../add-transaction/SKILL.md|/add-transaction]].

## Primary execution path — the deterministic script

This skill is backed by `scripts/python/add-installment/cli.py`. Use it; do not reinvent the write with raw MCP calls. The script enforces the same hard rules as [[../add-transaction/SKILL.md|/add-transaction]] (verbatim merchant name, holder → DS routing, exact card-title resolution, `Processed=true`), and additionally:

- Appends the `01/<total>` suffix itself — the spec passes the **base** merchant name, not the suffixed form.
- Sets `Transaction Datetime` equal to `Bill Cycle Date` (banks post installment terms onto the BC date itself).
- Defaults `bill_cycle` to the **most recently closed cycle** (see [[../../../docs/concepts/bill-cycle-patterns|bill-cycle-patterns]]). Banks bill the first installment in the just-closed statement, not the still-accumulating one. Override by passing `bill_cycle` explicitly when back-filling an older plan or starting on the upcoming cycle.
- Auto-classifies by default — on UOB One, the active promo's `installment_rule` resolves to **1%** cashback + `×0` multiplier, with a default `Note` explaining the rate.

Invocation:

```sh
echo '<JSON-spec>' | uv run scripts/python/add-installment/cli.py
# add --dry-run to preview the payload without writing
```

JSON spec:

```json
{
  "holder":           "nuta",
  "card":             "UOB One",
  "merchant":         "2C2P *SHOPEE",
  "term_amount":      449.10,
  "total_terms":      10,
  "bill_cycle":       "2026-05-25",       // optional; defaults to most-recently-closed cycle
  "auto_classify":    true,                // optional, default true
  "multiplier":       "×0",                // optional override
  "cashback_percent": 0.01,                // optional override (raw fraction)
  "note":             "..."                // optional; auto-filled when auto_classify hits
                                           //   the installment rule
}
```

Output:

```json
{
  "holder": "nuta", "card": "UOB One",
  "bill_cycle": "2026-05-25", "due_date": "2026-06-15",
  "merchant_base": "2C2P *SHOPEE", "total_terms": 10,
  "name": "2C2P *SHOPEE 01/10", "term_amount": 449.10,
  "classification": { "promotion_id": "uob-one-2026", "reason": "installment",
                       "cashback_percent": 0.01, "points_override": "×0" },
  "created": { "id": "...", "url": "...", "name": "...", "amount": 449.10, "date": "2026-05-25" }
}
```

## What the user supplies

1. **Cardholder** — Takumi / Baiboon / Nuta.
2. **Card name** — exact title in that holder's Cards DB.
3. **Base merchant name** — *without* the `NN/NN` suffix (e.g. `2C2P *SHOPEE`). The script appends `01/<total_terms>`.
4. **Per-term amount in baht** — what the bank bills each cycle.
5. **Total number of terms** — e.g. `10` for a 10-month plan.
6. **Optional `bill_cycle`** — if the plan's first term lands on a non-default cycle. Default is the most recently closed cycle for the card.

## Hard rules (the script enforces these)

### 1. Base merchant name is verbatim

`merchant` in the spec must be the exact base string the bank shows, minus the `NN/NN`. Don't normalize, don't shorten. The script writes `Name = "<base> 01/<total>"`.

If you ever pass a base that already ends with `NN/NN`, the validator rejects the spec — that mistake would put two suffixes on the row.

### 2. Transaction date == bill cycle date

Banks post installment terms onto the cycle's BC date itself. The script sets `Transaction Datetime` and `Bill Cycle Date` to the same ISO date. If the user later wants to record the original purchase date for context, it goes in `Note` — not on the `Transaction Datetime` field, which the bank statement and `/prepare-bill` rely on.

### 3. Bill cycle defaults to most-recently-closed

`active_cycle` (used by [[../add-transaction/SKILL.md|/add-transaction]]) returns the cycle currently accumulating. Installments instead post to the cycle that just closed — the bank already cut the statement and the first term lives there. The script uses `lib.bill_cycle.most_recent_closed_cycle` for this.

Pass `bill_cycle` explicitly only when:
- Back-filling a plan whose first term posted to an older statement.
- The plan's first term lands on the *upcoming* cycle (rare; check the bank's statement before assuming).

### 4. Parallel plans with the same base

The user often runs multiple parallel installments under the same bank-side merchant string (e.g. several `2C2P *SHOPEE` 10-term plans, each with a different per-term amount). The repo already has the precedent — see existing Nuta UOB One data — so the skill does **not** refuse a new plan when an in-progress one shares the same `(base, total_terms)`. The disambiguator is the per-term amount, which [[../populate-installment/SKILL.md|/populate-installment]] uses to cluster rows into distinct plans.

If the user explicitly wants one plan only, point them at the existing in-progress row and skip the write.

### 5. Default classification: 1% cashback + `×0` on UOB One

`auto_classify: true` (the default) runs `lib.promotions.classify` with `is_installment_override=True`, so the active promo's `installment_rule` decides the rate. For UOB One that's 1% per term and `×0` (the card never earns points). For First Choice, **don't** auto-classify cashback: pass `auto_classify: false` and ask the user — First Choice may credit installment cashback at purchase time only (see [[../add-transaction/SKILL.md|/add-transaction]] for the First Choice exception).

## Procedure

1. **Confirm holder, card, merchant base, term amount, total terms.** Ask only when the user's instruction is ambiguous; otherwise infer.
2. **Confirm the target cycle.** Default is most-recently-closed; pass `bill_cycle` only when the user explicitly names a different one.
3. **Build the JSON spec.**
4. **Run the script.** Pipe JSON in, read the envelope back.
5. **Report back** with the created row's name, term amount, cycle, and any classification reason. Mention if there's already an in-progress plan with the same base (point at the per-term amounts so the user can see they're distinct).

## After writing

The plan is **registered**. From this point on, [[../populate-installment/SKILL.md|/populate-installment]] handles the remaining `02/NN` … `NN/NN` rows in subsequent cycles.

## What this skill does NOT do

- Does **not** add subsequent terms — use [[../populate-installment/SKILL.md|/populate-installment]].
- Does **not** edit existing transactions — use [[../update-transaction/SKILL.md|/update-transaction]].
- Does **not** create cards or promotions.
- Does **not** translate Thai labels.
