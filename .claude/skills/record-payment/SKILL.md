---
name: record-payment
description: Record a bill payment as a negative-amount transaction on Baiboon's or Nuta's Transactions DB — the row that offsets the card's running balance so a paid cycle nets to zero. Use when a payment was made (a transfer slip exists, or the user says "record the payment", "Nuta paid her UOB One bill") and the ledger needs the matching `ชำระบิลเต็มจำนวน`-style row. Tags it to the paid bill's cycle, dates it on the slip, and never earns cashback/points. Dedups against existing payment rows.
---

# record-payment

Writes **one** payment row — a negative `ยอดชำระ` transaction — to Baiboon's or Nuta's Transactions DB. In this household's model a payment is not just the Bills-row `จ่ายแล้ว` checkbox; it's a negative-amount transaction (e.g. `ชำระบิลเต็มจำนวน` — paid bill in full) that **offsets the card's running balance** so the cycle nets to zero. The two are independent and complementary:

- `จ่ายแล้ว` on the Bills row records *that the statement was settled* → [[../update-bill/SKILL.md|/update-bill]].
- The negative transaction this skill writes is *the money leaving* → balances the cycle.

Takumi has no Bills DB, so this skill rejects `takumi`.

This is a write skill — it overrides the project's "don't mutate Notion without explicit instruction" rule because the user invoked it (or [[../update-bill/SKILL.md|/update-bill]] delegated to it) explicitly. It is the payment counterpart to [[../add-transaction/SKILL.md|/add-transaction]] (charges) and shares its write core (`lib.transaction_write`).

## The model (why a negative transaction)

The card's outstanding balance is the running sum of all its transactions: charges (positive) minus payments and cashback credits (negative). When a statement is paid, a negative row equal to the bill brings that cycle's sum back to ~zero. Discovered conventions in the data:

- **Tagged to the paid bill's cycle** — same `Bill Cycle Date` / `Due Date` as that cycle's *charges* (not the cycle in which the money moved). A payment made 2026-05-06 against the April UOB One bill carries `Bill Cycle Date = 2026-04-24`.
- **`Transaction Datetime` = the slip date** — when the money actually moved.
- **No cashback** — `% cb` stays unset; a payment is not a purchase. (This is the single most important rule — see [[../../scripts/repositories/README|repositories]] / promotions never apply.)
- **No points** — multiplier left off.
- **Free-form Thai name** — most common: `ชำระบิลเต็มจำนวน` / `ชำระเต็มจำนวน` (full), `ชำระบางส่วน` (partial), `ชำระบิลล่วงหน้า` (advance).

## Primary execution path — the deterministic script

Backed by `scripts/python/record-payment/cli.py`, with the reusable core in `scripts/python/lib/payments.py`. Use it.

```sh
echo '<JSON-spec>' | uv run scripts/python/record-payment/cli.py
# add --dry-run to preview the payload + dedup verdict without writing
```

JSON spec:

```json
{
  "holder":       "baiboon | nuta",
  "card":         "UOB One",
  "bill_cycle":   "2026-05-25",

  "amount":       10693.09,
  "payment_date": "2026-05-29",
  "kind":         "full",
  "name":         "...",
  "note":         "...",
  "due_date":     "2026-06-14",
  "force":        false
}
```

- **`holder`, `card`, `bill_cycle`** are required. `card` resolves by exact title against the holder's Cards DS; `bill_cycle` is the `วันตัดรอบบิล` of the bill being paid.
- **`amount`** is the payment magnitude (positive); it is stored **negated**. **Omit it with `kind: "full"`** and the CLI reads the bill's `ยอดชำระ` and pays it in full — the common case.
- **`payment_date`** is the slip date (`Transaction Datetime`); defaults to today.
- **`kind`** ∈ `full` (default) / `partial` / `advance` — selects the default Thai label. Override with `name`.
- **`due_date`** is optional. Omitted → the skill reuses the `Due Date` already on the cycle's existing charges (so it matches, including UOB's weekend/holiday shift); if the cycle has no rows yet (a true advance payment), it derives the due date from the card's bank pattern (see [[../../docs/concepts/bill-cycle-patterns|bill-cycle-patterns]]).
- **`force`** creates the row even if a matching payment already exists (see dedup below).

