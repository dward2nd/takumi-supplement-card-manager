#!/usr/bin/env python3
"""update-transaction — patch existing transaction pages with new property values.

deterministic + idempotent — re-running with the same input writes the
same values; safe to retry on partial failure (Notion's pages.update is
itself idempotent for property writes).

Companion to `scripts/python/add-transaction/cli.py` (which only
creates). Use this when an earlier write omitted a field that's now
required by policy — typical case is filling `% cb` on Baiboon's or
Nuta's transactions after merchant-tier classification.

Reads a JSON spec from stdin (or --input <file>):

  {
    "updates": [
      { "id": "<page-uuid>", "cashback_percent": 0.05 },
      { "id": "<page-uuid>", "cashback_percent": 0.00, "note": "foreign merchant in THB" },
      { "id": "<page-uuid>", "properties": { "<raw notion prop>": ... } }
    ]
  }

Recognized convenience keys per update:
  - cashback_percent → writes Notion `% cb` (raw fraction); `null` clears
  - note            → writes Notion `Note`
  - multiplier      → writes one of `×0`/`×2`/`×3`/`×4`/`×5`/`÷4` to true
  - properties      → escape hatch: raw Notion properties payload, merged

Writes a JSON envelope to stdout:

  { "count": N, "updated": [ { "id": ..., "fields": [...] }, ... ] }

--dry-run prints the resolved properties payloads without calling Notion.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import notion_client
from lib.transaction_write import VALID_MULTIPLIERS


_CLEAR_CASHBACK = object()


def _build_properties(update: dict) -> dict:
    props: dict = {}

    # `cashback_percent: null` is a sentinel for "clear the `% cb` field"
    # (writes JSON null to Notion, leaving the cell empty). Distinguishes
    # "user wants to clear" from "user didn't mention this field" — the
    # latter is the absence of the key.
    cb = update.get("cashback_percent", _CLEAR_CASHBACK)
    if cb is None:
        props["% cb"] = {"number": None}
    elif cb is not _CLEAR_CASHBACK:
        if not isinstance(cb, (int, float)) or isinstance(cb, bool) or not (0 <= cb <= 1):
            raise ValueError(
                f"cashback_percent must be a raw fraction in [0, 1] (or null to clear); got {cb!r}"
            )
        props["% cb"] = {"number": float(cb)}

    if (note := update.get("note")) is not None:
        if not isinstance(note, str):
            raise ValueError(f"note must be a string; got {type(note).__name__}")
        props["Note"] = {"rich_text": [{"text": {"content": note}}]}

    if (mult := update.get("multiplier")) is not None:
        if mult not in VALID_MULTIPLIERS:
            raise ValueError(
                f"multiplier must be one of {sorted(VALID_MULTIPLIERS)}; got {mult!r}"
            )
        props[mult] = {"checkbox": True}

    if (raw := update.get("properties")) is not None:
        if not isinstance(raw, dict):
            raise ValueError("properties escape-hatch must be an object")
        props.update(raw)

    if not props:
        raise ValueError(f"no recognized fields in update: {update!r}")

    return props


def run(spec: dict, *, dry_run: bool = False) -> dict:
    if not isinstance(spec, dict) or "updates" not in spec:
        raise ValueError("spec must be an object with key `updates`")
    updates = spec["updates"]
    if not isinstance(updates, list) or not updates:
        raise ValueError("`updates` must be a non-empty list")

    out: list[dict] = []
    for u in updates:
        page_id = u.get("id")
        if not isinstance(page_id, str) or not page_id:
            raise ValueError(f"each update needs a string `id`; got {u!r}")
        props = _build_properties(u)
        if dry_run:
            out.append({"id": page_id, "dry_run": True, "properties": props})
            continue
        resp = notion_client.update_page_properties(page_id, props)
        out.append({"id": resp.get("id", page_id), "fields": sorted(props.keys())})

    return {"count": len(out), "updated": out}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Resolve payloads without calling Notion")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
