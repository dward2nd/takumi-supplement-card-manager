"""BasePromotion — the contract every Promotion Bureau campaign implements.

deterministic + idempotent — pure functions of the transactions handed in.

Bank campaigns differ too much for one schema, so the payout *shape* is a
class too:

  BasePromotion            identity, matching, screening, the FCFS walk, the page
  ├── CashbackPromotion    baht shares, trackers, the `% cb` rule
  │   ├── LadderPromotion      (ladder.py) tranches of pooled spend — NW3, EPW538
  │   └── CreditCapPromotion   (capped.py) a per-row rate until a credit cap — UOB One
  └── UOBWorldBonus        (uob_world.py) a points quota

and each campaign subclasses its shape, stating the bank's terms in code:
code, title, cards, campaign, source_url; what counts (`qualifies`, `rules`);
the payout; and the page text. `screen` and `summary_blocks` read the same
`rules`, so the page and the screening can't drift apart.
"""

from __future__ import annotations

import datetime as dt
import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import ROUND_DOWN, Decimal
from itertools import groupby
from typing import Any, ClassVar

from .. import notion_blocks as nb

ELIGIBLE, UNCERTAIN, EXCLUDED = "eligible", "uncertain", "excluded"
CASHBACK, POINTS = "cashback", "points"
SATANG = Decimal("0.01")

# A household prefix that still marks a real card purchase: the friend's share
# of a charge on Takumi's primary card. Any other `[…]` prefix (`[ยกเลิก]`,
# `[ยกยอด…]`, `[เว็บรับหนี้…]`) marks a ledger adjustment, not spend.
_PURCHASE_PREFIX = "[บัตรหลัก]"
_THAI = re.compile(r"[฀-๿]")
# Household ledger entries that start in Latin script: the bank's auto-debit
# payment, and the balance-and-points reset (docs/concepts/ledger-reset.md).
# Thai *inside* a name is no sign: `traveloka เที่ยวบิน …` is a real purchase.
_LATIN_LEDGER_ENTRIES = ("AUTO DEBIT", "RESET ")


@dataclass(frozen=True)
class Tx:
    id: str
    holder: str
    name: str
    amount: Decimal
    date: str  # `Transaction Datetime` as stored: an ISO date, or a datetime
    cb: Decimal | None = None             # `% cb` as stored (raw fraction)
    multiplier: str | None = None         # the checked multiplier box; None = ×1
    points_used: Decimal | None = None    # `ใช้คะแนน`
    note: str = ""
    card: str = ""                        # the Card relation's title
    bill_cycle: str | None = None         # `Bill Cycle Date`

    @property
    def when(self) -> tuple:
        """FCFS order key: the day, then untimed rows (order unknown) before timed ones.

        Two rows with an equal key are simultaneous. Give both shares of a split
        charge the same time, or none, so they stay one group.
        """
        day, _, time = self.date.partition("T")
        return (day, bool(time), dt.datetime.fromisoformat(self.date) if time else None)

    @property
    def day(self) -> dt.date:
        return dt.date.fromisoformat(self.date[:10])

    @property
    def merchant(self) -> str:
        """The bank's merchant string, upper-cased, without `[บัตรหลัก]`."""
        return self.name.removeprefix(_PURCHASE_PREFIX).strip().upper()

    @property
    def is_card_purchase(self) -> bool:
        """False for payments, credits, transfers and other ledger entries.

        Card charges carry the bank's Latin-script merchant string; rows the
        household writes itself (`โอนยอดจาก…`, `ชำระ…`, `แลกคะแนน…`) start in Thai,
        with a couple of Latin-led exceptions (`_LATIN_LEDGER_ENTRIES`).
        """
        name = self.name.removeprefix(_PURCHASE_PREFIX).strip()
        return self.amount > 0 and not name.startswith("[") and not _THAI.match(name) \
            and not name.upper().startswith(_LATIN_LEDGER_ENTRIES)


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
class TxCredit:
    tx: Tx
    counted: Decimal  # baht of this row inside the quota
    credit: Decimal   # unrounded baht (0 for a points campaign)


@dataclass
class Allocation:
    pooled: Decimal                 # every counted row's spend, all holders
    counted: Decimal                # the part inside the quota
    credit: Decimal                 # what the bank pays in baht (0 for points)
    rows: list[TxCredit]
    shares: dict[str, Decimal]      # per holder, to the satang, summing to `credit`
    boundary: list[TxCredit] = field(default_factory=list)  # the group the quota ends in
    warnings: list[str] = field(default_factory=list)


