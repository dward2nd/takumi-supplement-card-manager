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
     -- <watched-paths>` → which watched files changed in which commit
     since `since`.
  3. `git status --porcelain --untracked-files=all -- <watched-paths>`
     → working-tree changes (modified + staged + untracked) on watched
     paths. This is critical because the documented workflow is
     `/update-poc` BEFORE `/release` — the sync needs to see the work
     about to be committed, not just what's already in history.
  4. Merge: uncommitted entries override committed ones for the same
     path (working-tree status is "more recent"). Untracked entries
     surface with `last_commit: null`, `last_subject: "(uncommitted)"`.
  5. Emit a JSON envelope.

`since` may be `null` when poc/ has no commits yet. In that case the
envelope advises the user to commit the current POC state first.

Watched paths — changes here may justify a POC update:

  Documentation surfaces (narrative):
  - docs/future-app/
  - docs/databases/
  - docs/concepts/
  - docs/formulas/
  - docs/people/
  - docs/cards/
  - docs/promotions/

  Structured repositories:
  - scripts/repositories/

  Capability surfaces (new docs without narrative are still POC-relevant):
  - .claude/skills/           # new SKILL.md → new user capability the POC may need to mirror
  - scripts/python/lib/       # new lib file → new domain concept (e.g. installments.py)

  Top-level config:
  - CLAUDE.md
  - .mcp.json

A change here is *evidence* of evolution, not a verdict. The agent
triages each change by `status` (A=added → likely new capability;
M=modified → existing surface evolved) and decides whether the POC
needs to reflect it. The CLI doesn't read file contents — it just
points the agent at what moved.

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
    # Documentation surfaces — narrative drift that may reshape the UI.
    "docs/future-app",
    "docs/databases",
    "docs/concepts",
    "docs/formulas",
    "docs/people",
    "docs/cards",
    "docs/promotions",
    # Structured repositories — cards + promotions seed data the POC mirrors.
    "scripts/repositories",
    # Capability surfaces — new skills / new domain libs change what users
    # can do, even when no narrative doc was edited. Without these, the CLI
    # silently misses a session that added /add-installment + lib/installments.py
    # but didn't touch any doc.
    ".claude/skills",
    "scripts/python/lib",
    # Top-level config.
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


def _uncommitted_files(watched: list[str]) -> list[dict]:
    """Working-tree changes (modified, staged, untracked) on watched paths.

    `--untracked-files=all` expands new directories to individual files
    so a fresh skill directory shows up as `.claude/skills/<name>/SKILL.md`
    rather than just `.claude/skills/<name>/` — the triage heuristics in
    the skill body key off the SKILL.md path.
    """
    raw = _git(
        [
            "status",
            "--porcelain",
            "--untracked-files=all",
            "--",
            *watched,
        ]
    )
    if not raw:
        return []

    out: list[dict] = []
    for line in raw.splitlines():
        if not line:
            continue
        # Format: "XY <path>" where X=index status, Y=worktree status.
        # Renames look like "R  <old> -> <new>" — keep the new path.
        status_raw = line[:2]
        payload = line[3:]
        if " -> " in payload:
            payload = payload.split(" -> ", 1)[1]
        path = payload.strip()
        # Compact "M ", " M", "A ", " A" → "M" / "A"; preserve "??", "AM", "MM", etc.
        status_compact = status_raw.strip() or status_raw
        out.append(
            {
                "path": path,
                "status": status_compact,
                "last_commit": None,
                "last_subject": "(uncommitted)",
            }
        )
    return out


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

    committed = _changed_files(since, watched)
    uncommitted = _uncommitted_files(watched)

    # Merge by path: uncommitted overrides committed (working tree is newer).
    merged: dict[str, dict] = {c["path"]: c for c in committed}
    for u in uncommitted:
        merged[u["path"]] = u

    changes = sorted(merged.values(), key=lambda r: r["path"])

    return {
        "since_commit": since,
        "poc_dir_exists": poc_dir_exists,
        "watched_paths": watched,
        "change_count": len(changes),
        "committed_count": len(committed),
        "uncommitted_count": len(uncommitted),
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
