"""Earning: how each card turns a transaction into cashback and points.

deterministic + idempotent — the registry is static.

  base      Card: the promotion step (YAML tiers) + hooks a family overrides
  families  UOBCard, TTBCard (fuel withheld), KrungsriFamilyCard, FirstChoice,
            AEONCard (MCC points exclusions), KTCCard / KTCUnionPay (KTC FOREVER)

`card_for(name)` picks the class: an explicit entry for a card that differs
from its issuer's family, else its issuer's family, else plain `Card`.
`lib.promotions.classify` is the public entry point and delegates here.
"""

from __future__ import annotations

from .. import card_repo
from .base import Card
from .families import (AEONCard, FirstChoice, KrungsriFamilyCard, KrungsriJCB, KrungsriPetrolCampaign, KTCCard,
                       KTCUnionPay, TTBCard, UOBCard)

# Cards whose rules differ from their issuer's family.
BY_NAME: dict[str, type[Card]] = {
    "First Choice": FirstChoice,
    "Krungsri JCB": KrungsriPetrolCampaign,     # points-only petrol campaign
    "Krungsri Lady": KrungsriPetrolCampaign,    # same campaign (Sep 2026 statement)
    "KTC UnionPay": KTCUnionPay,                # its own exclusion list (supermarkets …)
    "Lotus's Beyond": Card,        # Krungsri-issued partner card; CP ALL merchants keep earning
}
BY_ISSUER: dict[str, type[Card]] = {
    "UOB": UOBCard,
    "ttb": TTBCard,
    "Krungsri": KrungsriFamilyCard,
    "AEON": AEONCard,
    "KTC": KTCCard,
}


def card_for(name: str) -> Card:
    """The card's class, holding the caller's spelling of its name: promotions
    match on it exactly, and notes quote it (card_repo.get is forgiving on case)."""
    repo = card_repo.get(name)
    cls = (BY_NAME.get(repo.name) or BY_ISSUER.get(repo.issuer) if repo else None) or Card
    return cls(name, repo)


__all__ = ["AEONCard", "BY_ISSUER", "BY_NAME", "Card", "FirstChoice", "KrungsriFamilyCard", "KrungsriJCB",
           "KrungsriPetrolCampaign", "KTCCard", "KTCUnionPay",
           "TTBCard", "UOBCard", "card_for"]
