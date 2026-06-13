#!/usr/bin/env python3
"""record-payment — record a bill payment as a negative-amount transaction.

deterministic given its inputs; guards against double-recording by
scanning the cycle for a matching payment row before creating, so
re-running the same payment is effectively idempotent (unless `force`).

A payment is a negative `ยอดชำระ` row in the Transactions DB tagged to
the *paid bill's* cycle (same `Bill Cycle Date` / `Due Date` as that
cycle's charges), `Transaction Datetime` = the slip date, and **no
cashback**. See `lib.payments` for the model rationale.

Reads a JSON spec from stdin (or --input <file>):

  {
    "holder":       "baiboon" | "nuta",   // required (takumi has no Bills DB)
    "card":         "UOB One",             // required, exact Cards-DB title
    "bill_cycle":   "2026-05-25",          // required, วันตัดรอบบิล of the bill being paid

    "amount":       10693.09,              // payment magnitude (positive); stored negated.
                                           //   OMIT with kind="full" -> taken from the bill's ยอดชำระ
    "payment_date": "2026-05-29",          // slip date; default today
    "kind":         "full",                // full | partial | advance (default full)
    "name":         "...",                 // label override (default per kind)
    "note":         "...",                 // optional Note
    "due_date":     "2026-06-14",          // optional; else from the cycle's rows / bank pattern
    "force":        false                  // create even if a matching payment already exists
  }

Output envelope:

  {
    "created":      true,
    "id":           "<new-tx-page-id>",
    "holder":       "nuta",
    "card":         "UOB One",
    "bill_cycle":   "2026-05-25",
    "amount":       -10693.09,            // negative (a payment)
    "name":         "ชำระบิลเต็มจำนวน",
    "payment_date": "2026-05-29",
    "due_date":     "2026-06-14",
    "existing_payments": [ ... ]          // payment rows already in the cycle
  }

When a matching payment already exists, `created` is false and `reason`
explains the match (so the caller can see the dedup fired).

--dry-run resolves + dedups + builds the payload without writing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import payments
from lib.bills import find_bill
from lib.holders import resolve_holder


def _bill_amount(holder, card: str, bill_cycle: str) -> float:
    """Read `ยอดชำระ` off the (holder, card, bill_cycle) Bills row."""
    bill = find_bill(holder, card, bill_cycle)
    amount = (bill["properties"].get("ยอดชำระ", {}) or {}).get("number")
    if amount is None:
        raise ValueError(
            f"bill for card={card!r} วันตัดรอบบิล={bill_cycle!r} has no ยอดชำระ — "
            "pass an explicit `amount`"
        )
    return float(amount)


def run(spec: dict, *, dry_run: bool = False) -> dict:
    if not isinstance(spec, dict):
        raise ValueError("spec must be a JSON object")
    for key in ("holder", "card", "bill_cycle"):
        if not spec.get(key):
            raise ValueError(f"missing required field {key!r}")

    holder = resolve_holder(spec["holder"])
    card = spec["card"]
    bill_cycle = spec["bill_cycle"]
    kind = spec.get("kind", "full")

    amount = spec.get("amount")
    if amount is None:
        if kind != "full":
            raise ValueError(f"`amount` is required when kind={kind!r}")
        # full payment with no explicit amount -> take the bill's ยอดชำระ
        amount = _bill_amount(holder, card, bill_cycle)

    return payments.record_payment(
        holder,
        card,
        bill_cycle,
        amount=float(amount),
        payment_date=spec.get("payment_date"),
        kind=kind,
        name=spec.get("name"),
        note=spec.get("note"),
        due_date=spec.get("due_date"),
        force=bool(spec.get("force", False)),
        dry_run=dry_run,
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Resolve without writing")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
