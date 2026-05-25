#!/usr/bin/env python3
"""add-transaction — write transactions to Notion.

deterministic + idempotent — re-running creates new pages, so callers
should not retry on success. (No upsert: Notion has no natural key on
transactions, and the system relies on bank-statement reconciliation
of verbatim merchant names instead.)

Reads a JSON spec from stdin (or --input <file>). Writes a JSON
envelope to stdout:

  {
    "holder": "nuta",
    "card": "First Choice",
    "bill_cycle": "2026-05-29",
    "due_date": "2026-06-15",
    "count": 1,
    "created": [ { id, url, name, amount }, ... ]
  }

Input schema:

  {
    "holder":      "takumi" | "baiboon" | "nuta",   // required
    "card":        "First Choice",                  // required, exact title match
    "bill_cycle":  "2026-05-29",                    // optional ISO date, applied to
                                                    //   the whole batch; if omitted
                                                    //   (together with due_date),
                                                    //   inferred from the card's
                                                    //   bank pattern — see
                                                    //   lib/bill_cycle.py
    "due_date":    "2026-06-15",                    // optional ISO date, paired with
                                                    //   bill_cycle (both or neither)
    "processed":   true,                            // optional, default true
    "multiplier":  "×0",                            // optional, batch-level default;
                                                    //   one of ×0/×2/×3/×4/×5/÷4 or null
    "cashback_percent": 0.01,                       // optional, batch-level default;
                                                    //   Baiboon + Nuta only (% cb does
                                                    //   not exist on Takumi's DS);
                                                    //   raw fraction (0.05 == 5%)
    "transactions": [                                // required, non-empty
      {
        "date":              "2026-05-13",          // ISO date
        "name":              "TMN 7-11 BANGKOK TH", // verbatim merchant string
        "amount":            89.0,                  // baht
        "note":              "...",                 // optional
        "multiplier":        "×2",                  // optional, overrides batch
        "cashback_percent":  0.05                   // optional, overrides batch
      }
    ]
  }

Hard rules enforced here:
  1. `name` is written verbatim — no trimming or normalization.
  2. Holder routes to the correct transactions DS; never cross-write.
  3. Card relation must resolve to exactly one card; otherwise abort.
  4. `Processed` defaults to true unless the spec says otherwise.
  5. At most one multiplier checkbox is set per page. Absence ⇒ ×1.
  6. cashback_percent is Baiboon + Nuta only; rejected for Takumi at spec-validation
     (the `% cb` property does not exist on Takumi's Transactions DS).

--dry-run builds the payload and reports it without calling Notion.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import notion_client
from lib.bill_cycle import active_cycle
from lib.cards import find_card
from lib.holders import resolve_holder
from lib.transaction_write import build_transaction_properties

from validation import validate_spec


def run(spec: dict, *, dry_run: bool = False) -> dict:
    validate_spec(spec)
    holder = resolve_holder(spec["holder"])
    card = find_card(holder.cards_ds, spec["card"])
    card_page_id = card["id"]

    bill_cycle = spec.get("bill_cycle")
    due_date = spec.get("due_date")
    if not bill_cycle or not due_date:
        # Validation guarantees both-or-neither; only the neither path
        # reaches here. Infer from the card's bank pattern.
        bc, dd = active_cycle(spec["card"], _dt.date.today())
        bill_cycle = bc.isoformat()
        due_date = dd.isoformat()

    processed = spec.get("processed", True)
    batch_multiplier = spec.get("multiplier")
    batch_cashback = spec.get("cashback_percent")

    created: list[dict] = []
    for tx in spec["transactions"]:
        props = build_transaction_properties(
            name=tx["name"],
            amount=float(tx["amount"]),
            transaction_date=tx["date"],
            bill_cycle_date=bill_cycle,
            due_date=due_date,
            card_page_id=card_page_id,
            processed=processed,
            note=tx.get("note"),
            multiplier=tx.get("multiplier", batch_multiplier),
            cashback_percent=tx.get("cashback_percent", batch_cashback),
        )
        if dry_run:
            created.append({"dry_run": True, "properties": props})
            continue
        page = notion_client.create_page(holder.transactions_ds, props)
        created.append({
            "id": page["id"],
            "url": page.get("url"),
            "name": tx["name"],
            "amount": float(tx["amount"]),
            "date": tx["date"],
        })

    return {
        "holder": holder.key,
        "card": spec["card"],
        "card_page_id": card_page_id,
        "bill_cycle": bill_cycle,
        "due_date": due_date,
        "processed": processed,
        "count": len(created),
        "created": created,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Build payloads without calling Notion")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
