"""Card families — the issuer rules that aren't promotions.

deterministic + idempotent — pure functions of the inputs and the card YAML.

Each family states its rules as code, replacing the YAML flags that used to
switch them on (`petrol_exclusion`, `truemoney_711_points_exclusion`,
`installment_rewards_upfront`, `installment_note` — retired 2026-09-28).
Which card belongs to which family is the registry in `__init__.py`.
"""

from __future__ import annotations

import datetime as dt

from .. import promotions as promos
from ..promotions import Classification
from .base import AfterRule, Card, with_points_withheld


class FuelWithheldCard(Card):
    """Fuel earns nothing on either axis — cashback and points both."""

    def withholds_fuel(self) -> bool:
        return True


class UOBCard(FuelWithheldCard):
    """UOB One, World, Premier, Makro (petrol withheld: confirmed per card, 2026-05/08)."""


class TTBCard(FuelWithheldCard):
    """ttb so smart: petrol withheld like UOB's."""


class KrungsriFamilyCard(Card):
    """Krungsri's own cards: First Choice, Krungsri JCB/Lady/NOW/Visa, Central The 1 Redz.

    Two rules on top of any promotion:
      - An installment purchase's points and cashback are paid in full at
        purchase (user, 2026-08-10), so each `NN/NN` term earns nothing —
        unless a promotion rules installments itself (reason `installment`),
        which is the more specific fact (First Choice's U Plan).
      - 7-Eleven and TrueMoney earn no *points* (user, 2026-08-08; rows from
        2026-08-01). Cashback promotions are unaffected.
    Lotus's Beyond (a Krungsri partner card) is deliberately not in the family:
    7-Eleven, TrueMoney and Lotus's are all CP ALL, so they keep earning there.
    """

    def installment_note(self) -> str:
        return (f"Installment term — {self.name} grants points and cashback upfront at "
                f"purchase, so individual terms earn nothing.")

    def after_rules(self) -> list[AfterRule]:
        # Upfront first: it sets ×0, which the TrueMoney rule then sees and skips,
        # so an installment row at a TrueMoney merchant carries one explanation.
        return [self._installment_rewards_upfront, self._truemoney_711_points, *super().after_rules()]

    def _installment_rewards_upfront(self, result: Classification, date: dt.date, merchant: str,
                                     inst: bool) -> Classification:
        if not inst or result.reason.startswith("installment"):
            return result
        note = self.installment_note()
        return Classification(None, f"{result.note} {note}".strip() if result.note else note, "×0",
                              result.promotion_id, f"{result.reason}+installment-rewards-upfront")

    def _truemoney_711_points(self, result: Classification, date: dt.date, merchant: str,
                              inst: bool) -> Classification:
        if not promos.looks_truemoney_or_711(merchant) or result.points_override == "×0":
            return result
        return with_points_withheld(
            result, "7-11 / TrueMoney — Krungsri-family cards earn no reward points at these merchants.",
            "truemoney-711-points-exclusion")


class KrungsriJCB(KrungsriFamilyCard):
    """Krungsri's year-long Thai-petrol campaign withholds reward *points* on fuel
    (user, 2026-09-27; seen on BSRC-… and BANGCHAK-… rows). Points only — the
    card's cashback arrives as campaign credit rows, never `% cb` — so not the
    UOB/ttb rule, which zeroes both axes."""

    def after_rules(self) -> list[AfterRule]:
        return [*super().after_rules(), self._petrol_points]

    def _petrol_points(self, result: Classification, date: dt.date, merchant: str,
                       inst: bool) -> Classification:
        if not promos.looks_petrol(merchant) or result.points_override == "×0":
            return result
        return with_points_withheld(
            result, "Petrol station — Krungsri's year-long Thai-petrol campaign withholds reward points "
                    "on fuel spend.", "petrol-points-exclusion")


class FirstChoice(KrungsriFamilyCard):
    """A merchant installment books to First Choice's personal-loan line, not the
    card line, so the reason its terms earn nothing is different (user, 2026-08-10)."""

    def installment_note(self) -> str:
        return ("Installment term — booked against First Choice's personal-loan credit line, "
                "which earns no card points or cashback.")


class AEONCard(Card):
    """AEON withholds points by MCC from 2025-11-11. A merchant string doesn't
    carry its MCC, so the card YAML lists the strings known to bill under an
    excluded code (`points_excluded_merchants`: prefix, date, note); `*` means
    every merchant (AEON Rabbit)."""

    def after_rules(self) -> list[AfterRule]:
        return [*super().after_rules(), self._merchant_points_exclusions]

    def _merchant_points_exclusions(self, result: Classification, date: dt.date, merchant: str,
                                    inst: bool) -> Classification:
        if not self.repo or result.points_override == "×0":
            return result
        name = merchant.strip().removeprefix("[บัตรหลัก]").strip().upper()
        for ex in self.repo.points_excluded_merchants:
            if date >= ex.effective_from and (ex.prefix == "*" or name.startswith(ex.prefix.upper())):
                return with_points_withheld(result, ex.note, "merchant-points-exclusion")
        return result
