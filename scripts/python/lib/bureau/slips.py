"""SlipCreditPromotion — a fixed credit per qualifying slip, until a pooled cap (SUP1, PTT2, IS3).

deterministic + idempotent — pure functions of the transactions handed in.

The bank looks at each sales slip on its own: ฿1,500–3,999 at a supermarket
earns ฿35 and ฿4,000 or more earns ฿120 (SUP1); a PTT fill-up of ฿1,200 or
more earns ฿60 (PTT2). Slips never add up. What the period's slips earn is then
capped per primary card account, and the cap is claimed first come, first
served, like any credit cap. A subclass states `slip_credit`.
"""

from __future__ import annotations

from abc import abstractmethod
from decimal import Decimal

from .base import Tx
from .capped import CreditCapPromotion

_ONE = Decimal(1)


class SlipCreditPromotion(CreditCapPromotion):
    # A fixed ฿120 on a ฿4,045.50 slip isn't a rate: `% cb` stays as the household
    # keeps it, and the money lives in the Bureau's shares and the trackers.
    marks_rows = False
    split_text = (
        "Linked rows (รายการใช้จ่ายจาก…) are what the household counts toward this quota.",
        "Each slip earns its own fixed credit; slips never add up to a bigger tier.",
        "The period's credits are capped per primary card account, first come, first served by "
        "Transaction Datetime: slips after the cap is full earn nothing.",
    )

    @abstractmethod
    def slip_credit(self, tx: Tx) -> Decimal | None:
        """What one slip earns on its own, or None when it doesn't qualify."""

    def rate(self, tx: Tx) -> Decimal | None:
        # The cap walk asks for a rate; a slip's credit is fixed, so `line_credit` returns it whole.
        return _ONE if self.slip_credit(tx) is not None else None

    def line_credit(self, tx: Tx, rate: Decimal) -> Decimal:
        return (self.slip_credit(tx) or Decimal(0)) * rate
