---
name: fetch-notion-transactions
description: Query a cardholder's Notion Transactions database with structured conditions (card, date range, amount, flags) and return matched rows. Use when the user asks "what are the recent / last N / biggest / unpaid / etc. transactions on …" or otherwise wants to read transaction data filtered by some property. Read-only.
---

# fetch-notion-transactions

Reads transaction pages from **one** cardholder's Transactions database under user-specified conditions, then returns a summary sorted to the user's request.

This skill is **read-only**. It never creates, updates, or deletes Notion content. For writes, see [[add-notion-transaction]].

## Primary execution path — the deterministic script

This skill is backed by a Python CLI at `scripts/python/fetch-notion-transactions/cli.py`. Use it; do not reinvent the query with MCP calls when the script is available. It hits Notion's native `data_sources/{id}/query` endpoint (filter + sort + limit in one round trip), which the MCP cannot.

Invocation:

```sh
echo '<JSON-spec>' | uv run scripts/python/fetch-notion-transactions/cli.py
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
  "sort": "date_desc | date_asc | amount_desc | amount_asc | bill_cycle_desc | bill_cycle_asc",
  "limit": 5
}
```

Output: a JSON envelope `{holder, card, count, results: [...]}`. Each result has `id`, `url`, `name` (verbatim), `amount`, `transaction_date`, `bill_cycle_date`, `due_date`, `processed`, `paid`, `credit_return`, `note`, `card_ids`.

Translate the user's request into the spec, run the script, then format the JSON into the markdown table described in *Output shape* below. Don't summarize or paraphrase merchant names — pass them through verbatim.

## What the user typically asks

- "Last 5 transactions on Nuta's First Choice card."
- "Show me Baiboon's transactions between 2026-04-01 and 2026-04-30."
- "What's the largest charge on Takumi's UOB World this cycle?"
- "Which of Nuta's transactions in this bill cycle are not yet `ชำระแล้ว`?"

## MCP fallback (no script available)

If you're in an environment without the Python sandbox (e.g. a different repo), the MCP-only patterns below still work — they're slower and need client-side filtering, but they're correct. The Notion MCP exposes `mcp__notion__notion-fetch` (one page/data source by ID) and `mcp__notion__notion-search` (semantic, optionally scoped to a data source — **not** a structured filter). There is **no `query_data_sources` tool** wired in.

## Hard rules

### 1. Correct holder → correct database

Same routing table as [[add-notion-transaction]]:

| Holder   | Transactions data source ID                | Cards data source ID                       |
|----------|--------------------------------------------|--------------------------------------------|
| Takumi   | `1aacb755-f0f1-81dc-8e9f-000b20891025`     | `1aacb755-f0f1-818a-a284-000b17d155de`     |
| Baiboon  | `181cb755-f0f1-8167-b5b6-000bc6d47469`     | `99bb5ba6-79b1-47e2-9b8f-fa3102d5b294`     |
| Nuta     | `2a1cb755-f0f1-8110-9795-000bf7d48b4f`     | `2a1cb755-f0f1-8188-9b00-000b5fa448b8`     |

`CLAUDE.md` is the source of truth for these IDs.

### 2. Card name matching is exact

If the user names a card, resolve it the same way as the write skill: `notion-search` against that holder's Cards DS, **exact title match**, no substrings.

### 3. Return verbatim merchant names

When you display the results, the merchant name (`Name`) is reproduced **exactly** as Notion stores it. No translation, no cleanup. Same rule as the write skill.

### 4. Never mutate

Even if the user's question implies "and please also mark them as paid", **stop and confirm** before touching anything. This skill returns data; updates are a separate, explicit step.

## Procedure (MCP fallback only)

### Path A — card-scoped query (PREFERRED when a card is named)

This is the highest-fidelity path because the card row carries an inverse relation listing every transaction on that card.

1. **Resolve the card** in the holder's Cards DS via `notion-search` + exact-title filter. Capture the card's page ID.
2. **Fetch the card page** with `notion-fetch`. The response includes an inverse-relation property listing transaction URLs. Note: the column is named after the *holder's transactions DB title*, e.g. `รายการใช้จ่ายผ่านบัตรของใบบุญ` — and Nuta's Cards DS reuses Baiboon's label string for the same column (see [[../docs/concepts/known-divergences]] if/when documented). Read by *position*, not by name.
3. **Pick which transactions to fetch** based on the user's filter:
   - **"Last N by date"** → Notion page IDs are roughly creation-time-sortable, and the relation list tends to come back in creation order. Fetch the trailing `N + ~10` entries (a safety buffer for any out-of-order writes), then sort by `Transaction Datetime` DESC and slice the top N.
   - **"All in bill cycle X"** → fetch *all* entries, then filter on `date:Bill Cycle Date:start`.
   - **"Largest / smallest / matching note"** → fetch all entries, then filter/sort on the relevant property.
4. **Parallelize fetches** in one tool-use block (5–25 fetches per turn is fine; for >50, batch across turns to keep the conversation log readable).
5. **Sort / filter client-side** on the fetched property values.
6. **Display** a compact table: date, merchant (verbatim), amount in baht, optionally any flag the user cares about. Don't dump full URLs unless asked.

### Path B — holder-wide query (no card specified)

When the user doesn't pin a card, the inverse-relation traversal doesn't apply. Fallbacks:

- **Date-range / keyword queries** → try `mcp__notion__notion-search` with `data_source_url: "collection://<txn DS>"` and a substring query, then filter client-side. Acknowledge that semantic search may miss exact matches.
- **Bill-cycle scoped queries** → if the user is asking about a specific bill cycle, the corresponding row in that holder's Bills DB (`บิลเรียกเก็บค่าบัตรเครดิต`) may already aggregate. Check Bills before falling back to per-transaction reads.
- **Anything broader** → tell the user the structured-query gap exists and propose either (a) narrowing by card, or (b) creating a temporary filtered Notion view via `notion-create-view` and reading from that.

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

- Does **not** mutate Notion. Use [[add-notion-transaction]] for writes.
- Does **not** translate Thai labels.
- Does **not** fabricate filters — if a property the user references doesn't exist on this holder's DB (e.g. `% cb` on Baiboon), say so.
