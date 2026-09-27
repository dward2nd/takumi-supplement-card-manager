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
  3. Petrol exclusion (general rule): petrol-merchant strings on a card with
     `petrol_exclusion: true` earn nothing.

  Steps 2 and 3 are **not promo-driven** — they fire on a card with no active
  promotion too, forcing `×0`. Only a promo's `overrides` / `default: apply`
  can soften step 2, so with no promo the default exclusion always wins.
  4. Tier matching: first tier whose `patterns` matches the merchant
     string (and whose `exclude_patterns` does not) wins.
  5. Falls through to no cashback if nothing matches.
  6. Card-level *points-only* exclusions are layered on top of whatever
     1–5 decided: `truemoney_711_points_exclusion` (the Krungsri-family
     rule) forces `×0` on 7-11 / TrueMoney rows while leaving the
     cashback rate untouched, since only reward points are withdrawn.

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

# Petrol-station heuristic. The exclusion is *card-level* (driven by
# `petrol_exclusion: true` in scripts/repositories/cards/<card>.yaml),
# but the merchant-string heuristic for "is this a petrol station?" is
# kept here next to the rest of the classification logic.
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

# 7-Eleven / TrueMoney heuristic, for the *points-only* exclusion carried by
# `truemoney_711_points_exclusion: true` in scripts/repositories/cards/<card>.yaml
# (the Krungsri-family rule). TrueMoney is matched on the merchant *prefix*
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


def _card_excludes_petrol(card: str) -> bool:
    """True when the card-repo entry for `card` has `petrol_exclusion: true`."""
    entry = card_repo.get(card)
    return bool(entry and entry.petrol_exclusion)


def looks_truemoney_or_711(merchant_name: str) -> bool:
    """True for TrueMoney (`TMN `/`TMN*` prefix) or 7-Eleven merchant strings."""
    upper = merchant_name.strip().upper()
    if any(upper.startswith(p) for p in _TRUEMONEY_PREFIXES):
        return True
    return any(tok in upper for tok in _SEVEN_ELEVEN_TOKENS)


def _card_excludes_truemoney_711_points(card: str) -> bool:
    """True when the card carries `truemoney_711_points_exclusion: true`."""
    entry = card_repo.get(card)
    return bool(entry and entry.truemoney_711_points_exclusion)


def _apply_truemoney_711_points_exclusion(
    result: "Classification", card: str, merchant_name: str
) -> "Classification":
    """Force `×0` points on 7-11 / TrueMoney rows for cards carrying the flag.

    Points-only: `cashback_percent` is left exactly as the tier / promo logic
    computed it, because the Krungsri-family rule withdraws *reward points*
    only — cashback promotions are unaffected (user, 2026-08-08).
    """
    if not _card_excludes_truemoney_711_points(card):
        return result
    if not looks_truemoney_or_711(merchant_name):
        return result
    if result.points_override == "×0":
        return result  # already excluded by a stronger rule; leave the note alone
    note = (
        "7-11 / TrueMoney — Krungsri-family cards earn no reward points at "
        "these merchants."
    )
    return Classification(
        cashback_percent=result.cashback_percent,
        note=f"{result.note} {note}".strip() if result.note else note,
        points_override="×0",
        promotion_id=result.promotion_id,
        reason=f"{result.reason}+truemoney-711-points-exclusion",
    )


def _apply_merchant_points_exclusions(
    result: "Classification", card: str, date: _dt.date, merchant_name: str
) -> "Classification":
    """Force `×0` points on merchant strings the card's YAML lists as excluded.

    Points-only, like the 7-11 / TrueMoney rule: `cashback_percent` is left as
    computed. Entries come from `points_excluded_merchants` in the card YAML
    (e.g. AEON's MCC exclusions from 2025-11-11, where `WWW.MAKRO.PRO …` bills
    as MCC 5199 but `HTTPS://WWW.MAKRO.PRO/ …` as 5411). A prefix of `*`
    matches every merchant — AEON Rabbit stopped earning points altogether.
    """
    entry = card_repo.get(card)
    if not entry or not entry.points_excluded_merchants or result.points_override == "×0":
        return result
    name = merchant_name.strip()
    if name.startswith("[บัตรหลัก]"):
        name = name[len("[บัตรหลัก]"):].strip()
    for ex in entry.points_excluded_merchants:
        if date >= ex.effective_from and (ex.prefix == "*" or name.upper().startswith(ex.prefix.upper())):
            return Classification(
                cashback_percent=result.cashback_percent,
                note=f"{result.note} {ex.note}".strip() if result.note else ex.note,
                points_override="×0",
                promotion_id=result.promotion_id,
                reason=f"{result.reason}+merchant-points-exclusion",
            )
    return result


