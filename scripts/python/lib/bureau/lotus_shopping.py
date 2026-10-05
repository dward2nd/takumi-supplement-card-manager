"""Lotus's SMP1 "ช้อปคุ้มตัวแม่" (Sep – Dec 2026) and its October add-on SMT2.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.lotussmoney.com/cashback-nationwide on 2026-10-05.
Both count the same categories — department stores, fashion, cosmetics, mobile
/ IT shops and phone / internet bills paid to the operator, books, stationery
and household lifestyle shops — on the primary account's pooled spend in a
calendar month, supplements included. Takumi registered both before his
1 Oct AIS bill payment, which the app confirmed counts for both (user,
2026-10-05).

  SMP1  pays the **single highest tier reached only** ("สงวนสิทธิ์การให้เครดิตเงินคืน
        ระดับสูงสุดเพียงระดับเดียวเท่านั้น"): ฿70 per whole ฿3,500 (at most ฿350), or
        ฿450 per whole ฿25,000 (at most ฿1,800), or ฿2,600 from ฿150,000. So
        ฿24,999 earns ฿350 and ฿25,000 earns ฿450. Capped at ฿2,600 a month; the
        conditions say ฿10,400 for the campaign, one banner line ฿14,000.
  SMT2  ฿200 once at ฿2,000 in October, for the first 500 accounts that
        registered before spending and reach it ("รูดก่อน ได้ก่อน").

The joint terms bar spend that counts in another Lotus's promotion, but SMP1
and SMT2 share those terms and stack (the app shows both). Lotus's rows keep
`% cb` unset, so these write the Bureau and the trackers only, like LBS3.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .ladder import LadderPromotion, Tranche

SMALL_STEP, SMALL_PAY, SMALL_STEPS = Decimal(3_500), Decimal(70), 5
BIG_FROM = BIG_STEP = Decimal(25_000)
BIG_PAY, BIG_STEPS = Decimal(450), 4
TOP_AT, TOP_PAY = Decimal(150_000), Decimal(2_600)
SMT2_AT, SMT2_PAY = Decimal(2_000), Decimal(200)

# The page's named examples, by category. The bank decides by MCC, so a store in
# a category but not named here counts too; the household's rows are matched on
# these and checked by hand otherwise.
_CATEGORIES = re.compile(
    r"\bCENTRAL\b|PARAGON|ROBINSON|THE ?MALL|EMPORIUM|EMQUARTIER|ICONSIAM|KING ?POWER|"
    r"\bH ?& ?M\b|\bAIIZ\b|\bZARA\b|CHANEL|LOUIS ?VUITTON|UNIQLO|DECATHLON|ANELLO|"
    r"BEAUTRIUM|BATH ?& ?BODY|CUTE ?PRESS|EVE ?AND ?BOY|ORIENTAL ?PRINCESS|SEPHORA|"
    r"JAYMART|BANANA|BIG ?CAMERA|\bCOM ?7\b|I-?STUDIO|IT ?CITY|\bJIB\b|\bADVICE\b|TELEWIZ|"
    r"\bAIS\b|MY ?AIS|\bAWN\b|TRUE ?MOVE|TRUE ?ISERVICE|TRUE ?ONLINE|\bDTAC\b|"
    r"SE-?ED|ซีเอ็ด|NAIIN|นายอินทร์|ASIA ?BOOKS|NANMEE|KINOKUNIYA|\bB2S\b|OFFICE ?MATE|DAISO|"
    r"MR\.? ?D\.?I\.?Y|MINISO|MOSHI ?MOSHI")

_INCLUSIONS = (
    "Department stores (Central, Paragon, Robinson, The Mall, ICONSIAM, King Power); fashion (H&M, "
    "AIIZ, ZARA, Chanel, Louis Vuitton, UNIQLO, Decathlon, Anello); cosmetics (BEAUTRIUM, Bath & "
    "Body, Cute Press, EVEANDBOY, Oriental Princess, Sephora); mobile and IT (Jaymart, Banana, Big "
    "Camera, Com7, I-Studio, IT City, JIB, Advice, Telewiz) and phone / internet bills paid at the "
    "operator's counter, website or app (AIS Shop, My AIS, TRUE & dtac Shop, True iservice; True "
    "Money Wallet for the monthly bill only); books, stationery, office and household lifestyle "
    "(SE-ED, Naiin, Asia Books, Nanmeebooks, Kinokuniya, B2S, OfficeMate, Daiso, MR.DIY, MINISO, "
    "Moshi Moshi). The bank decides by the card network's MCC and the name on the slip.",
    "Full amount after discounts, at Thai merchants, in baht. Settled spend only, as billed on the "
    "statement; cancelled or returned spend is taken back out.",
    "Pooled per calendar month on the primary account (Takumi's); every supplement counts.",
)

_RULES = (
    Rule("Anything sold by Lotus's, and every supermarket, hypermarket and convenience store",
         r"LOTUS|BIG ?C\b|\bTOPS\b|MAKRO|7-?ELEVEN|^7-11|FAMILYMART|VILLA|FOODLAND|CENTRAL ?FOOD"),
    Rule("Power Buy and Power Mall", r"POWER ?BUY|POWER ?MALL"),
    Rule("Marketplaces and wallets: Lazada, Shopee, ShopeePay, Konvy, TikTok, True Select, Top Value, "
         "easyBills, AirPay, Alibaba, AliExpress, All Online by 7-Eleven",
         r"LAZADA|SHOPEE|KONVY|TIKTOK|TRUE ?SELECT|TOP ?VALUE|EASY ?BILLS|AIRPAY|ALIBABA|ALIEXPRESS|"
         r"ALL ?ONLINE"),
    Rule("Boots, Watsons and direct sales (Amway, Giffarine, Zhulian, Herbalife, Kangzen Kenko, Unicity)",
         r"BOOTS|WATSON|AMWAY|GIFFARINE|ZHULIAN|HERBALIFE|KANGZEN|UNICITY"),
    Rule("Gold, jewellery, watches and valuables"),
    Rule("Installments, including each billed term", test=lambda tx: promotions.is_installment(tx.name)),
    Rule("Spending abroad, currency exchange, and online stores registered abroad in any currency",
         test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
    Rule("Utility bills on monthly or yearly auto-debit"),
    Rule("Interest, fees and penalties; charges cancelled later or not yet billed"),
)


class SMP1Promotion(LadderPromotion):
    code = "SMP1"
    icon = "🛍️"
    title = "ช้อปคุ้มตัวแม่"
    cards = ("Lotus's Beyond",)
    campaign = (dt.date(2026, 9, 1), dt.date(2026, 12, 31))
    source_url = "https://www.lotussmoney.com/cashback-nationwide"
    headline = "2%"
    marks_rows = False   # Lotus's rows keep `% cb` unset; the money is in the trackers

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        if pooled >= TOP_AT:
            return [Tranche(Decimal(0), TOP_AT, TOP_PAY)]
        if pooled >= BIG_FROM:
            steps = min(int(pooled // BIG_STEP), BIG_STEPS)
            return [Tranche(Decimal(0), steps * BIG_STEP, steps * BIG_PAY)]
        steps = min(int(pooled // SMALL_STEP), SMALL_STEPS)
        return [Tranche(Decimal(0), steps * SMALL_STEP, steps * SMALL_PAY)] if steps else []

    def qualifies(self, tx: Tx) -> bool:
        return bool(_CATEGORIES.search(tx.merchant))

    ladder_rows: ClassVar = (
        ("under ฿3,500", "nothing"),
        ("every whole ฿3,500, while under ฿25,000", "฿70 — up to ฿350"),
        ("or every whole ฿25,000, from ฿25,000", "฿450 — up to ฿1,800"),
        ("or ฿150,000 or more", "฿2,600 — the monthly cap"),
    )
    inclusions: ClassVar = (
        "Only the single highest tier reached pays (\"ระดับสูงสุดเพียงระดับเดียวเท่านั้น\").",
        *_INCLUSIONS,
        "Only spend from the registration day on counts: UCHOOSE → \"SMP1\", or SMS \"SMP1 "
        "<16-digit card no.>\" to 081-250-7777. Once for the campaign.",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = (
        "Within 30 days after each month-end, on the primary account's statement.",
        "Caps: ฿2,600 a month and ฿10,400 for the campaign per primary account (the conditions; one "
        "banner line says ฿14,000).",
        "Spend counted in another Lotus's promotion can't count here; SMT2 shares these terms and stacks.",
    )


class SMT2Promotion(LadderPromotion):
    code = "SMT2"
    icon = "🐦"
    title = "รูดก่อน ได้ก่อน"
    cards = ("Lotus's Beyond",)
    campaign = (dt.date(2026, 10, 1), dt.date(2026, 10, 31))
    source_url = "https://www.lotussmoney.com/cashback-nationwide"
    headline = "฿200"
    marks_rows = False

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        return [Tranche(Decimal(0), SMT2_AT, SMT2_PAY)] if pooled >= SMT2_AT else []

    def qualifies(self, tx: Tx) -> bool:
        return bool(_CATEGORIES.search(tx.merchant))

    ladder_title = "Cashback"
    ladder_rows: ClassVar = (
        ("under ฿2,000", "nothing"),
        ("฿2,000 or more in October", "฿200, once"),
    )
    inclusions: ClassVar = (
        "SMP1's categories (below), in October 2026.",
        *_INCLUSIONS,
        "Register before spending: UCHOOSE → \"SMT2\", or SMS \"SMT2 <16-digit card no.>\" to "
        "081-250-7777. Spend before the registration doesn't count.",
        "Only the first 500 accounts to register and reach ฿2,000 are paid. Check the rights left in "
        "UCHOOSE before spending.",
    )
    rules: ClassVar = _RULES
    crediting: ClassVar = (
        "Within 30 days after October ends, on the primary account's statement.",
        "Cap: ฿200 per primary account for the campaign.",
        "Shares SMP1's joint terms and stacks with it.",
    )


PROMOTIONS = (SMP1Promotion, SMT2Promotion)
