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
    """Linked total vs the bank app's figure, with the single rows that would explain it."""
    delta = alloc.pooled - bank_spend
    return {
        "bank_spend": float(bank_spend),
        "linked_spend": float(alloc.pooled),
        "delta": float(delta),
        "bank_cashback": float(promo.cashback(bank_spend)),
        "rows_matching_delta": [line(t) for t in txs if delta and t.amount == abs(delta)],
    }
