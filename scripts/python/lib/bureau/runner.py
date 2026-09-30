"""Sync one Promotion Bureau row: link, split, settle, check, summarise.

deterministic + idempotent — every write sets a value to what the linked
transactions imply, and creates a Bureau or tracker row only when none exists;
a second run with nothing changed writes nothing.

The core of /sync-promotion, here so the ledger writers (/add-transaction,
/update-transaction, /record-statement) can re-sync the rows they touch
through `follow` without shelling out to another skill.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal

from ..holders import HOLDERS
from . import report, settle, store, sync
from . import promotion_for
from .base import CASHBACK, RIGHTS
from .store import BureauRow
from .sync import Writer


def _row(spec: dict, write: Writer) -> BureauRow:
    """The named Bureau row; with start/end, created when missing (a stand-in on a dry run)."""
    if not (spec.get("start") and spec.get("end")):
        return store.find_row(spec["promotion"])
    start, end = dt.date.fromisoformat(spec["start"]), dt.date.fromisoformat(spec["end"])
    promo = promotion_for(spec["promotion"], start, end)  # refuse a row no campaign class would match
    return sync.ensure_row(spec["promotion"], start, end, write, icon=promo.icon)


def run(spec: dict, *, dry_run: bool = False) -> dict:
    """The /sync-promotion envelope for one Bureau row (spec: see sync-promotion/cli.py)."""
    write = Writer(dry_run)
    row = _row(spec, write)
    promo = promotion_for(row.name, row.start, row.end)

    cards = sync.campaign_cards(promo)
    txs, candidates, adjustments, warnings = sync.collect(
        row, promo, cards, link=bool(spec.get("link_candidates")), write=write)
    alloc = promo.allocate(txs)
    warnings += alloc.warnings
    flagged, flagged_ids = report.flagged(promo, txs)
    mismatched = report.field_mismatches(promo, alloc)
    if mismatched:
        warnings.append(f"{len(mismatched)} linked row(s) carry fields the split disagrees with — see "
                        f"field_mismatches; fix with /update-transaction")

    totals = {"pooled": float(alloc.pooled), "counted": float(alloc.counted)}
    trackers: dict[str, list[str]] = {}
    held_back = False
    if promo.reward == CASHBACK:
        without_flagged = promo.allocate([t for t in txs if t.id not in flagged_ids])
        totals |= {"credit": float(alloc.credit),
                   "entered": None if row.total is None else float(row.total),
                   "if_flagged_rejected": float(without_flagged.credit)}
        shares_ok, w = settle.bureau_numbers(row, alloc, write)
        warnings += w
        held_back = not shares_ok
        if shares_ok:
            trackers, w = settle.trackers(row, promo, alloc, txs, adjustments, cards, write)
            warnings += w

    if promo.reward == RIGHTS:
        rights = sum(alloc.rights.values())
        totals |= {"rights": rights, "rights_by_holder": dict(alloc.rights)}
        if row.rights != rights:
            write(f"Bureau {store.RIGHTS}={rights}", store.write_numbers, row.id, {store.RIGHTS: Decimal(rights)})

    body = [] if sync.is_stand_in(row) else store.body_block_ids(row.id)
    if not body or spec.get("replace_summary"):
        write(f"{'replace' if body else 'write'} page summary", store.write_body, row.id,
              promo.summary_blocks(), replace=bool(body))

    out = {
        "promotion": {"name": row.name, "url": row.url, "class": type(promo).__name__,
                      "reward": promo.reward, "period": [row.start.isoformat(), row.end.isoformat()]},
        "spend": {h.key: float(sum((t.amount for t in txs if t.holder == h.key), Decimal(0)))
                  for h in HOLDERS.values()},
        "totals": totals,
        "shares": {k: float(v) for k, v in alloc.shares.items()},
        "held_back": held_back,
        "boundary": report.boundary(alloc),
        "field_mismatches": mismatched,
        "flagged": flagged,
        "unlinked_candidates": candidates,
        "trackers": trackers,
        "writes": write.done,
        "warnings": warnings,
        "dry_run": dry_run,
    }
    if spec.get("bank_spend") is not None:
        out["drift"] = report.drift(promo, alloc, txs, Decimal(str(spec["bank_spend"])))
    return out