def _apply_installment_rewards_upfront(
    result: "Classification", card: str, *, is_inst: bool
) -> "Classification":
    """Zero out both axes on installment terms for cards flagged upfront-rewards.

    Krungsri grants the points and cashback for an installment purchase **in
    full at the moment of purchase**, not spread across the terms (user,
    2026-08-10). Each `NN/NN` term therefore earns nothing on its own — the
    reward already landed on the original charge.

    The *reason* differs per card, so the explanation is data-driven: a card may
    supply its own `installment_note`. First Choice does, because there the
    mechanism is a dual credit line rather than upfront crediting — a
    merchant-offered installment is booked against the personal-loan line, which
    earns no card rewards at all.

    Unlike the 7-11 / TrueMoney rule this touches *both* axes, so it runs only
    when no promotion has spoken specifically about installments: a promo with
    an explicit `installment_rule` (reason `installment`) is the more specific
    fact and keeps its per-term rate. That is what leaves room for the First
    Choice U Plan case, where a row earns no points but may still take cashback
    under an active promo.
    """
    entry = card_repo.get(card)
    if not is_inst or not (entry and entry.installment_rewards_upfront):
        return result
    if result.reason.startswith("installment"):
        return result  # promo rules installments explicitly; it wins
    note = entry.installment_note or (
        f"Installment term — {card} grants points and cashback upfront at "
        "purchase, so individual terms earn nothing."
    )
    return Classification(
        cashback_percent=None,
        note=f"{result.note} {note}".strip() if result.note else note,
        points_override="×0",
        promotion_id=result.promotion_id,
        reason=f"{result.reason}+installment-rewards-upfront",
    )


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

    Card-level points-only exclusions are layered on top of the promo result
    (step 6 in the module docstring), so they can withdraw points without
    disturbing the cashback rate a promotion granted.
    """
    result = _classify_core(
        card,
        date,
        merchant_name,
        is_installment_override=is_installment_override,
        promotions=promotions,
    )
    is_inst = (
        is_installment(merchant_name)
        if is_installment_override is None
        else is_installment_override
    )
    # Upfront-rewards runs first: it sets `×0`, which the TrueMoney step then
    # sees and skips, so an installment row at a TrueMoney merchant carries one
    # explanation rather than two stacked ones.
    result = _apply_installment_rewards_upfront(result, card, is_inst=is_inst)
    result = _apply_truemoney_711_points_exclusion(result, card, merchant_name)
    return _apply_merchant_points_exclusions(result, card, date, merchant_name)


def _classify_core(
    card: str,
    date: _dt.date,
    merchant_name: str,
    *,
    is_installment_override: bool | None = None,
    promotions: list[Promotion] | None = None,
) -> Classification:
    actives = active_for_card_date(card, date, promotions=promotions)
    inst = (
        is_installment(merchant_name)
        if is_installment_override is None
        else is_installment_override
    )

    card_entry = card_repo.get(card)
    card_points_default = card_entry.points_default if card_entry else None

    if not actives:
        # No active promo → no cashback. But the exclusions that withdraw
        # *points* are not promo-driven, so they must still fire here — a row
        # has to classify the same way whether or not a promo happens to be
        # active on its card. Order mirrors the promo path below:
        # foreign-in-THB first, then petrol.
        #
        # The foreign-in-THB check was missing until 2026-08-31, which left
        # every foreign row on a promo-less card sitting at the card's default
        # multiplier instead of ×0 (found on Baiboon's
        # `[บัตรหลัก] AGODA.COM SL CNX-DMK INTERNET SG`, First Choice — a card
        # with no active promo). Cashback was unaffected either way (None
        # here regardless), so the bug was points-only.
        if looks_foreign_in_thb(merchant_name):
            return Classification(
                cashback_percent=None,
                note="Foreign merchant in THB — no cashback / points by default rule.",
                points_override="×0",
                promotion_id=None,
                reason="foreign-default-exclude",
            )
        if (_card_excludes_petrol(card) and looks_petrol(merchant_name)):
            return Classification(
                cashback_percent=None,
                note=f"Petrol station — {card} earns no cashback / points at fuel merchants.",
                # Petrol withdraws BOTH axes, so the multiplier is forced to ×0
                # rather than inheriting the card's default earning tier.
                points_override="×0",
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
    if (_card_excludes_petrol(card) and looks_petrol(merchant_name)):
        return Classification(
            cashback_percent=None,
            note=f"Petrol station — {card} earns no cashback / points at fuel merchants.",
            # As above: ×0 on both axes. Inheriting `promo.points_default` would
            # hand a petrol row the promo's boosted tier (e.g. UOB World's ×5),
            # contradicting the note this same branch writes.
            points_override="×0",
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
