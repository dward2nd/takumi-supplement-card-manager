"""Bank statements: parse the issuer's PDF, attribute each line to a holder,
and record the result.

deterministic + idempotent — parsing and attribution are pure; `record`
performs the Notion writes and skips anything already done.

Modules:
  model        — the normalized Statement shape and its self-check
  uob / kbank / aeon / krungsri / ktc — one parser per issuer layout
  attribution  — which holder's ledger each statement line belongs in
  record       — fetch the Notion rows, then apply an attribution plan
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from .. import pdf_text, statement_secrets
from . import aeon, kbank, krungsri, ktc, uob
from .model import Statement, StatementParseError

# Lotus's Money Services is a Krungsri company: same layout, same PDF password,
# and its card (Lotus's Beyond) carries `issuer: Krungsri` in the card repo. The
# `Lotus` key survives only to pick the parser + signature for a Lotus's PDF.
PARSERS = {"UOB": uob.parse, "KBank": kbank.parse, "AEON": aeon.parse, "Krungsri": krungsri.parse, "Lotus": krungsri.parse, "KTC": ktc.parse}
_CARD_ISSUER = {"Lotus": "Krungsri"}  # parser key → card_repo issuer (lookup + password)

# A word each issuer's own text carries, to catch a PDF handed to the wrong parser.
_SIGNATURES = {"UOB": "UOB", "KBank": "KBANK", "AEON": "AEON", "Krungsri": "TOTAL PAYMENT DUE FOR CREDIT CARD", "Lotus": "LOTUS", "KTC": "KRUNGTHAI CARD"}


def parse_text(issuer: str, text: str) -> Statement:
    if issuer not in PARSERS:
        raise StatementParseError(
            f"no parser for issuer {issuer!r} (have {sorted(PARSERS)}); transcribe the "
            f"statement into the Statement JSON shape instead"
        )
    if _SIGNATURES[issuer] not in text.upper():
        raise StatementParseError(f"this doesn't look like a {issuer} statement")
    # The issuer given wins over the parser's: it's what card numbers are looked up under.
    statement = replace(PARSERS[issuer](text), issuer=_CARD_ISSUER.get(issuer, issuer))
    statement.check()
    return statement


def load_pdf(path: str | Path, issuer: str) -> Statement:
    """Extract (decrypting with the issuer's registered password) and parse."""
    password = statement_secrets.password_for_issuer(_CARD_ISSUER.get(issuer, issuer))
    return parse_text(issuer, pdf_text.extract(path, password).text)
