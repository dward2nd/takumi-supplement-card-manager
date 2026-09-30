"""UnionPay QR — 6% off at every merchant in Thailand taking UnionPay QR, month by month from Sep 2026.

deterministic + idempotent — declarations and pure functions only (the pool
is read by `lib.bureau.quota` through `quota`).

Terms read from UnionPay International's offer page on 2026-09-30 (verbatim in
docs/sources/unionpay-qr-terms-2026-09-30.txt): "Get 6% off up to THB 60/card/
sales slip/day, and up to THB 300/card/month when register and paying with
UnionPay QR Code", through the KTC Mobile app among others. One redemption per
card a day; 12,000 redemptions a month nationwide, first come first served
(144,000 over the campaign, so presumably twelve months; UnionPay lists
September 2026 to January 2027 so far). Each month is its own offer, and each
card has to be registered for it.

UnionPay takes the discount off at payment and KTC charges the rest, so the
ledger row is already the net amount (user, 2026-09-30) — the shape is
`InstantDiscountPromotion`. The quota is per card number, and Baiboon's …2310
is a card of its own beside Takumi's …1346 (user, 2026-09-30): one Bureau row
per card a month. Takumi and Baiboon pay with KTC UnionPay by QR only (user,
2026-09-30), so every domestic purchase on these cards counts; `… CITY TH`
merchants are micro-merchants that take QR and little else. Nuta's KTC
UnionPay isn't registered.

September 2026's pool was gone on 12 Sep (UnionPay's Facebook page, 12 Sep:
"สิทธิ์ UnionPay QR เดือนก.ย. 69 เต็มแล้ว … เติมสิทธิ์อีกครั้ง 1 ต.ค. 69"), which
the ledger agrees with: the last discounted amounts are 9–10 Sep, and from
13 Sep the charges are whole prices.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .accounts import CardNumber
from .base import Rule, Tx
from .instant import InstantDiscountPromotion
from .unionpay_offer import UnionPayOffer

MERCHANT = "898463728627768"   # "All merchants in Thailand accepted UnionPay QRC"
INS_CODE = "299990156"

_DOMESTIC = re.compile(r"\bTHA?$")
_ONLINE = re.compile(r"WWW\.|HTTPS?:|\.COM\b|\.CO\.TH|SHOPEE|LAZADA|TIKTOK|2C2P|OMISE|GBPRIME|GOOGLE|"
                     r"APPLE\.COM|NETFLIX|SPOTIFY|YOUTUBE|STEAM|AMAZON")


class UnionPayQR(InstantDiscountPromotion):
    code = "UnionPay QR"
    icon = "📲"
    title = "UnionPay QR — Get 6% off at all merchants in Thailand accepting UnionPay QR"
    cards = ("KTC UnionPay",)
    campaign = (dt.date(2026, 9, 1), dt.date(2027, 1, 31))   # the months UnionPay lists so far
    source_url = f"https://marketing.unionpayintl.com/offer-promote/?language=en&insCode={INS_CODE}" \
                 f"&countryCode=764#/merchant?merchantNo={MERCHANT}"
    headline = "6%"

    rate = Decimal("0.06")
    per_slip = Decimal(60)
    per_day = 1
    cap = Decimal(300)
    quota = UnionPayOffer(merchant=MERCHANT, ins_code=INS_CODE)

    @property
    def authoritative_period(self) -> bool:
        # The discount is taken at payment, so the month is the payment's own date:
        # a row edited out of the month (or onto the other card number) leaves the row.
        return True

    def qualifies(self, tx: Tx) -> bool:
        return bool(_DOMESTIC.search(tx.merchant)) and not promotions.is_installment(tx.name)

    ladder_title = "Discount per slip"
    ladder_header = ("Slip", "Discount")
    ladder_rows: ClassVar = (
        ("Paid by UnionPay QR in KTC Mobile, card registered for the month", "6% off the price"),
        ("Most per slip", "฿60 (a ฿1,000 price)"),
        ("Per card", "1 discounted slip a day, ฿300 a month"),
        ("UnionPay's pool", "12,000 discounts a month nationwide, first come first served"),
    )
    inclusions: ClassVar = (
        "Per calendar month by the payment's date, and per card number: Takumi's …1346 (with Baiboon's "
        "[บัตรหลัก] shares on it) and Baiboon's own …2310, each with its own ฿300 and one slip a day.",
        "Every month is its own offer: register each card for it on UnionPay's page.",
        "Takumi and Baiboon pay with KTC UnionPay by QR only (user, 2026-09-30), so every domestic purchase "
        "on these cards counts. `… CITY TH` merchants are micro-merchants that take QR and little else.",
        "The discount is in the charge: ยอดชำระ is the price less 6%. ฿67.68 was a ฿72 price with ฿4.32 off.",
    )
    rules: ClassVar = (
        Rule("Online and in-app card payments (not UnionPay QR)", _ONLINE.pattern),
        Rule("Installments", test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Merchants abroad (the offer is for merchants in Thailand)"),
        Rule("A payment another UnionPay promotion takes: one promotion per payment, the best one"),
        Rule("Refunds: the discount isn't refunded"),
    )
    crediting: ClassVar = (
        "None: UnionPay takes the discount off at payment and KTC charges the rest. No % cb, no tracker "
        "rows, no credit rows.",
        "Quotas Exceeded Date is the day UnionPay's monthly pool ran out: first seen used up on the offer page by a "
        "sync, or set from UnionPay's Facebook post. From that day nothing is discounted.",
    )
    split_text: ClassVar = (
        "Each discount belongs to whoever's slip it was: first come first served by Transaction Datetime, "
        "the day's first slip, until the card's ฿300 or the pool runs out.",
        "A slip's net amount shows whether the discount was taken: ฿67.68 (94% of ฿72) was, ฿50 wasn't; "
        "a slip that shows none doesn't use the day's discount. One over ฿940 can't show it (a ฿60 "
        "discount fits any price), so the terms decide.",
        "A [บัตรหลัก] share and Takumi's part of the same charge are one slip; its discount is split pro rata.",
    )


class UnionPayQR1346(CardNumber, UnionPayQR):
    number, holder = "1346", "takumi"


class UnionPayQR2310(CardNumber, UnionPayQR):
    number, holder = "2310", "baiboon"


ACCOUNTS = (UnionPayQR1346, UnionPayQR2310)
