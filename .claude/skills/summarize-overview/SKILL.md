---
name: summarize-overview
description: Produce the cardholder's overview table — "สรุปบัตรและสินเชื่อที่<name>ถือ" — listing every card / credit line they hold with outstanding balance, points balance, bill cycle, and due date. Use when the user asks for an at-a-glance picture of one holder's portfolio (e.g. "what cards does Nuta have?", "show me Baiboon's summary", "what's outstanding across all of <holder>'s cards?"). Read-only.
---

# summarize-overview

Reads a cardholder's Cards data source and reproduces, in the conversation, the same overview the user sees in Notion under "สรุปบัตรและสินเชื่อที่<name>ถือ". One holder per invocation — that's how the user typically asks, even if they sometimes batch (e.g. "both Nuta and Baiboon's"). For batch requests, run the script once per holder and produce one table per holder.

This skill is **read-only**. For writes, see [[add-transaction]]. For querying individual transactions, see [[fetch-transactions]]. For any *other* form of summary (transaction totals, category breakdowns, monthly burn rate, etc.), a separate skill should be created — this one is intentionally narrow.

## Why this skill exists separately

The Notion database titled "สรุปบัตรและสินเชื่อที่<name>ถือ" shares the same data source UUID as the holder's Cards DB ([[../../docs/databases/baiboon-cards]] / `nuta-cards` / `takumi-cards`). The "summary" name is just a different display name for the same rows, with a particular table view (sorted by `ยอดค้างชำระ` DESC). The user *thinks of it* as a summary view, so the skill exists to honor that mental model — even though the underlying data is the Cards DS itself.

## Primary execution path — the deterministic script

This skill is backed by `scripts/python/summarize-overview/cli.py`. Use it; don't reinvent with raw MCP calls.

Invocation:

```sh
echo '{"holder":"baiboon"}' | uv run scripts/python/summarize-overview/cli.py
```

Input spec — all keys validated; `holder` is the only required key:

```json
{
  "holder": "takumi | baiboon | nuta",
  "include_zero_balance": false
}
```

`include_zero_balance` defaults to `false`. When false, rows where `outstanding_balance` rounds to zero at 2 d.p. are excluded — they're noise for a "what do I owe?" question. **Negative balances are kept** even with the filter on, because a credit balance (refund / overpayment) is meaningful information. The CLI's response includes both `total_count` (pre-filter) and `count` (returned) so you can mention how many were hidden.

Output: a JSON envelope `{holder, thai_name, title, count, results}`. Each result row is:

| Key                     | Notion property      | Type                                                   |
|-------------------------|----------------------|--------------------------------------------------------|
| `id` / `url`            | (page meta)          | string                                                 |
| `name`                  | `Name`               | title                                                  |
| `bank`                  | `ธนาคาร/บริษัท`        | select                                                 |
| `card_network`          | `Card Network`       | select (`JCB`, `Mastercard`, `VISA`, `UnionPay`, …)    |
| `premium_tier`          | `ความพรีเมียม`         | select (`สูง (Signature)`, `ธรรมดา (Platinum)`, `ไม่มี`) |
| `credit_limit`          | `วงเงินที่ได้`          | number (baht)                                          |
| `baht_per_point`        | `บาทต่อ 1 คะแนน`       | number                                                 |
| `points_per_bill_cycle` | `ให้คะแนนตามรอบบิล`     | checkbox                                               |
| `outstanding_balance`   | `ยอดค้างชำระ`          | formula → number                                       |
| `points_balance`        | `คะแนนสะสม`           | rollup → number (sum)                                  |
| `latest_bill_cycle`     | `วันตัดรอบบิล`          | rollup → date (latest)                                 |
| `latest_due_date`       | `วันครบกำหนดชำระ`      | rollup → date (latest)                                 |
| `note`                  | `Note`               | rich text                                              |

Rows are sorted the same way the Notion table view sorts them:

1. `outstanding_balance` DESC
2. `latest_bill_cycle` ASC
3. `points_balance` DESC
4. `name` ASC

Nulls in numeric / date columns sort to the bottom of their respective tie-break group.

## Procedure

1. **Confirm the holder.** Single holder per run. If the user asked for multiple, run the CLI once per holder and emit one table per holder.
2. **Decide on `include_zero_balance`.** Default is **false** — a "what does X hold?" / "what's outstanding?" question doesn't need cards at zero. Set it to **true** when the user's question doesn't depend on outstanding balance, namely:
   - Accumulated / total points across all cards.
   - Highest-earning card by `บาทต่อ 1 คะแนน`.
   - Anything about the *card portfolio* itself (network mix, premium-tier distribution, banks represented).
   - Anything that explicitly says "all cards" / "every card" / "the full list".
3. **Run the script.** Pipe the spec in, get JSON back.
4. **Format as markdown.** See *Output shape* below.
5. **Report back.** Lead with the Thai title (verbatim) for the holder so the user can map directly to what they see in Notion. If rows were filtered out, mention the hidden count in one trailing sentence (e.g. "8 zero-balance cards hidden — ask for the full list if you need them").

## Output shape

Default to a **lean** quick-glance table with these columns only:

| Card | ยอดค้างชำระ (฿) | วันตัดรอบบิล | วันครบกำหนดชำระ | คะแนนสะสม |

The CLI returns the full row dict (bank, card network, premium tier, credit limit, baht/point, points-per-bill-cycle, note, …) so that any *follow-up* the user asks ("which are UOB?", "which are Signature tier?", "how much credit is unused?") can be answered without a re-fetch. But **don't surface those columns by default** — they're bloat for the at-a-glance overview the user is asking for. Only add a column if the user explicitly asks ("…include the credit limits", "…group by bank") or the question genuinely depends on it.

Append a one-line total below the table: `Σ ยอดค้างชำระ = ฿<sum>`. Skip the points sum unless the user asked about points or any row's `คะแนนสะสม` is non-zero.

Don't dump `id` / `url` inline. If the user asks for raw URLs, list them as a trailing block.

## Hard rules

### 1. Verbatim Thai

Card titles, bank names, select-option labels (e.g. `บัตรกรุงศรี`, `ความพรีเมียม` values) stay in Thai. Don't translate them in the output table. Gloss in English on first use per response if the user is asking for an explanation, not data.

### 2. Read-only

If a user request implies a write ("…and please pay these off", "…and remove the closed cards"), stop and confirm before doing anything. This skill returns data.

### 3. One holder per CLI run

The CLI is single-holder by design. Batch requests are handled at the agent layer by running the CLI once per holder.

### 4. Don't double-up with other summary forms

If the user asks for a fundamentally different breakdown — by transaction category, by month, by merchant, by bill cycle — that's a *different* summary task. Don't bolt it onto this skill. Either invoke a more specific skill if one exists, or ask the user whether they want a new skill created.

## What this skill does NOT do

- Does **not** mutate Notion.
- Does **not** show per-transaction detail. For that, use [[fetch-transactions]].
- Does **not** show bills. The Bills DBs are separate (Baiboon and Nuta only) and out of scope here.
- Does **not** translate Thai labels.
