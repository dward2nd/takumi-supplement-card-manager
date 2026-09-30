"""Icons for Transactions rows: what kind of row first, then the merchant's category.

deterministic + idempotent — a pure function of the new page's properties.

A row is bookkeeping before it is a merchant: a payment, a cashback credit,
a carry-forward or a points row gets the kind's icon whatever merchant it
names, so a ledger reads at a glance. Kinds follow the tests the bills and
statements already use (`lib.ledger`, `lib.promotions`), so an icon never
contradicts how a script treats the row.
"""

from __future__ import annotations

import re

from .. import ledger, promotions
from .base import CARD, IconRule, PageIcons, emoji, first_match, number_of, title_of
from .merchants import merchant_emoji

_BRACKETS = re.compile(r"^(\[[^\]]*\]\s*)+")


def _cashback(name: str, amount: float) -> bool:
    return ledger.is_cashback_row({"name": name, "amount": amount}) or bool(
        re.search(r"เครดิตเงินคืน|CASH ?BACK|SPECIAL DISCOUNT|INTEREST REBATE", name, re.IGNORECASE))


def _payment(name: str, amount: float) -> bool:
    return ledger.is_bill_payment_row({"name": name, "amount": amount}) or bool(
        re.search(r"ชำระ|จ่าย|PAYMENT THANK YOU|AUTO DEBIT|DIRECT DEBIT|^PAYMENT-", name, re.IGNORECASE))


# Household bookkeeping, recognised by the bracket the row opens with.
_BRACKET_KINDS: tuple[IconRule, ...] = (
    IconRule("↪️", r"^\[(ยอดยกมา|ยกยอดมา)"),   # carry-forward between cycles
    IconRule("⚖️", r"^\[(หักลบหนี้|เว็บรับหนี้)"),  # offsets and debt takeovers
    IconRule("↩️", r"^\[ยกเลิก"),              # cancelled charges
    IconRule("⭐", r"^\[(ปรับคะแนน|คะแนนพิเศษ)"),  # points adjustments and bank bonuses
)

# Kinds recognised by the words in the name, after the bracket kinds.
_NAMED_KINDS: tuple[IconRule, ...] = (
    IconRule("🔄", r"^RESET\b"),                                   # ledger reset
    IconRule("🎁", r"\bPWP\b|แลกคะแนน|แลกแต้ม|REDEEM|CASH REBATE"),  # paid with points
    IconRule("⭐", r"คะแนน|BONUS POINT|^KBANK BONUS"),            # points-only rows
    IconRule("🔁", r"^(โอน|รวมยอด)"),                             # balance moved between ledgers
    IconRule("↩️", r"REFUND|REVERSAL|คืนเงิน"),
    IconRule("🛠️", r"วันตัดรอบบิล|เปิดบัตรใหม่"),                   # cycle and card admin
    IconRule("🧾", r"\bFEE\b|ค่าธรรมเนียม|^INTEREST\b|ดอกเบี้ย"),     # fees and interest
    IconRule("📆", r"\(INST \d+ OF \d+\)|ผ่อน", test=promotions.is_installment),  # an installment term
)


class TransactionIcons(PageIcons):
    def icon(self, properties: dict) -> dict | None:
        return emoji(self.pick(title_of(properties), number_of(properties, "ยอดชำระ") or 0.0))

    @staticmethod
    def pick(name: str, amount: float) -> str:
        name = name.strip()
        if (kind := first_match(_BRACKET_KINDS, name)):
            return kind
        bare = _BRACKETS.sub("", name)   # `[บัตรหลัก] …`, `[แลกคะแนน] …`: read what follows too
        if _cashback(bare, amount):
            return "🤑"
        if (kind := first_match(_NAMED_KINDS, name) or first_match(_NAMED_KINDS, bare)):
            return kind
        if _payment(bare, amount):
            return "💸"
        if (category := merchant_emoji(bare)):
            return "↩️" if amount < 0 else category
        if amount < 0:
            return "↩️"   # an unnamed credit: most likely a merchant refund
        if amount == 0:
            return "⭐"   # a ฿0 row carries points only
        return CARD
