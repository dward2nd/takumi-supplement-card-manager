#!/usr/bin/env python3
"""post-cashback-credits — write UOB One cashback credit rows for a cycle.

deterministic + idempotent — re-running with the same (holder, cycle)
refuses to overwrite: if any `*CASHBACK*` row already exists for the
cycle on the card, the script aborts so a second run doesn't
double-credit. Use the `--force` flag (or `force: true` in the spec)
to override after manually archiving the prior rows.

What it does:

1. Reads every transaction in the cycle on the named card.
2. Groups by `% cb` (raw fraction). Ignores rows where `% cb` is
   unset, and ignores rows whose `Name` already contains CASHBACK
   (so the skill can be re-run after a partial failure without
   double-counting the credit rows it wrote previously — those still
   trigger the abort guard above, but at least the math is safe).
3. For each tier with a positive eligible-sum, computes
   `credit = round(rate * sum, 2)` and writes a new transaction:
   - `Name`: `UOB ONE CASHBACK <rate-as-percent>%`
   - `ยอดชำระ`: `-credit` (negative; reduces the bill)
   - `Bill Cycle Date` / `Due Date`: the cycle's BC + DD (aligned per
     the explicit exception — see add-transaction Rule 4d in skill).
   - `Transaction Datetime`:
     * `1%` tier   → the BC date itself
     * other tiers → first weekday of the month *after* the BC date
   - `multiplier`: `×0` (UOB One never earns points).
   - `Note`: human-readable math (e.g. `Cycle 2026-05-25 cashback
     credit: 5% × 2048.00 = 102.40`).

The rate-to-date map is the UOB One convention the user established
on 2026-05-25 (1% credited at cycle close, higher tiers credited at
the start of the following month).

Reads a JSON spec from stdin (or --input <file>):

  {
    "holder":     "baiboon" | "nuta",       // required (Takumi has no UOB One workflow here)
    "card":       "UOB One",                // required; today only UOB One is supported
    "bill_cycle": "2026-05-25",             // optional ISO; inferred via active_cycle if omitted
    "force":      false                     // optional; override the duplicate-CASHBACK guard
  }

Writes a JSON envelope to stdout:

  {
    "holder":     "baiboon",
    "card":       "UOB One",
    "bill_cycle": "2026-05-25",
    "due_date":   "2026-06-15",
    "tier_totals": {"0.01": 6061.40, "0.05": 2048.00, "0.10": 0.0},
    "created":    [ { "rate": 0.01, "amount": -60.61, "date": "2026-05-25", "id": "..." }, ... ]
  }

Tiers with a sum ≤ 0 are skipped (no zero-baht placeholder rows). The
"created" list reflects what was actually written.

--dry-run resolves the totals + intended rows without writing.
"""

from __future__ import annotations

import argparse
import calendar
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import notion_client, promotions
from lib.bill_cycle import active_cycle, pattern_for_card, cycle_for_month
from lib.cards import find_card
from lib.holders import resolve_holder
from lib.transaction_write import build_transaction_properties


# Cards we know how to write cashback credit rows for: any card whose
# active promotion declares a `crediting_schedule` block. The schedule
# itself drives per-tier date placement (see _classify_tier_date), so
# adding a new card is purely a YAML edit in scripts/repositories/.
def _supported_promotions() -> dict[str, promotions.Promotion]:
    """Return {card_name: promotion} for promos that declare a crediting_schedule."""
    return {p.card: p for p in promotions.load_all() if p.crediting_schedule}


class PostCashbackError(RuntimeError):
    pass


def _first_weekday_of_next_month(bc: _dt.date) -> _dt.date:
    y, m = bc.year, bc.month
    if m == 12:
        y, m = y + 1, 1
    else:
        m += 1
    first = _dt.date(y, m, 1)
    while first.weekday() >= 5:  # 5=Sat, 6=Sun (no holiday shift — convention)
        first += _dt.timedelta(days=1)
    return first


def _classify_tier_date(rate: float, bc: _dt.date, schedule: dict[str, str]) -> _dt.date:
    """Resolve the credit-row date for a tier rate from the promo's crediting_schedule.

    Schedule keys are rate-as-strings (e.g. "0.01"); values are:
      - `bc_date` — the bill-cycle date itself
      - `first_weekday_next_month` — first Mon-Fri of the following calendar month
    Unrecognised values fall back to first_weekday_next_month with a warning
    only at the dictionary level (we don't surface to stdout — caller's job).
    """
    key = f"{rate:.4f}".rstrip("0").rstrip(".")  # "0.01" / "0.05" / "0.1"
    # Schedule may store either "0.1" or "0.10"; try both forms.
    convention = schedule.get(key) or schedule.get(f"{rate:.2f}")
    if convention == "bc_date":
        return bc
    return _first_weekday_of_next_month(bc)


def _due_date_for(card_name: str, bc: _dt.date) -> _dt.date:
    pattern = pattern_for_card(card_name)
    _, dd = cycle_for_month(pattern, bc.year, bc.month)
    return dd


def _fetch_cycle_rows(transactions_ds: str, card_page_id: str, bill_cycle: str) -> list[dict]:
    return notion_client.query_all(
        transactions_ds,
        filter={
            "and": [
                {"property": "Card", "relation": {"contains": card_page_id}},
                {"property": "Bill Cycle Date", "date": {"equals": bill_cycle}},
            ]
        },
    )


