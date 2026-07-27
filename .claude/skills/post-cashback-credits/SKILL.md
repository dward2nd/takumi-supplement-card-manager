---
name: post-cashback-credits
description: Auto-create UOB One cashback credit rows for a cycle by summing per-tier `% cb` totals on existing transactions and writing one negative-amount transaction per tier (1% at the BC date, higher tiers at the first weekday of next month). Use when the user says "post the cashback for Baiboon's UOB One", "credit the cycle's cashback before drafting the bill", or before running [[../prepare-bill/SKILL.md|/prepare-bill]] on a UOB One cycle.
---

# post-cashback-credits

Writes the cashback credit rows for **one** cycle of **one** holder's card, materializing the active promotion's payout into negative-amount transactions so [[../prepare-bill/SKILL.md|/prepare-bill]] can then sum the cycle to a correct net balance.

Currently supports `UOB One` only — it implements the [[../../docs/promotions/uob-one-2026|UOB One 2026 promotion]]'s crediting workflow (1% at BC, higher tiers at first weekday of next month). Per-promotion credit conventions differ; to support another card's active promotion, extend `SUPPORTED_CARDS` and `_classify_tier_date` in `scripts/python/post-cashback-credits/cli.py` and reference the new promotion note.

## Primary execution path — the deterministic script

```sh
echo '<JSON-spec>' | uv run scripts/python/post-cashback-credits/cli.py
# add --dry-run to preview the plan without writing
# add --force to override the duplicate-CASHBACK guard
```

JSON spec:

```json
{
  "holder":     "baiboon | nuta",
  "card":       "UOB One",
  "bill_cycle": "2026-05-25",
  "skip_populate_installments": false,
  "force":      false
}
```

- `holder` and `card` are required. `card` must be in `SUPPORTED_CARDS` (today: `UOB One`).
- `bill_cycle` is optional; if omitted, the active cycle for the card is inferred from `lib.bill_cycle.active_cycle`.
- `skip_populate_installments` is optional, default `false`. Before summing, the CLI populates this cycle's in-progress installment terms (same idempotent `lib.installments.populate_for_cycle` that [[../populate-installment/SKILL.md|/populate-installment]] and [[../prepare-bill/SKILL.md|/prepare-bill]] use), so each term's per-row `% cb` is captured in the credit. Set `true` only when re-crediting a historical cycle whose installment rows shouldn't be touched.
- `force` is optional, default `false`. The CLI refuses to write if any `*CASHBACK*` row already exists in the cycle (prevents double-credit). To rewrite, archive the prior rows first via `scripts/python/add-transaction/archive.py`, then re-run with `force: true`.

## What the script does

1. Resolves `(holder, card, cycle BC + DD)`.
2. **Populates in-progress installment terms** into the cycle (unless `skip_populate_installments: true`) — idempotent, so terms already in the cycle are skipped. This must happen *before* summing: installment rows carry a per-term `% cb` (1% on UOB One), so crediting without them under-counts the installment cashback. The result is echoed under `installments` in the response.
3. Fetches every transaction in the cycle on that card.
4. Aborts if any row already has `CASHBACK` in its title — unless `force` is set.
5. Groups eligible rows (those with `% cb` set, excluding existing `CASHBACK` rows) by tier rate.
6. For each tier where the eligible sum is positive, writes one negative-amount transaction:
   - `Name`: `UOB ONE CASHBACK <N>%`
   - `ยอดชำระ`: `-round(rate × tier_sum, 2)`
   - `Transaction Datetime`: BC date if `rate == 1%`, otherwise first weekday of the next calendar month.
   - `Bill Cycle Date` / `Due Date`: cycle's BC / DD (explicit alignment exception).
   - Multiplier: `×0` (UOB One never earns points).
   - `Note`: `Cycle <BC> cashback credit: <N>% × <sum> = <credit>.`
7. Returns `{installments, tier_totals, created}` so the caller can verify the math.

## Hard rules

### 1. UOB One only (for now)

The date-by-tier convention (1% at BC, others at first weekday of next month) is the [[../../docs/promotions/uob-one-2026|UOB One 2026 promotion]]'s crediting workflow as confirmed by the user 2026-05-25. Other promotions and other cards' workflows differ; adding support is a deliberate extension (update `SUPPORTED_CARDS` + `_classify_tier_date` + reference the new promo note), not an automatic generalization.

When the UOB One promotion renews for 2027 with a different crediting cadence, branch the promo note and revisit the `_classify_tier_date` function.

### 2. Zero-tier rows are skipped

Tiers whose eligible sum is `≤ 0` (or whose computed credit rounds to `≤ 0`) get **no row written**. Don't create 0-baht placeholder rows.

### 3. Idempotency via the duplicate guard

If the cycle already has any `*CASHBACK*` row, the CLI aborts. Re-running is safe — it never double-writes silently. To regenerate, archive the prior rows first.

### 4. Workflow position

`/post-cashback-credits` → verify the credits look right → `/prepare-bill` → verify the bill total → upload statement PDF via `/update-bill` (with `finalize: true` to strip the `[DRAFT] ` prefix once the numbers match the bank).

**Order-independent w.r.t. installments.** Because this skill populates installment terms itself (step 2) before summing, the credit is complete whether you run it before or after `/prepare-bill`. This closes a former footgun: running `/post-cashback-credits` *before* `/prepare-bill` used to miss the installment 1% entirely, since `/prepare-bill` was the only thing populating the terms. If you edit the cycle's transactions after crediting (add/move/remove a row), re-credit: archive the `*CASHBACK*` rows, re-run this skill, then refresh the bill via `/update-bill` with `refresh_from_transactions: true`.

## What the user typically asks

- "Post the cashback for Nuta's UOB One" → spec with `holder: "nuta"`, `card: "UOB One"`; cycle inferred.
- "Credit Baiboon's UOB One cashback before drafting" → as above.
- "Re-do the cashback rows on this cycle, I missed one" → archive the existing rows, then re-run with `--force`.

## What this skill does NOT do

- Does **not** back-fill `% cb` on transactions that lack it. Use [[../update-transaction/SKILL.md|/update-transaction]] (with the merchant-tier classification done by you, per the policies in [[../add-transaction/SKILL.md|/add-transaction]]'s *Card-specific earning policies*).
- Does **not** draft the bill. Use [[../prepare-bill/SKILL.md|/prepare-bill]] after this.
- Does **not** delete or update existing credit rows. Use `add-transaction/archive.py` to remove, then re-run this skill.
- Does **not** apply to Takumi (UOB One is only on Baiboon and Nuta in the current data).
- Does **not** translate Thai labels — `ยอดชำระ`, `Bill Cycle Date`, etc. stay verbatim per project convention.
