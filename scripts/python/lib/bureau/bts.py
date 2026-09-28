"""Krungsri BTS WORLD TOUR 'ARIRANG' IN BANGKOK — lucky-draw rights, 1 Aug – 15 Nov 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.firstchoice.co.th/promotion/bts-world-tour-arirang-in-bangkok
on 2026-09-29. No cashback and no points: every slip of ฿1,500 or more,
full-amount or installment, earns one right in the prize draw, up to 10 rights
per person per month, all card types together. Registration alone earns
nothing for an existing cardholder. Supplements' slips count toward the
primary card's number, so Baiboon's and Nuta's slips earn Takumi's rights and
use up his 10.

The cap is per company (user, 2026-09-29): First Choice (Ayudhya Capital
Services, one Visa card per principal) and Krungsri Card (Krungsri Ayudhya
Card, possibly several Visa cards) each give up to 10 rights a month — 20 in
all. So the Bureau keeps two rows a month, `… — BTS First Choice 10 rights` and
`… — BTS Krungsri Card 10 rights`. Only Visa counts: of the household's
Krungsri cards that's Krungsri VISA (Lady and NOW are Mastercard, JCB is JCB).
Tracked from August 2026.

Each draw takes the rights earned in its own window: August (drawn 10 Sep),
September (12 Oct), and 1 Oct – 15 Nov (20 Nov).
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import ClassVar


from .. import promotions
from .base import UNCERTAIN, Rule
from .rights import DrawRightsPromotion


class BTSDrawPromotion(DrawRightsPromotion):
    """The campaign's terms; each company's pool is a subclass naming its cards."""

    code = "BTS"
    title = "กรุงศรีร่วมแจม BTS WORLD TOUR 'ARIRANG' IN BANGKOK"
    pool: ClassVar[str]                  # the company whose 10 rights a month this is
    campaign = (dt.date(2026, 8, 1), dt.date(2026, 11, 15))
    source_url = "https://www.firstchoice.co.th/promotion/bts-world-tour-arirang-in-bangkok"
    headline = "10 rights"
    min_slip = Decimal(1_500)
    max_rights = 10

    ladder_rows: ClassVar = (
        ("A slip of ฿1,500 or more (full amount or installment)", "1 right"),
        ("Cap", "10 rights a month per person per company: First Choice and Krungsri Card each"),
    )
    def row_name(self, start: dt.date, end: dt.date) -> str:
        return f"{start.year}M{start.month} — BTS {self.pool} {self.headline}"

    inclusions: ClassVar = (
        "Krungsri VISA (every kind) and First Choice (every kind), through the Visa network; First "
        "Choice cash advances on the credit line count too.",
        "Each company counts its own 10 a month: First Choice's cards in one pool, Krungsri Card's "
        "Visa cards in the other.",
        "Per slip: slips never add up, and a bigger slip earns no more than one right.",
        "Supplements' slips count toward the primary card's number: they're Takumi's rights.",
        "Register once, on or before the transaction date: UCHOOSE → \"BTS\", or SMS \"BTS "
        "<16-digit card no.>\" to 081-927-9999 (Krungsri VISA) or 081-256-3333 (First Choice).",
        "Draws: August's rights on 10 Sep (announced 18 Sep), September's on 12 Oct (21 Oct), "
        "1 Oct – 15 Nov's on 20 Nov (25 Nov). One prize per winner for the whole campaign.",
        "No overdue balance of more than 30 days with the bank.",
    )
    rules: ClassVar = (
        Rule("Funds of every kind, LTF, RMF", r"\bFUND\b|\bLTF\b|\bRMF\b|ASSET MANAGEMENT"),
        Rule("An installment term: the bank counts the purchase slip, which the ledger may not show",
             test=lambda tx: promotions.is_installment(tx.name), level=UNCERTAIN,
             hint="a ฿1,500+ purchase converted to installments earns one right on its slip"),
        Rule("Cash advances on Krungsri VISA (First Choice's count); interest, fees and penalties; "
             "charges cancelled or refunded later", r"\bFEE\b|INTEREST|CASH ADVANCE|PENALTY"),
    )
    crediting: ClassVar = (
        "Winners are announced on krungsri.com, krungsricard.com and firstchoice.co.th; a prize "
        "of ฿1,000 or more carries 5% withholding tax and 7% VAT, paid by the winner.",
    )


class BTSFirstChoice(BTSDrawPromotion):
    pool = "First Choice"
    name_pattern = r"\bBTS First Choice\b"
    cards = ("First Choice",)


class BTSKrungsriCard(BTSDrawPromotion):
    pool = "Krungsri Card"
    name_pattern = r"\bBTS Krungsri Card\b"
    cards = ("Krungsri VISA",)   # Krungsri Card's Visa cards; Lady and NOW are Mastercard


POOLS = (BTSFirstChoice, BTSKrungsriCard)
