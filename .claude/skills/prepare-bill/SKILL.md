---
name: prepare-bill
description: Draft a new row on Baiboon's or Nuta's Bills DB for the current unbilled cycle of a single card. Sums `ยอดชำระ` across every transaction whose `Bill Cycle Date` matches the cycle's BC date and writes it as a `[DRAFT] <Card> <YYYY-MM>` Bills row that stays draft until the user uploads the official statement (via /update-bill) or manually strips the prefix. Use when the user says "prepare the bill for Nuta's UOB One", "draft the May bill for Baiboon's UOB World", or otherwise wants a pre-statement balance written into Notion. Also has a date-range mode that drafts every cycle whose bill cycle date falls in a window, across cards and holders — use it for "prepare the bills for whatever cards closed 25–27 September".
---

# prepare-bill

Creates **one** new row on Baiboon's or Nuta's Bills DB representing the cycle that's currently accumulating. Takumi's Bills DB is statement-driven — his bill is the bank's per-card total, not a sum of his own rows — so this skill rejects `takumi` (see [[../../docs/databases/takumi-bills|takumi-bills]]).

This is a write skill — it overrides the project's "don't mutate Notion without explicit instruction" rule because the user invoked it explicitly. For patching an existing bill see [[../update-bill/SKILL.md|/update-bill]].

## Primary execution path — the deterministic script

