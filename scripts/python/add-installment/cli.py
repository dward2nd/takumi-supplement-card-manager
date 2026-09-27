#!/usr/bin/env python3
"""add-installment — write the first term (01/NN) of a new installment plan.

deterministic + idempotent — re-running creates a new page; the script
does not upsert on merchant name. (Bank statements key on the page row,
not on the plan as a whole; duplicates are caught at reconciliation
time.)

Usage:

  echo '<JSON-spec>' | uv run scripts/python/add-installment/cli.py

JSON spec:

  {
    "holder":       "baiboon" | "nuta" | "takumi",   // required
    "card":         "UOB One",                        // required, exact title match
    "merchant":     "2C2P *SHOPEE",                   // required; base name WITHOUT
                                                      //   the `NN/NN` suffix — the CLI
                                                      //   appends it as `01/<total>`
    "term_amount":  449.10,                           // required; baht per term
    "total_terms":  10,                               // required; ≥ 1
    "bill_cycle":   "2026-05-25",                     // optional; default = the most
                                                      //   recently closed cycle for the
                                                      //   card (see lib/bill_cycle.py).
                                                      //   `due_date` is auto-derived
                                                      //   from the same cycle.
    "auto_classify": true,                            // optional, default true; the active
                                                      //   promotion's `installment_rule`
                                                      //   sets `% cb` + multiplier
    "campaign":     "dee-jang",                       // optional; id from
                                                      //   scripts/repositories/installment-campaigns/.
                                                      //   Declares the plan was converted under a
                                                      //   bank campaign whose reward treatment
                                                      //   (e.g. no points) applies to every term.
                                                      //   Nothing in the merchant string reveals
                                                      //   this, so it must be declared here — and
                                                      //   /populate-installment then inherits it
                                                      //   from the note this writes.
    "multiplier":   "×0",                             // optional override
    "cashback_percent": 0.01,                         // optional override (raw fraction)
    "note":         "..."                             // optional; if omitted and
                                                      //   auto_classify hits the
                                                      //   installment rule, a default
                                                      //   note is written
  }

Output:

  {
    "holder":        "nuta",
    "card":          "UOB One",
    "card_page_id":  "<uuid>",
    "bill_cycle":    "2026-05-25",
    "due_date":      "2026-06-15",
    "merchant_base": "2C2P *SHOPEE",
    "total_terms":   10,
    "name":          "2C2P *SHOPEE 01/10",
    "term_amount":   449.10,
    "created": { "id": "...", "url": "...", "name": "...", "amount": 449.10, "date": "2026-05-25" },
    "classification": { ... }    // when auto_classify == true
  }

Hard rules (mirrored from add-transaction):
  1. Merchant base is written verbatim — no trimming or normalization;
     the `NN/NN` suffix is appended by this script.
  2. Holder routes to the correct transactions DS; never cross-write.
  3. Card relation must resolve to exactly one card; otherwise abort.
  4. `Processed` defaults to true.
  5. Transaction date == bill_cycle_date (banks post installment terms on
     the BC date).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import card_repo, installment_campaigns, installments, notion_client, promotions
from lib.bill_cycle import most_recent_closed_cycle, pattern_for_card, cycle_for_month
from lib.cards import find_card
from lib.holders import resolve_holder
from lib.transaction_write import VALID_MULTIPLIERS, build_transaction_properties


_REQUIRED = ("holder", "card", "merchant", "term_amount", "total_terms")


class SpecError(ValueError):
    pass


def _validate(spec: dict) -> None:
    if not isinstance(spec, dict):
        raise SpecError("spec must be a JSON object")
    missing = [k for k in _REQUIRED if k not in spec]
    if missing:
        raise SpecError(f"missing required fields: {missing}")
    if not isinstance(spec["merchant"], str) or not spec["merchant"].strip():
        raise SpecError("merchant must be a non-empty string (the base name without NN/NN)")
    if installments.parse(spec["merchant"]) is not None:
        raise SpecError(
            f"merchant {spec['merchant']!r} already carries an NN/NN suffix — "
            "pass the BASE name; the script appends 01/<total>"
        )
    if not isinstance(spec["term_amount"], (int, float)) or isinstance(spec["term_amount"], bool):
        raise SpecError("term_amount must be a number")
    if spec["term_amount"] <= 0:
        raise SpecError("term_amount must be positive")
    if not isinstance(spec["total_terms"], int) or isinstance(spec["total_terms"], bool):
        raise SpecError("total_terms must be an integer")
    if spec["total_terms"] < 1:
        raise SpecError("total_terms must be ≥ 1")
    if "bill_cycle" in spec and spec["bill_cycle"] is not None:
        try:
            _dt.date.fromisoformat(spec["bill_cycle"])
        except ValueError as e:
            raise SpecError(f"bill_cycle is not a valid ISO date: {e}") from None
    if (m := spec.get("multiplier")) is not None and m not in VALID_MULTIPLIERS:
        raise SpecError(
            f"multiplier must be one of {sorted(VALID_MULTIPLIERS)} or null; got {m!r}"
        )
    if (camp := spec.get("campaign")) is not None:
        if not isinstance(camp, str) or not camp.strip():
            raise SpecError("campaign must be a non-empty campaign id string")
        # Raises InstallmentCampaignNotFoundError (listing known ids) on a typo,
        # rather than silently writing a plan with no campaign treatment.
        installment_campaigns.by_id(camp)
    if (cb := spec.get("cashback_percent")) is not None:
        if not isinstance(cb, (int, float)) or isinstance(cb, bool):
            raise SpecError("cashback_percent must be a number (raw fraction)")
        if not (0 <= cb <= 1):
            raise SpecError("cashback_percent must be in [0, 1] — 0.05 == 5%")
        if spec["holder"] == "takumi":
            raise SpecError("cashback_percent does not exist on Takumi's Transactions DS")


def _resolve_cycle(card_name: str, spec_bc: str | None) -> tuple[str, str]:
    """Return (bill_cycle, due_date) as ISO strings.

    If the spec provides `bill_cycle`, derive `due_date` from the bank's
    pattern for that month so the pair stays consistent. Otherwise default
    to the most-recently-closed cycle (banks post installment terms on
    the cycle that just closed).
    """
    if spec_bc:
        # Find the cycle whose BC matches spec_bc on the card's pattern.
        bc = _dt.date.fromisoformat(spec_bc)
        pattern = pattern_for_card(card_name)
        cand_bc, cand_dd = cycle_for_month(pattern, bc.year, bc.month)
        if cand_bc != bc:
            # User passed a non-pattern date (e.g. weekend). Honour it
            # verbatim for the BC and compute DD from the nominal rule.
            cand_dd = pattern.due_date_shift(pattern.due_from_nominal_bc(bc))
            cand_bc = bc
        return cand_bc.isoformat(), cand_dd.isoformat()
    bc, dd = most_recent_closed_cycle(card_name, _dt.date.today())
    return bc.isoformat(), dd.isoformat()


def run(spec: dict, *, dry_run: bool = False) -> dict:
    _validate(spec)
    holder = resolve_holder(spec["holder"])
    card_name = spec["card"]
    card = find_card(holder.cards_ds, card_name)
    card_page_id = card["id"]

    bill_cycle, due_date = _resolve_cycle(card_name, spec.get("bill_cycle"))
    total_terms = int(spec["total_terms"])
    base = spec["merchant"]
    name = installments.format_name(base, term=1, total=total_terms)
    amount = float(spec["term_amount"])

    auto_classify = bool(spec.get("auto_classify", True))

    multiplier = spec.get("multiplier")
    cashback_percent = spec.get("cashback_percent")
    note = spec.get("note")
    classification_info: dict | None = None

    if auto_classify:
        cls = promotions.classify(
            card_name, _dt.date.fromisoformat(bill_cycle), name,
            is_installment_override=True,
        )
        classification_info = {
            "promotion_id": cls.promotion_id,
            "reason": cls.reason,
            "cashback_percent": cls.cashback_percent,
            "points_override": cls.points_override,
        }
        if cashback_percent is None:
            cashback_percent = cls.cashback_percent
        if multiplier is None:
            multiplier = cls.points_override
        if note is None and cls.note:
            note = cls.note

    # Plan-level campaign (e.g. CardX ดีจังผ่อน 0%). Applied after
    # auto_classify because the campaign is the more specific fact, and
    # points-only: `% cb` is left exactly as the card's policy set it.
    # An explicit per-spec `multiplier` / `note` still wins over both.
    campaign = installment_campaigns.by_id(spec["campaign"]) if spec.get("campaign") else None
    campaign_hint: list[str] = []
    if campaign is not None:
        if spec.get("multiplier") is None and campaign.points_default:
            multiplier = campaign.points_default
        if spec.get("note") is None and campaign.note:
            note = campaign.note
    else:
        card_entry = card_repo.get(card_name)
        campaign_hint = installment_campaigns.hint_for_plan(
            issuer=card_entry.issuer if card_entry else None,
            total_terms=total_terms,
        )

    props = build_transaction_properties(
        name=name,
        amount=amount,
        transaction_date=bill_cycle,  # term posts on the BC date
        bill_cycle_date=bill_cycle,
        due_date=due_date,
        card_page_id=card_page_id,
        processed=bool(spec.get("processed", True)),
        note=note,
        multiplier=multiplier,
        cashback_percent=cashback_percent,
    )

    envelope: dict = {
        "holder": holder.key,
        "card": card_name,
        "card_page_id": card_page_id,
        "bill_cycle": bill_cycle,
        "due_date": due_date,
        "merchant_base": base,
        "total_terms": total_terms,
        "name": name,
        "term_amount": amount,
    }
    if classification_info is not None:
        envelope["classification"] = classification_info
    if campaign is not None:
        envelope["campaign"] = campaign.id
    if campaign_hint:
        envelope["campaign_hint"] = campaign_hint

    if dry_run:
        envelope["dry_run"] = True
        envelope["properties"] = props
        return envelope

    page = notion_client.create_page(holder.transactions_ds, props)
    envelope["created"] = {
        "id": page["id"],
        "url": page.get("url"),
        "name": name,
        "amount": amount,
        "date": bill_cycle,
    }
    return envelope


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", "-i", type=Path, help="JSON spec file (default: stdin)")
    ap.add_argument("--dry-run", action="store_true", help="Build payload without calling Notion")
    args = ap.parse_args(argv)

    raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    spec = json.loads(raw)

    out = run(spec, dry_run=args.dry_run)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
