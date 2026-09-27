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
   eligible ones with `link_candidates` (gather.py).
3. Splits the reward first come, first served (the campaign's `allocate`).
4. Cashback campaigns: writes `เงินคืนรวม` when empty and `เงินคืนส่วน<name>`,
   and upserts each holder's tracker row (settle.py). Points campaigns have
   no money to settle.
5. Checks every linked row's fields against the split (`expected`: `% cb`,
   multiplier, points used) and lists disagreements with ready
   /update-transaction entries — read-only.
6. Writes the campaign summary into the page body when it's empty (or always,
   with `replace_summary`).

Spec (stdin or --input):
  {
    "promotion":       "2026M9 — NW3 cb 2%",  // Bureau row Name, page ID or URL
    "start": "2026-09-01", "end": "2026-09-30",  // optional: create the row if missing
    "bank_spend":      36803.92,              // optional: the bank app's eligible total
    "link_candidates": false,                 // optional: link eligible unlinked rows
    "replace_summary": false                  // optional: rewrite a non-empty page body
  }

--dry-run computes and reports everything without writing.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.bureau import CASHBACK, promotion_for, store  # noqa: E402
from lib.holders import HOLDERS  # noqa: E402

import gather  # noqa: E402
import report  # noqa: E402
import settle  # noqa: E402


class Writer:
    """Records every write; performs it unless this is a dry run."""

    def __init__(self, dry_run: bool):
        self.dry_run, self.done = dry_run, []

    def __call__(self, what: str, fn, *args, **kwargs) -> None:
        self.done.append(what)
        if not self.dry_run:
            fn(*args, **kwargs)


def _find_or_create(spec: dict, write: Writer):
    try:
        return store.find_row(spec["promotion"])
    except LookupError:
        if not (spec.get("start") and spec.get("end")):
            raise
    start, end = dt.date.fromisoformat(spec["start"]), dt.date.fromisoformat(spec["end"])
    promotion_for(spec["promotion"], start, end)  # refuse a row no campaign class would match
    if write.dry_run:
        return None
    write.done.append(f"create Bureau row {spec['promotion']!r} {start}→{end}")
    return store.create_row(spec["promotion"], start, end)


def run(spec: dict, *, dry_run: bool = False) -> dict:
    write = Writer(dry_run)
    row = _find_or_create(spec, write)
    if row is None:
        return {"would_create": {"name": spec["promotion"], "start": spec["start"], "end": spec["end"]},
                "dry_run": True}
    promo = promotion_for(row.name, row.start, row.end)

    cards = gather.campaign_cards(promo)
    txs, candidates, warnings = gather.collect(row, promo, cards, link=bool(spec.get("link_candidates")),
                                               write=write)
    alloc = promo.allocate(txs)
    warnings += alloc.warnings
    flagged, flagged_ids = report.flagged(promo, txs)
    mismatched = report.field_mismatches(promo, alloc)
    if mismatched:
        warnings.append(f"{len(mismatched)} linked row(s) carry fields the split disagrees with — see "
                        f"field_mismatches; fix with /update-transaction")

    totals = {"pooled": float(alloc.pooled), "counted": float(alloc.counted)}
    trackers: dict[str, list[str]] = {}
    if promo.reward == CASHBACK:
        without_flagged = promo.allocate([t for t in txs if t.id not in flagged_ids])
        totals |= {"credit": float(alloc.credit),
                   "entered": None if row.total is None else float(row.total),
                   "if_flagged_rejected": float(without_flagged.credit)}
        shares_ok, w = settle.bureau_numbers(row, alloc, write)
        warnings += w
        if shares_ok:
            trackers, w = settle.trackers(row, promo, alloc, txs, cards, write)
            warnings += w

    body = store.body_block_ids(row.id)
    if not body or spec.get("replace_summary"):
        write(f"{'replace' if body else 'write'} page summary", store.write_body, row.id,
              promo.summary_blocks(), replace=bool(body))

    out = {
        "promotion": {"name": row.name, "url": row.url, "class": type(promo).__name__,
                      "reward": promo.reward, "period": [row.start.isoformat(), row.end.isoformat()]},
        "spend": {h.key: float(sum((t.amount for t in txs if t.holder == h.key), Decimal(0)))
                  for h in HOLDERS.values()},
        "totals": totals,
        "shares": {k: float(v) for k, v in alloc.shares.items()},
        "boundary": report.boundary(alloc),
        "field_mismatches": mismatched,
        "flagged": flagged,
        "unlinked_candidates": candidates,
        "trackers": trackers,
        "writes": write.done,
        "warnings": warnings,
        "dry_run": dry_run,
    }
    if spec.get("bank_spend") is not None:
        out["drift"] = report.drift(promo, alloc, txs, Decimal(str(spec["bank_spend"])))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text() if args.input else sys.stdin.read())
    print(json.dumps(run(spec, dry_run=args.dry_run), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
