"""How a credit settles a tracker — one class per case.

deterministic + idempotent — pure functions of the context.

Each basis answers one question: do the linked ledger rows account for this
tracker's credit? The cases (docs/databases/cashback-trackers.md):

  ExactCredit   the linked credit equals `Expected Cashback` (a bank `CB…`
                line, a household `UOB ONE CASHBACK 1%` row)
  PooledCredit  Takumi's tracker, settled by the bank's whole-pool credit on
                his card (`UOB One Cashback 10% 5%`): it equals the Bureau
                row's `เงินคืนรวม`, not his share (user, 2026-10-06)
  CycleCredits  a calendar-month tracker paid through per-cycle household
                credits (UOB One 10%/5% for Baiboon and Nuta): settled once a
                linked credit's cycle closes on or after the period's end.
                The amounts differ by design.
  ZeroShare     a ฿0 share with nothing to link (user, 2026-10-25)

`auto` tries ExactCredit, then PooledCredit. The other two change what
"settled" means, so the caller names them.
"""

from __future__ import annotations

import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar

from ..bureau.store import BureauRow
from ..holders import Holder, PrimaryHolder
from .model import LedgerRow, TrackerPage

TOLERANCE = Decimal("0.01")      # Bureau vs bank rounding (Sep 2026: ฿420.96 vs ฿420.95)


@dataclass(frozen=True)
class Context:
    holder: Holder
    tracker: TrackerPage
    rows: tuple[LedgerRow, ...]          # every row in `Slip Transaction` after this call
    bureau: BureauRow | None

    @property
    def credit(self) -> Decimal:
        """The linked credit as a positive figure (credit rows are negative)."""
        return -sum((r.amount for r in self.rows), Decimal(0))


@dataclass(frozen=True)
class Verdict:
    ok: bool
    reason: str


def _baht(x: Decimal | None) -> str:
    return "—" if x is None else f"฿{x:,.2f}"


class Basis(ABC):
    key: ClassVar[str]
    auto: ClassVar[bool] = False

    @abstractmethod
    def check(self, ctx: Context) -> Verdict: ...


class ExactCredit(Basis):
    key = "exact"
    auto = True

    def check(self, ctx: Context) -> Verdict:
        exp = ctx.tracker.expected
        if not ctx.rows:
            return Verdict(False, "no ledger row linked")
        if exp is None or exp <= 0:
            return Verdict(False, f"Expected Cashback is {_baht(exp)}")
        if abs(ctx.credit - exp) <= TOLERANCE:
            return Verdict(True, f"linked credit {_baht(ctx.credit)} = Expected Cashback {_baht(exp)}")
        return Verdict(False, f"linked credit {_baht(ctx.credit)} ≠ Expected Cashback {_baht(exp)}")


class PooledCredit(Basis):
    key = "pooled"
    auto = True

    def check(self, ctx: Context) -> Verdict:
        if not isinstance(ctx.holder, PrimaryHolder):
            return Verdict(False, "only Takumi's tracker is settled by the whole pool")
        if not ctx.rows:
            return Verdict(False, "no ledger row linked")
        total = ctx.bureau.total if ctx.bureau else None
        if total is None:
            return Verdict(False, "no Bureau row with เงินคืนรวม")
        if abs(ctx.credit - total) <= TOLERANCE:
            return Verdict(True, f"linked credit {_baht(ctx.credit)} = the pool's เงินคืนรวม {_baht(total)}")
        return Verdict(False, f"linked credit {_baht(ctx.credit)} ≠ the pool's เงินคืนรวม {_baht(total)}")


class CycleCredits(Basis):
    key = "cycles"

    def check(self, ctx: Context) -> Verdict:
        if ctx.bureau is None:
            return Verdict(False, "no Bureau row: the period's end is unknown")
        cycles = sorted({r.bill_cycle for r in ctx.rows if r.bill_cycle})
        if not cycles:
            return Verdict(False, "no linked credit carries a Bill Cycle Date")
        if cycles[-1] >= ctx.bureau.end:
            return Verdict(True, f"the cycle closing {cycles[-1]} covers the period's end {ctx.bureau.end}")
        return Verdict(False, f"latest linked cycle {cycles[-1]} closes before the period's end "
                              f"{ctx.bureau.end}: wait for the next cycle's credits")


class ZeroShare(Basis):
    key = "zero"

    def check(self, ctx: Context) -> Verdict:
        if ctx.rows:
            return Verdict(False, "a ฿0 share has nothing to link")
        if ctx.tracker.expected != 0:
            return Verdict(False, f"Expected Cashback is {_baht(ctx.tracker.expected)}, not ฿0")
        return Verdict(True, "Expected Cashback is ฿0")


BASES: dict[str, Basis] = {b.key: b for b in (ExactCredit(), PooledCredit(), CycleCredits(), ZeroShare())}


def judge(key: str, ctx: Context) -> tuple[str | None, Verdict]:
    """The basis that holds, and why — or why none does."""
    if key != "auto":
        if key not in BASES:
            raise ValueError(f"basis must be auto or one of {sorted(BASES)}")
        return key, BASES[key].check(ctx)
    reasons = []
    for basis in BASES.values():
        if not basis.auto:
            continue
        verdict = basis.check(ctx)
        if verdict.ok:
            return basis.key, verdict
        reasons.append(f"{basis.key}: {verdict.reason}")
    return None, Verdict(False, "; ".join(reasons))


def period_over(bureau: BureauRow | None, today: dt.date) -> bool:
    """A tracker ticked while its period runs is frozen before a later slip's
    share arrives, so ticking waits for the Bureau row's `End Date`. A tracker
    with no Bureau row has no period to wait for."""
    return bureau is None or bureau.end < today
