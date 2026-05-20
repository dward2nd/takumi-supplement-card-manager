---
name: add-notion-transaction
description: Add one or more transaction records to a cardholder's Notion Transactions database. Use when the user lists spending (merchant name + amount, optionally a date and card) and asks to record it in Notion. Enforces verbatim merchant names, correct holder→database routing, correct Card relation, and Processed=true as the default.
---

# add-notion-transaction

Adds transaction page rows to **one** cardholder's Notion Transactions database, all mapped to **one** of that holder's supplement cards.

This is the only sanctioned write path for transactions. It overrides the project's general "don't mutate Notion without explicit instruction" rule because the user invoked this skill explicitly.

## Primary execution path — the deterministic script

This skill is backed by a Python CLI at `scripts/python/add-notion-transaction/cli.py`. Use it; do not reinvent the write with raw MCP calls when the script is available. The script enforces every "hard rule" below in code — verbatim merchant name, holder → DS routing, exact card-title resolution, `Processed=true` default, leaving non-policy fields alone — so cooperation is "build the JSON, hand it off".

Invocation:

```sh
echo '<JSON-spec>' | uv run scripts/python/add-notion-transaction/cli.py
# add --dry-run to preview the payload without writing
```

JSON spec:

```json
{
  "holder": "takumi | baiboon | nuta",
  "card": "First Choice",
  "bill_cycle": "2026-05-29",
  "due_date": "2026-06-15",
  "processed": true,
  "transactions": [
    { "date": "2026-05-13", "name": "TMN 7-11 BANGKOK TH", "amount": 89.0, "note": "optional" }
  ]
}
```

Output: a JSON envelope `{holder, card, card_page_id, bill_cycle, due_date, processed, count, created: [{id, url, name, amount, date}, ...]}`. Surface the count + a compact list back to the user. Don't dump full URLs unless asked.

**Rollback** (cleanup or mistakes): `uv run scripts/python/add-notion-transaction/archive.py --ids <page-id>[,<page-id>...]`. Archiving is idempotent.

## What the user supplies

1. **Cardholder** — one of `Takumi` (เว็บ) / `Baiboon` (ใบบุญ) / `Nuta` (นุตา). Determines which Transactions DB you write to and which Cards DB you query for the relation.
2. **Card name** — e.g. `First Choice`, `UOB World`. Must match an existing row in that holder's Cards DB by `Name`.
3. **Billing window for the batch** — `Bill Cycle Date` and `Due Date`, both single ISO dates. Applied uniformly to every transaction in the batch unless the user splits the batch.
4. **The transaction list** — one or more entries, each carrying:
   - **Transaction date** (`Transaction Datetime`) — ISO date.
   - **Merchant string** — the *full*, *verbatim* merchant name as supplied.
   - **Amount in baht** (`ยอดชำระ`).
   - Optional **Note**.

The user often bundles entries under date headings ("## 13 May") — split them out into one Notion page per amount, all sharing that date.

## Hard rules (the script enforces these — listed here so you can explain them when the user asks)

### 1. Merchant name is verbatim

The `Name` field (title) must contain the **entire merchant string the user provided**. No truncation, no normalization, no expanding abbreviations, no removing currency tags or country codes.

- `TMN 7-11 BANGKOK TH` → `Name = "TMN 7-11 BANGKOK TH"`. Not `"TMN 7-11"`, not `"7-Eleven"`.
- `HTTPS://WWW.MAKRO.PRO/ BANGKOK TH` → `Name = "HTTPS://WWW.MAKRO.PRO/ BANGKOK TH"`. Not `"Makro"`.
- When the user says **"repeat this exact name"**, every page in that group gets the same `Name`, even if the amounts differ.

If you ever feel tempted to shorten a name to make it look tidier, **stop** — the verbatim string is what lets the user reconcile against their bank statement.

### 2. Correct holder → correct database

Pick the data source by holder. **Never** cross-write — a Baiboon transaction must never land in Nuta's DB, etc.

| Holder   | Transactions data source ID                | Cards data source ID                       |
|----------|--------------------------------------------|--------------------------------------------|
| Takumi   | `1aacb755-f0f1-81dc-8e9f-000b20891025`     | `1aacb755-f0f1-818a-a284-000b17d155de`     |
| Baiboon  | `181cb755-f0f1-8167-b5b6-000bc6d47469`     | `99bb5ba6-79b1-47e2-9b8f-fa3102d5b294`     |
| Nuta     | `2a1cb755-f0f1-8110-9795-000bf7d48b4f`     | `2a1cb755-f0f1-8188-9b00-000b5fa448b8`     |

