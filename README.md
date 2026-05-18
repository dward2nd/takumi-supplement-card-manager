# takumi-supplement-card-manager

A research repo documenting Takumi's Notion-based system for managing **supplement credit cards** issued to two friends — **Baiboon** (ใบบุญ) and **Nuta** (นุตา) — who share Takumi's credit limit.

This is **phase 1: observation only**. No software is being built here yet. The deliverables are:

- An Obsidian-native knowledge vault at [`docs/`](docs/index.md) that captures the schema, relations, formulas, and patterns of the live Notion workspace.
- A sandbox at [`scripts/`](scripts/README.md) for small, deterministic Notion automations (Bun for TypeScript, uv for Python).
- Guidance for future Claude Code instances in [`CLAUDE.md`](CLAUDE.md).

Phase 2 will be a custom full-stack application that **replaces Notion entirely**. Its data model is being shaped in `docs/future-app/` without committing to a particular tech stack.

## Cardholders

| Person  | Notion name | Role             |
|---------|-------------|------------------|
| Takumi  | เว็บ          | Primary cardholder |
| Baiboon | ใบบุญ        | Supplement holder  |
| Nuta    | นุตา          | Supplement holder  |

## How to use this repo

- **Read it as an Obsidian vault**: open the `docs/` folder in Obsidian. The graph view is the navigation; start from `docs/index.md`.
- **Run Notion operations through MCP**: `.mcp.json` wires the Notion HTTP MCP server. Use Claude Code with `mcp__notion__*` tools.
- **Don't run anything at the repo root**: this is not a runnable application.

## Documentation language

English narrative; Thai field names and Notion page titles are preserved verbatim (e.g. `ยอดชำระ`, `รายการใช้จ่ายผ่านบัตรของใบบุญ`) and glossed in English on first use within each note.
