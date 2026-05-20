"""Filesystem paths shared across scripts.

deterministic + idempotent — safe to re-run.

Single source of truth for "where the repo root is" so callers don't
each reinvent the same Path traversal. Keep this file dependency-free
so anything in lib/ can import from it without cycles.
"""

from __future__ import annotations

from pathlib import Path

# scripts/python/lib/paths.py → parents[3] = repo root
REPO_ROOT: Path = Path(__file__).resolve().parents[3]

ENV_FILE: Path = REPO_ROOT / ".env"
VERSION_FILE: Path = REPO_ROOT / "VERSION"
