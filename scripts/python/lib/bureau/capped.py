"""CreditCapPromotion — each row earns its own rate until a pooled credit cap (UOB One).

deterministic + idempotent — pure functions of the transactions handed in.

Unlike a ladder, the bank pays every qualifying row its rate (10%, 5%, 1% …)
but stops once the period's *credit* reaches a cap shared by everyone on the
account. Rows claim the cap first come, first served; a same-time group that
crosses it shares what's left pro rata by the credit each row would have earned.
"""

from __future__ import annotations

from abc import abstractmethod
from decimal import ROUND_HALF_UP, Decimal
from typing import ClassVar

from .base import SATANG, Allocation, CashbackPromotion, Tx, TxCredit


class CreditCapPromotion(CashbackPromotion):
    cap: ClassVar[Decimal]  # baht of credit per period, pooled across holders
    split_text = (
        "Linked rows (รายการใช้จ่ายจาก…) are what the household counts toward this quota.",
        "Every row earns its own rate until the period's credit reaches the cap; first come, "
        "first served by Transaction Datetime, so rows after the cap is full earn nothing.",
        "Same-date rows count as simultaneous: if they cross the cap together, what's left is "
        "shared pro rata by the credit each would have earned.",
    )

    @abstractmethod
    def rate(self, tx: Tx) -> Decimal | None:
        """The row's rate before the cap, or None when it earns nothing here."""

    def line_credit(self, tx: Tx, rate: Decimal) -> Decimal:
        """What one row earns before the cap. Unrounded by default; a bank that
        rounds per line (UOB) overrides this."""
        return rate * tx.amount

    def qualifies(self, tx: Tx) -> bool:
        return self.rate(tx) is not None

    def counts_linked(self, tx: Tx) -> bool:
        """Does a *linked* row earn? By default what `qualifies`. A campaign whose
        category the merchant string can't always show (restaurants) links only
        what it recognises, and trusts a row the household linked by hand."""
        return self.qualifies(tx)

    def allocate(self, txs: list[Tx]) -> Allocation:
        left = [self.cap]

        def take(lo: Decimal, hi: Decimal, grp: list[Tx]) -> list[TxCredit]:
            want = {t.id: self.line_credit(t, self.rate(t) or Decimal(0)) for t in grp}
            total = sum(want.values(), Decimal(0))
            granted = min(left[0], total)
            left[0] -= granted
            share = granted / total if total else Decimal(0)
            return [TxCredit(t, t.amount * share, want[t.id] * share) for t in grp]

        rows, boundary, warnings = self._walk([t for t in txs if self.counts_linked(t)], take)
        credit = sum((r.credit for r in rows), Decimal(0)).quantize(SATANG, rounding=ROUND_HALF_UP)
        return self._allocation(rows, boundary, warnings, credit=credit)
