"""StatementParser — one class per issuer's statement layout.

deterministic + idempotent — pure function of the extracted text.

Replaces the parallel lookup tables (parser, card issuer, signature, and
attribution's "separate statement per card" set) with one class per issuer,
next to that issuer's parse function (uob.py, kbank.py, …).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import ClassVar

from .model import Statement, StatementParseError


class StatementParser(ABC):
    key: ClassVar[str]           # the name a caller asks for ("UOB", "Lotus")
    issuer: ClassVar[str]        # the card repository's issuer: card numbers and the PDF password go by it
    signature: ClassVar[str]     # text the issuer's statements always carry, to catch a PDF handed to the wrong parser
    # One PDF per card number, principal and each supplement billed separately
    # (user, 2026-09-27): a friend with no section on it has only their
    # [บัตรหลัก] rows to find there.
    separate_card_statements: ClassVar[bool] = False

    @abstractmethod
    def parse_text(self, text: str) -> Statement:
        """The issuer's layout → Statement."""

    def parse(self, text: str) -> Statement:
        if self.signature not in text.upper():
            raise StatementParseError(f"this doesn't look like a {self.key} statement")
        statement = replace(self.parse_text(text), issuer=self.issuer)
        statement.check()
        return statement
