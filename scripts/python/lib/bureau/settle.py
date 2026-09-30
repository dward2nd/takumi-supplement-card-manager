"""Write a cashback campaign's money: the Bureau's baht fields and each holder's tracker row.

deterministic + idempotent — each write sets a value to what the split gives;
a tracker row is created only when none exists, and a ticked one is never touched.
Points campaigns have no money to settle; `runner` skips this module for them.
"""

from __future__ import annotations

from decimal import Decimal

from ..holders import HOLDERS
from . import store
from .base import Allocation, BasePromotion, Tx
from .store import BureauRow


def bureau_numbers(row: BureauRow, alloc: Allocation, write) -> tuple[bool, list[str]]:
    """Write `เงินคืนรวม` and `เงินคืนส่วน<name>`. False = shares held back.

    `เงินคืนรวม` is this script's while it equals the sum of the share fields (it
    wrote both), so it follows the split as rows are linked. Once someone types
    another figure there (the bank's actual credit), it's theirs: never
    overwritten, and a split that disagrees with it is held back.
    """
    ours = row.total is None or row.total == sum((v or Decimal(0) for v in row.shares.values()), Decimal(0))
    if not ours and row.total != alloc.credit:
        return False, [f"{store.TOTAL} holds ฿{row.total:,.2f} (entered by hand) but the split pays "
                       f"฿{alloc.credit:,.2f} on the linked ฿{alloc.pooled:,.2f} — shares and trackers not "
                       f"written. Fix the links, or clear {store.TOTAL} to let the computed figure stand."]
    numbers = {store.TOTAL: alloc.credit} if row.total != alloc.credit else {}
    numbers |= {store.share_prop(h): alloc.shares.get(h.key, Decimal(0)) for h in HOLDERS.values()
                if row.shares[h.key] != alloc.shares.get(h.key, Decimal(0))}
    if numbers:
        write(f"Bureau {', '.join(f'{k}={v}' for k, v in numbers.items())}",
              store.write_numbers, row.id, numbers)
    return True, []


def tracker_card(holder: str, cards: dict[str, str], txs: list[Tx]) -> str | None:
    """The card a holder's tracker row points at: the campaign's only card, or —
    for a campaign across several (EPW538) — the one carrying most of their spend."""
    if len(cards) <= 1:
        return next(iter(cards.values()), None)
    spend = {title: sum((t.amount for t in txs if t.holder == holder and t.card == title), Decimal(0))
             for title in cards}
    return cards[max(spend, key=spend.get)]


def trackers(row: BureauRow, promo: BasePromotion, alloc: Allocation, txs: list[Tx],
             adjustments: list[Tx], cards: dict[str, dict[str, str]], write
             ) -> tuple[dict[str, list[str]], list[str]]:
    """Each holder's tracker expects their share, net of cashback that already
    reached them another way (`adjustment_for`); the Bureau share stays the bank's."""
    title = promo.tracker_title(row.start, row.end)
    found_by_holder: dict[str, list[str]] = {}
    warnings: list[str] = []
    for h in HOLDERS.values():
        adjust = promo.adjustment_for(h.key, adjustments).quantize(Decimal("0.01"))
        share = alloc.shares.get(h.key, Decimal(0)) + adjust
        net = f" (share less ฿{-adjust} already paid via a carry-forward leg)" if adjust else ""
        found = store.trackers(h, row, title)
        found_by_holder[h.key] = [t.name for t in found]
        if not found:
            if share > 0:
                write(f"create {h.key} tracker {title!r} expecting ฿{share}{net}", store.create_tracker, h,
                      title=title, date=promo.tracker_date(row.start, row.end), card_id=tracker_card(h.key, cards[h.key], txs),
                      row_id=row.id, expected=share, icon=promo.icon)
        elif len(found) > 1 or not found[0].linked:
            warnings.append(f"{h.key}: tracker rows {[t.name for t in found]} need a look — more than "
                            f"one, or titled {title!r} without a Promotion link; left alone")
        elif found[0].settled:
            if found[0].expected != share:
                warnings.append(f"{h.key}: {found[0].name!r} is ticked as credited at "
                                f"฿{found[0].expected} but the split now gives ฿{share}; left alone")
        elif found[0].expected != share:
            write(f"{h.key} tracker Expected Cashback {found[0].expected} → {share}{net}",
                  store.set_expected, found[0].id, share)
    return found_by_holder, warnings
