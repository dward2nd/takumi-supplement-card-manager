#!/usr/bin/env python3
"""sync-points-balance — set each card's running points to its statement's printed outstanding points.

deterministic + idempotent — one `[ปรับคะแนน] ยอดคะแนนคงเหลือตามใบแจ้งยอด <BC>`
row per (card, statement); a re-run finds it and updates it in place, or
writes nothing when it already matches.

Reads a JSON spec from stdin (or --input <file>):

  {
    "pdf":       "/abs/path/statement.pdf",   // one statement: the issuer's PDF
    "issuer":    "UOB" | "KBank" | "KTC" | "Krungsri" | "Lotus" | "CardX",
    "statement": { ... },                     // alternative to pdf: a Statement dict with
                                              //   "rewards" (needs `issuer` for its parser)
    "latest":    true,                        // alternative to both: every card's latest
                                              //   statement PDF on the Bills DBs
    "dry_run":   false                        // or --dry-run: plan, write nothing
  }

Statement total = the principal's points + the friends' points (user,
2026-09-29). For every points summary the statement prints, lib.points_balance
sums the ledgers' `คะแนนที่ได้จริง` over the rows the summary covers as of the
statement, and writes the difference from the printed outstanding points on the
account holder's ledger (Takumi's for a pooled account, the card's holder on a
one-PDF-per-card issuer). Output:

  { "dry_run", "statements": [{issuer, statement_date, printed?, source?}], "warnings": [...],
    "counts": {status: n}, "accounts": [ { number, program, card, holder, account_holder,
      statement_date, status: ok|create|update|superseded|unmapped|no-outstanding,
      printed, ledger, by_holder, since, adjust, balance_now, row_id?, was?, reason? } ] }
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import points_balance  # noqa: E402
from lib.statements import load_pdf, parser_for  # noqa: E402
from lib.statements.model import Statement  # noqa: E402
from lib.statements.record import ledger_cycle, number_lookup  # noqa: E402
from latest import latest_statements  # noqa: E402


def _statements(spec: dict) -> tuple[list[tuple[Statement, object, str | None]], list[str]]:
    if spec.get("latest"):
        with tempfile.TemporaryDirectory(prefix="sync-points-balance-") as tmp:
            return latest_statements(Path(tmp))
    if not spec.get("issuer"):
        raise ValueError("spec needs `issuer` with `pdf` or `statement`, or `latest: true`")
    parser = parser_for(spec["issuer"])
    if spec.get("statement"):
        return [(Statement.from_dict(spec["statement"]), parser, None)], []
    if spec.get("pdf"):
        return [(load_pdf(Path(spec["pdf"]).expanduser(), spec["issuer"]), parser, Path(spec["pdf"]).name)], []
    raise ValueError("spec needs `pdf` or `statement`")


def _account(head: dict, p: points_balance.BalancePlan) -> tuple[str, str]:
    """The points account a plan is for: (card, whose card number) — a reissued
    card keeps its account under a new number (UOB World …4488 → …9310)."""
    return (p.card, p.holder) if p.card else (head["issuer"], p.number)


def _keep_latest(plans: list[tuple[dict, points_balance.BalancePlan]]) -> list[tuple[dict, points_balance.BalancePlan]]:
    """Per points account, one plan: the latest statement's. The `latest` mode reads
    every holder's bills, so a statement can come twice (a friend's bill keeps a
    copy) and an older one can come from a card whose own bills stopped."""
    newest: dict[tuple[str, str], str] = {}
    for head, p in plans:
        key = _account(head, p)
        newest[key] = max(newest.get(key, ""), p.statement_date)
    kept, seen = [], set()
    for head, p in plans:
        key = _account(head, p)
        if p.statement_date == newest[key] and key not in seen:
            seen.add(key)
            kept.append((head, p))
    return kept


def run(spec: dict, *, dry_run: bool = False) -> dict:
    found, warnings = _statements(spec)
    heads, planned = [], []
    for printed, parser, source in found:
        try:
            statement, cycle_warnings = ledger_cycle(printed)
        except ValueError as e:
            warnings.append(str(e))
            continue
        warnings += cycle_warnings
        head = {"issuer": statement.issuer, "statement_date": statement.statement_date}
        if statement is not printed:
            head["printed"] = printed.statement_date
        if source:
            head["source"] = source
        if statement.rewards:
            heads.append(head)
        planned += [(head, p) for p in points_balance.plan(statement, parser, number_lookup)]
    kept = _keep_latest(planned)
    plans = [p for _, p in kept]
    if not dry_run:
        points_balance.apply(plans)
    return {"dry_run": dry_run,
            "statements": [h for h in heads if any(h is k for k, _ in kept)],
            "warnings": warnings,
            "counts": dict(Counter(p.status for p in plans)),
            "accounts": [p.report() for p in plans]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="plan every balance row, write nothing")
    args = ap.parse_args(argv)
    spec = json.loads(args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read())
    json.dump(run(spec, dry_run=args.dry_run or bool(spec.get("dry_run"))), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
