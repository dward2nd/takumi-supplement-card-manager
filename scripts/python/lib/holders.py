"""Holder → data source ID routing.

deterministic + idempotent — safe to re-run.

Source of truth for these IDs is /CLAUDE.md. If you edit one, edit both.
Takumi (เว็บ) is the primary card holder; Baiboon (ใบบุญ) and Nuta (นุตา)
are supplement holders. Each has their own Cards and Transactions data
sources, and a Bills data source. Takumi is a `PrimaryHolder` — his Bills
DB (added 2026-09-27) is statement-driven, see `statement_bills` — and
Baiboon and Nuta are `SupplementHolder`s.

Since 2026-09-28 each holder also has a cashback tracker
(`รายการติดตามเครดิตเงินคืนของ<name>`), and all three share one Promotion
Bureau DS — see `lib.bureau`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

# Multiplier checkboxes every Transactions DS has; the primary's adds ×3. ×6 was
# added to all three on 2026-10-05 (Lotus's coins at Lotus's).
_MULTIPLIERS = frozenset({"×0", "×2", "×4", "×5", "×6", "÷4"})


@dataclass(frozen=True)
class Holder:
    """Where one cardholder's data lives. What kind of holder they are — the
    primary or a supplement — is the subclass."""

    key: str
    thai_name: str
    transactions_ds: str
    cards_ds: str
    bills_ds: str | None
    # `รายการติดตามเครดิตเงินคืนของ<name>` — one row per promotion credit the
    # holder expects back. Linked to the Promotion Bureau via `Promotion`.
    cashback_tracker_ds: str | None = None

    # True when this holder's bills are the bank statement's per-card totals
    # — principal plus every supplement section — not a sum of the holder's
    # own Transactions rows. Anything that computes a bill, or books a
    # full-bill payment, from one holder's rows must refuse such a holder.
    statement_bills: ClassVar[bool] = False
    # The multiplier checkboxes this holder's Transactions DS has.
    multipliers: ClassVar[frozenset[str]] = _MULTIPLIERS


@dataclass(frozen=True)
class PrimaryHolder(Holder):
    """Takumi: the accounts are his. He pays each card's whole bill to the bank,
    so his bill covers Baiboon's and Nuta's charges on it too, and his
    Transactions DS alone has the ×3 box."""

    statement_bills: ClassVar[bool] = True
    multipliers: ClassVar[frozenset[str]] = _MULTIPLIERS | {"×3"}


@dataclass(frozen=True)
class SupplementHolder(Holder):
    """Baiboon, Nuta: supplement cards on Takumi's accounts. Their bills are
    drafted from their own rows, and they pay Takumi."""


# The household-wide promotion ledger: one row per promotion period, linking
# every holder's qualifying transactions (`รายการใช้จ่ายจาก<name>`).
PROMOTION_BUREAU_DS = "3e7cb755-f0f1-80f0-8c78-000b1d9f44cb"
# Promotion Catalogues (2026-09-30): a Thai reading page per merchant per month — every promotion + a spending plan.
PROMOTION_CATALOGUES_DS = "3ebcb755-f0f1-80d5-a580-000bf9448d23"


HOLDERS: dict[str, Holder] = {
    "takumi": PrimaryHolder(
        key="takumi",
        thai_name="เว็บ",
        transactions_ds="1aacb755-f0f1-81dc-8e9f-000b20891025",
        cards_ds="1aacb755-f0f1-818a-a284-000b17d155de",
        bills_ds="63dcb755-f0f1-83df-aaa8-871bb9069dae",
        cashback_tracker_ds="96bcb755-f0f1-83ef-a5b9-079f9ba3ae98",
    ),
    "baiboon": SupplementHolder(
        key="baiboon",
        thai_name="ใบบุญ",
        transactions_ds="181cb755-f0f1-8167-b5b6-000bc6d47469",
        cards_ds="99bb5ba6-79b1-47e2-9b8f-fa3102d5b294",
        bills_ds="192cb755-f0f1-8064-9075-000be05ba72d",
        cashback_tracker_ds="374cb755-f0f1-80b2-97cc-000b0105e43e",
    ),
    "nuta": SupplementHolder(
        key="nuta",
        thai_name="นุตา",
        transactions_ds="2a1cb755-f0f1-8110-9795-000bf7d48b4f",
        cards_ds="2a1cb755-f0f1-8188-9b00-000b5fa448b8",
        bills_ds="2a1cb755-f0f1-8193-982d-000bd4e3156c",
        cashback_tracker_ds="2e4cb755-f0f1-838a-9317-877c67577916",
    ),
}


def primary() -> Holder:
    """The one holder whose accounts the others' cards sit on."""
    return next(h for h in HOLDERS.values() if isinstance(h, PrimaryHolder))


def supplements() -> list[Holder]:
    return [h for h in HOLDERS.values() if isinstance(h, SupplementHolder)]


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
