"""Promotions: load, list active, and classify a transaction against them.

deterministic + idempotent — pure function of (promo files, inputs).

Each promotion lives in `scripts/repositories/promotions/<id>.yaml`.
Schema documented in `scripts/repositories/README.md`. Human-readable
narrative for a promo (the why, history, open questions) lives in
`docs/promotions/<id>.md` and references the repository file as the
structured source of truth.

Classification semantics (see also that doc):
  1. Installment override (if the merchant string ends in `NN/NN` and the
     promo has an `installment_rule`): use that rate.
  2. Foreign-in-THB handling:
     - Default rule: foreign merchant billed in THB earns nothing.
     - The promo can override per-merchant via `foreign_in_thb_policy.overrides`
       (cashback granted at the override rate; `keeps_points_exclusion: true`
       means points are still excluded → set `×0`).
     - The promo can override globally via `foreign_in_thb_policy.default: apply`
       (tier rules then apply to foreign-in-THB rows like any other row).
  3. UOB-card petrol exclusion (general rule): petrol-merchant strings on
     UOB-prefixed cards earn nothing.
  4. Tier matching: first tier whose `patterns` matches the merchant
     string (and whose `exclude_patterns` does not) wins.
  5. Falls through to no cashback if nothing matches.

`points_default` on the promo (typically `"×0"` for cards like UOB One)
is returned alongside the rate so callers can set the correct multiplier
on the transaction page. `None` means "don't touch the multiplier".
"""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml

from . import card_repo, paths


# --------------------------------------------------------------------------
# Schema-shaped dataclasses
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Tier:
    rate: float
    label: str | None = None
    patterns: tuple[str, ...] = ()
    exclude_patterns: tuple[str, ...] = ()


@dataclass(frozen=True)
class ForeignOverride:
    merchant_substring: str
    rate: float
    keeps_points_exclusion: bool = True


@dataclass(frozen=True)
class ForeignInThbPolicy:
    default: str = "exclude"  # "exclude" | "apply"
    overrides: tuple[ForeignOverride, ...] = ()


@dataclass(frozen=True)
class InstallmentRule:
    rate: float
    credited: str | None = None  # "per_installment" | "at_purchase"


@dataclass(frozen=True)
class Promotion:
    id: str
    name: str
    card: str
    effective_start: _dt.date
    effective_end: _dt.date | None
    status: str
    tiers: tuple[Tier, ...]
    foreign_in_thb_policy: ForeignInThbPolicy
    installment_rule: InstallmentRule | None
    crediting_schedule: dict[str, str]
    points_default: str | None
    source_path: Path = field(default_factory=Path)

    def is_active_on(self, date: _dt.date) -> bool:
        if self.status != "active":
            return False
        if date < self.effective_start:
            return False
        if self.effective_end is not None and date > self.effective_end:
            return False
        return True


# --------------------------------------------------------------------------
# Frontmatter I/O
# --------------------------------------------------------------------------


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    """Write a promotion YAML file. Stable key order, unicode-safe."""
    text = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,  # avoid line-wrapping long patterns
    )
    path.write_text(text, encoding="utf-8")


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------


def _parse_date(value: Any, field_name: str) -> _dt.date | None:
    if value is None:
        return None
    if isinstance(value, _dt.date):
        return value
    if isinstance(value, str):
        return _dt.date.fromisoformat(value)
    raise TypeError(
        f"{field_name} must be an ISO date string (or null/None); got {value!r}"
    )


def _parse_tier(raw: dict[str, Any]) -> Tier:
    return Tier(
        rate=float(raw["rate"]),
        label=raw.get("label"),
        patterns=tuple(raw.get("patterns") or ()),
        exclude_patterns=tuple(raw.get("exclude_patterns") or ()),
    )


def _parse_foreign_policy(raw: dict[str, Any] | None) -> ForeignInThbPolicy:
    if not raw:
        return ForeignInThbPolicy()
    default = raw.get("default", "exclude")
    if default not in {"exclude", "apply"}:
        raise ValueError(
            f"foreign_in_thb_policy.default must be 'exclude' or 'apply'; got {default!r}"
        )
    overrides = tuple(
        ForeignOverride(
            merchant_substring=o["merchant_substring"],
            rate=float(o["rate"]),
            keeps_points_exclusion=bool(o.get("keeps_points_exclusion", True)),
        )
        for o in (raw.get("overrides") or [])
    )
    return ForeignInThbPolicy(default=default, overrides=overrides)


def _parse_installment(raw: dict[str, Any] | None) -> InstallmentRule | None:
    if not raw:
        return None
    return InstallmentRule(
        rate=float(raw["rate"]),
        credited=raw.get("credited"),
    )


