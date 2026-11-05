#!/usr/bin/env python3
"""settle-tracker — link a cashback tracker row to the ledger credit(s) that settle it, and tick it.

deterministic + idempotent — safe to re-run. Links are merged (existing
`Slip Transaction` links are kept); a ticked tracker is frozen, so a re-run
reports `unchanged` and any other change to it is refused.

Reads a JSON spec from stdin (or --input <file>):

  {
    "holder":  "takumi | baiboon | nuta",
    "tracker": "UOB One 10%/5% 1—31 Oct",     // exact title, or page ID / URL
    "link":    ["<ledger row ID or URL>"],     // rows of the holder's OWN Transactions DS
    "tick":    "auto",                         // "auto" (default) | true | false
    "basis":   "auto",                         // "auto" | "exact" | "pooled" | "cycles" | "zero"
    "note":    "..."                           // replaces the tracker's Note; omit to keep it
  }

tick "auto" ticks only when the Bureau row's End Date has passed (or there
is no Bureau row) AND the basis holds:
  exact   Σ linked credit = Expected Cashback (±฿0.01)
  pooled  Takumi only: Σ linked credit = the Bureau row's เงินคืนรวม
  cycles  a linked credit's Bill Cycle Date is on/after the period's end
  zero    Expected Cashback ฿0 and nothing to link
"auto" basis tries exact, then pooled. tick true = the user said the money
arrived; tick false = link now, tick later.

--dry-run reports the plan without writing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.trackers.settle import FrozenTracker, Spec, settle


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Plan the writes without calling Notion's write API")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    try:
        out = settle(Spec.parse(json.loads(raw)), dry_run=args.dry_run)
        code = 0
    except (FrozenTracker, LookupError, ValueError, KeyError) as exc:
        out, code = {"error": f"{type(exc).__name__}: {exc}"}, 1
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
