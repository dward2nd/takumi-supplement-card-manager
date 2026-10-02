#!/usr/bin/env python3
"""write-catalogue — write one Promotion Catalogues page: its dates, icon, logo cover and Markdown body.

deterministic + idempotent — the page is created only when no page has the
Name; dates and icon are set only when they differ; the cover is uploaded when
the page has none (or with `replace_cover`); the body is written when the page
is empty (or with `replace_body`). A second run with the same spec writes nothing.

Spec (stdin or --input):
  {
    "page":  "Makro — Oct 2026",                  // exact Name: "<Merchant> — <Mon YYYY>"
    "start": "2026-10-01", "end": "2026-10-31",   // needed to create; corrected when they differ
    "icon":  "🛒",                                 // emoji
    "cover": {                                     // optional
      "logo": "commons:Makro logo.svg",            //   commons:<File> | https://… | local path
      "logo_text": null,                           //   wordmark beside an icon-only logo ("TikTok Shop")
      "period": "ตุลาคม 2569",                      //   default: the Thai month of `start`
      "subtitle": "รวมโปรบัตร · แผนทำยอด",
      "theme": "makro"                             //   a preset (lib.catalogue.cover.PRESETS) or a dict
    },
    "replace_cover": false,
    "cover_out": null,                             // where to save the rendered JPEG (default: a temp dir)
    "body_file": "path/to/page.md",                // Markdown (lib.catalogue.markdown)
    "replace_body": false
  }

Or {"status": "2026-10"}: the Promotion Bureau's usage that month (pooled
spend, credit, cap, what's left), for the page's spending plan.

--dry-run renders the cover and converts the body, and reports what it would write.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.catalogue import cover, markdown, status, store  # noqa: E402

THAI_MONTHS = ("มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
               "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม")


def thai_month(day: dt.date) -> str:
    """`2026-10-01` → `ตุลาคม 2569` (Buddhist year)."""
    return f"{THAI_MONTHS[day.month - 1]} {day.year + 543}"


def run(spec: dict, *, dry_run: bool) -> dict:
    if spec.get("status"):
        return {"month": spec["status"], "bureau": status.usage(spec["status"])}

    name = spec["page"]
    start = dt.date.fromisoformat(spec["start"]) if spec.get("start") else None
    end = dt.date.fromisoformat(spec["end"]) if spec.get("end") else None
    writes: list[str] = []
    page = store.find(name)

    if page is None:
        if not (start and end):
            raise SystemExit(f"no page named {name!r}; pass start and end to create it")
        writes.append(f"create page {name!r} {start}→{end}")
        if not dry_run:
            page = store.create(name, start, end, spec.get("icon"))
    else:
        if start and end and (page.start, page.end) != (start, end):
            writes.append(f"dates {page.start}→{page.end} → {start}→{end}")
            if not dry_run:
                store.set_dates(page.id, start, end)
        if spec.get("icon") and page.icon != spec["icon"]:
            writes.append(f"icon {page.icon} → {spec['icon']}")
            if not dry_run:
                store.set_icon(page.id, spec["icon"])

    out: dict = {}
    if c := spec.get("cover"):
        period = c.get("period") or thai_month(start or page.start)
        logo = cover.load_logo(c["logo"])
        if c.get("logo_text"):
            logo = cover.with_wordmark(logo, c["logo_text"])
        dest = Path(spec.get("cover_out") or Path(tempfile.mkdtemp(prefix="catalogue-")) / "cover.jpg")
        cover.render(logo, period, c.get("subtitle", ""), cover.CoverTheme.of(c.get("theme", "makro")), dest)
        out["cover_file"] = str(dest)
        if page is None or not page.has_cover or spec.get("replace_cover"):
            writes.append(f"{'replace' if page and page.has_cover else 'set'} cover")
            if not dry_run:
                store.set_cover(page.id, dest)

    if spec.get("body_file"):
        blocks = markdown.convert(Path(spec["body_file"]).read_text())
        out["blocks"] = len(blocks)
        existing = store.body_block_ids(page.id) if page else []
        if not existing or spec.get("replace_body"):
            writes.append(f"{'replace' if existing else 'write'} body ({len(blocks)} blocks)")
            if not dry_run:
                store.write_body(page.id, blocks, replace=bool(existing))
        else:
            out["body"] = f"kept: the page already has {len(existing)} blocks (pass replace_body to rewrite)"

    return {"page": {"name": name, "url": page.url if page else None, "id": page.id if page else None},
            **out, "writes": writes, "dry_run": dry_run}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="render and convert, write nothing")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text() if args.input else sys.stdin.read())
    print(json.dumps(run(spec, dry_run=args.dry_run), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
