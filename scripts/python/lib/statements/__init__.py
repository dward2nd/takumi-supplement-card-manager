"""Bank statements: parse the issuer's PDF, attribute each line to a holder,
and record the result.

deterministic + idempotent — parsing and attribution are pure; `record`
performs the Notion writes and skips anything already done.

Modules:
  model        — the normalized Statement shape and its self-check
  parser       — StatementParser: the class every issuer's parser subclasses
  uob / kbank / aeon / krungsri / ktc / cardx — one parser class per issuer layout
  attribution  — which holder's ledger each statement line belongs in
  record       — fetch the Notion rows, then apply an attribution plan
"""

from __future__ import annotations

from pathlib import Path

from .. import pdf_text, statement_secrets
from .aeon import AEONParser
from .cardx import CardXParser
from .kbank import KBankParser
from .krungsri import KrungsriParser, LotusParser
from .ktc import KTCParser
from .model import Statement, StatementParseError
from .parser import StatementParser
from .uob import UOBParser

PARSERS: dict[str, StatementParser] = {p.key: p for p in (
    UOBParser(), KBankParser(), AEONParser(), KrungsriParser(), LotusParser(), KTCParser(), CardXParser())}


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


def read_pdf(path: str | Path, issuer: str) -> str:
    """A statement PDF's text, decrypted with the card issuer's registered
    password — each one in turn, for an issuer that locks a supplement's PDF
    with its holder's DOB (CardX)."""
    candidates = statement_secrets.passwords_for_issuer(issuer)
    for i, password in enumerate(candidates, 1):
        try:
            return pdf_text.extract(path, password).text
        except Exception as e:
            if pdf_text.is_wrong_password(e) and i < len(candidates):
                continue
            raise
    raise AssertionError("unreachable")


def load_pdf(path: str | Path, issuer: str) -> Statement:
    """Extract (decrypting with the issuer's registered password) and parse."""
    parser = parser_for(issuer)
    return parser.parse(read_pdf(path, parser.issuer))


def load_card_pdf(path: str | Path, card_issuer: str) -> tuple[Statement, StatementParser]:
    """Parse a PDF knowing only the card repository's issuer: the parser whose
    signature the text carries — the most specific class when several do
    (LotusParser subclasses KrungsriParser, and a Lotus's statement carries both)."""
    parsers = [p for p in PARSERS.values() if p.issuer == card_issuer]
    if not parsers:
        raise StatementParseError(f"no parser for card issuer {card_issuer!r}")
    text = read_pdf(path, card_issuer)
    matching = [p for p in parsers if p.signature in text.upper()]
    if not matching:
        raise StatementParseError(f"no {card_issuer} parser recognises {Path(path).name}")
    parser = max(matching, key=lambda p: len(type(p).__mro__))
    return parser.parse(text), parser
