#!/usr/bin/env python3
"""audit-bill — compare a bank statement against Notion for one (card, cycle).

deterministic + idempotent — read-only.

Diffs the transactions printed on a bank statement against the rows that
exist in Notion's Transactions DB for the same card and bill cycle. Reports:

- `missing_in_notion`: statement rows the matcher couldn't pair with any
  Notion row (charges absent from Notion — usually un-recorded).
- `extra_in_notion`: Notion rows the matcher couldn't pair with the
  statement (often cashback-credit convention rows, manual offsets like
  `[เว็บรับหนี้ไปบริหารต่อ]`, or — the case this skill exists for —
  charges that got cancelled by the bank but never deleted from Notion).
- `subtotal`: statement vs Notion totals + the signed delta.

The skill never mutates Notion. After reviewing the findings, use
/update-transaction (one row) or /add-transaction (missing rows) to
reconcile, per the user's judgment.

Reads a JSON spec from stdin (or --input <file>):

  {
    "holder":     "takumi" | "baiboon" | "nuta",  // required
    "card":       "UOB One",                      // required, exact title
    "bill_cycle": "2026-04-24",                   // optional ISO; default = most recently closed
    "statement_subtotal": 17936.84,               // optional; the bank's printed sub-total

    // Required: the rows from the statement's section for THIS (card, holder).
    // Caller pre-parses the PDF and feeds them here. CR/credit/refund rows
    // are passed with negative amounts. Skip any rows the bank prints that
    // aren't actual charges (PREVIOUS BALANCE, SUB TOTAL, etc.).
    "statement_transactions": [
      {"date": "2026-03-25", "name": "(FOR SHOPEE)*(FOR SHOP BANGKOK", "amount": 182.00},
      {"date": "2026-03-25", "name": "(FOR SHOPEE)*(FOR SHOP BANGKOK", "amount": -182.00},
      {"date": "2026-03-25", "name": "TMN 7-11 BANGKOK",               "amount": 132.00},
      ...
    ]
  }

Writes a JSON envelope:

  {
    "holder":     "nuta",
    "card":       "UOB One",
    "bill_cycle": "2026-04-24",

    "statement": { "count": 71, "subtotal": 17936.84, "subtotal_source": "given" | "computed" },
    "notion":    { "count": 73, "subtotal": 17434.72 },
    "subtotal_diff": -502.12,                     // notion - statement (negative = Notion smaller)

    "matched_count":      69,
    "name_mismatch_count": 1,                     // matched by amount only, names diverged

    "missing_in_notion": [ {date, name, amount}, ... ],
    "extra_in_notion":   [ {id, url, name, amount, transaction_date, note}, ... ],
    "name_mismatches":   [ {statement, notion}, ... ]
  }
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import notion_client
from lib.bill_cycle import most_recent_closed_cycle
from lib.cards import find_card
from lib.holders import resolve_holder
from lib.transaction_read import project_transaction

from matching import match


class AuditBillError(RuntimeError):
    pass


def _query_cycle(transactions_ds: str, card_page_id: str, bill_cycle: str) -> list[dict]:
    pages = notion_client.query_all(
        transactions_ds,
        filter={
            "and": [
                {"property": "Card", "relation": {"contains": card_page_id}},
                {"property": "Bill Cycle Date", "date": {"equals": bill_cycle}},
            ]
        },
    )
    return [project_transaction(p) for p in pages]


def _validate_statement_rows(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            raise AuditBillError(f"statement_transactions[{i}] is not an object")
        if "amount" not in r:
            raise AuditBillError(f"statement_transactions[{i}] missing `amount`")
        if "name" not in r:
            raise AuditBillError(f"statement_transactions[{i}] missing `name`")
        # Normalize to a small projection so output is uniform.
        out.append(
            {
                "date": r.get("date"),
                "name": str(r["name"]),
                "amount": round(float(r["amount"]), 2),
            }
        )
    return out


def _strip_notion_row(row: dict) -> dict:
    """Compact view for output — full row has more than is useful in findings."""
    return {
        "id": row.get("id"),
        "url": row.get("url"),
        "name": row.get("name"),
        "amount": row.get("amount"),
        "transaction_date": row.get("transaction_date"),
        "note": row.get("note") or None,
    }


def run(spec: dict) -> dict:
    if not isinstance(spec, dict):
        raise AuditBillError("spec must be a JSON object")
    for key in ("holder", "card", "statement_transactions"):
        if spec.get(key) is None:
            raise AuditBillError(f"missing required field: {key!r}")

    holder = resolve_holder(spec["holder"])
    card_name = spec["card"]
    card = find_card(holder.cards_ds, card_name)

    if (bc := spec.get("bill_cycle")):
        dt.date.fromisoformat(bc)  # validate
        bill_cycle = bc
    else:
        bc_date, _ = most_recent_closed_cycle(card_name, dt.date.today())
        bill_cycle = bc_date.isoformat()

    statement_rows = _validate_statement_rows(spec["statement_transactions"])
    notion_rows = _query_cycle(holder.transactions_ds, card["id"], bill_cycle)

    result = match(statement_rows, notion_rows)

    matched = result["matched"]
    name_mismatches = [m for m in matched if not m["name_match"]]

    statement_sum = round(sum(r["amount"] for r in statement_rows), 2)
    notion_sum = round(sum((r.get("amount") or 0) for r in notion_rows), 2)

    given_subtotal = spec.get("statement_subtotal")
    if given_subtotal is not None:
        statement_subtotal = round(float(given_subtotal), 2)
        subtotal_source = "given"
    else:
        statement_subtotal = statement_sum
        subtotal_source = "computed"

    out = {
        "holder": holder.key,
        "card": card_name,
        "bill_cycle": bill_cycle,
        "statement": {
            "count": len(statement_rows),
            "subtotal": statement_subtotal,
            "subtotal_source": subtotal_source,
            "rows_sum": statement_sum,
        },
        "notion": {
            "count": len(notion_rows),
            "subtotal": notion_sum,
        },
        "subtotal_diff": round(notion_sum - statement_subtotal, 2),
        "matched_count": len(matched),
        "name_mismatch_count": len(name_mismatches),
        "missing_in_notion": result["missing_in_notion"],
        "extra_in_notion": [_strip_notion_row(r) for r in result["extra_in_notion"]],
        "name_mismatches": [
            {
                "statement": m["statement"],
                "notion": _strip_notion_row(m["notion"]),
            }
            for m in name_mismatches
        ],
    }
    return out


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
