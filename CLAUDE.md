# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This repo is **phase 1: observation & research**. There is no application source code, no build system, and no runnable program. Do **not** scaffold any framework at the repo root — no `npm init`, no `pip install` at root, no `package.json`/`requirements.txt`/`tsconfig.json` at the repo root.

The point of this phase is to document Takumi's existing Notion-based system for managing supplement credit cards so that, when phase 2 begins, the target data model and behavioural rules are already well-specified. Phase 2 will be a custom full-stack application that **replaces Notion entirely** as the system of record.

**Canonical phase-2 spec**: [`docs/future-app/product-shape.md`](docs/future-app/product-shape.md). Pinned 2026-05-21 from a structured interview — covers users/roles, platform, entry flow, data-model decisions, rewards, categories, bills, notifications, migration, privacy, auth, audit log, theming, recurring transactions, and tech constraints. Every other doc in `docs/future-app/` and `docs/concepts/` cross-references it; treat it as the source of truth when reconciling.

## The three cardholders

Takumi (referred to in Notion as **เว็บ**) is the primary holder on several Thai credit cards and issues supplement cards from those accounts to two friends:

- **Baiboon** (ใบบุญ) — supplement holder
- **Nuta** (นุตา) — supplement holder

Both friends spend on credit that legally belongs to Takumi. The Notion structure exists to give each friend a transparent, auditable record of their own activity without exposing the others' data.

```
              Takumi (primary)
                    │
        ┌───────────┴───────────┐
     supplement              supplement
     cards on               cards on
     Takumi's               Takumi's
     accounts               accounts
        │                       │
     Baiboon                  Nuta
```

## Primary tool: the Notion HTTP API via `scripts/python`

All data lives in Notion. **Reach it through `scripts/python`, never through the Notion MCP server.** The scripts are the supported path: they carry the holder routing, card resolution, Thai property names, and write validation that ad-hoc MCP calls skip.

```sh
echo '{"holder":"takumi","limit":5,"sort":"date_desc"}' \
  | uv run --project scripts/python scripts/python/fetch-transactions/cli.py
```

Start from an existing skill (`/fetch-transactions`, `/summarize-overview`, `/add-transaction`, …). For a one-off read with no skill behind it, write a throwaway script in the scratchpad that imports `lib.notion_client` — still the HTTP API, still `lib/`. If a read is worth repeating, propose promoting it to a skill rather than leaving it ad-hoc.

`mcp__notion__*` is deprecated in this repo. `.mcp.json` still configures the server, but don't call it.

### Integration access

The scripts authenticate as the Notion integration **"Claude Code's Automated Scripts"** with `NOTION_TOKEN` from the repo-root `.env`. A database invisible to that integration returns `ObjectNotFound` on query, and — more quietly — **relations pointing into it read back as an empty array**, which looks like unset data rather than an access error.

