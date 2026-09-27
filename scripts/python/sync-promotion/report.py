"""Shape the sync-promotion envelope: flagged rows, the boundary group, drift.

deterministic + idempotent — pure formatting of already-computed values.
"""

from __future__ import annotations

from decimal import Decimal

from lib.bureau import ELIGIBLE, Allocation, BasePromotion, Tx


def line(tx: Tx) -> str:
    return f"{tx.holder} {tx.date[:10]} ฿{tx.amount:,.2f} {tx.name}"


def flagged(promo: BasePromotion, txs: list[Tx]) -> tuple[list[dict], Decimal]:
    """Linked rows the bank's terms would likely drop, grouped by reason."""
    groups: dict[str, dict] = {}
    for tx in txs:
        level, reason = promo.screen(tx)
        if level == ELIGIBLE:
            continue
        g = groups.setdefault(reason, {"level": level, "reason": reason, "count": 0,
                                       "amount": Decimal(0), "rows": []})
        g["count"] += 1
        g["amount"] += tx.amount
        g["rows"].append(line(tx))
    out = sorted(groups.values(), key=lambda g: -g["amount"])
    return [{**g, "amount": float(g["amount"])} for g in out], sum((g["amount"] for g in out), Decimal(0))


def boundary(alloc: Allocation) -> list[dict]:
    """The same-date group the last paying step ends in, and how it was split."""
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
    return {
        "bank_spend": float(bank_spend),
        "linked_spend": float(alloc.pooled),
        "delta": float(delta),
        "bank_cashback": float(promo.cashback(bank_spend)),
        "dates_matching_delta": [d for d, s in sorted(by_date.items()) if delta and s == abs(delta)],
        "repeats": repeats,
        "by_date": {d: float(s) for d, s in sorted(by_date.items())},
    }
