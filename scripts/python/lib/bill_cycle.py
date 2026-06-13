"""Bill-cycle and due-date inference per card.

deterministic + idempotent — pure function of (card_name, today).

Encodes the per-issuer cycle patterns documented in
``docs/concepts/bill-cycle-patterns.md``. Given a card name and a
reference date, returns (bill_cycle_date, due_date) for the cycle
that's currently active — i.e. the cycle whose bill-cycle date is
the next one on or after today (the upcoming cut-off the bill is
accumulating toward). On the cut-off day itself, that day is still
the active cycle's BC; the day after rolls forward to next month.

UOB has weekend / Thai-public-holiday shifts:
- Bill cycle date (nominal day 25) shifts *earlier* to the closest
  preceding workday if it lands on a non-working day.
- Due date (nominal day 25 + 20 = day 14 of the next month) shifts
  *later* to the closest following workday.
The two shifts are computed independently from the nominal dates.
"""

from __future__ import annotations

import calendar
import datetime as dt
from dataclasses import dataclass, field
from typing import Callable

import holidays

from . import card_repo


_TH_HOLIDAYS = holidays.country_holidays("TH")


def _is_workday(d: dt.date) -> bool:
    return d.weekday() < 5 and d not in _TH_HOLIDAYS


def _shift_earlier(d: dt.date) -> dt.date:
    while not _is_workday(d):
        d -= dt.timedelta(days=1)
    return d


def _shift_later(d: dt.date) -> dt.date:
    while not _is_workday(d):
        d += dt.timedelta(days=1)
    return d


def _identity(d: dt.date) -> dt.date:
    return d


def _add_months(year: int, month: int, delta: int) -> tuple[int, int]:
    n = (year * 12 + (month - 1)) + delta
    return n // 12, (n % 12) + 1


def _safe_day(year: int, month: int, day: int) -> dt.date:
    last = calendar.monthrange(year, month)[1]
    return dt.date(year, month, min(day, last))


def _due_plus(days: int) -> Callable[[dt.date], dt.date]:
    def f(bc: dt.date) -> dt.date:
        return bc + dt.timedelta(days=days)

    return f


def _due_fixed_next_month(day: int) -> Callable[[dt.date], dt.date]:
    """Due date = a fixed calendar `day` of the month *after* the bill cycle.

    Unlike `_due_plus` (a `BC + N days` offset), this pins the due date to a
    constant day-of-month. Used by issuers whose due date is a fixed date
    rather than a grace-period offset (AEON day 2, KBank day 10).
    """

    def f(bc: dt.date) -> dt.date:
        y, m = _add_months(bc.year, bc.month, 1)
        return _safe_day(y, m, day)

    return f


@dataclass(frozen=True)
class BillCyclePattern:
    key: str
    description: str
    bill_day: int
    due_from_nominal_bc: Callable[[dt.date], dt.date]
    bill_cycle_shift: Callable[[dt.date], dt.date] = field(default=_identity)
    due_date_shift: Callable[[dt.date], dt.date] = field(default=_identity)


