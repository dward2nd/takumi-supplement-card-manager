"""Bill-cycle and due-date inference per card — one class per issuer's rule.

deterministic + idempotent — pure function of (card_name, dates).

Encodes the per-issuer cycle patterns documented in
``docs/concepts/bill-cycle-patterns.md``. Each issuer is a `BillCycle`
subclass: its nominal bill-cycle day, how the due date follows from it,
and (UOB) how either shifts off weekends and Thai public holidays. A card
names its class through `bill_cycle_pattern` in its repository YAML.

Given a card and a reference date, the active cycle is the one whose
bill-cycle date is the next one on or after that date (the cut-off the bill
is accumulating toward). On the cut-off day itself that day is still the
active cycle's BC; the day after rolls forward to next month.

UOB's two shifts are computed independently from the nominal dates:
- the bill cycle (nominal day 25) shifts *earlier* to the closest
  preceding workday;
- the due date (nominal day 25 + 20) shifts *later* to the closest
  following workday.
"""

from __future__ import annotations

import calendar
import datetime as dt
from abc import ABC, abstractmethod
from typing import ClassVar

import holidays

from . import card_repo


_TH_HOLIDAYS = holidays.country_holidays("TH")


def _is_workday(d: dt.date) -> bool:
    return d.weekday() < 5 and d not in _TH_HOLIDAYS


def _add_months(year: int, month: int, delta: int) -> tuple[int, int]:
    n = (year * 12 + (month - 1)) + delta
    return n // 12, (n % 12) + 1


def _safe_day(year: int, month: int, day: int) -> dt.date:
    last = calendar.monthrange(year, month)[1]
    return dt.date(year, month, min(day, last))


class BillCycle(ABC):
    """One issuer's cycle rule. Subclasses set `key`, `description`, `bill_day`
    and the due-date rule; shifts default to none."""

    key: ClassVar[str]
    description: ClassVar[str]
    bill_day: ClassVar[int]

    @abstractmethod
    def due_from_nominal_bc(self, bc: dt.date) -> dt.date:
        """The nominal due date for a nominal bill-cycle date."""

    def bill_cycle_shift(self, d: dt.date) -> dt.date:
        return d

    def due_date_shift(self, d: dt.date) -> dt.date:
        return d

    def cycle(self, year: int, month: int) -> tuple[dt.date, dt.date]:
        """(bill_cycle_date, due_date) for the cycle nominally closing in (year, month)."""
        nominal_bc = _safe_day(year, month, self.bill_day)
        return self.bill_cycle_shift(nominal_bc), self.due_date_shift(self.due_from_nominal_bc(nominal_bc))

    def due_for(self, bc: dt.date) -> dt.date:
        """The due date for a given bill-cycle date. On the pattern: that cycle's
        due date. Off it (a row's BC typed by hand, e.g. a weekend): the due
        date derived from that date by the nominal rule and shift."""
        cand_bc, cand_dd = self.cycle(bc.year, bc.month)
        return cand_dd if cand_bc == bc else self.due_date_shift(self.due_from_nominal_bc(bc))

    def active(self, today: dt.date) -> tuple[dt.date, dt.date]:
        """The cycle whose BC is the next one on or after `today`."""
        bc, dd = self.cycle(today.year, today.month)
        if today <= bc:
            return bc, dd
        return self.cycle(*_add_months(today.year, today.month, 1))

    def closed(self, today: dt.date) -> tuple[dt.date, dt.date]:
        """The cycle whose BC is the last one strictly before `today`."""
        bc, dd = self.cycle(today.year, today.month)
        if today > bc:
            return bc, dd
        return self.cycle(*_add_months(today.year, today.month, -1))


class DueAfterDays(BillCycle):
    """Due a fixed number of days after the bill cycle closes."""

    due_days: ClassVar[int]

    def due_from_nominal_bc(self, bc: dt.date) -> dt.date:
        return bc + dt.timedelta(days=self.due_days)


class DueOnDayOfNextMonth(BillCycle):
    """Due on a fixed calendar day of the month after the bill cycle (AEON, KBank)."""

    due_day: ClassVar[int]

    def due_from_nominal_bc(self, bc: dt.date) -> dt.date:
        return _safe_day(*_add_months(bc.year, bc.month, 1), self.due_day)


class KrungsriCycle(DueAfterDays):
    key, bill_day, due_days = "krungsri", 5, 20
    description = "Krungsri / First Choice / CardX — bill cycle day 5, due +20 days"


class KTCCycle(DueAfterDays):
    key, bill_day, due_days = "ktc", 27, 15
    description = "KTC — bill cycle day 27, due +15 days"


