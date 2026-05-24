"""Project a Notion transaction page into a flat dict.

deterministic + idempotent — safe to re-run.

This file contains the *read* side of the Transactions schema. Keys
returned here are English so downstream JSON consumers stay portable;
Thai field names from Notion (e.g. `ยอดชำระ`) are kept verbatim in the
property lookups per project convention.

Pairs with `lib.transaction_write` (write side). They are split so a
reviewer can examine one side without scrolling past the other.
"""

from __future__ import annotations

from typing import Any


def _title(props: dict, name: str = "Name") -> str:
    return "".join(t.get("plain_text", "") for t in props.get(name, {}).get("title", []) or [])


def _rich_text(props: dict, name: str) -> str:
    return "".join(t.get("plain_text", "") for t in props.get(name, {}).get("rich_text", []) or [])


def _number(props: dict, name: str) -> float | None:
    return props.get(name, {}).get("number")


def _date(props: dict, name: str) -> str | None:
    d = props.get(name, {}).get("date") or {}
    return d.get("start")


def _checkbox(props: dict, name: str) -> bool:
    return bool(props.get(name, {}).get("checkbox"))


def _relation_ids(props: dict, name: str) -> list[str]:
    return [r.get("id") for r in props.get(name, {}).get("relation", []) or []]


def _formula_number(props: dict, name: str) -> float | None:
    f = props.get(name, {}).get("formula") or {}
    return f.get("number") if f.get("type") == "number" else None


def project_transaction(page: dict) -> dict[str, Any]:
    """Flatten a Notion transaction page into a small JSON-friendly dict.

    `cashback_percent` and `cashback` only exist on Nuta's DS; for Baiboon
    and Takumi those keys come back as None (property absent from the page).
    """
    props = page.get("properties", {})
    return {
        "id": page.get("id"),
        "url": page.get("url"),
        "name": _title(props, "Name"),
        "amount": _number(props, "ยอดชำระ"),
        "transaction_date": _date(props, "Transaction Datetime"),
        "process_date": _date(props, "Process Date"),
        "bill_cycle_date": _date(props, "Bill Cycle Date"),
        "due_date": _date(props, "Due Date"),
        "processed": _checkbox(props, "Processed"),
        "paid": _checkbox(props, "ชำระแล้ว"),
        "credit_return": _checkbox(props, "Credit Return"),
        "note": _rich_text(props, "Note"),
        "card_ids": _relation_ids(props, "Card"),
        "cashback_percent": _number(props, "% cb"),
        "cashback": _formula_number(props, "cashback"),
    }
