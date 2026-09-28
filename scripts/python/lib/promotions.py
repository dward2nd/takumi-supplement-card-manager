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
  3. Petrol exclusion: petrol-merchant strings earn nothing on cards whose
     family withholds fuel (UOB, ttb — lib.earning).

  Steps 2 and 3 are **not promo-driven** — they fire on a card with no active
  promotion too, forcing `×0`. Only a promo's `overrides` / `default: apply`
  can soften step 2, so with no promo the default exclusion always wins.
  4. Tier matching: first tier whose `patterns` matches the merchant
     string (and whose `exclude_patterns` does not) wins.
  5. Falls through to no cashback if nothing matches.
  6. The card family's own rules are layered on top of whatever 1–5
     decided (lib.earning): the Krungsri family's installment rewards paid
     upfront and its 7-11 / TrueMoney points exclusion, AEON's MCC points
     exclusions. The points-only ones leave the cashback rate untouched.

The steps themselves live in `lib.earning` (one class per card family);
this module keeps the promotion data, the merchant-string heuristics and
the public `classify`.

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

from . import paths


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
# merchant string.
#
# Both alpha-2 and alpha-3 forms appear in the data — the same issuer will
# bill `APPLE.COM/BILL CORK IE` one month and `... CORK IRL` the next — so
# both are listed. Three tokens are DELIBERATELY excluded; do not "complete"
# the list by adding them (checked against the live data 2026-08-20):
#
#   THA  — domestic Thailand, the alpha-3 form of TH. 712 rows carry it
#          (`WWW.SFCINEMACITY.COM-C BANGKOK THA`). Adding it would misclassify
#          the single largest group of ordinary domestic charges as foreign.
#   MTH  — also domestic (`7-11 PHOTHARAM ROAD CHANGPHUEAK MTH`), an issuer
#          variant spelling, not Mauritania/anything foreign.
#   VAT  — the tax line `SALES DR RETR FEE - INC OF VAT`, not Vatican City.
#          A genuine alpha-3 collision; the accounting row must stay domestic.
#   CHN  — foreign, but NOT foreign-in-THB. All 70 occurrences are CNY-billed
#          `Alipay Shanghai CHN` / `UNIONPAY MERCHANT BEIJING CHN` rows on
#          Nuta's AEON UnionPay, whose entire purpose is CNY spend at 3%
#          cashback. Those are *genuine foreign-currency* charges, which the
#          project rule explicitly does NOT exclude. Listing CHN here would
#          zero out the one card that earns on them. Note the asymmetry with
#          alpha-2 `CN`, which IS listed: `CN` has never appeared in the data,
#          so it carries no such counter-evidence. Revisit if a THB-billed
#          `… CHN` row ever shows up on a non-UnionPay card.
#
# Note this is a *heuristic on the merchant string* — the actual exclusion
# hinges on the charge being billed in THB, which the string cannot tell us.
# See the module docstring and docs/concepts/promotions.md.
_FOREIGN_COUNTRY_TOKENS: frozenset[str] = frozenset({
    # alpha-2
    "US", "JP", "SG", "KR", "HK", "TW", "CN", "MY", "VN",
    "ID", "PH", "AU", "GB", "UK", "DE", "FR", "ES", "IT", "NL",
    "CH", "CA", "NZ", "IN", "AE", "QA", "SA", "TR", "LA", "KH",
    "MM", "IE", "SE",
    # alpha-3 (THA / MTH / VAT excluded on purpose — see above)
    "USA", "JPN", "KOR", "SGP", "HKG", "TWN", "MYS", "VNM",
    "IDN", "PHL", "AUS", "GBR", "DEU", "FRA", "ESP", "ITA", "NLD",
    "CHE", "CAN", "NZL", "IND", "ARE", "QAT", "SAU", "TUR", "LAO",
    "KHM", "MMR", "IRL", "SWE",
})

_INSTALLMENT_RE = re.compile(r"\b\d{2}/\d{2}\b")

