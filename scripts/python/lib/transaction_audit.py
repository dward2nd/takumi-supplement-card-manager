"""Detect transaction rows whose (Bill Cycle Date, Due Date) don't match
the card's bank pattern.

deterministic + idempotent — pure functions of the page properties.

A row is *aligned* when both dates are present and their pair is the
shift-aware output of the card's pattern for the BC's month. We anchor
the comparison on the BC's *month*: we recompute what the pattern says
the (BC, Due) pair should be for that calendar month and check equality.

For UOB this works because the shift functions are deterministic (date
of week + Thai-holidays only). For all other issuers the shift is
identity.

When BC is missing we infer the *expected* BC from the transaction date
via `bill_cycle.active_cycle`; the user can then decide whether that's
the right cycle (back-fills sometimes belong to a closed older cycle).
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from . import bill_cycle


@dataclass(frozen=True)
class Issue:
    kind: str  # "both_missing" | "bc_missing" | "due_missing" | "bc_mismatch" | "due_mismatch"
    expected_bc: dt.date | None
    expected_due: dt.date | None


def _expected_pair_for_bc_month(
    pattern: bill_cycle.BillCyclePattern, bc: dt.date
) -> tuple[dt.date, dt.date]:
    """Given a BC date, recompute what (BC, Due) the pattern produces for that month."""
    return bill_cycle.cycle_for_month(pattern, bc.year, bc.month)


def diagnose(
    card_name: str,
    transaction_date: dt.date | None,
    bc: dt.date | None,
    due: dt.date | None,
) -> Issue | None:
    """Return an Issue if the (bc, due) pair is misaligned, else None.

    `transaction_date` is used only to infer the *expected* BC when the
    row is missing one — pass None to skip inference (the issue will
    still be flagged, just without expected values).
    """
    pattern = bill_cycle.pattern_for_card(card_name)

    if bc is None and due is None:
        exp_bc, exp_due = (
            bill_cycle.active_cycle(card_name, transaction_date)
            if transaction_date is not None
            else (None, None)
        )
        return Issue("both_missing", exp_bc, exp_due)

    if bc is None:
        # Due present without BC — can't anchor the expected pair on
        # Due's month (the next/prev rollover for things like AEON is
        # awkward to invert). Best-effort: use transaction_date if given.
        exp_bc, exp_due = (
            bill_cycle.active_cycle(card_name, transaction_date)
            if transaction_date is not None
            else (None, None)
        )
        return Issue("bc_missing", exp_bc, exp_due)

    exp_bc, exp_due = _expected_pair_for_bc_month(pattern, bc)

    if due is None:
        return Issue("due_missing", exp_bc, exp_due)

    if bc != exp_bc:
        return Issue("bc_mismatch", exp_bc, exp_due)
    if due != exp_due:
        return Issue("due_mismatch", exp_bc, exp_due)
    return None
