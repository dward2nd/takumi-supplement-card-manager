---
name: update-notion-transaction
description: Patch property values on one or more existing transaction pages in Notion (e.g. fill `% cb` after merchant-tier classification, add a `Note`, set a multiplier checkbox that was missed at write time). Use when the user says "update / patch / fix / amend transaction <id>", "set cashback on this row", or otherwise wants to mutate fields on already-created transactions. The write counterpart to [[../add-notion-transaction/SKILL.md|add-notion-transaction]].
---

# update-notion-transaction

Patches existing transaction pages without re-creating them. This is the only sanctioned **update** path for transactions — it overrides the project's general "don't mutate Notion without explicit instruction" rule because the user invoked this skill explicitly.

Use this when:

- A transaction was created without `% cb` and the cashback tier is now known (typical for Nuta after merchant-tier classification).
- A `Note` needs to be added retroactively to explain an exclusion (see [[../add-notion-transaction/SKILL.md|add-notion-transaction]] Rule 4c).
- A multiplier checkbox was omitted at write time and the card's earning policy says one should be set.
- Any other policy-required field is missing from already-written rows.

For creating brand-new transactions, use [[../add-notion-transaction/SKILL.md|/add-notion-transaction]]. For rolling back accidental writes, use that skill's `archive.py`. For reading rows, use [[../fetch-notion-transactions/SKILL.md|/fetch-notion-transactions]].

## Primary execution path — the deterministic CLI

`scripts/python/update-notion-transaction/cli.py` is the only mechanical step. The CLI enforces input validation and idempotency in code, so the agent's job is to build the right JSON spec and hand it off.

Invocation (run from `scripts/python/` so `uv` picks up the project env):

```sh
cd scripts/python
echo '<JSON-spec>' | uv run update-notion-transaction/cli.py
# add --dry-run to preview the resolved Notion properties payload without writing
```

JSON spec — `updates` is required and must be non-empty:

```json
{
  "updates": [
    { "id": "<page-uuid>", "cashback_percent": 0.05 },
    { "id": "<page-uuid>", "cashback_percent": 0.00, "note": "Foreign merchant (US) charged in THB — no points/cashback on Thai-issued cards." },
    { "id": "<page-uuid>", "multiplier": "×0" },
    { "id": "<page-uuid>", "properties": { "Note": { "rich_text": [{ "text": { "content": "raw escape hatch" } }] } } }
  ]
}
```

Recognized convenience keys per update entry:

| Key                 | Notion property | Notes                                                                 |
|---------------------|-----------------|-----------------------------------------------------------------------|
| `cashback_percent`  | `% cb`          | Raw fraction in `[0, 1]`. `0.05` → displays as `5%`. **Nuta only** — the field doesn't exist on Baiboon/Takumi. |
| `note`              | `Note`          | Free-form string. Replaces the existing `Note`.                       |
| `multiplier`        | one of `×0`/`×2`/`×3`/`×4`/`×5`/`÷4` | Sets the named checkbox to `true`. **Mutually exclusive** — only one multiplier per page; the CLI will not unset other multipliers, so don't use this to flip from one tier to another without first thinking about which checkbox is currently on. `×3` is Takumi-only. |
| `properties`        | (raw)           | Escape hatch: merge an arbitrary Notion `properties` payload. Use sparingly — prefer a convenience key. |

Output: `{ "count": N, "updated": [ { "id": "<page-id>", "fields": [<prop names set>] }, ... ] }`. Surface the count and field list back to the user.

## What the user supplies

1. **One or more transaction page IDs** — UUIDs (or full Notion URLs the agent strips to UUIDs). The user typically obtains these from a prior `/add-notion-transaction` or `/fetch-notion-transactions` run.
2. **Which fields to set** — and what values. If the user describes a tier ("5% cashback on this row") rather than the raw fraction, *you* do the conversion (5% → `0.05`); don't push the math back to the user.
3. *Optionally* the cardholder, if context isn't clear — used only to validate that `cashback_percent` is being written to a Nuta page (the field exists nowhere else).

## Hard rules

### 1. Page IDs only

The CLI takes Notion page UUIDs. If the user pastes a full URL, strip it down to the UUID before sending. Never write to a page whose UUID you haven't been given — the script has no "search by merchant" fallback, on purpose.

### 2. `% cb` is Nuta-only

`% cb` exists only on Nuta's Transactions data source. Setting it on a Baiboon or Takumi page returns a 400 from Notion. The CLI doesn't pre-check the page's parent DS — *you* must. When in doubt, fetch the page first with `mcp__notion__notion-fetch` and verify the parent collection.

### 3. Multipliers stay mutually exclusive

The CLI sets the named checkbox to `true` but does **not** unset other multiplier checkboxes. That means: if a page already has `×2` and you set `multiplier: "×5"`, the page ends up with **both** checked, which makes Notion's earning formula double-count. If you need to *change* a multiplier:

1. Fetch the page and see which multiplier (if any) is currently `true`.
2. If a different one is checked, use the `properties` escape hatch to set the old one to `false` and the new one to `true` in the same update.

### 4. Cashback raw fraction, not percentage

`cashback_percent: 0.05` means **5%**. `cashback_percent: 5` is **500%** and the CLI rejects it (`must be a raw fraction in [0, 1]`). This mirrors Notion's storage convention for percent-formatted number fields — see [[../../docs/concepts/cashback.md|cashback]] / [[../../docs/formulas/cashback.md|cashback formula]] and [[../../docs/databases/nuta-transactions.md|nuta-transactions]].

### 5. Don't second-guess the original merchant string

This skill does **not** edit `Name` (the merchant string). If a page has the wrong merchant name, that's a re-create case (archive + re-add), not an update — the verbatim rule from [[../add-notion-transaction/SKILL.md|add-notion-transaction]] Rule 1 is what reconciles against bank statements, and rewriting it after the fact defeats the purpose.

If the user explicitly asks to edit `Name` anyway, surface the rationale ("this'll break statement reconciliation — sure?") before reaching for the `properties` escape hatch.

## Procedure

1. **Resolve page IDs.** If the user pasted URLs, extract the UUIDs. If they referenced "the last batch", look at the most recent `/add-notion-transaction` envelope in the conversation.
2. **Apply policy if classifying tiers.** If the user dropped a batch like "set these to 5%, these to 1%", you do the tier classification (see [[../add-notion-transaction/SKILL.md|add-notion-transaction]] *Card-specific earning policies*) and produce the raw fractions yourself.
3. **Build the JSON spec.** One entry per page.
4. **Run with `--dry-run` first** if the batch is large (≥ 5 entries) or if any entry uses the `properties` escape hatch. Show the resolved payload to the user, then re-run without `--dry-run`.
5. **Report back** with the count and a compact list `{id → fields_set}`. Don't dump full URLs unless asked.

## What this skill does NOT do

- Does **not** create new transactions. Use [[../add-notion-transaction/SKILL.md|/add-notion-transaction]].
- Does **not** archive / delete transactions. Use `scripts/python/add-notion-transaction/archive.py`.
- Does **not** read rows. Use [[../fetch-notion-transactions/SKILL.md|/fetch-notion-transactions]].
- Does **not** edit cards or bills. Cards changes go through Notion directly; bills are out of scope.
- Does **not** translate Thai property names. `% cb`, `ยอดชำระ`, `Note` stay verbatim.
