"""Every card's latest statement PDF, from the `ใบแจ้งยอด (PDF)` files on the Bills DBs.

deterministic + idempotent — reads Notion and downloads to a scratch directory.

Per (holder, card), the Bills row with the latest `วันตัดรอบบิล` that carries a
statement PDF; each of its files is parsed with the card issuer's parser. The
same PDF sits on several bills (UOB bundles cards and holders; a friend's bill
keeps a copy), so files are de-duplicated by content before parsing.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from lib import card_repo, notion_client, notion_files
from lib.bills import STATEMENT_PDF, bill_card_id
from lib.cards import card_titles_by_id
from lib.holders import HOLDERS
from lib.statements import PARSERS, load_card_pdf
from lib.statements.model import Statement
from lib.statements.parser import StatementParser

_WITH_PARSER = {p.issuer for p in PARSERS.values()}


def _latest_bills() -> list[tuple[str, str, dict]]:
    """[(holder, card, bill page)] — each card's latest bill with a statement PDF."""
    out = []
    for key, holder in HOLDERS.items():
        if not holder.bills_ds:
            continue
        latest: dict[str, tuple[str, dict]] = {}
        titles = card_titles_by_id(holder.cards_ds)
        for page in notion_client.query_all(holder.bills_ds):
            props = page["properties"]
            card = titles.get(bill_card_id(page) or "")
            bc = ((props.get("วันตัดรอบบิล") or {}).get("date") or {}).get("start")
            if card and bc and (props.get(STATEMENT_PDF) or {}).get("files") and bc > latest.get(card, ("",))[0]:
                latest[card] = (bc, page)
        out += [(key, card, page) for card, (_, page) in sorted(latest.items())]
    return out


def latest_statements(work_dir: Path) -> tuple[list[tuple[Statement, StatementParser, str]], list[str]]:
    """([(statement, parser, source file name)], warnings) for every card's latest statement."""
    found, warnings, seen = [], [], set()
    for holder, card, page in _latest_bills():
        repo = card_repo.get(card)
        if repo is None or repo.issuer not in _WITH_PARSER:
            continue   # no statement parser for this issuer (ttb, Grab, Shopee …)
        for i, f in enumerate(page["properties"][STATEMENT_PDF]["files"]):
            if f.get("type") != "file":
                continue
            target = work_dir / f"{holder}-{page['id']}-{i}"
            target.mkdir(parents=True, exist_ok=True)
            path, name = notion_files.download_file(f, target)
            digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            try:
                statement, parser = load_card_pdf(path, repo.issuer)
            except Exception as e:
                warnings.append(f"{holder}'s {card} bill: {name} not read ({e})")
                continue
            found.append((statement, parser, name))
    return found, warnings
