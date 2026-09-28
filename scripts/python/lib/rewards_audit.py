"""Audit reward points: each statement's printed points summary vs the ledger's rows.

deterministic + idempotent — reads only.

For every points summary a statement prints (`Statement.rewards`, read by each
issuer's parser), total what the ledgers say for the same card and period:

  - which rows: every holder's rows on the card when the bank pools points on
    the account (UOB, KBank, Krungsri, Lotus's); on a one-PDF-per-card issuer
    (KTC) only that card's own rows — plus friends' `[บัตรหลัก]` shares when
    it's the principal's card;
  - which period (`StatementParser.points_timing`): "posting" — the rows posted
    from the previous statement date to the day before this one, `Process Date`
    or inferred (UOB credits points as each charge posts) — or "cycle" — the
    rows billed on the statement's cycle (KBank, AEON; the default);
  - how many points: the `คะแนนที่ได้จริง` formula per row (`lib.points`) — and,
    for a bank that rounds once per cycle (`points_rounding` "cycle": KBank, KTC,
    Krungsri), what that gives on the same rows: floor(Σ / baht per point) per
    multiplier. The difference is `rounding`, what per-row flooring loses;
    `[ปรับคะแนน]` rows are the household's split-line adjustments and count
    toward earned; other `ใช้คะแนน` rows are redemptions (or, named
    `ปรับคะแนน…`, the household's hand adjustments); `Reset …` rows are ledger
    bookkeeping and are left out.

A gap comes with the rows to look at: each row whose multiplier differs from
what the card's classifier gives (`lib.promotions.classify`).
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from . import promotions
from .bill_cycle import posting_date, pattern_for_card
from .cards import CardNotFoundError, find_card
from .holders import HOLDERS, primary
from .ledger import PRIMARY_PREFIX, cycle_rows
from .points import row_points
from .statements.model import RewardSummary, Statement
from .statements.parser import StatementParser

SPLIT_ADJUSTMENT = "[ปรับคะแนน]"
HAND_ADJUSTMENT = "ปรับคะแนน"
RESET = "Reset "


@dataclass
class Tally:
    earned: int = 0
    split_adjustments: int = 0
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


def _in_period(r: dict, card: str, timing: str, previous_bc: dt.date, bc: dt.date) -> bool:
    # Only charges post: redemption and adjustment rows (฿0 or less) belong to the cycle they're billed on.
    if timing == "posting" and (r["amount"] or 0) > 0:
        if not r["transaction_date"]:
            return False
        posted = posting_date(card, dt.date.fromisoformat(r["transaction_date"][:10]), r["name"], r["process_date"])
        return previous_bc <= posted < bc
    return (r["bill_cycle_date"] or "")[:10] == bc.isoformat()


def tally(summary: RewardSummary, card: str, holder: str, parser: StatementParser, bc: dt.date) -> Tally:
    principal = primary().key
    if parser.separate_card_statements:
        holders = {principal: None, **{h: "shares" for h in HOLDERS if h != principal}} if holder == principal \
            else {holder: "own"}
    else:
        holders = {h: None for h in HOLDERS}
    previous_bc = pattern_for_card(card).closed(bc)[0]
    cycles = [bc.isoformat()] + ([previous_bc.isoformat()] if parser.points_timing == "posting" else [])
    t = Tally()
    for h, only in holders.items():
        rows, bpp = _rows_for(h, card, cycles)
        t.bpp = t.bpp or bpp
        for r in rows:
            name = r["name"] or ""
            if only == "shares" and not name.startswith(PRIMARY_PREFIX):
                continue
            if only == "own" and name.startswith(PRIMARY_PREFIX):
                continue
            if not _in_period(r, card, parser.points_timing, previous_bc, bc):
                continue
            if name.startswith(RESET):
                t.left_out.append(f"{h} {r['transaction_date'][:10]} {name}")
                continue
            used = int(r["points_redeemed"] or 0)
            pts = row_points(r["amount"], bpp, r["multiplier"])
            t.earned += pts
            if name.startswith(SPLIT_ADJUSTMENT):
                t.split_adjustments -= used
            elif name.startswith(HAND_ADJUSTMENT):
                t.adjustments -= used
            else:
                t.redeemed += used
            t.holders[h] = t.holders.get(h, 0) + 1
            t.rows.append({**r, "holder": h, "points": pts})
            if (r["amount"] or 0) > 0:
                t.spend[r["multiplier"]] = t.spend.get(r["multiplier"], 0) + r["amount"]
    return t


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
        t = tally(s, card, holder, parser, bc)
        earned = t.earned + t.split_adjustments
        rounding = (_cycle_rounded(t) - t.earned) if parser.points_rounding == "cycle" else 0
        entry |= {"card": card, "holder": holder, "timing": parser.points_timing, "rounding_rule": parser.points_rounding,
                  "ledger": {"earned": t.earned, "split_adjustments": t.split_adjustments,
                             "adjustments": t.adjustments, "redeemed": t.redeemed, "rows_by_holder": t.holders},
                  "rounding": rounding,
                  "delta_earned": earned - (s.earned + s.bonus),
                  "delta_after_rounding": earned + rounding - (s.earned + s.bonus),
                  "delta_redeemed": t.redeemed - s.redeemed}
        entry["status"] = ("ok" if entry["delta_earned"] == 0 and entry["delta_redeemed"] == 0 else
                           "rounding" if entry["delta_after_rounding"] == 0 and entry["delta_redeemed"] == 0 else "gap")
        if t.left_out:
            entry["left_out"] = t.left_out
        if entry["status"] == "gap":
            entry["suspects"] = _suspects(t.rows, card)
        out.append(entry)
    return out
