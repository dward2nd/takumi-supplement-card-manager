"""Bill-row lookup + explanation on a holder's Bills DB.

deterministic + idempotent — safe to re-run.

Bills uniquely identify by (Card SELECT, วันตัดรอบบิล date). The Card
field is a SELECT (not a relation — see docs/concepts/known-divergences),
so card matching here is on the verbatim select-option string. Bill
cycle dates are ISO date strings.

Takumi has no Bills DB; lookups for `takumi` raise BillsNotSupported.

`explain_cycle()` produces a one-block Note text summarising the special
rows in a cycle — installment terms, cashback credit rows, and manual
adjustments — so the bill row itself documents *why* the total is what
it is. Used by both /prepare-bill (on draft) and /update-bill (on refresh).
"""

from __future__ import annotations

from collections import defaultdict

from . import installments, notion_client, payments
from .holders import Holder


class BillNotFoundError(RuntimeError):
    pass


class BillAmbiguousError(RuntimeError):
    pass


class BillsNotSupported(RuntimeError):
    pass


def require_bills_ds(holder: Holder) -> str:
    if not holder.bills_ds:
        raise BillsNotSupported(
            f"{holder.key!r} has no Bills database (only baiboon and nuta do)"
        )
    return holder.bills_ds


def find_bill(holder: Holder, card: str, bill_cycle: str) -> dict:
    """Return the single Bills page for (card, bill_cycle) on this holder.

    `card` matches the `Card` SELECT option verbatim. `bill_cycle` is
    the value of `วันตัดรอบบิล` (ISO date).
    """
    ds = require_bills_ds(holder)
    pages = notion_client.query_all(
        ds,
        filter={
            "and": [
                {"property": "Card", "select": {"equals": card}},
                {"property": "วันตัดรอบบิล", "date": {"equals": bill_cycle}},
            ]
        },
    )
    if not pages:
        raise BillNotFoundError(
            f"no bill on {holder.key}'s Bills DB for card={card!r}, "
            f"วันตัดรอบบิล={bill_cycle!r}"
        )
    if len(pages) > 1:
        raise BillAmbiguousError(
            f"multiple bills on {holder.key}'s Bills DB for card={card!r}, "
            f"วันตัดรอบบิล={bill_cycle!r}: {[p['id'] for p in pages]}"
        )
    return pages[0]


# --------------------------------------------------------------------------
# Cycle explanation — auto-generate the Bills.Note from cycle transactions
# --------------------------------------------------------------------------


def _categorize_row(row: dict) -> str:
    """Tag a transaction row by what it represents in the bill.

    Categories:
      - 'cashback'           — credit row (name contains CASHBACK).
      - 'installment-new'    — first term of a plan (term == 1).
      - 'installment-cont'   — second or later term of a plan.
      - 'bill-payment'       — a `ชำระ…`/`จ่าย…` row settling the bill.
                               EXCLUDED from `ยอดชำระ` by the callers, so it
                               must not be narrated as something that shaped
                               the total.
      - 'manual-adjustment'  — square-bracketed name (e.g.
                               `[เว็บรับหนี้ไปบริหารต่อ]`), or `Credit Return`
                               flag set, or a negative-amount row that isn't
                               cashback / installment / a bill payment.
      - 'regular'            — normal purchase.

    These are heuristics, not authoritative classifications. The bracket
    rule is intentionally limited to `[` — `(FOR SHOPEE)*(FOR SHOP …` is
    a legitimate merchant string that starts with `(` and should stay in
    `regular`.

    The 'bill-payment' test delegates to `payments.is_bill_payment_row`, the
    same predicate `/prepare-bill`'s `_sum_cycle` and `/update-bill`'s
    `refresh_from_transactions` use to drop these rows from the sum. Sharing
    the predicate is the point: when the two disagreed, the Note listed the
    payment among the "manual adjustments" that produced `ยอดชำระ` while the
    sum had excluded it, so following the Note's arithmetic landed a reader
    short by exactly the payment amount.
    """
    name = (row.get("name") or "").strip()
    if "CASHBACK" in name.upper():
        return "cashback"
    parsed = installments.parse(name)
    if parsed is not None:
        return "installment-new" if parsed.term == 1 else "installment-cont"
    if name.startswith("["):
        return "manual-adjustment"
    if row.get("credit_return"):
        return "manual-adjustment"
    # Must precede the negative-amount fallback below, which would otherwise
    # swallow every payment row into 'manual-adjustment'. Strict on the Thai
    # payment-verb prefix, so cashback credits, refunds and `[…]` rows are
    # untouched.
    if payments.is_bill_payment_row(row):
        return "bill-payment"
    amount = row.get("amount") or 0.0
    if amount < 0:
        # Negative + not cashback + not bracketed — most likely a refund or
        # a manually-entered adjustment row.
        return "manual-adjustment"
    return "regular"


