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

## Primary tool: Notion MCP

All data lives in Notion. Access it through the `mcp__notion__*` tool family — `mcp__notion__notion-fetch` for reads, `mcp__notion__notion-search` to discover, plus the page/update/create variants when modification is explicitly authorised.

The Notion MCP server is configured in `.mcp.json` (HTTP transport to `https://mcp.notion.com/mcp`).

### The eight databases

All under parent page **Personal Monetary Policy** (`b1989406427a4fb7b4c5ec1805bdbed8`):

| Owner   | Role         | Collection ID                              |
|---------|--------------|--------------------------------------------|
| Takumi  | Cards        | `1aacb755-f0f1-818a-a284-000b17d155de`     |
| Takumi  | Transactions | `1aacb755-f0f1-81dc-8e9f-000b20891025`     |
| Baiboon | Cards        | `99bb5ba6-79b1-47e2-9b8f-fa3102d5b294`     |
| Baiboon | Transactions | `181cb755-f0f1-8167-b5b6-000bc6d47469`     |
| Baiboon | Bills        | `192cb755-f0f1-8064-9075-000be05ba72d`     |
| Nuta    | Cards        | `2a1cb755-f0f1-8188-9b00-000b5fa448b8`     |
| Nuta    | Transactions | `2a1cb755-f0f1-8110-9795-000bf7d48b4f`     |
| Nuta    | Bills        | `2a1cb755-f0f1-8193-982d-000bd4e3156c`     |

Pass any collection ID to `mcp__notion__notion-fetch` as `id: "collection://<uuid>"`, or use the original notion.so URL.

Notable schema quirks worth knowing before you touch the data:

- Takumi has **no Bills database** — only Baiboon and Nuta do.
- Bills' `Card` field is a **SELECT (text)**, not a relation to the Cards DB. Deliberate denormalization. Don't try to "fix" it in Notion; document it.
- Nuta uniquely has `% cb` (writable `number`, percent display — raw fraction in storage so `0.05` shows as `5%`) and `cashback` (read-only formula = `% cb` × `ยอดชำระ`) on transactions.
- Takumi's transactions uniquely include a `หมวดหมู่` (category) relation and a `×3` multiplier checkbox.

Full schema is documented in `docs/databases/`.

## Repo layout

```
.
├── .mcp.json                # Notion HTTP MCP server config
├── CLAUDE.md                # this file
├── README.md
├── docs/                    # Obsidian-native knowledge vault (open this folder as a vault)
│   ├── index.md             # MOC / entry point
│   ├── people/              # one note per cardholder
│   ├── databases/           # one note per Notion database (8)
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
- **Notion is the source of truth**. When a question arises about a specific card, transaction, or bill, read Notion via MCP first. The vault describes structure; Notion holds data.
- **The vault is persistent memory**. When the user describes a new pattern or rule, **update `docs/` rather than only answering inline**.
- **Wikilinks everywhere**. The Obsidian graph is the navigation layer.
- **Don't mutate Notion** without explicit instruction. Reads via MCP are free; writes require asking.
- **Don't translate Thai labels**, don't rename `ยอดค้างชำระ` → `outstanding_balance`. The future app's data model can rename; the vault cannot.

## What NOT to do

- Don't add `package.json`/`pyproject.toml`/`tsconfig.json`/`requirements.txt` at the repo root. (Inside `scripts/typescript/` or `scripts/python/` is fine.)
- Don't introduce a build system or framework at root.
- Stack decisions are captured in `docs/future-app/product-shape.md` (Rust backend + JS/TS PWA frontend, self-hosted on a VPS, minimal setup for ~3 users). Other docs — `docs/concepts/`, `docs/databases/`, `docs/formulas/`, `docs/people/` — stay framework-agnostic: they describe the Notion-as-built world and the abstract phase-2 shape, not the implementation.
- Don't "fix" the Bills SELECT-vs-relation divergence in Notion. Document it in `docs/concepts/known-divergences.md`.
- Don't generate one-note-per-card upfront. Promote a card from `docs/cards/_stubs.md` to its own note only when you and the user have discussed that card's specific rules.
