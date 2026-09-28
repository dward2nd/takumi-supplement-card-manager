"""UOB One crediting — the household's per-bill-cycle agreement.

deterministic + idempotent — see lib/crediting/base.py.

How the household credits UOB One cashback to Baiboon and Nuta (user,
2026-05-25; kept 2026-09-28 as the agreement between them, even though UOB
itself counts 10%/5% per calendar month — the Promotion Bureau shows the
bank's view):

  For one holder's bill cycle, sum `ยอดชำระ` per `% cb` tier over the cycle's
  rows and write one negative credit row per tier:
    1%        `UOB ONE CASHBACK 1%`, dated the BC date
    10% / 5%  `UOB ONE CASHBACK 10%` / `5%`, dated the first weekday of the
              next month
  all billed on that cycle (BC/DD forced to it), ×0, Note with the working.

Summing the rows' own `% cb` nets carry-forward legs by construction (Nuta's
−฿231 at 1% takes ฿2.31 off the 1% credit). The cycle's in-progress
installment terms are populated first, since each earns 1%.
"""

from __future__ import annotations

import datetime as dt
from decimal import ROUND_HALF_UP, Decimal

from .. import bill_cycle, installments
from ..holders import Holder
from ..ledger import cycle_rows
from .base import CreditPlan, CreditRow, Crediting

SATANG = Decimal("0.01")


class CreditingError(RuntimeError):
    pass


def _pct(rate: Decimal) -> str:
    """`0.05` → `5%`, `0.1` → `10%` — the statement's spelling."""
    return f"{(rate * 100).normalize():f}%"


def _first_weekday_of_next_month(d: dt.date) -> dt.date:
    first = (d.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
    while first.weekday() >= 5:   # weekends only, no holiday shift — the household's convention
        first += dt.timedelta(days=1)
    return first


class UOBOneCrediting(Crediting):
    card = "UOB One"

    def plan(self, holder: Holder, card_page_id: str, spec: dict, write) -> CreditPlan:
        if holder.statement_bills:
            raise CreditingError(f"{holder.key}'s cashback comes off the bank statement (/record-statement); "
                                 f"there is nothing to post by hand")
        bc = (dt.date.fromisoformat(spec["bill_cycle"]) if spec.get("bill_cycle")
              else bill_cycle.active_cycle(self.card, dt.date.today())[0])
        dd = bill_cycle.due_date_for(self.card, bc)
        plan = CreditPlan(holder.key, self.card, detail={"bill_cycle": bc.isoformat(), "due_date": dd.isoformat()})

        simulated = self._populate_installments(holder, card_page_id, bc, dd, spec, write, plan)
        rows = cycle_rows(holder.transactions_ds, card_page_id, bc.isoformat())
        if not rows and not simulated:
            raise CreditingError(f"no transactions in cycle {bc} for {holder.key}/{self.card}; "
                                 f"nothing to compute cashback against")
        existing = [r["name"] for r in rows if "CASHBACK" in r["name"].upper()]
        if existing and not spec.get("force"):
            raise CreditingError(
                f"{holder.key}/{self.card} cycle {bc} already has CASHBACK rows: {existing}. Pass "
                f"`force: true` to write anyway, after archiving them with add-transaction/archive.py")

        totals: dict[Decimal, Decimal] = {}
        for r in [*rows, *simulated]:
            if "CASHBACK" in r["name"].upper() or r["cashback_percent"] is None or r["amount"] is None:
                continue
            rate = Decimal(str(round(r["cashback_percent"], 4)))
            totals[rate] = totals.get(rate, Decimal(0)) + Decimal(str(r["amount"]))
        plan.detail["tier_totals"] = {str(k): float(v.quantize(SATANG)) for k, v in sorted(totals.items())}

        for rate, total in sorted(totals.items()):
            credit = (rate * total).quantize(SATANG, rounding=ROUND_HALF_UP)
            if total <= 0 or credit <= 0:
                continue
            date = bc if rate == Decimal("0.01") else _first_weekday_of_next_month(bc)
            plan.rows.append(CreditRow(
                name=f"UOB ONE CASHBACK {_pct(rate)}", amount=-credit, date=date.isoformat(),
                bill_cycle=bc.isoformat(), due_date=dd.isoformat(),
                note=f"Cycle {bc} cashback credit: {_pct(rate)} × {total.quantize(SATANG)} = {credit}."))
        return plan

    def _populate_installments(self, holder, card_page_id, bc, dd, spec, write, plan) -> list[dict]:
        """Add this cycle's installment terms first (each earns 1%). A dry run only
        simulates them, so they come back as stand-in rows for the tier sums."""
        if spec.get("skip_populate_installments"):
            return []
        summary = installments.populate_for_cycle(
            holder_key=holder.key, transactions_ds=holder.transactions_ds, card_name=self.card,
            card_page_id=card_page_id, bill_cycle=bc.isoformat(), due_date=dd.isoformat(),
            auto_classify=True, exclude=set(), dry_run=write.dry_run)
        plan.detail["installments"] = summary
        appended = [e for e in summary.get("in_progress", []) if e.get("action") == "appended"]
        write.done += [f"append installment term {e['next_name']} ฿{e['amount']}" for e in appended]
        if not write.dry_run:
            return []   # written: the cycle query sees them
        return [{"name": e["next_name"], "amount": e["amount"],
                 "cashback_percent": (e.get("classification") or {}).get("cashback_percent")} for e in appended]
