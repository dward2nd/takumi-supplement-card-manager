"""Installment merchant-name parsing and per-card population.

deterministic + idempotent — re-running `populate` against the same
(holder, card, bill_cycle) skips plans whose cluster already has a row
in the target cycle.

Installment transactions are identified by a trailing ``NN/NN`` suffix on
the merchant name, e.g. ``2C2P *SHOPEE 03/10`` — the third of ten terms.
The suffix is zero-padded to match the width of the total (so a 10-term
plan reads ``01/10``, a 100-term plan reads ``001/100``).

Parallel plans under the same bank-side merchant string (the user often
runs multiple Shopee installments at once) are disambiguated by per-term
amount: rows in the same (base, total) group are clustered within a 2%
tolerance, and each cluster is its own plan with its own term sequence.

This module is the single source of truth for the format so that add-,
populate-, prepare-, and update-bill skills agree on what counts as an
installment row.
"""

from __future__ import annotations

import datetime as _dt
import re
from collections import defaultdict
from dataclasses import dataclass


# Suffix matches `<base>` + space + `NN/NN`. The base is any non-empty
# prefix; the term/total are 1+ digits each. We anchor on end-of-string
# so middle-of-name `12/03` (e.g. a date) is never misread.
_INSTALLMENT_SUFFIX_RE = re.compile(r"^(?P<base>.+?)\s+(?P<term>\d{1,3})/(?P<total>\d{1,3})$")

# Plans within a (base, total) group are clustered by per-term amount.
# Two amounts match iff they're within this fractional distance —
# tolerates the small per-term rounding the bank sometimes applies
# (e.g. 375.30 → 373.00 across consecutive terms, ~0.6%).
#
# Tightened 5% → 2% on 2026-07-26: two genuinely-distinct Nuta Shopee
# plans running at 1,032.60 and 1,079.20 per term are only 4.3% apart, so
# the old 5% window merged them into one cluster and populate-installment
# under-tracked the pair. 2% cleanly separates them while still absorbing
# every observed single-plan rounding gap (all ≤0.61% across all holders /
# cards — verified before the change). Keep this above the largest genuine
# per-term rounding and below the smallest real two-plan gap.
_AMOUNT_TOLERANCE = 0.02


@dataclass(frozen=True)
class InstallmentName:
    base: str        # merchant name without the trailing " NN/NN"
    term: int        # 1-indexed; 1 == first term
    total: int       # total number of terms in the plan


def parse(name: str) -> InstallmentName | None:
    """Parse an installment merchant name. Returns None if the suffix is absent.

    Examples:
        >>> parse("2C2P *SHOPEE 01/10")
        InstallmentName(base='2C2P *SHOPEE', term=1, total=10)
        >>> parse("TMN 7-11 BANGKOK TH")  # no suffix
        >>>
    """
    if not isinstance(name, str):
        return None
    m = _INSTALLMENT_SUFFIX_RE.match(name.strip())
    if not m:
        return None
    term = int(m.group("term"))
    total = int(m.group("total"))
    if term < 1 or total < 1 or term > total:
        # Bogus suffix — don't try to be clever, just reject.
        return None
    return InstallmentName(base=m.group("base").strip(), term=term, total=total)


def format_name(base: str, term: int, total: int) -> str:
    """Format an installment merchant name.

    The suffix is zero-padded to match the *width* of `total` (so a 10-term
    plan reads ``01/10`` and a 100-term plan reads ``001/100``). This keeps
    sorting lexicographic ↔ numeric.
    """
    if not base or not base.strip():
        raise ValueError("installment base merchant name is required")
    if term < 1 or total < 1 or term > total:
        raise ValueError(f"invalid installment term/total: {term}/{total}")
    width = max(2, len(str(total)))
    return f"{base.strip()} {term:0{width}d}/{total:0{width}d}"


def is_installment(name: str) -> bool:
    """True iff the merchant name carries an installment suffix."""
    return parse(name) is not None


def _amounts_match(a: float, b: float) -> bool:
    if a == 0 and b == 0:
        return True
    denom = max(abs(a), abs(b))
    if denom == 0:
        return False
    return abs(a - b) / denom < _AMOUNT_TOLERANCE


def cluster_rows_by_plan(rows: list[dict]) -> list[list[dict]]:
    """Partition installment rows into distinct plans.

    Each row must already carry the parsed installment info under the
    `_installment` key (see `fetch_card_installment_rows`). Rows are
    first grouped by (base, total), then clustered by per-term amount
    within each group. Each returned cluster is one plan.
    """
    groups: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for r in rows:
        info: InstallmentName = r["_installment"]
        groups[(info.base, info.total)].append(r)

    clusters: list[list[dict]] = []
    for _key, entries in sorted(groups.items()):
        buckets: list[list[dict]] = []
        for r in entries:
            amt = float(r.get("amount") or 0.0)
            placed = False
            for c in buckets:
                ref = float(c[0].get("amount") or 0.0)
                if _amounts_match(amt, ref):
                    c.append(r)
                    placed = True
                    break
            if not placed:
                buckets.append([r])
        clusters.extend(buckets)
    return clusters