def _fmt_thb(amount: float) -> str:
    """Format a THB amount with sign + 2dp + thousands separators."""
    sign = "−" if amount < 0 else ""
    return f"{sign}฿{abs(amount):,.2f}"


def _join_short(items: list[str], *, limit: int = 6) -> str:
    """Join up to `limit` items with semicolons; if longer, append a count.

    Avoids unbounded Note bloat when a cycle has many rows in a single
    bucket (e.g. 30 ongoing installment terms). The summary count stays
    accurate; the per-row enumeration is the part that's truncated.
    """
    if len(items) <= limit:
        return "; ".join(items)
    head = "; ".join(items[:limit])
    remaining = len(items) - limit
    return f"{head}; (+{remaining} more)"


def explain_cycle(rows: list[dict]) -> str | None:
    """Generate a Note text explaining the special rows in a cycle.

    `rows` is a list of projected transactions (see `lib.transaction_read`).
    Returns None when the cycle is entirely "regular" purchases and there's
    nothing worth noting; otherwise returns a single rich-text string ready
    to write to the Bills row's `Note` field.

    The Note structure:

        This cycle includes:
        - N new installment plan(s): ...
        - N ongoing installment term(s): ...
        - N cashback credit(s): ...
        - N manual adjustment(s): ...
        - N bill payment(s) (excluded from the total): ...

    Bullets are omitted when their bucket is empty.

    Every bullet except the last describes a row that *contributed* to
    `ยอดชำระ`. Bill payments are listed separately and labelled excluded,
    because the callers drop them from the sum — see `_categorize_row`.
    """
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        buckets[_categorize_row(r)].append(r)

    lines: list[str] = []

    new_inst = buckets.get("installment-new", [])
    if new_inst:
        descs = []
        for r in new_inst:
            info = installments.parse(r["name"])
            total = info.total if info else "?"
            amt = float(r.get("amount") or 0.0)
            descs.append(f"{r['name']} ({_fmt_thb(amt)}/term × {total})")
        label = "new installment plan" + ("" if len(new_inst) == 1 else "s")
        lines.append(f"- {len(new_inst)} {label}: {_join_short(descs)}.")

    cont = buckets.get("installment-cont", [])
    if cont:
        descs = [f"{r['name']} {_fmt_thb(float(r.get('amount') or 0.0))}" for r in cont]
        label = "ongoing installment term" + ("" if len(cont) == 1 else "s")
        lines.append(f"- {len(cont)} {label}: {_join_short(descs)}.")

    cashback = buckets.get("cashback", [])
    if cashback:
        descs = [f"{r['name']} {_fmt_thb(float(r.get('amount') or 0.0))}" for r in cashback]
        label = "cashback credit" + ("" if len(cashback) == 1 else "s")
        lines.append(f"- {len(cashback)} {label}: {_join_short(descs)}.")

    adjustments = buckets.get("manual-adjustment", [])
    if adjustments:
        descs = []
        for r in adjustments:
            amt = float(r.get("amount") or 0.0)
            note = (r.get("note") or "").strip()
            tail = f" — {note}" if note else ""
            descs.append(f"{r['name']} {_fmt_thb(amt)}{tail}")
        label = "manual adjustment" + ("" if len(adjustments) == 1 else "s")
        lines.append(f"- {len(adjustments)} {label}: {_join_short(descs)}.")

    # Last, and explicitly flagged: these rows are NOT part of `ยอดชำระ`.
    bill_payments = buckets.get("bill-payment", [])
    if bill_payments:
        descs = [
            f"{r['name']} {_fmt_thb(float(r.get('amount') or 0.0))}" for r in bill_payments
        ]
        label = "bill payment" + ("" if len(bill_payments) == 1 else "s")
        lines.append(
            f"- {len(bill_payments)} {label} (excluded from the total): "
            f"{_join_short(descs)}."
        )

    if not lines:
        return None
    return "This cycle includes:\n" + "\n".join(lines)
