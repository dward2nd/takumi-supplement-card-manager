"""Krungsri Lady's LADY'S FASHIONISTA — 7% per whole ฿2,000 of each slip at seven fashion brands, 1 Jan 2025 – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.krungsricard.com/th/product/creditcard/krungsri-lady
on 2026-10-28 (the "รายละเอียดและเงื่อนไขเพิ่มเติม" panel under LADY'S FASHIONISTA).
A card benefit of Krungsri Lady Titanium only, with no registration:

  "ยอดใช้จ่ายครบทุกๆ 2,000 บาท/เซลล์สลิป จะได้รับเครดิตเงินคืน 7%" at ZARA, H&M,
  JASPAL, Pomelo, SEPHORA, EVEANDBOY and Adidas, in their Thai branches and their
  own online channels, full-amount payments only. Per slip: slips never add up,
  and the remainder under ฿2,000 earns nothing, so a ฿2,735 slip earns ฿140.
  At most ฿560 per primary card account per month, supplements included.
  Credited to the primary account within 7 days after the merchant settles.
  Not combinable with other promotions.

Excluded: ZARA Online, Adidas Online and other online spend the bank can't
track; payment through TrueMoney Wallet, Rabbit LINE Pay or ShopeePay.

"สงวนสิทธิ์ยกเว้นการให้คะแนนสะสมกรุงศรีโบนัส สำหรับรายการใช้จ่ายที่เข้าเงื่อนไขได้รับเครดิตเงินคืน"
— no Krungsri Bonus points on spend that earns the cashback. Only slips of
฿2,000 or more earn it, so a merchant-prefix exclusion in the card YAML would
also zero a ฿1,500 slip. Instead `expected` ticks `×0` on each linked slip that
gets a credit, and `suggested_note` says why.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import Any, ClassVar

from .. import promotions
from .accounts import CardAccount
from .base import Rule, Tx, TxCredit
from .slips import SlipCreditPromotion

STEP = Decimal(2000)
PER_STEP = Decimal(140)   # 7% of ฿2,000
SOURCE = "https://www.krungsricard.com/th/product/creditcard/krungsri-lady"

# Statement names seen so far: `EVEANDBOY-MAYA CHIANGM CHIANGMAI TH`. The others are the brands as printed.
_BRANDS = re.compile(r"EVE ?AND ?BOY|\bZARA\b|\bH ?& ?M\b|\bJASPAL\b|\bPOMELO\b|\bSEPHORA\b|\bADIDAS\b")
_POINTS_NOTE = ("LADY'S FASHIONISTA: 7% cashback per whole ฿2,000 of the slip — Krungsri gives no "
                "Krungsri Bonus points on spend that earns it.")


class LadyFashionistaPromotion(SlipCreditPromotion):
    code = "Fashionista"
    icon = "👗"
    title = "LADY'S FASHIONISTA — เครดิตเงินคืน 7% ทุกยอด 2,000 บาท/เซลล์สลิป"
    campaign = (dt.date(2025, 1, 1), dt.date(2026, 12, 31))
    source_url = SOURCE
    headline = "7%"
    cap = Decimal(560)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        steps = int(tx.amount // STEP) if _BRANDS.search(tx.merchant) else 0
        return steps * PER_STEP if steps else None

    def expected(self, r: TxCredit) -> dict[str, Any]:
        # `% cb` stays unset as on every Krungsri row; the points go when the slip earns.
        return {"multiplier": "×0"} if r.credit > 0 else {}

    def suggested_note(self, r: TxCredit) -> str | None:
        return _POINTS_NOTE if r.credit > 0 else None

    ladder_title = "Cashback per slip"
    ladder_header = ("Fashion slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿2,000", "nothing"),
        ("every whole ฿2,000 on the slip", "฿140 (7%)"),
        ("Cap", "฿560 a calendar month per primary card account"),
    )
    inclusions: ClassVar = (
        "Krungsri Lady Titanium only. No registration.",
        "ZARA, H&M, JASPAL, Pomelo, SEPHORA, EVEANDBOY and Adidas: their Thai branches and "
        "their own online channels, in baht, full-amount payments only.",
        "Per slip: ฿3,999 earns ฿140, the same as ฿2,000. Slips never add up.",
        "Per calendar month, supplements included; the bank credits the primary account.",
        "No Krungsri Bonus points on spend that earns the cashback: such rows are ×0.",
    )
    rules: ClassVar = (
        Rule("ZARA Online / Adidas Online", r"ZARA ?ONLINE|ZARA\.COM|WWW\.ZARA|ADIDAS ?ONLINE|ADIDAS\.CO|WWW\.ADIDAS"),
        Rule("Paid through an e-wallet (TrueMoney, Rabbit LINE Pay, ShopeePay)",
             r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*|SHOPEEPAY"),
        Rule("Not a full-amount payment (installment)", test=lambda tx: promotions.is_installment(tx.name)),
    )
    crediting: ClassVar = (
        "Within 7 days after the merchant settles the slip, to the primary card account.",
        "Not combinable with other promotions.",
    )


class LadyFashionistaKrungsriLady(CardAccount, LadyFashionistaPromotion):
    cards = ("Krungsri Lady",)


ACCOUNTS = (LadyFashionistaKrungsriLady,)