def fetch_card_installment_rows(transactions_ds: str, card_page_id: str) -> list[dict]:
    """Return every installment row on the card (annotated with parsed info).

    Reads from Notion via `lib.notion_client`. Side-effectful — issues a
    paginated query against the holder's Transactions data source. Keeps
    only rows whose merchant name parses as an installment.
    """
    # Local imports to avoid pulling notion-client into modules that
    # only need parse/format.
    from . import notion_client
    from .transaction_read import project_transaction

    raw = notion_client.query_all(
        transactions_ds,
        filter={"property": "Card", "relation": {"contains": card_page_id}},
    )
    out: list[dict] = []
    for page in raw:
        tx = project_transaction(page)
        info = parse(tx.get("name") or "")
        if info is None:
            continue
        tx["_installment"] = info
        out.append(tx)
    return out


def populate_for_cycle(
    *,
    holder_key: str,
    transactions_ds: str,
    card_name: str,
    card_page_id: str,
    bill_cycle: str,
    due_date: str,
    auto_classify: bool = True,
    exclude: set[str] | None = None,
    dry_run: bool = False,
) -> dict:
    """Append next-term rows for every in-progress plan on the card.

    Returns the same envelope shape as `populate-installment/cli.py`'s
    `run()` minus `holder`/`card`/`bill_cycle`/`due_date` (callers
    decorate). Used by /populate-installment directly and by /prepare-bill
    via this function — keeps a single implementation in one place.
    """
    from . import notion_client, promotions  # local — keep parse/format light
    from .transaction_write import build_transaction_properties

    exclude = exclude or set()
    if auto_classify and holder_key == "takumi":
        raise ValueError(
            "auto_classify is not supported for holder='takumi' "
            "(Takumi's Transactions DS has no `% cb` field)"
        )

    rows = fetch_card_installment_rows(transactions_ds, card_page_id)
    plans: list[dict] = []
    count_appended = 0
    count_skipped = 0

    for cluster in cluster_rows_by_plan(rows):
        info: InstallmentName = cluster[0]["_installment"]
        base, total = info.base, info.total
        latest = max(cluster, key=lambda r: r["_installment"].term)
        max_term = latest["_installment"].term
        seed_amount = round(float(cluster[0].get("amount") or 0.0), 2)
        entry: dict = {
            "base": base,
            "total_terms": total,
            "max_term": max_term,
            "per_term_amount": seed_amount,
        }

        if base in exclude:
            entry["action"] = "skipped-excluded"
            count_skipped += 1
            plans.append(entry)
            continue

        if max_term >= total:
            entry["action"] = "skipped-complete"
            count_skipped += 1
            plans.append(entry)
            continue

        if any(r.get("bill_cycle_date") == bill_cycle for r in cluster):
            entry["action"] = "skipped-already-in-cycle"
            count_skipped += 1
            plans.append(entry)
            continue

        next_term = max_term + 1
        next_name = format_name(base, term=next_term, total=total)
        amount = float(latest.get("amount") or 0.0)

        multiplier = None
        cashback_percent = None
        note = None
        classification_info = None
        if auto_classify:
            cls = promotions.classify(
                card_name, _dt.date.fromisoformat(bill_cycle), next_name,
                is_installment_override=True,
            )
            classification_info = {
                "promotion_id": cls.promotion_id,
                "reason": cls.reason,
                "cashback_percent": cls.cashback_percent,
                "points_override": cls.points_override,
            }
            cashback_percent = cls.cashback_percent
            multiplier = cls.points_override
            note = cls.note

        props = build_transaction_properties(
            name=next_name,
            amount=amount,
            transaction_date=bill_cycle,
            bill_cycle_date=bill_cycle,
            due_date=due_date,
            card_page_id=card_page_id,
            processed=True,
            note=note,
            multiplier=multiplier,
            cashback_percent=cashback_percent,
        )

        entry["action"] = "appended"
        entry["next_term"] = next_term
        entry["next_name"] = next_name
        entry["amount"] = amount
        if classification_info is not None:
            entry["classification"] = classification_info

        if dry_run:
            entry["dry_run"] = True
            entry["properties"] = props
        else:
            page = notion_client.create_page(transactions_ds, props)
            entry["created"] = {
                "id": page["id"],
                "url": page.get("url"),
                "name": next_name,
                "amount": amount,
                "date": bill_cycle,
            }

        count_appended += 1
        plans.append(entry)

    return {
        "in_progress": plans,
        "count_appended": count_appended,
        "count_skipped": count_skipped,
    }


def in_progress_summary(transactions_ds: str, card_page_id: str) -> list[dict]:
    """Return a compact summary of in-progress plans (read-only, no writes).

    Each item: {base, total_terms, max_term, per_term_amount, remaining_terms}.
    Used by /update-bill to surface ongoing installment commitments without
    populating anything.
    """
    rows = fetch_card_installment_rows(transactions_ds, card_page_id)
    out: list[dict] = []
    for cluster in cluster_rows_by_plan(rows):
        info: InstallmentName = cluster[0]["_installment"]
        latest = max(cluster, key=lambda r: r["_installment"].term)
        max_term = latest["_installment"].term
        if max_term >= info.total:
            continue  # plan complete; not in progress
        seed_amount = round(float(cluster[0].get("amount") or 0.0), 2)
        out.append({
            "base": info.base,
            "total_terms": info.total,
            "max_term": max_term,
            "remaining_terms": info.total - max_term,
            "per_term_amount": seed_amount,
        })
    return out
