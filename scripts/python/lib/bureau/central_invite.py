"""Central The 1 "พิเศษเฉพาะคุณ รับเครดิตเงินคืนสูงสุด 400 บาท*" — by invitation, 16 Nov 2026 – 15 Jan 2027.

deterministic + idempotent — declarations and pure functions only.

Terms typed in by the user on 2026-11-26 from the invitation (UCHOOSE). The
campaign is for invited cardholders only and has no public page: a web search
that day found nothing, which is what an invitation-only offer looks like.
The bank's SMS / UCHOOSE code wasn't given, so the household calls it
"T1 Invite"; rename the Bureau row and trackers if the statement's credit line
shows the bank's code.

  Every whole ฿10,000 of spend accumulated over the whole campaign → ฿200, at
  most ฿400 per primary card account for the campaign (reached at ฿20,000).

One quota for the whole campaign (`2026M11 — T1 Invite cb ฿400`, 16 Nov –
15 Jan), counted by transaction date. Supplement spend pools with the primary
account, so Takumi's Central The 1 Redz rows and Baiboon's (her supplement and
her `[บัตรหลัก]` rows) share it. Only spend after registration is confirmed
counts. UCHOOSE's eligible list started with the 22 Nov THE BARISTRO slips
(user, 2026-11-26), and the card has no spend from 16 to 21 Nov, so the
registration date costs nothing.

The page lists the only exclusions, and spend thresholds are read verbatim:
utilities, funds, insurance (unit-linked included), cash withdrawals and Call
for Cash, cancelled or disputed charges, interest and fees. Makro,
marketplaces, delivery apps, e-wallets and foreign spend all count, unlike
First Choice NW4.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import UNCERTAIN, Rule, Tx
from .ladder import LadderPromotion, Tranche

STEP = Decimal(10_000)
PER_STEP = Decimal(200)
CAP_STEPS = 2   # ฿400 per primary account for the campaign


class CentralInvitePromotion(LadderPromotion):
    code = "T1 Invite"
    icon = "💌"
    title = "พิเศษเฉพาะคุณ รับเครดิตเงินคืนสูงสุด 400 บาท"
    cards = ("Central The 1 Redz",)
    campaign = (dt.date(2026, 11, 16), dt.date(2027, 1, 15))
    source_url = "https://www.centralthe1card.com/th/promotions"   # invitation only: not listed there
    headline = "฿400"

    # Compared on 2026-11-26 with First Choice NW4 (the Krungsri group's own ฿200 per ฿10,000
    # ladder) and with GWSE, the Central The 1 card's own one-off threshold (+฿300 at ฿50,000 at
    # GO Wholesale, 14 Oct – 24 Nov; docs/catalogues/2026-11/the1.md §3.1).
    related: ClassVar = ("NW4", "GWSE")
    changes: ClassVar = (
        "Period: one quota for the whole campaign, 16 Nov 2026 – 15 Jan 2027 (NW4: a ladder per "
        "calendar month; GWSE: one quota for its campaign too).",
        "Ladder: ฿200 for each whole ฿10,000, at most ฿400 for the campaign, reached at ฿20,000 (NW4: "
        "฿50 at ฿5,000–9,999, then ฿200 per ฿10,000 up to ฿2,000 a month; GWSE: ฿300 once at ฿50,000).",
        "What counts: any spend on the card, except utilities, funds, insurance, cash withdrawals and "
        "Call for Cash, cancelled or disputed charges, interest and fees. NW4 also leaves out "
        "marketplaces, delivery apps, travel, Makro (MCC 5199), government, gold, financial services, "
        "foreign spend, subscriptions and e-wallet top-ups, and caps supermarkets and fuel at ฿30,000. "
        "GWSE counts GO Wholesale only and leaves out every e-wallet.",
        "Crediting: within 60 days of the date the merchant bills each charge to the bank, so a step "
        "can pay before the campaign ends (NW4: within 60 days after each month-end; GWSE: within 7 "
        "days after its end).",
        "Who: invited cardholders only (NW4 and GWSE are open to every cardholder who registers). "
        "Registration is the same: UCHOOSE or SMS on or before the spend day, counting only spend "
        "after the confirmation.",
        "Supplement spend pools with the primary account and the credit goes to the primary, as for "
        "NW4 and GWSE.",
    )

    # One quota for the whole campaign: the Bureau row runs 16 Nov – 15 Jan (`2026M11`).
    def period_for(self, tx: Tx) -> tuple[dt.date, dt.date] | None:
        first, last = self.campaign
        return (first, last) if first <= tx.day <= last else None

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        counted = min(pooled // STEP, CAP_STEPS) * STEP
        return [Tranche(Decimal(0), counted, counted / STEP * PER_STEP)] if counted else []

    ladder_title = "Cashback for the campaign"
    ladder_header = ("Spend over the whole campaign", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿10,000", "nothing"),
        ("every whole ฿10,000", "฿200 — at most ฿400 per primary account, reached at ฿20,000"),
    )
    examples: ClassVar = ((9_999, 0), (10_000, 200), (19_999, 200), (20_000, 400), (60_000, 400))
    inclusions: ClassVar = (
        "Spend on the Central The 1 Redz, pooled over the whole campaign (16 Nov 2026 – 15 Jan 2027) "
        "on Takumi's primary account: Baiboon's supplement spend and her `[บัตรหลัก]` rows count with "
        "his. The bank credits the primary account only.",
        "Steps over the campaign, not a smooth 2%: ฿19,999 earns the same ฿200 as ฿10,000.",
        "For invited cardholders only. Register via SMS, or free in UCHOOSE, on or before the spend "
        "day; only spend after the confirmation SMS counts. Takumi was registered by 22 Nov 2026: "
        "UCHOOSE's eligible list starts with that day's THE BARISTRO slips (user, 2026-11-26), and "
        "the card has no spend from 16 to 21 Nov.",
        "Counted at the amount the merchant bills, which can differ from the price paid at the till.",
        "Only the listed exclusions apply. Makro, marketplaces, delivery apps, e-wallet payments "
        "(TMN …), foreign spend and subscriptions all count.",
    )
    rules: ClassVar = (
        Rule("Utilities: electricity, water, landline",
             r"\b(MEA|PEA|MWA|PWA)\b|ELECTRICITY|WATERWORKS|การไฟฟ้า|การประปา"),
        Rule("Funds of every kind", r"\bFUND\b|\bRMF\b|\bSSF\b|ASSET MANAGEMENT|กองทุน"),
        Rule("Insurance of every kind, unit-linked policies included",
             r"INSURANCE|ASSURANCE|\bAIA\b|\bFWD\b|ALLIANZ|UNIT ?LINK|ประกัน"),
        Rule("Cash withdrawals and Central The 1 Call for Cash",
             r"CASH ADVANCE|CALL ?FOR ?CASH|CASH WITHDRAW|เบิกเงินสด|ถอนเงินสด"),
        Rule("Interest and fees of every kind", r"\bFEE\b|INTEREST|LATE CHARGE|PENALTY"),
        Rule("Installment terms (`NN/NN`)", test=lambda tx: promotions.is_installment(tx.name),
             level=UNCERTAIN,
             hint="the page doesn't exclude installments; whether the bank counts the purchase once at "
                  "its full amount or each billed term isn't known"),
        Rule("Charges cancelled or disputed later (a refund nets off its charge)"),
    )
    crediting: ClassVar = (
        "Within 60 days of the date the merchant bills each charge to the bank, into the primary "
        "account (Takumi's Central The 1 Redz); it shows on his statement. A step can pay before the "
        "campaign ends.",
        "Only for an account still open and in good standing when the credit is given. A missing or "
        "wrong credit must be raised with the card centre within 90 days of the end (by 15 Apr 2027).",
    )
