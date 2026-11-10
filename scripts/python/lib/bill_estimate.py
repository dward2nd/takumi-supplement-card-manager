"""Estimate a statement-driven bill from the three ledgers, before the statement.

deterministic + idempotent — reads only.

Takumi's bill is the bank's printed card total: his principal section plus
every supplement section (docs/databases/takumi-bills.md). Every statement
line lives in exactly one ledger, so until the PDF lands the total can be
estimated by adding up, across all three holders, the rows on that card and
cycle that stand for statement lines. One thing no ledger holds is added from
outside: an `unmonitored` supplement's total (Lotus's 6524), which the user
reads off the bank's app and the caller passes in.

What counts, per holder:

- Takumi: every statement-line row (`is_statement_line_row`), bank credits
  included.
- A friend: their statement-line rows, plus their cashback rows. On these
  cards a friend's cashback row is the bank's credit booked in their ledger
  (Krungsri `CB…`, their share of First Choice's NW3, AEON's `CASH BACK …`),
  so it is on the statement. The exception is a card whose cashback comes back
  as household credit rows (`lib.crediting`: UOB One's computed
  `UOB ONE CASHBACK n%`), which the bank never prints.
- On an issuer that prints one statement per card number (KTC, CardX), a
  friend's own card has its own statement and bill, so only their
  `[บัตรหลัก]` rows sit on Takumi's.

The estimate assumes the previous statement was paid in full. A previous
bill not marked paid is reported, since the bank would carry its balance.

The one exception it handles is a previous statement that closed on a credit
(user, 2026-11-10). Nothing is paid against it, so the bank prints it as the
next statement's BALANCE BROUGHT FORWARD and the total due falls by that much.
The estimate adds it as its own `brought_forward` part. The figure is Takumi's
bill for the previous cycle when there is one. A credit cycle gets no bill, so
otherwise the previous cycle is estimated the same way, going back at most
`CARRY_DEPTH` cycles. A friend's `[ยอดยกมาจากรอบ …]` ± pair records the same
credit in their ledger and stays household bookkeeping: counting it as well
would count the credit twice, and an overpayment pair has the same shape but
the bank never prints it.
(First case: Baiboon's AEON World, 10 Oct 2026 closed at −฿15,701.78.)
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field

from . import card_repo, notion_client
from .bill_cycle import PatternNotFoundError, pattern_for_card
from .bills import bills_for
from .cards import CardNotFoundError, find_card
from .holders import HOLDERS, primary
from .ledger import PRIMARY_PREFIX, cycle_rows, is_cashback_row

UNMONITORED = "unmonitored"   # a statement_numbers value: billed, never recorded
BROUGHT_FORWARD = "brought_forward"   # split key: the previous statement's credit balance
CARRY_DEPTH = 3   # cycles to look back for an unbilled credit balance
NAMES = {h.key: h.thai_name for h in HOLDERS.values()}


class BillEstimateError(ValueError):
    pass


@dataclass
class BillEstimate:
    card: str
    bill_cycle: str
    # holder key (or UNMONITORED, BROUGHT_FORWARD) → that part's subtotal, in HOLDERS order
    split: dict[str, float] = field(default_factory=dict)
    lines: int = 0                      # ledger rows counted
    unmonitored_numbers: tuple[str, ...] = ()
    brought_forward_from: str | None = None   # the credit cycle, when BROUGHT_FORWARD is set
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> float:
        return round(sum(self.split.values()), 2)

    def parts(self) -> list[str]:
        out = []
        for key, amount in self.split.items():
            if key == UNMONITORED:
                label = "unmonitored supplement " + ", ".join(f"…{n}" for n in self.unmonitored_numbers)
            elif key == BROUGHT_FORWARD:
                label = f"credit brought forward from the {self.brought_forward_from} statement"
            else:
                label = NAMES[key]
            out.append(f"{label} ฿{amount:,.2f}")
        return out

    def note(self) -> str:
        note = (f"Estimated from the ledgers before the statement: ฿{self.total:,.2f} = "
                + " + ".join(self.parts()) + ". /record-statement replaces it with the printed total.")
        return " ".join([note, *self.warnings])


def counts_toward(row: dict, holder_key: str, card: str, *, per_number: bool) -> bool:
    """Is this projected row one of the lines on the principal's statement?"""
    from .statements.attribution import is_statement_line_row   # late: statements imports bill-side modules
    from .crediting import CREDITINGS

    friend = holder_key != primary().key
    if friend and per_number and not (row.get("name") or "").startswith(PRIMARY_PREFIX):
        return False
    if is_statement_line_row(row, holder_key):
        return True
    return (friend and card not in CREDITINGS and is_cashback_row(row)
            and is_statement_line_row(row, primary().key))


