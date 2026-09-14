"""Draft a Bills row from a cycle's transactions.

deterministic + idempotent — re-running for the same (holder, card,
bill_cycle) refuses to create a duplicate. A Bills row uniquely
identifies on (Card, วันตัดรอบบิล); `draft_bill` aborts when one already
exists for that pair (draft or final).

This is the core behind /prepare-bill. It lives in `lib/` rather than in
`scripts/python/prepare-bill/` because /update-bill also needs it: when a
payment slip arrives for a cycle whose Bills row doesn't exist yet, that
skill drafts the bill first so the slip has somewhere to attach (the
script directory name `prepare-bill` is not a valid Python identifier, so
sharing by import from there isn't possible).

Sums `ยอดชำระ` across every transaction whose `Bill Cycle Date` equals the
cycle's BC date for the named card, **excluding bill-payment rows** —
`ยอดชำระ` is the amount *due*, not the balance remaining. Cashback offsets
are expected to already exist in the cycle as negative-amount rows, so the
sum is the "balance including cashback".
"""

from __future__ import annotations

import datetime as _dt

from . import installments, notion_client, promotions
from .bill_cycle import active_cycle, cycle_for_month, pattern_for_card
from .bills import explain_cycle, require_bills_ds
from .cards import find_card
from .holders import resolve_holder
from .payments import is_bill_payment_row
from .transaction_read import project_transaction

DRAFT_PREFIX = "[DRAFT] "


class BillDraftError(RuntimeError):
    pass


def cards_with_crediting_schedule() -> frozenset[str]:
    """Cards whose active promo declares a crediting_schedule.

    Such cards need explicit `*CASHBACK*` credit rows in the cycle before
    the bill is drafted, otherwise the flat sum overstates the balance.
    Derived from the promotions repository, so adding a new cashback-tier
    card is a YAML edit, not a Python edit.
    """
    return frozenset(p.card for p in promotions.load_all() if p.crediting_schedule)


def select_options(ds_id: str) -> list[str]:
    """SELECT options on a Bills DS's `Card` property (verbatim strings)."""
    client = notion_client.get_client()
    ds = client.data_sources.retrieve(data_source_id=ds_id)
    card_prop = ds.get("properties", {}).get("Card", {})
    if card_prop.get("type") != "select":
        raise BillDraftError("Bills DS `Card` is not a SELECT — schema drift?")
    return [opt.get("name") for opt in card_prop.get("select", {}).get("options", [])]


def existing_bill(ds_id: str, card: str, bill_cycle: str) -> dict | None:
    pages = notion_client.query_all(
        ds_id,
        filter={
            "and": [
                {"property": "Card", "select": {"equals": card}},
                {"property": "วันตัดรอบบิล", "date": {"equals": bill_cycle}},
            ]
        },
    )
    return pages[0] if pages else None


def sum_cycle(
    transactions_ds: str, card_page_id: str, bill_cycle: str
) -> tuple[float, int, list[dict]]:
    rows = notion_client.query_all(
        transactions_ds,
        filter={
            "and": [
                {"property": "Card", "relation": {"contains": card_page_id}},
                {"property": "Bill Cycle Date", "date": {"equals": bill_cycle}},
            ]
        },
    )
    # Bill-payment rows (`ชำระ…` / `จ่าย…`) are excluded: `ยอดชำระ` is the
    # cycle's *amount due*, not its remaining balance. Including them would
    # net the payment into the total and make the result order-dependent — a
    # cycle drafted before its payment was recorded would read differently
    # from the same cycle drafted after. Cashback credits, refunds and
    # `[…]`-prefixed adjustments DO count; they change what is owed.
    # See lib.payments.is_bill_payment_row.
    total = 0.0
    for r in rows:
        projected = project_transaction(r)
        if is_bill_payment_row(projected):
            continue
        amt = projected.get("amount")
        if amt is not None:
            total += amt
    return round(total, 2), len(rows), rows


def has_cashback_credit_rows(rows: list[dict]) -> bool:
    """Heuristic: at least one row whose `Name` mentions CASHBACK."""
    for r in rows:
        props = r.get("properties", {})
        title = props.get("Name") or {}
        text = "".join(t.get("plain_text", "") for t in title.get("title", []) or [])
        if "CASHBACK" in text.upper():
            return True
    return False


