#!/usr/bin/env python3
"""sync-promotion — bring one Promotion Bureau row up to date.

deterministic + idempotent — every write sets a value to what the linked
transactions imply, and creates a Bureau or tracker row only when none exists;
a second run with nothing changed writes nothing.

For one Bureau row (one quota period, e.g. `2026M9 — NW3 cb 2%`), with the
campaign class from `lib.bureau` that matches it:

1. Creates the row when it doesn't exist yet and `start`/`end` are given.
2. Reads every holder's linked transactions and screens them; lists the
   campaign cards' unlinked rows in the period as candidates, and links the
   eligible ones with `link_candidates` (lib.bureau.sync).
3. Splits the reward first come, first served (the campaign's `allocate`).
4. Cashback campaigns: writes `เงินคืนรวม` when empty and `เงินคืนส่วน<name>`,
   and upserts each holder's tracker row (lib.bureau.settle). Points
   campaigns have no money to settle.
5. Checks every linked row's fields against the split (`expected`: `% cb`,
   multiplier, points used) and lists disagreements with ready
   /update-transaction entries — read-only.
6. Writes the campaign summary into the page body when it's empty (or always,
   with `replace_summary`).

A campaign with a nationwide pool (UnionPay QR) first reads the bank's page
and records the day the pool ran out in `Quotas Exceeded Date` (lib.bureau.quota).

Spec (stdin or --input):
  {
    "promotion":       "2026M9 — NW3 cb 2%",  // Bureau row Name, page ID or URL
    "start": "2026-09-01", "end": "2026-09-30",  // optional: create the row if missing
    "bank_spend":      36803.92,              // optional: the bank app's eligible total
    "link_candidates": false,                 // optional: link eligible unlinked rows
    "replace_summary": false,                 // optional: rewrite a non-empty page body
    "quota_gone":      "2026-09-12"           // optional: the day a nationwide pool ran out (UnionPay QR)
  }

--dry-run computes and reports everything without writing.

The work is `lib.bureau.runner.run`; /add-transaction, /update-transaction and
/record-statement reach it through `lib.bureau.follow` after they write rows.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.bureau.runner import run  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text() if args.input else sys.stdin.read())
    print(json.dumps(run(spec, dry_run=args.dry_run), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
