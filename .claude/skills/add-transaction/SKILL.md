---
name: add-transaction
description: Add one or more transaction records to a cardholder's Notion Transactions database. Use when the user lists spending (merchant name + amount, optionally a date and card) and asks to record it in Notion. Enforces verbatim merchant names, correct holder→database routing, correct Card relation, and Processed=true as the default.
---

# add-transaction

Adds transaction page rows to **one** cardholder's Notion Transactions database, all mapped to **one** of that holder's supplement cards.

This is the only sanctioned write path for transactions. It overrides the project's general "don't mutate Notion without explicit instruction" rule because the user invoked this skill explicitly.

## Primary execution path — the deterministic script

This skill is backed by a Python CLI at `scripts/python/add-transaction/cli.py`. Use it; do not reinvent the write with raw MCP calls when the script is available. The script enforces every "hard rule" below in code — verbatim merchant name, holder → DS routing, exact card-title resolution, `Processed=true` default, leaving non-policy fields alone — so cooperation is "build the JSON, hand it off".

Invocation:

```sh
echo '<JSON-spec>' | uv run scripts/python/add-transaction/cli.py
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
  "multiplier": "×0",
  "transactions": [
    { "date": "2026-05-13", "name": "TMN 7-11 BANGKOK TH", "amount": 89.0, "note": "optional", "multiplier": "×2" }
  ]
}
```

**`bill_cycle` and `due_date` are optional.** Omit them and the CLI infers both from the card's bank pattern (see [[../../../docs/concepts/bill-cycle-patterns|bill-cycle-patterns]]): today is compared against this month's bill cycle date for the card, and the active cycle is this-month-or-next accordingly. Pass them explicitly only when the user is back-filling an older cycle (e.g. transactions that posted late to a closed statement). They're "both or neither" — supplying only one is a spec error.

`multiplier` is optional. At top level it applies to every transaction in the batch; per-transaction it overrides the batch default. Valid values: `"×0"`, `"×2"`, `"×3"` (Takumi only), `"×4"`, `"×5"`, `"÷4"`. **At most one** multiplier checkbox is set per page — that's a hard rule on the Notion side; if you tried to set two, the formulas would double-count. Omitting `multiplier` leaves all checkboxes false, which Notion's formula treats as **×1** (the default earning rate).

Output: a JSON envelope `{holder, card, card_page_id, bill_cycle, due_date, processed, count, created: [{id, url, name, amount, date}, ...]}`. Surface the count + a compact list back to the user. Don't dump full URLs unless asked.

**Rollback** (cleanup or mistakes): `uv run scripts/python/add-transaction/archive.py --ids <page-id>[,<page-id>...]`. Archiving is idempotent.

## What the user supplies

1. **Cardholder** — one of `Takumi` (เว็บ) / `Baiboon` (ใบบุญ) / `Nuta` (นุตา). Determines which Transactions DB you write to and which Cards DB you query for the relation.
2. **Card name** — e.g. `First Choice`, `UOB World`. Must match an existing row in that holder's Cards DB by `Name`.
3. **Billing window for the batch** — `Bill Cycle Date` and `Due Date`, both single ISO dates, applied uniformly to every transaction in the batch unless the user splits the batch. Almost always **leave these out of the spec**: the CLI infers them from the card's bank pattern using today's date (see [[../../../docs/concepts/bill-cycle-patterns|bill-cycle-patterns]] for the per-issuer rules and the cut-off behaviour). Supply them explicitly only when back-filling a closed cycle or when the user names a non-default cycle. The two dates **must be consistent for the same card** — a bill cycle has exactly one due date on each card, set by the bank. If the user gives you a `bill_cycle` you've already seen paired with a different `due_date` on the same card, stop and confirm before writing.
4. **The transaction list** — one or more entries, each carrying:
   - **Transaction date** (`Transaction Datetime`) — ISO date.
   - **Merchant string** — the *full*, *verbatim* merchant name as supplied.
   - **Amount in baht** (`ยอดชำระ`).
   - Optional **Note**.