class BasePromotion(ABC):
    code: ClassVar[str]                 # the bank's code or a short name, e.g. "NW3"
    title: ClassVar[str]                # the bank's campaign name
    cards: ClassVar[tuple[str, ...]]    # card titles as in each holder's Cards DB
    campaign: ClassVar[tuple[dt.date, dt.date | None]]  # None = open-ended
    source_url: ClassVar[str]
    headline: ClassVar[str]             # short rate for tracker titles, e.g. "2%"

    reward: ClassVar[str]               # CASHBACK or POINTS
    period_basis: ClassVar[str] = "transaction_date"  # or "bill_cycle": Bureau End = the BC date
    name_pattern: ClassVar[str | None] = None         # regex on the Bureau Name; default: the code

    rules: ClassVar[tuple[Rule, ...]] = ()
    ladder_title: ClassVar[str] = "Cashback ladder"
    ladder_header: ClassVar[tuple[str, str]] = ("Pooled spend in the month", "Cashback")
    ladder_rows: ClassVar[tuple[tuple[str, str], ...]] = ()
    inclusions: ClassVar[tuple[str, ...]] = ()
    crediting: ClassVar[tuple[str, ...]] = ()
    split_text: ClassVar[tuple[str, ...]] = ()           # how the household shares it (page text)

    # -- matching ---------------------------------------------------------

    @classmethod
    def matches(cls, bureau_name: str, start: dt.date, end: dt.date) -> bool:
        """Does a Bureau row with this Name and period belong to this campaign?"""
        first, last = cls.campaign
        pattern = cls.name_pattern or rf"\b{re.escape(cls.code)}\b"
        return bool(re.search(pattern, bureau_name)) and first <= start and (last is None or end <= last)

    # -- rules ------------------------------------------------------------

    def qualifies(self, tx: Tx) -> bool:
        """Is the row the kind of spend this quota counts? Default: any purchase."""
        return True

    def screen(self, tx: Tx) -> tuple[str, str | None]:
        """(level, reason): not a purchase, not counted here, the first rule hit, or ELIGIBLE."""
        if not tx.is_card_purchase:
            return EXCLUDED, "not a card purchase (payment, credit, transfer or adjustment)"
        if not self.qualifies(tx):
            return EXCLUDED, f"not counted by {self.code} {self.headline}"
        for rule in self.rules:
            if rule.hits(tx):
                return rule.level, f"{rule.label} — {rule.hint}" if rule.hint else rule.label
        return ELIGIBLE, None

    # -- the household split ----------------------------------------------

    @abstractmethod
    def allocate(self, txs: list[Tx]) -> Allocation:
        """Hand the period's reward out first come, first served (see `_walk`)."""

    def _walk(self, txs: list[Tx], take: Callable[[Decimal, Decimal, list[Tx]], list[TxCredit]]
              ) -> tuple[list[TxCredit], list[TxCredit], list[str]]:
        """Walk rows first come, first served by `Transaction Datetime`.

        Rows with the same value count as simultaneous (a shared bill split
        across holders, or date-only rows whose order the ledger can't tell), so
        `take` gets one same-time group at a time, with the pooled spend before
        and after it. The group the quota ends in is returned as the boundary.
        Only its day needs exact order; give that day's rows times to settle it.
        """
        spend = sorted((t for t in txs if t.amount > 0), key=lambda t: t.when)
        rows: list[TxCredit] = []
        boundary: list[TxCredit] = []
        cum = Decimal(0)
        for _, grp in groupby(spend, key=lambda t: t.when):
            grp = list(grp)
            size = sum((t.amount for t in grp), Decimal(0))
            credited = take(cum, cum + size, grp)
            rows += credited
            if any(0 < r.counted < r.tx.amount for r in credited):
                boundary = credited
            cum += size

        warnings = []
        if boundary:
            day = boundary[0].tx.when[0]
            if len({t.when[1] for t in spend if t.when[0] == day}) > 1:
                warnings.append(f"{day} mixes timed and date-only rows and the quota ends that day; "
                                f"the date-only ones are placed first — give them times too")
        return rows, boundary, warnings

    def _allocation(self, rows: list[TxCredit], boundary: list[TxCredit], warnings: list[str], *,
                    credit: Decimal) -> Allocation:
        raw: dict[str, Decimal] = {}
        for r in rows:
            raw[r.tx.holder] = raw.get(r.tx.holder, Decimal(0)) + r.credit
        return Allocation(
            pooled=sum((r.tx.amount for r in rows), Decimal(0)),
            counted=sum((r.counted for r in rows), Decimal(0)),
            credit=credit,
            rows=rows,
            shares=_round_to_total(raw, credit) if self.reward == CASHBACK else {},
            boundary=boundary,
            warnings=warnings,
        )

    @abstractmethod
    def expected(self, r: TxCredit) -> dict[str, Any]:
        """The fields a row should carry after the split, as /update-transaction keys."""

    def suggested_note(self, r: TxCredit) -> str | None:
        """A Note to propose alongside a fix, when the household has a convention for it."""
        return None

    # -- Notion text --------------------------------------------------------

    def tracker_title(self, start: dt.date, end: dt.date) -> str:
        """`NW3 2% 1—30 Sep` — the household's naming for tracker rows."""
        span = (f"{start.day}—{end.day} {end:%b}" if (start.year, start.month) == (end.year, end.month)
                else f"{start.day} {start:%b}—{end.day} {end:%b}")
        return f"{self.code} {self.headline} {span}"

    def summary_blocks(self) -> list[dict]:
        """The Bureau page body: ladder, what counts, exclusions, crediting, split."""
        first, last = self.campaign
        span = f"{first:%-d %b %Y} – {last:%-d %b %Y}" if last else f"since {first:%-d %b %Y}"
        blocks = [
            nb.callout((f"{self.title} ({self.code})", "b"), f" · {span} · {', '.join(self.cards)} · ",
                       ("bank's terms", "", self.source_url)),
            nb.heading(self.ladder_title),
            nb.table(list(self.ladder_header), [list(r) for r in self.ladder_rows]),
        ]
        blocks += self._ladder_extras()
        blocks += [nb.heading("What counts"), *(nb.bullet(i) for i in self.inclusions)]
        if self.rules:
            blocks += [nb.heading("Excluded"), *(nb.bullet(r.label) for r in self.rules)]
        blocks += [nb.heading("Crediting"), *(nb.bullet(c) for c in self.crediting)]
        blocks += [nb.heading("Household split"), *(nb.bullet(s) for s in self.split_text)]
        return blocks

    def _ladder_extras(self) -> list[dict]:
        """Blocks to show right under the ladder table (a subclass's worked examples)."""
        return []


