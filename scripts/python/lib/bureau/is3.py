"""Krungsri First Choice IS3 — insurance premiums, per slip, 1 Jul – 30 Sep 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.firstchoice.co.th/promotion/insurance-credit-card
on 2026-09-29. Each insurance slip earns on its own, by its size band:
฿10,000–99,999 pays ฿80 per whole ฿10,000 (0.8%), ฿100,000–199,999 pays ฿100
per whole ฿10,000 (1%), and ฿200,000 or more pays ฿1,000 per whole ฿100,000.
What a month's slips earn is capped at ฿5,000 per primary account; the
฿15,000 campaign cap is 3 × ฿5,000, so it never binds on its own. The bank
credits it straight after the transaction. IS3 spend can't also count toward
NW3, which already leaves insurance out.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .slips import SlipCreditPromotion

_INSURANCE = re.compile(r"INSURANCE|ASSURANCE|INSURE|\bLIFE\b|ALLIANZ|\bFWD\b|TOKIO|VIRIYAH|DHIPAYA|"
                        r"MUANG ?THAI|THAI ?LIFE|BANGKOK ?LIFE|KRUNGTHAI-AXA|\bAXA\b|CHUBB|GENERALI|"
                        r"SOMPO|MSIG|ประกัน")


def _step_credit(amount: Decimal) -> Decimal | None:
    if amount < 10_000:
        return None
    if amount < 100_000:
        return amount // 10_000 * 80
    if amount < 200_000:
        return amount // 10_000 * 100
    return amount // 100_000 * 1_000


class IS3Promotion(SlipCreditPromotion):
    code = "IS3"
    icon = "🛡️"
    title = "ชำระค่าเบี้ยประกันทุกหมวด รับเครดิตเงินคืน"
    cards = ("First Choice",)
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))
    source_url = "https://www.firstchoice.co.th/promotion/insurance-credit-card"
    headline = "0.8–1%"
    cap = Decimal(5_000)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _INSURANCE.search(tx.merchant):
            return None
        return _step_credit(tx.amount)

    ladder_title = "Cashback per slip"
    ladder_header = ("Insurance slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿10,000", "nothing"),
        ("฿10,000 – 99,999", "฿80 per whole ฿10,000 (0.8%)"),
        ("฿100,000 – 199,999", "฿100 per whole ฿10,000 (1%)"),
        ("฿200,000 or more", "฿1,000 per whole ฿100,000 (1%)"),
        ("Cap", "฿5,000 a month and ฿15,000 for the campaign, per primary account"),
    )
    inclusions: ClassVar = (
        "Full-amount baht premiums of any kind — life (savings or pension), health, accident, car, "
        "home, travel, pet — first year or renewal, on the Krungsri First Choice Visa Platinum.",
        "Per slip: slips never add up. Dated by the transaction date.",
        "Supplements count toward the primary account (Takumi's), which the bank credits.",
        "Counts only after registration is confirmed, strictly before the spend: UCHOOSE → \"IS3\", "
        "or SMS \"IS3 <16-digit card no.>\" to 081-256-3333.",
    )
    rules: ClassVar = (
        Rule("Investment-linked life insurance (Unit Linked)", r"UNIT ?LINK"),
        Rule("AIA, every kind", r"\bAIA\b"),
        Rule("Through Krungsri General Insurance Broker (KGIB), Lotus's General Insurance Broker "
             "(LGIB) or Lotus's Life Assurance Broker (LLAB)", r"\bKGIB\b|\bLGIB\b|\bLLAB\b|KRUNGSRI GENERAL|"
             r"LOTUS'?S? (GENERAL|LIFE)"),
        Rule("Insurers registered abroad", test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
        # U PLAN takes the points only; the slip still counts (user, 2026-10-03).
        Rule("Installment terms (`NN/NN`): the slip is the full-amount charge. One later converted through "
             "U PLAN still counts, once, as that slip; a merchant installment on the personal-loan line "
             "never does", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Charges cancelled later"),
    )
    crediting: ClassVar = (
        "Straight after the transaction, to the primary account; it shows on the monthly statement.",
    )
