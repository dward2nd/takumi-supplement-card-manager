"""Builders for Notion page-body blocks (the content inside a page), and `text` for
a rich-text property value such as `Note`.

deterministic + idempotent — pure functions from text to block JSON.

Only the handful of block types the scripts write. A rich-text run is a
string, or a `(text, style)` tuple where style is any of "b" (bold),
"c" (code) and "i" (italic), or a `(text, style, url)` triple for a link.
"""

from __future__ import annotations

Run = str | tuple

# Notion rejects a rich-text item longer than 2,000 characters, counted in UTF-16 units.
TEXT_LIMIT = 2000


def text(content: str) -> list[dict]:
    """`content` as a rich-text array (a `Note` property, say), split into pieces
    Notion accepts. A generated bill Note can run past one piece's limit."""
    pieces, current, units = [], [], 0
    for ch in content:
        size = 2 if ord(ch) > 0xFFFF else 1
        if units + size > TEXT_LIMIT:
            pieces.append("".join(current))
            current, units = [], 0
        current.append(ch)
        units += size
    pieces.append("".join(current))
    return [{"type": "text", "text": {"content": p}} for p in pieces]


def rich(*runs: Run) -> list[dict]:
    out = []
    for run in runs:
        text, style, url = (run, "", None) if isinstance(run, str) else (*run, None)[:3]
        item = {"type": "text", "text": {"content": text}}
        if url:
            item["text"]["link"] = {"url": url}
        if style:
            item["annotations"] = {"bold": "b" in style, "code": "c" in style, "italic": "i" in style}
        out.append(item)
    return out


def _block(kind: str, runs: tuple[Run, ...], **extra) -> dict:
    return {"object": "block", "type": kind, kind: {"rich_text": rich(*runs), **extra}}


def heading(*runs: Run) -> dict:
    return _block("heading_3", runs)


def paragraph(*runs: Run) -> dict:
    return _block("paragraph", runs)


def bullet(*runs: Run) -> dict:
    return _block("bulleted_list_item", runs)


def callout(*runs: Run, emoji: str = "💳") -> dict:
    return _block("callout", runs, icon={"type": "emoji", "emoji": emoji})


def table(header: list[str], rows: list[list[str]]) -> dict:
    """A simple table; every cell is plain text."""
    def row(cells: list[str]) -> dict:
        return {"object": "block", "type": "table_row",
                "table_row": {"cells": [rich(c) for c in cells]}}

    return {"object": "block", "type": "table", "table": {
        "table_width": len(header), "has_column_header": True, "has_row_header": False,
        "children": [row(header), *(row(r) for r in rows)],
    }}
