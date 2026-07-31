---
name: update-bill
description: Patch a row on Baiboon's or Nuta's Bills DB — set `จ่ายแล้ว`, attach a payment slip to `หลักฐานการชำระ`, attach a statement PDF to `ใบแจ้งยอด (PDF)`, write a `Note`, or use a raw-properties escape hatch. Use when the user says "mark this bill paid", "attach the slip to <holder>'s bill", "save the statement PDF", or otherwise wants to mutate a Bills row. The write counterpart for bills (transactions live separately — see [[../update-transaction/SKILL.md|/update-transaction]]).
---

# update-bill

Patches property values on **one** row in Baiboon's or Nuta's Bills DB (`บิลเรียกเก็บค่าบัตรเครดิต`). Takumi has no Bills DB, so this skill rejects `takumi`.

This is a write skill — it overrides the project's "don't mutate Notion without explicit instruction" rule because the user invoked it explicitly. For reads on bills, query Notion directly via MCP for now (no dedicated read skill exists yet). For transaction patches see [[../update-transaction/SKILL.md|/update-transaction]]; for new transactions see [[../add-transaction/SKILL.md|/add-transaction]].

## Primary execution path — the deterministic script

Backed by `scripts/python/update-bill/cli.py`. Use it.

```sh
echo '<JSON-spec>' | uv run scripts/python/update-bill/cli.py
# add --dry-run to preview without writing
```

JSON spec:

```json
{
  "holder":        "baiboon | nuta",
  "card":          "First Choice",
  "bill_cycle":    "2026-06-05",
  "id":            "<bill-page-uuid>",

  "paid":          true,
  "note":          "...",
  "slip":          "/abs/path.jpg",
  "slips":         ["/abs/a.jpg", "/abs/b.jpg"],
  "statement_pdf": "/abs/path.pdf",
  "statement_pdfs":["/abs/a.pdf", "/abs/b.pdf"],
  "record_payment": true,
  "payment_date":   "2026-05-29",
  "finalize":      true,
  "auto_close_on_statement": true,
  "properties":    { "<raw notion prop>": ... }
}
```

`record_payment` (default `true`) — when a slip is attached, delegate to [[../record-payment/SKILL.md|/record-payment]] to record the matching negative-amount payment row (the **full** bill `ยอดชำระ`) in the Transactions DB, so the cycle nets to zero. Idempotent: [[../record-payment/SKILL.md|/record-payment]] dedups against existing payment rows, so re-attaching a slip won't double-record. `payment_date` (default today) sets that row's `Transaction Datetime` — pass the slip's date. Set `record_payment: false` to attach the slip without touching the ledger. **Partial / advance payments are not covered by this delegation** (it always records the full bill amount) — call [[../record-payment/SKILL.md|/record-payment]] directly with `kind: "partial"` / `"advance"`. See *Slip upload records the payment* below.

`finalize: true` strips a leading `[DRAFT] ` from the bill's title — pairs with /prepare-bill which writes the draft prefix. Idempotent: if the prefix is already gone the action is a no-op (still surfaced in the response so you can see it was checked).