# Petrol-station heuristic. Whether fuel is withheld is the card family's
# rule (lib.earning: UOB, ttb); the merchant-string heuristic for "is this a
# petrol station?" is kept here with the other string heuristics.
#
# One brand, several string forms — Bangchak bills as the ticker-style `BCP`,
# the spelled-out `BANGCHAK-…`, *and* `BSRC-…`. The last is Bangchak Sriracha
# (the former Esso Thailand network, renamed after Bangchak's acquisition), so
# the dealer name follows the prefix: `BSRC-PHAAPOOM ENERGY LAMPHUN TH`,
# `BSRC-SUSCO-MAE SA CHIANGMAI TH`. Added 2026-08-27 after a ttb so smart row
# classified as the flat 1% tier; the household had already been hand-noting
# those rows `หมวดหมู่น้ำมัน` (fuel category) since 2025-09.
_PETROL_TOKENS: tuple[str, ...] = (
    "PTTST", "PTT ", "BCP", "BANGCHAK", "BSRC", "ESSO", "SHELL", "CALTEX",
)

# 7-Eleven / TrueMoney heuristic, for the Krungsri family's *points-only*
# exclusion (lib.earning.KrungsriFamilyCard). TrueMoney is matched on the merchant *prefix*
# (`TMN ` / `TMN*`) so an unrelated merchant containing "TMN" mid-string
# doesn't trip it; 7-Eleven is matched anywhere in the string.
_TRUEMONEY_PREFIXES: tuple[str, ...] = ("TMN ", "TMN*")
_SEVEN_ELEVEN_TOKENS: tuple[str, ...] = ("7-11", "7-ELEVEN")


def is_installment(merchant_name: str) -> bool:
    """True if the merchant string ends in (or contains) the `NN/NN` installment marker."""
    return bool(_INSTALLMENT_RE.search(merchant_name))


def looks_foreign_in_thb(merchant_name: str) -> bool:
    """Heuristic: country suffix at end of the merchant string ≠ TH."""
    tokens = merchant_name.strip().split()
    if not tokens:
        return False
    return tokens[-1].upper() in _FOREIGN_COUNTRY_TOKENS


def looks_petrol(merchant_name: str) -> bool:
    upper = merchant_name.upper()
    return any(tok in upper for tok in _PETROL_TOKENS)


# An e-wallet top-up. UOB cuts the descriptor short: `2C2P *SHOPEEPAY (TOP BANGKOK`
# (user, 2026-09-28: "those are the top-up rows … should give no points").
# `TMN 7-11` is a TrueMoney *payment* at 7-Eleven, not a top-up, and doesn't match.
_WALLET_TOP_UP = re.compile(r"\(TOP\b|\bTOP ?-?UP\b")


def looks_wallet_top_up(merchant_name: str) -> bool:
    return bool(_WALLET_TOP_UP.search(merchant_name.upper()))


# Supermarkets and grocers (MCC 5411) whose names show it. KTC UnionPay earns no
# points there (docs/promotions/ktc-forever.md, rule 16).
_SUPERMARKET = re.compile(r"SAVEMART|LOTUS'?S|BIG ?C\b|\bTOPS\b|RIMPING|VILLA MARKET|GOURMET MARKET|MAX ?VALU|"
                          r"FOODLAND|CP FRESH|TESCO")
# Public transport and tolls (MCC 4111/4112/4131/4784): no KTC points (rule 17).
_TRANSPORT_TOLL = re.compile(r"EXPRESSWAY|EASY ?PASS|\bM-?PASS\b|\bBTS\b|\bMRT\b|\bSRT\b|\bBMTA\b")


def looks_supermarket(merchant_name: str) -> bool:
    return bool(_SUPERMARKET.search(merchant_name.upper()))


def looks_transport_or_toll(merchant_name: str) -> bool:
    return bool(_TRANSPORT_TOLL.search(merchant_name.upper()))


def looks_truemoney_or_711(merchant_name: str) -> bool:
    """True for TrueMoney (`TMN `/`TMN*` prefix) or 7-Eleven merchant strings."""
    upper = merchant_name.strip().upper()
    if any(upper.startswith(p) for p in _TRUEMONEY_PREFIXES):
        return True
    return any(tok in upper for tok in _SEVEN_ELEVEN_TOKENS)


def matches_tier(merchant_name: str, tier: Tier) -> bool:
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
    """Classify a single transaction: the card's class runs its active promotion,
    then the card's own rules (lib.earning).

    `is_installment_override` lets callers force-set the installment flag; by
    default it's auto-detected from the merchant string. Passing `False`
    explicitly disables auto-detection.
    """
    from .earning import card_for   # late: earning builds on this module
    return card_for(card).classify(date, merchant_name, is_installment_override=is_installment_override,
                                   promotions=promotions)
