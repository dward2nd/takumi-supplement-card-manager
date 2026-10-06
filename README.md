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
- **Run Notion operations through `scripts/python`**: the uv-managed CLIs in `scripts/python/` talk to the Notion HTTP API and are the supported path for every read and write. (`.mcp.json` still wires a Notion MCP server, but it's deprecated — don't use it.)
- **Don't run anything at the repo root**: this is not a runnable application.

## Running Claude Code in the cloud

Claude Code on the web (claude.ai/code) works on a fresh clone in a Linux container, so the gitignored secrets aren't there. Set them as environment variables in the cloud environment's settings (the environment menu in the session's title bar, then **Edit**):

| Variable | Value | Replaces |
|---|---|---|
| `NOTION_TOKEN` | the "Claude Code's Automated Scripts" integration token | `.env` |
| `STATEMENT_PASSWORDS_YAML` | `statement-passwords.yaml` as one line of YAML, e.g. `{issuers: {Krungsri: "DDMonYYYY", ttb: "DDMonYYYY"}}` | `scripts/repositories/statement-passwords.yaml` |

A new session picks them up. The repo's SessionStart hook (`scripts/install_pkgs.sh`) installs the Python dependencies and reports any missing variable.

The default network policy blocks the bank and merchant sites and Wikimedia Commons, which `/write-catalogue` needs. To research catalogues in the cloud, widen *Network access* in the same settings. Work done in the cloud lands on a `claude/…` branch; merge it into `main` by pull request. The full list of differences is in [`CLAUDE.md`](CLAUDE.md#cloud-sessions-claude-code-on-the-web).

## Documentation language

English narrative; Thai field names and Notion page titles are preserved verbatim (e.g. `ยอดชำระ`, `รายการใช้จ่ายผ่านบัตรของใบบุญ`) and glossed in English on first use within each note.
