"""UOB One crediting — the bank's periods, the pooled caps, and the household's nets.

deterministic + idempotent — see lib/crediting/base.py.

UOB pays (bank page, read 2026-09-28):
  1%     for each statement cycle, at the statement date      → `UOB ONE CASHBACK 1%`
  10%/5% for each calendar month, on its last day (the next   → `UOB ONE CASHBACK 10%` / `5%`
         working day if that's a weekend or holiday)
and caps both, pooled across everyone on the account. So the amounts come
from the Promotion Bureau's UOB One classes, first come, first served over the
account's linked rows; this module only turns a holder's share into rows.

Two household rules on top (user, 2026-09-28):
  - A carry-forward leg carrying `% cb` (Nuta's −฿231 at 1%) nets out of the
    credit: that cashback already reached the holder in an earlier period.
  - 10%/5% used to be credited per bill cycle (`Cycle <BC> cashback credit`).
    A row already covered that way is never credited again, so the first
    monthly run only pays for what the per-cycle credits didn't cover.
"""

from __future__ import annotations

import calendar
import datetime as dt
from decimal import ROUND_HALF_UP, Decimal

from .. import bill_cycle, installments, notion_client
from ..bureau import Tx, sync
from ..bureau.uob_one import UOBOneBase, UOBOneBonus
from ..holders import Holder
from ..transaction_read import project_transaction
from .base import CreditPlan, CreditRow, Crediting

SATANG = Decimal("0.01")


class CreditingError(RuntimeError):
    pass


def _pct(rate: Decimal) -> str:
    """`0.05` → `5%`, `0.1` → `10%` — the statement's spelling."""
    return f"{(rate * 100).normalize():f}%"


