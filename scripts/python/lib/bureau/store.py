"""Notion I/O for the Promotion Bureau and the per-holder cashback trackers.

deterministic + idempotent — reads are pure; every write here sets a value
to what the caller computed, so repeating one changes nothing.

Per-holder Bureau columns are named after the holder's Thai name, so one
template covers all three: `รายการใช้จ่ายจาก<name>` (relation to the holder's
Transactions), `ยอดจาก<name>` (its Σ `ยอดชำระ` rollup), `เงินคืนส่วน<name>`
(the holder's share of the credit). Transactions DSes and trackers link back
through a property called `Promotion`.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from decimal import Decimal
from functools import cache

from .. import notion_client
from ..cards import card_titles_by_id
from ..holders import HOLDERS, PROMOTION_BUREAU_DS, Holder
from ..icons.base import emoji
from ..transaction_read import project_transaction
from ..transaction_write import VALID_MULTIPLIERS
from .base import BasePromotion, Tx

LINK = "Promotion"      # on every Transactions DS and every tracker
TOTAL = "เงินคืนรวม"
RIGHTS = "สิทธิ์ลุ้นรางวัล"   # draw rights a RIGHTS campaign's period earned (BTS; added 2026-09-29)
SETTLED = ""            # the trackers' unnamed checkbox: the credit has reached the holder
_PAGE_ID = re.compile(r"([0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})\s*$")


def linked_prop(h: Holder) -> str:
    return f"รายการใช้จ่ายจาก{h.thai_name}"


def rollup_prop(h: Holder) -> str:
    return f"ยอดจาก{h.thai_name}"


def share_prop(h: Holder) -> str:
    return f"เงินคืนส่วน{h.thai_name}"


@dataclass(frozen=True)
class BureauRow:
    id: str
    url: str
    name: str
    start: dt.date
    end: dt.date
    total: Decimal | None                    # `เงินคืนรวม` as entered
    shares: dict[str, Decimal | None]        # `เงินคืนส่วน<name>` per holder key
    rollups: dict[str, Decimal]              # `ยอดจาก<name>` per holder key
    rights: int | None = None                # `สิทธิ์ลุ้นรางวัล`, on a draw-rights row


def _money(value) -> Decimal | None:
    return None if value is None else Decimal(str(round(value, 2)))


def _parse_row(page: dict) -> BureauRow:
    p = page["properties"]

    def date(name: str) -> dt.date:
        d = (p[name].get("date") or {}).get("start")
        if not d:
            raise ValueError(f"Bureau row is missing {name!r}")
        return dt.date.fromisoformat(d[:10])

    return BureauRow(
        id=page["id"],
        url=page["url"],
        name="".join(t["plain_text"] for t in p["Name"]["title"]),
        start=date("Start Date"),
        end=date("End Date"),
        total=_money(p[TOTAL]["number"]),
        shares={h.key: _money(p[share_prop(h)]["number"]) for h in HOLDERS.values()},
        rollups={h.key: _money(p[rollup_prop(h)]["rollup"].get("number")) or Decimal(0)
                 for h in HOLDERS.values()},
        rights=None if (n := (p.get(RIGHTS) or {}).get("number")) is None else int(n),
    )


def create_row(name: str, start: dt.date, end: dt.date, *, icon: str | None = None) -> BureauRow:
    """A new Bureau row for one quota period, with the campaign's page icon."""
    page = notion_client.create_page(PROMOTION_BUREAU_DS, {
        "Name": {"title": [{"text": {"content": name}}]},
        "Start Date": {"date": {"start": start.isoformat()}},
        "End Date": {"date": {"start": end.isoformat()}},
    }, icon=emoji(icon) if icon else None)
    return _parse_row(notion_client.get_page(page["id"]))


def find_row(ref: str) -> BureauRow:
    """A Bureau row by page ID / URL, or by its exact Name."""
    m = _PAGE_ID.search(ref.strip())
    if m:
        return _parse_row(notion_client.get_page(m.group(1)))
    pages = notion_client.query_all(
        PROMOTION_BUREAU_DS, filter={"property": "Name", "title": {"equals": ref.strip()}})
    if len(pages) != 1:
        names = ["".join(t["plain_text"] for t in pg["properties"]["Name"]["title"])
                 for pg in notion_client.query_all(PROMOTION_BUREAU_DS)]
        raise LookupError(f"{len(pages)} Bureau rows named {ref!r}; rows: {names}")
    return _parse_row(pages[0])


def all_rows() -> list[BureauRow]:
    """Every Bureau row (a handful per month)."""
    return [_parse_row(pg) for pg in notion_client.query_all(PROMOTION_BUREAU_DS)]


@cache
def card_titles(holder_key: str) -> dict[str, str]:
    """{card page id → title} for one holder, read once per process."""
    return card_titles_by_id(HOLDERS[holder_key].cards_ds)


