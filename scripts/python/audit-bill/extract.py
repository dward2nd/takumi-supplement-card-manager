#!/usr/bin/env python3
"""extract — dump text from a (possibly encrypted) statement PDF.

deterministic + idempotent — read-only, no network.

Helper for /audit-bill. The diff CLI expects pre-parsed
`statement_transactions`; this tool turns a PDF into plain text so the
agent can read it and construct that list without burning tokens on
multi-page screenshots. Layouts vary too much per issuer to bake table
extraction in — text is the lowest-common-denominator surface.

Reads either CLI flags or a JSON spec on stdin:

  $ uv run scripts/python/audit-bill/extract.py --pdf /abs/path.pdf [--password 1234]

  # Auto-resolve the password from the repository by card (or issuer):
  $ uv run scripts/python/audit-bill/extract.py --pdf /abs/path.pdf --card "First Choice"

  $ echo '{"pdf": "/abs/path.pdf", "password": "1234", "pages": "5-7"}' \\
      | uv run scripts/python/audit-bill/extract.py

Writes the joined per-page text to stdout, each page prefixed with
`===== Page N =====`. Encrypted PDFs are decrypted with --password
(or "password" in the JSON spec). When no explicit password is given but
`--card`/`--issuer` is, the password is looked up in
`scripts/repositories/statement-passwords.yaml` (gitignored) via
`lib.statement_secrets` — so the agent never needs to re-type a known
issuer's password.

Why a separate CLI: PDF text extraction is reusable beyond audit-bill
(e.g. parsing slip files for /update-bill). The implementation lives in
`lib/pdf_text.py`; this file is a thin entry point so the audit-bill
skill folder is the obvious place to look first.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import pdf_text, statement_secrets


def _parse_pages(spec: str | None, total: int) -> list[int]:
    """Parse a 1-indexed page selector like "1,3-5" against `total` pages."""
    if not spec:
        return list(range(1, total + 1))
    out: set[int] = set()
    for chunk in str(spec).split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            for i in range(int(a), int(b) + 1):
                out.add(i)
        else:
            out.add(int(chunk))
    return sorted(p for p in out if 1 <= p <= total)


def _resolve_spec(args: argparse.Namespace) -> dict:
    if args.pdf:
        return {
            "pdf": args.pdf,
            "password": args.password,
            "pages": args.pages,
            "card": args.card,
            "issuer": args.issuer,
            "holder": args.holder,
        }
    raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit("no spec on stdin and no --pdf flag")
    return json.loads(raw)


def _resolve_password(spec: dict) -> str | None:
    """Explicit `password` wins; otherwise look it up by card/issuer."""
    password = spec.get("password")
    if password:
        return password
    holder = spec.get("holder")
    card = spec.get("card")
    if card:
        return statement_secrets.password_for_card(card, holder=holder)
    issuer = spec.get("issuer")
    if issuer:
        return statement_secrets.password_for_issuer(issuer, holder=holder)
    return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pdf", help="Path to the PDF (absolute or relative).")
    ap.add_argument("--password", help="Decryption password, if the PDF is encrypted.")
    ap.add_argument("--pages", help='Page selector, e.g. "1,3-5". Default: every page.')
    ap.add_argument(
        "--card",
        help="Card title; auto-resolves the password from the repository when --password is omitted.",
    )
    ap.add_argument(
        "--issuer",
        help="Issuer name; alternative to --card for password auto-resolution.",
    )
    ap.add_argument(
        "--holder",
        help="Holder slug (baiboon|nuta|takumi); used only for issuers with per-holder password overrides.",
    )
    args = ap.parse_args(argv)

    spec = _resolve_spec(args)
    pdf_path = spec.get("pdf")
    if not pdf_path:
        raise SystemExit("missing `pdf` in spec")
    if not Path(pdf_path).is_file():
        raise SystemExit(f"PDF not found: {pdf_path}")

    extracted = pdf_text.extract(pdf_path, password=_resolve_password(spec))
    page_nums = _parse_pages(spec.get("pages"), len(extracted.pages))

    chunks: list[str] = []
    for n in page_nums:
        chunks.append(f"===== Page {n} =====")
        chunks.append(extracted.pages[n - 1].rstrip())
    sys.stdout.write("\n".join(chunks) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