class UOBOneCrediting(Crediting):
    card = "UOB One"

    def plan(self, holder: Holder, card_page_id: str, spec: dict, write) -> CreditPlan:
        if holder.statement_bills:
            raise CreditingError(f"{holder.key}'s cashback comes off the bank statement (/record-statement); "
                                 f"there is nothing to post by hand")
        today = dt.date.today()
        cycles = [dt.date.fromisoformat(spec["bill_cycle"])] if spec.get("bill_cycle") else []
        months = [tuple(int(x) for x in spec["month"].split("-"))] if spec.get("month") else []
        if not cycles and not months:
            cycles = [bill_cycle.most_recent_closed_cycle(self.card, today)[0]]
            last = today.replace(day=1) - dt.timedelta(days=1)
            months = [(last.year, last.month)]

        plan = CreditPlan(holder.key, self.card)
        posted = self._posted(holder, card_page_id)
        for bc in cycles:
            self._plan_cycle(plan, holder, card_page_id, bc, posted, spec, write)
        for y, m in months:
            self._plan_month(plan, holder, y, m, posted, spec, write)
        return plan

    # -- 1%, per statement cycle ------------------------------------------------

    def _plan_cycle(self, plan, holder, card_page_id, bc, posted, spec, write) -> None:
        title = "UOB ONE CASHBACK 1%"
        if any(p["name"] == title and p["bill_cycle"] == bc.isoformat() for p in posted) and not spec.get("force"):
            plan.already_posted.append(f"1% for the cycle closing {bc}")
            return
        dd = bill_cycle.due_date_for(self.card, bc)
        simulated = self._populate_installments(holder, card_page_id, bc, dd, spec, write)
        promo = UOBOneBase()
        row = sync.ensure_row(f"{bc.year}M{bc.month} — UOB One cb 1%", bill_cycle.cycle_start(self.card, bc), bc, write)
        txs, _, adjustments, _ = sync.collect(row, promo, sync.campaign_cards(promo), link=True, write=write)
        alloc = promo.allocate(txs + simulated)
        credit = sum((r.credit for r in alloc.rows if r.tx.holder == holder.key), Decimal(0))
        adjust = promo.adjustment_for(holder.key, adjustments)
        amount = (credit + adjust).quantize(SATANG, rounding=ROUND_HALF_UP)
        note = (f"Cycle {bc} cashback credit (1%): {holder.key}'s first-come-first-served share of the "
                f"account's 1% (฿{alloc.pooled:,.2f} pooled, ฿{alloc.credit:,.2f} credited, cap ฿2,000)")
        if adjust:
            note += f", less ฿{-adjust:,.2f} already credited through a carry-forward leg"
        plan.detail[f"1% {bc}"] = {"bureau_row": row.name, "share": float(credit.quantize(SATANG)),
                                   "adjustment": float(adjust), "credit": float(amount)}
        if amount > 0:
            plan.rows.append(CreditRow(title, -amount, bc.isoformat(), bc.isoformat(), dd.isoformat(), note + "."))

    def _populate_installments(self, holder, card_page_id, bc, dd, spec, write) -> list[Tx]:
        """Add this cycle's installment terms first (each earns 1%). A dry run only
        simulates them, so they're returned as stand-in rows for the split."""
        if spec.get("skip_populate_installments"):
            return []
        summary = installments.populate_for_cycle(
            holder_key=holder.key, transactions_ds=holder.transactions_ds, card_name=self.card,
            card_page_id=card_page_id, bill_cycle=bc.isoformat(), due_date=dd.isoformat(),
            auto_classify=True, exclude=set(), dry_run=write.dry_run)
        appended = [e for e in summary.get("in_progress", []) if e.get("action") == "appended"]
        write.done += [f"append installment term {e['next_name']} ฿{e['amount']}" for e in appended]
        if not write.dry_run:
            return []   # written: the Bureau sees them as ordinary rows
        return [Tx(id=f"dry-run:{e['next_name']}", holder=holder.key, name=e["next_name"],
                   amount=Decimal(str(e["amount"])), date=bc.isoformat(), card=self.card,
                   bill_cycle=bc.isoformat()) for e in appended]

    # -- 10%/5%, per calendar month ----------------------------------------------

    def _plan_month(self, plan, holder, y, m, posted, spec, write) -> None:
        start, end = dt.date(y, m, 1), dt.date(y, m, calendar.monthrange(y, m)[1])
        marker = f"Month {y}-{m:02d}"
        credit_date = bill_cycle.workday_on_or_after(end)
        bc, dd = bill_cycle.active_cycle(self.card, credit_date)
        promo = UOBOneBonus()
        row = sync.ensure_row(f"{y}M{m} — UOB One cb 10%/5%", start, end, write)
        txs, _, adjustments, _ = sync.collect(row, promo, sync.campaign_cards(promo), link=True, write=write)
        alloc = promo.allocate(txs)
        by_cycle = self._cycle_credited(posted)

        for rate in sorted(promo.tiers, reverse=True):
            title = f"UOB ONE CASHBACK {_pct(rate)}"
            if any(p["name"] == title and p["note"].startswith(marker) for p in posted) and not spec.get("force"):
                plan.already_posted.append(f"{_pct(rate)} for {y}-{m:02d}")
                continue
            mine = [r for r in alloc.rows if r.tx.holder == holder.key and promo.rate(r.tx) == rate]
            covered = [r for r in mine if (title, r.tx.bill_cycle) in by_cycle]
            credit = sum((r.credit for r in mine if r not in covered), Decimal(0))
            adjust = sum((t.amount * t.cb for t in adjustments
                          if t.holder == holder.key and t.cb == rate), Decimal(0))
            amount = (credit + adjust).quantize(SATANG, rounding=ROUND_HALF_UP)
            note = (f"{marker} cashback credit ({_pct(rate)}): {holder.key}'s first-come-first-served "
                    f"share of the account's 10%/5% (฿{alloc.credit:,.2f} credited, cap ฿500)")
            if covered:
                note += (f"; {len(covered)} row(s), ฿{sum(r.tx.amount for r in covered):,.2f}, already "
                         f"credited per bill cycle before the switch to calendar months")
            if adjust:
                note += f", less ฿{-adjust:,.2f} already credited through a carry-forward leg"
            plan.detail[f"{_pct(rate)} {y}-{m:02d}"] = {
                "bureau_row": row.name, "share": float(sum((r.credit for r in mine), Decimal(0)).quantize(SATANG)),
                "covered_per_cycle": float(sum((r.credit for r in covered), Decimal(0)).quantize(SATANG)),
                "adjustment": float(adjust), "credit": float(amount), "date": credit_date.isoformat()}
            if amount > 0:
                plan.rows.append(CreditRow(title, -amount, credit_date.isoformat(), bc.isoformat(),
                                           dd.isoformat(), note + "."))

    # -- what's already on the ledger -----------------------------------------------

    def _posted(self, holder: Holder, card_page_id: str) -> list[dict]:
        pages = notion_client.query_all(holder.transactions_ds, filter={"and": [
            {"property": "Card", "relation": {"contains": card_page_id}},
            {"property": "Name", "title": {"contains": "CASHBACK"}},
        ]})
        out = []
        for pg in pages:
            t = project_transaction(pg)
            out.append({"name": t["name"].strip().upper(), "bill_cycle": t["bill_cycle_date"], "note": t["note"]})
        return out

    @staticmethod
    def _cycle_credited(posted: list[dict]) -> set[tuple[str, str]]:
        """(title, BC) pairs credited under the old per-cycle rule (`Cycle <BC> …`)."""
        return {(p["name"], p["bill_cycle"]) for p in posted if p["note"].startswith("Cycle ")}

