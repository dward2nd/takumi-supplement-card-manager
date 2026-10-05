"""Card families — the issuer rules that aren't promotions.

deterministic + idempotent — pure functions of the inputs and the card YAML.

Each family states its rules as code, replacing the YAML flags that used to
switch them on (`petrol_exclusion`, `truemoney_711_points_exclusion`,
`installment_rewards_upfront`, `installment_note` — retired 2026-09-28).
Which card belongs to which family is the registry in `__init__.py`.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import replace

from .. import promotions as promos
from ..ledger import PRIMARY_PREFIX
from ..promotions import Classification
from .base import AfterRule, Card, with_points_withheld


class FuelWithheldCard(Card):
    """Fuel earns nothing on either axis — cashback and points both."""

    def withholds_fuel(self) -> bool:
        return True


class UOBCard(FuelWithheldCard):
    """UOB One, World, Premier, Makro (petrol withheld: confirmed per card, 2026-05/08).
    E-wallet top-ups earn nothing either — UOB's terms exclude them for points and
    cashback (user, 2026-09-28, on `2C2P *SHOPEEPAY (TOP …` rows)."""

    def withholds_top_ups(self) -> bool:
        return True


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


class KrungsriPetrolCampaign(KrungsriFamilyCard):
    """Krungsri's year-long Thai-petrol campaign withholds reward *points* on fuel
    (user, 2026-09-27; seen on BSRC-… and BANGCHAK-… rows). Points only — the
    card's cashback arrives as campaign credit rows (`BANGCHAK SPECIAL DISCOUNT`,
    `CB12_BC3P CAMPAIGN`), never `% cb` — so not the UOB/ttb rule, which zeroes
    both axes. Krungsri JCB, and Krungsri Lady since the Sep 2026 statement paid
    0 points on a ฿800 BANGCHAK row (user, 2026-09-28)."""

    def after_rules(self) -> list[AfterRule]:
        return [*super().after_rules(), self._petrol_points]

    def _petrol_points(self, result: Classification, date: dt.date, merchant: str,
                       inst: bool) -> Classification:
        if not promos.looks_petrol(merchant) or result.points_override == "×0":
            return result
        return with_points_withheld(
            result, "Petrol station — Krungsri's year-long Thai-petrol campaign withholds reward points "
                    "on fuel spend.", "petrol-points-exclusion")


KrungsriJCB = KrungsriPetrolCampaign   # the name the registry first used


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
        name = merchant.strip().removeprefix(PRIMARY_PREFIX).strip().upper()
        for ex in self.repo.points_excluded_merchants:
            if date >= ex.effective_from and (ex.prefix == "*" or name.startswith(ex.prefix.upper())):
                return with_points_withheld(result, ex.note, "merchant-points-exclusion")
        return result


class KTCCard(Card):
    """KTC FOREVER (docs/promotions/ktc-forever.md; KTC's terms, 2026-09-28): no
    points at 7-Eleven in any channel or through TrueMoney (rule 3), nor on public
    transport and expressway tolls (rule 17). Only what the merchant string shows is
    encoded; MCC-only exclusions are marked by hand."""

    def after_rules(self) -> list[AfterRule]:
        return [*super().after_rules(), self._ktc_exclusions]

    def _ktc_exclusions(self, result: Classification, date: dt.date, merchant: str,
                        inst: bool) -> Classification:
        if result.points_override == "×0":
            return result
        reason = self.excluded(merchant.removeprefix(PRIMARY_PREFIX).strip())
        return with_points_withheld(result, f"{reason} — no KTC FOREVER points.", "ktc-points-exclusion") \
            if reason else result

    def excluded(self, merchant: str) -> str | None:
        if promos.looks_truemoney_or_711(merchant):
            return "7-Eleven / TrueMoney"
        if promos.looks_transport_or_toll(merchant):
            return "Public transport or expressway toll"
        return None


class KTCUnionPay(KTCCard):
    """KTC UnionPay adds its own list (rule 16): supermarkets (5411), bakeries,
    fast food, public hospitals, cinemas, education, government… Supermarkets
    show in the name (user, 2026-07: JAMPHA SAVEMART); the others need the MCC."""

    def excluded(self, merchant: str) -> str | None:
        if promos.looks_supermarket(merchant):
            return "Supermarket (KTC UnionPay)"
        return super().excluded(merchant)


class LotussBeyond(Card):
    """Lotus's coins: 0.25 a ฿50 block on every charge, 1.5 at Lotus's — counted
    per statement line (decoded from the 5 Sep 2026 statement). The card's
    `คะแนนต่อ 1 หน่วย` is 0.25 at ฿50 a point, so a Lotus's row is ×6. Lotus's
    Beyond is a Krungsri partner card but not in the family: 7-Eleven, TrueMoney
    and Lotus's are all CP ALL, so they keep earning here.

    The card's coin terms (8 Jul 2025 – 31 Dec 2027, lotussmoney.com/credit-card/
    platinum-beyond, pasted by the user 2026-10-05) withhold coins on a list of
    spend; the ones a merchant string shows are `COIN_EXCLUSIONS`. The rest —
    government MCCs, mutual funds, unit-linked insurance, crypto — are ×0 by hand."""

    AT_LOTUS = re.compile(r"^(LOTUS'?S\b|TMN\*LOTUS HYPER)")
    COIN_EXCLUSIONS: tuple[tuple[str, re.Pattern | None], ...] = (
        ("Bangchak station", re.compile(r"BANGCHAK|^BCP\b|^BSRC\b")),
        ("Phone / internet (MCC 4814)", re.compile(r"\bAIS\b|\bAWN\b|TRUE ?MOVE|TRUE ?ONLINE|TRUE ?ISERVICE|\bDTAC\b")),
        ("Utility bill (MCC 4900)", re.compile(r"การไฟฟ้า|การประปา|\b(MEA|PEA|MWA|PWA)\b|ELECTRICITY AUTH|WATERWORKS")),
        ("Wholesale non-durables (MCC 5199)", re.compile(r"^WWW\.MAKRO\.PRO\b")),
        ("AIA insurance", re.compile(r"\bAIA\b")),
        ("Public transport or expressway toll", None),   # promotions.looks_transport_or_toll
        ("E-wallet top-up", None),                       # promotions.looks_wallet_top_up
    )

    def after_rules(self) -> list[AfterRule]:
        return [*super().after_rules(), self._coin_exclusions, self._at_lotus]

    def coin_exclusion(self, merchant: str) -> str | None:
        """Why the card's coin terms withhold coins on this merchant string, or None."""
        name = merchant.strip().removeprefix(PRIMARY_PREFIX).strip().upper()
        if promos.looks_transport_or_toll(name):
            return "Public transport or expressway toll"
        if promos.looks_wallet_top_up(name):
            return "E-wallet top-up"
        return next((label for label, rx in self.COIN_EXCLUSIONS if rx and rx.search(name)), None)

    def _coin_exclusions(self, result: Classification, date: dt.date, merchant: str,
                         inst: bool) -> Classification:
        if result.points_override == "×0":
            return result
        if inst:
            return with_points_withheld(result, "Installment — no Lotus's coins (card terms).", "lotus-coins-exclusion")
        reason = self.coin_exclusion(merchant)
        return with_points_withheld(result, f"{reason} — no Lotus's coins (card terms).", "lotus-coins-exclusion") \
            if reason else result

    def _at_lotus(self, result: Classification, date: dt.date, merchant: str, inst: bool) -> Classification:
        if result.points_override is not None or inst:
            return result
        if not self.AT_LOTUS.match(merchant.strip().removeprefix(PRIMARY_PREFIX).strip().upper()):
            return result
        return replace(result, points_override="×6", reason=f"{result.reason}+lotus-coins")
