"""UOB One cashback — two quotas: 10%/5% per calendar month, 1% per statement cycle.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.uob.co.th/personal/credit-cards/cash-back/one-cash-back-credit-card.page
on 2026-09-28:

  10% — BTS via LINE Pay or Rabbit Rewards packages, MRT Blue & Purple lines
        (tap-to-pay at the gate), Café Amazon
   5% — 7-Eleven and ALL ONLINE, Grab, Watsons (and Watsons online)
        ฿500 of credit a month for 10% and 5% together, counted by post date,
        credited on the last day of the month
   1% — everything else not excluded; ฿2,000 a statement cycle, credited in
        the cycle

Two caps, two periods, so the Bureau keeps two rows a month:
`2026M9 — UOB One cb 10%/5%` (1–30 Sep) and `2026M9 — UOB One cb 1%` (the
cycle closing 25 Sep). Both caps are shared by everyone on the account and
split first come, first served (user, 2026-09-28).

Which tier a row falls in is not decided here: it comes from the card's
promotion YAML (`scripts/repositories/promotions/uob-one-2026.yaml`) through
`lib.promotions.classify`, the same classifier /add-transaction uses. This
module adds only what the classifier can't see: the pooled caps.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .capped import CreditCapPromotion

# Makro in-store earns nothing on UOB One (bank's 1% exclusion list); the YAML's
# catch-all 1% tier doesn't know that. Makro PRO online (`MAKRO.PRO`) earns.
_MAKRO_IN_STORE = re.compile(r"^MAKRO_")


class _UOBOne(CreditCapPromotion):
    code = "UOB One"
    title = "UOB One cashback"
    cards = ("UOB One",)
    campaign = (dt.date(2026, 1, 1), dt.date(2026, 12, 31))  # uob-one-2026.yaml
    source_url = "https://www.uob.co.th/personal/credit-cards/cash-back/one-cash-back-credit-card.page"
    tiers: ClassVar[frozenset[Decimal]]

    ladder_title = "Cashback tiers"
    ladder_header = ("Where", "Cashback")

    def rate(self, tx: Tx) -> Decimal | None:
        if _MAKRO_IN_STORE.match(tx.merchant):
            return None
        c = promotions.classify(self.cards[0], tx.day, tx.name)
        rate = None if c.cashback_percent is None else Decimal(str(c.cashback_percent))
        return rate if rate in self.tiers else None


class UOBOneBonus(_UOBOne):
    name_pattern = r"\bUOB One cb 10%/5%"
    headline = "10%/5%"
    tiers = frozenset({Decimal("0.1"), Decimal("0.05")})
    cap = Decimal(500)

    ladder_rows = (
        ("BTS via LINE Pay or Rabbit Rewards packages; MRT Blue & Purple (tap-to-pay at the gate); "
         "Café Amazon", "10%"),
        ("7-Eleven and ALL ONLINE; Grab; Watsons and Watsons online", "5%"),
        ("Cap", "฿500 a calendar month, 10% and 5% together, per account"),
    )
    inclusions = (
        "Counted per calendar month by the bank's post date; Notion uses Transaction Datetime, "
        "so a charge posted a day or two later can land in the next month.",
        "Paying through an e-wallet earns 1%, not these tiers (BTS via LINE Pay is the exception). "
        "TrueMoney at 7-Eleven (TMN 7-11) is therefore 1%.",
        "Everyone on the account shares the ฿500 (Takumi's card and the supplements).",
    )
    rules = (
        Rule("Utility bills (MCC 4900) and top-ups into an e-wallet — no cashback at all since 1 Jan 2025"),
        Rule("Refunds in the same month are deducted from the month's cashback"),
    )
    crediting = (
        "On the last day of each month (next working day if it's a holiday), for the month's spend.",
        "Spend posted on the last day of the month is counted in the next month.",
    )


class UOBOneBase(_UOBOne):
    name_pattern = r"\bUOB One cb 1%(?!\d)"
    headline = "1%"
    period_basis = "bill_cycle"
    tiers = frozenset({Decimal("0.01")})
    cap = Decimal(2_000)

    ladder_rows = (
        ("Everything else that isn't excluded, including e-wallet payments and each billed "
         "installment term", "1%"),
        ("Cap", "฿2,000 a statement cycle, per account"),
    )
    inclusions = (
        "Counted per statement cycle: rows whose Bill Cycle Date is the cycle's close.",
        "Everyone on the account shares the ฿2,000 (Takumi's card and the supplements).",
        "UOB PayAnything earns 1% on up to ฿100,000 a cycle; UOB Pay Bills earns 1% (except "
        "MEA/PEA electricity and MWA water).",
    )
    rules = (
        Rule("Funds, unit-linked insurance, unbilled installment balances, cash advances, "
             "Fund Transfer, currency exchange"),
        Rule("Petrol stations and Makro in-store (Makro PRO online still earns)"),
        Rule("MEA/PEA electricity and MWA water bills; utility bills and anything under MCC 4900; "
             "top-ups into an e-wallet"),
        Rule("Baht charges at foreign merchants or foreign-registered sites"),
        Rule("Interest, fees and penalties; cancelled charges; business spend; spend over twice "
             "the credit limit; UOB i-Plan at participating schools"),
    )
    crediting = (
        "Within the statement cycle, on the statement.",
        "Spend posted on the statement date is counted in the next cycle.",
        "Refunds in the same cycle are deducted; a refund in a later cycle comes off that cycle's "
        "cashback.",
    )