Output envelope: `{would_create, created, holder, card, bill_cycle, amount, name, payment_date, due_date, existing_payments, id?, url?}`. When dedup fires, `created: false` + `reason`.

## Dedup — don't double-record

Before writing, the skill scans the cycle for existing **payment** rows (negative-amount rows that are not cashback credits and not `[…]`-bracketed bookkeeping rows). It skips creation (returns `created: false`) when:

- a single existing payment row matches `amount` (± ฿0.50, to absorb satang), **or**
- the existing payment rows already **sum** to `amount` (± ฿0.50) — covers a bill paid in two slips.

This makes re-runs safe and idempotent. Pass `force: true` only when you intentionally want a second payment row (e.g. a genuinely separate partial payment the sum-check would otherwise swallow).

## Amount semantics — full vs partial

- **Full payment (default):** record the bill's `ยอดชำระ` exactly. The cycle nets to **0**, even when the actual transfer was a few satang short — the shortfall is handled out-of-band (see *carry-forward* below), not by under-recording the payment. This is the household's chosen convention.
- **Partial payment:** pass `kind: "partial"` and the explicit `amount` actually paid. The cycle keeps the unpaid remainder as a positive residual.
- **Advance payment** (paying before the statement closes / before charges are entered): `kind: "advance"`, explicit `amount`. Due date falls back to the bank pattern when the cycle is empty.

### Satang shortfalls / carry-forward

When a transfer is a few satang under the bill (e.g. ฿10,693.00 vs ฿10,693.09), the convention is: record the **full** payment here (cycle → 0) **and** carry the residual to the next cycle as a `[ยอดยกมาจากรอบ YYYY-MM]` positive adjustment via [[../add-transaction/SKILL.md|/add-transaction]] (`×0`, **no `% cb`**). See the carry-forward convention in project memory. Don't reconcile by editing the bill or under-recording the payment — *reconcile, don't correct* ([[../../docs/concepts/reconcile-dont-correct|reconcile-dont-correct]]).

## What the user typically asks

- "Record that Nuta paid her UOB One bill" → `{holder:nuta, card:UOB One, bill_cycle:<cycle>}` (full, amount from bill).
- "Log Baiboon's ฿5,000 partial payment on First Choice this cycle" → `kind: "partial"`, `amount: 5000`.
- "Nuta paid ฿11,835 ahead on UOB One before the statement" → `kind: "advance"`, `amount: 11835`.

Most of the time you arrive here **via [[../update-bill/SKILL.md|/update-bill]]**: attaching a slip auto-delegates here for the full bill amount. Call this skill directly for partial/advance payments, or when there's no slip to attach.

## Hard rules

### 1. Holder routing (no Takumi)

| Holder   | Transactions data source ID                |
|----------|--------------------------------------------|
| baiboon  | `181cb755-f0f1-8167-b5b6-000bc6d47469`     |
| nuta     | `2a1cb755-f0f1-8110-9795-000bf7d48b4f`     |
| takumi   | *(no Bills DB — rejected)*                 |

### 2. Never any cashback or points

`% cb` is never written; no multiplier checkbox is set. A payment must not earn. The script enforces this — there is no spec field to add cashback to a payment row.

### 3. Tag to the paid bill's cycle, date on the slip

`Bill Cycle Date` / `Due Date` = the bill's cycle (so the offset lands against the right statement). `Transaction Datetime` = the slip date. Do not tag the payment to the cycle in which the money moved.

### 4. Dry-run when unsure

`--dry-run` shows the payload **and** the dedup verdict (`would_create`, `existing_payments`) without writing. Use it whenever the cycle might already hold a payment.

## What this skill does NOT do

- Does **not** patch the Bills row (`จ่ายแล้ว`, slip/statement files, Note). That's [[../update-bill/SKILL.md|/update-bill]] — which can *delegate here* on slip upload.
- Does **not** attach the slip file. The slip is bill evidence (Bills `หลักฐานการชำระ`); this skill records the ledger movement.
- Does **not** add charges or installment terms — see [[../add-transaction/SKILL.md|/add-transaction]] / [[../add-installment/SKILL.md|/add-installment]].
- Does **not** edit existing transactions — see [[../update-transaction/SKILL.md|/update-transaction]].
- Does **not** translate Thai labels — `ยอดชำระ`, `ชำระบิลเต็มจำนวน`, `Bill Cycle Date` stay verbatim per project convention.
