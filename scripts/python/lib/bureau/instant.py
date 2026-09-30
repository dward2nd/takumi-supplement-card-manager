"""InstantDiscountPromotion — the reward comes off the charge itself (UnionPay QR 6%).

deterministic + idempotent — pure functions of the transactions handed in.

Most campaigns pay a credit later: a row's `ยอดชำระ` is the full price, and the
reward is money still to come. Here the network takes the discount off at the
till and the bank charges the rest, so the ledger row already holds the net
amount (user, 2026-09-30: "the cashback is combined to the transaction
charges, not separated"). Nothing is credited later: no tracker rows, no
`% cb` (it would promise a credit), no credit rows.

So the discount is read back from the net amount. A slip priced G earns
min(rate × G, `per_slip`, what's left of the period's `cap`); with N = G − D,
an uncapped slip's discount is N × rate / (1 − rate).

The net amount is also the evidence of whether the discount was taken. Prices
at the household's QR merchants are whole baht, so a discounted slip's net is
94% of a whole number (฿67.68 = 72 × 0.94) and an undiscounted one is whole
(฿50). A slip whose net can't say — one past the per-slip cap (any price fits
a ฿60 discount) or a satang price — follows the terms. Evidence only ever
takes a discount away: a slip that shows none doesn't use the day's discount.

The walk, first come first served by `Transaction Datetime`, per day:
  - at most `per_day` discounted slips; within a day whose order the ledger
    doesn't know, the slips whose amount shows the discount go first;
  - nothing once the period's `cap` is used;
  - nothing from `quota_gone`, the day the bank's pool for the period ran out,
    except, on that day itself, a slip whose amount shows it was discounted.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import ROUND_HALF_UP, Decimal
from itertools import groupby
from typing import ClassVar

from ..ledger import PRIMARY_PREFIX
from .base import SATANG, Allocation, CashbackPromotion, Tx, TxCredit
from .sync import line

_ZERO = Decimal(0)
_COUNTRY = re.compile(r"\s+THA?$")


def _merchant(tx: Tx) -> str:
    """The merchant string without its country suffix: the holders' ledgers spell
    one charge `… CHIANGMAI THA` (Takumi's, from the statement) and `… CHIANGMAI TH`."""
    return " ".join(_COUNTRY.sub("", tx.merchant).split())


def slips(txs: list[Tx]) -> list[list[Tx]]:
    """One sales slip per charge. A friend's `[บัตรหลัก]` share and another holder's
    part of the same charge (same day, same merchant) are one slip;
    two rows of one holder stay two slips."""
    out: list[list[Tx]] = []
    for t in sorted(txs, key=lambda t: t.when):
        for s in out:
            shared = t.name.startswith(PRIMARY_PREFIX) or any(x.name.startswith(PRIMARY_PREFIX) for x in s)
            if shared and s[0].day == t.day and _merchant(s[0]) == _merchant(t) \
                    and t.holder not in {x.holder for x in s}:
                s.append(t)
                break
        else:
            out.append([t])
    return out


def _label(slip: list[Tx]) -> str:
    return " + ".join(line(t) for t in slip)


class InstantDiscountPromotion(CashbackPromotion):
    rate: ClassVar[Decimal]       # the discount, e.g. 0.06
    per_slip: ClassVar[Decimal]   # most baht off one slip
    per_day: ClassVar[int]        # discounted slips per card a day
    cap: ClassVar[Decimal]        # baht per period, per card

    marks_rows = False   # the discount is inside ยอดชำระ already
    tracked = False      # and nothing is credited later: no tracker rows

    # The first day of the period with no discount left in the bank's pool: the
    # Bureau row's `Quotas Exceeded Date`, set by `lib.bureau.quota.observe` before `allocate`.
    quota_gone: dt.date | None = None

    def full_discount(self, net: Decimal) -> Decimal:
        """The discount behind a net amount when no cap clipped it."""
        return net * self.rate / (1 - self.rate)

    def discount(self, net: Decimal, left: Decimal) -> Decimal:
        return min(self.full_discount(net), self.per_slip, left).quantize(SATANG, rounding=ROUND_HALF_UP)

    def shows_discount(self, net: Decimal, left: Decimal) -> bool | None:
        """True / False when the net amount shows whether the discount was taken;
        None when it can't (a capped slip, a satang price)."""
        full = self.full_discount(net)
        if full > self.per_slip:
            return None
        if full > left:                       # the period's cap clipped it
            return True if (net + left) % 1 == 0 else None
        if (net / (1 - self.rate)) % 1 == 0:
            return True
        return False if net % 1 == 0 else None

    def allocate(self, txs: list[Tx]) -> Allocation:
        rows: list[TxCredit] = []
        boundary: list[TxCredit] = []
        warnings: list[str] = []
        left, gone = self.cap, self.quota_gone
        spend = [t for t in txs if t.amount > 0 and self.qualifies(t)]
        by_day = groupby(sorted(slips(spend), key=lambda s: s[0].when), key=lambda s: s[0].day)
        for day, group in by_day:
            group = list(group)
            net = {id(s): sum((t.amount for t in s), _ZERO) for s in group}
            shown = {id(s): self.shows_discount(net[id(s)], left) for s in group}
            # Timed slips keep their order. On a day the ledger can't order, the slips
            # whose amount shows the discount go first.
            timed = all(s[0].when[1] for s in group)
            group.sort(key=lambda s: (not timed and shown[id(s)] is not True, s[0].when))
            taken: list[list[Tx]] = []
            passed: list[list[Tx]] = []   # slips the terms would discount but whose amount shows none
            for s in group:
                n = net[id(s)]
                evidence = self.shows_discount(n, left)
                why = None
                if gone and (day > gone or (day == gone and evidence is not True)):
                    why = f"UnionPay's pool ran out on {gone}"
                elif len(taken) >= self.per_day:
                    why = f"the day's discount went to {_label(taken[0])}"
                elif left <= 0:
                    why = f"the card's ฿{self.cap:,.0f} for the month is used"
                if why or evidence is False:
                    if why and evidence is True:
                        warnings.append(f"{_label(s)}: the amount looks discounted (94% of a whole price), "
                                        f"but {why} — a coincidence, or a wrong Quotas Exceeded Date / order?")
                    if not why:
                        passed.append(s)
                    rows += [TxCredit(t, _ZERO, _ZERO) for t in s]
                    continue
                d = self.discount(n, left)
                credited = [TxCredit(t, t.amount, d * t.amount / n) for t in s]
                if d < min(self.full_discount(n), self.per_slip):
                    boundary = credited
                left -= d
                taken.append(s)
                rows += credited
                rivals = [r for r in group if r is not s and shown[id(r)] is not False]
                if evidence is None and rivals and len(taken) == 1 and not timed:
                    warnings.append(f"{day}: which slip took the day's discount is a guess (no times): "
                                    f"{_label(s)} over {'; '.join(_label(r) for r in rivals)}")
            if passed and not taken:
                warnings.append(f"{_label(passed[0])}: the amount shows no discount although the terms "
                                f"give one — card not registered for the month yet, not paid by QR, the "
                                f"merchant not taking part, or the pool gone before Quotas Exceeded Date says")
        credit = sum((r.credit for r in rows), _ZERO).quantize(SATANG, rounding=ROUND_HALF_UP)
        return self._allocation(rows, boundary, warnings, credit=credit)
