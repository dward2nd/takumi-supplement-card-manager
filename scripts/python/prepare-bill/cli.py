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
    "holder":     "baiboon" | "nuta",          // required (takumi has no Bills DB)
    "card":       "UOB One",                   // required, must match a SELECT option
    "bill_cycle": "2026-05-25"                 // optional ISO date; inferred if omitted
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
from lib.bills import require_bills_ds
from lib.cards import find_card
from lib.holders import resolve_holder

DRAFT_PREFIX = "[DRAFT] "

# Cards whose cashback policy is tier-credit-row based: the cycle must
# already contain explicit `*CASHBACK*` credit rows before the bill is
# drafted, otherwise the sum will overstate the balance. Keep this list
# narrow — only add a card when we've documented its credit-row workflow.
CASHBACK_CREDIT_CARDS: frozenset[str] = frozenset({"UOB One"})


class PrepareBillError(RuntimeError):
    pass


def _select_options(ds_id: str) -> list[str]:
    """SELECT options on a Bills DS's `Card` property (verbatim strings)."""
    client = notion_client.get_client()
    ds = client.data_sources.retrieve(data_source_id=ds_id)
    card_prop = ds.get("properties", {}).get("Card", {})
    if card_prop.get("type") != "select":
        raise PrepareBillError("Bills DS `Card` is not a SELECT — schema drift?")
    return [opt.get("name") for opt in card_prop.get("select", {}).get("options", [])]


def _existing_bill(ds_id: str, card: str, bill_cycle: str) -> dict | None:
    pages = notion_client.query_all(
        ds_id,
        filter={
            "and": [
                {"property": "Card", "select": {"equals": card}},
                {"property": "วันตัดรอบบิล", "date": {"equals": bill_cycle}},
            ]
        },
    )
    return pages[0] if pages else None


def _sum_cycle(transactions_ds: str, card_page_id: str, bill_cycle: str) -> tuple[float, int, list[dict]]:
    rows = notion_client.query_all(
        transactions_ds,
        filter={
            "and": [
                {"property": "Card", "relation": {"contains": card_page_id}},
                {"property": "Bill Cycle Date", "date": {"equals": bill_cycle}},
            ]
        },
    )
    total = 0.0
    for r in rows:
        amt = (r.get("properties", {}).get("ยอดชำระ") or {}).get("number")
        if amt is not None:
            total += amt
    return round(total, 2), len(rows), rows


def _has_cashback_credit_rows(rows: list[dict]) -> bool:
    """Heuristic: at least one row whose `Name` mentions CASHBACK."""
    for r in rows:
        props = r.get("properties", {})
        title = props.get("Name") or {}
        text = "".join(t.get("plain_text", "") for t in title.get("title", []) or [])
        if "CASHBACK" in text.upper():
            return True
    return False


def run(spec: dict, *, dry_run: bool = False) -> dict:
    if not isinstance(spec, dict):
        raise PrepareBillError("spec must be a JSON object")
    for key in ("holder", "card"):
        if not spec.get(key):
            raise PrepareBillError(f"missing required field: {key!r}")

    holder = resolve_holder(spec["holder"])
    bills_ds = require_bills_ds(holder)
    card_name = spec["card"]

    options = _select_options(bills_ds)
    if card_name not in options:
        raise PrepareBillError(
            f"card {card_name!r} is not a SELECT option on {holder.key}'s "
            f"Bills `Card` field. Options: {sorted(options)}"
        )
    card = find_card(holder.cards_ds, card_name)

    if (bc := spec.get("bill_cycle")):
        # Validate ISO format eagerly so we fail loud.
        _dt.date.fromisoformat(bc)
        bill_cycle = bc
    else:
        bc_date, _ = active_cycle(card_name, _dt.date.today())
        bill_cycle = bc_date.isoformat()

    existing = _existing_bill(bills_ds, card_name, bill_cycle)
    if existing is not None:
        raise PrepareBillError(
            f"a bill row already exists for {holder.key}/{card_name} cycle "
            f"{bill_cycle} (id={existing['id']}). Refusing to create a duplicate."
        )

    total, tx_count, rows = _sum_cycle(holder.transactions_ds, card["id"], bill_cycle)
    if tx_count == 0:
        raise PrepareBillError(
            f"no transactions found for {holder.key}/{card_name} cycle {bill_cycle} "
            f"— nothing to bill. Did you mean a different cycle date?"
        )

    if card_name in CASHBACK_CREDIT_CARDS and not spec.get("skip_cashback_check"):
        if not _has_cashback_credit_rows(rows):
            raise PrepareBillError(
                f"{card_name} requires cashback credit rows before drafting the bill — "
                f"the cycle has no `*CASHBACK*` transactions, so the sum would overstate "
                f"the balance owed. Run /post-cashback-credits first (or pass "
                f'`"skip_cashback_check": true` in the spec to override).'
            )

    bc_date = _dt.date.fromisoformat(bill_cycle)
    title = f"{DRAFT_PREFIX}{card_name} {bc_date.strftime('%Y-%m')}"

    properties = {
        "title": {"title": [{"text": {"content": title}}]},
        "Card": {"select": {"name": card_name}},
        "วันตัดรอบบิล": {"date": {"start": bill_cycle}},
        "ยอดชำระ": {"number": total},
        "จ่ายแล้ว": {"checkbox": False},
    }

    if dry_run:
        return {
            "dry_run": True,
            "holder": holder.key,
            "card": card_name,
            "bill_cycle": bill_cycle,
            "title": title,
            "ยอดชำระ": total,
            "tx_count": tx_count,
        }

    page = notion_client.create_page(bills_ds, properties)
    return {
        "id": page["id"],
        "url": page.get("url"),
        "holder": holder.key,
        "card": card_name,
        "bill_cycle": bill_cycle,
        "title": title,
        "ยอดชำระ": total,
        "tx_count": tx_count,
    }


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
