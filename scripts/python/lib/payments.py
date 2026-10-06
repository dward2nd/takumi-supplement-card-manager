"""lib.payments — record a bill payment as a negative-amount transaction.

In this household's model a *payment* is recorded as a negative `ยอดชำระ`
row in the Transactions DB (e.g. `ชำระบิลเต็มจำนวน` — paid bill in full),
tagged to the **paid bill's cycle** — the same `Bill Cycle Date` /
`Due Date` as that cycle's charges — with `Transaction Datetime` set to
the date the money actually moved (the payment slip's date). The row
carries **no cashback** (`% cb` stays unset): a payment is not a purchase.

Why a negative row at all, when the Bills DB already has `จ่ายแล้ว`?
The `จ่ายแล้ว` checkbox records *that* a statement was settled; the
negative transaction is what offsets the card's running balance so the
cycle nets to zero. The two are independent — the checkbox lives on the
Bills row (patched by /update-bill), the offset lives in Transactions.

This module is the shared core for the `/record-payment` skill and for
`/update-bill`'s slip-upload delegation. It is deterministic given its
inputs; `record_payment` additionally guards against double-recording by
scanning the cycle for an existing matching payment row before creating,
so re-running the same payment is effectively a no-op (unless `force`).
"""

from __future__ import annotations

import datetime as _dt

from lib import notion_client
from lib.ledger import cycle_rows, is_bill_payment_row  # noqa: F401 — re-exported for callers
from lib.bill_cycle import due_date_for
from lib.cards import find_card
from lib.holders import HOLDERS, Holder, resolve_holder
from lib.transaction_write import build_transaction_properties

# Default label per payment kind. Free-form Thai, matching the most common
# forms already in the data. Callers may override with an explicit `name`.
PAYMENT_LABELS: dict[str, str] = {
    "full": "ชำระบิลเต็มจำนวน",  # paid the statement in full
    "partial": "ชำระบางส่วน",  # paid only part of the statement
    "advance": "ชำระบิลล่วงหน้า",  # paid ahead of the statement closing
    "completing": "ชำระเพิ่มบางส่วนจนครบ",  # the payment that finishes a partly paid bill
}

# How close (in baht) an existing negative row must be to the target before
# we treat the bill as already paid in the ledger. 0.5 absorbs satang drift
# (e.g. a ฿10,693.00 transfer against a ฿10,693.09 bill) without matching an
# unrelated small refund.
_MATCH_TOLERANCE = 0.5


def is_payment_row(row: dict) -> bool:
    """True if a projected row looks like a *payment* — LOOSE, for dedup only.

    A payment is a negative-amount row that is neither a cashback credit
    nor a bracket-prefixed bookkeeping row (`[ยกเลิก]`, `[เว็บรับหนี้…]`,
    `[ยอดยกมา…]`). Those carry their own meaning and must not be mistaken
    for "the payment that settled this bill". Magnitude matching (below)
    is the real safeguard; this filter just removes obvious non-payments.

    Deliberately over-inclusive: it also matches plain merchant **refunds**
    (`WWW.GRAB.COM BANGKOK TH −75`, `UNIONPAY MERCHANT BEIJING CHN`) and
    `CB`-prefixed cashback credits (`CB HTTPS://WWW.MAKRO.PRO/ …`), because
    inside `record_payment` the amount check filters those out anyway. Do
    **not** reuse this as a standalone gate — use `is_bill_payment_row`.
    """
    amount = row.get("amount") or 0.0
    if amount >= 0:
        return False
    name = (row.get("name") or "").strip()
    if "cashback" in name.lower():
        return False
    if name.startswith("["):
        return False
    return True


def _coverage_match(existing_payments: list[dict], target: float) -> str | None:
    """Return how the cycle already covers `target`, or None.

    - 'sum'    — the existing payment rows already sum to ~target.
    - 'single' — one existing payment row is ~target on its own.
    """
    total = round(sum(abs(p.get("amount") or 0.0) for p in existing_payments), 2)
    if abs(total - target) <= _MATCH_TOLERANCE:
        return "sum"
    for p in existing_payments:
        if abs(abs(p.get("amount") or 0.0) - target) <= _MATCH_TOLERANCE:
            return "single"
    return None


