#!/usr/bin/env python3
"""summarize-overview — read-only "cards & credit lines held by <holder>" overview.

deterministic + idempotent — safe to re-run.

Mirrors the default table view of the Notion database
"สรุปบัตรและสินเชื่อที่<name>ถือ", which under the hood is the same data
source as the holder's Cards DB. Returns one JSON envelope per holder.

Reads a JSON spec from stdin (or --input <file>):

  {
    "holder":               "takumi" | "baiboon" | "nuta",   // required
    "include_zero_balance": false                            // optional, default false
  }

Writes a JSON envelope to stdout:

  {
    "holder": "baiboon",
    "thai_name": "ใบบุญ",
    "title": "สรุปบัตรและสินเชื่อที่ใบบุญถือ",
    "include_zero_balance": false,
    "total_count": 14,     // pre-filter row count
    "count": 6,            // returned row count
    "results": [
      {
        "id": ..., "url": ..., "name": ..., "bank": ..., "card_network": ...,
        "premium_tier": ..., "credit_limit": ..., "baht_per_point": ...,
        "points_per_bill_cycle": ..., "outstanding_balance": ...,
        "points_balance": ..., "latest_bill_cycle": ..., "latest_due_date": ...,
        "note": ...
      },
      ...
    ]
  }

Filter rules:
  - By default, rows where `round(outstanding_balance, 2) == 0.00` are
    excluded — they're irrelevant to a quick "what do I owe" inquiry.
    Negative balances (credit / overpayment / refund) are **kept**
    because they're meaningful information.
  - Pass `include_zero_balance: true` when the question doesn't depend
    on outstanding balance — e.g. "what's the total accumulated points
    across all cards?", "which cards earn at the highest baht/point?".

Rows are sorted to match the Notion view "ตาราง" on this database:
  1. outstanding_balance DESC
  2. latest_bill_cycle    ASC
  3. points_balance       DESC
  4. name                 ASC

Nulls in numeric / date fields sort to the bottom of their respective
direction (Notion's default).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import notion_client
from lib.card_read import project_card
from lib.holders import resolve_holder


_TITLE_FMT = "สรุปบัตรและสินเชื่อที่{thai}ถือ"


def _is_effectively_zero(value: float | None) -> bool:
    """Strictly-zero or rounds-to-zero-at-2dp counts as zero.

    The "rounds-to-zero" arm catches Notion floating-point noise like
    `3e-12` on a fully-paid card (seen on Nuta's KTC UnionPay).
    Negative balances are NOT zero — a refund / credit position is
    meaningful information and should pass the filter.
    """
    return value is not None and round(value, 2) == 0.0


def _sort_key(row: dict) -> tuple:
    """Match the Notion 'ตาราง' view sort, with explicit null handling."""
    bal = row["outstanding_balance"]
    cyc = row["latest_bill_cycle"]
    pts = row["points_balance"]
    name = row["name"] or ""
    return (
        # outstanding_balance DESC; nulls last.
        (bal is None, -(bal or 0.0)),
        # latest_bill_cycle ASC; nulls last.
        (cyc is None, cyc or ""),
        # points_balance DESC; nulls last.
        (pts is None, -(pts or 0.0)),
        # name ASC.
        name,
    )


def run(spec: dict) -> dict:
    if not isinstance(spec, dict) or "holder" not in spec:
        raise ValueError("spec must be an object with key `holder`")
    holder = resolve_holder(spec["holder"])
    include_zero = bool(spec.get("include_zero_balance", False))

    pages = notion_client.query_all(holder.cards_ds)
    rows = [project_card(p) for p in pages]
    total_count = len(rows)
    if not include_zero:
        rows = [r for r in rows if not _is_effectively_zero(r["outstanding_balance"])]
    rows.sort(key=_sort_key)

    return {
        "holder": holder.key,
        "thai_name": holder.thai_name,
        "title": _TITLE_FMT.format(thai=holder.thai_name),
        "include_zero_balance": include_zero,
        "total_count": total_count,
        "count": len(rows),
        "results": rows,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
