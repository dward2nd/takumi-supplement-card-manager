"""DrawRightsPromotion — lucky-draw rights per qualifying slip, up to a count per period (BTS).

deterministic + idempotent — pure functions of the transactions handed in.

Some campaigns pay neither cashback nor points but entries into a prize draw:
one right (สิทธิ์) per sales slip of at least a minimum amount, up to a
limit per person per month. There's no money to split and no row field to
set; what the Bureau keeps is how many rights the month earned, and which
slips earned them, first come, first served. The count goes in the Bureau's
`สิทธิ์ลุ้นรางวัล` (draw rights).
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, ClassVar

from .base import RIGHTS, Allocation, BasePromotion, Tx, TxCredit


class DrawRightsPromotion(BasePromotion):
    reward = RIGHTS
    min_slip: ClassVar[Decimal]      # a slip earns a right at this amount or more
    max_rights: ClassVar[int]        # rights per period, per person
    ladder_title = "Draw rights"
    ladder_header = ("Spend", "Rights")
    split_text = (
        "Linked rows (รายการใช้จ่ายจาก…) are the slips the household counts toward the draw.",
        "One right per qualifying slip, first come, first served by Transaction Datetime, until the "
        "month's limit; slips after it earn nothing.",
        "The rights are the primary cardholder's (Takumi's): a supplement's slips count toward the "
        "primary card number. Which holder's slip earned each right is kept for the record only.",
    )

    def qualifies(self, tx: Tx) -> bool:
        return tx.amount >= self.min_slip

    def allocate(self, txs: list[Tx]) -> Allocation:
        left = [self.max_rights]
        warnings: list[str] = []

        def take(lo: Decimal, hi: Decimal, grp: list[Tx]) -> list[TxCredit]:
            # Each slip is its own right. A same-time group bigger than what's left
            # gives the last rights by amount (largest first); a draw can't split one.
            ordered = sorted(grp, key=lambda t: (-t.amount, t.id))
            out = []
            for t in ordered:
                right = left[0] > 0
                left[0] -= right
                out.append(TxCredit(t, t.amount if right else Decimal(0), Decimal(0)))
            if 0 < sum(1 for r in out if r.counted) < len(out):
                warnings.append(f"{grp[0].date[:10]}: {len(grp)} slips at the same time and only "
                                f"{sum(1 for r in out if r.counted)} right(s) left — given to the largest")
            return out

        rows, boundary, w = self._walk([t for t in txs if self.qualifies(t)], take)
        alloc = self._allocation(rows, boundary, warnings + w, credit=Decimal(0))
        for r in rows:
            if r.counted:
                alloc.rights[r.tx.holder] = alloc.rights.get(r.tx.holder, 0) + 1
        return alloc

    def expected(self, r: TxCredit) -> dict[str, Any]:
        return {}   # a right changes nothing on the row
