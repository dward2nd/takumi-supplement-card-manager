"""Build the Notion `properties` payload for a new transaction page.

deterministic + idempotent — same input produces the same payload.
(The act of POSTing the payload to Notion is *not* idempotent — that
caveat lives in add-transaction/cli.py.)

Pairs with `lib.transaction_read` (read side). They are split so a
reviewer can examine one side without scrolling past the other.
"""

from __future__ import annotations


# Mutually exclusive — at most one per transaction. Unchecked = ×1 (default).
# ×3 exists only on Takumi's Transactions DB; the others are universal.
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
) -> dict:
    """Assemble the Notion `properties` payload for one transaction page.

    `name` is written verbatim — no trimming, no normalization, no
    abbreviation expansion. That rule is what lets the user reconcile
    against bank statements.

    `multiplier`, if given, must be one of VALID_MULTIPLIERS. Only one
    multiplier checkbox can be set per page; absence means ×1 (default).

    `cashback_percent`, if given, is a raw fraction in [0, 1]. Notion
    stores percent-formatted numbers as the raw fraction (0.05 displays
    as 5%). The destination property is `% cb`, which exists on
    Baiboon's and Nuta's Transactions DSes but not Takumi's — the
    caller is responsible for not passing this for Takumi.
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
    return props