def unmonitored_numbers(card: str) -> tuple[str, ...]:
    repo = card_repo.get(card)
    return tuple(n for n, h in (repo.statement_numbers if repo else {}).items() if h == UNMONITORED)


def estimate(card: str, bill_cycle: str, *, unmonitored: float | None = None) -> BillEstimate:
    """The principal's statement total for `card`'s cycle, from the ledgers.

    `card` is the card YAML name or a Cards page title; each holder's own page
    for it is looked up by name. `unmonitored` is required for a card with an
    unmonitored supplement (0 if it spent nothing) and refused for any other.
    A credit balance on the previous statement is added (see the module note).
    """
    return _estimate(card, bill_cycle, unmonitored=unmonitored, depth=CARRY_DEPTH)


def _estimate(card: str, bill_cycle: str, *, unmonitored: float | None, depth: int,
              strict: bool = True) -> BillEstimate:
    from .statements import separate_card_statements   # late: see counts_toward

    repo = card_repo.get(card)
    name = repo.name if repo else card
    per_number = bool(repo) and separate_card_statements(repo.issuer)
    est = BillEstimate(name, bill_cycle, unmonitored_numbers=unmonitored_numbers(name))
    for key, holder in HOLDERS.items():
        try:
            page = find_card(holder.cards_ds, name)
        except CardNotFoundError:
            continue
        rows = [r for r in cycle_rows(holder.transactions_ds, page["id"], bill_cycle)
                if counts_toward(r, key, name, per_number=per_number)]
        if rows:
            est.split[key] = round(sum(float(r["amount"]) for r in rows), 2)
            est.lines += len(rows)
    if est.unmonitored_numbers:
        if unmonitored is None and strict:
            raise BillEstimateError(
                f"{name} has an unmonitored supplement ({', '.join('…' + n for n in est.unmonitored_numbers)}) "
                f"that no ledger holds: pass its total for {bill_cycle} as `unmonitored` (0 if it spent nothing)")
        est.split[UNMONITORED] = round(float(unmonitored or 0), 2)
    elif unmonitored is not None:
        raise BillEstimateError(f"{name} has no unmonitored supplement in its card YAML's statement_numbers")
    if depth > 0 and (carried := _brought_forward(name, bill_cycle, depth)) is not None:
        est.brought_forward_from, est.split[BROUGHT_FORWARD] = carried
    return est


def _brought_forward(card: str, bill_cycle: str, depth: int) -> tuple[str, float] | None:
    """(previous BC, its closing balance) when the previous statement closed on a credit.

    Takumi's bill for the previous cycle settles it when there is one: below
    zero is the credit, anything else was due and is assumed paid. With no
    bill, the previous cycle is estimated from the ledgers (its own carry
    included, `depth` cycles back at most). An unmonitored supplement counts
    as ฿0 there, since nobody supplied its figure.
    """
    try:
        prev = pattern_for_card(card).closed(_dt.date.fromisoformat(bill_cycle))[0].isoformat()
    except PatternNotFoundError:
        return None
    holder = primary()
    try:
        page = find_card(holder.cards_ds, card)
    except CardNotFoundError:
        return None
    bills = bills_for(holder.bills_ds, page["id"], prev) if holder.bills_ds else []
    if bills:
        balance = bills[0]["properties"]["ยอดชำระ"]["number"] or 0.0
    else:
        balance = _estimate(card, prev, unmonitored=None, depth=depth - 1, strict=False).total
    return (prev, round(balance, 2)) if balance < -0.005 else None


def previous_bill_warning(bills_ds: str, card_page_id: str, bill_cycle: str) -> str | None:
    """A caveat when the card's previous bill isn't marked paid: the statement would carry it."""
    pages = notion_client.query_page(bills_ds, page_size=1, filter={"and": [
        {"property": "Card", "relation": {"contains": card_page_id}},
        {"property": "วันตัดรอบบิล", "date": {"before": bill_cycle}},
    ]}, sorts=[{"property": "วันตัดรอบบิล", "direction": "descending"}])
    if not pages or pages[0]["properties"]["จ่ายแล้ว"]["checkbox"]:
        return None
    prev = pages[0]["properties"]["วันตัดรอบบิล"]["date"]["start"]
    return (f"The previous bill ({prev}) isn't marked paid; if any of it is still owed, "
            f"the statement carries that balance on top of this estimate.")