All fourteen databases are shared as of 2026-09-30 (Takumi's Bills DB joined 2026-09-27; the Promotion Bureau and the three cashback trackers 2026-09-28; Promotion Catalogues 2026-09-30). If a relation ever comes back empty across a whole table, suspect this before suspecting the data — that was the symptom while Takumi's Cards DS was still unshared. Confirm what the token can see with `client.search(filter={"property": "object", "value": "data_source"})`.

### The fourteen databases

All under parent page **Personal Monetary Policy** (`b1989406427a4fb7b4c5ec1805bdbed8`):

| Owner   | Role         | Collection ID                              |
|---------|--------------|--------------------------------------------|
| Takumi  | Cards        | `1aacb755-f0f1-818a-a284-000b17d155de`     |
| Takumi  | Transactions | `1aacb755-f0f1-81dc-8e9f-000b20891025`     |
| Takumi  | Bills        | `63dcb755-f0f1-83df-aaa8-871bb9069dae`     |
| Baiboon | Cards        | `99bb5ba6-79b1-47e2-9b8f-fa3102d5b294`     |
| Baiboon | Transactions | `181cb755-f0f1-8167-b5b6-000bc6d47469`     |
| Baiboon | Bills        | `192cb755-f0f1-8064-9075-000be05ba72d`     |
| Nuta    | Cards        | `2a1cb755-f0f1-8188-9b00-000b5fa448b8`     |
| Nuta    | Transactions | `2a1cb755-f0f1-8110-9795-000bf7d48b4f`     |
| Nuta    | Bills        | `2a1cb755-f0f1-8193-982d-000bd4e3156c`     |
| Takumi  | Cashback tracker | `96bcb755-f0f1-83ef-a5b9-079f9ba3ae98` |
| Baiboon | Cashback tracker | `374cb755-f0f1-80b2-97cc-000b0105e43e` |
| Nuta    | Cashback tracker | `2e4cb755-f0f1-838a-9317-877c67577916` |
| (all)   | Promotion Bureau | `3e7cb755-f0f1-80f0-8c78-000b1d9f44cb` |
| (all)   | Promotion Catalogues | `3ebcb755-f0f1-80d5-a580-000bf9448d23` |

These IDs are data source IDs for the 2025-09-03 API: `GET /v1/data_sources/{id}` for the schema (formula bodies included, inline as `expression`), `POST /v1/data_sources/{id}/query` for rows. `lib/holders.py` mirrors this table — edit both together.

Notable schema quirks worth knowing before you touch the data:

- Takumi's Bills DB (added 2026-09-27) is **statement-driven**: each row is the bank's per-card total — principal plus every supplement section — not a sum of his own rows. Takumi is a `PrimaryHolder` (`lib/holders.py`, `statement_bills = True`), which makes automatic payment rows refuse him. `/prepare-bill` drafts his bills differently: since 2026-10-06 it estimates them from all three ledgers plus any unmonitored supplement's total. `/update-bill`'s refresh re-estimates a `[DRAFT]` the same way, and `/record-statement` completes the draft with the printed total. See `docs/databases/takumi-bills.md`.
- Bills' `Card` field is a **one-way relation** to the holder's own Cards DB (since 2026-09-30, at the user's request; it was a SELECT). The old SELECT is kept as `Card (old select)` until the household's views move over. Scripts ignore it. `lib/bills.py` (`find_bill`, `card_relation`, `bill_card_id`) is the one place bill↔card matching lives.
- All three Transactions DSes have `% cb` (writable `number`, percent display — raw fraction in storage so `0.05` shows as `5%`) and `cashback` (read-only formula = `% cb` × `ยอดชำระ`). Takumi's were added 2026-09-28, copied from Baiboon's; his cashback figures only exist on rows from then on (first: AEON Rabbit).
- Takumi's transactions uniquely include a `หมวดหมู่` (category) relation and a `×3` multiplier checkbox.
- Every Cards DS has `คะแนนต่อ 1 หน่วย` (points per unit, empty = 1) and every Transactions DS a `×6` box (2026-10-05): the points formula multiplies by the per-unit figure after its floors, so Lotus's Beyond (0.25) earns fractional coins. See `docs/cards/lotuss-beyond.md`.
- The **Promotion Bureau** (2026-09-28) pools campaigns that pay on the primary account's combined spend (NW3, UOB One's caps, UOB World ×5, EPW538): one row per **quota period** (`<year>M<month> — …`), two-way linked to every holder's transactions (`Promotion` on the Transactions side). Each payout shape is a class (`LadderPromotion`, `CreditCapPromotion`, …) and each campaign subclasses one in `scripts/python/lib/bureau/`, not YAML: bank terms don't share a shape. The credit is split **first come, first served** by `Transaction Datetime`. `/sync-promotion` drives it. `/add-transaction`, `/update-transaction` and `/record-statement` also re-sync the Bureau rows their rows touch after every write (`lib.bureau.follow`, 2026-09-28), and set linked rows' `% cb` / multiplier to the split. They never create a Bureau row. See `docs/concepts/promotion-bureau.md`.
- **Promotion Catalogues** (2026-09-30) is reading material, not accounting: one Thai page per merchant per month (`Makro — Sep 2026`), a spending plan for the household's cards plus every promotion there, shown as a gallery with logo covers. `/write-catalogue` writes it. See `docs/databases/promotion-catalogues.md`.

Full schema is documented in `docs/databases/`.

## Repo layout

```
.
├── .mcp.json                # Notion MCP server config (deprecated — use scripts/python)
├── CLAUDE.md                # this file
├── README.md
├── docs/                    # Obsidian-native knowledge vault (open this folder as a vault)
│   ├── index.md             # MOC / entry point
│   ├── people/              # one note per cardholder
│   ├── databases/           # one note per Notion database (the three cashback trackers share one)
│   ├── concepts/            # cross-cutting concepts (multipliers, billing cycle, etc.)
│   ├── cards/               # stub list now; individual notes promoted lazily
│   ├── formulas/            # Notion formula decodings
│   └── future-app/          # phase-2 target: product-shape.md (canonical) + data-model + migration
└── scripts/                 # sandboxed deterministic automation
    ├── typescript/          # Bun runtime
    └── python/              # uv runtime
```

## Scripts sandbox

`scripts/` is allowed for **reusable, deterministic, idempotent** automation against the Notion HTTP API — the kind of unit task an agent might invoke. Organized **by language**, not by script name:

- `scripts/typescript/` — runtime: **Bun** (latest stable). One shared `package.json` for all TS scripts. Init with `bun init -y` only when the first TS script is written.
- `scripts/python/` — runtime: **uv** (latest stable, current Python). One shared `pyproject.toml` + `uv.lock`. Init with `uv init` only when the first Python script is written.

Rules:

1. **Never** place a dependency manifest at the repo root.
2. Each language folder has exactly one manifest, shared across all scripts in that language.
3. Scripts target the Notion HTTP API directly (the MCP server is a Claude-side integration, not importable by standalone scripts).
4. Isolate Notion access in one client module per language. Python: `scripts/python/lib/notion_client.py`. If TypeScript is ever introduced, mirror the pattern under `scripts/typescript/lib/`. Business logic must remain portable to the future app.
5. Mark each script's header with a one-line declaration of what it does and that it is deterministic + idempotent.

## Working conventions

- **Documentation language**: English narrative, **Thai field names preserved verbatim** in code-spans. Gloss the Thai term in English on first use per note: `` `ยอดชำระ` (amount due) ``. Never translate Thai labels away.
- **Notion is the source of truth**. When a question arises about a specific card, transaction, or bill, read Notion via `scripts/python` first. The vault describes structure; Notion holds data.
- **The vault is persistent memory**. When the user describes a new pattern or rule, **update `docs/` rather than only answering inline**.
- **Wikilinks everywhere**. The Obsidian graph is the navigation layer.
- **Don't mutate Notion** without explicit instruction. Reads are free; writes require asking.
- **Don't translate Thai labels**, don't rename `ยอดค้างชำระ` → `outstanding_balance`. The future app's data model can rename; the vault cannot.

## What NOT to do

- Don't add `package.json`/`pyproject.toml`/`tsconfig.json`/`requirements.txt` at the repo root. (Inside `scripts/typescript/` or `scripts/python/` is fine.)
- Don't introduce a build system or framework at root.
- Stack decisions are captured in `docs/future-app/product-shape.md` (Rust backend + JS/TS PWA frontend, self-hosted on a VPS, minimal setup for ~3 users). Other docs — `docs/concepts/`, `docs/databases/`, `docs/formulas/`, `docs/people/` — stay framework-agnostic: they describe the Notion-as-built world and the abstract phase-2 shape, not the implementation.
- Don't write to `Card (old select)` on the Bills DBs, and don't delete it until the user says the views have moved to the `Card` relation.
- Don't generate one-note-per-card upfront. Promote a card from `docs/cards/_stubs.md` to its own note only when you and the user have discussed that card's specific rules.
