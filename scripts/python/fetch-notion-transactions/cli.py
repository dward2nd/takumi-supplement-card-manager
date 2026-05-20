#!/usr/bin/env python3
"""fetch-notion-transactions — read-only Notion transaction query.

deterministic + idempotent — safe to re-run.

Reads a JSON filter spec from stdin (or --input <file>). Writes a JSON
envelope to stdout:

  {
    "holder": "nuta",
    "card": "First Choice" | null,
    "count": 3,
    "results": [ { id, url, name, amount, transaction_date, ... }, ... ]
  }

Input schema (all keys optional except `holder`):

  {
    "holder":                 "takumi" | "baiboon" | "nuta",
    "card":                   "First Choice",            // exact title match
    "bill_cycle":             "2026-05-29",              // ISO date
    "bill_cycle_range":       ["2026-05-01", "2026-05-31"],
    "transaction_date_range": ["2026-05-01", "2026-05-31"],
    "min_amount":             100,
    "max_amount":             5000,
    "processed":              true,
    "paid":                   false,
    "credit_return":          false,
    "note_contains":          "uber",
    "sort":                   "date_desc",               // see filters.SORT_MAP
    "limit":                  5
  }
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import notion_client
from lib.cards import find_card
from lib.holders import resolve_holder
from lib.transaction_read import project_transaction

from filters import build_filter, resolve_sort


def run(spec: dict) -> dict:
    holder = resolve_holder(spec["holder"])

    card_page_id: str | None = None
    card_title: str | None = None
    if (card_name := spec.get("card")):
        card = find_card(holder.cards_ds, card_name)
        card_page_id = card["id"]
        card_title = card_name

    filter_ = build_filter(spec, card_page_id)
    sorts = resolve_sort(spec)
    limit = spec.get("limit")

    if isinstance(limit, int) and 0 < limit <= 100:
        pages = notion_client.query_page(
            holder.transactions_ds,
            page_size=limit,
            **({"filter": filter_} if filter_ else {}),
            sorts=sorts,
        )
    else:
        pages = notion_client.query_all(
            holder.transactions_ds,
            **({"filter": filter_} if filter_ else {}),
            sorts=sorts,
        )
        if isinstance(limit, int) and limit > 0:
            pages = pages[:limit]

    return {
        "holder": holder.key,
        "card": card_title,
        "count": len(pages),
        "results": [project_transaction(p) for p in pages],
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
