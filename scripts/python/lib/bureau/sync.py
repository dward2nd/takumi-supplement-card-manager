"""Collect a Bureau row's transactions: linked rows, candidates, and adjustments.

deterministic + idempotent — reads, plus (only with `link`) linking eligible
candidates, which is a no-op once they're linked.

Shared by /sync-promotion and /post-cashback-credits, so both see the same
rows the same way.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal

from ..holders import HOLDERS
from . import store
from .base import ELIGIBLE, BasePromotion, Tx
from .store import BureauRow

# A dry run over a period with no Bureau row yet runs against this stand-in:
# nothing links to it, so every row in the period comes back as a candidate.
_STAND_IN_ID = "00000000-0000-4000-8000-000000000000"


class Writer:
    """Records every write; performs it unless this is a dry run."""

    def __init__(self, dry_run: bool):
        self.dry_run, self.done = dry_run, []

    def __call__(self, what: str, fn, *args, **kwargs) -> None:
        self.done.append(what)
        if not self.dry_run:
            fn(*args, **kwargs)


def is_stand_in(row: BureauRow) -> bool:
    return row.id == _STAND_IN_ID


def ensure_row(name: str, start: dt.date, end: dt.date, write) -> BureauRow:
    """The Bureau row for a quota period: found, created, or (dry run) a stand-in."""
    try:
        return store.find_row(name)
    except LookupError:
        pass
    write.done.append(f"create Bureau row {name!r} {start}→{end}")
    if write.dry_run:
        zero = {h.key: None for h in HOLDERS.values()}
        return BureauRow(id=_STAND_IN_ID, url="", name=name, start=start, end=end, total=None,
                         shares=zero, rollups={k: 0 for k in zero})
    return store.create_row(name, start, end)


def line(tx: Tx) -> str:
    return f"{tx.holder} {tx.date[:10]} ฿{tx.amount:,.2f} {tx.name}"


def campaign_cards(promo: BasePromotion) -> dict[str, dict[str, str]]:
    """{holder → {card title → page id}} for the campaign's cards each holder has."""
    return {h.key: {t: i for i, t in store.card_titles(h.key).items() if t in promo.cards}
            for h in HOLDERS.values()}


def collect(row: BureauRow, promo: BasePromotion, cards: dict[str, dict[str, str]], *,
            link: bool, write) -> tuple[list[Tx], list[dict], list[Tx], list[str]]:
    """(linked rows incl. newly linked, candidates left unlinked, adjustments, warnings).

    Adjustments are the period's ledger entries on the campaign's cards (never
    linked: they aren't purchases) — carry-forward legs and the like, which
    some campaigns net out of what reaches a holder (`adjustment_for`).
    """
    txs: list[Tx] = []
    candidates: list[dict] = []
    adjustments: list[Tx] = []
    warnings: list[str] = []
    for h in HOLDERS.values():
        linked = store.linked_txs(row, h)
        txs += linked
        total = sum((t.amount for t in linked), Decimal(0))
        if total != row.rollups[h.key]:
            warnings.append(f"{store.rollup_prop(h)} shows ฿{row.rollups[h.key]:,.2f} but the linked "
                            f"rows sum to ฿{total:,.2f}")
        for tx, existing in store.unlinked_txs(row, h, list(cards[h.key].values()), promo):
            if not tx.is_card_purchase:
                adjustments.append(tx)
                continue
            level, reason = promo.screen(tx)
            if level == ELIGIBLE and link:
                write(f"link {line(tx)}", store.link_tx, tx.id, existing, row.id)
                txs.append(tx)
            elif level == ELIGIBLE or promo.qualifies(tx):
                candidates.append({"id": tx.id, "row": line(tx), "level": level, "reason": reason})
    return txs, candidates, adjustments, warnings
