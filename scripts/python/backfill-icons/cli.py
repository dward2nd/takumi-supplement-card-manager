#!/usr/bin/env python3
"""backfill-icons — give existing Notion rows the page icon a new row would get.

deterministic + idempotent — plans from each page's current properties; a
re-run writes only what still differs. Rows that already have an icon are
left alone unless --replace. The Cards DBs are never touched (see
docs/concepts/page-icons.md).

  uv run backfill-icons/cli.py [--dry-run] [--replace]
      [--db transactions,bills,bureau,trackers] [--holder takumi,baiboon,nuta]

Output: {"dry_run", "replace", "planned": {database: n}, "set": {database: n},
         "by_icon": {emoji: n}, "sample": [{database, title, old, new}]}
Progress goes to stderr every 100 writes.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.icons import backfill  # noqa: E402


def _label(icon: dict | None) -> str | None:
    if not icon:
        return None
    return icon.get("emoji") or (icon.get("custom_emoji") or {}).get("name") or icon.get("type")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--replace", action="store_true", help="also re-set pages whose existing icon differs")
    ap.add_argument("--db", default=",".join(backfill.DATABASES))
    ap.add_argument("--holder", default="")
    args = ap.parse_args()
    databases = tuple(d for d in args.db.split(",") if d)
    unknown = set(databases) - set(backfill.DATABASES)
    if unknown:
        ap.error(f"unknown --db {sorted(unknown)}; choose from {backfill.DATABASES}")
    holders = tuple(h for h in args.holder.split(",") if h) or None

    changes = backfill.plan(databases, holders, replace=args.replace)
    out = {
        "dry_run": args.dry_run,
        "replace": args.replace,
        "planned": dict(Counter(c.database for c in changes)),
        "by_icon": dict(Counter(_label(c.new) for c in changes).most_common()),
        "sample": [{"database": c.database, "title": c.title, "old": _label(c.old), "new": _label(c.new)}
                   for c in changes[:: max(1, len(changes) // 25)][:25]],
    }
    out["set"] = {} if args.dry_run else backfill.apply(changes)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