def draft_bill(spec: dict, *, dry_run: bool = False) -> dict:
    """Create the `[DRAFT] <Card> <YYYY-MM>` Bills row for a cycle.

    Spec keys: `holder`, `card` (required); `bill_cycle` (optional, inferred
    from the card's bank pattern); `skip_populate_installments`,
    `skip_cashback_check`, `skip_auto_note` (all optional, default False).
    """
    if not isinstance(spec, dict):
        raise BillDraftError("spec must be a JSON object")
    for key in ("holder", "card"):
        if not spec.get(key):
            raise BillDraftError(f"missing required field: {key!r}")

    holder = resolve_holder(spec["holder"])
    bills_ds = require_bills_ds(holder)
    card_name = spec["card"]

    options = select_options(bills_ds)
    if card_name not in options:
        raise BillDraftError(
            f"card {card_name!r} is not a SELECT option on {holder.key}'s "
            f"Bills `Card` field. Options: {sorted(options)}"
        )
    card = find_card(holder.cards_ds, card_name)

    if (bc := spec.get("bill_cycle")):
        # Validate ISO format eagerly so we fail loud.
        _dt.date.fromisoformat(bc)
        bill_cycle = bc
    else:
        bc_date, _ = active_cycle(card_name, _dt.date.today())
        bill_cycle = bc_date.isoformat()

    existing = existing_bill(bills_ds, card_name, bill_cycle)
    if existing is not None:
        raise BillDraftError(
            f"a bill row already exists for {holder.key}/{card_name} cycle "
            f"{bill_cycle} (id={existing['id']}). Refusing to create a duplicate."
        )

    # Auto-populate in-progress installments into this cycle before summing.
    # Without this, a 10-month plan whose next term hasn't been written yet
    # would silently shrink the bill total. The populate call is idempotent —
    # plans whose next term already lives in this cycle are skipped — and
    # uses the same library function /populate-installment calls, so the two
    # skills can't disagree. The user can disable this for back-fills where
    # they're recreating a historical bill snapshot.
    installments_summary: dict | None = None
    if not spec.get("skip_populate_installments"):
        # Derive the cycle's due date from the card's bank pattern so
        # appended rows carry the correct DD without depending on the
        # Bills DB which doesn't store DD on its own.
        bc_date = _dt.date.fromisoformat(bill_cycle)
        pattern = pattern_for_card(card_name)
        cand_bc, cand_dd = cycle_for_month(pattern, bc_date.year, bc_date.month)
        if cand_bc != bc_date:
            cand_dd = pattern.due_date_shift(pattern.due_from_nominal_bc(bc_date))
        installments_summary = installments.populate_for_cycle(
            holder_key=holder.key,
            transactions_ds=holder.transactions_ds,
            card_name=card_name,
            card_page_id=card["id"],
            bill_cycle=bill_cycle,
            due_date=cand_dd.isoformat(),
            auto_classify=True,
            exclude=set(),
            dry_run=dry_run,
        )

    total, tx_count, rows = sum_cycle(holder.transactions_ds, card["id"], bill_cycle)
    if tx_count == 0:
        raise BillDraftError(
            f"no transactions found for {holder.key}/{card_name} cycle {bill_cycle} "
            f"— nothing to bill. Did you mean a different cycle date?"
        )

    if card_name in cards_with_crediting_schedule() and not spec.get("skip_cashback_check"):
        if not has_cashback_credit_rows(rows):
            raise BillDraftError(
                f"{card_name} requires cashback credit rows before drafting the bill — "
                f"its active promotion declares a crediting_schedule but the cycle has no "
                f"`*CASHBACK*` transactions, so the sum would overstate the balance owed. "
                f"Run /post-cashback-credits first (or pass "
                f'`"skip_cashback_check": true` in the spec to override).'
            )

    bc_date = _dt.date.fromisoformat(bill_cycle)
    title = f"{DRAFT_PREFIX}{card_name} {bc_date.strftime('%Y-%m')}"

    # Auto-generate the Note explaining special rows in this cycle (cashback
    # credits, manual adjustments, installment terms). Skip when the user
    # passes `skip_auto_note: true` — they may want to leave Note blank or
    # supply their own text via /update-bill afterwards.
    auto_note: str | None = None
    if not spec.get("skip_auto_note"):
        projected = [project_transaction(r) for r in rows]
        auto_note = explain_cycle(projected)

    properties = {
        "title": {"title": [{"text": {"content": title}}]},
        "Card": {"select": {"name": card_name}},
        "วันตัดรอบบิล": {"date": {"start": bill_cycle}},
        "ยอดชำระ": {"number": total},
        "จ่ายแล้ว": {"checkbox": False},
    }
    if auto_note:
        properties["Note"] = {"rich_text": [{"text": {"content": auto_note}}]}

    if dry_run:
        out: dict = {
            "dry_run": True,
            "holder": holder.key,
            "card": card_name,
            "bill_cycle": bill_cycle,
            "title": title,
            "ยอดชำระ": total,
            "tx_count": tx_count,
        }
        if installments_summary is not None:
            out["installments"] = installments_summary
        if auto_note:
            out["auto_note"] = auto_note
        return out

    page = notion_client.create_page(bills_ds, properties)
    out = {
        "id": page["id"],
        "url": page.get("url"),
        "holder": holder.key,
        "card": card_name,
        "bill_cycle": bill_cycle,
        "title": title,
        "ยอดชำระ": total,
        "tx_count": tx_count,
    }
    if installments_summary is not None:
        out["installments"] = installments_summary
    if auto_note:
        out["auto_note"] = auto_note
    return out
