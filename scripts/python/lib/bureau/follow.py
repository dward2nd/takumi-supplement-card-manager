"""Keep the Promotion Bureau in step with the ledger rows a skill just wrote.

deterministic + idempotent — re-syncs Bureau rows through `runner` (itself
idempotent) and sets transaction fields to what the split expects; following
the same rows again writes nothing.

/add-transaction, /update-transaction and /record-statement hand `follow` the
rows they wrote. For each row it finds the Bureau rows it can count toward:
the ones it's already linked to, and, for every campaign on its card, the row
for the quota period its date (or bill cycle) falls in. It re-syncs those with
`link_candidates`, so eligible rows are linked, the reward re-split, and the
shares and trackers updated. Then it writes every linked row's `% cb` /
multiplier / `ใช้คะแนน` to what the split expects (user, 2026-09-28).

A fix can move a row into another quota (a UOB One 10%/5% row past the ฿500
becomes 1%, which the cycle's 1% quota counts), so the rows it fixed are
followed again, until a pass fixes nothing.

An edit that moves a row onto another statement cycle (or card) unlinks it
from the Bureau row it no longer belongs to, which is then re-synced without it.

It never creates a Bureau row. A period with no row comes back under `missing`
with the /sync-promotion spec that creates it. Periods before a campaign's
first Bureau row are untracked, so they aren't reported.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import dataclass
from decimal import Decimal

from .. import notion_client
from ..bill_cycle import PatternNotFoundError
from ..holders import HOLDERS
from ..transaction_read import project_transaction
from ..transaction_write import build_update_properties
from . import PROMOTIONS, promotion_for, runner, store
from .base import CASHBACK, RIGHTS, BasePromotion, Tx
from .store import LINK, BureauRow

MAX_PASSES = 4
_MONTH = re.compile(r"^(\d{4})M(\d{1,2})\b")


@dataclass(frozen=True)
class Written:
    """A transaction row, as much as the Bureau needs to place it."""

    id: str | None                   # None on a dry run: nothing written yet
    holder: str
    card: str                        # the Card relation's title
    day: dt.date                     # `Transaction Datetime`
    bill_cycle: dt.date | None       # `Bill Cycle Date`
    links: tuple[str, ...] = ()      # Bureau rows it's already linked to (`Promotion`)
    name: str = ""                   # the merchant string (installment terms and posting rules read it)
    posted: str | None = None        # `Process Date`, once a statement has given it

    @classmethod
    def of(cls, id: str | None, holder: str, card_id: str, day: str, bill_cycle: str | None,
           links: tuple[str, ...] = (), name: str = "", posted: str | None = None) -> Written:
        return cls(id=id, holder=holder, card=store.card_titles(holder).get(card_id, ""),
                   day=dt.date.fromisoformat(day[:10]),
                   bill_cycle=dt.date.fromisoformat(bill_cycle[:10]) if bill_cycle else None,
                   links=links, name=name, posted=posted[:10] if posted else None)

    @property
    def label(self) -> str:
        return f"{self.holder} {self.day} {self.name}".rstrip()

    def as_tx(self) -> Tx:
        """The row as a campaign sees it (no amount needed to place it)."""
        return Tx(id=self.id or "", holder=self.holder, name=self.name, amount=Decimal(0),
                  date=self.day.isoformat(), card=self.card, posted=self.posted,
                  bill_cycle=self.bill_cycle.isoformat() if self.bill_cycle else None)


def read(page_ids: list[str]) -> list[Written]:
    """The rows as they stand in Notion (after /update-transaction's writes)."""
    by_ds = {h.transactions_ds: h.key for h in HOLDERS.values()}
    out = []
    for pid in page_ids:
        page = notion_client.get_page(pid)
        holder = by_ds.get(page.get("parent", {}).get("data_source_id"))
        t = project_transaction(page)
        if holder is None or not t["transaction_date"]:
            continue  # not a Transactions row, or undated
        links = tuple(r["id"] for r in page["properties"].get(LINK, {}).get("relation", []))
        out.append(Written.of(page["id"], holder, (t["card_ids"] or [""])[0], t["transaction_date"],
                              t["bill_cycle_date"], links, t["name"], t["process_date"]))
    return out


# -- placing rows --------------------------------------------------------------


def _load() -> tuple[list[tuple[BureauRow, BasePromotion]], list[str]]:
    rows, warnings = [], []
    for row in store.all_rows():
        try:
            rows.append((row, promotion_for(row.name, row.start, row.end)))
        except LookupError:
            warnings.append(f"Bureau row {row.name!r} matches no campaign class; left alone")
    return rows, warnings


def _covers(row: BureauRow, promo: BasePromotion, w: Written) -> bool:
    return promo.covers(row.start, row.end, w.as_tx())


def _stale(w: Written, rows: list[tuple[BureauRow, BasePromotion]]) -> tuple[list[BureauRow], list[str]]:
    """(Bureau rows `w` should no longer be linked to, warnings).

    A row linked to a campaign its card isn't on, or outside a period the
    campaign reads off authoritative dates (a Bill Cycle Date; UOB One's
    posting dates), was moved by an edit or a statement: the old link goes. A
    calendar-month row dated outside its month is only warned about: the bank
    may count by posting date, so a link across a month boundary can be the
    household's deliberate call.
    """
    by_id = {r.id: (r, p) for r, p in rows}
    stale, warnings = [], []
    for r, p in (by_id[i] for i in w.links if i in by_id):
        if (w.card and w.card not in p.cards) or (p.authoritative_period and not _covers(r, p, w)):
            stale.append(r)
        elif not _covers(r, p, w):
            warnings.append(f"{w.label} is linked to {r.name!r} ({r.start}→{r.end}) but dated outside it; "
                            f"left linked — unlink it in Notion if the bank didn't post it in that month")
    return stale, warnings


def _unlink(written: list[Written], rows, write: bool) -> tuple[list[Written], list[dict], list[str]]:
    """Drop stale links from the written rows: (rows as they now stand, what was unlinked, warnings)."""
    out, unlinked, warnings = [], [], []
    for w in written:
        stale, ws = _stale(w, rows)
        warnings += ws
        if stale and w.id:
            keep = tuple(i for i in w.links if i not in {r.id for r in stale})
            if write:
                store.set_links(w.id, list(keep))
            unlinked += [{"row": w.label, "bureau": r.name} for r in stale]
            # Keep the old link in `links` so the old Bureau row is re-synced without it.
        out.append(w)
    return out, unlinked, warnings


def _place(w: Written, rows: list[tuple[BureauRow, BasePromotion]]
           ) -> tuple[set[str], list[dict], list[str]]:
    """(Bureau row ids to sync, missing periods, warnings) for one row."""
    known = {r.id for r, _ in rows}
    ids = {i for i in w.links if i in known}
    missing, warnings = [], []
    for cls in PROMOTIONS:
        promo = cls()
        if w.card not in promo.cards:
            continue
        try:
            period = promo.period_for(w.as_tx())
        except PatternNotFoundError as e:
            warnings.append(f"{cls.__name__}: {e}")
            continue
        if period is None:
            continue
        start, end = period
        name = promo.row_name(start, end)
        ours = [r for r, p in rows if type(p) is cls]
        hit = [r for r in ours if _covers(r, promo, w)]
        if not hit:
            # Same campaign and month, other dates: sync it anyway, and say why rows won't link.
            hit = [r for r in ours if (m := _MONTH.match(r.name)) and m.groups() == _MONTH.match(name).groups()]
            warnings += [f"{r.name!r} runs {r.start}→{r.end}, but the period is {start}→{end} "
                         f"({'a cycle row ends the day before its BC date' if promo.period_basis == 'bill_cycle' else 'a calendar month'}); "
                         f"rows in it can't be linked until its Start/End Date say so" for r in hit]
        ids |= {r.id for r in hit}
        if not hit and ours and end >= min(r.start for r in ours):
            spec = {"promotion": name, "start": start.isoformat(), "end": end.isoformat(),
                    "link_candidates": True}
            missing.append({"name": name, "campaign": cls.__name__, "create_with": spec})
    return ids, missing, warnings


def _affected(written: list[Written], rows) -> tuple[set[str], list[dict], list[str]]:
    ids: set[str] = set()
    missing: list[dict] = []
    warnings: list[str] = []
    for w in written:
        i, m, ws = _place(w, rows)
        ids |= i
        missing += [x for x in m if x not in missing]
        warnings += [x for x in ws if x not in warnings]
    return ids, missing, warnings


# -- following -----------------------------------------------------------------


def _summary(out: dict, writes: list[str], mine: set[str]) -> dict:
    """One Bureau row's result, trimmed to what the writer's caller acts on."""
    s: dict = {"bureau": out["promotion"]["name"]}
    if out["promotion"]["reward"] == CASHBACK:
        s["credit"], s["shares"] = out["totals"]["credit"], out["shares"]
    elif out["promotion"]["reward"] == RIGHTS:
        s["rights"] = out["totals"]["rights"]
    if writes:
        s["writes"] = writes
    not_linked = [{k: c[k] for k in ("row", "level", "reason")}
                  for c in out["unlinked_candidates"] if c["id"] in mine]
    if not_linked:
        s["not_linked"] = not_linked
    flagged = [{"row": row, "reason": g["reason"]} for g in out["flagged"]
               for row, i in zip(g["rows"], g["ids"]) if i in mine]
    if flagged:
        s["flagged"] = flagged
    if out["warnings"]:
        s["warnings"] = out["warnings"]
    return s


def follow(written: list[Written], *, dry_run: bool = False) -> dict:
    """Re-sync every Bureau row the written rows touch, and fix the fields the
    split disagrees with. A dry run only names the rows it would sync."""
    rows, warnings = _load()
    names = {r.id: r.name for r, _ in rows}
    written, unlinked, w = _unlink(written, rows, write=not dry_run)
    warnings += w
    queue, missing, w = _affected(written, rows)
    warnings += w
    if dry_run:
        return {"would_sync": sorted(names[i] for i in queue), "would_unlink": unlinked,
                "missing": missing, "warnings": warnings}

    mine = {x.id for x in written if x.id}
    latest: dict[str, dict] = {}
    writes: dict[str, list[str]] = {}
    fixed: list[dict] = []
    applied: set[tuple[str, str]] = set()
    for _ in range(MAX_PASSES):
        touched: list[str] = []
        for row_id in sorted(queue, key=names.get):
            out = runner.run({"promotion": row_id, "link_candidates": True})
            latest[row_id] = out
            writes.setdefault(row_id, []).extend(out["writes"])
            if out["held_back"]:
                continue  # the split disagrees with a hand-typed เงินคืนรวม; the warning says so
            for m in out["field_mismatches"]:
                key = (m["id"], json.dumps(m["want"], sort_keys=True))
                if key in applied:  # two quotas want different values; don't flip-flop
                    msg = (f"{m['row']}: {out['promotion']['name']} wants {m['want']} back after another "
                           f"quota changed it — left as {m['has']}; settle it by hand")
                    warnings += [msg] if msg not in warnings else []
                    continue
                applied.add(key)
                notion_client.update_page_properties(m["id"], build_update_properties(m["update"]))
                fixed.append({"row": m["row"], "bureau": out["promotion"]["name"],
                              "from": m["has"], "to": m["want"]})
                touched.append(m["id"])
        if not touched:
            break
        queue, _, _ = _affected(read(touched), rows)
    else:
        warnings.append(f"fields still changing after {MAX_PASSES} passes — run /sync-promotion "
                        f"on the rows under `synced`")

    return {
        "synced": [_summary(latest[i], writes[i], mine) for i in sorted(latest, key=names.get)],
        "unlinked": unlinked,
        "fixed": fixed,
        "missing": missing,
        "warnings": warnings,
    }


def follow_safely(written: list[Written] | None = None, *, ids: list[str] | None = None,
                  dry_run: bool = False) -> dict:
    """`follow` for a writer that has already written its rows — given as
    `written`, or as page `ids` to read back first. A failure here is reported,
    not raised, so the caller doesn't mistake it for a failed write (and, for
    /add-transaction, write the rows twice)."""
    try:
        return follow(read(ids) if ids is not None else written or [], dry_run=dry_run)
    except Exception as e:  # noqa: BLE001 — the rows are written either way
        return {"error": f"{type(e).__name__}: {e}",
                "hint": "the ledger rows are written; re-run /sync-promotion on the affected Bureau rows"}
