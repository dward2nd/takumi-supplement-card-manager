"""Build the Notion `properties` payload for a new transaction page, or a patch to one.

deterministic + idempotent — same input produces the same payload.
(The act of POSTing the payload to Notion is *not* idempotent — that
caveat lives in add-transaction/cli.py.)

Pairs with `lib.transaction_read` (read side). They are split so a
reviewer can examine one side without scrolling past the other.
"""

from __future__ import annotations

import datetime as dt


# Mutually exclusive — at most one per transaction. Unchecked = ×1 (default).
# Every multiplier box any holder has; which ones a holder's DS actually has is
# `Holder.multipliers` (×3 is the primary's only).
VALID_MULTIPLIERS = frozenset({"×0", "×2", "×3", "×4", "×5", "÷4"})


def build_transaction_properties(
    *,
    name: str,
    amount: float,
    transaction_date: str,
    bill_cycle_date: str,
    due_date: str,
    card_page_id: str,
    processed: bool = True,
    note: str | None = None,
    multiplier: str | None = None,
    cashback_percent: float | None = None,
    points_redeemed: float | None = None,
    process_date: str | None = None,
) -> dict:
    """Assemble the Notion `properties` payload for one transaction page.

    `name` is written verbatim — no trimming, no normalization, no
    abbreviation expansion. That rule is what lets the user reconcile
    against bank statements.

    `multiplier`, if given, must be one of VALID_MULTIPLIERS. Only one
    multiplier checkbox can be set per page; absence means ×1 (default).

    `cashback_percent`, if given, is a raw fraction in [0, 1]. Notion
    stores percent-formatted numbers as the raw fraction (0.05 displays
    as 5%). The destination property is `% cb`, on all three holders'
    Transactions DSes (Takumi's since 2026-09-28).

    `points_redeemed`, if given, writes to `ใช้คะแนน` (a `number`
    property on all three holders' Transactions DSes). Positive values
    deduct points from the lifetime balance — a redemption row, e.g.
    "Major Combo set 1 ชุด" at 1,400 points. Negative values add points
    back (manual adjustment / refund of a prior redemption). The bank
    posts redemption events as zero-baht rows: callers should usually
    pair `points_redeemed` with `amount=0` and `multiplier="×0"` so the
    row doesn't accidentally earn anything either.

    `process_date`, if given, writes `Process Date`: the posting date a
    statement prints for the line (only /record-statement knows it).
    """
    props: dict = {
        "Name": {"title": [{"text": {"content": name}}]},
        "ยอดชำระ": {"number": amount},
        "Card": {"relation": [{"id": card_page_id}]},
        "Transaction Datetime": {"date": {"start": transaction_date}},
        "Bill Cycle Date": {"date": {"start": bill_cycle_date}},
        "Due Date": {"date": {"start": due_date}},
        "Processed": {"checkbox": bool(processed)},
    }
    if note:
        props["Note"] = {"rich_text": [{"text": {"content": note}}]}
    if multiplier is not None:
        if multiplier not in VALID_MULTIPLIERS:
            raise ValueError(
                f"multiplier must be one of {sorted(VALID_MULTIPLIERS)}; got {multiplier!r}"
            )
        props[multiplier] = {"checkbox": True}
    if cashback_percent is not None:
        if not (0 <= cashback_percent <= 1):
            raise ValueError(
                f"cashback_percent must be a raw fraction in [0, 1] "
                f"(0.05 = 5%); got {cashback_percent!r}"
            )
        props["% cb"] = {"number": float(cashback_percent)}
    if points_redeemed is not None:
        props["ใช้คะแนน"] = {"number": float(points_redeemed)}
    if process_date:
        props["Process Date"] = {"date": {"start": process_date}}
    return props


# Sentinel for "key was absent from the update", distinguishing it from
# "user explicitly passed null to clear the underlying Notion field".
_MISSING = object()


def build_update_properties(update: dict) -> dict:
    """The Notion `properties` patch for one /update-transaction entry.

    Keys: cashback_percent, note, multiplier, points_redeemed, bill_cycle +
    due_date, and the raw `properties` escape hatch (see update-transaction/cli.py).
    An explicit `null` clears `% cb` / `ใช้คะแนน`; an absent key leaves it alone.
    """
    props: dict = {}

    # `cashback_percent: null` clears `% cb` (writes JSON null → empty cell).
    # Distinguishes "user wants to clear" from "user didn't mention this
    # field" — the latter is the absence of the key.
    cb = update.get("cashback_percent", _MISSING)
    if cb is None:
        props["% cb"] = {"number": None}
    elif cb is not _MISSING:
        if not isinstance(cb, (int, float)) or isinstance(cb, bool) or not (0 <= cb <= 1):
            raise ValueError(
                f"cashback_percent must be a raw fraction in [0, 1] (or null to clear); got {cb!r}"
            )
        props["% cb"] = {"number": float(cb)}

    if (note := update.get("note")) is not None:
        if not isinstance(note, str):
            raise ValueError(f"note must be a string; got {type(note).__name__}")
        props["Note"] = {"rich_text": [{"text": {"content": note}}]}

    if (mult := update.get("multiplier")) is not None:
        if mult not in VALID_MULTIPLIERS:
            raise ValueError(
                f"multiplier must be one of {sorted(VALID_MULTIPLIERS)}; got {mult!r}"
            )
        props[mult] = {"checkbox": True}

    # `points_redeemed: null` clears `ใช้คะแนน` (mirrors cashback_percent's
    # sentinel semantics). Positive = deduct from lifetime balance, negative
    # = add back. The field exists on all three holders' Transactions DSes.
    pts = update.get("points_redeemed", _MISSING)
    if pts is None:
        props["ใช้คะแนน"] = {"number": None}
    elif pts is not _MISSING:
        if not isinstance(pts, (int, float)) or isinstance(pts, bool):
            raise ValueError(
                f"points_redeemed must be a number (or null to clear); got {pts!r}"
            )
        props["ใช้คะแนน"] = {"number": float(pts)}

    # bill_cycle / due_date: re-cycle a row (backdate or foredate). The two
    # dates form a pair on a given card — passing one without the other
    # leaves the row half-updated, which we refuse. Use the issuer's bill
    # cycle pattern (docs/concepts/bill-cycle-patterns) to pick a
    # consistent pair if you're not sure.
    has_bc = "bill_cycle" in update
    has_dd = "due_date" in update
    if has_bc ^ has_dd:
        raise ValueError(
            "bill_cycle and due_date must be provided together "
            "(both move the row to a different cycle); got one without the other"
        )
    if has_bc and has_dd:
        bc = update["bill_cycle"]
        dd = update["due_date"]
        if not isinstance(bc, str) or not isinstance(dd, str):
            raise ValueError(
                f"bill_cycle / due_date must be ISO date strings; got {bc!r} / {dd!r}"
            )
        # Best-effort ISO parse to fail loud on typos. Don't enforce the
        # bank's per-issuer cycle math here — the caller might be writing
        # an adjustment row outside the normal pattern.
        try:
            dt.date.fromisoformat(bc)
            dt.date.fromisoformat(dd)
        except ValueError as e:
            raise ValueError(
                f"bill_cycle / due_date must be valid ISO dates: {e}"
            ) from None
        props["Bill Cycle Date"] = {"date": {"start": bc}}
        props["Due Date"] = {"date": {"start": dd}}

    if (raw := update.get("properties")) is not None:
        if not isinstance(raw, dict):
            raise ValueError("properties escape-hatch must be an object")
        props.update(raw)

    if not props:
        raise ValueError(f"no recognized fields in update: {update!r}")

    return props
