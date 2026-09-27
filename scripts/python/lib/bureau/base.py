"""BasePromotion — the contract every Promotion Bureau campaign implements.

deterministic + idempotent — pure functions of the transactions handed in.

Bank campaigns differ too much for one schema (NW3 is a stepped ladder on
pooled monthly spend; the next may be a flat rate, a merchant bonus, or
points), so each campaign is a subclass that states the bank's terms in code:

  code, title, card, campaign, source_url   what it is, and when
  tranches(pooled)                          the cashback ladder
  rules                                     what the bank excludes
  ladder_rows, examples, inclusions,
  crediting                                 the rest of the page summary

The shared machinery reads those declarations: `screen` checks a row against
`rules`, `allocate` hands the credit out first come, first served, and
`summary_blocks` renders the Bureau page. The page and the screening read one
list of rules, so they can't drift apart.
"""

from __future__ import annotations

import datetime as dt
import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import ROUND_DOWN, Decimal
from itertools import groupby
from typing import ClassVar

from .. import notion_blocks as nb

ELIGIBLE, UNCERTAIN, EXCLUDED = "eligible", "uncertain", "excluded"
SATANG = Decimal("0.01")

# A household prefix that still marks a real card purchase: the friend's share
# of a charge on Takumi's primary card. Any other `[…]` prefix (`[ยกเลิก]`,
# `[ยกยอด…]`, `[เว็บรับหนี้…]`) marks a ledger adjustment, not spend.
_PURCHASE_PREFIX = "[บัตรหลัก]"
_THAI = re.compile(r"[฀-๿]")


@dataclass(frozen=True)
class Tx:
    id: str
    holder: str
    name: str
    amount: Decimal
    date: str  # `Transaction Datetime` as stored: an ISO date, or a datetime

    @property
    def merchant(self) -> str:
        """The bank's merchant string, upper-cased, without `[บัตรหลัก]`."""
        return self.name.removeprefix(_PURCHASE_PREFIX).strip().upper()

    @property
    def is_card_purchase(self) -> bool:
        """False for payments, credits, transfers and other ledger entries.

        Card charges carry the bank's Latin-script merchant string; rows the
        household writes itself (`โอนยอดจาก…`, `ชำระ…`, `แลกคะแนน…`) are Thai.
        """
        name = self.name.removeprefix(_PURCHASE_PREFIX).strip()
        return self.amount > 0 and not name.startswith("[") and not _THAI.match(name) \
            and name.upper() != "AUTO DEBIT"


@dataclass(frozen=True)
class Rule:
    """One bank exclusion. `label` is the page text; the rest screens a row.

    A row hits when `pattern` matches its merchant string (or `test` returns
    True) and, if `over` is set, its amount is above it. A rule with neither
    `pattern` nor `test` is page-only — the merchant string can't show it.
    """

    label: str
    pattern: str | None = None
    over: Decimal | None = None
    test: Callable[[Tx], bool] | None = None
    level: str = EXCLUDED
    hint: str | None = None  # why an UNCERTAIN hit is only a maybe

    def hits(self, tx: Tx) -> bool:
        if self.pattern is None and self.test is None:
            return False
        if self.over is not None and tx.amount <= self.over:
            return False
        if self.pattern is not None and not re.search(self.pattern, tx.merchant):
            return False
        return self.test is None or self.test(tx)


@dataclass(frozen=True)
class Tranche:
    """A band of pooled spend, [start, end), that earns `credit` in total.

    The credit is spread evenly over the band's baht, so whoever's spend
    fills the band earns its slice of it.
    """

    start: Decimal
    end: Decimal
    credit: Decimal

    def earned(self, lo: Decimal, hi: Decimal) -> Decimal:
        overlap = min(hi, self.end) - max(lo, self.start)
        return overlap * self.credit / (self.end - self.start) if overlap > 0 else Decimal(0)

    def counted(self, lo: Decimal, hi: Decimal) -> Decimal:
        return max(min(hi, self.end) - max(lo, self.start), Decimal(0))


@dataclass(frozen=True)
class TxCredit:
    tx: Tx
    counted: Decimal  # baht of this row inside a paying tranche
    credit: Decimal   # unrounded


@dataclass
class Allocation:
    pooled: Decimal                 # every row's spend, all holders
    counted: Decimal                # the part inside paying tranches
    credit: Decimal                 # what the bank pays on `pooled`
    rows: list[TxCredit]
    shares: dict[str, Decimal]      # per holder, to the satang, summing to `credit`
    boundary: list[TxCredit] = field(default_factory=list)  # the date group the last paying step ends in


