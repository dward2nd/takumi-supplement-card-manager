"""Bank statements: parse the issuer's PDF, attribute each line to a holder,
and record the result.

deterministic + idempotent — parsing and attribution are pure; `record`
performs the Notion writes and skips anything already done.

Modules:
  model        — the normalized Statement shape and its self-check
  parser       — StatementParser: the class every issuer's parser subclasses
  uob / kbank / aeon / krungsri / ktc — one parser class per issuer layout
  attribution  — which holder's ledger each statement line belongs in
  record       — fetch the Notion rows, then apply an attribution plan
"""

from __future__ import annotations

from pathlib import Path

from .. import pdf_text, statement_secrets
from .aeon import AEONParser
from .kbank import KBankParser
from .krungsri import KrungsriParser, LotusParser
from .ktc import KTCParser
from .model import Statement, StatementParseError
from .parser import StatementParser
from .uob import UOBParser

PARSERS: dict[str, StatementParser] = {p.key: p for p in (
    UOBParser(), KBankParser(), AEONParser(), KrungsriParser(), LotusParser(), KTCParser())}


def parser_for(key: str) -> StatementParser:
    if key not in PARSERS:
        raise StatementParseError(
            f"no parser for issuer {key!r} (have {sorted(PARSERS)}); transcribe the "
            f"statement into the Statement JSON shape instead")
    return PARSERS[key]


def separate_card_statements(issuer: str) -> bool:
    """Does this card-repository issuer print one statement per card number?"""
    return any(p.separate_card_statements for p in PARSERS.values() if p.issuer == issuer)


def parse_text(issuer: str, text: str) -> Statement:
    return parser_for(issuer).parse(text)


def load_pdf(path: str | Path, issuer: str) -> Statement:
    """Extract (decrypting with the issuer's registered password) and parse."""
    parser = parser_for(issuer)
    password = statement_secrets.password_for_issuer(parser.issuer)
    return parser.parse(pdf_text.extract(path, password).text)
