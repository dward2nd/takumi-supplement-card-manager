"""Input-spec validation for add-transaction.

deterministic + idempotent — safe to re-run.

Surfaces obvious mistakes (missing keys, empty merchant, malformed
dates) before we hit Notion, so the user gets a clear error rather
than a 400 from the API.
"""

from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.transaction_write import VALID_MULTIPLIERS


class SpecError(ValueError):
    pass


_REQUIRED_TOP = ("holder", "card", "transactions")
_REQUIRED_TX = ("date", "name", "amount")


def _check_multiplier(value: Any, field: str) -> None:
    if value is None:
        return
    if not isinstance(value, str) or value not in VALID_MULTIPLIERS:
        raise SpecError(
            f"{field}={value!r} must be one of {sorted(VALID_MULTIPLIERS)} or null"
        )


def _check_cashback_percent(value: Any, field: str) -> None:
    if value is None:
        return
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise SpecError(f"{field}={value!r} must be a number (raw fraction, 0.05 = 5%)")
    if not (0 <= value <= 1):
        raise SpecError(
            f"{field}={value!r} must be in [0, 1] — pass 0.05 for 5%, not 5"
        )


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

    if "bill_cycle" in spec and spec["bill_cycle"] is not None:
        _iso_date(spec["bill_cycle"], "bill_cycle")
    if "due_date" in spec and spec["due_date"] is not None:
        _iso_date(spec["due_date"], "due_date")
    # bill_cycle / due_date are optional: when omitted, the CLI infers
    # them from the card's bank pattern (see lib/bill_cycle.py). When
    # the user supplies one, they must supply the other — a half-spec
    # would mix inference and user intent in confusing ways.
    has_bc = bool(spec.get("bill_cycle"))
    has_dd = bool(spec.get("due_date"))
    if has_bc ^ has_dd:
        raise SpecError(
            "bill_cycle and due_date must be provided together or both omitted "
            "(omit both to auto-infer from the card's bank pattern)"
        )

    if "processed" in spec and not isinstance(spec["processed"], bool):
        raise SpecError("processed must be a boolean")

    _check_multiplier(spec.get("multiplier"), "multiplier")
    _check_cashback_percent(spec.get("cashback_percent"), "cashback_percent")

    holder = spec["holder"]
    has_batch_cb = spec.get("cashback_percent") is not None

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
        _check_multiplier(tx.get("multiplier"), f"transactions[{i}].multiplier")
        _check_cashback_percent(
            tx.get("cashback_percent"), f"transactions[{i}].cashback_percent"
        )
        if (has_batch_cb or tx.get("cashback_percent") is not None) and holder != "nuta":
            raise SpecError(
                f"cashback_percent (`% cb`) only exists on Nuta's Transactions DS; "
                f"holder is {holder!r}"
            )
