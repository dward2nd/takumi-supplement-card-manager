#!/usr/bin/env python3
"""release — bump VERSION, commit, tag, push.

NOT idempotent: each invocation creates a new commit and tag. Re-running
after a successful release fails at the tag step (tag already exists),
which is a deliberate safety net.

Full flow on `uv run scripts/python/release/cli.py <type>`:

  1. Read repo-root VERSION; bump per <type> (major | minor | patch).
  2. Write the new value back to VERSION.
  3. `git add -A`               (any unstaged/uncommitted changes ride along)
  4. `git commit -m "release: v<next>"`
  5. `git tag -a v<next> -m "Release v<next>"`
  6. `git push origin <current-branch>`
  7. `git push origin v<next>`   (only the new tag, never `--tags`)

Each side-effect can be skipped via --no-commit / --no-tag / --no-push.
Use --dry-run to write VERSION and skip every git step (useful for
exercising the bump math without touching history).

Output: JSON envelope on stdout describing the bump, the commit hash if
created, the tag if created, and which actions ran. Errors raise and
exit non-zero — partial states are visible (the VERSION write happens
before any git op; if a later step fails, `git restore VERSION` rolls
the file back).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import git_ops  # noqa: E402
import semver  # noqa: E402
import version_file  # noqa: E402


def run(
    bump_type: str,
    *,
    commit: bool = True,
    tag: bool = True,
    push: bool = True,
    dry_run: bool = False,
) -> dict:
    previous = version_file.read()
    next_v = semver.bump(previous, bump_type)

    out: dict = {
        "previous": str(previous),
        "next": str(next_v),
        "type": bump_type,
        "version_file": version_file.path(),
        "actions": [],
    }

    version_file.write(next_v)
    out["actions"].append("write_version")

    if dry_run:
        out["dry_run"] = True
        return out

    tag_name = f"v{next_v}"

    if commit:
        if not git_ops.status_porcelain():
            raise RuntimeError(
                "git status is clean after VERSION bump; refusing to commit "
                "(this should never happen — check the file write succeeded)"
            )
        git_ops.stage_all()
        out["actions"].append("git_add")
        out["commit"] = git_ops.commit(f"release: {tag_name}")
        out["actions"].append("git_commit")

    if tag:
        git_ops.tag(tag_name, message=f"Release {tag_name}")
        out["tag"] = tag_name
        out["actions"].append("git_tag")

    if push:
        if not git_ops.has_remote():
            out["push_skipped"] = "no `origin` remote configured"
        else:
            branch = git_ops.current_branch()
            git_ops.push_branch(branch)
            out["actions"].append(f"git_push:{branch}")
            if tag:
                git_ops.push_tag(tag_name)
                out["actions"].append(f"git_push_tag:{tag_name}")

    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("type", choices=semver.BUMP_TYPES, help="Bump type")
    ap.add_argument("--no-commit", action="store_true", help="Skip `git add` + `git commit`")
    ap.add_argument("--no-tag", action="store_true", help="Skip `git tag`")
    ap.add_argument("--no-push", action="store_true", help="Skip `git push` for branch and tag")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Write VERSION but skip every git op (overrides --no-* flags)",
    )
    args = ap.parse_args(argv)

    out = run(
        args.type,
        commit=not args.no_commit,
        tag=not args.no_tag,
        push=not args.no_push,
        dry_run=args.dry_run,
    )
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
