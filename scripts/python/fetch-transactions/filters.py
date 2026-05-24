"""Filter & sort spec → Notion native filter+sort payload.

deterministic + idempotent — safe to re-run.

Mirrors the JSON spec documented in cli.py. Translating it into a
Notion query in one place keeps cli.py free of API-shape details.
"""

from __future__ import annotations

from typing import Any


SORT_MAP: dict[str, list[dict]] = {
    "date_desc": [{"property": "Transaction Datetime", "direction": "descending"}],
    "date_asc": [{"property": "Transaction Datetime", "direction": "ascending"}],
    "amount_desc": [{"property": "ยอดชำระ", "direction": "descending"}],
    "amount_asc": [{"property": "ยอดชำระ", "direction": "ascending"}],
    "bill_cycle_desc": [{"property": "Bill Cycle Date", "direction": "descending"}],
    "bill_cycle_asc": [{"property": "Bill Cycle Date", "direction": "ascending"}],
}

_CHECKBOX_FLAGS = [
    ("processed", "Processed"),
    ("paid", "ชำระแล้ว"),
    ("credit_return", "Credit Return"),
]


def build_filter(spec: dict[str, Any], card_page_id: str | None) -> dict | None:
    clauses: list[dict] = []

    if card_page_id:
        clauses.append({"property": "Card", "relation": {"contains": card_page_id}})

    if (d := spec.get("bill_cycle")):
        clauses.append({"property": "Bill Cycle Date", "date": {"equals": d}})

    if (rng := spec.get("bill_cycle_range")):
        a, b = rng
        clauses.append({"property": "Bill Cycle Date", "date": {"on_or_after": a}})
        clauses.append({"property": "Bill Cycle Date", "date": {"on_or_before": b}})

    if (rng := spec.get("transaction_date_range")):
        a, b = rng
        clauses.append({"property": "Transaction Datetime", "date": {"on_or_after": a}})
        clauses.append({"property": "Transaction Datetime", "date": {"on_or_before": b}})

    if (v := spec.get("min_amount")) is not None:
        clauses.append({"property": "ยอดชำระ", "number": {"greater_than_or_equal_to": v}})
    if (v := spec.get("max_amount")) is not None:
        clauses.append({"property": "ยอดชำระ", "number": {"less_than_or_equal_to": v}})

    for flag, prop in _CHECKBOX_FLAGS:
        if flag in spec:
            clauses.append({"property": prop, "checkbox": {"equals": bool(spec[flag])}})

    if (q := spec.get("note_contains")):
        clauses.append({"property": "Note", "rich_text": {"contains": q}})

    if (q := spec.get("name_contains")):
        clauses.append({"property": "Name", "title": {"contains": q}})

    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"and": clauses}


def resolve_sort(spec: dict[str, Any]) -> list[dict]:
    key = spec.get("sort", "date_desc")
    if key not in SORT_MAP:
        raise ValueError(
            f"unknown sort {key!r}; supported: {sorted(SORT_MAP)}"
        )
    return SORT_MAP[key]
