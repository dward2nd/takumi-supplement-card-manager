"""LadderPromotion — cashback paid in steps of pooled spend (NW3, EPW538).

deterministic + idempotent — pure functions of the transactions handed in.

The bank looks at the period's pooled spend and pays per whole step (฿200 per
฿10,000, ฿100 per ฿5,000 …). A subclass states the ladder as `tranches()`:
bands of pooled spend, each paying a fixed credit spread over its baht. Rows
fill the bands first come, first served; spend past the last whole step earns
nothing, whoever it belongs to.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar

from .. import notion_blocks as nb
from .base import Allocation, CashbackPromotion, Tx, TxCredit


@dataclass(frozen=True)
class Tranche:
    """A band of pooled spend, [start, end), that earns `credit` in total.

    The credit is spread evenly over the band's baht, so whoever's spend
    fills the band earns its slice of it.
    """

    start: Decimal
    end: Decimal
    credit: Decimal

    def earned(self, lo: Decimal, hi: Decimal) -> Decimal:
        overlap = min(hi, self.end) - max(lo, self.start)
        return overlap * self.credit / (self.end - self.start) if overlap > 0 else Decimal(0)

    def counted(self, lo: Decimal, hi: Decimal) -> Decimal:
        return max(min(hi, self.end) - max(lo, self.start), Decimal(0))


class LadderPromotion(CashbackPromotion):
    examples: ClassVar[tuple[tuple[int, int], ...]] = ()  # the bank's own (spend, cashback)
    split_text = (
        "Linked rows (รายการใช้จ่ายจาก…) are what the household counts toward this promotion.",
        "First come, first served by Transaction Datetime: only spend inside a paying step earns, "
        "and it goes to whoever spent it first. Spend past the last full step earns nothing.",
        "Same-date rows count as simultaneous (e.g. one bill split across holders): the part inside "
        "the step is shared pro rata by amount.",
    )

    @abstractmethod
    def tranches(self, pooled: Decimal) -> list[Tranche]:
        """The paying bands for one period's pooled spend."""

    def cashback(self, pooled: Decimal) -> Decimal:
        return sum((t.credit for t in self.tranches(pooled)), Decimal(0))

    def allocate(self, txs: list[Tx]) -> Allocation:
        """Fill the tranches first come, first served; a row earns on the part of
        it that lands inside one."""
        pooled = sum((t.amount for t in txs if t.amount > 0), Decimal(0))
        tranches = self.tranches(pooled)

        def take(lo: Decimal, hi: Decimal, grp: list[Tx]) -> list[TxCredit]:
            size = hi - lo
            earned = sum((b.earned(lo, hi) for b in tranches), Decimal(0))
            counted = sum((b.counted(lo, hi) for b in tranches), Decimal(0))
            return [TxCredit(t, counted * t.amount / size, earned * t.amount / size) for t in grp]

        return self._allocation(*self._walk(txs, take), credit=self.cashback(pooled))

    def _ladder_extras(self) -> list[dict]:
        wrong = [(s, want, self.cashback(Decimal(s))) for s, want in self.examples
                 if self.cashback(Decimal(s)) != want]
        if wrong:
            raise AssertionError(f"{type(self).__name__}.tranches disagrees with the bank: {wrong}")
        if not self.examples:
            return []
        return [nb.paragraph(("Bank's examples: ", "b"), " · ".join(
            f"฿{spend:,} → ฿{self.cashback(Decimal(spend)):,.0f}" for spend, _ in self.examples))]
