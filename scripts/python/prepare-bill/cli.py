#!/usr/bin/env python3
"""prepare-bill — draft a Bills row from the cycle's transactions.

deterministic + idempotent — re-running with the same (holder, card,
bill_cycle) refuses to create a duplicate. A Bills row uniquely
identifies on (Card, วันตัดรอบบิล); the script aborts when one
already exists for that pair (draft or final).

Sums `ยอดชำระ` across every transaction row whose `Bill Cycle Date`
equals the cycle's BC date for the named card. The cashback offset is
already encoded in the data: at cycle close, the `/prepare-bill` flow
expects cashback credit transactions to have been written as
negative-amount rows in the same cycle (see add-transaction's UOB One
policy notes), so a flat sum here is the "balance including cashback".

The new Bills row is written with `[DRAFT] ` prefixed to its title.
The user strips the prefix manually once the official statement
arrives — or uploads the PDF via /update-bill, which can also drop
the prefix.

Reads a JSON spec from stdin (or --input <file>):

  {
    "holder":     "baiboon" | "nuta" | "takumi", // required; takumi → an estimate from all
                                               //   three ledgers (lib.bill_draft.draft_primary_bill),
                                               //   plus "unmonitored": <amount> for a card with an
                                               //   untracked supplement
    "card":       "UOB One",                   // required, must match a SELECT option
    "bill_cycle": "2026-05-25",                // optional ISO date; inferred if omitted
    "skip_populate_installments": false,       // optional; default false. When false,
                                               //   in-progress installments on this card
                                               //   are auto-populated into the cycle
                                               //   BEFORE the sum is computed, so the
                                               //   drafted balance reflects them.
    "skip_auto_note": false                    // optional; default false. When false,
                                               //   the bill's Note is auto-generated to
                                               //   explain special rows (cashback credits,
                                               //   installment terms, manual adjustments).
                                               //   Set true to leave Note blank.
  }

Writes a JSON envelope to stdout:

  {
    "id":         "<new-bill-page-id>",
    "url":        "https://www.notion.so/...",
    "holder":     "baiboon",
    "card":       "UOB One",
    "bill_cycle": "2026-05-25",
    "title":      "[DRAFT] UOB One 2026-05",
    "ยอดชำระ":     1810.97,
    "tx_count":   12
  }

--dry-run resolves the cycle + total without writing anything.

Date-range mode — draft every cycle whose BC falls in a window, across
cards and holders. Selected by the presence of `bill_cycle_from`:

  {
    "bill_cycle_from": "2026-09-25",           // required, ISO, inclusive
    "bill_cycle_to":   "2026-09-27",           // required, ISO, inclusive; ≤ 31 days
    "holders": ["baiboon", "nuta"],            // optional; default both (or "holder"); "takumi"
                                               //   drafts his statement bills at the estimate,
                                               //   with "unmonitored": {"<card>": <amount>}
    "cards":   ["UOB One"],                    // optional filter, case-insensitive
    "skip_populate_installments": false,       // optional; passed to every draft
    "skip_cashback_check": false,              //   "
    "skip_auto_note": false                    //   "
  }

Cycles come from the Transactions DBs' `Bill Cycle Date` values. Each is
drafted through the single-card path, so its guards still apply per cycle.
The envelope lists one result per (holder, card, BC) with a status —
`created` / `would-create`, `exists`, `off-pattern`, or `blocked` + reason
— and `counts` per status.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.bill_draft import DRAFT_PREFIX, BillDraftError, draft_bill, draft_bills_in_window  # noqa: F401

# The drafting core lives in `lib.bill_draft` so /update-bill can reuse it —
# it drafts a missing bill before attaching a payment slip. This module is
# the CLI surface. `PrepareBillError` stays as an alias so anything that
# catches it by name keeps working.
PrepareBillError = BillDraftError


def run(spec: dict, *, dry_run: bool = False) -> dict:
    if isinstance(spec, dict) and ("bill_cycle_from" in spec or "bill_cycle_to" in spec):
        return draft_bills_in_window(spec, dry_run=dry_run)
    return draft_bill(spec, dry_run=dry_run)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Compute the draft without writing")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
