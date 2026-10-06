---
name: fetch-transactions
description: Query a cardholder's Notion Transactions database with structured conditions (card, date range, amount, merchant substring, flags) and return matched rows. Optionally aggregate with `summary: true` to get count / Σ ยอดชำระ / Σ cashback. Use when the user asks "what are the recent / last N / biggest / unpaid / etc. transactions on …" or aggregate questions like "total spend at <merchant> this cycle" or "cumulative cashback this cycle". Read-only.
---

# fetch-transactions

Reads transaction pages from **one** cardholder's Transactions database under user-specified conditions, then returns a summary sorted to the user's request.

This skill is **read-only**. It never creates, updates, or deletes Notion content. For writes, see [[add-transaction]].

## Primary execution path — the deterministic script

This skill is backed by a Python CLI at `scripts/python/fetch-transactions/cli.py`. Use it; do not reinvent the query with MCP calls when the script is available. It hits Notion's native `data_sources/{id}/query` endpoint (filter + sort + limit in one round trip), which the MCP cannot.

Invocation:

```sh
echo '<JSON-spec>' | uv run scripts/python/fetch-transactions/cli.py
```

JSON spec — all keys optional except `holder`:

```json
{
  "holder": "takumi | baiboon | nuta",
  "card": "First Choice",
  "bill_cycle": "2026-05-29",
  "bill_cycle_range": ["2026-05-01", "2026-05-31"],
  "transaction_date_range": ["2026-05-01", "2026-05-31"],
  "min_amount": 100,
  "max_amount": 5000,
  "processed": true,
  "paid": false,
  "credit_return": false,
  "note_contains": "uber",
  "name_contains": "MAKRO",
  "sort": "date_desc | date_asc | amount_desc | amount_asc | bill_cycle_desc | bill_cycle_asc",
  "limit": 5,
  "summary": true
}
```

`name_contains` is a case-sensitive substring match on the merchant title — use it for "spending at X" questions. Notion's `title.contains` is the native predicate, so the filter runs server-side.

`summary: true` adds a `summary` block to the envelope with `{count, total_amount, total_cashback}` computed from the returned rows. Use it for aggregate questions like "what's my Makro spend this cycle?" or "cumulative cashback this cycle?". Drop `limit` when you want the aggregate over the full filtered set — `limit` truncates *before* the summation. For "summary only" (no per-row dump), just ignore the `results` array client-side; we don't have a dedicated summary-only mode.

Output: a JSON envelope `{holder, card, count, results: [...], summary?: {...}}`. Each result row has `id`, `url`, `name` (verbatim), `amount`, `transaction_date`, `bill_cycle_date`, `due_date`, `processed`, `paid`, `credit_return`, `note`, `card_ids`, `cashback_percent`, `cashback`. The last two are populated for Baiboon and Nuta but come back `null` for Takumi (the properties don't exist on Takumi's DS), and `total_cashback` in the summary will be `0` for Takumi.

Translate the user's request into the spec, run the script, then format the JSON into the markdown table described in *Output shape* below. Don't summarize or paraphrase merchant names — pass them through verbatim.

## What the user typically asks

- "Last 5 transactions on Nuta's First Choice card."
- "Show me Baiboon's transactions between 2026-04-01 and 2026-04-30."
- "What's the largest charge on Takumi's UOB World this cycle?"
- "Which of Nuta's transactions in this bill cycle are not yet `ชำระแล้ว`?"
- "Total Makro spend on Baiboon's First Choice this cycle?" → `name_contains: "MAKRO"` + `summary: true`.
- "Cumulative cashback on Nuta's UOB One this cycle?" → `bill_cycle` + `summary: true` (no limit).

## Hard rules

### 1. Correct holder → correct database

Same routing table as [[add-transaction]]:

| Holder   | Transactions data source ID                | Cards data source ID                       |
|----------|--------------------------------------------|--------------------------------------------|
| Takumi   | `1aacb755-f0f1-81dc-8e9f-000b20891025`     | `1aacb755-f0f1-818a-a284-000b17d155de`     |
| Baiboon  | `181cb755-f0f1-8167-b5b6-000bc6d47469`     | `99bb5ba6-79b1-47e2-9b8f-fa3102d5b294`     |
| Nuta     | `2a1cb755-f0f1-8110-9795-000bf7d48b4f`     | `2a1cb755-f0f1-8188-9b00-000b5fa448b8`     |

`CLAUDE.md` is the source of truth for these IDs.

### 2. Card name matching is exact

If the user names a card, the CLI's `card` key resolves it the same way as the write skill (`lib.cards.find_card` against that holder's Cards DS): **exact title match**, no substrings.

### 3. Return verbatim merchant names

When you display the results, the merchant name (`Name`) is reproduced **exactly** as Notion stores it. No translation, no cleanup. Same rule as the write skill.

### 4. Never mutate

Even if the user's question implies "and please also mark them as paid", **stop and confirm** before touching anything. This skill returns data; updates are a separate, explicit step.

## Filterable properties on Transactions

Common ones, all readable from a fetched transaction page:

| Property                    | Type      | Usage                                          |
|-----------------------------|-----------|------------------------------------------------|
| `Name`                      | title     | merchant string, verbatim                      |
| `Card`                      | relation  | JSON array string with one card URL            |
| `ยอดชำระ`                    | number    | amount in baht                                 |
| `date:Transaction Datetime` | date      | when the user made the charge                  |
| `date:Process Date`         | date      | bank processing date (often blank)             |
| `date:Bill Cycle Date`      | date      | which statement                                |
| `date:Due Date`             | date      | payment deadline                               |
| `Processed`                 | checkbox  | `"__YES__"` / `"__NO__"`                       |
| `ชำระแล้ว`                   | checkbox  | paid by the supplement holder                  |
| `Credit Return`             | checkbox  | refund/chargeback                              |
| `×0` `×2` `×3` `×4` `×5` `÷4` | checkbox | point multipliers (Takumi-only `×3`)         |
| `ใช้คะแนน`                   | number    | points redeemed                                |
| `Note`                      | text      |                                                |

Read-only / derived (don't try to filter through Notion — compute after fetching):

- `คะแนนที่ได้จริง`, `คะแนน unrealized` — formulas.
- `บาทต่อ 1 คะแนน` — rollup from the Card.
- Nuta's `% cb`, `cashback` — formulas.
- Takumi's `หมวดหมู่` — relation to category DB.

## Output shape

Default to a small markdown table. Example:

```
| # | Date       | Merchant                      | Amount (฿) | ชำระแล้ว |
|---|------------|-------------------------------|-----------:|:--------:|
| 1 | 2026-05-18 | HTTPS://WWW.MAKRO.PRO/ BANGKOK TH | 6,839  |    ✗     |
```

Append a one-line total when it's useful (sum of `ยอดชำระ` over the result set), and the card + holder above the table so the routing is obvious.

If the user asks for the raw page URLs, include them as a trailing list — don't inline them in the table.

## What this skill does NOT do

- Does **not** mutate Notion. Use [[add-transaction]] for writes.
- Does **not** translate Thai labels.
- Does **not** fabricate filters — if a property the user references doesn't exist on this holder's DB (e.g. `% cb` on Baiboon), say so.
