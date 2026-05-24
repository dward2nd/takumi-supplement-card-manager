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
  "properties":    { "<raw notion prop>": ... }
}
```

**Identify the bill row** either by `(holder, card, bill_cycle)` *or* by `id`. If `id` is set, the lookup keys are optional (used only for the response echo). Otherwise all three lookup keys are required and must match a unique row.

**At least one update field is required** (`paid`, `note`, `slip`/`slips`, `statement_pdf`/`statement_pdfs`, or `properties`). The script errors out on an empty update so a typo doesn't silently no-op.

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
- Does **not** add transactions. Use [[../add-transaction/SKILL.md|/add-transaction]].
- Does **not** edit transactions. Use [[../update-transaction/SKILL.md|/update-transaction]].
- Does **not** mutate Takumi's data (Takumi has no Bills DB).
- Does **not** translate Thai labels — `จ่ายแล้ว`, `หลักฐานการชำระ`, `ใบแจ้งยอด (PDF)`, `วันตัดรอบบิล` stay verbatim per project convention.
