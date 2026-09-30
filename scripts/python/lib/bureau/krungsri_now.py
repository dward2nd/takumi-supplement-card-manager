"""Krungsri NOW online cashback — ฿25 per whole ฿500 on each online slip, 1 Jan – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.krungsricard.com/th/product/creditcard/now on
2026-09-29 (a card benefit, no registration): "5%" on purchases through a
website or an app, counted per whole ฿500 of each slip (฿718.36 earns ฿25),
at most ฿300 a month. Insurance, funds and travel (hotels, tickets, car rental,
travel agencies), online advertising, QR-code payments and Krungsri Smart Plan
installments don't count. Credited within 5 days of posting — a `CB <merchant>`
line (Baiboon's Makro PRO ฿4,159 → `CB HTTPS://WWW.MAKRO.PRO/ BANGKOK` −฿200,
Sep 2026). The household books that line as a separate row and never sets
`% cb` (scripts/repositories/cards/krungsri-now.yaml); rows that earn it earn
no points (×0).
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .accounts import CardAccount
from .base import UNCERTAIN, Rule, Tx
from .slips import SlipCreditPromotion

BLOCK, PER_BLOCK = Decimal(500), Decimal(25)

_ONLINE = re.compile(r"WWW\.|HTTPS?:|\.COM\b|\.CO\.TH|\.PRO\b|SHOPEE|LAZADA|TIKTOK|2C2P|OMISE|GBPRIME|"
                     r"ANTHROPIC|OPENAI|GOOGLE|APPLE\.COM|NETFLIX|SPOTIFY|YOUTUBE|STEAM|AMAZON|AIS ONLINE")
_TRAVEL_ETC = re.compile(r"AGODA|BOOKING|EXPEDIA|TRAVELOKA|TRIP\.COM|CTRIP|KLOOK|AIR ?ASIA|AIRWAYS|AIRLINES|"
                         r"NOK ?AIR|VIETJET|HOTEL|RESORT|AIRBNB|HERTZ|\bAVIS\b|INSURANCE|ASSURANCE|\bAIA\b|"
                         r"\bFUND\b|FACEBK|FACEBOOK ADS|GOOGLE ADS")


class KrungsriNOWOnline(SlipCreditPromotion):
    code = "NOW"
    icon = "🛍️"
    title = "บัตรเครดิต กรุงศรี นาว แพลทินัม — เครดิตเงินคืน 5% ช้อปออนไลน์"
    campaign = (dt.date(2026, 1, 1), dt.date(2026, 12, 31))
    source_url = "https://www.krungsricard.com/th/product/creditcard/now"
    headline = "5%"
    cap = Decimal(300)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        blocks = tx.amount // BLOCK
        return blocks * PER_BLOCK if blocks else None

    def qualifies(self, tx: Tx) -> bool:
        return self.slip_credit(tx) is not None and bool(_ONLINE.search(tx.merchant)) \
            and not _TRAVEL_ETC.search(tx.merchant) and not promotions.is_installment(tx.name)

    def counts_linked(self, tx: Tx) -> bool:
        return self.slip_credit(tx) is not None   # an online slip the household linked by hand counts

    ladder_title = "Cashback per slip"
    ladder_header = ("Online slip", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿500", "nothing"),
        ("every whole ฿500 on the slip", "฿25 (5%)"),
        ("Cap", "฿300 a month"),
    )
    inclusions: ClassVar = (
        "Purchases through a website or an app on the Krungsri NOW Platinum; no registration.",
        "Per slip: ฿999 earns ฿25, the same as ฿500.",
        "Rows that earn it earn no points (×0).",
        "Online-looking merchants are linked automatically; link any other online slip by hand and "
        "it counts.",
    )
    rules: ClassVar = (
        Rule("Insurance, funds, travel (hotels, tickets, car rental, travel agencies), online "
             "advertising", _TRAVEL_ETC.pattern),
        Rule("QR-code payments", r"^TMN\*?PROMPTPAY|PROMPTPAY|\bQR\b", level=UNCERTAIN,
             hint="QR payments don't count; a TrueMoney or PromptPay row may be one"),
        Rule("Krungsri Smart Plan installments", test=lambda tx: promotions.is_installment(tx.name)),
    )
    crediting: ClassVar = (
        "Within 5 days of the charge posting, as `CB <merchant>`; the household books it as its own row.",
    )


class NOWKrungsriNOW(CardAccount, KrungsriNOWOnline):
    cards = ("Krungsri NOW",)


ACCOUNTS = (NOWKrungsriNOW,)
