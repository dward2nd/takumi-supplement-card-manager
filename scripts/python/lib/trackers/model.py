"""Tracker pages and the ledger rows that settle them — the read side.

deterministic + idempotent — reads only.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from decimal import Decimal

from .. import notion_client
from ..holders import Holder
from ..transaction_read import project_transaction

NAME = "Name"
SETTLED = ""                     # the unnamed checkbox: the credit has reached the holder
LINKS = "Slip Transaction"       # relation to the holder's own Transactions DS
NOTE = "Note"
EXPECTED = "Expected Cashback"
PROMOTION = "Promotion"          # relation to the Promotion Bureau row

_PAGE_ID = re.compile(r"([0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})\s*$", re.IGNORECASE)


def page_id(ref: str) -> str | None:
    """The page ID in a bare ID or a Notion URL; None for anything else (a title)."""
    m = _PAGE_ID.search(ref.strip())
    return m.group(1) if m else None


def _norm(page_or_ds_id: str) -> str:
    return page_or_ds_id.replace("-", "").lower()


def _parent_ds(page: dict) -> str | None:
    parent = page.get("parent") or {}
    return parent.get("data_source_id")


def _money(value) -> Decimal | None:
    return None if value is None else Decimal(str(round(value, 2)))


def _text(prop: dict) -> str:
    return "".join(t["plain_text"] for t in prop.get(prop["type"], []))


@dataclass(frozen=True)
class TrackerPage:
    id: str
    title: str
    settled: bool
    expected: Decimal | None
    links: tuple[str, ...]
    note: str
    promotion_id: str | None


def _tracker(page: dict) -> TrackerPage:
    p = page["properties"]
    promo = [r["id"] for r in p[PROMOTION]["relation"]]
    return TrackerPage(
        id=page["id"],
        title=_text(p[NAME]),
        settled=bool(p[SETTLED]["checkbox"]),
        expected=_money(p[EXPECTED]["number"]),
        links=tuple(r["id"] for r in p[LINKS]["relation"]),
        note=_text(p[NOTE]),
        promotion_id=promo[0] if promo else None,
    )


def find_tracker(holder: Holder, ref: str) -> TrackerPage:
    """The holder's tracker row by page ID / URL, or by its exact title."""
    if not holder.cashback_tracker_ds:
        raise LookupError(f"{holder.key} has no cashback tracker")
    pid = page_id(ref)
    if pid:
        page = notion_client.get_page(pid)
        if _norm(_parent_ds(page) or "") != _norm(holder.cashback_tracker_ds):
            raise LookupError(f"{ref!r} is not a row of {holder.key}'s cashback tracker")
        return _tracker(page)
    pages = notion_client.query_all(holder.cashback_tracker_ds,
                                    filter={"property": NAME, "title": {"equals": ref.strip()}})
    if len(pages) != 1:
        raise LookupError(f"{len(pages)} rows titled {ref!r} in {holder.key}'s cashback tracker; "
                          "pass the page ID instead")
    return _tracker(pages[0])


@dataclass(frozen=True)
class LedgerRow:
    id: str
    name: str
    amount: Decimal
    bill_cycle: dt.date | None

    @property
    def is_credit(self) -> bool:
        return self.amount < 0


def ledger_row(holder: Holder, ref: str) -> LedgerRow:
    """A row of the holder's own Transactions DS. `Slip Transaction` reaches
    only that DS, so a row from anyone else's ledger is refused."""
    pid = page_id(ref)
    if not pid:
        raise ValueError(f"{ref!r} is not a page ID or URL")
    page = notion_client.get_page(pid)
    if page.get("in_trash") or page.get("archived"):
        raise ValueError(f"ledger row {pid} is archived")
    if _norm(_parent_ds(page) or "") != _norm(holder.transactions_ds):
        raise ValueError(f"ledger row {pid} is not in {holder.key}'s Transactions DS; "
                         "a friend's credit on Takumi's card is settled by his transfer slip instead")
    tx = project_transaction(page)
    bc = tx["bill_cycle_date"]
    return LedgerRow(id=page["id"], name=tx["name"] or "", amount=_money(tx["amount"] or 0),
                     bill_cycle=dt.date.fromisoformat(bc[:10]) if bc else None)
