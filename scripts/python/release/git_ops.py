"""Git subprocess wrappers for the release flow.

NOT idempotent — most operations have visible side effects. Re-running
`tag()` for a tag that already exists raises GitError; commit() creates
a new commit each time. The cli orchestrates these in the right order.

All commands run with `cwd=REPO_ROOT` so the script behaves the same
regardless of the working directory at invocation time.
"""

from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import paths  # noqa: E402


class GitError(RuntimeError):
    pass


def _run(args: list[str], *, stream: bool = False) -> str:
    """Run a git command. `stream=True` lets stdout/stderr reach the user
    in real time (useful for `git push`); the return value is "" then."""
    try:
        if stream:
            subprocess.run(args, cwd=paths.REPO_ROOT, check=True)
            return ""
        proc = subprocess.run(
            args,
            cwd=paths.REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        return (proc.stdout or "").strip()
    except subprocess.CalledProcessError as e:
        cmd = " ".join(shlex.quote(a) for a in args)
        stderr = (getattr(e, "stderr", "") or "").strip()
        raise GitError(f"$ {cmd}\n{stderr}") from e


def current_branch() -> str:
    return _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def has_remote(name: str = "origin") -> bool:
    return name in _run(["git", "remote"]).split()


def status_porcelain() -> str:
    """Returns the porcelain status string; empty means clean."""
    return _run(["git", "status", "--porcelain"])


def stage_all() -> None:
    _run(["git", "add", "-A"], stream=True)


def commit(message: str) -> str:
    """Returns the new commit's hash."""
    _run(["git", "commit", "-m", message], stream=True)
    return _run(["git", "rev-parse", "HEAD"])


def tag(name: str, message: str | None = None) -> None:
    """Create an annotated tag if message is given, else lightweight."""
    if message:
        _run(["git", "tag", "-a", name, "-m", message], stream=True)
    else:
        _run(["git", "tag", name], stream=True)


def push_branch(branch: str, remote: str = "origin") -> None:
    _run(["git", "push", remote, branch], stream=True)


def push_tag(tag_name: str, remote: str = "origin") -> None:
    """Push exactly one tag — never `--tags`, which would push every local tag."""
    _run(["git", "push", remote, tag_name], stream=True)
