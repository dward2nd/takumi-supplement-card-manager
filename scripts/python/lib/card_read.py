"""Project a Notion card page into a flat dict for summary display.

deterministic + idempotent — safe to re-run.

Pairs with the Cards data sources defined in `lib.holders`. The cards
DB and the "สรุปบัตรและสินเชื่อที่<name>ถือ" database share the same data
source ID — the summary title is just a different display name on the
same rows. So this projector serves both reads.

English-keyed projection (Thai property names looked up verbatim in
the page JSON, per project doc-language convention).
"""

from __future__ import annotations

from typing import Any


def _title(props: dict, name: str = "Name") -> str:
    return "".join(
        t.get("plain_text", "") for t in props.get(name, {}).get("title", []) or []
    )


def _rich_text(props: dict, name: str) -> str:
    return "".join(
        t.get("plain_text", "") for t in props.get(name, {}).get("rich_text", []) or []
    )


def _number(props: dict, name: str) -> float | None:
    return props.get(name, {}).get("number")


def _select(props: dict, name: str) -> str | None:
    sel = props.get(name, {}).get("select") or {}
    return sel.get("name")


def _checkbox(props: dict, name: str) -> bool:
    return bool(props.get(name, {}).get("checkbox"))


def _formula_number(props: dict, name: str) -> float | None:
    f = props.get(name, {}).get("formula") or {}
    if f.get("type") == "number":
        return f.get("number")
    return None


def _rollup_number(props: dict, name: str) -> float | None:
    r = props.get(name, {}).get("rollup") or {}
    if r.get("type") == "number":
        return r.get("number")
    return None


def _rollup_date(props: dict, name: str) -> str | None:
    """Rollup with aggregation=`latest_date` (or earliest) projects as a date."""
    r = props.get(name, {}).get("rollup") or {}
    if r.get("type") == "date":
        d = r.get("date") or {}
        return d.get("start")
    return None


def project_card(page: dict) -> dict[str, Any]:
    """Flatten a Cards-DS page into the columns the summary table shows."""
    props = page.get("properties", {})
    return {
        "id": page.get("id"),
        "url": page.get("url"),
        "name": _title(props, "Name"),
        "bank": _select(props, "ธนาคาร/บริษัท"),
        "card_network": _select(props, "Card Network"),
        "premium_tier": _select(props, "ความพรีเมียม"),
        "credit_limit": _number(props, "วงเงินที่ได้"),
        "baht_per_point": _number(props, "บาทต่อ 1 คะแนน"),
        "points_per_bill_cycle": _checkbox(props, "ให้คะแนนตามรอบบิล"),
        "outstanding_balance": _formula_number(props, "ยอดค้างชำระ"),
        "points_balance": _rollup_number(props, "คะแนนสะสม"),
        "latest_bill_cycle": _rollup_date(props, "วันตัดรอบบิล"),
        "latest_due_date": _rollup_date(props, "วันครบกำหนดชำระ"),
        "note": _rich_text(props, "Note"),
    }
