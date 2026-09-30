"""Page icons for the rows the scripts create, so each kind of row stands out.

deterministic + idempotent — the icon is a function of the new page's
properties.

`notion_client.create_page` asks `for_new_page` whenever its caller passes no
icon, so every write path gets one without knowing about icons. Callers that
know better pass their own: the Promotion Bureau and its cashback trackers use
each campaign's `icon` (lib.bureau.base.BasePromotion). The Cards DBs get none:
the household sets their bank logos by hand (user, 2026-09-30).

See docs/concepts/page-icons.md for the scheme.
"""

from __future__ import annotations

from ..holders import HOLDERS, PROMOTION_BUREAU_DS
from .base import CARD, FixedIcon, IconRule, PageIcons, emoji
from .bills import BillIcons
from .transactions import TransactionIcons

CASHBACK = "🤑"   # a campaign row or tracker whose caller named no campaign icon


def _registry() -> dict[str, PageIcons]:
    out: dict[str, PageIcons] = {PROMOTION_BUREAU_DS: FixedIcon(CASHBACK)}
    for h in HOLDERS.values():
        out[h.transactions_ds] = TransactionIcons()
        if h.bills_ds:
            out[h.bills_ds] = BillIcons()
        if h.cashback_tracker_ds:
            out[h.cashback_tracker_ds] = FixedIcon(CASHBACK)
    return out


_BY_DATA_SOURCE = _registry()


def for_new_page(data_source_id: str, properties: dict) -> dict | None:
    """The icon for a page about to be created in this data source; None where
    the scripts leave icons to the household (the Cards DBs, anything unknown)."""
    picker = _BY_DATA_SOURCE.get(data_source_id)
    return picker.icon(properties) if picker else None


__all__ = ["CARD", "CASHBACK", "IconRule", "PageIcons", "emoji", "for_new_page"]
