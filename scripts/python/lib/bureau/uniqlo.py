"""UNIQLO card campaigns, 1 Oct 2026 – 28 Feb 2027 — UOB (UNO), Krungsri (UNQ), KBank (UQN), ttb (UQCB).

deterministic + idempotent — declarations and pure functions only.

Terms read on 2026-10-01 from UNIQLO's bank pages
(https://www.uniqlo.com/th/th/special-feature/cp/promotion/{uob,krungsri,ktc,kbank},
tiers and dates from each page's banner image) and ttb's own page
(https://www.ttbbank.com/th/promotion/credit-card/shopping/uniqlo-oct26). Every
one pays per slip at UNIQLO stores and online; slips never add up; the monthly
cap is the only one that binds (each campaign cap is 5 × the month's).

  UNO  (UOB)      ฿150 per whole ฿3,000, ฿800 from ฿12,000; ฿800 a month per
                  cardholder, every UOB card pooled. Register by SMS *every time*,
                  within the transaction day. Stores inside department stores and
                  UOB LADY LUXE PAY are out.
  UNQ  (Krungsri) ฿150 / ฿300 / ฿450 at ฿3,000 / 6,000 / 9,000, and from ฿10,000
                  ฿800 on Krungsri JCB, ฿700 on the other cards; that is also each
                  card account's monthly cap. Register once (UCHOOSE or SMS).
  UQN  (KBank)    ฿100 / 200 / 300 / 600 at ฿3,000 / 6,000 / 9,000 / 12,000;
                  ฿600 a month. The page says "per person", but KBank counts each
                  card on its own unless it says otherwise (user, 2026-10-01), so
                  the Bureau keeps one row per KBank card. Register once before
                  spending; registered 2026-10-01 (user), on every KBank card. The K Point extras (+200/400/600 points, 1,200 a month)
                  are bank bonus points: `[คะแนนพิเศษ]` rows when they post.
  UQCB (ttb)      as UNO: ฿150 per whole ฿3,000, ฿800 from ฿12,000; ฿800 a month
                  per person, primary and supplements pooled. Register once.

KTC's UNIQLO page is points only (KTC JCB ×2/×3/×5 on monthly spend at UNIQLO,
MUJI, COMME des GARÇONS, ISSEY MIYAKE and BEAMS, 1 Jul – 31 Dec 2026, credited
later as bonus points), and Krungsri JCB's 3× at UNIQLO is the same kind of
bonus: neither is a Bureau campaign. See docs/promotions/uniqlo-2026.md.

Fixed credits per slip, so `% cb` stays unset (`SlipCreditPromotion`).
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .accounts import CardAccount
from .base import Rule, Tx
from .slips import SlipCreditPromotion

CAMPAIGN = (dt.date(2026, 10, 1), dt.date(2027, 2, 28))
TITLE = "ช้อปคุ้มที่ UNIQLO ทุกสาขาและออนไลน์"
_UNIQLO = re.compile(r"UNIQLO")
_WALLET = r"^TMN[ *]|TRUE ?MONEY|^LINEPAY\*|^LPTH\*|SHOPEEPAY|RABBIT"


def _per_3000(tx: Tx, *, top_from: int, top: Decimal) -> Decimal | None:
    """฿150 per whole ฿3,000 of the slip, or `top` from `top_from` (UNO, UQCB)."""
    if not _UNIQLO.search(tx.merchant) or tx.amount < 3_000:
        return None
    return top if tx.amount >= top_from else tx.amount // 3_000 * Decimal(150)


class _UniqloSlips(SlipCreditPromotion):
    icon = "👕"
    campaign = CAMPAIGN
    title = TITLE
    ladder_title = "Cashback per slip"
    ladder_header = ("UNIQLO slip", "Cashback")


class UOBUniqloPromotion(_UniqloSlips):
    code = "UNO"
    cards = ("UOB One", "UOB World", "UOB Premier", "UOB Makro")
    source_url = "https://www.uniqlo.com/th/th/special-feature/cp/promotion/uob"
    headline = "฿150–800"
    cap = Decimal(800)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        return _per_3000(tx, top_from=12_000, top=Decimal(800))

    ladder_rows: ClassVar = (
        ("under ฿3,000", "nothing"),
        ("every whole ฿3,000, under ฿12,000", "฿150 — up to ฿450"),
        ("฿12,000 or more", "฿800"),
        ("Cap", "฿800 a month and ฿4,000 for the campaign, per cardholder"),
    )
    inclusions: ClassVar = (
        "Full-amount spend at UNIQLO stores and UNIQLO online, on every UOB card (business cards "
        "excluded).",
        "Per slip: slips never add up.",
        "Pooled per primary cardholder: every UOB card Takumi holds and every supplement on them.",
        "Register by SMS \"UNO <last 12 digits>\" to 4545111, or Rewards+ in UOB TMRW, every time, "
        "within the day of the purchase. UOB Reserve and Infinite don't need to.",
    )
    rules: ClassVar = (
        Rule("UNIQLO stores inside a department store"),
        Rule("UOB LADY LUXE PAY", r"LUXE ?PAY"),
        Rule("Paid through an e-wallet", _WALLET),
        Rule("Installments (UOB i-Plan)", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Charges cancelled or returned later"),
    )
    crediting: ClassVar = (
        "Within 60 days after the campaign ends (28 Feb 2027), to a primary card the bank picks.",
        "Not combinable with other promotions. The top 5 spenders over ฿10,000 also win a suitcase.",
    )


class KrungsriUniqloPromotion(_UniqloSlips):
    code = "UNQ"
    source_url = "https://www.uniqlo.com/th/th/special-feature/cp/promotion/krungsri"
    headline = "฿150–700"
    cap = Decimal(700)
    top: ClassVar[Decimal] = Decimal(700)   # ฿10,000 or more; ฿800 on Krungsri JCB

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _UNIQLO.search(tx.merchant) or tx.amount < 3_000:
            return None
        return self.top if tx.amount >= 10_000 else tx.amount // 3_000 * Decimal(150)

    @property
    def ladder_rows(self):
        return (
            ("under ฿3,000", "nothing"),
            ("฿3,000 – 5,999 / 6,000 – 8,999 / 9,000 – 9,999", "฿150 / ฿300 / ฿450"),
            ("฿10,000 or more", f"฿{self.top:,.0f}"),
            ("Cap", f"฿{self.cap:,.0f} a month and ฿{self.cap * 5:,.0f} for the campaign, per primary "
                    f"card account"),
        )

    inclusions: ClassVar = (
        "Full-amount spend at every UNIQLO store, uniqlo.com and the UNIQLO app, on every Krungsri card "
        "(Visa, Mastercard, JCB).",
        "Per slip: slips never add up. From ฿10,000 a slip earns ฿800 on Krungsri JCB cards and ฿700 "
        "on the others.",
        "Each primary card account has its own cap; supplements count, and the bank credits the "
        "primary account.",
        "Register once in UCHOOSE (\"UNQ\") or by SMS \"UNQ <16-digit card no.>\" to 081-927-9999, "
        "within the day of the purchase.",
    )
    rules: ClassVar = (
        Rule("Krungsri Consumer Installment Plan", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Foreign currency; interest, fees and penalties; charges cancelled, refunded or never "
             "billed", test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
    )
    crediting: ClassVar = (
        "Within 30 days after each month-end, to the primary card account.",
        "Not combinable with other promotions. Krungsri JCB Platinum also earns 3× points at UNIQLO "
        "(no registration, at most 400 bonus points a month): bank bonus points, not tracked here.",
    )


class KBankUniqloPromotion(_UniqloSlips):
    code = "UQN"
    source_url = "https://www.uniqlo.com/th/th/special-feature/cp/promotion/kbank"
    headline = "฿100–600"
    cap = Decimal(600)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        if not _UNIQLO.search(tx.merchant) or tx.amount < 3_000:
            return None
        return Decimal(600) if tx.amount >= 12_000 else tx.amount // 3_000 * Decimal(100)

    ladder_rows: ClassVar = (
        ("under ฿3,000", "nothing"),
        ("฿3,000 – 5,999 / 6,000 – 8,999 / 9,000 – 11,999", "฿100 / ฿200 / ฿300 (+200 / 400 / 600 K Point)"),
        ("฿12,000 or more", "฿600"),
        ("Cap", "฿600 a month and ฿3,000 for the campaign — per card, as KBank counts cards separately"),
    )
    inclusions: ClassVar = (
        "Full-amount spend at every UNIQLO store and UNIQLO online, on every KBank credit card (business "
        "and fleet cards excluded).",
        "Per slip: slips never add up.",
        "The page caps it per person; KBank counts each card separately unless it says otherwise "
        "(user), so each KBank card has its own ฿600 a month.",
        "Register once before spending: K PLUS → Privilege & Offer → Missions For You, or SMS "
        "\"UQN <last 12 digits>\" to 4545888.",
        "The extra K Points (at most 1,200 a month; not on KBank LINE Points or Titanium Mastercard) "
        "arrive as bank bonus points: book them as [คะแนนพิเศษ] rows.",
    )
    rules: ClassVar = (
        Rule("KBank Smart Pay 0% and Smart Pay by Phone installments",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Paid through an e-wallet (TrueMoney, Rabbit LINE Pay, ShopeePay …)", _WALLET),
        Rule("Charges cancelled, returned or never billed"),
    )
    crediting: ClassVar = (
        "Within 60 days after the campaign ends (28 Feb 2027), cashback and extra points together.",
    )


class TTBUniqloPromotion(_UniqloSlips):
    code = "UQCB"
    cards = ("ttb so smart",)
    source_url = "https://www.ttbbank.com/th/promotion/credit-card/shopping/uniqlo-oct26"
    headline = "฿150–800"
    cap = Decimal(800)

    def slip_credit(self, tx: Tx) -> Decimal | None:
        return _per_3000(tx, top_from=12_000, top=Decimal(800))

    ladder_rows: ClassVar = (
        ("under ฿3,000", "nothing"),
        ("every whole ฿3,000, under ฿12,000", "฿150 — up to ฿450"),
        ("฿12,000 or more", "฿800"),
        ("Cap", "฿800 a month and ฿4,000 for the campaign, per person (every card together)"),
    )
    inclusions: ClassVar = (
        "Full-amount spend at every UNIQLO store and UNIQLO online, on every ttb card, primary and "
        "supplement pooled into the primary cardholder's account (Takumi's …7368, Baiboon's …0864).",
        "Read as each slip earning its own tier, as for the hypermarket campaign; the page's "
        "boilerplate also speaks of \"the highest slip per round\".",
        "Register once, before or on the transaction date: ttb touch, or SMS \"UQCB <last 12 digits>\" "
        "to 4899777.",
    )
    rules: ClassVar = (
        Rule("Converted to ttb so goood (which also loses so smart's 1%)",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Business spend; charges cancelled or returned later"),
    )
    crediting: ClassVar = (
        "Within 60 days after each month's end, to the primary card with the most spend.",
        "The points half (12% for ttb rewards plus points) doesn't apply: ttb so smart earns no points.",
    )


class UNQKrungsriVISA(CardAccount, KrungsriUniqloPromotion):
    cards = ("Krungsri VISA",)


class UNQKrungsriJCB(CardAccount, KrungsriUniqloPromotion):
    cards = ("Krungsri JCB",)
    headline = "฿150–800"
    cap = Decimal(800)
    top = Decimal(800)


class UNQKrungsriLady(CardAccount, KrungsriUniqloPromotion):
    cards = ("Krungsri Lady",)


class UNQKrungsriNOW(CardAccount, KrungsriUniqloPromotion):
    cards = ("Krungsri NOW",)


class UQNKBankJCB(CardAccount, KBankUniqloPromotion):
    cards = ("KBank JCB",)


class UQNKBankLINEPoints(CardAccount, KBankUniqloPromotion):
    cards = ("KBank LINE Points",)


class UQNKBankPLUSTINUM(CardAccount, KBankUniqloPromotion):
    cards = ("KBank PLUSTINUM",)


class UQNKBankShopee(CardAccount, KBankUniqloPromotion):
    cards = ("KBank Shopee",)


PROMOTIONS = (UOBUniqloPromotion, TTBUniqloPromotion,
              UNQKrungsriVISA, UNQKrungsriJCB, UNQKrungsriLady, UNQKrungsriNOW,
              UQNKBankJCB, UQNKBankLINEPoints, UQNKBankPLUSTINUM, UQNKBankShopee)