`auto_close_on_statement` (default `true`) — attaching a statement PDF (`statement_pdf` / `statement_pdfs`) *closes* the bill: the CLI auto-finalizes (strips `[DRAFT] `) and, **only when payment is proven**, sets `จ่ายแล้ว: true`. See [[#when-a-bill-gets-marked-จ่ายแล้ว-true|When a bill gets marked จ่ายแล้ว]] for the evidence gate. An explicit `finalize` / `paid` in the spec overrides the auto behaviour; set `auto_close_on_statement: false` to disable it entirely (e.g. saving a statement on a cycle that isn't settled yet without touching the title). Needs the bill resolvable by `(holder, card, bill_cycle)` — the `id`-only form skips it. The `auto_paid` block in the response reports `amount_due`, `recorded_payments`, and the `settled` decision.

`refresh_from_transactions: true` re-derives the bill's `ยอดชำระ` from the cycle's transactions — **excluding bill-payment rows**, since `ยอดชำระ` is the amount *due*, not the balance remaining. Payment rows are matched by `lib.payments.is_bill_payment_row` (negative amount + a name opening with `ชำระ…` / `จ่าย…`); cashback credits, refunds and `[…]`-prefixed adjustments all still count. See [[../prepare-bill/SKILL.md#payment-rows-are-excluded-from-the-total|/prepare-bill → Payment rows are excluded]] for why (the total would otherwise be order-dependent), and note that bills drafted before this rule existed will compute differently on refresh — don't mass-refresh settled bills to reconcile them. It also (unless the spec also passes an explicit `note`) regenerates the explanation Note via the same `lib.bills.explain_cycle` function [[../prepare-bill/SKILL.md|/prepare-bill]] uses on draft. Use this after appending installment terms or cashback credits to a cycle whose bill was already drafted — without it, the bill row's amount would silently drift from the underlying transactions. Requires the bill to be resolvable by `(holder, card, bill_cycle)`; the `id`-only form needs those echo fields supplied alongside.

**Identify the bill row** either by `(holder, card, bill_cycle)` *or* by `id`. If `id` is set, the lookup keys are optional (used only for the response echo). Otherwise all three lookup keys are required and must match a unique row.

**At least one update field is required** (`paid`, `note`, `slip`/`slips`, `statement_pdf`/`statement_pdfs`, `finalize`, or `properties`). The script errors out on an empty update so a typo doesn't silently no-op.

### Response includes `in_progress_installments`

When the bill was resolved by `(holder, card, bill_cycle)` (or by `id` with the echo fields supplied), the script also computes the set of in-progress installment plans on the bill's card and returns them under `in_progress_installments`:

```json
{
  "id": "...",
  "fields": ["จ่ายแล้ว"],
  "in_progress_installments": [
    { "base": "2C2P *SHOPEE", "total_terms": 10, "max_term": 3, "remaining_terms": 7, "per_term_amount": 1079.20 },
    { "base": "COM7-ID175-BN-CT-CHO", "total_terms": 10, "max_term": 5, "remaining_terms": 5, "per_term_amount": 959.00 }
  ]
}
```

Surface this to the user when marking a bill paid — it shows what installment commitments will appear on the next several statements. Read-only side effect: no plan rows are added by this skill. To advance the cycle, use [[../populate-installment/SKILL.md|/populate-installment]] (or let [[../prepare-bill/SKILL.md|/prepare-bill]] handle it on the next bill).

### When a bill gets marked `จ่ายแล้ว: true`

**What `จ่ายแล้ว` means.** It records that the **peer has transferred their share to Takumi** — *not* that the bank has been paid. The normal flow is: the peer (Baiboon / Nuta) transfers the money to Takumi first (that transfer's **slip** lands in `หลักฐานการชำระ`), and Takumi settles with the bank himself, **later**. So the **transfer slip is the payment evidence**; the bank statement is not, and neither is a bank-payment line printed on it.

**Automatic path — `auto_close_on_statement` (default on).** When a call attaches a statement PDF, the CLI *closes* the bill:

1. **Always finalizes** — strips a leading `[DRAFT] `.
2. **Marks `จ่ายแล้ว: true` only when the transfer is proven:** a transfer slip is present in `หลักฐานการชำระ` (already on file, or attached in the same call) **and** the cycle's recorded `ชำระ…`/`จ่าย…` payment rows cover `ยอดชำระ` (within ฿0.5). When there's no slip yet, or the recorded transfer falls short, it finalizes but **leaves `จ่ายแล้ว` alone** and reports `auto_paid.settled: false` with the reason. The `auto_paid` block returns `amount_due`, `recorded_payments`, `slip_on_file`, and `settled`.

The CLI can't OCR a slip image, so it uses the slip-derived payment row (the `record_payment` companion writes one when a slip is attached) as the amount check. When you attach a **new** transfer slip, still parse its amount yourself to confirm it matches before trusting the auto-mark — that's the manual criterion below, unchanged.

**Explicit paths — always win over the automatic one:**

1. **Verified transfer slip.** `หลักฐานการชำระ` has slip(s) whose amounts (parsed from each slip's content) **sum to the bill's `ยอดชำระ` exactly** — not "close enough", not "one slip, ignore the rest". Then pass `paid: true`. On a mismatch, surface the delta and leave `จ่ายแล้ว` alone. This is a check, not a correction — per *Reconcile against the statement PDF* below, don't adjust `ยอดชำระ` or any slip amount to make them line up.
2. **Explicit user instruction.** The user says "mark it paid" or passes `paid: true`. This is also how the user declares the **exception** to the peer-transfers-first model: when a peer **paid the bank directly themselves**, there's no transfer slip to Takumi, so the user marks it paid explicitly. The CLI never infers this case on its own.

**Adjacent corner cases:**

- *Transfer slip present, but no statement yet.* The automatic path is statement-triggered, so it won't fire — but you may still mark paid via the explicit verified-slip path once the slip amount matches. The bill stays `[DRAFT]` until a statement finalizes it.
- *Statement uploaded, no transfer slip yet.* Auto-finalizes, leaves `จ่ายแล้ว` unpaid (`settled: false`, reason "no transfer slip"). Correct — the peer hasn't settled with Takumi.
- *A bank-payment line on the statement (or a `ชำระ…` ledger row) but no slip file.* Does **not** by itself mark paid — that reflects Takumi paying the bank, not the peer transferring. The transfer-slip file is the contract.
- *Multiple slips totalling the bill amount.* Allowed — sum them.

### Reconcile against the statement PDF — *report-only, never auto-correct*

When the user uploads a statement PDF and asks to finalize one or more bills, **the agent's job includes comparing the statement against Notion** and surfacing any mismatches it can spot. The user maintains Notion's `ยอดชำระ` as the *internal* calculated balance — drift from the bank statement is expected (cashback-credit timing, debt-takeover offsets, hand-entered adjustment rows) and is preserved on purpose. So:

1. **Never call `refresh_from_transactions: true` to "make the balance match" the statement.** The bank's number is for verification; the Notion number is the system of record for the household's accounting.
2. **Do not edit individual transaction rows** to reconcile them against the statement unless the user explicitly asks. Even for clear data-entry mistakes (an off-by-one on an installment term, a baht-and-satang typo), report first.
3. **Do** call out, in the response back to the user:
   - **Total discrepancy** per bill: statement subtotal vs Notion `ยอดชำระ`. Sign and magnitude.
   - **Row-level diffs** when identifiable: missing rows in Notion (statement has a charge that Notion doesn't), extra rows in Notion (typically `[บัตรหลัก]`-style debt-takeover offsets or hand-entered adjustments), amount mismatches (small or large), date mismatches that change which cycle a row falls into.
   - **Installment-term drift**: when the statement's `NN/NN` differs from Notion's labelling, this usually indicates an off-by-one in a prior cycle. Note which plan and which row is suspect — a single mislabelled row can cascade into every future cycle via [[../populate-installment/SKILL.md|/populate-installment]]. Pair the comment with the suggested fix path (e.g. "if you fix this row in cycle 2026-04-24 to 03/10, next populate run will be correct").
   - **Convention-difference notes**, written shortly: the bank credits cashback on the *next* statement; the user's Notion writes it inside the *closing* cycle. Cite once if relevant, don't repeat per row.
4. **Multi-cardholder PDFs**: a single UOB statement bundles Takumi's primary card alongside Baiboon's and Nuta's supplements. Each sub-card has its own subtotal — use the right one when comparing against each holder's Notion bill. Per-row attribution: rows on the primary's sub-card stay with Takumi; rows on the supplement's sub-card belong to that supplement, even if the user's Notion has tagged them with `[บัตรหลัก]` to internally offset back to the primary.

Phrasing: lead the report with the per-bill totals table (Notion vs statement vs Δ), then a per-bill bullet list of misalignments grouped by cause. Keep convention-difference notes terse — the user already knows about them.

## What the user typically asks

- "Attach this slip to Baiboon's First Choice bill" → resolve to the active cycle, `slip: "<path>"`.
- "Mark Nuta's UOB One bill paid for cycle 2026-04-25" → `paid: true`, `bill_cycle: "2026-04-25"`.
- "Save the statement PDF on Baiboon's KTC UnionPay bill" → `statement_pdf: "<path>"`.
- "Add this note to the current bill: …" → `note: "..."`.

## Hard rules

### 1. Holder routing

| Holder   | Bills data source ID                       |
|----------|--------------------------------------------|
| baiboon  | `192cb755-f0f1-8064-9075-000be05ba72d`     |
| nuta     | `2a1cb755-f0f1-8193-982d-000bd4e3156c`     |
| takumi   | *(no Bills DB — rejected)*                 |

### 2. The `Card` field is a SELECT, not a relation

A bill's `Card` is a SELECT option keyed off the verbatim card name (see [[../../docs/databases/baiboon-bills]] for the option list). The script's `find_bill` matches `Card.select.equals` exactly — no substring, no inferring "First Choice" from "FC". If the spelling drifts, the lookup fails.

### 3. File appends preserve existing entries

Notion's `pages.update` on a files property is *replace* semantics — the new list overwrites the old. The script handles this for you: for each existing file in `หลักฐานการชำระ` or `ใบแจ้งยอด (PDF)`, it re-uploads from the live signed URL and re-attaches by `file_upload` ID. So you can append safely without losing what's already there.

The user routinely attaches multiple files per bill (multiple transfer slips, partial-payment evidence). Don't ask whether to replace vs. append — always append.

### Slip upload records the payment (delegates to /record-payment)

Attaching a slip is evidence that the bill was paid. So unless `record_payment: false`, the script delegates to `lib.payments.record_payment` (the core behind [[../record-payment/SKILL.md|/record-payment]]) to write the matching **negative-amount payment transaction** for the **full** bill `ยอดชำระ`, tagged to the bill's cycle, dated on `payment_date` (default today). This is what makes the cycle net to zero — the slip file is evidence on the Bills row; the negative transaction is the ledger movement. The result rides back in the envelope under `payment`.

It is **idempotent**: `record_payment` dedups against existing payment rows in the cycle (single-row match or sum-of-rows match within ฿0.50), so re-attaching a slip won't double-record — `payment.created` comes back `false` with a `reason`. It only fires when the bill resolves by `(holder, card, bill_cycle)` and at least one slip is being attached; the `id`-only form skips it.

This is the **only** transaction this skill writes, and it does so by delegating — the boundary with [[../add-transaction/SKILL.md|/add-transaction]] (charges) and [[../record-payment/SKILL.md|/record-payment]] (the payment core) stays intact. **Partial / advance payments are out of scope here** (the delegation always pays the full bill); use [[../record-payment/SKILL.md|/record-payment]] directly with `kind: "partial"` / `"advance"`.

### 4. Date alignment

`bill_cycle` is the value of `วันตัดรอบบิล` on the Bills row. It corresponds to the same date the Transactions DB uses as `Bill Cycle Date` for that cycle — see [[../../docs/concepts/bill-cycle-patterns]] for per-issuer rules. If the user gives you a transaction-side BC date and a card name, the matching bill row uses the *same* date.

### 5. Dry-run for risky writes

Pass `--dry-run` to the CLI when a mistake would be hard to undo (e.g. writing a `Note` over an existing one — the script *replaces* the rich-text content). Files appends are safe to retry idempotently because uploads are content-addressed inside Notion.

## Procedure

1. **Resolve the bill row.** Prefer `(holder, card, bill_cycle)`; fall back to `id` only when the user gave you one directly.
2. **Build the spec.** Only include the fields the user asked to update. Files take absolute paths.
3. **Run the script.** Pipe JSON in, read the envelope back.
4. **Report.** Lead with the bill (card + cycle), then list the fields that were touched. If `slip`/`slips`/`statement_pdf`/`statement_pdfs` were involved, mention that existing files were preserved.

## What this skill does NOT do

- Does **not** create new Bills rows. The Bills DB has its own creation flow per cycle; this skill only patches.
- Does **not** add *charge* transactions. Use [[../add-transaction/SKILL.md|/add-transaction]]. (It does record one *payment* transaction on slip upload, by delegating to [[../record-payment/SKILL.md|/record-payment]] — see *Slip upload records the payment*.)
- Does **not** edit transactions. Use [[../update-transaction/SKILL.md|/update-transaction]].
- Does **not** mutate Takumi's data (Takumi has no Bills DB).
- Does **not** translate Thai labels — `จ่ายแล้ว`, `หลักฐานการชำระ`, `ใบแจ้งยอด (PDF)`, `วันตัดรอบบิล` stay verbatim per project convention.
