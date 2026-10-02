"""UOB World ×5 — bonus points on the first ฿20,000 of each statement cycle.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.uob.co.th/personal/credit-cards/rewards/uob-world-credit-card.page
on 2026-09-28: 5 UOB Rewards points per ฿25 (×5) on online (card-network
e-commerce), e-wallet, dining, travel and foreign-currency spend, up to
฿20,000 a cycle; past that, and on everything else, 2 per ฿25 (×2).

The household's reading (user, 2026-09-28): the ฿20,000 counts *every*
transaction on the account (Takumi's principal and Baiboon's supplement),
bonus category or not, excluded or not. The bank's page words it as a cap on
bonus-category spend; the household's observation wins.

A points campaign, so no baht shares and no tracker rows: what the split
decides is each row's multiplier. Conventions already in the ledger:

  - a bonus row wholly past the quota: ×2, Note `ได้คะแนน 2 เท่าเพราะเต็มโควต้า 20k แล้ว`
  - the row the quota ends in keeps ×5 and gives back the over-quota part's
    extra points through `ใช้คะแนน` (points used): ⌊over × (5 − 2) / 25⌋.
    RYOTA SHABU, Apr 2026: ฿729.55 over → 87 points.

Which rows are bonus-category can't always be read off the merchant string
(dining especially), so `category()` decides only what it can and otherwise
trusts how the household marked the row.
"""

from __future__ import annotations

import datetime as dt
import math
import re
from decimal import Decimal
from typing import Any

from .. import promotions
from .base import POINTS, BasePromotion, Rule, Tx, TxCredit

QUOTA = Decimal(20_000)
PER_POINT_UNIT = Decimal(25)   # baht per point unit
BONUS, BASE = 5, 2
BONUS_MARK, BASE_MARK, ZERO_MARK = "×5", "×2", "×0"

_ZERO = re.compile(r"^MAKRO_|\b(MEA|PEA|MWA)\b")              # Makro in-store, utility bills
_BONUS = re.compile(r"^TMN[ *]|LINE ?PAY|^LPTH\*|SHOPEE|LAZADA|TIKTOK|TRUE ?MONEY|GRAB|RABBIT")
_BASE = re.compile(r"LOTUS|BIG ?C\b|TOPS\b|RIMPING|VILLA|GOURMET|MAX ?VALU|FOODLAND|CP FRESH|"
                   r"CLINIC|DENT|HOSPITAL|PHARMA")
_FX_NOTE = re.compile(r"\b(USD|JPY|CNY|EUR|SGD|HKD|KRW|TWD|GBP|AUD|MYR|VND|MOP|CHF)\b")
_QUOTA_NOTE = re.compile(r"โควต้า|quota", re.I)


