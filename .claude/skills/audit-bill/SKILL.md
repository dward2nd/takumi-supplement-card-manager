---
name: audit-bill
description: Diff a bank statement against Notion's Transactions DB for one (holder, card, bill cycle). Surfaces statement rows missing from Notion (un-recorded charges), Notion rows missing from the statement (often cancelled charges still sitting in Notion, or local-only cashback / offset rows), and the subtotal delta. Read-only — never mutates. Use when the user uploads a statement PDF and asks "what's missing?", "what's different?", "audit Nuta's UOB One bill", or "is there anything cancelled I didn't notice?".
---

# audit-bill

Compares the transactions printed on a bank statement against the Notion rows for the same `(holder, card, bill cycle)` and reports drift. Most useful when a charge was cancelled by the bank without being mirrored in Notion — that row stays in the cycle's Notion total but no longer appears on the statement.

This skill is **read-only**. It does not delete, edit, or create anything. Once findings are reviewed, the user can hand specific row IDs to [[../update-transaction/SKILL.md|/update-transaction]] (to amend or tag) or [[../add-transaction/SKILL.md|/add-transaction]] (to add a missing row). Per [[../../docs/concepts/reconcile-dont-correct|reconcile, don't correct]], **never** auto-edit Notion to make its total match the bank — the household's calculated balance is the system of record.

## Primary execution path — two deterministic scripts

The skill is two CLIs working together. **Step 1** extracts the statement PDF to plain text (handles password-encrypted PDFs); **Step 2** diffs your transcribed rows against Notion.

```sh
# Step 1 — extract the PDF to text (do not screenshot the PDF page by page,
# that burns tokens). Add --password "..." if the bank encrypted it.
uv run scripts/python/audit-bill/extract.py --pdf /abs/path/statement.pdf [--password XXXX] [--pages 4-7]

# Step 2 — diff the cycle. Read the text from step 1, pick out only the
# requested holder's sub-section, build the JSON below.
echo '<JSON-spec>' | uv run scripts/python/audit-bill/cli.py
```

The Notion query in step 2 is built off the same `Bill Cycle Date` filter [[../prepare-bill/SKILL.md|/prepare-bill]] uses, so what you audit here is exactly what got summed into the bill.

JSON spec:

```json
{
  "holder":              "takumi | baiboon | nuta",
  "card":                "UOB One",
  "bill_cycle":          "2026-04-24",
  "statement_subtotal":  17936.84,
  "statement_transactions": [
    {"date": "2026-03-25", "name": "(FOR SHOPEE)*(FOR SHOP BANGKOK", "amount": 182.00},
    {"date": "2026-03-25", "name": "(FOR SHOPEE)*(FOR SHOP BANGKOK", "amount": -182.00},
    {"date": "2026-03-25", "name": "TMN 7-11 BANGKOK",               "amount": 132.00}
  ]
}
```

- `holder` and `card` are required. `card` is resolved by exact title against the holder's Cards DS (same rule as the other skills).
- `bill_cycle` is optional. Omitted → infer the **most recently closed** cycle on this card via `lib.bill_cycle.most_recent_closed_cycle` (since statements arrive *after* the cycle closes). For UOB the BC stored in Notion is the *shifted* date (e.g. 2026-04-24 because 2026-04-25 was a Saturday) — feed the same value here.
- `statement_subtotal` is optional. When given, it's used as the bank's printed sub-total; when omitted, the CLI uses the sum of `statement_transactions` instead. Pass it explicitly when the PDF prints it — keeps the `subtotal_diff` honest if the agent missed a row when transcribing.
- `statement_transactions` is the list extracted from the statement. **Pre-parse the PDF before calling.** Caller is responsible for converting `CR` / refund rows to negative amounts, skipping non-charge rows (PREVIOUS BALANCE, SUB TOTAL, TOTAL BALANCE, payment-thank-you rows that aren't on the holder's section, the issuer's `*CASHBACK*` credits that they post to the *primary* card rather than the supplement), and converting foreign-currency rows to the THB amount the bank prints.

## Output envelope

```json
{
  "holder": "nuta",
  "card": "UOB One",
  "bill_cycle": "2026-04-24",

  "statement": { "count": 71, "subtotal": 17936.84, "subtotal_source": "given", "rows_sum": 17936.84 },
  "notion":    { "count": 73, "subtotal": 17434.72 },
  "subtotal_diff": -502.12,

  "matched_count":      69,
  "name_mismatch_count": 1,

  "missing_in_notion": [ {"date": "...", "name": "...", "amount": 132.0} ],
  "extra_in_notion":   [ {"id": "...", "url": "...", "name": "UOB ONE CASHBACK 5%", "amount": -357.25, "transaction_date": "...", "note": "..."} ],
  "name_mismatches":   [ {"statement": {...}, "notion": {...}} ]
}
```

- `subtotal_diff = notion.subtotal − statement.subtotal`. Sign matters: **negative** means Notion is smaller than the bank (typical when Notion's cashback credit rows are inside the cycle but the bank credits them to the primary instead). **Positive** means Notion is larger than the bank (e.g. a cancelled charge still living in Notion, or a manual `[เว็บรับหนี้ไปบริหารต่อ]` offset that nets in the user's favour).
- `extra_in_notion` is the bucket where cancelled charges show up. It also legitimately contains the household's bookkeeping rows: `*CASHBACK*` credits, `[เว็บรับหนี้ไปบริหารต่อ]` debt-takeover offsets, manual `[…]`-prefixed adjustments. Read each row's `name` / `note` before flagging anything to the user.
- `missing_in_notion` is the bucket for "the bank charged me but Notion doesn't know". Usually a row the user forgot to add — re-confirm with the user, then `/add-transaction`.
- `name_mismatches` is matched-by-amount but the merchant tokens diverged — could be a legitimate match (different formatting for the same merchant) or a coincidence (two unrelated rows happen to share an amount). Always worth a quick eyeball.

## Matching algorithm

Greedy 1-1 pairing by exact baht amount (rounded to 2dp), with merchant-token preference:

1. Bucket Notion rows by amount.
2. For each statement row, look in the matching-amount bucket. Among candidates, prefer one whose merchant name shares **any uppercase alphanumeric token of length ≥ 3** with the statement row's name (e.g. `WWW.GRAB.COM BANGKOK` and `WWW.GRAB.COM BANGKOK` share `GRAB`, `BANGKOK`; `2C2P *SHOPEE 03/10` and `2C2P *SHOPEE 03/10` share `2C2P`, `SHOPEE`). If no name match, fall back to first available — flagged `name_match: false`.
3. Anything left in either pile after the sweep becomes a finding.

**Why exact-amount-first instead of fuzzy:** the bill cycle is a narrow window (≤ ~30 days, one card), and merchant amounts rarely collide by coincidence even with high-volume merchants. Bank statements re-print the exact baht amount that hits the user's account, so the amount column is the strongest signal. Fuzzy on amount risks pairing unrelated rows that happen to be a few baht apart.

**Known limitation:** the matcher does not align dates. The bank's `TRANS DATE` and Notion's `Transaction Datetime` agree most of the time, but occasionally drift by ±1 day (timezone, late-night posts). If you spot a `name_mismatch` whose dates also disagree, that's a stronger "really different rows" signal worth verifying manually.

## What the user typically asks

- "Audit Nuta's UOB One bill for this cycle" → resolve the latest UOB statement PDF, transcribe Nuta's section, run the skill.
- "Anything missing or extra on Baiboon's KTC for cycle 2026-04-27?"
- "The bank's total is X but Notion shows Y — where's the gap?"

## Procedure

1. **Get the statement — Notion first, disk second, ask only as a last resort.** Each Bills row stores the issuer's PDF on `ใบแจ้งยอด (PDF)`; that's the authoritative copy. Query the Bills DB for `(Card, วันตัดรอบบิล)` matching the cycle, pull the file's signed `file.url`, `curl` it to a temp path. Only if Notion has no statement attached should you look in `~/Downloads` / ask the user. UOB / AEON statements are bundles — pages cover Takumi (primary) + Baiboon + Nuta on the same product. CardX / KTC / Krungsri-family statements are scoped to one (card, holder). For bundles, find the sub-section whose cardmember name matches the requested holder (e.g. `JINUTA SAKARUN` for Nuta) — see [[../../docs/concepts/statement-bundling]].
2. **Extract the PDF to text** using `audit-bill/extract.py --pdf <path> [--password …] [--pages a-b]`. Read the text. Do not screenshot the PDF page by page — the text version is faithful enough and an order of magnitude cheaper.
3. **Slice this holder's rows for this card** from the text. Skip `PREVIOUS BALANCE`, `SUB TOTAL`, `TOTAL BALANCE`, payment-acknowledgement rows. CR rows → negative `amount`. Foreign-currency rows: use the printed THB column, not the foreign one.
4. **Compute the cycle's BC date in Notion's convention.** UOB shifts the day-25 BC earlier on weekend/Thai holidays — feed the *shifted* date (see `lib.bill_cycle` and [[../../docs/concepts/bill-cycle-patterns]]).
5. **Build the JSON spec.** Include `statement_subtotal` when the PDF prints it — the script will then surface any transcription drift between your `statement_transactions` sum and the bank's printed total via `statement.subtotal_source` / `statement.rows_sum`.
6. **Run the diff CLI. Read the envelope.**
7. **Report** to the user in this order:
   - Subtotal table: Notion / Statement / Δ.
   - `missing_in_notion` (rows to consider `/add-transaction` for).
   - `extra_in_notion` (rows to scrutinize — flag cancelled-but-not-removed ones distinctly from legitimate `*CASHBACK*` / `[…]` bookkeeping rows).
   - `name_mismatches` (matched by amount only — quick eyeball).
   - One-line summary of the most likely cause of the subtotal Δ.

   **Never** propose to "fix" the Notion side to match the bank without explicit user direction.

## Hard rules

### 1. Read-only

Same posture as [[../audit-transaction-dates/SKILL.md|/audit-transaction-dates]] and [[../fetch-transactions/SKILL.md|/fetch-transactions]]. The script never calls `pages.update` / `pages.create`. If the diff suggests a change, hand the row ID to the appropriate write skill (and ask the user first).

### 2. Right holder, right sub-section of the PDF

UOB / AEON statement PDFs bundle all holders on the same account (see [[../../docs/concepts/statement-bundling]]). When auditing Nuta, feed *only* the rows under Nuta's cardmember sub-section (`JINUTA SAKARUN`). The primary's `*CASHBACK*` credit rows belong to Takumi's accounting; don't mix them into Nuta's input even though they're "her" cashback by promotion design.

### 3. Verbatim merchant names

Pass the statement's name **verbatim** — no cleaning, no translation. The matcher normalizes internally; passing modified names defeats the name-overlap preference and can cause spurious mismatches.

### 4. Negative amounts for credits / refunds

The bank prints `CR` next to credit rows; the matcher expects negative numbers. Refunds, cashback credits (when on this holder's sub-section), and chargebacks all go negative.

### 5. Cycle date follows the bank pattern

The Notion BC stored on the cycle's transactions is the same value [[../prepare-bill/SKILL.md|/prepare-bill]] writes onto the Bills row — including UOB's weekend/holiday shift. Pass that value here, not the bank's printed `STATEMENT DATE` (which is one day later).

## What this skill does NOT do

- Does **not** parse PDF *tables*. The extract CLI gets you faithful text; row parsing is the agent's job because layouts vary too much per issuer (UOB / AEON bundle multiple holders, CardX prints one sub-card, KTC mixes points + transactions in one block). A future revision can bolt per-issuer table parsers on top of `lib/pdf_text.py` without changing the diff CLI.
- Does **not** mutate Notion. Findings flow back through [[../update-transaction/SKILL.md|/update-transaction]] or [[../add-transaction/SKILL.md|/add-transaction]] only after the user confirms.
- Does **not** audit non-transaction Bills properties (paid flag, files). For those, use Notion directly or [[../update-bill/SKILL.md|/update-bill]] when patching.
- Does **not** translate Thai labels — `ยอดชำระ`, `Bill Cycle Date`, `จ่ายแล้ว` stay verbatim per project convention.
- Does **not** auto-reconcile by editing rows. The household's Notion `ยอดชำระ` is the calculated balance of record; drift is signal, not error.
