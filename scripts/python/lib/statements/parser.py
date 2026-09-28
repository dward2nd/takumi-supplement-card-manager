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

from .model import RewardSummary, Statement, StatementParseError


class StatementParser(ABC):
    key: ClassVar[str]           # the name a caller asks for ("UOB", "Lotus")
    issuer: ClassVar[str]        # the card repository's issuer: card numbers and the PDF password go by it
    signature: ClassVar[str]     # text the issuer's statements always carry, to catch a PDF handed to the wrong parser
    # One PDF per card number, principal and each supplement billed separately
    # (user, 2026-09-27): a friend with no section on it has only their
    # [บัตรหลัก] rows to find there.
    separate_card_statements: ClassVar[bool] = False
    # When the bank credits reward points (user, 2026-09-28): "posting" — as each
    # charge posts, the statement's summary counting the lines posted in its window
    # (UOB) — or "cycle" — at the statement, for what's billed on it (KBank, AEON;
    # the default until an issuer is shown otherwise).
    points_timing: ClassVar[str] = "cycle"
    # How the bank rounds points: "cycle" — once on the cycle's spend per rate,
    # floor(Σ ยอดชำระ / baht per point) × multiplier (KBank, KTC, Krungsri: matched
    # Aug/Sep 2026) — or "line" — per statement line, like the ledger formula (UOB).
    points_rounding: ClassVar[str] = "cycle"

    def rewards(self, text: str, statement: Statement) -> tuple[RewardSummary, ...]:
        """The points summaries the statement prints (none by default)."""
        return ()

    @abstractmethod
    def parse_text(self, text: str) -> Statement:
        """The issuer's layout → Statement."""

    def parse(self, text: str) -> Statement:
        if self.signature not in text.upper():
            raise StatementParseError(f"this doesn't look like a {self.key} statement")
        statement = replace(self.parse_text(text), issuer=self.issuer)
        statement = replace(statement, rewards=self.rewards(text, statement))
        statement.check()
        return statement