def _due_date_for_cycle(
    rows: list[dict], card_name: str, bill_cycle: str
) -> str:
    """Due date for the payment row.

    Prefer the `Due Date` already used by the cycle's existing charges —
    that guarantees consistency with the rest of the cycle, including
    UOB's weekend/holiday shift. Fall back to deriving it from the card's
    bank pattern when the cycle has no rows yet (e.g. an advance payment
    before any charge has been entered).
    """
    for r in rows:
        dd = r.get("due_date")
        if dd:
            return dd
    return due_date_for(card_name, _dt.date.fromisoformat(bill_cycle)).isoformat()


def _payment_summary(payments: list[dict]) -> list[dict]:
    return [
        {"id": p.get("id"), "name": p.get("name"), "amount": p.get("amount")}
        for p in payments
    ]


def record_payment(
    holder_input: str | Holder,
    card_name: str,
    bill_cycle: str,
    *,
    amount: float,
    payment_date: str | None = None,
    kind: str = "full",
    name: str | None = None,
    note: str | None = None,
    due_date: str | None = None,
    force: bool = False,
    dry_run: bool = False,
) -> dict:
    """Record one bill payment as a negative-amount transaction.

    `amount` is the payment magnitude (positive); it is stored negated.
    `bill_cycle` is the `วันตัดรอบบิล` of the bill being paid — the row
    is tagged to that cycle. `payment_date` (the slip date) defaults to
    today. `kind` selects the default label (full/partial/advance);
    `name` overrides it. The row never earns cashback or points.

    Idempotency guard: unless `force`, if the cycle already has payment
    row(s) that match `amount` (a single row ~amount, or the payment
    rows summing to ~amount), no row is created and `created: False` is
    returned with the matching rows echoed.
    """
    holder = resolve_holder(holder_input) if isinstance(holder_input, str) else holder_input
    if holder.bills_ds is None:
        raise ValueError(
            f"{holder.key!r} has no Bills DB — payments are recorded for baiboon/nuta only"
        )
    if holder.statement_bills:
        # Takumi's slip pays the bank for the whole card — the supplements'
        # shares too — so a single full-bill row would drive his own card's
        # balance negative by their amount. His 2025 ledger balanced it with
        # `โอนยอดจาก<holder> - <card>` rows; that pairing isn't automated yet.
        raise ValueError(
            f"{holder.key!r} pays the whole card bill to the bank; a full-bill payment "
            f"row needs matching โอนยอดจาก… rows for the supplements' shares, which "
            f"this helper doesn't write — record it by hand"
        )
    if kind not in PAYMENT_LABELS:
        raise ValueError(f"kind must be one of {sorted(PAYMENT_LABELS)}; got {kind!r}")

    card = find_card(holder.cards_ds, card_name)
    card_page_id = card["id"]
    target = round(abs(float(amount)), 2)
    if target == 0:
        raise ValueError("amount must be non-zero")
    payment_date = payment_date or _dt.date.today().isoformat()
    label = name or PAYMENT_LABELS[kind]

    rows = cycle_rows(holder.transactions_ds, card_page_id, bill_cycle)
    existing = [p for p in rows if is_payment_row(p)]
    match = _coverage_match(existing, target)

    base = {
        "holder": holder.key,
        "card": card_name,
        "bill_cycle": bill_cycle,
        "target_amount": target,
        "existing_payments": _payment_summary(existing),
    }

    if match and not force:
        return {
            **base,
            "would_create": False,
            "created": False,
            "reason": f"matching payment already present in cycle ({match} match)",
        }

    if due_date is None:
        due_date = _due_date_for_cycle(rows, card_name, bill_cycle)

    props = build_transaction_properties(
        name=label,
        amount=-target,  # negative — it's a payment, not a charge
        transaction_date=payment_date,
        bill_cycle_date=bill_cycle,
        due_date=due_date,
        card_page_id=card_page_id,
        processed=True,
        note=note,
        multiplier=None,  # payments don't earn points — leave all checkboxes off
        cashback_percent=None,  # NO cashback — a payment is not a purchase
    )

    out = {
        **base,
        "would_create": True,
        "created": not dry_run,
        "forced": bool(force and match),
        "kind": kind,
        "name": label,
        "amount": -target,
        "payment_date": payment_date,
        "due_date": due_date,
    }
    if dry_run:
        out["dry_run"] = True
        out["properties"] = props
        return out

    page = notion_client.create_page(holder.transactions_ds, props)
    out["id"] = page["id"]
    out["url"] = page.get("url")
    return out


