#!/usr/bin/env python3
"""add-promotion — declare a new promotion in scripts/repositories/promotions/.

deterministic + idempotent — re-running with the same spec refuses to
overwrite an existing file (unique by `id`). Use /update-promotion to
modify.

Reads a JSON spec from stdin (or --input <file>). Spec mirrors the
promotion schema in scripts/repositories/README.md.

Minimal spec:

  {
    "id":              "first-choice-2026-q3",          // required, kebab-case
    "name":            "First Choice Q3 2026 promo",    // required
    "card":            "First Choice",                  // required; must exist in cards/
    "effective_start": "2026-07-01",                    // required, ISO date
    "effective_end":   "2026-09-30",                    // optional; null = open-ended
    "status":          "active",                         // active | superseded | expired
    "tiers": [
      { "rate": 0.02, "label": "base", "patterns": ["*"] }
    ]
  }

Optional fields:
  - points_default        "×0" or null (rarely useful at promo level — usually card-level)
  - foreign_in_thb_policy { default: "exclude"|"apply", overrides: [...] }
  - installment_rule      { rate, credited: "per_installment"|"at_purchase" }
  - crediting_schedule    { "0.01": "bc_date", "0.05": "first_weekday_next_month", ... }

Writes the YAML file and prints a JSON envelope to stdout:

  { "id": "...", "path": "<absolute>", "status": "created" }

--dry-run validates + serializes without touching disk.
--force allows overwriting an existing file (otherwise refuses).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import card_repo, paths, promotions


class AddPromotionError(RuntimeError):
    pass


_ALLOWED_TOP_LEVEL = {
    "id", "name", "card", "effective_start", "effective_end", "status",
    "points_default", "foreign_in_thb_policy", "tiers", "installment_rule",
    "crediting_schedule",
}


def _validate(spec: dict) -> None:
    if not isinstance(spec, dict):
        raise AddPromotionError("spec must be a JSON object")

    extras = set(spec.keys()) - _ALLOWED_TOP_LEVEL
    if extras:
        raise AddPromotionError(
            f"unknown top-level fields: {sorted(extras)}. "
            f"Allowed: {sorted(_ALLOWED_TOP_LEVEL)}"
        )

    for k in ("id", "name", "card", "effective_start", "status"):
        if not spec.get(k):
            raise AddPromotionError(f"missing required field: {k!r}")

    pid = spec["id"]
    if not isinstance(pid, str) or "/" in pid or pid.startswith("_") or " " in pid:
        raise AddPromotionError(
            f"id={pid!r} must be a kebab-case slug (no spaces, no slashes, no leading underscore)"
        )

    # Card must exist in the cards repo so promo→card joins resolve later.
    if card_repo.get(spec["card"]) is None:
        raise AddPromotionError(
            f"card={spec['card']!r} is not registered in scripts/repositories/cards/. "
            f"Add the card YAML first."
        )

    # Parse via the lib to catch schema errors (date formats, foreign policy
    # default values, tier rate types, etc.).
    promotions.parse_promotion(spec)


def _file_path_for(promo_id: str) -> Path:
    return paths.PROMOTIONS_REPO_DIR / f"{promo_id}.yaml"


def run(spec: dict, *, dry_run: bool = False, force: bool = False) -> dict:
    _validate(spec)

    promo_id = spec["id"]
    target = _file_path_for(promo_id)

    if target.exists() and not force:
        raise AddPromotionError(
            f"a promotion file already exists at {target}. "
            f"Pass --force to overwrite, or use /update-promotion to patch."
        )

    if dry_run:
        return {
            "id": promo_id,
            "path": str(target),
            "status": "would-write" if not target.exists() else "would-overwrite",
            "dry_run": True,
        }

    paths.PROMOTIONS_REPO_DIR.mkdir(parents=True, exist_ok=True)
    # Pin a stable top-level key ordering for readability.
    ordered: dict = {}
    for k in (
        "id", "name", "card", "effective_start", "effective_end", "status",
        "points_default", "foreign_in_thb_policy", "tiers", "installment_rule",
        "crediting_schedule",
    ):
        if k in spec:
            ordered[k] = spec[k]
    promotions.write_yaml(target, ordered)

    return {
        "id": promo_id,
        "path": str(target),
        "status": "overwritten" if target.exists() and force else "created",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Validate without writing")
    ap.add_argument("--force", action="store_true", help="Overwrite an existing promotion file")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec, dry_run=args.dry_run, force=args.force)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
