"""Card — how one card earns: its active promotion, then the card's own rules.

deterministic + idempotent — pure function of (card and promotion YAML, inputs).

Every card runs the same promotion step — the promotion YAML's tiers,
installment rule and foreign-in-THB policy stay data (user, 2026-09-28:
migrate gradually, tier lists stay in YAML). What differs between issuers is
code, one class per family (families.py):

  withholds_fuel()   does fuel earn nothing, on both axes?        (UOB, ttb)
  withholds_top_ups()  do e-wallet top-ups earn nothing, on both axes?  (UOB)
  after_rules()      points-only rules layered on top, in order   (Krungsri family, AEON)

Classification order (unchanged from lib.promotions before 2026-09-28):
  no active promotion: foreign-in-THB → ×0; withheld fuel → ×0; else the
    card's `points_default`
  a promotion: its installment rule; foreign-in-THB (overrides, or ×0);
    withheld fuel; the first matching tier; else nothing
  then the card's after_rules (e.g. installment rewards paid upfront, then
    7-11/TrueMoney points, then MCC points exclusions).
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Callable

from .. import promotions as promos
from ..card_repo import CardRepo
from ..promotions import Classification, Promotion

AfterRule = Callable[[Classification, dt.date, str, bool], Classification]


class Card:
    """A card with no rules of its own beyond its promotions."""

    def __init__(self, name: str, repo: CardRepo | None):
        self.name, self.repo = name, repo

    @property
    def points_default(self) -> str | None:
        return self.repo.points_default if self.repo else None

    # -- hooks a family overrides ------------------------------------------------

    def withholds_fuel(self) -> bool:
        return False

    def withholds_top_ups(self) -> bool:
        return False

    def after_rules(self) -> list[AfterRule]:
        return []

    # -- the template ------------------------------------------------------------

    def classify(self, date: dt.date, merchant: str, *, is_installment_override: bool | None = None,
                 promotions: list[Promotion] | None = None) -> Classification:
        inst = promos.is_installment(merchant) if is_installment_override is None else is_installment_override
        result = self._promotion_step(date, merchant, inst, promotions)
        for rule in self.after_rules():
            result = rule(result, date, merchant, inst)
        return result

    def _promotion_step(self, date: dt.date, merchant: str, inst: bool,
                        promotions: list[Promotion] | None) -> Classification:
        actives = promos.active_for_card_date(self.name, date, promotions=promotions)
        if not actives:
            # No promotion → no cashback. The points-withdrawing exclusions aren't
            # promo-driven, so they still fire: a row classifies the same way
            # whether or not a promotion happens to be active on its card.
            if promos.looks_foreign_in_thb(merchant):
                return _foreign_excluded(None)
            if self.withholds_fuel() and promos.looks_petrol(merchant):
                return self._fuel_excluded(None)
            if self.withholds_top_ups() and promos.looks_wallet_top_up(merchant):
                return self._top_up_excluded(None)
            return Classification(None, None, self.points_default, None, "no-promo")

        # Several at once is rare; the most recent start wins.
        promo = sorted(actives, key=lambda p: p.effective_start, reverse=True)[0]
        points = promo.points_default or self.points_default

        if inst and promo.installment_rule:
            rate = promo.installment_rule.rate
            return Classification(
                rate if rate > 0 else None,
                f"Installment transaction — per {promo.name}, {rate * 100:.0f}% per installment row.",
                points, promo.id, "installment")

        if promos.looks_foreign_in_thb(merchant) and promo.foreign_in_thb_policy.default == "exclude":
            for ov in promo.foreign_in_thb_policy.overrides:
                if ov.merchant_substring.upper() in merchant.upper():
                    return Classification(
                        ov.rate if ov.rate > 0 else None,
                        (f"Per {promo.name}: {ov.rate * 100:.2f}% on {ov.merchant_substring!r} "
                         f"(promo override of foreign-in-THB rule). "
                         + ("Points still excluded (×0) — promo did not override."
                            if ov.keeps_points_exclusion else "")).strip(),
                        "×0" if ov.keeps_points_exclusion else promo.points_default,
                        promo.id, "foreign-override")
            return _foreign_excluded(promo.id)
        # (policy "apply": tiers apply to foreign-in-THB rows too)

        if self.withholds_fuel() and promos.looks_petrol(merchant):
            return self._fuel_excluded(promo.id)
        if self.withholds_top_ups() and promos.looks_wallet_top_up(merchant):
            return self._top_up_excluded(promo.id)

        for tier in promo.tiers:
            if promos.matches_tier(merchant, tier):
                return Classification(tier.rate if tier.rate > 0 else None, None, points, promo.id, "tier")
        return Classification(None, None, points, promo.id, "no-tier-match")

    def _fuel_excluded(self, promotion_id: str | None) -> Classification:
        # Both axes: ×0 rather than the card's or promotion's earning tier, which
        # would hand a petrol row e.g. UOB World's ×5.
        return Classification(
            None, f"Petrol station — {self.name} earns no cashback / points at fuel merchants.",
            "×0", promotion_id, "petrol-exclusion")


    def _top_up_excluded(self, promotion_id: str | None) -> Classification:
        return Classification(
            None, f"E-wallet top-up — {self.name} earns no cashback / points on wallet top-ups.",
            "×0", promotion_id, "top-up-exclusion")


def _foreign_excluded(promotion_id: str | None) -> Classification:
    return Classification(None, "Foreign merchant in THB — no cashback / points by default rule.",
                          "×0", promotion_id, "foreign-default-exclude")


def with_points_withheld(result: Classification, note: str, tag: str) -> Classification:
    """`result` with points forced to ×0 and the reason appended; cashback untouched."""
    return Classification(result.cashback_percent, f"{result.note} {note}".strip() if result.note else note,
                          "×0", result.promotion_id, f"{result.reason}+{tag}")