class UOBWorldBonus(BasePromotion):
    code = "UOB World"
    name_pattern = r"\bUOB World ×5\b"
    title = "UOB World ×5 UOB Rewards points"
    cards = ("UOB World",)
    campaign = (dt.date(2025, 1, 1), None)   # promotions/uob-world-points.yaml: standing
    source_url = "https://www.uob.co.th/personal/credit-cards/rewards/uob-world-credit-card.page"
    headline = "×5"
    reward = POINTS
    icon = "📈"
    period_basis = "bill_cycle"

    ladder_title = "Points"
    ladder_header = ("Spend in the statement cycle", "Points per ฿25")
    ladder_rows = (
        ("Online (card-network e-commerce), e-wallet, dining, travel, foreign currency — inside "
         "the first ฿20,000 of the cycle", "5 (×5)"),
        ("The same categories past ฿20,000", "2 (×2)"),
        ("Everything else; supermarkets (MCC 5411) up to ฿100,000 a cycle", "2 (×2)"),
        ("Excluded spend (below)", "0 (×0)"),
    )
    inclusions = (
        "The ฿20,000 counts every transaction on the account, bonus category or not, excluded or "
        "not: Takumi's principal card and Baiboon's supplement together.",
        "Online means what Mastercard/Visa classify as e-commerce. UOB i-Plan installments in the "
        "bonus categories earn ×2.",
        "Points on spend posted on the statement date appear on the next statement.",
    )
    rules = (
        Rule("Petrol stations, Makro in-store, MEA/PEA electricity and MWA water, utility bills "
             "(MCC 4900)"),
        Rule("Top-ups into an e-wallet (`… (TOP` on the statement)",
             test=lambda tx: promotions.looks_wallet_top_up(tx.merchant)),
        Rule("Baht charges at foreign merchants or foreign-registered sites"),
        Rule("Funds, unit-linked insurance, unbilled installments, cash advances, Fund Transfer, "
             "currency exchange, interest and fees, cancelled charges, business spend"),
    )
    crediting = (
        "Points appear on the statement for the cycle; UOB PayAnything earns ×2 on up to "
        "฿100,000 a cycle.",
    )
    split_text = (
        "Every row on UOB World counts toward the ฿20,000, first come, first served by "
        "Transaction Datetime.",
        "A bonus-category row inside the ฿20,000 is ×5. One wholly past it is ×2, noted "
        "ได้คะแนน 2 เท่าเพราะเต็มโควต้า 20k แล้ว.",
        "The row the ฿20,000 ends in keeps ×5 and gives back the extra points on its over-quota "
        "part through ใช้คะแนน: ⌊over × 3 / 25⌋.",
    )

    def split(self, txs: list[Tx]):
        def take(lo: Decimal, hi: Decimal, grp: list[Tx]) -> list[TxCredit]:
            inside = max(min(hi, QUOTA) - lo, Decimal(0))
            size = hi - lo
            return [TxCredit(t, inside * t.amount / size, Decimal(0)) for t in grp]

        rows, boundary, warnings = self._walk([t for t in txs if t.is_card_purchase], take)
        return self._allocation(rows, boundary, warnings, credit=Decimal(0))

    # -- per-row expectations -----------------------------------------------

    def category(self, tx: Tx) -> str | None:
        """'bonus', 'base' or 'zero' when the merchant string settles it, else None."""
        m = tx.merchant
        if promotions.looks_petrol(m) or promotions.looks_wallet_top_up(m) or _ZERO.search(m):
            return "zero"
        if promotions.looks_foreign_in_thb(m):
            return "bonus" if _FX_NOTE.search(tx.note) else "zero"   # real FX vs baht-at-foreign
        if _BONUS.search(m):
            return "bonus"
        if _BASE.search(m):
            return "base"
        return None

    def _as_marked(self, tx: Tx) -> str:
        """The household's own call, read back from the row."""
        if tx.multiplier == BONUS_MARK or (tx.multiplier == BASE_MARK and _QUOTA_NOTE.search(tx.note)):
            return "bonus"
        return "zero" if tx.multiplier == ZERO_MARK else "base"

    def expected(self, r: TxCredit) -> dict[str, Any]:
        kind = self.category(r.tx) or self._as_marked(r.tx)
        if kind == "zero":
            return {"multiplier": ZERO_MARK}
        if kind == "base":
            return {"multiplier": BASE_MARK}
        if r.counted <= 0:
            return {"multiplier": BASE_MARK, "points_redeemed": None}
        return {"multiplier": BONUS_MARK, "points_redeemed": self._give_back(r) or None}

    def _give_back(self, r: TxCredit) -> int:
        over = r.tx.amount - r.counted
        return math.floor(over * (BONUS - BASE) / PER_POINT_UNIT) if over > 0 else 0

    def suggested_note(self, r: TxCredit) -> str | None:
        if (self.category(r.tx) or self._as_marked(r.tx)) != "bonus":
            return None
        if r.counted <= 0:
            return "ได้คะแนน 2 เท่าเพราะเต็มโควต้า 20k แล้ว"
        if r.counted < r.tx.amount:
            return (f"ยอดเกินมาจาก quota 20k เป็นจำนวน {r.tx.amount - r.counted:,.2f} บาท "
                    f"เหลือยอดที่ได้ 5 เท่า {r.counted:,.2f} บาท จึงทดไป {self._give_back(r)} คะแนน"
                    f"เพื่อสะท้อนส่วนที่ได้ 2 เท่า")
        return None
