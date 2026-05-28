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
  - note            → writes Notion `Note`; `""` (empty string) clears
  - multiplier      → writes one of `×0`/`×2`/`×3`/`×4`/`×5`/`÷4` to true
  - points_redeemed → writes Notion `ใช้คะแนน`; `null` clears.
                      Positive = deduct from lifetime, negative = add back.
  - bill_cycle      → writes `Bill Cycle Date` (ISO date). Re-cycle a row
                      (backdate to a closed cycle, or foredate to next).
                      Must be paired with `due_date` so the pair stays
                      consistent for that card's bank pattern.
  - due_date        → writes `Due Date` (ISO date). Pair with bill_cycle.
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


# Sentinel for "key was absent from the update", distinguishing it from
# "user explicitly passed null to clear the underlying Notion field".
_MISSING = object()


def _build_properties(update: dict) -> dict:
    props: dict = {}

    # `cashback_percent: null` clears `% cb` (writes JSON null → empty cell).
    # Distinguishes "user wants to clear" from "user didn't mention this
    # field" — the latter is the absence of the key.
    cb = update.get("cashback_percent", _MISSING)
    if cb is None:
        props["% cb"] = {"number": None}
    elif cb is not _MISSING:
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

    # `points_redeemed: null` clears `ใช้คะแนน` (mirrors cashback_percent's
    # sentinel semantics). Positive = deduct from lifetime balance, negative
    # = add back. The field exists on all three holders' Transactions DSes.
    pts = update.get("points_redeemed", _MISSING)
    if pts is None:
        props["ใช้คะแนน"] = {"number": None}
    elif pts is not _MISSING:
        if not isinstance(pts, (int, float)) or isinstance(pts, bool):
            raise ValueError(
                f"points_redeemed must be a number (or null to clear); got {pts!r}"
            )
        props["ใช้คะแนน"] = {"number": float(pts)}

    # bill_cycle / due_date: re-cycle a row (backdate or foredate). The two
    # dates form a pair on a given card — passing one without the other
    # leaves the row half-updated, which we refuse. Use the issuer's bill
    # cycle pattern (docs/concepts/bill-cycle-patterns) to pick a
    # consistent pair if you're not sure.
    has_bc = "bill_cycle" in update
    has_dd = "due_date" in update
    if has_bc ^ has_dd:
        raise ValueError(
            "bill_cycle and due_date must be provided together "
            "(both move the row to a different cycle); got one without the other"
        )
    if has_bc and has_dd:
        bc = update["bill_cycle"]
        dd = update["due_date"]
        if not isinstance(bc, str) or not isinstance(dd, str):
            raise ValueError(
                f"bill_cycle / due_date must be ISO date strings; got {bc!r} / {dd!r}"
            )
        # Best-effort ISO parse to fail loud on typos. Don't enforce the
        # bank's per-issuer cycle math here — the caller might be writing
        # an adjustment row outside the normal pattern.
        import datetime as _dt
        try:
            _dt.date.fromisoformat(bc)
            _dt.date.fromisoformat(dd)
        except ValueError as e:
            raise ValueError(
                f"bill_cycle / due_date must be valid ISO dates: {e}"
            ) from None
        props["Bill Cycle Date"] = {"date": {"start": bc}}
        props["Due Date"] = {"date": {"start": dd}}

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