def parse_promotion(frontmatter: dict[str, Any], source_path: Path | None = None) -> Promotion:
    """Build a Promotion from a frontmatter dict. Raises on schema violations."""
    required = ("id", "name", "card", "effective_start", "status")
    missing = [k for k in required if k not in frontmatter]
    if missing:
        raise ValueError(
            f"promotion missing required field(s): {missing} (in {source_path})"
        )

    return Promotion(
        id=str(frontmatter["id"]),
        name=str(frontmatter["name"]),
        card=str(frontmatter["card"]),
        effective_start=_parse_date(frontmatter["effective_start"], "effective_start"),
        effective_end=_parse_date(frontmatter.get("effective_end"), "effective_end"),
        status=str(frontmatter["status"]),
        tiers=tuple(_parse_tier(t) for t in (frontmatter.get("tiers") or [])),
        foreign_in_thb_policy=_parse_foreign_policy(frontmatter.get("foreign_in_thb_policy")),
        installment_rule=_parse_installment(frontmatter.get("installment_rule")),
        crediting_schedule=dict(frontmatter.get("crediting_schedule") or {}),
        points_default=frontmatter.get("points_default"),
        source_path=source_path or Path(),
    )


# --------------------------------------------------------------------------
# Discovery
# --------------------------------------------------------------------------


def _promotion_files(promotions_dir: Path | None = None) -> Iterable[Path]:
    base = promotions_dir or paths.PROMOTIONS_REPO_DIR
    if not base.exists():
        return []
    for p in sorted(base.glob("*.yaml")):
        if p.name.startswith("_"):  # reserved for indexes/stubs
            continue
        yield p


def load_all(promotions_dir: Path | None = None) -> list[Promotion]:
    """Load every promotion YAML in the repository."""
    out = []
    for path in _promotion_files(promotions_dir):
        data = read_yaml(path)
        if "id" not in data or "card" not in data:
            continue
        out.append(parse_promotion(data, source_path=path))
    return out


def active_for_card_date(
    card: str, date: _dt.date, promotions: list[Promotion] | None = None
) -> list[Promotion]:
    """Return every promotion that's active for this card on this date."""
    promos = promotions if promotions is not None else load_all()
    return [p for p in promos if p.card == card and p.is_active_on(date)]


# --------------------------------------------------------------------------
# Classification
# --------------------------------------------------------------------------


# Country suffixes we treat as "foreign" when they appear at the end of the
# merchant string. TH is intentionally absent (TH = domestic).
_FOREIGN_COUNTRY_TOKENS: frozenset[str] = frozenset({
    "US", "USA", "JP", "SG", "KR", "HK", "TW", "CN", "MY", "VN",
    "ID", "PH", "AU", "GB", "UK", "DE", "FR", "ES", "IT", "NL",
    "CH", "CA", "NZ", "IN", "AE", "QA", "SA", "TR", "LA", "KH",
    "MM",
})

_INSTALLMENT_RE = re.compile(r"\b\d{2}/\d{2}\b")

# Petrol-station heuristic. The exclusion is *card-level* (driven by
# `petrol_exclusion: true` in scripts/repositories/cards/<card>.yaml),
# but the merchant-string heuristic for "is this a petrol station?" is
# kept here next to the rest of the classification logic.
_PETROL_TOKENS: tuple[str, ...] = (
    "PTTST", "PTT ", "BCP", "BANGCHAK", "ESSO", "SHELL", "CALTEX",
)


def is_installment(merchant_name: str) -> bool:
    """True if the merchant string ends in (or contains) the `NN/NN` installment marker."""
    return bool(_INSTALLMENT_RE.search(merchant_name))


def looks_foreign_in_thb(merchant_name: str) -> bool:
    """Heuristic: country suffix at end of the merchant string ≠ TH."""
    tokens = merchant_name.strip().split()
    if not tokens:
        return False
    return tokens[-1].upper() in _FOREIGN_COUNTRY_TOKENS


def _looks_petrol(merchant_name: str) -> bool:
    upper = merchant_name.upper()
    return any(tok in upper for tok in _PETROL_TOKENS)


def _card_excludes_petrol(card: str) -> bool:
    """True when the card-repo entry for `card` has `petrol_exclusion: true`."""
    entry = card_repo.get(card)
    return bool(entry and entry.petrol_exclusion)


def _matches_tier(merchant_name: str, tier: Tier) -> bool:
    name_upper = merchant_name.upper()
    matched = any(
        p == "*" or p.upper() in name_upper for p in tier.patterns
    )
    if not matched:
        return False
    excluded = any(p.upper() in name_upper for p in tier.exclude_patterns)
    return not excluded