`CLAUDE.md` at the repo root is the source of truth for these IDs — re-read it if anything feels stale.

### 3. The Card relation must resolve

Before creating any pages:

1. Call `mcp__notion__notion-search` with `data_source_url: "collection://<holder-cards-collection>"` and `query: "<card name>"`.
2. Filter the results to an **exact** match on the card's title. Reject substring matches (`Krungsri JCB` is not `Krungsri NOW`; `UOB One` is not `UOB World`).
3. Capture the card page URL (`https://www.notion.so/<id>`). Pass it in the `Card` property as a **JSON array string** containing one element:

   ```json
   "Card": "[\"https://www.notion.so/<card-page-id>\"]"
   ```

   The Notion `Card` relation column is documented in the schema as "JSON string of a single page URL". A single-element JSON array is the working format.

- **Zero matches** → stop and tell the user the card name was not found in that holder's Cards DB. Do not invent or guess. Suggest they check the spelling against `docs/cards/_stubs.md`.
- **Multiple exact matches** → stop and ask which one.

### 4. `Processed` is true by default

Always set `"Processed": "__YES__"`, regardless of the real processing status. This is current user policy — only override if the user explicitly says "leave Processed false" for a batch.

### 5. Properties to set on each page

| Notion property                          | Value                                                                |
|------------------------------------------|----------------------------------------------------------------------|
| `Name`                                   | verbatim merchant string                                             |
| `Card`                                   | JSON array string with the matched card's page URL                   |
| `ยอดชำระ`                                 | numeric, in baht                                                     |
| `date:Transaction Datetime:start`        | ISO date (e.g. `"2026-05-13"`)                                       |
| `date:Transaction Datetime:is_datetime`  | `0` (unless the user supplied a time)                                |
| `date:Bill Cycle Date:start`             | ISO date for the batch                                               |
| `date:Bill Cycle Date:is_datetime`       | `0`                                                                  |
| `date:Due Date:start`                    | ISO date for the batch                                               |
| `date:Due Date:is_datetime`              | `0`                                                                  |
| `Processed`                              | `"__YES__"`                                                          |
| `Note`                                   | only if the user provided one                                        |

**Leave alone** (do NOT set unless the user explicitly asks):

- `Process Date` — bank-side; we don't know it at write time.
- `Credit Return`, `ชำระแล้ว` — payment-lifecycle flags.
- All point-multiplier checkboxes (`×0` `×2` `×4` `×5` `÷4`, plus Takumi-only `×3`). Defaults are false; the realized-points formula will compute correctly.
- `ใช้คะแนน` — points-redemption is rare and explicit.
- Takumi-only `หมวดหมู่` (category) relation.

Nuta-only `% cb` / `cashback` are formulas — not writable anyway.

## Procedure

1. **Confirm holder and parse the batch.** If the holder is ambiguous from context, ask.
2. **Build the JSON spec** described in *Primary execution path*. Every amount the user listed becomes its own entry in `transactions`, even when the merchant string repeats across amounts.
3. **Run the script.** Pipe the JSON in, read the JSON envelope back.
4. **Report back** with the count, the merchant/amount/date list, and the card. Don't dump every Notion URL unless asked.
5. **MCP fallback** — only if the script isn't available (e.g. wrong repo): use one `mcp__notion__notion-create-pages` call with `parent: { type: "data_source_id", data_source_id: "<holder transactions DS>" }` and the same property mapping below.

## After writing

If anything in the API response looks off (a `Card` field that didn't resolve, a missing amount, a date that came back unset), surface it immediately and offer to retry the affected pages.

## What this skill does NOT do

- Does **not** edit existing transactions. Updates go through `mcp__notion__notion-update-page`, by direct user instruction.
- Does **not** create bills (`บิลเรียกเก็บค่าบัตรเครดิต`). Bills are separate DBs and out of scope.
- Does **not** add cards. The card must already exist in the holder's Cards DB.
- Does **not** translate Thai labels. Property names stay verbatim in code-spans, per project doc conventions.
