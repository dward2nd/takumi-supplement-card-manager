"""The normalized shape every issuer's statement parser produces.

deterministic + idempotent — plain data plus a self-check.

A statement is a set of **accounts** (one per billable card product, each with
a printed total balance), and each account holds one or more **sections** (one
per physical card number: the primary, and any supplements). UOB prints
several sections under one product total; KBank and AEON print one section per
product.

Amounts are signed baht as they affect the balance: charges and fees are
positive, credits and payments negative. `check()` proves the parse is
complete — previous balance plus every line must land on the printed total —
and a statement that fails it must not be written anywhere.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

LINE_KINDS = frozenset({"charge", "fee", "credit", "payment"})
_TOLERANCE = 0.005


class StatementParseError(ValueError):
    pass


@dataclass(frozen=True)
class StatementLine:
    date: str  # transaction date, ISO
    name: str  # description exactly as printed
    amount: float  # signed THB
    kind: str  # charge | fee | credit | payment
    note: str | None = None  # e.g. the original foreign amount, or why a line is undated
    posted: str | None = None  # posting date, ISO, when the issuer prints one (UOB's POST column)

    def __post_init__(self) -> None:
        if self.kind not in LINE_KINDS:
            raise StatementParseError(f"unknown line kind {self.kind!r}")


@dataclass(frozen=True)
class CardSection:
    number: str  # last four digits of the card number
    previous_balance: float = 0.0
    lines: tuple[StatementLine, ...] = ()


@dataclass(frozen=True)
class CardAccount:
    product: str  # the issuer's product heading, verbatim
    total: float  # printed total balance — what the bank bills for this product
    sections: tuple[CardSection, ...] = ()

    def computed_total(self) -> float:
        return round(
            sum(s.previous_balance + sum(l.amount for l in s.lines) for s in self.sections), 2
        )

    def has_activity(self) -> bool:
        """Anything besides a payment settling the previous bill."""
        return any(l.kind != "payment" for s in self.sections for l in s.lines) or abs(self.total) > _TOLERANCE


@dataclass(frozen=True)
class Statement:
    issuer: str
    statement_date: str  # ISO — the bill cycle date
    due_date: str  # ISO — as printed
    accounts: tuple[CardAccount, ...] = field(default_factory=tuple)

    def check(self) -> None:
        """Raise unless every account's lines reproduce its printed total."""
        if not self.accounts:
            raise StatementParseError("no card accounts found — wrong issuer, or the layout changed")
        for a in self.accounts:
            got = a.computed_total()
            if abs(got - a.total) > _TOLERANCE:
                raise StatementParseError(
                    f"{a.product}: previous balance + lines = {got:,.2f} but the statement "
                    f"prints {a.total:,.2f} — a line was missed or misread"
                )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Statement":
        """Rebuild from `to_dict()` output — or from a hand transcription for an
        issuer that has no parser yet."""
        return cls(
            issuer=d["issuer"],
            statement_date=d["statement_date"],
            due_date=d["due_date"],
            accounts=tuple(
                CardAccount(
                    product=a["product"],
                    total=float(a["total"]),
                    sections=tuple(
                        CardSection(
                            number=str(s["number"]),
                            previous_balance=float(s.get("previous_balance", 0.0)),
                            lines=tuple(StatementLine(**l) for l in s.get("lines", [])),
                        )
                        for s in a["sections"]
                    ),
                )
                for a in d["accounts"]
            ),
        )


def parse_amount(text: str) -> float:
    return float(text.replace(",", ""))
