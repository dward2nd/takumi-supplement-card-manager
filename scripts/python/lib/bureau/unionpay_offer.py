"""UnionPay International's offer pages — how much of a monthly offer's pool is left.

deterministic + idempotent — read-only HTTP GETs against UnionPay's public API.

The offer page (`marketing.unionpayintl.com/offer-promote/…#/merchant?merchantNo=…`)
is a JavaScript app over a JSON API (read 2026-09-30):

  h5Promote/v1/coupon/getMerchantCouponList?merchantNo=…&insCode=…&language=en
      the merchant's offers, one per month: `couponno`, `startDate`, `endDate`
  h5Promote/v1/coupon/flushProcess?couponno=…&couponType=07&insCode=…&language=en
      `show` "1" once the month has started; `percent` the share of the pool left

The page shows "left N%" while `percent` > 0, "Coming soon" before the month
starts, and "The budget for today has been used up" once `percent` is 0 — the
state September 2026 was in from 12 Sep.
"""

from __future__ import annotations

import datetime as dt
import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from decimal import Decimal
from functools import cache

from .quota import LIVE, NOT_STARTED, UNLISTED, USED_UP, QuotaSource, QuotaStatus

API = "https://marketing.unionpayintl.com/h5Promote/v1/"
PAGE = "https://marketing.unionpayintl.com/offer-promote/?language=en&insCode={ins}#/offer?offerNo={offer}"
TIMEOUT = 15


def _get(path: str, **params: str) -> dict:
    url = f"{API}{path}?{urllib.parse.urlencode(params)}"
    # The API turns away Python's default User-Agent (403).
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


@cache
def _offers(merchant: str, ins_code: str) -> tuple[tuple[str, dt.date, dt.date], ...]:
    """(offer number, first day, last day) for each month the merchant lists; read once per process."""
    data = _get("coupon/getMerchantCouponList", merchantNo=merchant, insCode=ins_code,
                language="en", currCode="THB")
    return tuple((c["couponno"], dt.date.fromisoformat(c["startDate"][:10]), dt.date.fromisoformat(c["endDate"][:10]))
                 for c in data.get("couponList") or [])


@dataclass(frozen=True)
class UnionPayOffer(QuotaSource):
    merchant: str    # UnionPay's merchant number for the offer ("all merchants in Thailand …")
    ins_code: str    # the issuer-side code the page is opened with

    @property
    def name(self) -> str:
        return "UnionPay's offer page"

    def status(self, start: dt.date, end: dt.date) -> QuotaStatus:
        now = dt.datetime.now(dt.timezone.utc)
        offer = next((no for no, first, last in _offers(self.merchant, self.ins_code)
                      if first <= start and end <= last), None)
        if offer is None:
            return QuotaStatus(UNLISTED, None, None, None, now)
        data = _get("coupon/flushProcess", couponno=offer, couponType="07", insCode=self.ins_code,
                    language="en")["data"]
        left = Decimal(str(data.get("percent") or 0))
        state = NOT_STARTED if data.get("show") != "1" else LIVE if left > 0 else USED_UP
        return QuotaStatus(state, left, offer, PAGE.format(ins=self.ins_code, offer=offer), now)
