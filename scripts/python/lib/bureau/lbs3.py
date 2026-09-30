"""Lotus's LBS3 — "ช้อปของใหญ่จัดเต็ม", big-ticket categories, 1 Sep – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.lotussmoney.com/promotion/credit-card/shopping/cashback-nationwide-bigticket
on 2026-09-29. Pooled monthly spend at home-décor and building-material
stores, electrical-appliance stores, car service centres and Makro (every
channel) pays for the **single highest tier reached only**: ฿80 per whole
฿5,000 (at most 4, ฿320), or ฿500 per whole ฿30,000 (at most 5, ฿2,500), or
฿3,500 from ฿300,000. So ฿29,999 earns ฿320 and ฿30,000 earns ฿500. Capped at
฿3,500 a month and ฿14,000 for the campaign per primary account.

LMK2 (฿5,000 for the first 100 accounts past ฿800,000 at Makro PRO) isn't
tracked. Lotus's rows keep `% cb` unset, so this writes the Bureau and the
trackers only.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import Rule, Tx
from .ladder import LadderPromotion, Tranche

SMALL_STEP, SMALL_PAY, SMALL_STEPS = Decimal(5_000), Decimal(80), 4
BIG_FROM = BIG_STEP = Decimal(30_000)
BIG_PAY, BIG_STEPS = Decimal(500), 5
TOP_AT, TOP_PAY = Decimal(300_000), Decimal(3_500)

_STORES = re.compile(
    r"HOME ?PRO|IKEA|INDEX|MEGA ?HOME|DO ?HOME|GLOBAL ?HOUSE|SB ?DESIGN|BOONTHAVORN|บุญถาวร|THAI ?WATSADU|"
    r"ไทวัสดุ|BNB ?HOME|HARDWAREHOUSE|Q-?CHANG|\bSCG\b|LANDSCAPE PRO|DOODECO|"
    r"POWER ?BUY|POWER ?MALL|DAIKIN|ELECTROLUX|HAIER|HITACHI|\bLG\b|MODERN AIR|PANASONIC|SHARP|TOSHIBA|"
    r"SANG ?GROUP|ส\.แสง|"
    r"B-?QUIK|FIT ?AUTO|AUTOBACS|GOODYEAR|AUTO ?1|TYRE ?PLUS|BENZ|BRIDGESTONE|COCKPIT|HONDA|ISUZU|"
    r"KLEAN ?SQUARE|MAZDA|NISSAN|SUZUKI|TOYOTA|WIZARD|YAMAHA|"
    r"MAKRO")


class LBS3Promotion(LadderPromotion):
    code = "LBS3"
    icon = "🛒"
    title = "ช้อปของใหญ่จัดเต็ม"
    cards = ("Lotus's Beyond",)
    campaign = (dt.date(2026, 9, 1), dt.date(2026, 12, 31))
    source_url = ("https://www.lotussmoney.com/promotion/credit-card/shopping/"
                  "cashback-nationwide-bigticket")
    headline = "1.6%"
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
        return bool(_STORES.search(tx.merchant))

    ladder_rows: ClassVar = (
        ("under ฿5,000", "nothing"),
        ("every whole ฿5,000, while under ฿30,000", "฿80 — up to ฿320"),
        ("or every whole ฿30,000, from ฿30,000", "฿500 — up to ฿2,500"),
        ("or ฿300,000 or more", "฿3,500 — the monthly cap"),
    )
    examples: ClassVar = ((4_999, 0), (10_000, 160), (29_999, 320), (30_000, 500), (60_000, 1_000),
                          (150_000, 2_500), (299_999, 2_500), (300_000, 3_500))
    inclusions: ClassVar = (
        "Only the single highest tier reached pays (\"เพียงระดับสูงสุดระดับเดียวเท่านั้น\").",
        "Home décor and building materials (HomePro, IKEA, Index Living Mall, Mega Home, DoHome, "
        "Global House, SB Design Square, Boonthavorn, Thai Watsadu, SCG …); electrical appliances "
        "(Power Buy, Power Mall, Daikin, Electrolux, Haier, Hitachi, LG, Panasonic, Sharp, Toshiba …); "
        "car maintenance and service centres (B-Quik, Fit Auto, Autobacs, Goodyear, Toyota, Honda …); "
        "and Makro through every channel — app, website, stores. The bank decides by the card "
        "network's MCC and the name on the slip.",
        "Full amount after discounts, in Thailand, in baht; in store, Tap & Go or the store's own "
        "online shop. Settled spend only, as billed on the statement.",
        "Pooled per calendar month on the primary account (Takumi's); supplements count.",
        "Only spend from the registration day on counts: UCHOOSE → \"LBS3\", or SMS \"LBS3 "
        "<16-digit card no.>\" to 081-250-7777. Once for the campaign.",
    )
    rules: ClassVar = (
        Rule("Anything sold by Lotus's, and every supermarket, hypermarket and convenience store "
             "(Makro excepted)", r"LOTUS|BIG ?C\b|\bTOPS\b|7-?ELEVEN|FAMILYMART|VILLA|FOODLAND"),
        Rule("Marketplaces and wallets: Lazada, Shopee, ShopeePay, Konvy, TikTok, True Select, Top "
             "Value, easyBills, AirPay, Alibaba, AliExpress, All Online, LINE Pay",
             r"LAZADA|SHOPEE|KONVY|TIKTOK|TRUE ?SELECT|TOP ?VALUE|EASY ?BILLS|AIRPAY|ALIBABA|ALIEXPRESS|"
             r"ALL ?ONLINE|LINE ?PAY|^LPTH\*|^TMN"),
        Rule("Boots, Watsons and direct sales (Amway, Giffarine, Zhulian, Herbalife …)",
             r"BOOTS|WATSON|AMWAY|GIFFARINE|ZHULIAN|HERBALIFE|KANGZEN|UNICITY"),
        Rule("Installments, including each billed term", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Spending abroad, and online stores registered abroad in any currency",
             test=lambda tx: promotions.looks_foreign_in_thb(tx.merchant)),
        Rule("Interest, fees and penalties; charges cancelled later or not yet billed"),
    )
    crediting: ClassVar = (
        "Within 60 days after each month-end, on the primary account's statement.",
        "Caps: ฿3,500 a month and ฿14,000 for the campaign, per primary account.",
        "Spend counted here can't count toward another Lotus's promotion.",
    )