PATTERNS: dict[str, BillCyclePattern] = {
    "krungsri": BillCyclePattern(
        key="krungsri",
        description="Krungsri / First Choice / CardX — bill cycle day 5, due +20 days",
        bill_day=5,
        due_from_nominal_bc=_due_plus(20),
    ),
    "ktc": BillCyclePattern(
        key="ktc",
        description="KTC — bill cycle day 27, due +15 days",
        bill_day=27,
        due_from_nominal_bc=_due_plus(15),
    ),
    "ttb": BillCyclePattern(
        key="ttb",
        description="ttb — bill cycle day 27, due +20 days",
        bill_day=27,
        due_from_nominal_bc=_due_plus(20),
    ),
    "aeon": BillCyclePattern(
        key="aeon",
        description="AEON — bill cycle day 10, due day 2 of next month",
        bill_day=10,
        due_from_nominal_bc=_due_fixed_next_month(2),
    ),
    "kbank": BillCyclePattern(
        key="kbank",
        description="KBank — bill cycle day 25, due day 10 of next month",
        bill_day=25,
        due_from_nominal_bc=_due_fixed_next_month(10),
    ),
    "lotus": BillCyclePattern(
        key="lotus",
        description="Lotus — bill cycle day 28, due +20 days",
        bill_day=28,
        due_from_nominal_bc=_due_plus(20),
    ),
    "spaylater": BillCyclePattern(
        key="spaylater",
        description="SPayLater — bill cycle day 15, due +10 days",
        bill_day=15,
        due_from_nominal_bc=_due_plus(10),
    ),
    "uob": BillCyclePattern(
        key="uob",
        description=(
            "UOB — bill cycle day 25 (shift earlier on weekend/Thai holiday), "
            "due +20 days from nominal (shift later on weekend/Thai holiday)"
        ),
        bill_day=25,
        due_from_nominal_bc=_due_plus(20),
        bill_cycle_shift=_shift_earlier,
        due_date_shift=_shift_later,
    ),
}


class PatternNotFoundError(LookupError):
    pass


def pattern_for_card(card_name: str) -> BillCyclePattern:
    """Return the bill-cycle pattern that applies to the given card name.

    The card must be registered in `scripts/repositories/cards/<slug>.yaml`
    with a `bill_cycle_pattern` field naming one of `PATTERNS`. To add a
    new card or change its pattern, edit the card's YAML file (no Python
    change needed).
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

    key = card.bill_cycle_pattern
    if key not in PATTERNS:
        raise PatternNotFoundError(
            f"card {card_name!r} declares bill_cycle_pattern={key!r}, "
            f"which is not in lib.bill_cycle.PATTERNS "
            f"({sorted(PATTERNS)}). Fix the YAML or extend PATTERNS."
        )
    return PATTERNS[key]


def cycle_for_month(
    pattern: BillCyclePattern, year: int, month: int
) -> tuple[dt.date, dt.date]:
    """Return (bill_cycle_date, due_date) for the cycle anchored to (year, month).

    `year`/`month` is the calendar month of the *nominal* bill cycle day.
    Shifts (if any) are applied independently to BC and DD.
    """
    nominal_bc = _safe_day(year, month, pattern.bill_day)
    nominal_dd = pattern.due_from_nominal_bc(nominal_bc)
    return pattern.bill_cycle_shift(nominal_bc), pattern.due_date_shift(nominal_dd)


def active_cycle(
    card_name: str, today: dt.date | None = None
) -> tuple[dt.date, dt.date]:
    """Return (bill_cycle_date, due_date) for the cycle currently active.

    Active = the next BC date ≥ today. If today ≤ this month's BC, that BC
    is active; otherwise roll forward to next month. For UOB the comparison
    uses the *shifted* BC.
    """
    if today is None:
        today = dt.date.today()
    pattern = pattern_for_card(card_name)
    bc, dd = cycle_for_month(pattern, today.year, today.month)
    if today <= bc:
        return bc, dd
    y, m = _add_months(today.year, today.month, 1)
    return cycle_for_month(pattern, y, m)


def most_recent_closed_cycle(
    card_name: str, today: dt.date | None = None
) -> tuple[dt.date, dt.date]:
    """Return (bill_cycle_date, due_date) for the most recently closed cycle.

    Closed = the largest BC date strictly less than today. If today > this
    month's BC, that BC is the most recently closed; otherwise step back
    to last month. On the BC date itself the cycle is still active, so we
    step back to the previous month (mirrors `active_cycle`'s "≤" rule).

    Used by installment skills, since banks post installment terms onto
    the cycle that just closed rather than the one currently accumulating.
    """
    if today is None:
        today = dt.date.today()
    pattern = pattern_for_card(card_name)
    bc, dd = cycle_for_month(pattern, today.year, today.month)
    if today > bc:
        return bc, dd
    y, m = _add_months(today.year, today.month, -1)
    return cycle_for_month(pattern, y, m)
