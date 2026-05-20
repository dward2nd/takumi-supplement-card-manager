"""Build the Notion `properties` payload for a new transaction page.

deterministic + idempotent — same input produces the same payload.
(The act of POSTing the payload to Notion is *not* idempotent — that
caveat lives in add-notion-transaction/cli.py.)

Pairs with `lib.transaction_read` (read side). They are split so a
reviewer can examine one side without scrolling past the other.
"""

from __future__ import annotations


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
) -> dict:
    """Assemble the Notion `properties` payload for one transaction page.

    `name` is written verbatim — no trimming, no normalization, no
    abbreviation expansion. That rule is what lets the user reconcile
    against bank statements.
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
    return props
