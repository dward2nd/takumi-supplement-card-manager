#!/usr/bin/env python3
"""post-cashback-credits — write a card's cashback credit rows into a holder's ledger.

deterministic + idempotent — a period whose credit row already exists is
reported under `already_posted` and skipped (override with `force`, after
archiving the old row); linking rows to the Bureau is a no-op once done.

The card's own Crediting class decides the periods, the dates and the amounts
(lib/crediting). Today that's UOB One, credited the way the bank does it:

  1%      per statement cycle, dated the statement date     `UOB ONE CASHBACK 1%`
  10%/5%  per calendar month, dated its last day (the next  `UOB ONE CASHBACK 10%` / `5%`
          working day if that's a weekend or holiday),
          billed on the cycle that date falls in

Amounts are the holder's first-come-first-served share of the account's
capped cashback, taken from the Promotion Bureau's UOB One rows (created and
linked here when missing), less cashback that already reached the holder
through a carry-forward leg carrying `% cb`. Before the 1%, this cycle's
installment terms are populated (each earns 1%); skip with
`skip_populate_installments`.

Spec (stdin or --input):
  {
    "holder":     "baiboon" | "nuta",   // required; Takumi's credits come off his statement
    "card":       "UOB One",            // required; a card with a Crediting class
    "bill_cycle": "2026-09-25",         // optional: post the 1% for this cycle
    "month":      "2026-09",            // optional: post the 10%/5% for this calendar month
    "skip_populate_installments": false,
    "force":      false                 // re-post a period whose row exists (archive it first)
  }
With neither `bill_cycle` nor `month`: the most recently closed cycle and the
last completed calendar month.

Envelope: {holder, card, detail (per period: Bureau row, share, adjustment,
credit), already_posted, plan, writes (links, installment terms, Bureau rows),
created, dry_run}.
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
    created = [] if dry_run else credit.post(holder, card_id, plan)
    return {
        "holder": holder.key,
        "card": credit.card,
        "detail": plan.detail,
        "already_posted": plan.already_posted,
        "plan": [{"name": r.name, "amount": float(r.amount), "date": r.date, "bill_cycle": r.bill_cycle,
                  "due_date": r.due_date, "note": r.note} for r in plan.rows],
        "writes": write.done,
        "created": created,
        "dry_run": dry_run,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Plan without writing")
    ap.add_argument("--force", action="store_true", help="Re-post periods whose row already exists")
    args = ap.parse_args(argv)
    spec = json.loads(args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read())
    if args.force:
        spec["force"] = True
    json.dump(run(spec, dry_run=args.dry_run), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
