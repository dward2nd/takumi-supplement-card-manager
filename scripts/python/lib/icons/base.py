"""Shared pieces for page icons: the icon payload, a matching rule, the base class.

deterministic + idempotent — declarations and pure functions only.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

# The fallback when nothing more specific fits.
CARD = "💳"


def emoji(char: str) -> dict:
    """A Notion page icon. Always a real emoji: colourful, unlike Notion's own
    monochrome icon set (user, 2026-09-30)."""
    return {"type": "emoji", "emoji": char}


@dataclass(frozen=True)
class IconRule:
    """`emoji` for a name matching `pattern` (case-insensitive), or passing `test`."""

    emoji: str
    pattern: str | None = None
    test: Callable[[str], bool] | None = None

    def matches(self, name: str) -> bool:
        if self.pattern and re.search(self.pattern, name, re.IGNORECASE):
            return True
        return bool(self.test and self.test(name))


def first_match(rules: tuple[IconRule, ...], name: str) -> str | None:
    return next((r.emoji for r in rules if r.matches(name)), None)


def title_of(properties: dict) -> str:
    """The text of whichever property in a create payload is the title."""
    for value in properties.values():
        if isinstance(value, dict) and "title" in value:
            return "".join(t.get("text", {}).get("content", "") for t in value["title"])
    return ""


def number_of(properties: dict, name: str) -> float | None:
    value = properties.get(name)
    return value.get("number") if isinstance(value, dict) else None


class PageIcons(ABC):
    """Picks the icon for a new page in one kind of database."""

    @abstractmethod
    def icon(self, properties: dict) -> dict | None:
        """The icon payload for a page created with these properties, or None for none."""


class FixedIcon(PageIcons):
    """The same emoji for every page (a fallback where the caller knows better)."""

    def __init__(self, char: str) -> None:
        self.char = char

    def icon(self, properties: dict) -> dict | None:
        return emoji(self.char)
