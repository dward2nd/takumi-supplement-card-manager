"""Notion I/O for the Promotion Catalogues DB: find or create a page, its dates, icon, cover and body.

deterministic + idempotent — each write sets a value to what the caller asked
for; a page is created only when none has the Name, and a body or cover is
replaced only when the caller says so.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path

from .. import notion_client, notion_files
from ..holders import PROMOTION_CATALOGUES_DS

APPEND_LIMIT = 100   # blocks per append call


@dataclass(frozen=True)
class CataloguePage:
    id: str
    url: str
    name: str
    start: dt.date | None
    end: dt.date | None
    icon: str | None      # the emoji, if the icon is one
    has_cover: bool


def _date(p: dict, name: str) -> dt.date | None:
    d = ((p.get(name) or {}).get("date") or {}).get("start")
    return dt.date.fromisoformat(d[:10]) if d else None


def _parse(page: dict) -> CataloguePage:
    p = page["properties"]
    icon = page.get("icon") or {}
    return CataloguePage(
        id=page["id"], url=page["url"],
        name="".join(t["plain_text"] for t in p["Name"]["title"]),
        start=_date(p, "Start Date"), end=_date(p, "End Date"),
        icon=icon.get("emoji") if icon.get("type") == "emoji" else None,
        has_cover=bool(page.get("cover")),
    )


def find(name: str) -> CataloguePage | None:
    """The page with exactly this Name, or None. Two pages with one Name is an error."""
    pages = notion_client.query_all(PROMOTION_CATALOGUES_DS,
                                    filter={"property": "Name", "title": {"equals": name}})
    if len(pages) > 1:
        raise LookupError(f"{len(pages)} Promotion Catalogues pages are named {name!r}; keep one")
    return _parse(pages[0]) if pages else None


def all_pages() -> list[CataloguePage]:
    return [_parse(p) for p in notion_client.query_all(PROMOTION_CATALOGUES_DS)]


def _dates(start: dt.date, end: dt.date) -> dict:
    return {"Start Date": {"date": {"start": start.isoformat()}}, "End Date": {"date": {"start": end.isoformat()}}}


def create(name: str, start: dt.date, end: dt.date, emoji: str | None) -> CataloguePage:
    page = notion_client.create_page(PROMOTION_CATALOGUES_DS, {
        "Name": {"title": [{"text": {"content": name}}]}, **_dates(start, end),
    }, icon={"type": "emoji", "emoji": emoji} if emoji else None)
    return _parse(notion_client.get_page(page["id"]))


def set_dates(page_id: str, start: dt.date, end: dt.date) -> None:
    notion_client.update_page_properties(page_id, _dates(start, end))


def set_icon(page_id: str, emoji: str) -> None:
    notion_client.set_icon(page_id, {"type": "emoji", "emoji": emoji})


def set_cover(page_id: str, image: Path) -> None:
    upload = notion_files.upload_file(image)
    notion_client.set_cover(page_id, {"type": "file_upload", "file_upload": {"id": upload}})


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
    """Append the blocks; with `replace`, delete the page's current body first."""
    client = notion_client.get_client()
    if replace:
        for block_id in body_block_ids(page_id):
            client.blocks.delete(block_id=block_id)
    for i in range(0, len(blocks), APPEND_LIMIT):
        client.blocks.children.append(block_id=page_id, children=blocks[i:i + APPEND_LIMIT])