class CashbackPromotion(BasePromotion):
    """A campaign paid in baht: shares per holder, tracker rows, and `% cb` on rows."""

    reward = CASHBACK
    # Whether this campaign's split is what a row's `% cb` shows. A row has one
    # `% cb`, but it can earn from two campaigns (UOB One's 1% and EPW538), so
    # only the card's own cashback claims it. An overlay paid as a lump sum on
    # top (EPW538) sets this False and lives in the trackers alone.
    marks_rows: ClassVar[bool] = True

    def expected(self, r: TxCredit) -> dict[str, Any]:
        """The full rate when the whole row earns; `% cb` unset when only part of
        it does (the row or same-time group the quota ends in) or none of it does
        (user, 2026-09-28). The exact money lives in the Bureau's share fields
        and the trackers, not here."""
        if not self.marks_rows:
            return {}
        if r.counted != r.tx.amount or r.credit <= 0:
            return {"cashback_percent": None}
        return {"cashback_percent": (r.credit / r.tx.amount).quantize(Decimal("0.0001"))}

    def adjustment_for(self, holder: str, adjustments: list[Tx]) -> Decimal:
        """Cashback that reaches `holder` another way, to net out of what they're
        still owed (their share stays the bank's view). None by default."""
        return Decimal(0)


def _round_to_total(raw: dict[str, Decimal], total: Decimal) -> dict[str, Decimal]:
    """Round each share down to the satang, then give the leftover satang to
    the largest remainders, so the shares add up to `total` exactly."""
    floor = {k: v.quantize(SATANG, rounding=ROUND_DOWN) for k, v in raw.items()}
    leftover = int((total.quantize(SATANG) - sum(floor.values(), Decimal(0))) / SATANG)
    for k in sorted(raw, key=lambda k: raw[k] - floor[k], reverse=True)[:max(leftover, 0)]:
        floor[k] += SATANG
    return floor
