#!/usr/bin/env python3
"""archive — soft-delete one or more Notion transaction pages.

deterministic + idempotent — re-archiving an already-archived page is a no-op.

Companion to cli.py. Used to roll back a mistaken write, or to clean
up test rows after script/skill cooperation checks. Reads page IDs
from --ids (comma-separated) or stdin (one ID per line, or JSON list).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import notion_client


def _parse_ids(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    if raw.startswith("["):
        return [str(x) for x in json.loads(raw)]
    return [line.strip() for line in raw.splitlines() if line.strip()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ids", help="Comma-separated page IDs (otherwise read from stdin)")
    args = ap.parse_args(argv)

    if args.ids:
        ids = [s.strip() for s in args.ids.split(",") if s.strip()]
    else:
        ids = _parse_ids(sys.stdin.read())

    if not ids:
        print("no page IDs supplied", file=sys.stderr)
        return 2

    archived: list[dict] = []
    for page_id in ids:
        resp = notion_client.archive_page(page_id)
        archived.append({"id": resp.get("id"), "archived": resp.get("archived", True)})

    json.dump({"count": len(archived), "archived": archived}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
