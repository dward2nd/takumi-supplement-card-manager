"""Audit reward points: each statement's printed points summary vs the ledger's rows.

deterministic + idempotent — reads only.

For every points summary a statement prints (`Statement.rewards`, read by each
issuer's parser), total what the ledgers say for the same card and period:

  - which rows: the summary's `PointsAccount` (`lib.points_account`) — every
    holder's rows on the card when the bank pools points on the account (UOB,
    KBank, Krungsri, Lotus's); on a one-PDF-per-card issuer (KTC, CardX) only
    that card's own rows — plus friends' `[บัตรหลัก]` shares when it's the
    principal's card;
  - which period: the parser's `PointsPeriod` — "posting", the rows posted
    from the previous statement date to the day before this one, `Process Date`
    or inferred (UOB credits points as each charge posts) — or "cycle", the
    rows billed on the statement's cycle (KBank, AEON; the default);
  - how many points: the `คะแนนที่ได้จริง` formula per row (`lib.points`) — and,
    for a bank that rounds once per cycle (`points_rounding` "cycle": KBank, KTC,
    Krungsri), what that gives on the same rows: floor(Σ / baht per point) per
    multiplier. The difference is `rounding`, what per-row flooring loses;
    `[ปรับคะแนน]` rows are the household's adjustments on the principal's
    ledger — split lines, and (`[ปรับคะแนน] ปัดเศษ…`) the cycle's rounding —
    and count toward earned; `[คะแนนพิเศษ]` rows are bonus points (vs the
    bank's bonus); other `ใช้คะแนน` rows are redemptions (or, named
    `ปรับคะแนน…`, the household's hand adjustments); `Reset …` rows and
    `[ปรับคะแนน] ยอดคะแนนคงเหลือ…` rows (a card's balance set to a statement's
    printed outstanding points by /sync-points-balance) are ledger bookkeeping
    and are left out. A coin programme (Lotus's) isn't compared:
    its fractional coins don't fit the ledger's whole points (user, 2026-09-28).

A gap comes with the rows to look at: each row whose multiplier differs from
what the card's classifier gives (`lib.promotions.classify`).
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from . import promotions
from .bill_cycle import pattern_for_card
from .cards import CardNotFoundError, find_card
from .holders import HOLDERS
from .ledger import cycle_rows
from .points import row_points
from .points_account import account_for, is_bookkeeping, period_for
from .statements.model import RewardSummary, Statement
from .statements.parser import StatementParser

SPLIT_ADJUSTMENT = "[ปรับคะแนน]"
ROUNDING_ADJUSTMENT = "[ปรับคะแนน] ปัดเศษ"   # the cycle's rounding, on the principal's ledger
BONUS = "[คะแนนพิเศษ]"
HAND_ADJUSTMENT = "ปรับคะแนน"


@dataclass
class Tally:
    earned: int = 0
    split_adjustments: int = 0
    rounding_adjustments: int = 0
    bonus: int = 0
    adjustments: int = 0
    redeemed: int = 0
    rows: list[dict] = field(default_factory=list)
    holders: dict[str, int] = field(default_factory=dict)   # rows counted per holder
    spend: dict = field(default_factory=dict)                # multiplier → Σ ยอดชำระ of earning rows
    bpp: float | None = None                                 # the card's baht per point
    left_out: list[str] = field(default_factory=list)


def _rows_for(holder_key: str, card: str, bill_cycles: list[str]) -> tuple[list[dict], float | None]:
    try:
        page = find_card(HOLDERS[holder_key].cards_ds, card)
    except CardNotFoundError:
        return [], None
    bpp = (page["properties"].get("บาทต่อ 1 คะแนน") or {}).get("number")
    rows = [r for bc in bill_cycles for r in cycle_rows(HOLDERS[holder_key].transactions_ds, page["id"], bc)]
    return rows, bpp


def tally(summary: RewardSummary, card: str, holder: str, parser: StatementParser, bc: dt.date) -> Tally:
    account, period = account_for(parser, card, holder), period_for(parser)
    previous_bc = pattern_for_card(card).closed(bc)[0]
    cycles = period.bill_cycles(bc, previous_bc)
    t = Tally()
    for h in account.holders():
        rows, bpp = _rows_for(h, card, cycles)
        t.bpp = t.bpp or bpp
        for r in rows:
            name = r["name"] or ""
            if not account.counts(h, name) or not period.in_statement(r, card, previous_bc, bc):
                continue
            if is_bookkeeping(name):
                t.left_out.append(f"{h} {r['transaction_date'][:10]} {name}")
                continue
            used = int(r["points_redeemed"] or 0)
            pts = row_points(r["amount"], bpp, r["multiplier"])
            t.earned += pts
            if name.startswith(ROUNDING_ADJUSTMENT):
                t.rounding_adjustments -= used
            elif name.startswith(SPLIT_ADJUSTMENT):
                t.split_adjustments -= used
            elif name.startswith(BONUS):
                t.bonus -= used
            elif name.startswith(HAND_ADJUSTMENT):
                t.adjustments -= used
            else:
                t.redeemed += used
            t.holders[h] = t.holders.get(h, 0) + 1
            t.rows.append({**r, "holder": h, "points": pts})
            if (r["amount"] or 0) > 0:
                t.spend[r["multiplier"]] = t.spend.get(r["multiplier"], 0) + r["amount"]
    return t


def rounding_lost(t: Tally) -> int:
    """Points per-row flooring loses against a bank that rounds once per cycle."""
    return _cycle_rounded(t) - t.earned


def _cycle_rounded(t: Tally) -> int:
    """Points on the cycle's spend rounded once per multiplier, as KBank/KTC/Krungsri do."""
    return sum(row_points(total, t.bpp, m) for m, total in t.spend.items()) if t.bpp else t.earned


