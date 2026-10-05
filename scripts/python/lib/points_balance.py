"""Points balance: bring each card's running points to a statement's printed outstanding points.

deterministic + idempotent — `plan` only reads; `apply` writes one row per
(card, statement), and on a re-run updates that row instead of adding another.

A card's `คะแนนสะสม` is the sum of its ledger rows, and a ledger never holds the
account's whole history: Takumi's reset rows zeroed his cards (2026-09-22) and
friends' ledgers start when they did. The statement is the truth. Its total =
the principal's points + the friends' points (user, 2026-09-29).

For every points summary a statement prints (`Statement.rewards`):

  1. the rows it covers are its `PointsAccount`'s (`lib.points_account`) — every
     holder's for a pooled account, the card number's own for a one-PDF-per-card
     issuer — on the card's whole history;
  2. each row is before or after the statement by its `PointsPeriod`: posted
     before the cycle date (UOB) or billed on or before the cycle (the rest);
     `Reset …` rows are always before;
  3. the ledgers' points as of the statement = Σ `คะแนนที่ได้จริง` over the rows
     before it; the difference from the printed outstanding points goes on
     `[ปรับคะแนน] ยอดคะแนนคงเหลือตามใบแจ้งยอด <BC>` in the account holder's
     ledger — ฿0, `×0`, `ใช้คะแนน` = −difference, filed on the statement's cycle.

Rows after the statement (the open cycle, a redemption since) stay on top, so
the card reads the bank's figure plus what has happened since. A later
statement's balance row on the card makes an older statement `superseded`:
the latest one is what counts, and rewriting an older one would shift it.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass, field

from . import notion_client
from . import notion_blocks as nb
from .cards import CardNotFoundError, find_card
from .holders import HOLDERS
from .ledger import card_rows
from .points import as_points
from .points_account import BALANCE_ADJUSTMENT, RESET, account_for, balance_row_name, period_for
from .statements.model import Statement
from .statements.parser import StatementParser
from .transaction_write import build_transaction_properties


@dataclass
class BalancePlan:
    number: str
    program: str
    status: str                      # ok | create | update | superseded | unmapped | no-outstanding
    card: str | None = None
    holder: str | None = None        # whose card number the summary is printed for
    account_holder: str | None = None  # whose ledger carries the balance row
    statement_date: str | None = None
    printed: float | None = None     # outstanding points, as printed
    ledger: float = 0                # the covered rows' points as of the statement
    by_holder: dict[str, float] = field(default_factory=dict)
    since: float = 0                 # points on the covered rows after the statement
    adjust: float = 0                # the balance row's points (−ใช้คะแนน); coins keep their fraction
    row_id: str | None = None        # the balance row, existing or written
    was: float | None = None         # an existing row's points before an update
    reason: str | None = None
    note: str | None = None
    due_date: str | None = None

    @property
    def balance_now(self) -> float | None:
        return None if self.printed is None else self.printed + self.since

    def report(self) -> dict:
        out = {k: v for k, v in asdict(self).items() if v not in (None, {}, []) and k not in ("note", "due_date")}
        if self.balance_now is not None:
            out["balance_now"] = self.balance_now
        return out


def _note(p: BalancePlan) -> str:
    split = " + ".join(f"{HOLDERS[h].thai_name} {v:g}" for h, v in p.by_holder.items()) or "no rows"
    return (f"Points balance set to the {p.card} …{p.number} statement of {p.statement_date}: the bank prints "
            f"{p.printed:g} points outstanding; the ledgers held {p.ledger:g} ({split}) as of that statement. "
            f"{p.adjust:+} points here (ใช้คะแนน {-p.adjust}). Statement total = the principal's + friends' points "
            f"(user, 2026-09-29); /sync-points-balance.")


def _plan_one(p: BalancePlan, statement: Statement, parser: StatementParser) -> None:
    account, period = account_for(parser, p.card, p.holder), period_for(parser)
    bc = dt.date.fromisoformat(statement.statement_date)
    name = balance_row_name(statement.statement_date)
    p.account_holder = account.account_holder
    existing, later = None, []
    for h in account.holders():
        try:
            page = find_card(HOLDERS[h].cards_ds, p.card)
        except CardNotFoundError:
            continue
        for r in card_rows(HOLDERS[h].transactions_ds, page["id"]):
            row_name = r["name"] or ""
            if not account.counts(h, row_name):
                continue
            if h == account.account_holder and row_name == name:
                existing = r
                continue
            pts = r["points_realized"] or 0
            if not row_name.startswith(RESET) and period.after_statement(r, p.card, bc):
                p.since += pts
                if row_name.startswith(BALANCE_ADJUSTMENT):
                    later.append(f"{h}: {row_name}")
            else:
                p.ledger += pts
                p.by_holder[h] = p.by_holder.get(h, 0) + pts
    p.adjust = as_points(p.printed - p.ledger)
    if existing is not None:
        p.row_id, p.was = existing["id"], as_points(-(existing["points_redeemed"] or 0))
    if later:
        p.status, p.reason = "superseded", "a later statement's balance row is on the card: " + "; ".join(later)
    elif existing is None:
        p.status = "ok" if p.adjust == 0 else "create"
    else:
        p.status = "ok" if p.was == p.adjust else "update"
    p.note = _note(p)


def plan(statement: Statement, parser: StatementParser, number_lookup) -> list[BalancePlan]:
    """One BalancePlan per points summary the statement prints. Reads only."""
    out = []
    for s in statement.rewards:
        p = BalancePlan(number=s.number, program=s.program, status="", statement_date=statement.statement_date,
                        printed=s.outstanding, due_date=statement.due_date)
        owner = number_lookup(statement.issuer, s.number)
        if owner is None:
            p.status, p.reason = "unmapped", f"card …{s.number} isn't in any {statement.issuer} card's statement_numbers"
        elif s.outstanding is None:
            p.card, p.holder = owner
            p.status, p.reason = "no-outstanding", "the statement prints no outstanding points figure"
        else:
            p.card, p.holder = owner
            _plan_one(p, statement, parser)
        out.append(p)
    return out


def apply(plans: list[BalancePlan]) -> None:
    """Write the `create` / `update` plans' balance rows (sets `row_id`)."""
    for p in plans:
        holder = HOLDERS[p.account_holder] if p.account_holder else None
        if p.status == "create":
            page = notion_client.create_page(holder.transactions_ds, build_transaction_properties(
                name=balance_row_name(p.statement_date), amount=0, transaction_date=p.statement_date,
                bill_cycle_date=p.statement_date, due_date=p.due_date,
                card_page_id=find_card(holder.cards_ds, p.card)["id"], note=p.note, multiplier="×0",
                points_redeemed=-p.adjust))
            p.row_id = page["id"]
        elif p.status == "update":
            notion_client.update_page_properties(p.row_id, {
                "ใช้คะแนน": {"number": -p.adjust}, "Note": {"rich_text": nb.text(p.note)}})
