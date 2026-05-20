"""Input-spec validation for add-notion-transaction.

deterministic + idempotent — safe to re-run.

Surfaces obvious mistakes (missing keys, empty merchant, malformed
dates) before we hit Notion, so the user gets a clear error rather
than a 400 from the API.
"""

from __future__ import annotations

import datetime as _dt
from typing import Any


class SpecError(ValueError):
    pass


_REQUIRED_TOP = ("holder", "card", "bill_cycle", "due_date", "transactions")
_REQUIRED_TX = ("date", "name", "amount")


def _iso_date(s: Any, field: str) -> str:
    if not isinstance(s, str):
        raise SpecError(f"{field} must be an ISO date string, got {type(s).__name__}")
    try:
        _dt.date.fromisoformat(s)
    except ValueError as e:
        raise SpecError(f"{field}={s!r} is not a valid ISO date: {e}") from None
    return s


def validate_spec(spec: dict[str, Any]) -> None:
    if not isinstance(spec, dict):
        raise SpecError("top-level spec must be a JSON object")

    missing = [k for k in _REQUIRED_TOP if k not in spec]
    if missing:
        raise SpecError(f"missing required keys: {missing}")

    _iso_date(spec["bill_cycle"], "bill_cycle")
    _iso_date(spec["due_date"], "due_date")

    if "processed" in spec and not isinstance(spec["processed"], bool):
        raise SpecError("processed must be a boolean")

    txs = spec["transactions"]
    if not isinstance(txs, list) or not txs:
        raise SpecError("transactions must be a non-empty list")

    for i, tx in enumerate(txs):
        if not isinstance(tx, dict):
            raise SpecError(f"transactions[{i}] must be an object")
        missing = [k for k in _REQUIRED_TX if k not in tx]
        if missing:
            raise SpecError(f"transactions[{i}] missing keys: {missing}")
        _iso_date(tx["date"], f"transactions[{i}].date")
        if not isinstance(tx["name"], str) or not tx["name"].strip():
            raise SpecError(f"transactions[{i}].name must be a non-empty string")
        if not isinstance(tx["amount"], (int, float)):
            raise SpecError(f"transactions[{i}].amount must be a number")
        if "note" in tx and tx["note"] is not None and not isinstance(tx["note"], str):
            raise SpecError(f"transactions[{i}].note must be a string if present")
