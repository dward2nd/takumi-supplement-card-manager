"""Read/write the repo's VERSION file.

deterministic + idempotent — safe to re-run.

Thin wrapper so `cli.py` doesn't deal with filesystem paths directly,
and so a future caller (e.g. a CI check) can ask "what's the current
version?" without going through the CLI.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import paths  # noqa: E402

from semver import Version, parse  # noqa: E402


class VersionFileMissing(FileNotFoundError):
    pass


def read() -> Version:
    if not paths.VERSION_FILE.exists():
        raise VersionFileMissing(
            f"{paths.VERSION_FILE} does not exist. "
            "Create it with the initial version (e.g. `0.0.1`) before bumping."
        )
    return parse(paths.VERSION_FILE.read_text(encoding="utf-8"))


def write(v: Version) -> None:
    paths.VERSION_FILE.write_text(f"{v}\n", encoding="utf-8")


def path() -> str:
    return str(paths.VERSION_FILE)
