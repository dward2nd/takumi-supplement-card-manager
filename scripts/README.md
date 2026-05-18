# `scripts/` — sandboxed Notion automation

A holding pen for **reusable, deterministic, idempotent** unit tasks that operate against the Notion HTTP API. Agent-callable. No business logic that belongs in the future app.

## Layout

Organised **by language**, not by script name. One shared manifest per language.

```
scripts/
├── typescript/      # Bun runtime
│   ├── README.md
│   └── (package.json appears after `bun init -y`)
└── python/          # uv runtime
    ├── README.md
    └── (pyproject.toml + uv.lock appear after `uv init`)
```

## Rules

1. **No dependency manifests at the repo root.** All `package.json` / `pyproject.toml` / lockfiles live inside `scripts/typescript/` or `scripts/python/` respectively.
2. **One manifest per language**, shared across every script in that language. Don't create per-script folders or per-script `package.json`s.
3. **Init lazily.** Run `bun init -y` (TypeScript) or `uv init` (Python) only when you're about to write the first script in that language. Don't pre-init empty manifests.
4. **Scripts call the Notion HTTP API directly.** The Notion MCP server is a Claude-side integration — it isn't importable by standalone scripts. Use Notion's REST endpoints with a personal integration token (read via env var, never committed).
5. **Isolate Notion access** in one client file per language: `scripts/typescript/_notion-client.ts`, `scripts/python/_notion_client.py`. Phase-2 migration replaces just this file.
6. **Header every script** with one line stating what it does, plus an explicit `deterministic + idempotent` marker.

## Why this shape

The repo is stack-agnostic until phase 2 begins. Putting dep manifests at the root would prematurely commit the project to a runtime. Organising scripts by language (not by name) keeps the sandbox flat — these are unit tasks, usually one file each, and they don't deserve ceremonial folders.

See `CLAUDE.md` (root) and `docs/index.md` for project context.
