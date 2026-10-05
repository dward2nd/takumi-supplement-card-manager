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
    ],
    "sync_promotions": true   // optional, default true — see below
  }

Recognized convenience keys per update:
  - cashback_percent → writes Notion `% cb` (raw fraction); `null` clears
  - note            → writes Notion `Note`; `""` (empty string) clears
  - multiplier      → writes one of `×0`/`×2`/`×3`/`×4`/`×5`/`×6`/`÷4` to true
  - points_redeemed → writes Notion `ใช้คะแนน`; `null` clears.
                      Positive = deduct from lifetime, negative = add back.
  - bill_cycle      → writes `Bill Cycle Date` (ISO date). Re-cycle a row
                      (backdate to a closed cycle, or foredate to next).
                      Must be paired with `due_date` so the pair stays
                      consistent for that card's bank pattern.
  - due_date        → writes `Due Date` (ISO date). Pair with bill_cycle.
  - properties      → escape hatch: raw Notion properties payload, merged

Writes a JSON envelope to stdout:

  { "count": N, "updated": [ { "id": ..., "fields": [...] }, ... ], "promotions": {...} }

`promotions` (unless `sync_promotions` is false): the patched rows are read
back and every Promotion Bureau row they count toward is re-synced, and linked
rows' `% cb` / multiplier / `ใช้คะแนน` set to what the split expects — which can
put back a value this update just wrote (lib.bureau.follow).

--dry-run prints the resolved properties payloads without calling Notion
(`promotions` then only names the Bureau rows it would re-sync).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import notion_client
from lib.bureau import follow
from lib.transaction_write import build_update_properties


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
        props = build_update_properties(u)
        if dry_run:
            out.append({"id": page_id, "dry_run": True, "properties": props})
            continue
        resp = notion_client.update_page_properties(page_id, props)
        out.append({"id": resp.get("id", page_id), "fields": sorted(props.keys())})

    result = {"count": len(out), "updated": out}
    if spec.get("sync_promotions", True):
        result["promotions"] = follow.follow_safely(ids=[u["id"] for u in updates], dry_run=dry_run)
    return result


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
