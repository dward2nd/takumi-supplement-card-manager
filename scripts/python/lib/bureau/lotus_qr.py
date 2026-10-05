"""Lotus's QRT4 — "จ่ายแบบไหน ก็ได้คืน", 10% (at most ฿10) on a ฿100 slip in five categories, 1 Jul – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.lotussmoney.com/promotion/credit-card/shopping/shopping-lotus-paywave
on 2026-10-05. Lotus's Mastercard only (Lotus's Beyond is one). A slip of ฿100
or more in fashion, department stores, private hospitals / clinics / pharmacies,
restaurants (not inside hotels) or home décor and building materials earns 10%,
at most ฿10 — so ฿10 a slip. Two channels with their own caps, per primary card
number and calendar month:

  Tap & Go                         ฿10 a month
  UCHOOSE credit-card QR, or the   ฿10 a slip, ฿40 a month
  card linked in TrueMoney Wallet

฿50 a month and ฿300 for the campaign in all. The ledger can't tell a tap from a
QR payment; the household pays by QR / TrueMoney (the bank's credit line reads
`CB TMN QR QRT4<MON><YY>`), so the cap here is the QR channel's ฿40. A tap at
one of the categories would add up to ฿10 a month on top.

The bank decides the category by MCC. Only the department-store, fashion and
home names show it, and the household's QRT4 slips are restaurants with
names nothing can match (`MOOYIM JIMJUM CITY TH`, `CHAILAISALADROLLHEALHT CITY TH`).
So every ฿100 slip counts except merchants whose names show they're outside the
five categories: Lotus's and every supermarket and convenience store, Makro,
marketplaces, phone and utility bills, fuel, transport, top-ups, PromptPay.
Verified against the credits: all five ฿100 slips of 2 Sep – 1 Oct 2026 were
paid ฿10 each within three days, and the ฿52 slip of 2 Sep wasn't.

`% cb` stays unset (a fixed ฿10 isn't a rate); the money is in the Bureau and
Takumi's tracker, and the bank's credit lines are already in his ledger.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import UNCERTAIN, Rule, Tx
from .slips import SlipCreditPromotion

MIN_SLIP, RATE, MAX_PER_SLIP = Decimal(100), Decimal("0.10"), Decimal(10)

# Merchants whose names show they're outside the five categories.
_OUTSIDE = re.compile(
    r"LOTUS|7-?11|7-?ELEVEN|FAMILYMART|\bCJ ?MORE\b|MAKRO|GO ?WHOLESALE|PROMPTPAY|"
    r"SHOPEE(?! ?FOOD)|LAZADA|TIKTOK|"
    r"\bAIS\b|\bAWN\b|TRUE ?MOVE|TRUE ?ONLINE|TRUE ?ISERVICE|\bDTAC\b|"
    r"การไฟฟ้า|การประปา|\b(MEA|PEA|MWA|PWA)\b")


def _outside(tx: Tx) -> bool:
    m = tx.merchant
    return bool(_OUTSIDE.search(m)) or promotions.looks_supermarket(m) or promotions.looks_petrol(m) \
        or promotions.looks_transport_or_toll(m) or promotions.looks_wallet_top_up(m) \
        or promotions.looks_foreign_in_thb(m)


class QRT4Promotion(SlipCreditPromotion):
    code = "QRT4"
    icon = "📱"
    title = "จ่ายแบบไหน ก็ได้คืน"
    cards = ("Lotus's Beyond",)
    campaign = (dt.date(2026, 7, 1), dt.date(2026, 12, 31))
    source_url = "https://www.lotussmoney.com/promotion/credit-card/shopping/shopping-lotus-paywave"
    headline = "10%"
    cap = Decimal(40)

    def qualifies(self, tx: Tx) -> bool:
        return tx.amount >= MIN_SLIP and not _outside(tx)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        return min(tx.amount * RATE, MAX_PER_SLIP) if self.qualifies(tx) else None

    ladder_title = "Cashback per slip"
    ladder_header = ("Slip in the five categories", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿100", "nothing"),
        ("฿100 or more", "10%, at most ฿10 — so ฿10"),
        ("Cap", "฿40 a month by UCHOOSE QR or TrueMoney (tracked here); Tap & Go ฿10 a month on its own; "
                "฿50 a month and ฿300 for the campaign in all, per primary card number"),
    )
    inclusions: ClassVar = (
        "Five categories, by the merchant's MCC: fashion (UNIQLO, ZARA, H&M); department stores "
        "(Central, Emporium, The Mall, Paragon); private hospitals, vet hospitals, health and beauty "
        "clinics, dental clinics and pharmacies; restaurants; home décor and building materials "
        "(Thai Watsadu, Boonthavorn, DoHome, Global House, HomePro, IKEA, Index Living Mall, MR.D.I.Y., "
        "Mega Home, SB Design Square, SCG Home).",
        "Paid by Tap & Go, by scanning the card's QR in UCHOOSE, or with the card linked in TrueMoney "
        "Wallet. One slip of ฿100 or more each time; slips never add up.",
        "Restaurants can't be told apart by name, so every ฿100 slip counts here unless the name shows "
        "it's outside the categories. The bank's own credit (`CB TMN QR QRT4<MON><YY>`, a few days "
        "after the slip) confirms each one.",
        "Lotus's Mastercard only. Per primary card number: supplements count, and their credit goes to "
        "the primary account.",
        "Register once, before the transaction: UCHOOSE → \"QRT4\", or SMS \"QRT4 <16-digit card no.>\" "
        "to 081-250-7777.",
    )
    rules: ClassVar = (
        Rule("Installments, including each billed term", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Government hospitals (MCC 9399)", r"HOSPITAL|โรงพยาบาล|MAHARAJ|SRIPHAT|NAKORNPING",
             level=UNCERTAIN, hint="private hospitals, clinics and pharmacies count; a state hospital "
                                   "bills under MCC 9399, which doesn't"),
        Rule("Restaurants inside hotels", r"HOTEL|RESORT", level=UNCERTAIN,
             hint="a hotel's restaurant doesn't count, and a hotel stay isn't one of the categories"),
        Rule("Food delivery apps (Grab, LINE MAN, foodpanda, Robinhood, ShopeeFood)",
             r"GRAB|LINE ?MAN|_LM_|FOODPANDA|ROBINHOOD|SHOPEE ?FOOD", level=UNCERTAIN,
             hint="counts only if the app bills under a restaurant MCC, which is unknown"),
        Rule("Cancelled charges; use against the card's purpose; digital assets, crypto and forex"),
    )
    crediting: ClassVar = (
        "Terms: within 60 days after each month-end, to the primary account. In practice each slip's "
        "฿10 posts within three days as `CB TMN QR QRT4<MON><YY>`, named for the month of the slip.",
        "Caps: ฿40 a month here (QR and TrueMoney), ฿10 a month more for Tap & Go, ฿300 for the "
        "campaign per primary card number.",
    )


PROMOTIONS = (QRT4Promotion,)
