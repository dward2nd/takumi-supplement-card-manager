# `scripts/python/` — uv-based automation sandbox

Runtime: **uv** (latest stable) managing a modern stable Python. One shared `pyproject.toml` and `uv.lock` for every script here.

Most scripts target Notion (the project's current source of truth), but anything deterministic and reusable can live here — `release/` is an example that touches git instead.

## Layout

```
scripts/python/
├── pyproject.toml
├── uv.lock                          # commit this
├── .python-version                  # in .gitignore
├── .venv/                           # in .gitignore
├── lib/                             # shared code — imported by every CLI
│   ├── paths.py                     # REPO_ROOT, ENV_FILE, VERSION_FILE — repo-relative anchors
│   ├── notion_client.py             # the single point of Notion HTTP access
│   ├── holders.py                   # PrimaryHolder (Takumi) / SupplementHolder (Baiboon, Nuta) + DS routing
│   ├── cards.py, card_repo.py       # card-page resolution; card YAML (data only)
│   ├── ledger.py                    # a cycle's rows, amount due, payment / cashback row tests
│   ├── transaction_read.py / _write.py
│   ├── promotions.py                # promotion YAML + merchant heuristics + classify() (delegates to earning)
│   ├── earning/                     # Card, one class per card family (UOBCard, KrungsriFamilyCard, AEONCard …)
│   ├── bill_cycle.py                # BillCycle, one class per issuer's cycle rule
│   ├── crediting/                   # Crediting, one class per card that gets credit rows (UOBOneCrediting)
│   ├── points_account.py            # PointsAccount (pooled / principal card / supplement card) + PointsPeriod (posting / cycle)
│   ├── rewards_audit.py, points_balance.py  # statement points vs ledgers; balance rows to the printed figure
│   ├── icons/                       # page icons for new rows (create_page asks here); backfill for old ones
│   ├── bureau/                      # Promotion Bureau: payout shapes (ladder, credit cap, points, instant discount) + campaigns;
│   │                                #   runner = one row's sync, follow = re-sync after a ledger write,
│   │                                #   quota = a bank's nationwide pool (UnionPay's offer page)
│   └── statements/                  # StatementParser, one class per issuer; attribution; recording
└── <skill-name>/                    # one folder per skill, dir name = skill name
    ├── __init__.py
    ├── cli.py                       # entry point (stdin/stdout JSON)
    └── ...                          # additional files as the skill grows
```

**One class per case** (user, 2026-09-28): where banks, cards, issuers or campaigns differ, the difference is a subclass of an abstract base, not a flag on a shared function. Data that's genuinely data (tier lists, statement numbers, IDs) stays in YAML.

Why this shape: skills can be flexible (the agent calls them), but scripts must be **deterministic** and **reusable**. Putting one folder per skill lets a skill split its logic across files without exploding the sandbox, while `lib/` keeps Notion access — the thing most likely to change when phase 2 begins — isolated to one file.

## Design principles

These shape every script under this directory:

1. **Reusability over copy-paste.** Anything two skills could share goes in `lib/`. A skill folder should never reimplement holder routing, card lookup, or Notion HTTP — it imports them.
2. **Maintainability through modularity.** Each skill folder may (and should) split into focused files — `cli.py`, `filters.py`, `validation.py`, `archive.py`, etc. — instead of one growing monolith. The goal is that a reviewer can read one short file in isolation and understand it. If `cli.py` starts past a handful of clearly-named functions, extract.
3. **Keep small-scale ergonomics.** Modularity is for the implementer; the caller should still see a one-liner — JSON in on stdin, JSON envelope out on stdout. Don't introduce subcommands, multi-step workflows, or required config files when a single pipe still works.
4. **Determinism + idempotence are the default.** When a script is not safe to re-run (the `add-` writer creates new pages on each call), say so explicitly in the file header. Every other script must be safe to invoke twice.

## Conventions

- Every script header starts with: a one-line description and the marker `deterministic + idempotent — safe to re-run.` (Or, when re-running is *not* safe, an explicit note saying so — see `add-transaction/cli.py`.)
- Notion access goes through `lib/notion_client.py`. Don't instantiate `notion_client.Client` inline anywhere else.
- The integration token is read from `NOTION_TOKEN` (loaded from the repo-root `.env` automatically). Never hardcode it. Never commit it.
- CLIs take a JSON spec on **stdin** (or via `--input <file>`) and write a JSON envelope to **stdout**. This makes them composable from Claude, from shell, or from a future application. (A tiny script with a single argument may use a positional CLI arg instead — see `release/cli.py`. Pick whichever is more ergonomic for the *caller*.)
- Thai property names stay verbatim in code (`"ยอดชำระ"`, `"ชำระแล้ว"`, etc.). Project rule.
- Hyphenated folder names match skill names. CLIs use `sys.path.insert` to import `lib`, so the parent dir doesn't need to be a Python package.

## Running

```sh
# From any directory:
echo '{"holder":"nuta","card":"First Choice","limit":5}' \
  | uv run --project scripts/python scripts/python/fetch-transactions/cli.py

# From scripts/python/:
echo '{"holder":"nuta","card":"First Choice","limit":5}' \
  | uv run fetch-transactions/cli.py
```

## Current scripts

| Skill | Entry point | Reads | Writes |
|---|---|---|---|
| `fetch-transactions` | `fetch-transactions/cli.py` | filter spec on stdin | JSON results to stdout |
| `add-transaction` | `add-transaction/cli.py` | write spec on stdin | created-page envelope to stdout |
| `add-transaction` (rollback) | `add-transaction/archive.py` | page IDs via `--ids` or stdin | archive confirmations |
| `release` | `release/cli.py` | positional `type` arg (`major\|minor\|patch`) | bumps VERSION, commits, tags, pushes; JSON envelope to stdout |

## Why uv

The user prefers uv for Python dependency management. Don't substitute pip, poetry, pipenv, or conda without explicit instruction.
