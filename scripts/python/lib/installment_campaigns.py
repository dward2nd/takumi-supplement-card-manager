"""Installment-campaign repository — plan-level reward campaigns.

deterministic + idempotent — pure function of the on-disk YAML files.

Some issuers run campaigns that change how an installment *plan* earns
rewards, and membership is a property of the plan rather than of the card
or the merchant. CardX's **ดีจังผ่อน 0%** is the motivating case: the
cardholder asks the bank to convert an already-posted charge into 0%
installments, and those terms earn no points — while a merchant-offered
installment on the very same card earns normally. Nothing in the merchant
string separates the two.

That rules out both places a card rule would normally live:

  * `cards/<slug>.yaml` — a card-level flag would zero points on every
    installment on the card, including merchant-offered ones.
  * `promotions/<id>.yaml` + `lib.promotions.classify` — classify() only
    sees (card, date, merchant_name), which is provably insufficient here.

So campaigns are matched against the plan's **existing terms**: the note
written on term 1 is the evidence that term 2 inherits. See
`lib.installments.populate_for_cycle`.

One YAML file per campaign under `scripts/repositories/installment-campaigns/`.
See `scripts/repositories/README.md` for the schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from . import paths


@dataclass(frozen=True)
class InstallmentCampaign:
    id: str
    name: str
    issuer: str
    status: str
    points_default: str | None   # multiplier string ("×0") applied to every term
    cashback: str | None         # "unaffected" — campaigns are points-only so far
    note: str | None             # written verbatim onto each term
    note_contains: str | None    # definitive detection substring
    typical_total_terms: tuple[int, ...]  # advisory hint only — never auto-applied
    notes: str | None
    source_path: Path


class InstallmentCampaignNotFoundError(LookupError):
    pass


def _parse_campaign(data: dict[str, Any], source: Path) -> InstallmentCampaign:
    required = ("id", "name", "issuer")
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"{source}: campaign missing required field(s) {missing}")
    detect = data.get("detect") or {}
    raw_terms = detect.get("typical_total_terms") or []
    if isinstance(raw_terms, int):
        raw_terms = [raw_terms]
    return InstallmentCampaign(
        id=str(data["id"]),
        name=str(data["name"]),
        issuer=str(data["issuer"]),
        status=str(data.get("status", "active")),
        points_default=data.get("points_default"),
        cashback=data.get("cashback"),
        note=data.get("note"),
        note_contains=detect.get("note_contains"),
        typical_total_terms=tuple(int(t) for t in raw_terms),
        notes=data.get("notes"),
        source_path=source,
    )


@lru_cache(maxsize=1)
def load_all() -> tuple[InstallmentCampaign, ...]:
    """Load every campaign YAML in the repository. Cached for process lifetime."""
    base = paths.INSTALLMENT_CAMPAIGNS_REPO_DIR
    if not base.exists():
        return ()
    out = []
    for path in sorted(base.glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        out.append(_parse_campaign(data, path))
    return tuple(out)


def by_id(campaign_id: str) -> InstallmentCampaign:
    """Look up one campaign by its `id`. Raises if unknown."""
    for c in load_all():
        if c.id == campaign_id:
            return c
    known = sorted(c.id for c in load_all())
    raise InstallmentCampaignNotFoundError(
        f"unknown installment campaign {campaign_id!r}; known ids: {known}"
    )


def detect_from_note(note: str | None) -> InstallmentCampaign | None:
    """DEFINITIVE detection: does this row's `Note` name a known campaign?

    Matching on the note (rather than the merchant string) is what makes
    campaign membership inheritable — the note on an earlier term is the
    only durable record that the plan was converted.
    """
    if not note:
        return None
    for c in load_all():
        if c.note_contains and c.note_contains in note:
            return c
    return None


def detect_from_rows(rows: list[dict]) -> InstallmentCampaign | None:
    """Definitive detection across every recorded term of one plan.

    Returns the first campaign named by any row's `Note`. A single tagged
    term is enough: the campaign applies to the plan as a whole, and a
    partially-tagged plan means earlier automation missed some terms (which
    is exactly the gap this module closes) — not that the plan is mixed.
    """
    for r in rows:
        if (c := detect_from_note(r.get("note"))) is not None:
            return c
    return None


def hint_for_plan(*, issuer: str | None, total_terms: int | None) -> list[str]:
    """ADVISORY: campaign ids whose term-count signature this plan matches.

    Returns ids only — callers surface them for a human to confirm and must
    never apply the reward treatment off the back of a hint. A term count is
    circumstantial: Dee-Jang issues 4 terms, but so could a merchant.
    """
    if not issuer or not total_terms:
        return []
    return [
        c.id
        for c in load_all()
        if c.status == "active"
        and c.issuer.casefold() == issuer.casefold()
        and total_terms in c.typical_total_terms
    ]
