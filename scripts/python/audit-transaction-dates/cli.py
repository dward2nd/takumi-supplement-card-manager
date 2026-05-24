#!/usr/bin/env python3
"""audit-transaction-dates — flag transactions whose (BC, Due) don't match the card's pattern.

deterministic + idempotent — read-only.

Scans one holder's Transactions DB (optionally filtered to one card) and
reports every row whose `Bill Cycle Date` / `Due Date` pair doesn't fit
the card's issuer pattern (see docs/concepts/bill-cycle-patterns.md and
lib/bill_cycle.py).

Cards whose name doesn't match any known pattern prefix are skipped and
counted in `skipped_unknown_pattern` — the issuer needs to be documented
before they can be audited.

Reads a JSON spec from stdin (or --input <file>):

  {
    "holder": "takumi" | "baiboon" | "nuta",
    "card":   "First Choice"          // optional — if omitted, scan all cards
  }

Writes a JSON envelope:

  {
    "holder":                    "baiboon",
    "card":                      "First Choice" | null,
    "scanned":                   79,
    "issue_count":               5,
    "skipped_unknown_pattern":   0,
    "issues": [
      {
        "id":                       "<page-id>",
        "url":                      "<page-url>",
        "name":                     "<merchant>",
        "card_name":                "First Choice",
        "amount":                   235,
        "transaction_date":         "2026-04-20",
        "bill_cycle_date":          "2026-05-05",
        "due_date":                 "2026-05-05",
        "expected_bill_cycle_date": "2026-05-05",
        "expected_due_date":        "2026-05-25",
        "issue":                    "due_mismatch"
      },
      ...
    ]
  }
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import bill_cycle, notion_client
from lib.cards import find_card
from lib.holders import resolve_holder
from lib.transaction_audit import diagnose
from lib.transaction_read import project_transaction


def _card_name_map(cards_ds: str) -> dict[str, str]:
    """Build {card_page_id: card_title} for one holder's Cards DS."""
    pages = notion_client.query_all(cards_ds)
    out: dict[str, str] = {}
    for p in pages:
        title = ""
        for prop in p.get("properties", {}).values():
            if prop.get("type") == "title":
                title = "".join(t.get("plain_text", "") for t in prop.get("title", []))
                break
        out[p["id"]] = title.strip()
    return out


def _to_date(s: str | None) -> dt.date | None:
    return dt.date.fromisoformat(s) if s else None


def run(spec: dict) -> dict:
    holder = resolve_holder(spec["holder"])

    card_filter_id: str | None = None
    card_filter_title: str | None = None
    if (card_name := spec.get("card")):
        card = find_card(holder.cards_ds, card_name)
        card_filter_id = card["id"]
        card_filter_title = card_name

    card_names = _card_name_map(holder.cards_ds)

    filter_payload = (
        {"property": "Card", "relation": {"contains": card_filter_id}}
        if card_filter_id
        else None
    )
    pages = notion_client.query_all(
        holder.transactions_ds,
        **({"filter": filter_payload} if filter_payload else {}),
    )

    issues: list[dict] = []
    skipped = 0

    for page in pages:
        row = project_transaction(page)
        card_ids = row.get("card_ids") or []
        if not card_ids:
            # transaction with no Card relation — flag separately? for now, skip
            continue
        cname = card_names.get(card_ids[0], "")
        if not cname:
            continue
        try:
            bill_cycle.pattern_for_card(cname)
        except bill_cycle.PatternNotFoundError:
            skipped += 1
            continue

        issue = diagnose(
            cname,
            _to_date(row["transaction_date"]),
            _to_date(row["bill_cycle_date"]),
            _to_date(row["due_date"]),
        )
        if issue is None:
            continue

        issues.append(
            {
                "id": row["id"],
                "url": row["url"],
                "name": row["name"],
                "card_name": cname,
                "amount": row["amount"],
                "transaction_date": row["transaction_date"],
                "bill_cycle_date": row["bill_cycle_date"],
                "due_date": row["due_date"],
                "expected_bill_cycle_date": (
                    issue.expected_bc.isoformat() if issue.expected_bc else None
                ),
                "expected_due_date": (
                    issue.expected_due.isoformat() if issue.expected_due else None
                ),
                "issue": issue.kind,
            }
        )

    issues.sort(key=lambda r: (r["card_name"], r["transaction_date"] or "0000-00-00"))

    return {
        "holder": holder.key,
        "card": card_filter_title,
        "scanned": len(pages),
        "issue_count": len(issues),
        "skipped_unknown_pattern": skipped,
        "issues": issues,
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
