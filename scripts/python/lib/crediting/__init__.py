"""Crediting: the ledger rows that pay a card's cashback back to a holder.

deterministic + idempotent — see base.py.

Modules:
  base     Crediting (plan + post), CreditRow, CreditPlan
  uob_one  UOB One: 1% per statement cycle, 10%/5% per calendar month,
           amounts from the Promotion Bureau's pooled caps

To credit another card: subclass Crediting in a new module and register it
below. /prepare-bill refuses to draft a registered card's cycle until its
credit rows exist.
"""

from __future__ import annotations

from .base import CreditPlan, CreditRow, Crediting
from .uob_one import CreditingError, UOBOneCrediting

CREDITINGS: dict[str, type[Crediting]] = {c.card: c for c in (UOBOneCrediting,)}


def for_card(card: str) -> Crediting:
    if card not in CREDITINGS:
        raise CreditingError(f"no crediting for {card!r}; cards with one: {sorted(CREDITINGS)}")
    return CREDITINGS[card]()


__all__ = ["CREDITINGS", "CreditPlan", "CreditRow", "Crediting", "CreditingError", "UOBOneCrediting",
           "for_card"]
