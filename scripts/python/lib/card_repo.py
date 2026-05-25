"""Cards repository — script-side facts keyed by exact card title.

deterministic + idempotent — pure function of the on-disk YAML files.

The Cards data sources in Notion hold per-holder card pages (title,
network, premium tier, etc.); this module holds script-side policy
flags that don't fit cleanly in Notion or that are needed without a
Notion round-trip: bill-cycle pattern key, default points multiplier,
petrol-station exclusion, issuer.

One YAML file per card under `scripts/repositories/cards/`. See
`scripts/repositories/README.md` for the schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from . import paths


@dataclass(frozen=True)
class CardRepo:
    name: str
    issuer: str
    bill_cycle_pattern: str
    points_default: str | None
    petrol_exclusion: bool
    notes: str | None
    source_path: Path


class CardRepoNotFoundError(LookupError):
    pass


def _parse_card(data: dict[str, Any], source: Path) -> CardRepo:
    required = ("name", "issuer", "bill_cycle_pattern")
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"{source}: card missing required field(s) {missing}")
    return CardRepo(
        name=str(data["name"]),
        issuer=str(data["issuer"]),
        bill_cycle_pattern=str(data["bill_cycle_pattern"]),
        points_default=data.get("points_default"),
        petrol_exclusion=bool(data.get("petrol_exclusion", False)),
        notes=data.get("notes"),
        source_path=source,
    )


@lru_cache(maxsize=1)
def load_all() -> tuple[CardRepo, ...]:
    """Load every card YAML in the repository. Cached for process lifetime."""
    base = paths.CARDS_REPO_DIR
    if not base.exists():
        return ()
    out = []
    for path in sorted(base.glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        out.append(_parse_card(data, path))
    return tuple(out)


def by_name(name: str) -> CardRepo:
    """Return the CardRepo for the given exact title; raise if not found."""
    target = name.strip()
    for c in load_all():
        if c.name == target:
            return c
    known = sorted(c.name for c in load_all())
    raise CardRepoNotFoundError(
        f"no card titled {target!r} in scripts/repositories/cards/. "
        f"Known cards: {known}. Add a YAML file to register a new card."
    )


def get(name: str, *, default: CardRepo | None = None) -> CardRepo | None:
    """Like by_name but returns `default` instead of raising when missing."""
    try:
        return by_name(name)
    except CardRepoNotFoundError:
        return default


def list_names() -> list[str]:
    return [c.name for c in load_all()]
