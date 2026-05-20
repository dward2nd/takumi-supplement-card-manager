"""Holder → data source ID routing.

deterministic + idempotent — safe to re-run.

Source of truth for these IDs is /CLAUDE.md. If you edit one, edit both.
Takumi (เว็บ) is the primary card holder; Baiboon (ใบบุญ) and Nuta (นุตา)
are supplement holders. Each has their own Cards and Transactions data
sources; only Baiboon and Nuta have Bills (Takumi does not).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Holder:
    key: str
    thai_name: str
    transactions_ds: str
    cards_ds: str
    bills_ds: str | None


HOLDERS: dict[str, Holder] = {
    "takumi": Holder(
        key="takumi",
        thai_name="เว็บ",
        transactions_ds="1aacb755-f0f1-81dc-8e9f-000b20891025",
        cards_ds="1aacb755-f0f1-818a-a284-000b17d155de",
        bills_ds=None,
    ),
    "baiboon": Holder(
        key="baiboon",
        thai_name="ใบบุญ",
        transactions_ds="181cb755-f0f1-8167-b5b6-000bc6d47469",
        cards_ds="99bb5ba6-79b1-47e2-9b8f-fa3102d5b294",
        bills_ds="192cb755-f0f1-8064-9075-000be05ba72d",
    ),
    "nuta": Holder(
        key="nuta",
        thai_name="นุตา",
        transactions_ds="2a1cb755-f0f1-8110-9795-000bf7d48b4f",
        cards_ds="2a1cb755-f0f1-8188-9b00-000b5fa448b8",
        bills_ds="2a1cb755-f0f1-8193-982d-000bd4e3156c",
    ),
}


def resolve_holder(name: str) -> Holder:
    """Accept English key or verbatim Thai name; reject anything else."""
    if not name:
        raise KeyError("holder is required (takumi/baiboon/nuta)")
    key = name.strip().lower()
    if key in HOLDERS:
        return HOLDERS[key]
    for h in HOLDERS.values():
        if h.thai_name == name.strip():
            return h
    raise KeyError(
        f"unknown holder: {name!r}; expected one of "
        f"{sorted(HOLDERS)} or Thai names {[h.thai_name for h in HOLDERS.values()]}"
    )