Backed by `scripts/python/prepare-bill/cli.py`, a thin CLI over `lib.bill_draft.draft_bill` (where the drafting core lives so [[../update-bill/SKILL.md|/update-bill]] can reuse it — it drafts a missing bill when a payment slip needs somewhere to attach). Use it.

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
  "skip_cashback_check": false,
  "skip_populate_installments": false
}
```

- `holder` and `card` are required.
- `bill_cycle` is optional. Omit it and the CLI infers the **active cycle** from the card's bank pattern (see [[../../docs/concepts/bill-cycle-patterns|bill-cycle-patterns]]). Pass it explicitly only to back-fill a non-current cycle.
- `skip_cashback_check` is optional, default `false`. For cards listed in `CASHBACK_CREDIT_CARDS` (currently `UOB One`), the CLI refuses to draft if no `*CASHBACK*`-named transaction exists in the cycle — that pattern means the cashback credit rows haven't been written yet and the sum would overstate the balance. Set this to `true` only when you've verified the card doesn't need credit rows this cycle.
- `skip_populate_installments` is optional, default `false`. Before summing, the CLI calls [[../populate-installment/SKILL.md|/populate-installment]] internally for this (holder, card, bill_cycle), so the cycle's installment-term rows are present before the sum is taken. The call is idempotent — plans whose next term already lives in the cycle are skipped — and uses the same library function the standalone skill calls. Disable only when re-drafting a historical cycle whose installment rows shouldn't be touched.
- `skip_auto_note` is optional, default `false`. When the cycle contains special rows (cashback credits, installment terms, manual adjustments), the drafted bill's `Note` is set to a human-readable summary listing what's in the cycle. Pass `true` to leave Note blank — the user can then write their own via [[../update-bill/SKILL.md|/update-bill]] later.

## What the user typically asks

- "Prepare the bill for Nuta's UOB One" → `{holder: "nuta", card: "UOB One"}`.
- "Draft Baiboon's UOB World statement for May" → spec as above; CLI infers BC=2026-05-25 from today.
- "Make a draft bill for cycle 2026-04-25" → pass `bill_cycle` explicitly.

## Date-range mode — every cycle closing in a window

When the user asks for bills by date rather than by card — "prepare the bills for Nuta and Baiboon for whatever card with bill cycle dates within 25–27 September" — pass a window instead of `card` + `bill_cycle`:

```json
{
  "bill_cycle_from": "2026-09-25",
  "bill_cycle_to":   "2026-09-27",
  "holders": ["baiboon", "nuta"],
  "cards":   ["UOB One"]
}
```

- `bill_cycle_from` / `bill_cycle_to` — required, inclusive, at most **31 days** apart. The cap is deliberate: a wide window over history would mass-draft every old cycle that never got a Bills row.
- `holders` (or `holder`) — optional; defaults to both supplement holders.
- `cards` — optional filter, case-insensitive.
- `skip_populate_installments` / `skip_cashback_check` / `skip_auto_note` — passed through to every draft.

Cycles are **discovered from the Transactions DBs** (every distinct `(Card, Bill Cycle Date)` with a BC inside the window), not predicted from card patterns — a card with no rows in the window has nothing to bill. Each cycle is then drafted through the single-card path, so every guard above still applies *per cycle*; a guard that refuses becomes that cycle's status instead of aborting the rest.

The envelope has `counts` per status and one `results` entry per cycle:

| `status` | Meaning |
|----------|---------|
| `created` / `would-create` | Drafted (or would be, under `--dry-run`). Carries `title`, `ยอดชำระ`, `tx_count`, and `installments_appended` when relevant. |
| `exists` | A Bills row already has this `(Card, วันตัดรอบบิล)` — carries `bill_id`. Re-running a window is therefore idempotent. |
| `off-pattern` | The rows' BC isn't the card's bank-pattern BC for that month: misdated rows (run [[../audit-transaction-dates/SKILL.md\|/audit-transaction-dates]]), or a genuine bank-side shift the holiday library missed — draft that one in single mode with an explicit `bill_cycle`. |
| `blocked` | A guard refused; `reason` says which. The common one is **UOB One without cashback credits** — run [[../post-cashback-credits/SKILL.md\|/post-cashback-credits]] for that cycle, then re-run the window. |

Rows in the window with no `Card` relation are counted under `unassigned_rows` — they can't belong to any bill.

**Always `--dry-run` a window first** and show the user the plan: it touches several cards at once, and each `would-create` UOB One cycle needs its credits posted before the real run. A cycle whose BC is *today* is still open (same-day convention) — confirm the user has no more rows to add before drafting it.

## What the script does

1. Resolves `(holder, card)` to the right Bills DS + Cards page.
2. Resolves the card in the holder's **Cards DB** with `lib.cards.find_card` (exact title, then case-insensitive; no fuzzy matching). A typo aborts here with substring candidates. The bill links that Cards page.
3. Resolves the bill cycle date — from `bill_cycle` if given, otherwise via `lib.bill_cycle.active_cycle(card_name, today)`.
4. Checks the Bills DS for an existing row with that `(Card, วันตัดรอบบิล)` pair. If one exists (draft or final), **aborts** — never silently overwrites.
5. **Populates in-progress installments** into this cycle (unless `skip_populate_installments: true`) — same idempotent logic as the standalone [[../populate-installment/SKILL.md|/populate-installment]] skill. The result is echoed back under `installments` in the response so the user can see which plans were extended.
6. Queries the Transactions DS for every row whose `Bill Cycle Date` matches and whose `Card` relates to the resolved card.
7. Sums `ยอดชำระ` across those rows (a flat sum — see *Cashback handling* below).
8. Creates the Bills row with:
   - **Title**: `[DRAFT] <Card> <YYYY-MM>` (YYYY-MM derived from the BC date).
   - `Card`: relation to the card's page in the holder's Cards DB.
   - `วันตัดรอบบิล`: BC date.
   - `ยอดชำระ`: the computed sum, rounded to 2dp.
   - `จ่ายแล้ว`: unchecked.

## Installment handling

In-progress installments would otherwise silently shrink the bill total — a 10-month plan whose next term hasn't been written yet would miss its row in this cycle's sum. To prevent that, the CLI calls `lib.installments.populate_for_cycle` (the same function backing the standalone [[../populate-installment/SKILL.md|/populate-installment]] skill) before computing the total. Plans whose next term already sits in the target cycle are skipped — so re-running `/prepare-bill` on the same cycle doesn't double-write.

The response's `installments` block shows the per-plan disposition. When you surface the bill summary to the user, mention any plans the skill appended so they know to expect those rows on the bank statement.

## Auto-generated Note

When the cycle contains rows that aren't straightforward purchases — cashback credits, installment terms, manual adjustments — the bill's `Note` field is filled in automatically with a brief explanation listing those rows. The structure:

```
This cycle includes:
- N new installment plan(s): <name> (฿<amt>/term × <total>), ...
- N ongoing installment term(s): <name> ฿<amt>, ...
- N cashback credit(s): <name> ±฿<amt>, ...
- N manual adjustment(s): <name> ±฿<amt> — <note>, ...
```

Lines are omitted when their bucket is empty; if a bucket has many rows, only the first six are listed and the rest are folded into `(+N more)`. The detection is heuristic:

- **Cashback**: name contains `CASHBACK` (case-insensitive).
- **Installment**: name parses as `<base> NN/NN`.
- **Manual adjustment**: name starts with `[` (e.g. `[เว็บรับหนี้ไปบริหารต่อ]`), or `Credit Return` is checked, or the amount is negative and the row isn't already cashback / installment.
- Everything else is a regular purchase and doesn't appear in the Note.

Pass `skip_auto_note: true` to opt out. The `auto_note` field in the response shows whatever was written (or absent when no special rows existed).

## Payment rows are excluded from the total

`ยอดชำระ` is the cycle's **amount due**, not its remaining balance — so the sum skips bill-payment rows, identified by `lib.payments.is_bill_payment_row` (a negative-amount row whose name starts with the Thai payment verb `ชำระ…` or `จ่าย…`: `ชำระบิลเต็มจำนวน`, `ชำระบิลล่วงหน้า`, `ชำระบางส่วน`, `จ่ายเต็มจำนวน`, …).

Without this the total would silently net its own payment and become **order-dependent**: the same cycle reads ฿388.10 if drafted before the payment was recorded and ฿152.00 if drafted after. Historical bills drafted under the old flat-sum behaviour therefore disagree with what a refresh computes today — that's expected drift, not an error to chase. Per [[../../docs/concepts/reconcile-dont-correct|reconcile, don't correct]], don't mass-refresh settled bills to "fix" them.

Everything that genuinely changes what is owed still counts: cashback credits (`UOB ONE CASHBACK 5%`, `Cashback …`, `CB …`), merchant refunds (a negative `WWW.GRAB.COM …` row), `[ยกเลิก]` cancellations, `[เว็บรับหนี้…]` takeovers and `[ยอดยกมา…]` carry-forwards. Note the deliberately *looser* `is_payment_row` in the same module is for `record_payment`'s dedup only — it matches refunds and `CB`-prefixed credits too, and must not be reused here.

The same rule is mirrored in `/update-bill`'s `refresh_from_transactions`.

## Cashback handling

The bill total is "balance including cashback". The skill itself does **no** cashback arithmetic — that's deliberate. Cashback offsets must already be encoded in the cycle's transactions as **negative-amount rows** (e.g. `UOB ONE CASHBACK 5%` with `ยอดชำระ = -22.77`). A flat sum then yields the net amount due.

For cards in the `CASHBACK_CREDIT_CARDS` set (currently `UOB One`, whose active promotion is [[../../docs/promotions/uob-one-2026|UOB One 2026]]), running this skill before the credit rows exist is a footgun — the bill would overstate the balance. The CLI guards against this: it scans the cycle's transactions for any title containing `CASHBACK` (case-insensitive) and refuses to draft if none is present. Run [[../post-cashback-credits/SKILL.md|/post-cashback-credits]] first to write the tier-split credit rows, then come back here.

For cards without an active cashback promotion at the cycle's date (e.g. UOB World, KTC, First Choice between promos), no preparation is needed — there are no cashback rows to sum and the bill total is the raw `ยอดชำระ` total of the cycle's transactions. The safety check does not apply.

For First Choice **during** an active promotion: the user currently manages those cashback adjustments manually (no per-promo credit-row workflow is documented yet). Until First Choice promos get their own promo notes + credit-row convention, `/prepare-bill` won't trigger the safety check for First Choice — confirm with the user that promo cashback has been applied per-row before drafting.

## Hard rules

### 1. Holder routing

| Holder   | Bills DS                                   |
|----------|--------------------------------------------|
| baiboon  | `192cb755-f0f1-8064-9075-000be05ba72d`     |
| nuta     | `2a1cb755-f0f1-8193-982d-000bd4e3156c`     |
| takumi   | *(statement-driven — rejected)*            |

### 2. `Card` is a relation, on Bills and on Transactions

Since 2026-09-30 a bill's `Card` is a one-way relation to the card's page in the holder's own Cards DB, the same page the cycle's transactions point at. The CLI resolves the spec's `card` once, with `lib.cards.find_card`: exact title first, then case-insensitive, refusing ambiguity. A typo aborts there with substring candidates. That one page ID then drives everything:

- the duplicate check (`existing_bill`: Bills `Card` relation *contains* the page, plus `วันตัดรอบบิล`),
- the Transactions query (`Card.relation.contains`),
- and the new row's `Card` relation.

The draft's title uses the Cards page title: `[DRAFT] <Card> <YYYY-MM>`.

There are no SELECT options to mint any more, so the old `new_select_option` envelope flag is gone. A card that has never been billed just gets its first bill, as long as it exists in the holder's Cards DB. (Before the relation, a first bill had to add a SELECT option; first hit 2026-09-27 on Baiboon's `KBank JCB`.)

The former SELECT survives as **`Card (old select)`**, kept only so the household's Notion views keep working until they move to the relation. The CLI neither reads nor writes it. See [[../../docs/concepts/known-divergences|known-divergences]] #1.

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
