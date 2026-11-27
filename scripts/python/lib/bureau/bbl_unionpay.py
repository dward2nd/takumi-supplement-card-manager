"""Bangkok Bank UnionPay 2% — all-spend cashback credit, 1 Jul 2026 – 30 Jun 2027.

deterministic + idempotent — declarations and pure functions only.

Terms from the card page
https://www.bangkokbank.com/th-TH/Personal/Cards/Credit-Cards/Bangkok-Bank-UnionPay-Credit-Card,
read for the Oct and Nov 2026 catalogue research and checked word for word on
2026-11-27 against the page saved as a PDF by the user (the site had timed out
here on 2026-11-26). docs/promotions/bbl-unionpay.md has the full reading:

  2% cashback credit on the month's spend once it reaches ฿2,000, in Thailand
  and abroad except China, online and in store, no registration. At most ฿1,000
  a customer a month (reached at ฿50,000) and ฿12,000 over the programme
  (12 × ฿1,000, so never binding alone). Principal and supplement spend
  combine. Credited within 60 days after the statement date, against the card
  balance. A separate 4% on ฿5,000+ a month spent in China in CNY (not online),
  with its own ฿1,000 a month cap, isn't modelled: the household has no China
  spend on it.

Takumi opened the card in Nov 2026 with a supplement for Baiboon (user,
2026-11-26), so the quota is one pool for both. The month is read as the
calendar month by transaction date. The terms only say "a month" (ต่อเดือน), so
the first statement will show whether the bank means its statement cycle
(day 10) instead.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal
from typing import ClassVar

from .. import promotions
from .base import EXCLUDED, Allocation, Rule, Tx, TxCredit
from .capped import CreditCapPromotion

RATE = Decimal("0.02")
MINIMUM = Decimal(2_000)    # the month's spend must reach this before anything earns


_CHINA = re.compile(r"\b(CN|CHN|CHINA)$")


def _china(tx: Tx) -> bool:
    return bool(_CHINA.search(tx.merchant.strip()))


class BBLUnionPayCashback(CreditCapPromotion):
    code = "BBL UnionPay"
    icon = "🤑"
    title = "บัตรเครดิตธนาคารกรุงเทพ ยูเนี่ยนเพย์ เครดิตเงินคืน 2%"
    cards = ("BBL UnionPay",)
    campaign = (dt.date(2026, 7, 1), dt.date(2027, 6, 30))
    source_url = "https://www.bangkokbank.com/th-TH/Personal/Cards/Credit-Cards/Bangkok-Bank-UnionPay-Credit-Card"
    headline = "2%"
    cap = Decimal(1_000)

    # Compared on 2026-11-26 with the household's other all-spend cashback: First Choice NW4,
    # UOB One's 1% and ttb so smart's 1%. No earlier round of this programme is in the vault.
    related: ClassVar = ("NW4", "UOB One", "ttb so smart")
    changes: ClassVar = (
        "Rate: a flat 2% on the month's whole spend once it reaches ฿2,000 (NW4: ฿200 per whole "
        "฿10,000, with ฿50 at ฿5,000–9,999; UOB One and ttb so smart: 1%, from the first baht).",
        "Cap: ฿1,000 a month per customer, reached at ฿50,000, and ฿12,000 for the programme (NW4: "
        "฿2,000 a month; UOB One 1% and ttb so smart: ฿2,000 a statement cycle).",
        "Period: a calendar month by transaction date (as NW4; UOB One 1% and ttb so smart count by "
        "statement cycle). The terms only say \"a month\"; unconfirmed until the first statement.",
        "What counts: almost everything, fuel, supermarkets, Makro PRO, e-wallet payments and foreign "
        "spend included. Left out: China, Alipay and WeChat Pay, funds, insurance, cash, interest, "
        "fees, fines, tax, foreign-currency purchases, BBL installments, cancelled and refunded "
        "charges. (NW4 leaves out "
        "marketplaces, delivery, travel, Makro, foreign spend and e-wallet top-ups; UOB One 1% and "
        "ttb so smart leave out fuel; ttb so smart also 7-Eleven and TrueMoney.)",
        "Registration: none (NW4 needs it; UOB One's and ttb so smart's are card benefits too).",
        "Crediting: within 60 days after the statement date, onto the card (NW4: within 60 days after "
        "each month-end; UOB One: on the statement; ttb so smart: into a ttb no fixed account).",
        "Points: the terms list Thank You Rewards points (1 per ฿25) and the cashback side by side and "
        "never say one replaces the other, so rows keep earning points (NW4 rows keep First Choice "
        "points too; UOB One earns none; Bangkok Bank Titanium pays cashback instead of points).",
    )

    def rate(self, tx: Tx) -> Decimal | None:
        if any(r.level == EXCLUDED and r.hits(tx) for r in self.rules):
            return None
        return RATE

    def qualifies(self, tx: Tx) -> bool:
        """Every purchase is the kind of spend this counts; the rules say which are
        left out, and the screen names the rule."""
        return True

    def counts_linked(self, tx: Tx) -> bool:
        return self.rate(tx) is not None

    def split(self, txs: list[Tx]) -> Allocation:
        """The credit cap, but only once the month's counted spend reaches ฿2,000:
        below it nobody earns, and every row shows `% cb` unset."""
        spend = sum((t.amount for t in txs if t.amount > 0 and self.counts_linked(t)), Decimal(0))
        alloc = super().split(txs)
        if spend >= MINIMUM:
            return alloc
        rows = [TxCredit(r.tx, Decimal(0), Decimal(0)) for r in alloc.rows]
        short = [f"the month's spend is ฿{spend:,.2f}, under the ฿2,000 it needs before anything earns"] \
            if spend else []
        return self._allocation(rows, [], [*alloc.warnings, *short], credit=Decimal(0))

    ladder_title = "Cashback"
    ladder_header = ("Spend in the calendar month", "Cashback")
    ladder_rows: ClassVar = (
        ("under ฿2,000", "nothing"),
        ("฿2,000 or more", "2% of all of it"),
        ("Cap", "฿1,000 a month per customer (reached at ฿50,000), ฿12,000 for the programme"),
    )
    inclusions: ClassVar = (
        "Every purchase on the BBL UnionPay, in Thailand or abroad (not China), online and in store. "
        "Takumi's principal and Baiboon's supplement pool into one quota; the credit lands on the "
        "principal's card.",
        "No registration.",
        "Foreign spend is converted at the rate of its posting date as printed on the principal "
        "card's statement.",
        "Read as the calendar month by transaction date. If the first statement shows the bank "
        "counting by its statement cycle (day 10), switch `period_basis` to \"bill_cycle\".",
        "China in CNY (not online) earns a separate 4% on ฿5,000+ a month, with its own ฿1,000 a "
        "month and ฿12,000 caps (the terms don't say whether the two caps are shared); not modelled.",
    )
    rules: ClassVar = (
        Rule("Spending in China (the separate 4% in CNY isn't modelled)", test=_china),
        Rule("E-wallet payments through Alipay and WeChat Pay", r"ALIPAY|WECHAT|WEIXIN|TENPAY"),
        Rule("Securities and funds (MCC 6211)", r"SECURITIES|\bFUND\b|\bRMF\b|\bSSF\b|ASSET MANAGEMENT"),
        Rule("Insurance (MCC 5960, 6300, 6381, 6399)", r"INSURANCE|ASSURANCE|\bAIA\b|\bFWD\b|ALLIANZ|ประกัน"),
        Rule("Cash advances (MCC 6010, 6011 or TC 30, 31)", r"CASH ADVANCE|CASH WITHDRAW|\bATM\b"),
        Rule("Interest (TC 11–13) and fees of every kind (MCC 6012, 4829)",
             r"\bFEE\b|INTEREST|LATE CHARGE|PENALTY"),
        Rule("Fines (MCC 9222) and tax (MCC 7276, 9311)", r"REVENUE DEP|\bTAX\b|กรมสรรพากร"),
        Rule("Foreign-currency purchases (exchange counters)", r"SUPER ?RICH|EXCHANGE"),
        Rule("Bangkok Bank installments (Be Smart; not offered on UnionPay cards)",
             test=lambda tx: promotions.is_installment(tx.name)),
        Rule("Cancelled charges and goods returned later (TC 41, 43); a tourist tax refund comes off "
             "the spend"),
    )
    crediting: ClassVar = (
        "Within 60 days after the statement date (ภายใน 60 วันหลังจากสรุปยอดบัญชี), against the "
        "principal card's balance; it shows on a later statement.",
        "Only for a cardholder still holding the card, with no missed payment and no breach of the "
        "card terms, up to the day of crediting. It can't be cashed or transferred, and the bank can "
        "take it back if a qualifying charge is cancelled later.",
    )

