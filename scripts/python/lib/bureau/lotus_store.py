"""Lotus's LAN — "ช้อปโลตัส รับคืนซูเปอร์คุ้ม", every Lotus's branch and Lotus's Shop Online, 1 Oct – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.lotussmoney.com/promotion/credit-card/shopping/lotuss-shopping-online
on 2026-10-05. Pooled monthly spend at Lotus's, paid by EDC, tap or UCHOOSE QR
(no e-wallet of any kind), pays for the **single highest tier reached only**
("สงวนสิทธิ์การให้เครดิตเงินคืนเพียงระดับสูงสุดเพียงระดับเดียวเท่านั้น"): ฿40 per whole
฿2,000 (at most ฿200), or ฿300 per whole ฿20,000 (at most ฿600). So ฿19,999 earns
฿200 and ฿20,000 earns ฿300. Capped at ฿600 a month and ฿1,800 for the campaign
per primary account, which three full months reach exactly. Takumi registered
on or before 2 Oct 2026 (user, 2026-10-05).

The ledger only sees Takumi's and Baiboon's spend: the untracked supplement
…6524 counts toward the same pool but sits in Takumi's ledger as one
`โอนยอดจากบัตรเสริม` lump, so the bank can pay a higher tier than this split.
Lotus's rows keep `% cb` unset, so this writes the Bureau and the trackers only,
like LBS3.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .ladder import LadderPromotion, Tranche

SMALL_STEP, SMALL_PAY, SMALL_STEPS = Decimal(2_000), Decimal(40), 5
BIG_FROM = BIG_STEP = Decimal(20_000)
BIG_PAY, BIG_STEPS = Decimal(300), 2

# A Lotus's branch posts as `LOTUS'S <branch> …` (Baiboon's ledger has a curly
# `LOTUS’S`). How Lotus's Shop Online posts isn't in any ledger yet.
_LOTUSS = re.compile(r"LOTUS['’]?S|LOTUSS\.COM")
_AT_LOTUSS = re.compile(r"^LOTUS['’]?S\b|^LOTUSS\.COM")
_WALLET = r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*|SHOPEEPAY|RABBIT"


class LANPromotion(LadderPromotion):
    code = "LAN"
    icon = "🛒"
    title = "ช้อปโลตัส รับคืนซูเปอร์คุ้ม"
    cards = ("Lotus's Beyond",)
    campaign = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
    source_url = "https://www.lotussmoney.com/promotion/credit-card/shopping/lotuss-shopping-online"
    headline = "2%"
    marks_rows = False   # Lotus's rows keep `% cb` unset; the money is in the trackers

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        if pooled >= BIG_FROM:
            steps = min(int(pooled // BIG_STEP), BIG_STEPS)
            return [Tranche(Decimal(0), steps * BIG_STEP, steps * BIG_PAY)]
        steps = min(int(pooled // SMALL_STEP), SMALL_STEPS)
        return [Tranche(Decimal(0), steps * SMALL_STEP, steps * SMALL_PAY)] if steps else []

    def qualifies(self, tx: Tx) -> bool:
        return bool(_LOTUSS.search(tx.merchant))

    ladder_rows: ClassVar = (
        ("under ฿2,000", "nothing"),
        ("every whole ฿2,000, while under ฿20,000", "฿40 — up to ฿200"),
        ("or every whole ฿20,000, from ฿20,000", "฿300 — up to ฿600, the monthly cap"),
    )
    inclusions: ClassVar = (
        "Only the single highest tier reached pays (\"เพียงระดับสูงสุดเพียงระดับเดียวเท่านั้น\").",
        "Every Lotus's branch and Lotus's Shop Online, in Thailand, paid by EDC, tap or UCHOOSE QR; "
        "no e-wallet of any kind.",
        "Settled spend only, as billed on the statement; cancelled or returned spend is taken back out.",
        "Pooled per calendar month on the primary account (Takumi's); supplements count, and their "
        "credit goes to the primary account. The untracked supplement …6524 counts too, so the bank "
        "can pay a higher tier than the linked rows reach.",
        "Only spend from the registration day on counts: UCHOOSE → \"LAN\", or SMS \"LAN <16-digit "
        "card no.>\" to 081-250-7777. Once for the campaign. Takumi registered on or before 2 Oct 2026.",
        "Cards approved from 1 Aug 2026 on can't join.",
    )
    rules: ClassVar = (
        Rule("Paid through an e-wallet (TMN*LOTUS HYPER, TMN LOTUS …)", _WALLET),
        Rule("Shops renting space and food courts inside Lotus's malls",
             test=lambda tx: not _AT_LOTUSS.search(tx.merchant)),
        Rule("Installments, including each billed term", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Lotus's abroad", test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
        Rule("Lotus's goods bought through another platform (Shopee, Lazada, Grab, LINE MAN …)"),
        # The bank takes these items out of a slip; the ledger only sees the slip's total.
        Rule("Gift baskets, alcohol, cigarettes and infant formula (stages 1 and 2) inside a slip"),
        Rule("Utility bills, mutual funds, insurance, cash advances, balance transfers, fees and interest"),
    )
    crediting: ClassVar = (
        "Within 60 days after each month-end, on the primary account's statement: October's by "
        "December, November's by January 2027, December's by February 2027.",
        "Caps: ฿600 a month and ฿1,800 for the campaign, per primary account.",
    )


PROMOTIONS = (LANPromotion,)
