"""UOB EPW538 — "ช้อปออนไลน์ คุ้มทุกคลิก", e-Commerce & e-Wallet, 1 Jul – 30 Sep 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from
https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/e-commerce-e-wallet-epw538-0926.page
(content from its JSON, `…/shopping-lifestyle/e-commerce-e-wallet-epw538-0926.json`)
on 2026-09-28. ฿100 per whole ฿5,000 of eligible spend a month, up to ฿200.

Everything the primary cardholder is billed for pools: every UOB card Takumi
holds (One, World, Premier, Makro) and every supplement on them. The bank
credits the month's total to one of Takumi's UOB cards of its choosing within
60 days after the campaign, so which card the money lands on can't be
predicted; the household split doesn't depend on it.

The ฿600 campaign cap is 3 × the ฿200 monthly cap, so it never binds alone.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .ladder import LadderPromotion, Tranche

STEP = Decimal(5_000)
PER_STEP = Decimal(100)
MONTH_CAP_STEPS = 2

# The apps and wallets the bank names. Anything else doesn't count, however online it is.
_APPS = re.compile(r"SHOPEE|LAZADA|TIKTOK|LINE ?PAY|^LPTH\*|LINE SHOPPING|CENTRAL ?(APP|ONLINE)|"
                   r"KING ?POWER|^TMN[ *]|TRUE ?MONEY")


class EPW538Promotion(LadderPromotion):
    code = "EPW538"
    title = "ช้อปออนไลน์ คุ้มทุกคลิก"
    cards = ("UOB One", "UOB World", "UOB Premier", "UOB Makro")
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))
    source_url = ("https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/"
                  "e-commerce-e-wallet-epw538-0926.page")
    headline = "2%"
    marks_rows = False   # an overlay on each card's own cashback; `% cb` stays the card's

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        counted = min(pooled // STEP, MONTH_CAP_STEPS) * STEP
        return [Tranche(Decimal(0), counted, counted / STEP * PER_STEP)] if counted else []

    def qualifies(self, tx: Tx) -> bool:
        return bool(_APPS.search(tx.merchant))

    ladder_rows: ClassVar = (
        ("under ฿5,000", "nothing"),
        ("every whole ฿5,000", "฿100 — up to ฿200, reached at ฿10,000"),
        ("Cap", "฿200 a month and ฿600 for the campaign, per primary cardholder"),
    )
    inclusions: ClassVar = (
        "Full-amount spend through Shopee, Lazada, TikTok, LINE Pay, LINE Shopping, Central App, "
        "King Power, ShopeePay and TrueMoney.",
        "TrueMoney counts at its partner stores: 7-Eleven, McDonald's, Dairy Queen, Major "
        "Cineplex, TrueCoffee, CP Freshmart, Swensen's, Boots, Caffe Muan Chon, Chester's and "
        "others (not Makro).",
        "Pooled across every UOB card Takumi holds and every supplement on them: the bank sums "
        "the primary cardholder's accounts.",
        "Dated by the transaction (approval) date; cancelled charges are netted out first.",
        "Register once before spending: SMS \"EC <last 12 digits of the card>\" to 4545111, or "
        "Rewards+ in UOB TMRW. UOB Reserve and Infinite don't need to register.",
    )
    rules: ClassVar = (
        Rule("LINE MAN food delivery via LINE Pay, and ShopeeFood via ShopeePay",
             r"LINE ?MAN|_LM_|PF_LM|SHOPEE ?FOOD"),
        Rule("Bill payments, insurance, tax, utilities, Easy Pass",
             r"BILL|INSURANCE|\bAIA\b|\bTAX\b|\b(MEA|PEA|MWA)\b|EASY ?PASS|EXPRESSWAY|ISERVICE"),
        Rule("Fuel paid through any wallet", test=lambda tx: promotions.looks_petrol(tx.merchant)),
        Rule("Makro through TrueMoney", r"MAKRO"),
        Rule("Top-ups into TrueMoney, ShopeePay or LINE Pay wallets", r"TOP ?-?UP"),
        Rule("Installments (only full-amount spend counts)",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Charges cancelled later"),
    )
    crediting: ClassVar = (
        "Within 60 days after 30 Sep 2026, into one of the primary cardholder's UOB cards; the bank "
        "picks which.",
        "When promotions in the same merchant category overlap, the bank pays only the best one.",
    )
