"""Greedy 1-1 match between statement rows and Notion transactions.

deterministic + idempotent — pure function of its inputs.

Used by audit-bill/cli.py. Statement rows come from the bank PDF
(extracted by the agent), Notion rows come from the cycle's
transactions on the named card. The matcher pairs them by exact
amount (in baht, rounded to 2dp), preferring pairs whose normalized
merchant tokens overlap. Unmatched rows on either side surface as
audit findings.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any


_TOKEN_MIN_LEN = 3


def _normalize_tokens(name: str) -> set[str]:
    if not name:
        return set()
    parts = re.split(r"[^A-Za-z0-9]+", name.upper())
    return {p for p in parts if len(p) >= _TOKEN_MIN_LEN}


def _name_match(a: str, b: str) -> bool:
    return bool(_normalize_tokens(a) & _normalize_tokens(b))


def _amount_key(amount: float | int | None) -> float:
    return round(float(amount or 0), 2)


def match(statement_rows: list[dict], notion_rows: list[dict]) -> dict[str, Any]:
    """Pair statement rows with notion rows.

    Each statement row is a dict with at least `amount` (float, signed) and
    `name` (str). `date` (ISO string) is optional and echoed back. Notion
    rows are projections from `lib.transaction_read.project_transaction`
    (already have `amount`, `name`, `transaction_date`, etc.).

    Returns:
      {
        "matched":           [{statement, notion, name_match: bool}, ...],
        "missing_in_notion": [statement_row, ...],   # statement has, notion doesn't
        "extra_in_notion":   [notion_row, ...],      # notion has, statement doesn't
      }
    """
    notion_by_amt: dict[float, list[dict]] = defaultdict(list)
    for nr in notion_rows:
        notion_by_amt[_amount_key(nr.get("amount"))].append(nr)

    matched: list[dict] = []
    missing: list[dict] = []

    for sr in statement_rows:
        key = _amount_key(sr.get("amount"))
        bucket = notion_by_amt.get(key) or []
        if not bucket:
            missing.append(sr)
            continue

        sname = sr.get("name") or ""
        # Prefer a candidate whose name shares ≥1 token of length ≥3.
        chosen_idx: int | None = None
        for i, c in enumerate(bucket):
            if _name_match(sname, c.get("name") or ""):
                chosen_idx = i
                break

        if chosen_idx is None:
            chosen = bucket.pop(0)
            name_match_flag = False
        else:
            chosen = bucket.pop(chosen_idx)
            name_match_flag = True

        matched.append(
            {
                "statement": sr,
                "notion": chosen,
                "name_match": name_match_flag,
            }
        )

    extras: list[dict] = []
    for bucket in notion_by_amt.values():
        extras.extend(bucket)

    return {
        "matched": matched,
        "missing_in_notion": missing,
        "extra_in_notion": extras,
    }