def record_primary_payment(
    holder_input: str | Holder,
    card_name: str,
    bill_cycle: str,
    *,
    amount: float,
    bill_total: float,
    payment_date: str,
    memo: str | None = None,
    covers: dict[str, float] | None = None,
    due_date: str | None = None,
    dry_run: bool = False,
) -> dict:
    """Takumi's payment of one of his (statement-driven) bills.

    The bank bills the whole card, so his slip can pay his own charges and
    his friends' shares at once. His ledger gets the payment row (−amount)
    and, for each friend share the slip `covers`, a `โอนยอดจาก<name>` row
    (+share) that moves that share onto his balance — the friend's own
    ledger records their payment to him when they pay. The label follows
    what's already paid on the bill: in full, partly, or the payment that
    completes it. Idempotent: a payment row of the same amount and date, or
    a transfer row of the same name, amount and date, is not written twice.
    """
    holder = resolve_holder(holder_input) if isinstance(holder_input, str) else holder_input
    if not holder.statement_bills:
        raise ValueError(f"{holder.key!r} isn't the primary holder; use record_payment")
    covers = covers or {}
    unknown = [h for h in covers if h not in HOLDERS or HOLDERS[h].statement_bills]
    if unknown:
        raise ValueError(f"covers names holders that aren't supplement holders: {unknown}")
    target = round(abs(float(amount)), 2)
    card_page_id = find_card(holder.cards_ds, card_name)["id"]
    rows = cycle_rows(holder.transactions_ds, card_page_id, bill_cycle)
    # Bill payments only (`ชำระ…`/`จ่าย…`, or the bank's `AUTO DEBIT`) — not refunds or credits.
    paid = [p for p in rows if is_bill_payment_row(p) or (p.get("name") == "AUTO DEBIT" and (p.get("amount") or 0) < 0)]
    paid_before = round(-sum(p["amount"] for p in paid), 2)
    same = [p for p in paid if abs(p["amount"] + target) < 0.005 and (p.get("transaction_date") or "")[:10] == payment_date]
    if same:
        paid_before -= target   # this slip is already in the ledger
    completes = paid_before + target >= float(bill_total) - _MATCH_TOLERANCE
    kind = "full" if completes and paid_before < _MATCH_TOLERANCE else "completing" if completes else "partial"
    due_date = due_date or _due_date_for_cycle(rows, card_name, bill_cycle)

    writes: list[dict] = []
    if not same:
        writes.append({"name": PAYMENT_LABELS[kind], "amount": -target,
                       "note": f"Slip memo: {memo}" if memo else None})
    for h, share in covers.items():
        name = f"โอนยอดจาก{HOLDERS[h].thai_name}"
        share = round(float(share), 2)
        if any(r["name"] == name and abs((r["amount"] or 0) - share) < 0.005
               and (r.get("transaction_date") or "")[:10] == payment_date for r in rows):
            continue
        # ×0: a positive amount earns points, and those points are already on the friend's rows.
        writes.append({"name": name, "amount": share, "multiplier": "×0",
                       "note": f"{HOLDERS[h].thai_name}'s share of the card bill, paid to the bank by this slip."})

    out = {"holder": holder.key, "card": card_name, "bill_cycle": bill_cycle, "kind": kind,
           "paid_before": paid_before, "amount": -target, "already_recorded": bool(same),
           "rows": [{k: v for k, v in w.items() if v is not None} for w in writes], "dry_run": dry_run}
    if dry_run:
        return out
    for w in writes:
        props = build_transaction_properties(
            name=w["name"], amount=w["amount"], transaction_date=payment_date, bill_cycle_date=bill_cycle,
            due_date=due_date, card_page_id=card_page_id, processed=True, note=w["note"],
            multiplier=w.get("multiplier"))
        w["id"] = notion_client.create_page(holder.transactions_ds, props)["id"]
    out["rows"] = [{k: v for k, v in w.items() if v is not None} for w in writes]
    return out

