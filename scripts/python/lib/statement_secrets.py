"""Statement-PDF decryption passwords — gitignored, keyed by issuer.

deterministic + idempotent — pure function of the on-disk YAML.

Several Thai banks ship their statement PDFs AES-encrypted. The Krungsri
family bundles the primary cardholder plus every supplement holder into a
single PDF, locked with the *primary* holder's date of birth — so one
password covers First Choice / Krungsri NOW / Krungsri JCB / Krungsri Visa.

The real passwords live in `scripts/repositories/statement-passwords.yaml`,
which is gitignored (see `statement-passwords.example.yaml` for the committed
template, and the repositories README for the schema). Resolution is
`card name -> card_repo issuer -> password`.

File shape:

    issuers:
      Krungsri: "<password>"      # default for every card from this issuer
      # optional per-holder overrides, when an issuer locks each supplement's
      # PDF with that holder's own DOB instead of the primary's:
      # CardX:
      #   default: "<primary DOB>"
      #   holders:
      #     nuta: "<nuta DOB>"
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import yaml

from . import card_repo, paths


@lru_cache(maxsize=1)
def _load() -> dict[str, Any]:
    path = paths.STATEMENT_PASSWORDS_FILE
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def password_for_issuer(issuer: str, *, holder: str | None = None) -> str | None:
    """Return the statement password for an issuer, or None if unregistered.

    A scalar value is the issuer-wide password. A mapping may carry a
    `default` plus a `holders` override map (keyed by lowercase holder slug)
    for issuers that lock each supplement's PDF with that holder's own DOB.
    """
    entry = (_load().get("issuers") or {}).get(issuer)
    if entry is None:
        return None
    if isinstance(entry, dict):
        if holder:
            override = (entry.get("holders") or {}).get(holder.strip().lower())
            if override is not None:
                return str(override)
        default = entry.get("default")
        return str(default) if default is not None else None
    return str(entry)


def password_for_card(card_name: str, *, holder: str | None = None) -> str | None:
    """Resolve a card title to its statement password via its issuer."""
    card = card_repo.get(card_name)
    if card is None:
        return None
    return password_for_issuer(card.issuer, holder=holder)
