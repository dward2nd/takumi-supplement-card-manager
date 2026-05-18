# `scripts/python/` — uv-based Notion scripts

Runtime: **uv** (latest stable) managing a modern stable Python (3.12+ at time of writing). One shared `pyproject.toml` for every script here.

## First-time setup

When you're about to write the first Python script:

```sh
cd scripts/python
uv init --no-readme
uv add notion-client       # official Notion Python SDK
```

That produces:

```
scripts/python/
├── pyproject.toml
├── uv.lock              # commit this
├── .python-version      # in .gitignore
├── _notion_client.py    # thin wrapper around notion-client
└── <your_script>.py
```

## Conventions

- Every script is a single `.py` file. Helpers are prefixed with `_` (e.g. `_notion_client.py`).
- Top of each script:
  ```python
  """<one-line description>

  deterministic + idempotent — safe to re-run.
  """
  ```
- Notion access goes through `_notion_client.py` — don't instantiate `notion_client.Client` inline.
- Read the integration token from `os.environ["NOTION_TOKEN"]`. Never hardcode it. Never commit it.
- Run with `uv run <script>.py`.

## Why uv

The user prefers uv for Python dependency management. Don't substitute pip, poetry, pipenv, or conda without explicit instruction.
