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
split first come, first served (user, 2026-09-28). Once the ฿500 is used up,
the month's remaining 10%/5% spend earns 1% instead (user, 2026-09-28): such
a row is marked `% cb` 1%, and the 1% quota counts it from that mark.

Which tier a row falls in is not decided here: it comes from the card's
promotion YAML (`scripts/repositories/promotions/uob-one-2026.yaml`) through
`lib.promotions.classify`, the same classifier /add-transaction uses. This
module adds only what the classifier can't see: the pooled caps.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import Any, ClassVar

from .. import promotions
from .base import Rule, Tx, TxCredit
from .capped import CreditCapPromotion

# Makro in-store earns nothing on UOB One (bank's 1% exclusion list); the YAML's
# catch-all 1% tier doesn't know that. Makro PRO online (`MAKRO.PRO`) earns.
_MAKRO_IN_STORE = re.compile(r"^MAKRO_")
BASE_RATE = Decimal("0.01")


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
        tier = self._tier(tx)
        return tier if tier in self.tiers else None

    def _tier(self, tx: Tx) -> Decimal | None:
        c = promotions.classify(self.cards[0], tx.day, tx.name)
        return None if c.cashback_percent is None else Decimal(str(c.cashback_percent))

    def adjustment_for(self, holder: str, adjustments: list[Tx]) -> Decimal:
        """A carry-forward leg carrying `% cb` in this quota's tiers moves cashback
        between periods: e.g. Nuta's `[ยอดยกมาจากรอบ 2026-08]` −฿231 at 1%, whose
        ฿2.31 already reached her in August's credit although UOB pays it in
        September (user, 2026-09-28: the bank's view stays in the share, the
        holder's net goes to the tracker and the ledger credit)."""
        return sum((t.amount * t.cb for t in adjustments
                    if t.holder == holder and t.cb is not None and t.cb in self.tiers), Decimal(0))


class UOBOneBonus(_UOBOne):
    name_pattern = r"\bUOB One cb 10%/5%"
    headline = "10%/5%"
    tiers = frozenset({Decimal("0.1"), Decimal("0.05")})
    cap = Decimal(500)

    def expected(self, r: TxCredit) -> dict[str, Any]:
        """Inside the ฿500: the row's own rate. Wholly past it: 1% (the bank drops
        the rest of the month to the base rate). The row the cap runs out on is
        left unset, like any boundary row."""
        if r.counted == r.tx.amount:
            return {"cashback_percent": self.rate(r.tx)}
        return {"cashback_percent": BASE_RATE if r.counted == 0 else None}

    ladder_rows = (
        ("BTS via LINE Pay or Rabbit Rewards packages; MRT Blue & Purple (tap-to-pay at the gate); "
         "Café Amazon", "10%"),
        ("7-Eleven and ALL ONLINE; Grab; Watsons and Watsons online", "5%"),
        ("Cap", "฿500 a calendar month, 10% and 5% together, per account"),
        ("Past the cap", "the rest of the month's 10%/5% spend earns 1%"),
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
    tiers = frozenset({BASE_RATE})
    cap = Decimal(2_000)

    def rate(self, tx: Tx) -> Decimal | None:
        """1% rows, plus 10%/5% rows that ran past the month's ฿500 and are marked
        `% cb` 1% (UOBOneBonus.expected asks for that mark)."""
        if super().rate(tx) is not None:
            return BASE_RATE
        overflowed = self._tier(tx) in UOBOneBonus.tiers and tx.cb == BASE_RATE
        return BASE_RATE if overflowed and not _MAKRO_IN_STORE.match(tx.merchant) else None

    ladder_rows = (
        ("Everything else that isn't excluded, including e-wallet payments and each billed "
         "installment term", "1%"),
        ("10%/5% spend past that month's ฿500 cap (marked `% cb` 1%)", "1%"),
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
