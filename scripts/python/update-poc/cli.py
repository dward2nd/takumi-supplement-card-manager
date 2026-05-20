#!/usr/bin/env python3
"""update-poc — enumerate "potentially significant" project changes
since the last commit that touched poc/.

deterministic + idempotent: read-only `git log` queries. The script
never writes to poc/ — that's the skill body's job. Its only output
is a list of files for the agent to inspect.

Full flow on `uv run scripts/python/update-poc/cli.py`:

  1. `git log -1 --format=%H -- poc` → the most recent commit that
     touched poc/. Call this `since`.
  2. `git log <since>..HEAD --name-status --format='__commit__ %H %s'
     -- <watched-paths>` → which watched files changed in which commit.
  3. Deduplicate by path (keeping the newest commit's status/subject)
     and emit a JSON envelope.

`since` may be `null` when poc/ has no commits yet. In that case the
envelope advises the user to commit the current POC state first.

Watched paths — changes here may justify a POC update:

  - docs/future-app/
  - docs/databases/
  - docs/concepts/
  - docs/formulas/
  - docs/people/
  - CLAUDE.md
  - .mcp.json

Override the list with --path (repeatable) if a non-standard sweep is
needed (e.g. inspecting docs/cards/ after a card-by-card promotion).

Output: JSON envelope on stdout — see `run()` for the schema.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import paths  # noqa: E402

DEFAULT_WATCHED: list[str] = [
    "docs/future-app",
    "docs/databases",
    "docs/concepts",
    "docs/formulas",
    "docs/people",
    "CLAUDE.md",
    ".mcp.json",
]

POC_PATH = "poc"


def _git(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=paths.REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return (proc.stdout or "").rstrip("\n")


def _last_poc_commit() -> str | None:
    out = _git(["log", "-1", "--format=%H", "--", POC_PATH])
    return out or None


def _changed_files(since: str, watched: list[str]) -> list[dict]:
    raw = _git(
        [
            "log",
            f"{since}..HEAD",
            "--name-status",
            "--format=__commit__ %H %s",
            "--",
            *watched,
        ]
    )
    if not raw:
        return []

    files: dict[str, dict] = {}
    current_hash: str | None = None
    current_subject: str | None = None

    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("__commit__ "):
            rest = line.removeprefix("__commit__ ")
            parts = rest.split(" ", 1)
            current_hash = parts[0]
            current_subject = parts[1] if len(parts) > 1 else ""
            continue
        if "\t" not in line:
            continue
        status, _, payload = line.partition("\t")
        # Rename/copy lines look like `R100\told\tnew` — the post-rename path is what matters.
        path = payload.split("\t")[-1]
        # git log is newest-first; keep only the first (newest) entry per path.
        files.setdefault(
            path,
            {
                "path": path,
                "status": status,
                "last_commit": current_hash,
                "last_subject": current_subject,
            },
        )

    return sorted(files.values(), key=lambda r: r["path"])


def run(*, watched: list[str]) -> dict:
    since = _last_poc_commit()
    poc_dir_exists = (paths.REPO_ROOT / POC_PATH).is_dir()

    if since is None:
        return {
            "since_commit": None,
            "poc_dir_exists": poc_dir_exists,
            "watched_paths": watched,
            "change_count": 0,
            "changes": [],
            "note": (
                "No prior commit touches `poc/`. Commit the current POC state first, "
                "then re-run `/update-poc` to compute deltas."
            ),
        }

    changes = _changed_files(since, watched)
    return {
        "since_commit": since,
        "poc_dir_exists": poc_dir_exists,
        "watched_paths": watched,
        "change_count": len(changes),
        "changes": changes,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--path",
        action="append",
        help=(
            "Override watched paths. Repeatable. Defaults to "
            f"{DEFAULT_WATCHED}."
        ),
    )
    args = ap.parse_args(argv)
    watched = args.path if args.path else list(DEFAULT_WATCHED)
    out = run(watched=watched)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
