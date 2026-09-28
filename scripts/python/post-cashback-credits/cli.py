#!/usr/bin/env python3
"""post-cashback-credits — write a card's cashback credit rows for one bill cycle.

deterministic + idempotent — re-running with the same (holder, cycle) refuses
to overwrite: if any `*CASHBACK*` row already exists in the cycle on the card,
the script aborts so a second run doesn't double-credit. Pass `force` to
override after archiving the prior rows.

The card's Crediting class (lib/crediting) builds the rows. UOB One follows
the household's agreement (user, 2026-05-25, kept 2026-09-28): per bill cycle,
one row per `% cb` tier — `UOB ONE CASHBACK 1%` dated the BC date,
`UOB ONE CASHBACK 10%` / `5%` dated the first weekday of the next month — all
billed on the cycle, amount = −round(rate × tier sum, 2), ×0. The cycle's
in-progress installment terms are populated first (each earns 1%); skip with
`skip_populate_installments`.

Reads a JSON spec from stdin (or --input <file>):

  {
    "holder":     "baiboon" | "nuta",       // required (Takumi's credits come off his statement)
    "card":       "UOB One",                // required; a card with a Crediting class
    "bill_cycle": "2026-05-25",             // optional ISO; inferred via active_cycle if omitted
    "skip_populate_installments": false,    // optional; skip the installment populate step
    "force":      false                     // optional; override the duplicate-CASHBACK guard
  }

Writes a JSON envelope to stdout:

  {
    "holder": "baiboon", "card": "UOB One",
    "bill_cycle": "2026-05-25", "due_date": "2026-06-15",
    "installments": {...},
    "tier_totals": {"0.01": 6061.40, "0.05": 2048.00},
    "counted_next_cycle": [...],   // UOB One: rows posted on the statement date (their cashback moves on)
    "plan":    [ {name, amount, date, note}, ... ],        // --dry-run
    "created": [ {name, amount, date, bill_cycle, id}, ... ]
  }

Tiers with a sum ≤ 0 are skipped (no zero-baht placeholder rows).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import crediting  # noqa: E402
from lib.bureau.sync import Writer  # noqa: E402
from lib.cards import find_card  # noqa: E402
from lib.holders import resolve_holder  # noqa: E402


def run(spec: dict, *, dry_run: bool = False) -> dict:
    for key in ("holder", "card"):
        if not spec.get(key):
            raise crediting.CreditingError(f"missing required field: {key!r}")
    holder = resolve_holder(spec["holder"])
    credit = crediting.for_card(spec["card"])
    card_id = find_card(holder.cards_ds, credit.card)["id"]
    write = Writer(dry_run)

    plan = credit.plan(holder, card_id, spec, write)
    out = {
        "holder": holder.key,
        "card": credit.card,
        "bill_cycle": plan.detail.get("bill_cycle"),
        "due_date": plan.detail.get("due_date"),
        "installments": plan.detail.get("installments"),
        "tier_totals": plan.detail.get("tier_totals"),
    }
    if plan.detail.get("counted_next_cycle"):
        out["counted_next_cycle"] = plan.detail["counted_next_cycle"]
    if dry_run:
        return out | {"dry_run": True, "plan": [
            {"name": r.name, "amount": float(r.amount), "date": r.date, "note": r.note} for r in plan.rows]}
    return out | {"created": credit.post(holder, card_id, plan)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Compute the plan without writing")
    ap.add_argument("--force", action="store_true", help="Override the duplicate-CASHBACK guard")
    args = ap.parse_args(argv)
    spec = json.loads(args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read())
    if args.force:
        spec["force"] = True
    json.dump(run(spec, dry_run=args.dry_run), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
