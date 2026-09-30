"""Give existing rows the icon a new row would get: plan, then apply.

deterministic + idempotent — the plan is a function of each page's current
properties; applying it twice writes nothing the second time. By default a
page that already has an icon is left alone (the household's hand-set ones
stay); `replace=True` re-applies the scheme to every page whose icon differs.
The Cards DBs are never planned.
"""

from __future__ import annotations

import datetime as dt
import sys
import time
from dataclasses import dataclass
from typing import Callable, Iterator

from notion_client.errors import APIResponseError

from .. import notion_client
from ..holders import HOLDERS, PROMOTION_BUREAU_DS, Holder
from .base import emoji
from .bills import bill_icon
from .transactions import TransactionIcons

DATABASES = ("transactions", "bills", "bureau", "trackers")
_PACE = 0.05          # seconds between writes: each call takes ~0.3 s, keeping under Notion's ~3/s; 429s retry
_RETRIES = 6


@dataclass
class Change:
    database: str
    page_id: str
    title: str
    old: dict | None
    new: dict


def _key(icon: dict | None) -> tuple | None:
    """What makes two icons the same, ignoring the URLs Notion adds on read."""
    if not icon:
        return None
    kind = icon.get("type")
    if kind == "emoji":
        return kind, icon["emoji"]
    if kind == "custom_emoji":
        return kind, icon["custom_emoji"]["id"]
    return kind, str(icon.get(kind))


def _title(page: dict) -> str:
    return "".join(t["plain_text"] for p in page["properties"].values()
                   if p["type"] == "title" for t in p["title"])


def _changes(database: str, pages: list[dict], pick: Callable[[dict], dict | None], replace: bool) -> Iterator[Change]:
    for page in pages:
        old = page.get("icon")
        if old and not replace:
            continue
        new = pick(page)
        if new and _key(new) != _key(old):
            yield Change(database, page["id"], _title(page), old, new)


def _transactions(h: Holder, replace: bool) -> Iterator[Change]:
    def pick(page: dict) -> dict:
        p = page["properties"]
        return emoji(TransactionIcons.pick(_title(page), p["ยอดชำระ"]["number"] or 0.0))
    return _changes("transactions", notion_client.query_all(h.transactions_ds), pick, replace)


def _bills(h: Holder, replace: bool) -> Iterator[Change]:
    return _changes("bills", notion_client.query_all(h.bills_ds), lambda page: bill_icon(_title(page)), replace)


def _campaign_icon(page: dict) -> dict:
    """A Bureau row's campaign icon; 🤑 when no campaign class claims the row."""
    from ..bureau import promotion_for   # late: the Bureau package is heavy
    p = page["properties"]
    try:
        start = dt.date.fromisoformat(p["Start Date"]["date"]["start"][:10])
        end = dt.date.fromisoformat(p["End Date"]["date"]["start"][:10])
        return emoji(promotion_for(_title(page), start, end).icon)
    except (LookupError, TypeError, KeyError, ValueError):
        return emoji("🤑")


def bureau_pages() -> list[dict]:
    return notion_client.query_all(PROMOTION_BUREAU_DS)


def _bureau(pages: list[dict], replace: bool) -> Iterator[Change]:
    return _changes("bureau", pages, _campaign_icon, replace)


def _trackers(h: Holder, by_bureau_row: dict[str, dict], replace: bool) -> Iterator[Change]:
    def pick(page: dict) -> dict:
        linked = [r["id"] for r in page["properties"].get("Promotion", {}).get("relation", [])]
        return next((by_bureau_row[i] for i in linked if i in by_bureau_row), emoji("🤑"))
    return _changes("trackers", notion_client.query_all(h.cashback_tracker_ds), pick, replace)


def plan(databases: tuple[str, ...] = DATABASES, holders: tuple[str, ...] | None = None,
         *, replace: bool = False) -> list[Change]:
    chosen = [HOLDERS[k] for k in (holders or tuple(HOLDERS))]
    out: list[Change] = []
    bureau = bureau_pages() if {"bureau", "trackers"} & set(databases) else []
    if "bureau" in databases:
        out += _bureau(bureau, replace)
    for h in chosen:
        if "transactions" in databases:
            out += _transactions(h, replace)
        if "bills" in databases and h.bills_ds:
            out += _bills(h, replace)
    if "trackers" in databases:
        by_row = {pg["id"]: _campaign_icon(pg) for pg in bureau}
        for h in chosen:
            if h.cashback_tracker_ds:
                out += _trackers(h, by_row, replace)
    return out


def _set(page_id: str, icon: dict) -> None:
    for attempt in range(_RETRIES):
        try:
            notion_client.set_icon(page_id, icon)
            return
        except APIResponseError as e:
            if e.code not in ("rate_limited", "internal_server_error", "service_unavailable") \
                    or attempt == _RETRIES - 1:
                raise
            time.sleep(2 ** attempt)


def apply(changes: list[Change], *, progress_every: int = 100) -> dict[str, int]:
    done: dict[str, int] = {}
    for n, c in enumerate(changes, 1):
        _set(c.page_id, c.new)
        done[c.database] = done.get(c.database, 0) + 1
        if n % progress_every == 0:
            print(f"{n}/{len(changes)} icons set", file=sys.stderr, flush=True)
        time.sleep(_PACE)
    return done
