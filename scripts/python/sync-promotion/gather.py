"""Collect a Bureau row's transactions: the linked ones, and candidates not linked yet.

deterministic + idempotent — reads, plus (only with `link`) linking eligible
candidates, which is a no-op once they're linked.
"""

from __future__ import annotations

from decimal import Decimal

from lib.bureau import ELIGIBLE, BasePromotion, Tx, store
from lib.bureau.store import BureauRow
from lib.holders import HOLDERS

import report


def campaign_cards(promo: BasePromotion) -> dict[str, dict[str, str]]:
    """{holder → {card title → page id}} for the campaign's cards each holder has."""
    return {h.key: {t: i for i, t in store.card_titles(h.key).items() if t in promo.cards}
            for h in HOLDERS.values()}


def collect(row: BureauRow, promo: BasePromotion, cards: dict[str, dict[str, str]], *,
            link: bool, write) -> tuple[list[Tx], list[dict], list[str]]:
    """(linked rows incl. newly linked, candidates left unlinked, warnings)."""
    txs: list[Tx] = []
    candidates: list[dict] = []
    warnings: list[str] = []
    for h in HOLDERS.values():
        linked = store.linked_txs(row, h)
        txs += linked
        total = sum((t.amount for t in linked), Decimal(0))
        if total != row.rollups[h.key]:
            warnings.append(f"{store.rollup_prop(h)} shows ฿{row.rollups[h.key]:,.2f} but the linked "
                            f"rows sum to ฿{total:,.2f}")
        for tx, existing in store.unlinked_txs(row, h, list(cards[h.key].values()), promo.period_basis):
            level, reason = promo.screen(tx)
            if level == ELIGIBLE and link:
                write(f"link {report.line(tx)}", store.link_tx, tx.id, existing, row.id)
                txs.append(tx)
            elif tx.is_card_purchase and (level == ELIGIBLE or promo.qualifies(tx)):
                candidates.append({"row": report.line(tx), "level": level, "reason": reason})
    return txs, candidates, warnings
