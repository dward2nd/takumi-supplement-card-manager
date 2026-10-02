"""SlipCountPromotion — fixed credits for the Nth qualifying slip in a period (Krungsri EAT).

deterministic + idempotent — pure functions of the transactions handed in.

Some campaigns count slips, not baht: the month's first qualifying slip earns
฿100, and the third earns another ฿100 (EAT). A subclass states
`milestones` — {n: credit} — and what makes a slip qualify. Slips are counted
first come, first served by `Transaction Datetime`, so the milestone credit
goes to whoever's slip reached it.
"""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from .base import Allocation, CashbackPromotion, Tx, TxCredit


class SlipCountPromotion(CashbackPromotion):
    milestones: ClassVar[dict[int, Decimal]]   # the nth qualifying slip → its credit
    marks_rows = False   # a milestone credit isn't a rate on the slip
    split_text = (
        "Linked rows (รายการใช้จ่ายจาก…) are the slips the household counts toward this campaign.",
        "Slips are counted first come, first served by Transaction Datetime; each milestone's "
        "credit goes to whoever's slip reached it.",
    )

    def counts_linked(self, tx: Tx) -> bool:
        return self.qualifies(tx)

    def split(self, txs: list[Tx]) -> Allocation:
        seen = [0]

        def take(lo: Decimal, hi: Decimal, grp: list[Tx]) -> list[TxCredit]:
            out = []
            for t in sorted(grp, key=lambda t: (-t.amount, t.id)):
                seen[0] += 1
                credit = self.milestones.get(seen[0], Decimal(0))
                out.append(TxCredit(t, t.amount if credit else Decimal(0), credit))
            return out

        rows, boundary, warnings = self._walk([t for t in txs if self.counts_linked(t)], take)
        credit = sum((r.credit for r in rows), Decimal(0))
        return self._allocation(rows, boundary, warnings, credit=credit)
