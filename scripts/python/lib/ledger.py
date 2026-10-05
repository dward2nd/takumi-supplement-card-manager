"""Ledger — the Transactions-DB reads and row tests several skills share.

deterministic + idempotent — reads and pure tests only.

One copy each of what used to be repeated across bill drafting, bill refresh,
payments, statement recording, auditing and crediting: a cycle's rows, its
amount due, whether a row is a payment or a cashback credit, a page's title.
"""

from __future__ import annotations

import re

from . import notion_client
from .transaction_read import project_transaction

# The household prefix on a friend's share of a charge on Takumi's primary card.
PRIMARY_PREFIX = "[บัตรหลัก]"

# Thai verbs that open every bill-payment row name in the data: ชำระ ("settle")
# and จ่าย ("pay"). Observed variants include ชำระบิลเต็มจำนวน, ชำระเต็มจำนวน,
# ชำระบิลล่วงหน้า, ชำระบางส่วน, ชำระบิลบางส่วน, ชำระล่วงหน้า,
# ชำระล่วงหน้าบางส่วน, ชำระเพิ่มบางส่วนจนครบ, ชำระเต็มจำนวนอย่างล่าช้า,
# จ่ายเต็มจำนวน, จ่ายบิลเต็มจำนวน, จ่ายก่อนบิลมา, จ่ายบิลล่วงหน้าบางส่วน,
# จ่ายส่วนขาดเพิ่มเติม. No non-payment row in the data starts with either.
# `AUTO DEBIT` is Takumi's bank-side auto-debit row (the Krungsri family pays
# that way; his 2025 UOB rows read `AUTO DEBIT - <card>`). Only his ledger
# carries it.
_PAYMENT_NAME_PREFIXES: tuple[str, ...] = ("ชำระ", "จ่าย", "AUTO DEBIT")

# The separator after `CB` varies — a space, a hyphen before a batch number, or
# a digit opening a campaign code — so this is a character class rather than a
# `startswith("CB ")`.
_CB_PREFIX_RE = re.compile(r"^CB[\s\-_0-9]")

# The household's line for a charge the merchant cancelled: `[ยกเลิก] <merchant>`,
# or `[ยกเลิกรายการใช้จ่าย] <merchant>` on the 2025 rows.
CANCELLED_PREFIX_RE = re.compile(r"^\[ยกเลิก[^\]]*\]\s*")

# Bank credits under a Latin name that no merchant gave back: rebates and
# discounts (`CASH REBATE 1 POINTS`, `BANGCHAK SPECIAL DISCOUNT OF 2 %`), a typo'd
# campaign credit (`CP12_BC3P CAMPAIGN …`), adjustments, payments, points
# redemptions (`PWP: …`), interest, the ledger reset, and Krungsri's reversal of a
# charge re-split into installments on the card line (`REV-FC PLAN ON DEMAND: …`,
# U PLAN): the charge still happened and the bank's spend campaigns still count it
# (user, 2026-10-03). Cashback has its own test.
_BANK_CREDIT_RE = re.compile(
    r"REBATE|SPECIAL DISCOUNT|^CP\d+_|ADJUSTMENT|^PAYMENT\b|PAYMENT THANK YOU|DIRECT DEBIT|"
    r"\bPWP\b|^INTEREST\b|^RESET\b|^REV-\w+ PLAN ON DEMAND\b")


def title_text(page: dict) -> str:
    """A page's title, whatever its title property is called."""
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(t.get("plain_text", "") for t in prop.get("title", []) or [])
    return ""


def cycle_pages(transactions_ds: str, card_page_id: str, bill_cycle: str) -> list[dict]:
    """Every raw transaction page on (Card, Bill Cycle Date)."""
    return notion_client.query_all(transactions_ds, filter={"and": [
        {"property": "Card", "relation": {"contains": card_page_id}},
        {"property": "Bill Cycle Date", "date": {"equals": bill_cycle}},
    ]})


