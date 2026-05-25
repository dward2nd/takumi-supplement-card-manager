#!/usr/bin/env python3
"""update-promotion — patch an existing promotion file in scripts/repositories/promotions/.

deterministic + idempotent — re-applying the same patch produces the
same file. Loads the existing YAML, merges the spec's `set` patch at the
top level (lists like `tiers` are *replaced*, not concatenated), and
writes it back.

Reads a JSON spec from stdin (or --input <file>):

  {
    "id":   "uob-one-2026",        // required — promotion to patch
    "set":  {                      // required — partial top-level fields to update
      "effective_end": "2026-12-31",
      "status":        "active"
    }
  }

The `set` dict's keys must be recognised top-level promotion fields.
List-valued fields (`tiers`, `foreign_in_thb_policy.overrides`) are
*replaced* whole — if you need to change one tier, send the full list
back. (Composing finer-grained operations on top of this is
straightforward and can be added when the data shape warrants it.)

Writes a JSON envelope:

  {
    "id":          "uob-one-2026",
    "path":        "<absolute>",
    "fields":      ["effective_end", "status"],
    "previous":    { "effective_end": "...", "status": "..." }
  }

--dry-run shows the merged result without writing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import paths, promotions


_ALLOWED_FIELDS = {
    "name", "card", "effective_start", "effective_end", "status",
    "points_default", "foreign_in_thb_policy", "tiers", "installment_rule",
    "crediting_schedule",
    # `id` is intentionally not patchable here — to rename a promo,
    # delete + recreate (the id is the file name).
}


class UpdatePromotionError(RuntimeError):
    pass


def run(spec: dict, *, dry_run: bool = False) -> dict:
    if not isinstance(spec, dict):
        raise UpdatePromotionError("spec must be a JSON object")
    promo_id = spec.get("id")
    if not promo_id or not isinstance(promo_id, str):
        raise UpdatePromotionError("missing required field: 'id'")
    patch = spec.get("set")
    if not isinstance(patch, dict) or not patch:
        raise UpdatePromotionError("'set' must be a non-empty object of field updates")

    unknown = set(patch.keys()) - _ALLOWED_FIELDS
    if unknown:
        raise UpdatePromotionError(
            f"unknown field(s) in `set`: {sorted(unknown)}. "
            f"Allowed: {sorted(_ALLOWED_FIELDS)}"
        )

    path = paths.PROMOTIONS_REPO_DIR / f"{promo_id}.yaml"
    if not path.exists():
        raise UpdatePromotionError(
            f"no promotion file at {path}. Use /add-promotion to create."
        )

    current = promotions.read_yaml(path)
    previous = {k: current.get(k) for k in patch.keys()}

    merged = dict(current)
    for k, v in patch.items():
        merged[k] = v

    # Validate the merged result against the schema before writing.
    try:
        promotions.parse_promotion(merged)
    except Exception as e:
        raise UpdatePromotionError(
            f"merged spec fails schema validation: {e}"
        ) from None

    if dry_run:
        return {
            "id": promo_id,
            "path": str(path),
            "dry_run": True,
            "fields": sorted(patch.keys()),
            "previous": previous,
            "merged": merged,
        }

    promotions.write_yaml(path, merged)
    return {
        "id": promo_id,
        "path": str(path),
        "fields": sorted(patch.keys()),
        "previous": previous,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Resolve the patch without writing")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