def _row_title(page: dict) -> str:
    title = page.get("properties", {}).get("Name") or {}
    return "".join(t.get("plain_text", "") for t in title.get("title", []) or [])


def _existing_cashback_rows(rows: list[dict]) -> list[str]:
    """Return titles of existing rows whose Name contains CASHBACK (case-insensitive)."""
    out = []
    for r in rows:
        title = _row_title(r)
        if "CASHBACK" in title.upper():
            out.append(title)
    return out


def _tier_totals(rows: list[dict], skip_cashback_names: bool = True) -> dict[float, float]:
    totals: dict[float, float] = {}
    for r in rows:
        if skip_cashback_names and "CASHBACK" in _row_title(r).upper():
            continue
        props = r.get("properties", {})
        rate = (props.get("% cb") or {}).get("number")
        amt = (props.get("ยอดชำระ") or {}).get("number")
        if rate is None or amt is None:
            continue
        # Round the rate to 4 decimal places so 0.0099999... and 0.01
        # bucket together — Notion may serialize % cb with FP noise.
        key = round(float(rate), 4)
        totals[key] = totals.get(key, 0.0) + float(amt)
    return totals


def run(spec: dict, *, dry_run: bool = False) -> dict:
    if not isinstance(spec, dict):
        raise PostCashbackError("spec must be a JSON object")
    for key in ("holder", "card"):
        if not spec.get(key):
            raise PostCashbackError(f"missing required field: {key!r}")

    card_name = spec["card"]
    supported = _supported_promotions()
    if card_name not in supported:
        known = sorted(supported)
        raise PostCashbackError(
            f"card {card_name!r} has no active promotion with a `crediting_schedule` "
            f"in scripts/repositories/promotions/. Supported cards (derived from "
            f"the repo): {known}. Add a crediting_schedule to the card's active "
            f"promotion YAML to enable this skill for it."
        )
    promo = supported[card_name]

    holder = resolve_holder(spec["holder"])
    card = find_card(holder.cards_ds, card_name)

    if (bc_str := spec.get("bill_cycle")):
        bc = _dt.date.fromisoformat(bc_str)
    else:
        bc, _ = active_cycle(card_name, _dt.date.today())
    dd = _due_date_for(card_name, bc)
    bill_cycle = bc.isoformat()
    due_date = dd.isoformat()

    rows = _fetch_cycle_rows(holder.transactions_ds, card["id"], bill_cycle)
    if not rows:
        raise PostCashbackError(
            f"no transactions in cycle {bill_cycle} for {holder.key}/{card_name}; "
            f"nothing to compute cashback against."
        )

    existing = _existing_cashback_rows(rows)
    if existing and not spec.get("force"):
        raise PostCashbackError(
            f"{holder.key}/{card_name} cycle {bill_cycle} already has CASHBACK rows: "
            f"{existing}. Pass `force: true` (or --force) to write anyway, but archive "
            f"the prior rows first via add-transaction/archive.py to avoid double-counting."
        )

    totals = _tier_totals(rows, skip_cashback_names=True)

    plan: list[dict] = []
    for rate, total in sorted(totals.items()):
        if total <= 0:
            continue
        credit = round(rate * total, 2)
        if credit <= 0:
            continue
        rate_pct = int(round(rate * 100))
        # Credit-row title format keys off the card's name + rate.
        # Verbatim, statement-style: e.g. "UOB ONE CASHBACK 5%".
        cb_name = f"{card_name.upper()} CASHBACK {rate_pct}%"
        plan.append(
            {
                "rate": rate,
                "tier_sum": round(total, 2),
                "amount": -credit,
                "date": _classify_tier_date(rate, bc, promo.crediting_schedule).isoformat(),
                "name": cb_name,
                "note": (
                    f"Cycle {bill_cycle} cashback credit: "
                    f"{rate_pct}% × {round(total, 2):.2f} = {credit:.2f}."
                ),
            }
        )

    if dry_run:
        return {
            "dry_run": True,
            "holder": holder.key,
            "card": card_name,
            "bill_cycle": bill_cycle,
            "due_date": due_date,
            "tier_totals": {str(k): round(v, 2) for k, v in sorted(totals.items())},
            "plan": plan,
        }

    multiplier = promo.points_default  # may be None for cards that earn points normally
    created: list[dict] = []
    for row in plan:
        props = build_transaction_properties(
            name=row["name"],
            amount=row["amount"],
            transaction_date=row["date"],
            bill_cycle_date=bill_cycle,
            due_date=due_date,
            card_page_id=card["id"],
            processed=True,
            note=row["note"],
            multiplier=multiplier,
        )
        page = notion_client.create_page(holder.transactions_ds, props)
        created.append({
            "rate": row["rate"],
            "amount": row["amount"],
            "date": row["date"],
            "name": row["name"],
            "id": page["id"],
            "url": page.get("url"),
        })

    return {
        "holder": holder.key,
        "card": card_name,
        "bill_cycle": bill_cycle,
        "due_date": due_date,
        "tier_totals": {str(k): round(v, 2) for k, v in sorted(totals.items())},
        "created": created,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Compute the plan without writing")
    ap.add_argument("--force", action="store_true", help="Override the duplicate-CASHBACK guard")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)
    if args.force:
        spec["force"] = True

    out = run(spec, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