def cycle_rows(transactions_ds: str, card_page_id: str, bill_cycle: str) -> list[dict]:
    """Every projected transaction row on (Card, Bill Cycle Date)."""
    return [project_transaction(p) for p in cycle_pages(transactions_ds, card_page_id, bill_cycle)]


def card_rows(transactions_ds: str, card_page_id: str) -> list[dict]:
    """Every projected transaction row on a card — its whole history, which is what
    the card's `ยอดค้างชำระ` / `คะแนนสะสม` rollups sum."""
    return [project_transaction(p) for p in notion_client.query_all(
        transactions_ds, filter={"property": "Card", "relation": {"contains": card_page_id}})]


def is_bill_payment_row(row: dict) -> bool:
    """True if a projected row is a *bill payment* — STRICT, for bill totals.

    A bill's `ยอดชำระ` is the cycle's **amount due**, so drafting and refreshing
    a bill exclude these rows from the sum. Without that the total silently
    nets its own payment and becomes order-dependent: the same cycle would read
    388.10 or 152.00 depending only on whether the payment was recorded before
    or after the bill was drafted.

    Matches on the Thai payment-verb prefix rather than "negative and not
    obviously something else" (see `payments.is_payment_row`, which is too
    loose for this job). Everything that genuinely changes what is owed keeps
    counting: cashback credits (`Cashback …`, `CB …`, `UOB ONE CASHBACK …`),
    merchant refunds, `[ยกเลิก]` cancellations, `[เว็บรับหนี้…]` takeovers and
    `[ยอดยกมา…]` carry-forwards.
    """
    if (row.get("amount") or 0.0) >= 0:
        return False
    return (row.get("name") or "").strip().startswith(_PAYMENT_NAME_PREFIXES)


def amount_due(rows: list[dict]) -> float:
    """A cycle's amount due: Σ `ยอดชำระ` over its projected rows, payments excluded."""
    return round(sum(float(r.get("amount") or 0.0) for r in rows if not is_bill_payment_row(r)), 2)


def is_cashback_row(row: dict) -> bool:
    """True when a projected row is a cashback credit under either naming convention.

    The `CB`-prefix branch also requires a **negative** amount. `CB` is only
    two letters and could plausibly open a real merchant string, and every
    cashback row in all three holders' data is a credit — so the sign costs
    nothing and keeps a hypothetical `CB…` merchant out.

    The CASHBACK-substring branch is deliberately sign-agnostic: it is specific
    enough on its own, and a positive `Cashback …` row (a clawback of
    previously-credited cashback) still belongs here.
    """
    name = (row.get("name") or "").strip().upper()
    if "CASHBACK" in name:
        return True
    return bool(_CB_PREFIX_RE.match(name)) and (row.get("amount") or 0.0) < 0


def is_refund_row(row: dict) -> bool:
    """True when a projected row is a merchant refund: money given back for a charge.

    Either a negative row under the bank's merchant string
    (`UNIONPAY MERCHANT BEIJING CHN`, `WWW.GRAB.COM BANGKOK TH`), `[บัตรหลัก]`
    included, or the household's cancellation line `[ยกเลิก] <merchant>`.
    Cashback credits, payments, points redemptions, interest, adjustments and
    every other `[…]` or Thai-named ledger entry aren't refunds.
    """
    amount = row.get("amount") or 0.0
    name = (row.get("name") or "").strip().removeprefix(PRIMARY_PREFIX).strip()
    if amount >= 0 or not name:
        return False
    if CANCELLED_PREFIX_RE.match(name):
        return True
    if name.startswith("[") or re.match(r"[฀-๿]", name):
        return False
    upper = name.upper()
    return not (is_cashback_row({"name": upper, "amount": amount}) or re.search(r"CASH ?BACK", upper)
                or upper.startswith(_PAYMENT_NAME_PREFIXES) or _BANK_CREDIT_RE.search(upper))