class BasePromotion(ABC):
    code: ClassVar[str]                 # the bank's registration code, e.g. "NW3"
    title: ClassVar[str]                # the bank's campaign name
    card: ClassVar[str]                 # card title in every holder's Cards DB
    campaign: ClassVar[tuple[dt.date, dt.date]]
    source_url: ClassVar[str]
    headline: ClassVar[str]             # short rate for tracker titles, e.g. "2%"

    rules: ClassVar[tuple[Rule, ...]] = ()
    ladder_rows: ClassVar[tuple[tuple[str, str], ...]] = ()
    examples: ClassVar[tuple[tuple[int, int], ...]] = ()  # the bank's own (spend, cashback)
    inclusions: ClassVar[tuple[str, ...]] = ()
    crediting: ClassVar[tuple[str, ...]] = ()

    @abstractmethod
    def tranches(self, pooled: Decimal) -> list[Tranche]:
        """The paying bands for one period's pooled spend."""

    # -- matching ---------------------------------------------------------

    @classmethod
    def matches(cls, bureau_name: str, start: dt.date, end: dt.date) -> bool:
        """Does a Bureau row with this Name and period belong to this campaign?"""
        first, last = cls.campaign
        return bool(re.search(rf"\b{re.escape(cls.code)}\b", bureau_name)) \
            and first <= start and end <= last

    # -- rules ------------------------------------------------------------

    def cashback(self, pooled: Decimal) -> Decimal:
        return sum((t.credit for t in self.tranches(pooled)), Decimal(0))

    def screen(self, tx: Tx) -> tuple[str, str | None]:
        """(level, reason) — the first rule the row hits, or ELIGIBLE."""
        if not tx.is_card_purchase:
            return EXCLUDED, "not a card purchase (payment, credit, transfer or adjustment)"
        for rule in self.rules:
            if rule.hits(tx):
                return rule.level, f"{rule.label} — {rule.hint}" if rule.hint else rule.label
        return ELIGIBLE, None

    # -- the household split ----------------------------------------------

    def allocate(self, txs: list[Tx]) -> Allocation:
        """Hand the credit out first come, first served by `Transaction Datetime`.

        Rows are walked in date order, filling the paying tranches; a row
        earns the credit on the part of it that lands inside one. Rows on the
        same date count as simultaneous — a shared bill split across holders,
        or any two charges whose order the ledger can't tell — so a date group
        that straddles a step shares its slice pro rata by amount.
        """
        spend = sorted((t for t in txs if t.amount > 0), key=lambda t: t.date)
        pooled = sum((t.amount for t in spend), Decimal(0))
        tranches = self.tranches(pooled)
        top = max((t.end for t in tranches), default=Decimal(0))

        rows: list[TxCredit] = []
        boundary: list[TxCredit] = []
        cum = Decimal(0)
        for _, grp in groupby(spend, key=lambda t: t.date):
            grp = list(grp)
            size = sum((t.amount for t in grp), Decimal(0))
            lo, hi = cum, cum + size
            earned = sum((b.earned(lo, hi) for b in tranches), Decimal(0))
            counted = sum((b.counted(lo, hi) for b in tranches), Decimal(0))
            credited = [TxCredit(t, counted * t.amount / size, earned * t.amount / size) for t in grp]
            rows += credited
            if lo < top < hi:
                boundary = credited
            cum = hi

        credit = self.cashback(pooled)
        raw: dict[str, Decimal] = {}
        for r in rows:
            raw[r.tx.holder] = raw.get(r.tx.holder, Decimal(0)) + r.credit
        return Allocation(
            pooled=pooled,
            counted=sum((r.counted for r in rows), Decimal(0)),
            credit=credit,
            rows=rows,
            shares=_round_to_total(raw, credit),
            boundary=boundary,
        )

    # -- Notion text --------------------------------------------------------

    def tracker_title(self, start: dt.date, end: dt.date) -> str:
        """`NW3 2% 1—30 Sep` — the household's naming for tracker rows."""
        span = (f"{start.day}—{end.day} {end:%b}" if (start.year, start.month) == (end.year, end.month)
                else f"{start.day} {start:%b}—{end.day} {end:%b}")
        return f"{self.code} {self.headline} {span}"

    def summary_blocks(self) -> list[dict]:
        """The Bureau page body: ladder, what counts, exclusions, crediting, split."""
        self._check_examples()
        first, last = self.campaign
        blocks = [
            nb.callout((f"{self.title} ({self.code})", "b"),
                       f" · {first:%-d %b %Y} – {last:%-d %b %Y} · {self.card} · ",
                       ("bank's terms", "", self.source_url)),
            nb.heading("Cashback ladder"),
            nb.table(["Pooled spend in the month", "Cashback"], [list(r) for r in self.ladder_rows]),
        ]
        if self.examples:
            blocks.append(nb.paragraph(("Bank's examples: ", "b"), " · ".join(
                f"฿{spend:,} → ฿{self.cashback(Decimal(spend)):,.0f}" for spend, _ in self.examples)))
        blocks += [nb.heading("What counts"), *(nb.bullet(i) for i in self.inclusions)]
        blocks += [nb.heading("Excluded"), *(nb.bullet(r.label) for r in self.rules)]
        blocks += [nb.heading("Crediting"), *(nb.bullet(c) for c in self.crediting)]
        blocks += [nb.heading("Household split"), *(nb.bullet(s) for s in _SPLIT_TEXT)]
        return blocks

    def _check_examples(self) -> None:
        wrong = [(s, want, self.cashback(Decimal(s))) for s, want in self.examples
                 if self.cashback(Decimal(s)) != want]
        if wrong:
            raise AssertionError(f"{type(self).__name__}.tranches disagrees with the bank: {wrong}")


_SPLIT_TEXT = (
    "Linked rows (รายการใช้จ่ายจาก…) are what the household counts toward this promotion.",
    "First come, first served by Transaction Datetime: only spend inside a paying step earns, "
    "and it goes to whoever spent it first. Spend past the last full step earns nothing.",
    "Same-date rows count as simultaneous (e.g. one bill split across holders): the part inside "
    "the step is shared pro rata by amount.",
)


def _round_to_total(raw: dict[str, Decimal], total: Decimal) -> dict[str, Decimal]:
    """Round each share down to the satang, then give the leftover satang to
    the largest remainders, so the shares add up to `total` exactly."""
    floor = {k: v.quantize(SATANG, rounding=ROUND_DOWN) for k, v in raw.items()}
    leftover = int((total.quantize(SATANG) - sum(floor.values(), Decimal(0))) / SATANG)
    for k in sorted(raw, key=lambda k: raw[k] - floor[k], reverse=True)[:max(leftover, 0)]:
        floor[k] += SATANG
    return floor
