# `scripts/typescript/` — Bun-based Notion scripts

Runtime: **Bun** (latest stable). One shared `package.json` for every script here.

## First-time setup

When you're about to write the first TypeScript script:

```sh
cd scripts/typescript
bun init -y
bun add @notionhq/client     # official Notion JS SDK
```

That produces:

```
scripts/typescript/
├── package.json
├── bun.lock           # commit this
├── tsconfig.json
├── _notion-client.ts  # thin wrapper around @notionhq/client
└── <your-script>.ts
```

## Conventions

- Every script is a single `.ts` file. If it needs helpers, name them `_<helper>.ts` (underscore prefix marks "not directly runnable").
- Top of each script:
  ```ts
  // <one-line description>
  // deterministic + idempotent — safe to re-run
  ```
- Notion access goes through `_notion-client.ts` — never instantiate `@notionhq/client` inline.
- Read the integration token from `process.env.NOTION_TOKEN`. Never hardcode it. Never commit it.
- Run with `bun run <script>.ts`.

## Why Bun

The user prefers Bun for TypeScript work. Don't substitute Node, ts-node, deno, or pnpm without explicit instruction.
