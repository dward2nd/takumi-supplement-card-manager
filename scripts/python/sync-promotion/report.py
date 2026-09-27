"""Shape the sync-promotion envelope: flagged rows, row-field mismatches, the boundary, drift.

deterministic + idempotent — pure formatting of already-computed values.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from lib.bureau import ELIGIBLE, Allocation, BasePromotion, LadderPromotion, Tx


def line(tx: Tx) -> str:
    return f"{tx.holder} {tx.date[:10]} ฿{tx.amount:,.2f} {tx.name}"


def flagged(promo: BasePromotion, txs: list[Tx]) -> tuple[list[dict], set[str]]:
    """Linked rows the campaign's terms would likely drop, grouped by reason, and their ids."""
    groups: dict[str, dict] = {}
    ids: set[str] = set()
    for tx in txs:
        level, reason = promo.screen(tx)
        if level == ELIGIBLE:
            continue
        ids.add(tx.id)
        g = groups.setdefault(reason, {"level": level, "reason": reason, "count": 0,
                                       "amount": Decimal(0), "rows": []})
        g["count"] += 1
        g["amount"] += tx.amount
        g["rows"].append(line(tx))
    out = sorted(groups.values(), key=lambda g: -g["amount"])
    return [{**g, "amount": float(g["amount"])} for g in out], ids


# How each /update-transaction key reads back off a row, and when two values agree.
_READ = {"cashback_percent": lambda t: t.cb, "multiplier": lambda t: t.multiplier,
         "points_redeemed": lambda t: t.points_used}


def _same(key: str, have: Any, want: Any) -> bool:
    if key == "points_redeemed":
        return Decimal(have or 0) == Decimal(want or 0)
    if key == "cashback_percent" and have is not None and want is not None:
        return Decimal(have) == Decimal(want)
    return have == want


def _plain(v: Any) -> Any:
    return float(v) if isinstance(v, Decimal) else v


def field_mismatches(promo: BasePromotion, alloc: Allocation) -> list[dict]:
    """Linked rows whose fields disagree with the split (`BasePromotion.expected`),
    each with a ready /update-transaction entry. A multiplier change goes through
    the `properties` escape hatch so the old box is unticked in the same write."""
    out = []
    for r in alloc.rows:
        diff = {k: v for k, v in promo.expected(r).items() if not _same(k, _READ[k](r.tx), v)}
        if not diff:
            continue
        update: dict[str, Any] = {"id": r.tx.id}
        for key, want in diff.items():
            if key == "multiplier":
                props = {r.tx.multiplier: {"checkbox": False}} if r.tx.multiplier else {}
                if want:
                    props[want] = {"checkbox": True}
                update["properties"] = props
            else:
                update[key] = _plain(want)
        if (note := promo.suggested_note(r)) and not r.tx.note:
            update["note"] = note
        out.append({"row": line(r.tx), "has": {k: _plain(_READ[k](r.tx)) for k in diff},
                    "want": {k: _plain(v) for k, v in diff.items()}, "update": update})
    return out


def boundary(alloc: Allocation) -> list[dict]:
    """The same-time group the quota ends in, and how it was split."""
    return [{"row": line(r.tx), "counted": float(round(r.counted, 2)), "credit": float(round(r.credit, 4))}
            for r in alloc.boundary]


def drift(promo: BasePromotion, alloc: Allocation, txs: list[Tx], bank_spend: Decimal) -> dict:
    """Linked total vs the bank app's figure, laid out to find the gap by eye.

    `by_date` is meant to be read against the app's list. `dates_matching_delta`
    is the whole-day version of "one thing is missing". `repeats` are rows that
    appear twice: the same holder twice, or two holders without a `[บัตรหลัก]`
    split between them. A single row equal to the gap is no lead: every even
    half of a split charge is one.
    """
    delta = alloc.pooled - bank_spend
    by_date: dict[str, Decimal] = {}
    groups: dict[tuple, list[Tx]] = {}
    for t in txs:
        by_date[t.date[:10]] = by_date.get(t.date[:10], Decimal(0)) + t.amount
        groups.setdefault((t.date, t.merchant, t.amount), []).append(t)
    repeats = [
        [line(t) for t in g] for g in groups.values()
        if len(g) > 1 and not any(t.name.startswith("[บัตรหลัก]") for t in g)
    ]
    out = {
        "bank_spend": float(bank_spend),
        "linked_spend": float(alloc.pooled),
        "delta": float(delta),
        "dates_matching_delta": [d for d, s in sorted(by_date.items()) if delta and s == abs(delta)],
        "repeats": repeats,
        "by_date": {d: float(s) for d, s in sorted(by_date.items())},
    }
    if isinstance(promo, LadderPromotion):
        out["bank_cashback"] = float(promo.cashback(bank_spend))
    return out
