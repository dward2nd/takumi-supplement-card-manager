---
name: prepare-bill
description: Draft a new row on Baiboon's or Nuta's Bills DB for the current unbilled cycle of a single card. Sums `ยอดชำระ` across every transaction whose `Bill Cycle Date` matches the cycle's BC date and writes it as a `[DRAFT] <Card> <YYYY-MM>` Bills row that stays draft until the user uploads the official statement (via /update-bill) or manually strips the prefix. Use when the user says "prepare the bill for Nuta's UOB One", "draft the May bill for Baiboon's UOB World", or otherwise wants a pre-statement balance written into Notion.
---

# prepare-bill

Creates **one** new row on Baiboon's or Nuta's Bills DB representing the cycle that's currently accumulating. Takumi has no Bills DB, so this skill rejects `takumi`.

This is a write skill — it overrides the project's "don't mutate Notion without explicit instruction" rule because the user invoked it explicitly. For patching an existing bill see [[../update-bill/SKILL.md|/update-bill]].

## Primary execution path — the deterministic script

Backed by `scripts/python/prepare-bill/cli.py`. Use it.

```sh
echo '<JSON-spec>' | uv run scripts/python/prepare-bill/cli.py
# add --dry-run to resolve cycle + total without writing
```

JSON spec:

```json
{
  "holder":              "baiboon | nuta",
  "card":                "UOB One",
  "bill_cycle":          "2026-05-25",
  "skip_cashback_check": false
}
```

- `holder` and `card` are required.
- `bill_cycle` is optional. Omit it and the CLI infers the **active cycle** from the card's bank pattern (see [[../../docs/concepts/bill-cycle-patterns|bill-cycle-patterns]]). Pass it explicitly only to back-fill a non-current cycle.
- `skip_cashback_check` is optional, default `false`. For cards listed in `CASHBACK_CREDIT_CARDS` (currently `UOB One`), the CLI refuses to draft if no `*CASHBACK*`-named transaction exists in the cycle — that pattern means the cashback credit rows haven't been written yet and the sum would overstate the balance. Set this to `true` only when you've verified the card doesn't need credit rows this cycle.

## What the user typically asks

- "Prepare the bill for Nuta's UOB One" → `{holder: "nuta", card: "UOB One"}`.
- "Draft Baiboon's UOB World statement for May" → spec as above; CLI infers BC=2026-05-25 from today.
- "Make a draft bill for cycle 2026-04-25" → pass `bill_cycle` explicitly.

## What the script does

1. Resolves `(holder, card)` to the right Bills DS + Cards page.
2. Verifies the card name is a valid SELECT option on the Bills DS's `Card` field (no fuzzy matching).
3. Resolves the bill cycle date — from `bill_cycle` if given, otherwise via `lib.bill_cycle.active_cycle(card_name, today)`.
4. Checks the Bills DS for an existing row with that `(Card, วันตัดรอบบิล)` pair. If one exists (draft or final), **aborts** — never silently overwrites.
5. Queries the Transactions DS for every row whose `Bill Cycle Date` matches and whose `Card` relates to the resolved card.
6. Sums `ยอดชำระ` across those rows (a flat sum — see *Cashback handling* below).
7. Creates the Bills row with:
   - **Title**: `[DRAFT] <Card> <YYYY-MM>` (YYYY-MM derived from the BC date).
   - `Card`: SELECT, the verbatim card name.
   - `วันตัดรอบบิล`: BC date.
   - `ยอดชำระ`: the computed sum, rounded to 2dp.
   - `จ่ายแล้ว`: unchecked.

## Cashback handling

The bill total is "balance including cashback". The skill itself does **no** cashback arithmetic — that's deliberate. Cashback offsets must already be encoded in the cycle's transactions as **negative-amount rows** (e.g. `UOB ONE CASHBACK 5%` with `ยอดชำระ = -22.77`). A flat sum then yields the net amount due.

For cards in the `CASHBACK_CREDIT_CARDS` set (currently `UOB One`), running this skill before the credit rows exist is a footgun — the bill would overstate the balance. The CLI guards against this: it scans the cycle's transactions for any title containing `CASHBACK` (case-insensitive) and refuses to draft if none is present. Run [[../post-cashback-credits/SKILL.md|/post-cashback-credits]] first to write the tier-split credit rows, then come back here.

For cards that don't pay cashback (e.g. UOB World, KTC, First Choice without an active promo, etc.), no preparation is needed — there are no cashback rows to sum and the bill total is the raw `ยอดชำระ` total of the cycle's transactions. The safety check does not apply.

## Hard rules

### 1. Holder routing

| Holder   | Bills DS                                   |
|----------|--------------------------------------------|
| baiboon  | `192cb755-f0f1-8064-9075-000be05ba72d`     |
| nuta     | `2a1cb755-f0f1-8193-982d-000bd4e3156c`     |
| takumi   | *(no Bills DB — rejected)*                 |

### 2. Card SELECT vs Card relation

A bill's `Card` is a SELECT keyed off the card's verbatim title (see [[../../docs/concepts/known-divergences|known-divergences]]). The CLI validates the spec's `card` against the live SELECT option list — a typo aborts with a list of valid options.

The Transactions DS uses a `Card` **relation** to the Cards DB. The CLI resolves the card name to its Cards page ID via the existing `lib.cards.find_card` (exact title equality), then filters Transactions by `Card.relation.contains`.

### 3. No duplicate bills

A `(Card, วันตัดรอบบิล)` pair uniquely identifies a Bills row. The CLI refuses to create a second row for an existing pair — re-running is idempotent (it errors with the existing page ID, doesn't double-write).

If you actually want to regenerate the draft, archive the existing row first or use `/update-bill` to patch its `ยอดชำระ` in place.

### 4. Date alignment

The BC date used here is the same value Transactions rows carry in `Bill Cycle Date`. Per-issuer patterns live in [[../../docs/concepts/bill-cycle-patterns|bill-cycle-patterns]]. For UOB the BC may shift earlier (weekend/Thai-holiday rule), which `active_cycle` already encodes.

### 5. The `[DRAFT] ` prefix is meaningful

It signals "this number came from our own running total, not the bank statement". The user removes the prefix manually (or implicitly by uploading a statement PDF through /update-bill, if that flow ever automates the strip) once the official cut-off arrives and the numbers reconcile.

Until then, anything that consumes Bills data should treat `[DRAFT] ` rows as **estimates**, not commitments.

## Procedure

1. Confirm holder + card from the user's wording. For UOB One specifically: verify the cashback credit rows are already written for this cycle (1% / 5% / 10% as applicable). If they're missing, write them via /add-transaction first.
2. Build the JSON spec. Omit `bill_cycle` unless the user named a specific past cycle.
3. Run the script. Read the envelope back.
4. **Report** the new bill's title, `ยอดชำระ`, and tx count back to the user. Mention the draft prefix explicitly so the user knows the row is provisional.

## What this skill does NOT do

- Does **not** finalize a bill. The `[DRAFT] ` prefix stays until the user strips it (manually or via the statement-upload flow).
- Does **not** write transactions. For cashback credit rows, use [[../add-transaction/SKILL.md|/add-transaction]] first.
- Does **not** edit an existing bill row. Use [[../update-bill/SKILL.md|/update-bill]] for patches (paid flag, slips, statement PDFs, notes).
- Does **not** mutate Takumi's data (Takumi has no Bills DB).
- Does **not** translate Thai labels — `ยอดชำระ`, `วันตัดรอบบิล`, `จ่ายแล้ว` stay verbatim per project convention.
