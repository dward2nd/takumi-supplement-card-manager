#!/usr/bin/env python3
"""record-statement — record one bank statement across all three ledgers and file Takumi's bill.

deterministic + idempotent — re-running over a statement already recorded
matches every line and writes nothing new.

Reads a JSON spec from stdin (or --input <file>):

  {
    "pdf":       "/abs/path/statement.pdf",   // the issuer's PDF (decrypted with the
                                              //   issuer's registered password)
    "issuer":    "UOB" | "KBank" | "AEON",    // required with `pdf` — picks the parser
    "statement": { ... },                     // alternative to pdf+issuer: a Statement
                                              //   dict (lib.statements.model) transcribed
                                              //   by hand for an issuer with no parser
    "attach_pdf": true                        // optional, default true when `pdf` is given
  }

For every card account on the statement it:
  - checks each supplement section against that holder's rows (reports gaps),
  - renames a friend's row that sits on the primary card to `[บัตรหลัก] …`,
  - writes Takumi's own primary-card lines (charges, bank credits, fees),
  - creates Takumi's bill at the printed card total and attaches the PDF.
Payments are never recorded — they settle the previous bill.

Card numbers map to (card, holder) via `statement_numbers` in
scripts/repositories/cards/<card>.yaml; an unmapped number blocks its account.

--dry-run   plan everything, write nothing
--parse-only  print the parsed statement and stop (no Notion access)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.statements import load_pdf  # noqa: E402
from lib.statements.model import Statement  # noqa: E402
from lib.statements.record import record  # noqa: E402


def load_statement(spec: dict) -> Statement:
    if spec.get("statement"):
        st = Statement.from_dict(spec["statement"])
        st.check()
        return st
    if not (spec.get("pdf") and spec.get("issuer")):
        raise ValueError("spec needs `pdf` + `issuer`, or a `statement` object")
    return load_pdf(Path(spec["pdf"]).expanduser(), spec["issuer"])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Plan without writing")
    ap.add_argument("--parse-only", action="store_true", help="Print the parsed statement and stop")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)
    statement = load_statement(spec)

    if args.parse_only:
        out = statement.to_dict()
    else:
        pdf = Path(spec["pdf"]).expanduser() if spec.get("pdf") and spec.get("attach_pdf", True) else None
        out = record(statement, pdf=pdf, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