class TTBCycle(DueAfterDays):
    key, bill_day, due_days = "ttb", 27, 20
    description = "ttb — bill cycle day 27, due +20 days"


class AEONCycle(DueOnDayOfNextMonth):
    key, bill_day, due_day = "aeon", 10, 2
    description = "AEON — bill cycle day 10, due day 2 of next month"


class KBankCycle(DueOnDayOfNextMonth):
    key, bill_day, due_day = "kbank", 25, 10
    description = "KBank — bill cycle day 25, due day 10 of next month"


class LotusCycle(DueAfterDays):
    """HISTORICAL — no card points here any more. Lotus's Beyond moved to
    `krungsri` (day 5, +20d) on 2026-08-08; its pre-switch rows still carry BC
    day 28 / DD +20, so the rule is kept for reading that history."""

    key, bill_day, due_days = "lotus", 28, 20
    description = "Lotus (historical, pre-2026-08-08) — bill cycle day 28, due +20 days"


class SPayLaterCycle(DueAfterDays):
    key, bill_day, due_days = "spaylater", 15, 10
    description = "SPayLater — bill cycle day 15, due +10 days"


class GrabCycle(DueAfterDays):
    key, bill_day, due_days = "grab", 1, 6
    description = "Grab PayLater — bill cycle day 1, due day 7 of the same month"


class UOBCycle(DueAfterDays):
    key, bill_day, due_days = "uob", 25, 20
    description = ("UOB — bill cycle day 25 (shift earlier on weekend/Thai holiday), "
                   "due +20 days from nominal (shift later on weekend/Thai holiday)")

    def bill_cycle_shift(self, d: dt.date) -> dt.date:
        while not _is_workday(d):
            d -= dt.timedelta(days=1)
        return d

    def due_date_shift(self, d: dt.date) -> dt.date:
        while not _is_workday(d):
            d += dt.timedelta(days=1)
        return d


PATTERNS: dict[str, BillCycle] = {c.key: c() for c in (
    KrungsriCycle, KTCCycle, TTBCycle, AEONCycle, KBankCycle, LotusCycle, SPayLaterCycle, GrabCycle, UOBCycle)}

BillCyclePattern = BillCycle   # the name callers have typed against


class PatternNotFoundError(LookupError):
    pass


def pattern_for_card(card_name: str) -> BillCycle:
    """The bill-cycle rule that applies to the given card name.

    The card must be registered in `scripts/repositories/cards/<slug>.yaml`
    with a `bill_cycle_pattern` naming one of `PATTERNS`. A new issuer is a
    new `BillCycle` subclass here.
    """
    if not card_name or not card_name.strip():
        raise PatternNotFoundError("card name is required")
    try:
        card = card_repo.by_name(card_name)
    except card_repo.CardRepoNotFoundError as e:
        raise PatternNotFoundError(
            f"no card registered for {card_name!r}. {e}. Add the card to "
            f"scripts/repositories/cards/ (or pass bill_cycle/due_date "
            f"explicitly in the spec)."
        ) from None
    if card.bill_cycle_pattern not in PATTERNS:
        raise PatternNotFoundError(
            f"card {card_name!r} declares bill_cycle_pattern={card.bill_cycle_pattern!r}, "
            f"which is not in lib.bill_cycle.PATTERNS ({sorted(PATTERNS)}). Fix the YAML or "
            f"add a BillCycle subclass.")
    return PATTERNS[card.bill_cycle_pattern]


def cycle_for_month(pattern: BillCycle, year: int, month: int) -> tuple[dt.date, dt.date]:
    """(bill_cycle_date, due_date) for the cycle anchored to (year, month)."""
    return pattern.cycle(year, month)


def active_cycle(card_name: str, today: dt.date | None = None) -> tuple[dt.date, dt.date]:
    """(bill_cycle_date, due_date) for the cycle currently active on the card."""
    return pattern_for_card(card_name).active(today or dt.date.today())


def most_recent_closed_cycle(card_name: str, today: dt.date | None = None) -> tuple[dt.date, dt.date]:
    """(bill_cycle_date, due_date) for the most recently closed cycle on the card.

    Used by installment skills, since banks post installment terms onto the
    cycle that just closed rather than the one currently accumulating.
    """
    return pattern_for_card(card_name).closed(today or dt.date.today())


def due_date_for(card_name: str, bill_cycle: dt.date) -> dt.date:
    """The due date for a bill-cycle date on the card (see `BillCycle.due_for`)."""
    return pattern_for_card(card_name).due_for(bill_cycle)
