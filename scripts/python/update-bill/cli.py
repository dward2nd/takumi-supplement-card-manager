#!/usr/bin/env python3
"""update-bill — patch a Bills row on Baiboon's or Nuta's Bills DB.

deterministic + idempotent — re-running the same spec re-applies the
same property writes. Appends are append-only (existing files in the
target property are preserved by re-uploading them; see
`lib.notion_files.append_files_to_page`).

Reads a JSON spec from stdin (or --input <file>):

  {
    "holder":        "baiboon" | "nuta",
    "card":          "First Choice",          // SELECT option, verbatim
    "bill_cycle":    "2026-06-05",            // ISO date (วันตัดรอบบิล)
    "id":            "<page-uuid>",           // alternative to (holder,card,bill_cycle)

    "paid":          true,                    // sets จ่ายแล้ว
    "note":          "...",                   // sets Note
    "slip":          "/abs/path.jpg",         // appends one file to หลักฐานการชำระ
    "slips":         ["/abs/a.jpg", ...],     // appends many
    "statement_pdf": "/abs/path.pdf",         // appends one to ใบแจ้งยอด (PDF)
    "statement_pdfs":["/abs/a.pdf", ...],     // appends many
    "finalize":      true,                    // strips a leading `[DRAFT] ` from the
                                              //   title (no-op if already finalized)
    "properties":    { "<raw notion prop>": ... }   // escape hatch (replace semantics)
  }

Resolution rules:
- If `id` is given, it wins; the holder/card/bill_cycle keys are then
  optional (only used for the response echo).
- Otherwise `holder`, `card`, `bill_cycle` are all required.
- Slip/statement appends preserve existing entries in the target
  property (re-uploaded from their signed URLs). Takumi has no Bills DB.

Output:
  {
    "id":          "<bill-page-id>",
    "holder":      "baiboon",
    "card":        "First Choice",
    "bill_cycle":  "2026-06-05",
    "fields":      ["จ่ายแล้ว", "หลักฐานการชำระ", ...]
  }

--dry-run prints the resolved bill ID and the actions it *would* take
without writing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import notion_client, notion_files
from lib.bills import find_bill
from lib.holders import resolve_holder


_SLIP_PROP = "หลักฐานการชำระ"
_STATEMENT_PROP = "ใบแจ้งยอด (PDF)"
_DRAFT_PREFIX = "[DRAFT] "


def _current_title(page_id: str) -> str:
    page = notion_client.get_page(page_id)
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    return ""


def _resolve_bill(spec: dict) -> tuple[str, str | None, str | None, str | None]:
    """Return (page_id, holder_key, card, bill_cycle) — echo fields may be None."""
    if (page_id := spec.get("id")):
        return page_id, spec.get("holder"), spec.get("card"), spec.get("bill_cycle")

    for key in ("holder", "card", "bill_cycle"):
        if not spec.get(key):
            raise ValueError(
                f"missing {key!r}: either pass id, or pass all of holder+card+bill_cycle"
            )
    holder = resolve_holder(spec["holder"])
    bill = find_bill(holder, spec["card"], spec["bill_cycle"])
    return bill["id"], holder.key, spec["card"], spec["bill_cycle"]


def _collect_files(spec: dict, single_key: str, plural_key: str) -> list[str]:
    out: list[str] = []
    if (v := spec.get(single_key)) is not None:
        if not isinstance(v, str):
            raise ValueError(f"{single_key!r} must be a path string; got {type(v).__name__}")
        out.append(v)
    if (v := spec.get(plural_key)) is not None:
        if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
            raise ValueError(f"{plural_key!r} must be a list of path strings")
        out.extend(v)
    return out


def run(spec: dict, *, dry_run: bool = False) -> dict:
    if not isinstance(spec, dict):
        raise ValueError("spec must be a JSON object")

    page_id, holder_key, card, bill_cycle = _resolve_bill(spec)

    actions: list[str] = []
    simple_props: dict = {}

    if (paid := spec.get("paid")) is not None:
        if not isinstance(paid, bool):
            raise ValueError(f"paid must be a boolean; got {type(paid).__name__}")
        simple_props["จ่ายแล้ว"] = {"checkbox": paid}
        actions.append("จ่ายแล้ว")

    if (note := spec.get("note")) is not None:
        if not isinstance(note, str):
            raise ValueError(f"note must be a string; got {type(note).__name__}")
        simple_props["Note"] = {"rich_text": [{"text": {"content": note}}]}
        actions.append("Note")

    if (raw := spec.get("properties")) is not None:
        if not isinstance(raw, dict):
            raise ValueError("properties escape-hatch must be an object")
        simple_props.update(raw)
        actions.extend(k for k in raw if k not in actions)

    finalize = spec.get("finalize")
    if finalize is not None and not isinstance(finalize, bool):
        raise ValueError(f"finalize must be a boolean; got {type(finalize).__name__}")
    finalized_title: str | None = None
    if finalize:
        current = _current_title(page_id)
        if current.startswith(_DRAFT_PREFIX):
            finalized_title = current[len(_DRAFT_PREFIX):]
            simple_props["title"] = {"title": [{"text": {"content": finalized_title}}]}
            actions.append("title (finalized)")
        else:
            # Idempotent: if the prefix is already gone, finalize is a no-op
            # rather than an error. Surfaces in the response so caller can see.
            actions.append("title (already finalized)")

    slips = _collect_files(spec, "slip", "slips")
    statements = _collect_files(spec, "statement_pdf", "statement_pdfs")

    if not (simple_props or slips or statements):
        raise ValueError("nothing to do: spec must include at least one update field")

    if dry_run:
        return {
            "id": page_id,
            "holder": holder_key,
            "card": card,
            "bill_cycle": bill_cycle,
            "dry_run": True,
            "would_set": sorted(simple_props.keys()),
            "would_append_slips": slips,
            "would_append_statements": statements,
        }

    if simple_props:
        notion_client.update_page_properties(page_id, simple_props)

    if slips:
        notion_files.append_files_to_page(page_id, _SLIP_PROP, slips)
        actions.append(_SLIP_PROP)

    if statements:
        notion_files.append_files_to_page(page_id, _STATEMENT_PROP, statements)
        actions.append(_STATEMENT_PROP)

    return {
        "id": page_id,
        "holder": holder_key,
        "card": card,
        "bill_cycle": bill_cycle,
        "fields": actions,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Resolve without writing")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
