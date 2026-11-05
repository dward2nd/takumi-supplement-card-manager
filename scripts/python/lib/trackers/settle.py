"""Plan and apply one tracker settlement.

deterministic + idempotent — links are merged, never dropped; a second run
with the same spec finds nothing left to write.

A ticked tracker is frozen: `/sync-promotion` never changes it, and neither
does this. Re-running on one reports `unchanged`; asking it to add a link,
change the Note or untick is refused.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

from .. import notion_client
from ..bureau.store import BureauRow, find_row
from ..holders import resolve_holder
from .basis import Context, judge, period_over
from .model import LINKS, NOTE, SETTLED, LedgerRow, find_tracker, ledger_row, page_id

BANGKOK = ZoneInfo("Asia/Bangkok")


class FrozenTracker(RuntimeError):
    """The tracker is ticked; its row can't change any more."""


@dataclass(frozen=True)
class Spec:
    holder: str
    tracker: str
    link: tuple[str, ...] = ()
    tick: str | bool = "auto"            # "auto" | True (the user's word) | False (link only)
    basis: str = "auto"
    note: str | None = None              # replaces the Note; None keeps it

    @classmethod
    def parse(cls, raw: dict) -> "Spec":
        unknown = set(raw) - {"holder", "tracker", "link", "tick", "basis", "note"}
        if unknown:
            raise ValueError(f"unknown spec keys: {sorted(unknown)}")
        for key in ("holder", "tracker"):
            if not raw.get(key):
                raise ValueError(f"{key!r} is required")
        link = raw.get("link") or []
        if isinstance(link, str):
            link = [link]
        tick = raw.get("tick", "auto")
        if tick not in ("auto", True, False):
            raise ValueError("tick must be \"auto\", true or false")
        return cls(holder=raw["holder"], tracker=raw["tracker"], link=tuple(link), tick=tick,
                   basis=raw.get("basis", "auto"), note=raw.get("note"))


@dataclass
class Plan:
    properties: dict = field(default_factory=dict)
    envelope: dict = field(default_factory=dict)


def _row_json(r: LedgerRow) -> dict:
    return {"id": r.id, "name": r.name, "amount": float(r.amount),
            "bill_cycle": r.bill_cycle.isoformat() if r.bill_cycle else None}


def plan(spec: Spec, today: dt.date | None = None) -> Plan:
    today = today or dt.datetime.now(BANGKOK).date()
    holder = resolve_holder(spec.holder)
    tracker = find_tracker(holder, spec.tracker)
    bureau: BureauRow | None = find_row(tracker.promotion_id) if tracker.promotion_id else None

    new_ids = []
    for ref in spec.link:
        pid = page_id(ref)
        if pid is None:
            raise ValueError(f"link {ref!r} is not a page ID or URL")
        new_ids.append(pid)
    known = {i.replace("-", "") for i in tracker.links}
    added = [ledger_row(holder, i) for i in dict.fromkeys(new_ids) if i.replace("-", "") not in known]
    existing = [ledger_row(holder, i) for i in tracker.links]
    rows = tuple(existing + added)

    ctx = Context(holder=holder, tracker=tracker, rows=rows, bureau=bureau)
    basis_key, verdict = judge(spec.basis, ctx)
    over = period_over(bureau, today)
    if spec.tick is True:
        tick, why = True, "ticked on the caller's word"
    elif spec.tick is False:
        tick, why = False, "link only (tick: false)"
    elif not over:
        tick, why = False, f"the period runs to {bureau.end}: link now, tick once it has ended"
    elif not verdict.ok:
        tick, why = False, verdict.reason
    else:
        tick, why = True, verdict.reason

    note_changes = spec.note is not None and spec.note != tracker.note
    props: dict = {}
    if added:
        props[LINKS] = {"relation": [{"id": i} for i in list(tracker.links) + [r.id for r in added]]}
    if tick and not tracker.settled:
        props[SETTLED] = {"checkbox": True}
    if note_changes:
        props[NOTE] = {"rich_text": [{"type": "text", "text": {"content": spec.note}}]}

    if tracker.settled:
        if spec.tick is False:
            raise FrozenTracker(f"{tracker.title!r} is ticked; trackers are never unticked here")
        if props:
            raise FrozenTracker(f"{tracker.title!r} is ticked, so it can't change: "
                                f"would write {sorted(props)}")

    warnings = [f"{r.name} ฿{r.amount} is not a credit (amount ≥ 0)" for r in added if not r.is_credit]
    envelope = {
        "holder": holder.key,
        "tracker": {
            "id": tracker.id, "title": tracker.title,
            "expected": float(tracker.expected) if tracker.expected is not None else None,
            "bureau": bureau.name if bureau else None,
            "period_end": bureau.end.isoformat() if bureau else None,
            "settled_before": tracker.settled,
        },
        "links": {"kept": [_row_json(r) for r in existing], "added": [_row_json(r) for r in added]},
        "credit_linked": float(ctx.credit),
        "bureau_total": float(bureau.total) if bureau and bureau.total is not None else None,
        "basis": {"key": basis_key, "ok": verdict.ok, "reason": verdict.reason},
        "tick": {"requested": spec.tick, "ticked": tracker.settled or tick, "reason": why},
        "writes": sorted(props) if props else [],
        "unchanged": not props,
        "warnings": warnings,
    }
    return Plan(properties=props, envelope=envelope)


def settle(spec: Spec, *, dry_run: bool = False, today: dt.date | None = None) -> dict:
    p = plan(spec, today)
    if p.properties and not dry_run:
        notion_client.update_page_properties(p.envelope["tracker"]["id"], p.properties)
    return {**p.envelope, "dry_run": dry_run}