def _to_tx(h: Holder, page: dict) -> Tx:
    t = project_transaction(page)
    p = page["properties"]
    cb, used = t["cashback_percent"], (p.get("ใช้คะแนน") or {}).get("number")
    return Tx(id=t["id"], holder=h.key, name=t["name"],
              amount=_money(t["amount"]) or Decimal(0), date=t["transaction_date"] or "",
              cb=None if cb is None else Decimal(str(cb)),
              multiplier=next((m for m in sorted(VALID_MULTIPLIERS) if (p.get(m) or {}).get("checkbox")), None),
              points_used=None if used is None else Decimal(str(used)),
              note=t["note"],
              card=card_titles(h.key).get(t["card_ids"][0], "") if t["card_ids"] else "",
              bill_cycle=t["bill_cycle_date"],
              posted=t["process_date"])


def linked_txs(row: BureauRow, h: Holder) -> list[Tx]:
    """Every transaction of `h` linked to the row (queried from the Transactions
    side: a page's own relation list is cut off at 25)."""
    pages = notion_client.query_all(
        h.transactions_ds, filter={"property": LINK, "relation": {"contains": row.id}})
    return [_to_tx(h, pg) for pg in pages]


def unlinked_txs(row: BureauRow, h: Holder, card_ids: list[str], promo: BasePromotion
                 ) -> list[tuple[Tx, list[str]]]:
    """The cards' rows inside the period that aren't linked to the row, with each
    one's existing `Promotion` links (to preserve when linking). The campaign
    decides what "inside" means (`candidate_filter` to query, `covers` to keep)."""
    if not card_ids:
        return []
    pages = notion_client.query_all(h.transactions_ds, filter={"and": [
        {"or": [{"property": "Card", "relation": {"contains": c}} for c in card_ids]},
        *promo.candidate_filter(row.start, row.end),
        {"property": LINK, "relation": {"does_not_contain": row.id}},
    ]})
    out = []
    for pg in pages:
        tx = _to_tx(h, pg)
        if promo.covers(row.start, row.end, tx):
            out.append((tx, [r["id"] for r in pg["properties"][LINK]["relation"]]))
    return out


def link_tx(tx_id: str, existing: list[str], row_id: str) -> None:
    rel = [{"id": i} for i in [*existing, row_id]]
    notion_client.update_page_properties(tx_id, {LINK: {"relation": rel}})


def set_links(tx_id: str, row_ids: list[str]) -> None:
    """Replace a transaction's `Promotion` links (dropping one it no longer belongs to)."""
    notion_client.update_page_properties(tx_id, {LINK: {"relation": [{"id": i} for i in row_ids]}})


def write_numbers(row_id: str, values: dict[str, Decimal]) -> None:
    notion_client.update_page_properties(
        row_id, {k: {"number": float(v)} for k, v in values.items()})


# -- trackers ------------------------------------------------------------------


@dataclass(frozen=True)
class Tracker:
    id: str
    name: str
    expected: Decimal | None
    settled: bool
    linked: bool


def _tracker(page: dict) -> Tracker:
    p = page["properties"]
    return Tracker(
        id=page["id"],
        name="".join(t["plain_text"] for t in p["Name"]["title"]),
        expected=_money(p["Expected Cashback"]["number"]),
        settled=bool(p[SETTLED]["checkbox"]),
        linked=bool(p[LINK]["relation"]),
    )


def trackers(h: Holder, row: BureauRow, title: str) -> list[Tracker]:
    """The holder's tracker rows for this Bureau row: linked to it, or — so a
    hand-made row isn't duplicated — carrying the same title."""
    pages = notion_client.query_all(h.cashback_tracker_ds, filter={"or": [
        {"property": LINK, "relation": {"contains": row.id}},
        {"property": "Name", "title": {"equals": title}},
    ]})
    return [_tracker(pg) for pg in pages]


def create_tracker(h: Holder, *, title: str, date: dt.date, card_id: str | None, row_id: str,
                   expected: Decimal, icon: str | None = None) -> str:
    page = notion_client.create_page(h.cashback_tracker_ds, {
        "Name": {"title": [{"text": {"content": title}}]},
        "Transaction Date": {"date": {"start": date.isoformat()}},
        "Card": {"relation": [{"id": card_id}] if card_id else []},
        LINK: {"relation": [{"id": row_id}]},
        "Expected Cashback": {"number": float(expected)},
    }, icon=emoji(icon) if icon else None)
    return page["id"]


def set_expected(tracker_id: str, expected: Decimal) -> None:
    notion_client.update_page_properties(tracker_id, {"Expected Cashback": {"number": float(expected)}})


# -- page body -----------------------------------------------------------------


def body_block_ids(page_id: str) -> list[str]:
    client = notion_client.get_client()
    ids, cursor = [], None
    while True:
        resp = client.blocks.children.list(block_id=page_id, **({"start_cursor": cursor} if cursor else {}))
        ids += [b["id"] for b in resp["results"]]
        if not resp.get("has_more"):
            return ids
        cursor = resp["next_cursor"]


def write_body(page_id: str, blocks: list[dict], *, replace: bool) -> None:
    client = notion_client.get_client()
    if replace:
        for block_id in body_block_ids(page_id):
            client.blocks.delete(block_id=block_id)
    for i in range(0, len(blocks), 100):  # the API appends at most 100 blocks per call
        client.blocks.children.append(block_id=page_id, children=blocks[i:i + 100])