5. **Point multiplier** (optional) — see `multiplier` in the JSON spec above. For cards that **never** earn points (e.g. UOB One), the user expects `×0` set on every transaction; ask once per session and then apply for the whole batch.

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

### 4a. Multipliers are mutually exclusive

Only **one** of `×0` / `×2` / `×3` / `×4` / `×5` / `÷4` can be checked per transaction page. If a card's policy says it always earns at a particular tier (e.g. UOB One = `×0`), pass `multiplier` once at the batch level and the CLI applies it to every entry. A page with **no** multiplier checkbox set is treated as `×1` (default earning) by Notion's `คะแนนที่ได้จริง` formula — never set `×1` manually because that field does not exist.

### 4b. Cashback rate (`% cb`) on Baiboon's and Nuta's transactions

Baiboon's and Nuta's Transactions DSes both have a `% cb` field (number, percent display); Takumi's does not. The CLI accepts `cashback_percent` at batch and per-tx level; the value is the **raw fraction** (e.g. `0.05` for 5%). For Takumi, omit it — the field doesn't exist and the validator rejects the spec to prevent a 400 from Notion.

When the user supplies tier rules per card (see *Card-specific earning policies* below), classify each transaction's merchant against the tier table and pass the resulting `cashback_percent` per tx. Don't ask the user to compute the fraction — apply the policy yourself, but surface ambiguity (e.g. an aggregator merchant that could bundle several tiers).

