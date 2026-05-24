"""Bill-row lookup on a holder's Bills DB.

deterministic + idempotent — safe to re-run.

Bills uniquely identify by (Card SELECT, วันตัดรอบบิล date). The Card
field is a SELECT (not a relation — see docs/concepts/known-divergences),
so card matching here is on the verbatim select-option string. Bill
cycle dates are ISO date strings.

Takumi has no Bills DB; lookups for `takumi` raise BillsNotSupported.
"""

from __future__ import annotations

from . import notion_client
from .holders import Holder


class BillNotFoundError(RuntimeError):
    pass


class BillAmbiguousError(RuntimeError):
    pass


class BillsNotSupported(RuntimeError):
    pass


def require_bills_ds(holder: Holder) -> str:
    if not holder.bills_ds:
        raise BillsNotSupported(
            f"{holder.key!r} has no Bills database (only baiboon and nuta do)"
        )
    return holder.bills_ds


def find_bill(holder: Holder, card: str, bill_cycle: str) -> dict:
    """Return the single Bills page for (card, bill_cycle) on this holder.

    `card` matches the `Card` SELECT option verbatim. `bill_cycle` is
    the value of `วันตัดรอบบิล` (ISO date).
    """
    ds = require_bills_ds(holder)
    pages = notion_client.query_all(
        ds,
        filter={
            "and": [
                {"property": "Card", "select": {"equals": card}},
                {"property": "วันตัดรอบบิล", "date": {"equals": bill_cycle}},
            ]
        },
    )
    if not pages:
        raise BillNotFoundError(
            f"no bill on {holder.key}'s Bills DB for card={card!r}, "
            f"วันตัดรอบบิล={bill_cycle!r}"
        )
    if len(pages) > 1:
        raise BillAmbiguousError(
            f"multiple bills on {holder.key}'s Bills DB for card={card!r}, "
            f"วันตัดรอบบิล={bill_cycle!r}: {[p['id'] for p in pages]}"
        )
    return pages[0]
