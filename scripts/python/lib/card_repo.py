"""Cards repository — script-side facts keyed by exact card title.

deterministic + idempotent — pure function of the on-disk YAML files.

The Cards data sources in Notion hold per-holder card pages (title,
network, premium tier, etc.); this module holds script-side policy
flags that don't fit cleanly in Notion or that are needed without a
Notion round-trip: bill-cycle pattern key, default points multiplier,
petrol-station exclusion, 7-11/TrueMoney points exclusion, issuer.

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
    truemoney_711_points_exclusion: bool
    installment_rewards_upfront: bool
    installment_note: str | None
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
        truemoney_711_points_exclusion=bool(
            data.get("truemoney_711_points_exclusion", False)
        ),
        installment_rewards_upfront=bool(
            data.get("installment_rewards_upfront", False)
        ),
        installment_note=data.get("installment_note"),
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


def _fold_apostrophes(value: str) -> str:
    """Fold typographic apostrophes to ASCII before matching a card title.

    ASCII `'` is the preferred spelling in both Notion and this repository
    (user, 2026-08-08). But U+2019 is visually indistinguishable from it and
    Notion's editor inserts it readily — `Lotus's Beyond` sat mismatched
    between the two for months. Folding makes a stray curly apostrophe resolve
    instead of silently returning None (which would drop the card's bill-cycle
    pattern and exclusion flags).
    """
    return value.replace("’", "'").replace("‘", "'")


def _fold_for_case(value: str) -> str:
    """Apostrophe-fold *and* casefold a card title, for last-resort matching."""
    return _fold_apostrophes(value).casefold()


def by_name(name: str) -> CardRepo:
    """Return the CardRepo for the given title; raise if not found.

    Three passes, strict to forgiving:

    1. exact match;
    2. typographic apostrophes folded, so `Lotus's Beyond` and
       `Lotus’s Beyond` both resolve;
    3. case-insensitive (apostrophes still folded), so Notion's
       `Krungsri VISA` resolves against this repo's `Krungsri Visa`.

    Pass 3 exists because a card's title is spelled independently in two
    places in Notion — the Cards DS page title and the Bills `Card` SELECT
    option — and the two do not always agree on case. `Krungsri VISA`
    (Cards DS) vs `Krungsri Visa` (Bills SELECT, and this repo) was found
    2026-08-27; see docs/concepts/known-divergences.md. A caller holding
    either spelling must still find the card, or the lookup returns None and
    silently drops the card's `bill_cycle_pattern` and exclusion flags —
    the same failure mode the apostrophe fold was added to prevent.

    Ambiguity is refused rather than guessed: no two registered cards
    currently differ only by case, and if two ever do, the caller should be
    told instead of handed a coin flip.
    """
    target = name.strip()
    for c in load_all():
        if c.name == target:
            return c
    folded = _fold_apostrophes(target)
    for c in load_all():
        if _fold_apostrophes(c.name) == folded:
            return c
    caseless = _fold_for_case(target)
    case_hits = [c for c in load_all() if _fold_for_case(c.name) == caseless]
    if len(case_hits) == 1:
        return case_hits[0]
    if len(case_hits) > 1:
        raise CardRepoNotFoundError(
            f"card title {target!r} matches {len(case_hits)} registered cards "
            f"case-insensitively: {sorted(c.name for c in case_hits)}. "
            f"Pass the exact title."
        )
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
