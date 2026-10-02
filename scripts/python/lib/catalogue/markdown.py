"""Markdown → Notion blocks, for Promotion Catalogues pages.

deterministic + idempotent — a pure function from text to block JSON.

Only what a catalogue page uses:

  # / ## / ###        heading 1 / 2 / 3
  - item              bulleted item; "  - item" (two-space indent) nests one level under the item above
  1. item             numbered item; nests the same way
  > text              quote
  !> 🛒 text          callout with that emoji
  ---                 divider
  | a | b |           table; the first row is the header, a "|---|" row is skipped
  anything else       paragraph (a blank line only separates blocks)

Inline: **bold**, *italic* or _italic_, __underline__, `code`, [text](https://…),
and bare https:// URLs become links. An underscore inside a word
(`MAKRO_CHIANG`) stays literal.
"""

from __future__ import annotations

import re

# Notion rejects a rich-text item over 2,000 characters (UTF-16 units).
_TEXT_LIMIT = 2000

_INLINE = re.compile(
    r"\*\*(?P<bold>.+?)\*\*"
    r"|__(?P<under>.+?)__"
    r"|(?<![\w*])\*(?P<star>[^*\s](?:.*?[^*\s])?)\*(?![\w*])"
    r"|(?<![\w_])_(?P<ital>[^_\s](?:.*?[^_\s])?)_(?![\w_])"
    r"|`(?P<code>.+?)`"
    r"|\[(?P<ltext>.+?)\]\((?P<lurl>https?://[^)\s]+)\)"
    r"|(?P<bare>https?://[^\s)]+)"
)
_LIST = re.compile(r"^(?P<indent>\s*)(?:(?P<bullet>-)|(?P<num>\d+)\.)\s+(?P<text>.*)$")


def _pieces(text: str) -> list[str]:
    out, cur, units = [], [], 0
    for ch in text:
        size = 2 if ord(ch) > 0xFFFF else 1
        if units + size > _TEXT_LIMIT:
            out.append("".join(cur))
            cur, units = [], 0
        cur.append(ch)
        units += size
    out.append("".join(cur))
    return out


def rich(s: str, **inherited) -> list[dict]:
    """One line of inline Markdown as a Notion rich-text array."""
    out: list[dict] = []

    def add(text: str, link: str | None = None, **ann) -> None:
        ann = {**inherited, **ann}
        for piece in _pieces(text) if text else []:
            item: dict = {"type": "text", "text": {"content": piece}}
            if link:
                item["text"]["link"] = {"url": link}
            if ann:
                item["annotations"] = ann
            out.append(item)

    pos = 0
    for m in _INLINE.finditer(s):
        add(s[pos:m.start()])
        g = m.groupdict()
        if g["bold"] is not None:
            out.extend(rich(g["bold"], **{**inherited, "bold": True}))
        elif g["under"] is not None:
            out.extend(rich(g["under"], **{**inherited, "underline": True}))
        elif g["star"] is not None or g["ital"] is not None:
            out.extend(rich(g["star"] or g["ital"], **{**inherited, "italic": True}))
        elif g["code"] is not None:
            add(g["code"], code=True)
        elif g["ltext"] is not None:
            add(g["ltext"], link=g["lurl"])
        else:
            add(g["bare"], link=g["bare"])
        pos = m.end()
    add(s[pos:])
    return out


def _block(kind: str, text: str, **extra) -> dict:
    return {"object": "block", "type": kind, kind: {"rich_text": rich(text), **extra}}


def _table(rows: list[list[str]]) -> dict:
    width = max(len(r) for r in rows)
    return {"object": "block", "type": "table", "table": {
        "table_width": width, "has_column_header": True, "has_row_header": False,
        "children": [{"object": "block", "type": "table_row",
                      "table_row": {"cells": [rich(c) for c in r + [""] * (width - len(r))]}}
                     for r in rows],
    }}


def convert(md: str) -> list[dict]:
    """A page body in Markdown as the list of Notion blocks to append."""
    blocks: list[dict] = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(_table(rows))
            continue
        if line.strip() == "---":
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        elif m := re.match(r"^(#{1,3}) (.*)$", line):
            blocks.append(_block(f"heading_{len(m.group(1))}", m.group(2)))
        elif line.startswith("!> "):
            emoji, _, text = line[3:].partition(" ")
            blocks.append(_block("callout", text, icon={"type": "emoji", "emoji": emoji}))
        elif line.startswith("> "):
            blocks.append(_block("quote", line[2:]))
        elif m := _LIST.match(line):
            kind = "bulleted_list_item" if m.group("bullet") else "numbered_list_item"
            item = _block(kind, m.group("text"))
            parent = blocks[-1] if blocks else None
            if m.group("indent") and parent and parent["type"] in ("bulleted_list_item", "numbered_list_item"):
                parent[parent["type"]].setdefault("children", []).append(item)
            else:
                blocks.append(item)
        else:
            blocks.append(_block("paragraph", line))
        i += 1
    return blocks
