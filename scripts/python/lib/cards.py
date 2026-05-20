"""Card-name → Notion page resolution for a given holder.

deterministic + idempotent — safe to re-run.

Matching is strict: case-sensitive equality on the title text after
trimming whitespace. We never substring-match (`UOB One` is not
`UOB World`), and we never invent a card if zero matches. The caller
gets an explicit error and is expected to surface it to the user.
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
    """Return the single Card page whose title exactly equals `card_name`."""
    target = (card_name or "").strip()
    if not target:
        raise CardNotFoundError("card name is required")

    pages = notion_client.query_all(cards_ds)
    exact = [p for p in pages if _title_text(p).strip() == target]

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


def list_card_titles(cards_ds: str) -> list[str]:
    """Helper for diagnostics / fuzzy suggestions."""
    return sorted({_title_text(p).strip() for p in notion_client.query_all(cards_ds)})