**Zero-cashback rows: leave `% cb` unset.** When the tier classification yields 0% (a row that earns no cashback under the card's policy), **omit** `cashback_percent` entirely rather than passing `0`. The Notion field stays empty, which is how the user wants ineligible rows represented. Only pass a numeric `cashback_percent` when the row actually earns something.

### 4c. Note explains exclusion reasons

If a transaction earns **no** cashback / points for a reason that is **not** the card's default policy, write the reason into `Note`. Examples that need a Note:

- A foreign merchant (country suffix like `US`, `USA`, `JP`, `SG` in the merchant string) charged in THB → `"Foreign merchant (<country>) charged in THB — no points/cashback on Thai-issued cards."`
- A UOB-card petrol-station charge → `"Petrol station — UOB cards earn no points/cashback at fuel merchants."`

Examples that **don't** need a Note:

- A UOB One transaction at `×0` — that's the card's default policy, already obvious from the card relation.
- A UOB One transaction at 1% cashback (the "everything else" tier) — that's normal tiering, not an exclusion.
- A Nuta UOB One `TMN 7-11` row at 1% (not 5%) — the cashback tier table already documents that `TMN 7-11` is the "else" tier; no per-row Note required.

The Note exists so a future reviewer of the transactions can immediately see *why* a row diverges from the card's normal earning rate without having to consult the card's policy doc.

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
- `ใช้คะแนน` — points-redemption is rare and explicit.
- Takumi-only `หมวดหมู่` (category) relation.

Point-multiplier checkboxes (`×0` `×2` `×4` `×5` `÷4`, plus Takumi-only `×3`) are set explicitly via the spec's `multiplier` field — see *Rule 4a* and the card-specific policies below.

**`% cb`** (Baiboon + Nuta) is a writable `number` property displayed as a percent — storage is the raw fraction, so `0.05` shows as `5%` in the Notion UI. The CLI accepts it as `cashback_percent` at batch level or per-tx. **`cashback`** (Baiboon + Nuta) is a read-only formula = `% cb` × `ยอดชำระ` — never write to it. Takumi's DS has neither.

## Card-specific earning policies

When the user gives you a card name, apply that card's known policy before sending the spec. Ask once if the user hasn't already confirmed it for the session.

### UOB One

- **Points**: this card **does not earn points**. Always pass `"multiplier": "×0"` at the batch level. No exceptions — if the user lists a transaction that looks like it "should" earn points, it still doesn't on UOB One.
- **Cashback tiers** (the `cashback` formula reads from the card and the merchant string; we don't write a `% cb` field — Notion does):
  - **10%** on BTS / MRT / AMZ merchants.
  - **5%** on 7-11 (**but not** `TMN 7-11` — that's a TrueMoney top-up at 7-Eleven, treated separately), WATSON, and GRAB *from Thailand only* (`WWW.GRAB.COM` and `GRABTAXI`).
  - **1%** on everything else.
- Subject to the [general earning exclusions](#general-earning-exclusions) below.

When in doubt about whether a particular merchant string falls into a tier, leave the spec as-is and surface the ambiguity to the user — don't try to re-classify by editing the merchant name (that would violate Rule 1).

### CardX JCB

- **Cashback**:
  - **3%** on **in-store** transactions billed in the **local currency** of **Japan, South Korea, Hong Kong, Singapore, or Taiwan** (e.g. a JPY purchase at a Tokyo shop, a HKD purchase in Hong Kong). Online purchases are excluded; assume in-store unless the merchant string clearly indicates online (`HTTPS://…`, `*.COM`, etc.).
  - **No cashback** everywhere else — including domestic Thai (`… BANGKOK TH`), foreign merchants billed in THB, and any of the five eligible countries when the bill is in THB instead of local currency.
- **Points**: no special multiplier; default earning (no `multiplier` field set).
- Pass `cashback_percent: 0.03` for eligible rows; **omit** `cashback_percent` entirely for ineligible ones (see Rule 4b on leaving 0% rows unset).

## General earning exclusions

These apply across **every** card we manage (Takumi, Baiboon, Nuta) unless a card's own page documents an exception:

1. **Foreign merchants billed in THB earn neither points nor cashback**, even when the card would normally earn at a higher tier. Examples in the data: `X CORP. PAID FEATURES BASTROP US`, `Google YouTubePremium Mountain View USA`. Country suffix tells you the merchant is foreign even when the amount is in baht.
2. **UOB cards: petrol stations earn neither points nor cashback.** Watch for merchant strings containing PT, BCP, ESSO, SHELL, CALTEX, PTT — when in doubt, surface to the user.
3. The card-level **cashback formula** on Nuta's transactions and the **realized-points formula** on every transaction already encode these rules where they can; but the formulas can't tell "foreign-merchant-in-THB" apart from a regular domestic THB charge, so a separate flag may be needed in future — for now, just **be aware** that the computed cashback/points on such transactions may overstate reality. Flag it when the user asks for a cashback total.

### A note on Notion percentage fields

Notion's `number` property type with a "percent" format displays as `1%` while the underlying stored value is `0.01`. If you ever read a `% cb` value via the API and want to render it, multiply by 100. When writing via the API, pass the raw fraction (`0.01`), not `1`. We don't currently write percentage fields directly — this caveat is documented so future formula work doesn't trip on it.

## Procedure

1. **Confirm holder and parse the batch.** If the holder is ambiguous from context, ask.
2. **Build the JSON spec** described in *Primary execution path*. Every amount the user listed becomes its own entry in `transactions`, even when the merchant string repeats across amounts.
3. **Run the script.** Pipe the JSON in, read the JSON envelope back.
4. **Report back** with the count, the merchant/amount/date list, and the card. Don't dump every Notion URL unless asked.
5. **MCP fallback** — only if the script isn't available (e.g. wrong repo): use one `mcp__notion__notion-create-pages` call with `parent: { type: "data_source_id", data_source_id: "<holder transactions DS>" }` and the same property mapping below.

## After writing

If anything in the API response looks off (a `Card` field that didn't resolve, a missing amount, a date that came back unset), surface it immediately and offer to retry the affected pages.

## What this skill does NOT do

- Does **not** edit existing transactions. For property patches on already-created rows (filling `% cb` after tier classification, adding a `Note`, fixing a missed multiplier), use [[../update-transaction/SKILL.md|/update-transaction]].
- Does **not** create bills (`บิลเรียกเก็บค่าบัตรเครดิต`). Bills are separate DBs and out of scope.
- Does **not** add cards. The card must already exist in the holder's Cards DB.
- Does **not** translate Thai labels. Property names stay verbatim in code-spans, per project doc conventions.