def _suspects(rows: list[dict], card: str) -> list[dict]:
    """Rows whose multiplier differs from what the card's classifier gives."""
    out = []
    for r in rows:
        if not r["amount"] or r["amount"] <= 0 or (r["name"] or "").startswith("["):
            continue
        c = promotions.classify(card, dt.date.fromisoformat(r["transaction_date"][:10]), r["name"])
        if (c.points_override or None) != (r["multiplier"] or None):
            out.append({"row": f"{r['holder']} {r['transaction_date'][:10]} ฿{r['amount']:,.2f} {r['name']}",
                        "has": r["multiplier"] or "×1", "classifier": c.points_override or "×1", "reason": c.reason})
    return out


def audit(statement: Statement, parser: StatementParser, number_lookup) -> list[dict]:
    bc = dt.date.fromisoformat(statement.statement_date)
    out = []
    for s in statement.rewards:
        owner = number_lookup(statement.issuer, s.number)
        entry = {"number": s.number, "program": s.program,
                 "bank": {"earned": s.earned, "bonus": s.bonus, "adjusted": s.adjusted,
                          "redeemed": s.redeemed, "outstanding": s.outstanding}}
        if owner is None:
            out.append({**entry, "status": "unmapped",
                        "reason": f"card …{s.number} isn't in any {statement.issuer} card's statement_numbers"})
            continue
        card, holder = owner
        if "coins" in s.program.lower():
            out.append({**entry, "card": card, "holder": holder, "status": "not-comparable",
                        "reason": "coins accrue in fractions (Lotus's: 0.25 per ฿50, 1.5 per ฿50 at Lotus's); "
                                  "the ledger keeps whole points"})
            continue
        t = tally(s, card, holder, parser, bc)
        base = t.earned + t.split_adjustments + t.bonus
        rounding = rounding_lost(t) if parser.points_rounding == "cycle" else 0
        entry |= {"card": card, "holder": holder, "timing": parser.points_timing, "rounding_rule": parser.points_rounding,
                  "ledger": {"earned": t.earned, "split_adjustments": t.split_adjustments,
                             "rounding_adjustments": t.rounding_adjustments, "bonus": t.bonus,
                             "adjustments": t.adjustments, "redeemed": t.redeemed, "rows_by_holder": t.holders},
                  "rounding": rounding,
                  "delta_earned": base + t.rounding_adjustments - (s.earned + s.bonus),
                  "delta_after_rounding": base + rounding - (s.earned + s.bonus),
                  "delta_redeemed": t.redeemed - s.redeemed}
        entry["status"] = ("ok" if entry["delta_earned"] == 0 and entry["delta_redeemed"] == 0 else
                           "rounding" if entry["delta_after_rounding"] == 0 and entry["delta_redeemed"] == 0 else "gap")
        if t.left_out:
            entry["left_out"] = t.left_out
        if entry["status"] == "gap":
            entry["suspects"] = _suspects(t.rows, card)
        out.append(entry)
    return out
