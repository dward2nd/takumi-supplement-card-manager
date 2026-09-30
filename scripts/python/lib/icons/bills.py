"""Icons for Bills rows: where the bill stands — 📝 draft, 🧾 final.

deterministic + idempotent — a pure function of the bill's title.

Every row is a bill, and the `Card` relation already shows whose card it is,
so the icon says the one thing the row doesn't: whether the bill is still a
draft (`[DRAFT] …`, drafted from transactions or a placeholder awaiting the
statement) or final. Paid-ness has its own checkbox, `จ่ายแล้ว`, so it gets
no icon (user, 2026-09-30).

The writers that turn a draft final (/update-bill's finalize,
/record-statement completing a placeholder) re-set the icon with the title.
A title edited by hand in Notion keeps its old icon until
`backfill-icons --db bills --replace`.
"""

from __future__ import annotations

from ..bills import DRAFT_PREFIX
from .base import PageIcons, emoji, title_of

DRAFT = "📝"
FINAL = "🧾"


def bill_icon(title: str) -> dict:
    return emoji(DRAFT if title.startswith(DRAFT_PREFIX) else FINAL)


class BillIcons(PageIcons):
    def icon(self, properties: dict) -> dict | None:
        return bill_icon(title_of(properties))
