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

# Repositories: lightweight script-side database.
# See scripts/repositories/README.md for the schema.
REPOSITORIES_DIR: Path = REPO_ROOT / "scripts" / "repositories"
CARDS_REPO_DIR: Path = REPOSITORIES_DIR / "cards"
PROMOTIONS_REPO_DIR: Path = REPOSITORIES_DIR / "promotions"

# Statement-PDF decryption passwords, keyed by issuer. Real secrets — gitignored
# (see statement-passwords.example.yaml for the committed template).
STATEMENT_PASSWORDS_FILE: Path = REPOSITORIES_DIR / "statement-passwords.yaml"
