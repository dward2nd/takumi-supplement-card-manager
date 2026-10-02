"""Krungsri First Choice NW4 — "รูดก็ได้เงินคืน กดก็ได้แคชเบ็ค", 1 Oct – 31 Dec 2026.

deterministic + idempotent — declarations and pure functions only.

Terms read from https://www.firstchoice.co.th/promotion/firstchoice-cashback
on 2026-10-01. NW3's successor, with the same ladder but a smaller top:

  ฿5,000–9,999 of pooled full-amount spend in the month → ฿50; every whole
  ฿10,000 → ฿200 (2%), up to ฿2,000 (reached at ฿100,000). NW3's +฿500 at
  ฿200,000 is gone, so the monthly cap is ฿2,000 and the campaign's ฿6,000 is
  3 × that, never binding alone.

What changed in what counts:

  - Supermarket and fuel spend each count only up to ฿30,000 a month per
    primary account. The part past ฿30,000 is left out of the ladder; the part
    up to it counts as usual (NW3 dropped single charges over ฿10,000 / ฿3,000
    instead). `split` caps them first come, first served.
  - MCC 5199 is out. `WWW.MAKRO.PRO` posts under 5199; `HTTPS://WWW.MAKRO.PRO/`
    is 5411, a supermarket (see the AEON World card YAML).
  - The campaigns NW4 points marketplaces, delivery, travel and insurance to
    are now ON4, DLV3, TR3 and IS4.

The page's second part (a bonus on cash advances) needs a cash advance, which the
household doesn't take; it isn't modelled.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import replace
from decimal import Decimal
from itertools import groupby
from typing import ClassVar

from .. import promotions
from .base import Allocation, Rule, Tx, TxCredit
from .ladder import Tranche
from .nw3 import NW3Promotion, _foreign

STEP = Decimal(10_000)
RATE = Decimal("0.02")
STEP_CAP = Decimal(100_000)    # 10 steps × ฿200 = the ฿2,000 monthly cap
CATEGORY_CAP = Decimal(30_000)

_MCC_5199 = re.compile(r"^WWW\.MAKRO\.PRO")
_SUPERMARKET = re.compile(r"BIG ?C\b|BIGC|LOTUS|\bTOPS\b|VILLA|GOURMET|HOME FRESH|MAX ?VALU|FOODLAND|"
                          r"RIMPING|\bCFW-|GO ?WHOLESALE|MAKRO|CP AXTRA")


def _supermarket(tx: Tx) -> bool:
    return bool(_SUPERMARKET.search(tx.merchant))


def _fuel(tx: Tx) -> bool:
    return promotions.looks_petrol(tx.merchant)


class NW4Promotion(NW3Promotion):
    code = "NW4"
    title = "รูดก็ได้เงินคืน กดก็ได้แคชเบ็ค"
    campaign = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
    source_url = "https://www.firstchoice.co.th/promotion/firstchoice-cashback"
    headline = "2%"

    # Spend a category can bring to the ladder each month, per primary account.
    category_caps: ClassVar = (("supermarkets", _supermarket, CATEGORY_CAP), ("fuel", _fuel, CATEGORY_CAP))

    def tranches(self, pooled: Decimal) -> list[Tranche]:
        if pooled < 5_000:
            return []
        if pooled < STEP:
            return [Tranche(Decimal(0), Decimal(5_000), Decimal(50))]
        counted = min(pooled // STEP * STEP, STEP_CAP)
        return [Tranche(Decimal(0), counted, counted * RATE)]

    def countable(self, txs: list[Tx]) -> dict[str, Decimal]:
        """Each row's baht the ladder may count: supermarket and fuel rows share
        their ฿30,000 first come, first served; a same-time group crossing it
        shares what's left pro rata by amount."""
        room = {label: cap for label, _, cap in self.category_caps}
        out: dict[str, Decimal] = {}
        spend = sorted((t for t in txs if t.amount > 0), key=lambda t: t.when)
        for _, grp in groupby(spend, key=lambda t: t.when):
            grp = list(grp)
            for label, test, _ in self.category_caps:
                hits = [t for t in grp if test(t) and t.id not in out]
                size = sum((t.amount for t in hits), Decimal(0))
                if not size:
                    continue
                share = min(room[label], size) / size
                room[label] -= min(room[label], size)
                out |= {t.id: t.amount * share for t in hits}
            out |= {t.id: t.amount for t in grp if t.id not in out}
        return out

    def split(self, txs: list[Tx]) -> Allocation:
        """The ladder over what `countable` lets through; each row keeps its own
        amount, so a row cut by a category cap earns on part of itself only."""
        countable = self.countable(txs)
        shadow = [replace(t, amount=countable[t.id]) for t in txs if countable.get(t.id)]
        inner = super().split(shadow)
        by_id = {t.id: t for t in txs}
        credited = {r.tx.id: r for r in inner.rows}
        rows = [TxCredit(t, credited[t.id].counted, credited[t.id].credit) if t.id in credited
                else TxCredit(t, Decimal(0), Decimal(0))
                for t in sorted((t for t in txs if t.amount > 0), key=lambda t: t.when)]
        boundary = [TxCredit(by_id[r.tx.id], r.counted, r.credit) for r in inner.boundary]
        capped = [t for t in txs if t.amount > 0 and countable.get(t.id, t.amount) < t.amount]
        warnings = inner.warnings + ([f"{len(capped)} supermarket/fuel row(s) past the ฿30,000 a month "
                                      f"count only in part or not at all"] if capped else [])
        return self._allocation(rows, boundary, warnings, credit=inner.credit)

    ladder_rows: ClassVar = (
        ("under ฿5,000", "nothing"),
        ("฿5,000 – 9,999", "฿50 flat"),
        ("every whole ฿10,000", "฿200 (2%) — up to ฿2,000, reached at ฿100,000: the monthly cap"),
    )
    examples: ClassVar = (
        (4_900, 0), (5_000, 50), (8_000, 50), (10_000, 200), (30_000, 600), (120_000, 2_000),
        (200_000, 2_000),
    )
    inclusions: ClassVar = (
        "Full-amount (รูดเต็มจำนวน) purchases on the Krungsri First Choice Visa Platinum, pooled per "
        "calendar month on the primary account (Takumi's). The bank credits the primary account only.",
        "Steps, not a smooth 2%: ฿39,999 earns the same ฿600 as ฿30,000.",
        "Supermarket spend (Big C, Lotus's, Tops, Villa, Gourmet, Home Fresh Mart, MaxValu, Foodland, "
        "their online stores …) and fuel each count up to ฿30,000 a month; the part past that is left "
        "out, first come, first served.",
        "Dated by the statement's transaction date, net of discounts. A charge the merchant hasn't "
        "settled within 30 days of month-end doesn't count.",
        "Counts from the moment registration is confirmed: UCHOOSE → \"NW4\", or SMS \"NW4 <16-digit "
        "card no.>\" to 081-256-3333. NW4 registrants with more than ฿10,000 of NW3 spend in both Jul "
        "and Aug 2026 were enrolled for the whole of Oct–Dec.",
    )
    rules: ClassVar = (
        Rule("Installments (ผ่อน) — including 0% merchant plans on the personal-loan line",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Marketplaces: Shopee, Lazada, TikTok (ON4 covers them)", r"SHOPEE(?! ?FOOD)|LAZADA|TIKTOK"),
        Rule("Food delivery: LINE MAN, ShopeeFood, Robinhood, Bolt, and everything in the Grab app "
             "(DLV3)", r"LINE ?MAN|SHOPEE ?FOOD|ROBINHOOD|\bBOLT\b|GRAB"),
        Rule("Travel: flights, hotels, travel agencies, car booking & rental, duty-free (TR3)",
             r"AGODA|BOOKING\.COM|EXPEDIA|TRAVELOKA|TRIP\.COM|CTRIP|AIR ?ASIA|AIRWAYS|AIRLINES|"
             r"NOK ?AIR|VIETJET|LION AIR|HOTEL|RESORT|AIRBNB|KING ?POWER|DUTY ?FREE|HERTZ|\bAVIS\b"),
        Rule("Insurance of any kind (IS4)", r"INSURANCE|ASSURANCE|\bAIA\b|\bFWD\b|ALLIANZ|ประกัน"),
        Rule("MCC 5199 — `WWW.MAKRO.PRO` (Makro PRO's `HTTPS://WWW.MAKRO.PRO/` is 5411 and counts)",
             _MCC_5199.pattern),
        Rule("Utilities: electricity, water, landline (MCC 4900, 9402)",
             r"\b(MEA|PEA|MWA|PWA)\b|ELECTRICITY|WATERWORKS|การไฟฟ้า|การประปา"),
        Rule("Government bodies — taxes, state fees, some public hospitals (MCC 9399, 9405, 7800) — "
             "and public organizations (องค์การมหาชน) such as Museum Siam",
             r"MUSEUM SIAM|REVENUE DEP|GOVERNMENT|MINISTRY|DEPARTMENT OF|กรม|องค์การ"),
        Rule("Gold and jewellery shops, e-wallet payments there included", r"\bGOLD\b|JEWEL|ทอง"),
        Rule("Financial services: funds (RMF/SSF), brokers, currency exchange, crypto & digital assets",
             r"\bFUND\b|\bRMF\b|\bSSF\b|SECURITIES|ASSET MANAGEMENT|BITKUB|BINANCE|CRYPTO|SUPER ?RICH"),
        Rule("Spending abroad or in foreign currency, and baht charges from foreign-registered sites "
             "(Amazon, Google, Facebook, Agoda, Expedia, Traveloka, Booking.com …)", test=_foreign),
        Rule("Recurring monthly or yearly auto-debits (subscriptions)",
             r"NETFLIX|SPOTIFY|YOUTUBE|DISNEY|\bHBO\b|ITUNES|APPLE\.COM|OPENAI|CHATGPT|CANVA|ADOBE"),
        Rule("Interest, fees and penalties; charges later cancelled or refunded",
             r"\bFEE\b|INTEREST|LATE CHARGE|PENALTY"),
        # Page-only, as for NW3: the app's NW3 list counted TrueMoney card payments.
        Rule("E-wallet top-ups (TrueMoney, Rabbit LINE Pay, ShopeePay …). Card payments made through "
             "TrueMoney (TMN*…) still count, as they did for NW3"),
    )
    crediting: ClassVar = (
        "Within 60 days after each month-end, to the primary account; it shows on the statement.",
        "Taken back if a counted charge is later cancelled or refunded.",
        "Caps: ฿2,000 a month and ฿6,000 for the campaign, per primary account.",
    )
