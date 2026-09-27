#!/usr/bin/env python3
"""sync-promotion — bring one Promotion Bureau row up to date.

deterministic + idempotent — every write sets a value to what the linked
transactions imply, and creates a tracker row only when none exists; a second
run with nothing changed writes nothing.

For one Bureau row (e.g. `2026M9 — NW3 cb 2%`), with the campaign class
from `lib.bureau` that matches it:

1. Reads every holder's linked transactions, screens each against the
   campaign's exclusions, and lists the card's unlinked rows in the period
   as candidates (links the eligible ones with `link_candidates`).
2. Splits the credit first come, first served (see BasePromotion.allocate).
3. Writes `เงินคืนรวม` when empty, and `เงินคืนส่วน<name>` per holder —
   unless `เงินคืนรวม` already holds a different figure, which is reported.
4. Upserts each holder's tracker row (`<CODE> 2% 1—30 Sep`) linked to the
   Bureau row with `Expected Cashback` = the share; a ticked (settled) row
   is left alone.
5. Writes the campaign summary into the Bureau page body when it's empty
   (or always, with `replace_summary`).

Spec (stdin or --input):
  {
    "promotion":       "2026M9 — NW3 cb 2%",  // Bureau row Name, page ID or URL
    "bank_spend":      36803.92,              // optional: the bank app's pooled figure
    "link_candidates": false,                 // optional: link eligible unlinked rows
    "replace_summary": false                  // optional: rewrite a non-empty page body
  }

--dry-run computes and reports everything without writing.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib import cards  # noqa: E402
from lib.bureau import ELIGIBLE, promotion_for, store  # noqa: E402
from lib.holders import HOLDERS  # noqa: E402

import report  # noqa: E402


def run(spec: dict, *, dry_run: bool = False) -> dict:
    row = store.find_row(spec["promotion"])
    promo = promotion_for(row.name, row.start, row.end)
    writes: list[str] = []
    warnings: list[str] = []

    def write(what: str, fn, *args, **kwargs) -> None:
        writes.append(what)
        if not dry_run:
            fn(*args, **kwargs)

    # 1. linked rows, and candidates on the card that aren't linked yet
    txs, candidates = [], []
    card_ids = {h.key: cards.find_card(h.cards_ds, promo.card)["id"] for h in HOLDERS.values()}
    for h in HOLDERS.values():
        linked = store.linked_txs(row, h)
        txs += linked
        total = sum((t.amount for t in linked), Decimal(0))
        if total != row.rollups[h.key]:
            warnings.append(f"{store.rollup_prop(h)} shows ฿{row.rollups[h.key]:,.2f} but the linked "
                            f"rows sum to ฿{total:,.2f}")
        for tx, existing in store.unlinked_txs(row, h, card_ids[h.key]):
            level, reason = promo.screen(tx)
            if level == ELIGIBLE and spec.get("link_candidates"):
                write(f"link {report.line(tx)}", store.link_tx, tx.id, existing, row.id)
                txs.append(tx)
            elif tx.is_card_purchase:
                candidates.append({"row": report.line(tx), "level": level, "reason": reason})

    # 2. the split
    alloc = promo.allocate(txs)
    flagged, flagged_amount = report.flagged(promo, txs)
    shares = {h.key: alloc.shares.get(h.key, Decimal(0)) for h in HOLDERS.values()}
    warnings += alloc.warnings

    # 3. Bureau numbers
    if row.total is not None and row.total != alloc.credit:
        warnings.append(f"{store.TOTAL} holds ฿{row.total:,.2f} but the ladder pays ฿{alloc.credit:,.2f} on "
                        f"the linked ฿{alloc.pooled:,.2f} — shares and trackers not written. Fix the links, "
                        f"or clear {store.TOTAL} to let the ladder figure stand.")
        shares_ok = False
    else:
        shares_ok = True
        numbers = {} if row.total is not None else {store.TOTAL: alloc.credit}
        numbers |= {store.share_prop(h): shares[h.key] for h in HOLDERS.values()
                    if row.shares[h.key] != shares[h.key]}
        if numbers:
            write(f"Bureau {', '.join(f'{k}={v}' for k, v in numbers.items())}",
                  store.write_numbers, row.id, numbers)

    # 4. trackers
    title = promo.tracker_title(row.start, row.end)
    trackers = {}
    for h in HOLDERS.values():
        share = shares[h.key]
        found = store.trackers(h, row, title)
        trackers[h.key] = [t.name for t in found]
        if not shares_ok:
            continue
        if not found:
            if share > 0:
                write(f"create {h.key} tracker {title!r} expecting ฿{share}", store.create_tracker, h,
                      title=title, date=row.start, card_id=card_ids[h.key], row_id=row.id, expected=share)
        elif len(found) > 1 or not found[0].linked:
            warnings.append(f"{h.key}: tracker rows {[t.name for t in found]} need a look — more than "
                            f"one, or titled {title!r} without a Promotion link; left alone")
        elif found[0].settled:
            if found[0].expected != share:
                warnings.append(f"{h.key}: {found[0].name!r} is ticked as credited at "
                                f"฿{found[0].expected} but the split now gives ฿{share}; left alone")
        elif found[0].expected != share:
            write(f"{h.key} tracker Expected Cashback {found[0].expected} → {share}",
                  store.set_expected, found[0].id, share)

    # 5. page summary
    body = store.body_block_ids(row.id)
    if not body or spec.get("replace_summary"):
        write(f"{'replace' if body else 'write'} page summary", store.write_body, row.id,
              promo.summary_blocks(), replace=bool(body))

    out = {
        "promotion": {"name": row.name, "url": row.url, "class": type(promo).__name__,
                      "period": [row.start.isoformat(), row.end.isoformat()]},
        "spend": {h.key: float(sum((t.amount for t in txs if t.holder == h.key), Decimal(0)))
                  for h in HOLDERS.values()} | {"pooled": float(alloc.pooled)},
        "cashback": {"ladder": float(alloc.credit), "entered": None if row.total is None else float(row.total),
                     "counted_spend": float(alloc.counted),
                     "if_flagged_rejected": float(promo.cashback(alloc.pooled - flagged_amount))},
        "shares": {k: float(v) for k, v in shares.items()},
        "boundary": report.boundary(alloc),
        "flagged": flagged,
        "unlinked_candidates": candidates,
        "trackers": trackers,
        "writes": writes,
        "warnings": warnings,
        "dry_run": dry_run,
    }
    if spec.get("bank_spend") is not None:
        out["drift"] = report.drift(promo, alloc, txs, Decimal(str(spec["bank_spend"])))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text() if args.input else sys.stdin.read())
    print(json.dumps(run(spec, dry_run=args.dry_run), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
