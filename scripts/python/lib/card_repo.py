"""Cards repository — script-side facts keyed by exact card title.

deterministic + idempotent — pure function of the on-disk YAML files.

The Cards data sources in Notion hold per-holder card pages (title,
network, premium tier, etc.); this module holds script-side policy
flags that don't fit cleanly in Notion or that are needed without a
Notion round-trip: bill-cycle pattern key, default points multiplier,
petrol-station exclusion, 7-11/TrueMoney points exclusion, merchant
points exclusions, issuer.

One YAML file per card under `scripts/repositories/cards/`. See
`scripts/repositories/README.md` for the schema.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from . import paths


@dataclass(frozen=True)
class MerchantPointsExclusion:
    """Merchant strings that earn no points on this card from a date onwards.

    Issuers exclude by MCC, which a merchant string doesn't carry, so an entry
    names the strings known to bill under an excluded code. Matched as a
    prefix, after dropping a leading `[บัตรหลัก] `; `*` matches every merchant.
    """

    prefix: str
    effective_from: _dt.date
    note: str
    mcc: str | None = None


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
    # Last four digits printed on the issuer's statement → holder slug
    # (takumi / baiboon / nuta / unmonitored). Takumi's number is the primary
    # card; any other holder's is their supplement. Read by /record-statement.
    statement_numbers: dict[str, str] = field(default_factory=dict)
    points_excluded_merchants: tuple[MerchantPointsExclusion, ...] = ()


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
        statement_numbers=_parse_statement_numbers(data.get("statement_numbers"), source),
        points_excluded_merchants=_parse_merchant_exclusions(data.get("points_excluded_merchants"), source),
    )


def _parse_merchant_exclusions(raw: Any, source: Path) -> tuple[MerchantPointsExclusion, ...]:
    """Validate `points_excluded_merchants` — each entry needs prefix, effective_from, note."""
    out = []
    for i, e in enumerate(raw or []):
        missing = [k for k in ("prefix", "effective_from", "note") if not e.get(k)]
        if missing:
            raise ValueError(f"{source}: points_excluded_merchants[{i}] missing {missing}")
        start = e["effective_from"]
        if not isinstance(start, _dt.date):
            start = _dt.date.fromisoformat(str(start))
        out.append(MerchantPointsExclusion(
            prefix=str(e["prefix"]), effective_from=start, note=str(e["note"]),
            mcc=str(e["mcc"]) if e.get("mcc") is not None else None,
        ))
    return tuple(out)


# `unmonitored`: a real supplement nobody in the household tracks — its
# charges count toward the bill but are recorded in no ledger.
_HOLDER_SLUGS = frozenset({"takumi", "baiboon", "nuta", "unmonitored"})


def _parse_statement_numbers(raw: Any, source: Path) -> dict[str, str]:
    """Validate `statement_numbers` — quoted 4-digit keys, known holder slugs.

    Keys must be quoted in YAML: an unquoted `0052` loads as an integer (and
    YAML 1.1 reads a leading zero as octal), which would silently never match.
    """
    if not raw:
        return {}
    if not isinstance(raw, dict):
        raise ValueError(f"{source}: statement_numbers must be a mapping")
    out: dict[str, str] = {}
    for k, v in raw.items():
        if not (isinstance(k, str) and len(k) == 4 and k.isdigit()):
            raise ValueError(f"{source}: statement_numbers key {k!r} must be a quoted 4-digit string")
        if str(v).lower() not in _HOLDER_SLUGS:
            raise ValueError(f"{source}: statement_numbers[{k!r}] = {v!r} is not a holder slug")
        out[k] = str(v).lower()
    return out


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
