"""Points accounts and periods: which ledger rows a printed points summary covers.

deterministic + idempotent — pure classes; reads nothing.

A statement's points summary is printed for one card number, but the points on
it can sit in several ledgers. What the summary covers is a `PointsAccount`,
one class per shape:

  - `PooledAccount` — the bank pools points on the account (UOB, KBank,
    Krungsri, Lotus's): every holder's rows on the card count, and the
    household's adjustments go on the principal's ledger.
  - `PrincipalCardAccount` — one statement per card number (KTC, CardX), the
    principal's own card: the principal's rows plus friends' `[บัตรหลัก]`
    shares on it; adjustments on the principal's ledger.
  - `SupplementCardAccount` — one statement per card number, a supplement's own
    card: that holder's rows except their `[บัตรหลัก]` shares, which belong to
    the principal's statement; adjustments on that holder's ledger.

When the bank credits a row's points is a `PointsPeriod` (the parser's
`points_timing`): `PostingPeriod` — as each charge posts (UOB) — or
`CyclePeriod` — at the statement, for what's billed on it (the rest).

Statement total = the principal's points + the friends' points (user,
2026-09-29): the rows an account covers are exactly the ones that add up to the
printed figure.
"""

from __future__ import annotations

import datetime as dt
from abc import ABC, abstractmethod

from .bill_cycle import posting_date
from .holders import HOLDERS, primary
from .ledger import PRIMARY_PREFIX

# Ledger bookkeeping rows — never points earned in the cycle they're filed on.
RESET = "Reset "
# A card's running points set to a statement's printed outstanding points
# (/sync-points-balance): an opening balance, one row per card per statement.
BALANCE_ADJUSTMENT = "[ปรับคะแนน] ยอดคะแนนคงเหลือ"


def balance_row_name(statement_date: str) -> str:
    return f"{BALANCE_ADJUSTMENT}ตามใบแจ้งยอด {statement_date}"


def is_bookkeeping(name: str | None) -> bool:
    return (name or "").startswith((RESET, BALANCE_ADJUSTMENT))


class PointsAccount(ABC):
    """The ledger rows one printed points summary covers."""

    def __init__(self, card: str, holder: str):
        self.card = card        # the card title, as in the Cards DSes
        self.holder = holder    # who the printed card number belongs to

    @property
    @abstractmethod
    def account_holder(self) -> str:
        """Whose ledger carries the household's adjustments for this account."""

    @abstractmethod
    def holders(self) -> tuple[str, ...]:
        """The holders whose ledgers have rows on this account."""

    @abstractmethod
    def counts(self, holder: str, name: str) -> bool:
        """Does this holder's row (by name) belong to this account?"""


class PooledAccount(PointsAccount):
    @property
    def account_holder(self) -> str:
        return primary().key

    def holders(self) -> tuple[str, ...]:
        return tuple(HOLDERS)

    def counts(self, holder: str, name: str) -> bool:
        return True


class PrincipalCardAccount(PointsAccount):
    @property
    def account_holder(self) -> str:
        return self.holder

    def holders(self) -> tuple[str, ...]:
        return (self.holder, *(h for h in HOLDERS if h != self.holder))

    def counts(self, holder: str, name: str) -> bool:
        return holder == self.holder or (name or "").startswith(PRIMARY_PREFIX)


class SupplementCardAccount(PointsAccount):
    @property
    def account_holder(self) -> str:
        return self.holder

    def holders(self) -> tuple[str, ...]:
        return (self.holder,)

    def counts(self, holder: str, name: str) -> bool:
        return holder == self.holder and not (name or "").startswith(PRIMARY_PREFIX)


def account_for(parser, card: str, holder: str) -> PointsAccount:
    """The account a statement parser's points summary for (card, holder) covers."""
    if not parser.separate_card_statements:
        return PooledAccount(card, holder)
    if holder == primary().key:
        return PrincipalCardAccount(card, holder)
    return SupplementCardAccount(card, holder)


class PointsPeriod(ABC):
    """Which statement a ledger row's points land on."""

    @abstractmethod
    def bill_cycles(self, bc: dt.date, previous_bc: dt.date) -> list[str]:
        """The bill cycles to read for one statement's rows."""

    @abstractmethod
    def in_statement(self, row: dict, card: str, previous_bc: dt.date, bc: dt.date) -> bool:
        """Is this row's points on the statement closing `bc`?"""

    @abstractmethod
    def after_statement(self, row: dict, card: str, bc: dt.date) -> bool:
        """Do this row's points land after the statement closing `bc`?"""


def _billed(row: dict) -> str:
    return (row.get("bill_cycle_date") or "")[:10]


class CyclePeriod(PointsPeriod):
    """Points credited at the statement, for the rows billed on it (KBank, KTC, Krungsri, AEON …)."""

    def bill_cycles(self, bc, previous_bc):
        return [bc.isoformat()]

    def in_statement(self, row, card, previous_bc, bc):
        return _billed(row) == bc.isoformat()

    def after_statement(self, row, card, bc):
        # A row with no bill cycle is old history: before any statement.
        return bool(_billed(row)) and _billed(row) > bc.isoformat()


class PostingPeriod(PointsPeriod):
    """Points credited as each charge posts (UOB): a statement counts the charges
    posted from the previous statement date to the day before its own. Only
    charges post; redemption and adjustment rows (฿0 or less) go by the cycle
    they're billed on."""

    def bill_cycles(self, bc, previous_bc):
        return [bc.isoformat(), previous_bc.isoformat()]

    @staticmethod
    def _posted(row: dict, card: str) -> dt.date | None:
        if (row.get("amount") or 0) <= 0 or not row.get("transaction_date"):
            return None
        return posting_date(card, dt.date.fromisoformat(row["transaction_date"][:10]), row.get("name") or "",
                            row.get("process_date"))

    def in_statement(self, row, card, previous_bc, bc):
        if (row.get("amount") or 0) > 0:
            posted = self._posted(row, card)
            return posted is not None and previous_bc <= posted < bc
        return _billed(row) == bc.isoformat()

    def after_statement(self, row, card, bc):
        posted = self._posted(row, card)
        if posted is not None:
            return posted >= bc
        return bool(_billed(row)) and _billed(row) > bc.isoformat()


_PERIODS: dict[str, PointsPeriod] = {"posting": PostingPeriod(), "cycle": CyclePeriod()}


def period_for(parser) -> PointsPeriod:
    return _PERIODS[parser.points_timing]
