"""Bill-row lookup + explanation on a holder's Bills DB.

deterministic + idempotent — safe to re-run.

Bills uniquely identify by (Card, วันตัดรอบบิล date). `Card` is a relation
to the holder's own Cards DS (since 2026-09-30; before that a SELECT, now
kept as `Card (old select)` — see docs/concepts/known-divergences), so a
card is matched by its Cards page, found by title through `cards.find_card`.
Bill cycle dates are ISO date strings.

All three holders have a Bills DB. Takumi's holds statement-driven bills
(`Holder.statement_bills`); lookups work the same way on it.

`explain_cycle()` produces a one-block Note text summarising the special
rows in a cycle — installment terms, cashback credit rows, and manual
adjustments — so the bill row itself documents *why* the total is what
it is. Used by both /prepare-bill (on draft) and /update-bill (on refresh).
"""

from __future__ import annotations

from collections import defaultdict

from . import installments, notion_client
from .cards import CardAmbiguousError, CardNotFoundError, find_card
from .ledger import is_bill_payment_row, is_cashback_row

# The Bills property that holds the bank statement PDF(s).
STATEMENT_PDF = "ใบแจ้งยอด (PDF)"
# The bill's card: a one-way relation to the holder's own Cards DS (user, 2026-09-30).
CARD = "Card"
# The SELECT it replaced, renamed and kept until the household's views move over.
OLD_CARD_SELECT = "Card (old select)"
# A bill not yet final: drafted from transactions, or a placeholder awaiting the statement.
DRAFT_PREFIX = "[DRAFT] "
from .holders import Holder


def card_relation(card_page_id: str) -> dict:
    """The `Card` property value linking a bill to its Cards page."""
    return {"relation": [{"id": card_page_id}]}


def bill_card_id(page: dict) -> str | None:
    """The Cards page a Bills row links to, or None."""
    rel = (page.get("properties", {}).get(CARD) or {}).get("relation") or []
    return rel[0]["id"] if rel else None


def bills_for(bills_ds: str, card_page_id: str, bill_cycle: str) -> list[dict]:
    """Every Bills row for (card page, วันตัดรอบบิล) — normally zero or one."""
    return notion_client.query_all(bills_ds, filter={"and": [
        {"property": CARD, "relation": {"contains": card_page_id}},
        {"property": "วันตัดรอบบิล", "date": {"equals": bill_cycle}},
    ]})


class BillNotFoundError(RuntimeError):
    pass


class BillAmbiguousError(RuntimeError):
    pass


class BillsNotSupported(RuntimeError):
    pass


def require_bills_ds(holder: Holder) -> str:
    if not holder.bills_ds:
        raise BillsNotSupported(
            f"{holder.key!r} has no Bills database"
        )
    return holder.bills_ds


def find_bill(holder: Holder, card: str, bill_cycle: str) -> dict:
    """Return the single Bills page for (card, bill_cycle) on this holder.

    `card` is the card's title in the holder's Cards DS (case-insensitive
    fallback, as `cards.find_card`). `bill_cycle` is the value of
    `วันตัดรอบบิล` (ISO date).
    """
    ds = require_bills_ds(holder)
    try:
        card_page = find_card(holder.cards_ds, card)
    except (CardNotFoundError, CardAmbiguousError) as e:
        raise BillNotFoundError(f"no bill on {holder.key}'s Bills DB for card={card!r}: {e}") from e
    pages = bills_for(ds, card_page["id"], bill_cycle)
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


# Cashback credits are named under two conventions in the data:
#
#   1. the word CASHBACK somewhere in the name — `Cashback 5%`,
#      `UOB ONE CASHBACK 10%`, `NW2 Cashback 2% (1 พ.ค. - 31 พ.ค.)`,
#      `[บัตรหลัก][Cashback] …`. Used on the UOB / AEON / First Choice cards.
#   2. a `CB` prefix ahead of the merchant or campaign being credited —
#      `CB TMN FAST FOOD BANGKOK THA`, `CB HTTPS://WWW.MAKRO.PRO/ BANGKOK TH`,
#      `CB-025 SHELL-CALTEX NOV 2025`, `CB15_ SUP1 CAMPAIGN 1AUG26-31AUG26`,
#      `CB88_SAV1 Campaign 01JUN26-30JUN26`. Used on Krungsri NOW (where the
#      recording convention is a separate credit row rather than `% cb` — see
#      scripts/repositories/cards/krungsri-now.yaml) and on several of
#      Takumi's cards.
#
def _categorize_row(row: dict) -> str:
    """Tag a transaction row by what it represents in the bill.

    Categories:
      - 'cashback'           — credit row; see `ledger.is_cashback_row` for the two
                               naming conventions it recognizes.
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

    The 'bill-payment' test delegates to `ledger.is_bill_payment_row`, the
    same predicate `/prepare-bill`'s `_sum_cycle` and `/update-bill`'s
    `refresh_from_transactions` use to drop these rows from the sum. Sharing
    the predicate is the point: when the two disagreed, the Note listed the
    payment among the "manual adjustments" that produced `ยอดชำระ` while the
    sum had excluded it, so following the Note's arithmetic landed a reader
    short by exactly the payment amount.
    """
    name = (row.get("name") or "").strip()
    # Ahead of the installment test on purpose: a credit row that names the
    # installment it refunds (`CB … 03/10`) is a cashback credit, not a term.
    if is_cashback_row(row):
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
    if is_bill_payment_row(row):
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