@dataclass(frozen=True)
class Classification:
    cashback_percent: float | None  # None = leave `% cb` unset
    note: str | None
    points_override: str | None  # multiplier string ("×0", etc.) or None
    promotion_id: str | None  # which promo fired; None = no active promo
    reason: str  # short tag: "no-promo", "installment", "foreign-override", "foreign-default-exclude", "uob-petrol", "tier", "no-tier-match"


def classify(
    card: str,
    date: _dt.date,
    merchant_name: str,
    *,
    is_installment_override: bool | None = None,
    promotions: list[Promotion] | None = None,
) -> Classification:
    """Classify a single transaction against the active promotion(s).

    `is_installment_override` lets callers force-set the installment flag; by
    default it's auto-detected from the merchant string. Passing `False`
    explicitly disables auto-detection.
    """
    actives = active_for_card_date(card, date, promotions=promotions)
    inst = (
        is_installment(merchant_name)
        if is_installment_override is None
        else is_installment_override
    )

    card_entry = card_repo.get(card)
    card_points_default = card_entry.points_default if card_entry else None

    if not actives:
        # No active promo → no cashback. Still surface the petrol exclusion
        # for the Note when it applies (card-driven).
        if (_card_excludes_petrol(card) and _looks_petrol(merchant_name)):
            return Classification(
                cashback_percent=None,
                note=f"Petrol station — {card} earns no cashback / points at fuel merchants.",
                points_override=card_points_default,
                promotion_id=None,
                reason="petrol-exclusion",
            )
        return Classification(
            cashback_percent=None,
            note=None,
            points_override=card_points_default,
            promotion_id=None,
            reason="no-promo",
        )

    # If multiple promos apply (shouldn't be common), prefer the first by
    # effective_start descending (most recent wins). Document the rule so
    # the caller knows what to expect.
    promo = sorted(actives, key=lambda p: p.effective_start, reverse=True)[0]

    # 1) Installment override
    if inst and promo.installment_rule:
        rate = promo.installment_rule.rate
        return Classification(
            cashback_percent=rate if rate > 0 else None,
            note=(
                f"Installment transaction — per {promo.name}, "
                f"{rate * 100:.0f}% per installment row."
            ),
            points_override=promo.points_default or card_points_default,
            promotion_id=promo.id,
            reason="installment",
        )

    # 2) Foreign-in-THB handling
    is_foreign = looks_foreign_in_thb(merchant_name)
    if is_foreign:
        if promo.foreign_in_thb_policy.default == "exclude":
            # Per-merchant override?
            for ov in promo.foreign_in_thb_policy.overrides:
                if ov.merchant_substring.upper() in merchant_name.upper():
                    return Classification(
                        cashback_percent=ov.rate if ov.rate > 0 else None,
                        note=(
                            f"Per {promo.name}: {ov.rate * 100:.2f}% on "
                            f"{ov.merchant_substring!r} "
                            f"(promo override of foreign-in-THB rule). "
                            + (
                                "Points still excluded (×0) — promo did not override."
                                if ov.keeps_points_exclusion
                                else ""
                            )
                        ).strip(),
                        points_override=(
                            "×0" if ov.keeps_points_exclusion else promo.points_default
                        ),
                        promotion_id=promo.id,
                        reason="foreign-override",
                    )
            # No override → default rule excludes both cashback and points.
            return Classification(
                cashback_percent=None,
                note="Foreign merchant in THB — no cashback / points by default rule.",
                points_override="×0",
                promotion_id=promo.id,
                reason="foreign-default-exclude",
            )
        # default == "apply": tier rules apply to foreign-in-THB rows too.

    # 3) Petrol exclusion (card-level rule)
    if (_card_excludes_petrol(card) and _looks_petrol(merchant_name)):
        return Classification(
            cashback_percent=None,
            note=f"Petrol station — {card} earns no cashback / points at fuel merchants.",
            points_override=promo.points_default or card_points_default,
            promotion_id=promo.id,
            reason="petrol-exclusion",
        )

    # 4) Tier matching
    for tier in promo.tiers:
        if _matches_tier(merchant_name, tier):
            return Classification(
                cashback_percent=tier.rate if tier.rate > 0 else None,
                note=None,
                points_override=promo.points_default or card_points_default,
                promotion_id=promo.id,
                reason="tier",
            )

    # 5) Fallthrough — no tier matched
    return Classification(
        cashback_percent=None,
        note=None,
        points_override=promo.points_default or card_points_default,
        promotion_id=promo.id,
        reason="no-tier-match",
    )
