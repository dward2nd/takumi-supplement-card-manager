"""Card-name → Notion page resolution for a given holder.

deterministic + idempotent — safe to re-run.

Matching is strict first, then forgiving on case only: exact
case-sensitive equality on the title text after trimming whitespace,
falling back to case-insensitive equality when that finds nothing. We
never substring-match (`UOB One` is not `UOB World`), we never resolve
an ambiguous match, and we never invent a card if zero matches. The
caller gets an explicit error and is expected to surface it to the user.
"""

from __future__ import annotations

from . import notion_client


class CardNotFoundError(RuntimeError):
    pass


class CardAmbiguousError(RuntimeError):
    pass


def _title_text(page: dict) -> str:
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    return ""


def find_card(cards_ds: str, card_name: str) -> dict:
    """Return the single Card page whose title equals `card_name`.

    Two passes, strict to forgiving:

    1. exact, case-sensitive match;
    2. case-insensitive match, when pass 1 finds nothing.

    Pass 2 exists because a card's name is spelled independently in more
    than one place, and they do not always agree on case: `Krungsri VISA`
    (Cards DS title) vs `Krungsri Visa` (the YAML repo, and the Bills `Card`
    SELECT before it became a relation on 2026-09-30); see
    docs/concepts/known-divergences.md #11. A caller passing either spelling
    must land on the same page. `card_repo.by_name` carries the same
    case-insensitive fallback for the same reason.

    Case folding cannot reintroduce the confusion strictness guards against
    — `UOB One` and `UOB World` differ by more than case — and an ambiguous
    fold still raises rather than guessing.
    """
    target = (card_name or "").strip()
    if not target:
        raise CardNotFoundError("card name is required")

    pages = notion_client.query_all(cards_ds)
    exact = [p for p in pages if _title_text(p).strip() == target]

    if not exact:
        exact = [p for p in pages if _title_text(p).strip().casefold() == target.casefold()]

    if not exact:
        substring_hits = sorted(
            {_title_text(p).strip() for p in pages if target.lower() in _title_text(p).lower()}
        )
        raise CardNotFoundError(
            f"no card titled exactly {target!r} in this holder's Cards DB. "
            f"Substring candidates: {substring_hits or 'none'}"
        )
    if len(exact) > 1:
        raise CardAmbiguousError(
            f"multiple cards titled {target!r}: page IDs {[p['id'] for p in exact]}"
        )
    return exact[0]


def card_title_text(page: dict) -> str:
    """A Card page's title, whitespace-trimmed."""
    return _title_text(page).strip()


def card_titles_by_id(cards_ds: str) -> dict[str, str]:
    """{page id → title} for every row of a Cards DB, in one query.

    For resolving many `Card` relation IDs at once — a relation carries only
    the page ID.
    """
    return {p["id"]: card_title_text(p) for p in notion_client.query_all(cards_ds)}


def list_card_titles(cards_ds: str) -> list[str]:
    """Helper for diagnostics / fuzzy suggestions."""
    return sorted({_title_text(p).strip() for p in notion_client.query_all(cards_ds)})
