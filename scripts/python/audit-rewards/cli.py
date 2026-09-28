#!/usr/bin/env python3
"""audit-rewards — reconcile a statement's printed points summary against every holder's ledger.

deterministic + idempotent — read-only; writes nothing to Notion.

Reads a JSON spec from stdin (or --input <file>):

  {
    "pdf":       "/abs/path/statement.pdf",   // the issuer's PDF
    "issuer":    "UOB" | "KBank" | "KTC" | "Krungsri" | "Lotus",
    "statement": { ... }                      // alternative to pdf: a Statement dict
                                              //   (with "rewards") for an issuer with no parser
  }

For each points summary the statement prints (lib.statements.*Parser.rewards),
lib.rewards_audit totals the ledger's points for the same card and period
(posting window for UOB, bill cycle otherwise) and reports:

  { "statement": {issuer, statement_date, printed?}, "warnings": [...],
    "accounts": [ { number, program, card, holder, timing, status: ok|gap|unmapped,
                    bank: {earned, bonus, adjusted, redeemed, outstanding},
                    ledger: {earned, split_adjustments, adjustments, redeemed, rows_by_holder},
                    delta_earned, delta_redeemed, left_out?, suspects? } ] }

`delta_*` is ledger minus bank. A statement that prints no points (First Choice,
Central The 1, AEON) returns no accounts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.rewards_audit import audit  # noqa: E402
from lib.statements import load_pdf, parser_for  # noqa: E402
from lib.statements.model import Statement  # noqa: E402
from lib.statements.record import ledger_cycle, number_lookup  # noqa: E402


def run(spec: dict) -> dict:
    if not spec.get("issuer"):
        raise ValueError("spec needs `issuer` (UOB, KBank, KTC, Krungsri, Lotus)")
    parser = parser_for(spec["issuer"])
    if spec.get("statement"):
        printed = Statement.from_dict(spec["statement"])
    elif spec.get("pdf"):
        printed = load_pdf(Path(spec["pdf"]).expanduser(), spec["issuer"])
    else:
        raise ValueError("spec needs `pdf` or `statement`")
    statement, warnings = ledger_cycle(printed)
    head = {"issuer": statement.issuer, "statement_date": statement.statement_date}
    if statement is not printed:
        head["printed"] = printed.statement_date
    return {"statement": head, "warnings": warnings, "accounts": audit(statement, parser, number_lookup)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    args = ap.parse_args(argv)
    spec = json.loads(args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read())
    json.dump(run(spec), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
