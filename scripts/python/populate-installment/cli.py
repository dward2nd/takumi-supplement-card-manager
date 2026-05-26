#!/usr/bin/env python3
"""populate-installment — append next-term rows for all in-progress installment plans.

deterministic + idempotent — re-running for the same (holder, card,
target_cycle) is a no-op: a plan whose cluster already has a row in
the target cycle is skipped.

Core logic lives in ``lib.installments.populate_for_cycle``; this CLI is
the thin user-facing wrapper (spec validation, default target cycle,
JSON I/O). The same library function is invoked by /prepare-bill so the
two skills never disagree on which rows would be appended.

Usage:

  echo '<JSON-spec>' | uv run scripts/python/populate-installment/cli.py

JSON spec:

  {
    "holder":      "baiboon" | "nuta" | "takumi",   // required
    "card":        "UOB One",                        // required, exact title match
    "bill_cycle":  "2026-05-25",                     // optional; default = most
                                                     //   recently closed cycle
    "exclude":     ["2C2P *SHOPEE"],                 // optional; base merchant names
                                                     //   to skip (e.g. a plan the user
                                                     //   has cancelled or closed early)
    "auto_classify": true                            // optional, default true
  }
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import installments
from lib.bill_cycle import most_recent_closed_cycle, pattern_for_card, cycle_for_month
from lib.cards import find_card
from lib.holders import resolve_holder


_REQUIRED = ("holder", "card")


class SpecError(ValueError):
    pass


def _validate(spec: dict) -> None:
    if not isinstance(spec, dict):
        raise SpecError("spec must be a JSON object")
    missing = [k for k in _REQUIRED if k not in spec]
    if missing:
        raise SpecError(f"missing required fields: {missing}")
    if "bill_cycle" in spec and spec["bill_cycle"] is not None:
        try:
            _dt.date.fromisoformat(spec["bill_cycle"])
        except ValueError as e:
            raise SpecError(f"bill_cycle is not a valid ISO date: {e}") from None
    if "exclude" in spec and spec["exclude"] is not None:
        if not isinstance(spec["exclude"], list) or not all(
            isinstance(x, str) for x in spec["exclude"]
        ):
            raise SpecError("exclude must be a list of base-merchant strings")


def _resolve_cycle(card_name: str, spec_bc: str | None) -> tuple[str, str]:
    if spec_bc:
        bc = _dt.date.fromisoformat(spec_bc)
        pattern = pattern_for_card(card_name)
        cand_bc, cand_dd = cycle_for_month(pattern, bc.year, bc.month)
        if cand_bc != bc:
            cand_dd = pattern.due_date_shift(pattern.due_from_nominal_bc(bc))
            cand_bc = bc
        return cand_bc.isoformat(), cand_dd.isoformat()
    bc, dd = most_recent_closed_cycle(card_name, _dt.date.today())
    return bc.isoformat(), dd.isoformat()


def run(spec: dict, *, dry_run: bool = False) -> dict:
    _validate(spec)
    holder = resolve_holder(spec["holder"])
    card_name = spec["card"]
    card = find_card(holder.cards_ds, card_name)
    card_page_id = card["id"]

    bill_cycle, due_date = _resolve_cycle(card_name, spec.get("bill_cycle"))
    exclude = set((spec.get("exclude") or []))
    auto_classify = bool(spec.get("auto_classify", True))

    result = installments.populate_for_cycle(
        holder_key=holder.key,
        transactions_ds=holder.transactions_ds,
        card_name=card_name,
        card_page_id=card_page_id,
        bill_cycle=bill_cycle,
        due_date=due_date,
        auto_classify=auto_classify,
        exclude=exclude,
        dry_run=dry_run,
    )

    return {
        "holder": holder.key,
        "card": card_name,
        "card_page_id": card_page_id,
        "bill_cycle": bill_cycle,
        "due_date": due_date,
        **result,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Plan appends without calling Notion")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
