#!/usr/bin/env python3
"""classify-transaction — preview the cashback / points classification for
one or more transactions, WITHOUT writing anything.

Read-only. This is the inspectable front-end to `lib.promotions.classify`
(the same logic /add-transaction, /add-installment, /populate-installment
run behind `auto_classify: true`). Use it to see *what* a promotion would
assign — `% cb`, multiplier, the exclusion/tier reason, and the suggested
Note — before committing a write. The classification is pure: it reads the
card repo + promotion YAML, never Notion.

Reads a JSON spec from stdin (or --input <file>):

  {
    "card": "UOB One",
    "transactions": [
      { "date": "2026-05-29", "name": "WWW.GRAB.COM BANGKOK TH", "amount": 250 },
      { "date": "2026-05-29", "name": "2C2P *SHOPEE 03/10",      "amount": 1079.2 }
    ]
  }

`amount` is optional per row — when present, the preview also reports the
baht cashback (`% cb` × amount). A single transaction may be given inline
at the top level ({card, date, name, amount}) instead of via `transactions`.

Output envelope:

  {
    "card": "UOB One",
    "card_known": true,                 // false => card not in scripts/repositories/cards (likely a typo)
    "count": 2,
    "classifications": [
      {
        "name": "WWW.GRAB.COM BANGKOK TH", "date": "2026-05-29", "amount": 250,
        "promotion_id": "uob-one-2026", "reason": "tier",
        "cashback_percent": 0.05, "cashback_display": "5%", "cashback_amount": 12.5,
        "multiplier": "×0", "note": null
      },
      ...
    ]
  }

This skill never mutates Notion or any repo file. Hand the previewed values
to /add-transaction (with explicit per-row `cashback_percent` / `multiplier`)
when you're ready to write.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import card_repo, promotions


def _percent_display(fraction: float | None) -> str | None:
    if fraction is None:
        return None
    # raw fraction (0.05) -> "5%"; strip trailing zeros (0.015 -> "1.5%")
    return f"{fraction * 100:g}%"


def _normalize_transactions(spec: dict) -> list[dict]:
    txns = spec.get("transactions")
    if txns is None:
        # Allow a single inline transaction at the top level.
        if spec.get("name") and spec.get("date"):
            return [{"date": spec["date"], "name": spec["name"], "amount": spec.get("amount")}]
        raise ValueError("spec needs `transactions` (a list) or inline `date` + `name`")
    if not isinstance(txns, list) or not txns:
        raise ValueError("`transactions` must be a non-empty list")
    return txns


def run(spec: dict) -> dict:
    if not isinstance(spec, dict):
        raise ValueError("spec must be a JSON object")
    card = spec.get("card")
    if not card:
        raise ValueError("missing required field 'card'")

    txns = _normalize_transactions(spec)

    out_rows: list[dict] = []
    for tx in txns:
        if not tx.get("date") or not tx.get("name"):
            raise ValueError(f"each transaction needs `date` and `name`; got {tx!r}")
        cls = promotions.classify(card, _dt.date.fromisoformat(tx["date"]), tx["name"])
        amount = tx.get("amount")
        cashback_amount = None
        if amount is not None and cls.cashback_percent is not None:
            cashback_amount = round(float(amount) * cls.cashback_percent, 2)
        out_rows.append(
            {
                "name": tx["name"],
                "date": tx["date"],
                "amount": amount,
                "promotion_id": cls.promotion_id,
                "reason": cls.reason,
                "cashback_percent": cls.cashback_percent,
                "cashback_display": _percent_display(cls.cashback_percent),
                "cashback_amount": cashback_amount,
                "multiplier": cls.points_override,
                "note": cls.note,
            }
        )

    return {
        "card": card,
        "card_known": card_repo.get(card) is not None,
        "count": len(out_rows),
        "classifications": out_rows,
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
