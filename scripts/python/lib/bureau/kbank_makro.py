"""KBank MKR — "ช้อปเยอะคุ้มกว่า ที่ MAKRO", monthly Makro spend, 1 Oct – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-makro.aspx
on 2026-10-01 (behind an Akamai challenge; a real browser gets through). One
registration (K PLUS, or SMS `MKR <last 12 digits>` to 4545888, before or after
spending) for the two cashback parts, on full-amount spend at MAKRO in store
and MAKRO PRO online, added up over the calendar month:

  ต่อ 1 — ฿100 from ฿10,000, ฿240 from ฿20,000 (the bands replace each other);
          ฿240 a month, ฿720 for the campaign. `KBankMakroPromotion`.
  ต่อ 2 — ฿1,500 per whole ฿300,000, counting only spend after registering;
          ฿3,000 a month, ฿9,000 for the campaign. `KBankMakroBonusPromotion`,
          a separate quota. No household card comes near ฿300,000 a month at Makro,
          so it has no Bureau rows; create the month's row if one ever does.

The page caps both per person, but KBank counts each card separately unless it
says otherwise (user, 2026-10-01), so each KBank card is its own account
(`CardAccount`). Baiboon's Makro PRO slips go on KBank PLUSTINUM, the principal's
card, so they pool with Takumi's there.

The third part (10% back for K Points, `BCB` by SMS each time) is a redemption,
not tracked. KBank rows never carry `% cb` (points cards), so the credit lives in
the Bureau and the trackers (`marks_rows = False`). On KBank LINE Points, spend
counted here earns no LINE POINTS.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .accounts import CardAccount
from .base import Rule, Tx
from .ladder import LadderPromotion, Tranche

CAMPAIGN = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
SOURCE = "https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-makro.aspx"
TITLE = "ช้อปเยอะคุ้มกว่า ที่ MAKRO"
BANDS = ((Decimal(20_000), Decimal(240)), (Decimal(10_000), Decimal(100)))
BONUS_STEP, BONUS_PAY, BONUS_STEPS = Decimal(300_000), Decimal(1_500), 2

_MAKRO = re.compile(r"MAKRO")
_WALLET = r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*|SHOPEEPAY|RABBIT"
_RULES = (
    Rule("Paid through an e-wallet (TMN MAKRO, Rabbit LINE Pay, ShopeePay …)", _WALLET),
    Rule("Makro through other platforms (Shopee, Lazada, TikTok)", r"SHOPEE|LAZADA|TIKTOK"),
    Rule("KBank Smart Pay 0% and Smart Pay by Phone installments",
         test=lambda tx: promotions.is_installment(tx.name)),
    Rule("The liquor department, gift cards and e-gift cards, redemption goods, shops renting space "
         "inside the store"),
    Rule("Charges cancelled or refunded later"),
)
_INCLUSIONS = (
    "Full-amount spend at MAKRO in store and MAKRO PRO online, on every KBank credit card (business, "
    "juristic, Fleet and ThaiBev cards excluded), added up over the calendar month.",
    "Each KBank card is its own quota: KBank counts cards separately unless it says otherwise (the "
    "page says \"per person\").",
    "Register once, before or after spending, between 1 Oct and 31 Dec 2026: K PLUS, or SMS "
    "\"MKR <last 12 digits>\" to 4545888.",
)


def _makro(tx: Tx) -> bool:
    return bool(_MAKRO.search(tx.merchant))


class KBankMakroPromotion(LadderPromotion):
    code = "MKR"
    icon = "🛒"
    title = f"{TITLE} — ต่อ 1"
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "฿100/240"
    marks_rows = False   # KBank rows never carry `% cb`; the money is in the trackers

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        for reach, pay in BANDS:
            if pooled >= reach:
                return [Tranche(Decimal(0), reach, pay)]
        return []

    def qualifies(self, tx: Tx) -> bool:
        return _makro(tx)

    ladder_rows: ClassVar = (
        ("under ฿10,000", "nothing"),
        ("฿10,000 – 19,999", "฿100"),
        ("฿20,000 or more", "฿240 — the monthly cap"),
    )
    examples: ClassVar = ((9_999, 0), (10_000, 100), (19_999, 100), (20_000, 240), (90_000, 240))
    inclusions: ClassVar = _INCLUSIONS
    rules: ClassVar = _RULES
    crediting: ClassVar = (
        "Within 60 days after the campaign ends (31 Dec 2026), to the card.",
        "Caps: ฿240 a month and ฿720 for the campaign.",
    )


class KBankMakroBonusPromotion(LadderPromotion):
    code = "MKR+"
    icon = "🛒"
    title = f"{TITLE} — ต่อ 2 (เครดิตเงินคืนเพิ่ม)"
    campaign = CAMPAIGN
    source_url = SOURCE
    headline = "฿1,500"
    marks_rows = False

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        steps = min(int(pooled // BONUS_STEP), BONUS_STEPS)
        return [Tranche(Decimal(0), steps * BONUS_STEP, steps * BONUS_PAY)] if steps else []

    def qualifies(self, tx: Tx) -> bool:
        return _makro(tx)

    ladder_rows: ClassVar = (
        ("under ฿300,000", "nothing"),
        ("every whole ฿300,000", "฿1,500 — up to ฿3,000, reached at ฿600,000"),
    )
    examples: ClassVar = ((299_999, 0), (300_000, 1_500), (600_000, 3_000), (900_000, 3_000))
    inclusions: ClassVar = (*_INCLUSIONS, "Counts only spend made after the registration is confirmed.")
    rules: ClassVar = _RULES
    crediting: ClassVar = (
        "Within 60 days after the campaign ends (31 Dec 2026), to the card.",
        "Caps: ฿3,000 a month and ฿9,000 for the campaign.",
    )


class MKRKBankJCB(CardAccount, KBankMakroPromotion):
    cards = ("KBank JCB",)


class MKRKBankLINEPoints(CardAccount, KBankMakroPromotion):
    cards = ("KBank LINE Points",)


class MKRKBankPLUSTINUM(CardAccount, KBankMakroPromotion):
    cards = ("KBank PLUSTINUM",)


class MKRKBankShopee(CardAccount, KBankMakroPromotion):
    cards = ("KBank Shopee",)


class MKRBonusKBankJCB(CardAccount, KBankMakroBonusPromotion):
    cards = ("KBank JCB",)


class MKRBonusKBankLINEPoints(CardAccount, KBankMakroBonusPromotion):
    cards = ("KBank LINE Points",)


class MKRBonusKBankPLUSTINUM(CardAccount, KBankMakroBonusPromotion):
    cards = ("KBank PLUSTINUM",)


class MKRBonusKBankShopee(CardAccount, KBankMakroBonusPromotion):
    cards = ("KBank Shopee",)


ACCOUNTS = (MKRKBankJCB, MKRKBankLINEPoints, MKRKBankPLUSTINUM, MKRKBankShopee,
            MKRBonusKBankJCB, MKRBonusKBankLINEPoints, MKRBonusKBankPLUSTINUM, MKRBonusKBankShopee)
