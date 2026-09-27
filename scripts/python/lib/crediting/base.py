"""Crediting — the ledger rows that pay a card's cashback back to a holder.

deterministic + idempotent — `plan` reads (and may link Bureau rows, which is a
no-op once linked); `post` writes the planned rows, and a posted period is
recognised and skipped on the next run.

Banks credit cashback on their own schedule (UOB One: 1% at the statement
date, 10%/5% on the last day of each month), so how a card's credit rows are
built is a class per card. A subclass plans the rows; the shared `post` writes
them as negative-amount, ×0 transactions on the holder's card.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import ClassVar

from .. import notion_client
from ..holders import Holder
from ..transaction_write import build_transaction_properties


@dataclass(frozen=True)
class CreditRow:
    name: str            # verbatim, statement-style: `UOB ONE CASHBACK 5%`
    amount: Decimal      # negative: it reduces the bill
    date: str            # when the bank credits it
    bill_cycle: str
    due_date: str
    note: str


@dataclass
class CreditPlan:
    holder: str
    card: str
    rows: list[CreditRow] = field(default_factory=list)
    already_posted: list[str] = field(default_factory=list)  # periods skipped as done
    detail: dict = field(default_factory=dict)                # per-period working, for the envelope


class Crediting(ABC):
    card: ClassVar[str]
    multiplier: ClassVar[str | None] = "×0"   # a credit row earns nothing

    @abstractmethod
    def plan(self, holder: Holder, card_page_id: str, spec: dict, write) -> CreditPlan:
        """The credit rows due for the periods the spec names (or the latest ones)."""

    def post(self, holder: Holder, card_page_id: str, plan: CreditPlan) -> list[dict]:
        created = []
        for row in plan.rows:
            page = notion_client.create_page(holder.transactions_ds, build_transaction_properties(
                name=row.name, amount=float(row.amount), transaction_date=row.date,
                bill_cycle_date=row.bill_cycle, due_date=row.due_date, card_page_id=card_page_id,
                processed=True, note=row.note, multiplier=self.multiplier))
            created.append({"name": row.name, "amount": float(row.amount), "date": row.date,
                            "bill_cycle": row.bill_cycle, "id": page["id"]})
        return created
