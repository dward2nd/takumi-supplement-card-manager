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
    "record_payment": true,                   // default true. When a slip is attached,
                                              //   record the matching negative-amount
                                              //   payment row (full bill ยอดชำระ) in the
                                              //   Transactions DB via lib.payments. Dedups,
                                              //   so it's a no-op if a payment already
                                              //   exists. Set false to skip. Partial /
                                              //   advance payments → use /record-payment.
    "payment_date":  "2026-05-29",            // optional slip date for the payment row
                                              //   (default today). Only used with a slip.
    "finalize":      true,                    // strips a leading `[DRAFT] ` from the
                                              //   title (no-op if already finalized)
    "refresh_from_transactions": true,        // recompute ยอดชำระ from cycle's
                                              //   transactions; if no explicit `note`
                                              //   was supplied, also regenerate the
                                              //   Note explaining special rows
                                              //   (cashback, installments, manual
                                              //   adjustments). Requires (holder, card,
                                              //   bill_cycle) to be resolvable.
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

from lib import installments, notion_client, notion_files, payments
from lib.bills import explain_cycle, find_bill
from lib.cards import CardNotFoundError, find_card
from lib.holders import HOLDERS, resolve_holder
from lib.transaction_read import project_transaction


_SLIP_PROP = "หลักฐานการชำระ"
_STATEMENT_PROP = "ใบแจ้งยอด (PDF)"
_DRAFT_PREFIX = "[DRAFT] "


def _current_title(page_id: str) -> str:
    page = notion_client.get_page(page_id)
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    return ""


def _bill_amount(page_id: str) -> float | None:
    """Read `ยอดชำระ` off the Bills page (None if unset / draft-without-sum)."""
    page = notion_client.get_page(page_id)
    return (page.get("properties", {}).get("ยอดชำระ", {}) or {}).get("number")


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


def _in_progress_for(holder_key: str | None, card_name: str | None) -> list[dict] | None:
    """Return in-progress installment plans on the bill's card, if resolvable.

    Read-only — does not write. When the bill was resolved by `id` alone
    (no holder/card echo), we can't look up the Cards DS, so we just
    return None and let the caller skip the section.
    """
    if not holder_key or not card_name:
        return None
    holder = HOLDERS.get(holder_key.strip().lower())
    if holder is None:
        return None
    try:
        card = find_card(holder.cards_ds, card_name)
    except CardNotFoundError:
        return None
    return installments.in_progress_summary(holder.transactions_ds, card["id"])


def _refresh_from_transactions(
    holder_key: str, card_name: str, bill_cycle: str
) -> tuple[float, int, str | None] | None:
    """Recompute (total, tx_count, auto_note) from the cycle's transactions.

    Returns None when the (holder, card, bill_cycle) trio can't resolve a
    card page (e.g. user passed only `id`). Otherwise scans every row on
    that (Card relation, Bill Cycle Date) and returns the recomputed sum,
    the row count, and the explanation Note (or None if nothing special).
    """
    holder = HOLDERS.get((holder_key or "").strip().lower())
    if holder is None:
        return None
    try:
        card = find_card(holder.cards_ds, card_name)
    except CardNotFoundError:
        return None

    raw_rows = notion_client.query_all(
        holder.transactions_ds,
        filter={
            "and": [
                {"property": "Card", "relation": {"contains": card["id"]}},
                {"property": "Bill Cycle Date", "date": {"equals": bill_cycle}},
            ]
        },
    )
    projected = [project_transaction(r) for r in raw_rows]
    total = round(sum(float(r.get("amount") or 0.0) for r in projected), 2)
    note = explain_cycle(projected)
    return total, len(projected), note


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

    # `refresh_from_transactions` recomputes the bill's `ยอดชำระ` from every
    # transaction in the cycle, and (unless the spec also passes an explicit
    # `note`) regenerates the explanation Note. Use this after adding /
    # populating installment rows in the cycle so the bill total stays in
    # sync with what the user will see on the bank statement.
    refresh = bool(spec.get("refresh_from_transactions"))
    refreshed: dict | None = None
    if refresh:
        if not (holder_key and card and bill_cycle):
            raise ValueError(
                "refresh_from_transactions requires the bill to be resolvable "
                "by (holder, card, bill_cycle); pass those alongside `id` if "
                "you used the id form"
            )
        rf = _refresh_from_transactions(holder_key, card, bill_cycle)
        if rf is None:
            raise ValueError(
                f"refresh_from_transactions: could not resolve "
                f"holder={holder_key!r}/card={card!r}/cycle={bill_cycle!r}"
            )
        total, tx_count, auto_note = rf
        simple_props["ยอดชำระ"] = {"number": total}
        actions.append("ยอดชำระ (refreshed)")
        # Auto-generated Note loses to a user-supplied `note` — that's already
        # in simple_props from the earlier branch; only fill in when blank.
        if auto_note and "Note" not in simple_props:
            simple_props["Note"] = {"rich_text": [{"text": {"content": auto_note}}]}
            actions.append("Note (auto)")
        refreshed = {"ยอดชำระ": total, "tx_count": tx_count, "auto_note": auto_note}

    slips = _collect_files(spec, "slip", "slips")
    statements = _collect_files(spec, "statement_pdf", "statement_pdfs")

    if not (simple_props or slips or statements):
        raise ValueError("nothing to do: spec must include at least one update field")

    in_progress = _in_progress_for(holder_key, card)

    # Slip-upload delegation → lib.payments. A payment slip implies the bill
    # was paid, so (unless `record_payment: false`) record the matching
    # negative-amount payment row in the Transactions DB for the *full* bill
    # `ยอดชำระ`. This is independent of the `จ่ายแล้ว` flag: the checkbox
    # records *that* it's settled; the negative row offsets the card's
    # running balance so the cycle nets to zero. lib.payments dedups, so it's
    # a no-op when a matching payment already exists. Only fires when the bill
    # is resolvable by (holder, card, bill_cycle) and at least one slip is
    # being attached. Partial / advance payments go through /record-payment.
    def _maybe_record_payment(dry: bool) -> dict | None:
        if not (slips and spec.get("record_payment", True)):
            return None
        if not (holder_key and card and bill_cycle):
            return None
        amount = _bill_amount(page_id)
        if amount is None:
            return {
                "would_create": False,
                "created": False,
                "reason": "bill has no ยอดชำระ yet — record manually via /record-payment",
            }
        try:
            return payments.record_payment(
                holder_key,
                card,
                bill_cycle,
                amount=float(amount),
                payment_date=spec.get("payment_date"),
                kind="full",
                dry_run=dry,
            )
        except CardNotFoundError as e:
            # The bill's `Card` SELECT resolved (find_bill matched), but the
            # same string doesn't match a Cards-DB title — usually an
            # apostrophe-style divergence (SELECT `Lotus's…` vs title
            # `Lotus's…`). Don't crash the whole update after the slip is
            # already attached: skip the payment and tell the caller to use
            # /record-payment with the exact Cards-DB title.
            return {
                "would_create": False,
                "created": False,
                "reason": (
                    f"could not resolve card {card!r} in the Cards DB (likely a "
                    f"Card-SELECT vs Cards-title divergence, e.g. apostrophe style) — "
                    f"slip attached; record the payment via /record-payment with the "
                    f"exact card title. ({e})"
                ),
            }

    if dry_run:
        out = {
            "id": page_id,
            "holder": holder_key,
            "card": card,
            "bill_cycle": bill_cycle,
            "dry_run": True,
            "would_set": sorted(simple_props.keys()),
            "would_append_slips": slips,
            "would_append_statements": statements,
        }
        if in_progress is not None:
            out["in_progress_installments"] = in_progress
        if refreshed is not None:
            out["refreshed"] = refreshed
        payment = _maybe_record_payment(True)
        if payment is not None:
            out["payment"] = payment
        return out

    if simple_props:
        notion_client.update_page_properties(page_id, simple_props)

    if slips:
        notion_files.append_files_to_page(page_id, _SLIP_PROP, slips)
        actions.append(_SLIP_PROP)

    if statements:
        notion_files.append_files_to_page(page_id, _STATEMENT_PROP, statements)
        actions.append(_STATEMENT_PROP)

    # Record the payment row after the slip is attached (evidence first).
    payment = _maybe_record_payment(False)
    if payment is not None and payment.get("created"):
        actions.append("payment recorded")

    out = {
        "id": page_id,
        "holder": holder_key,
        "card": card,
        "bill_cycle": bill_cycle,
        "fields": actions,
    }
    if in_progress is not None:
        out["in_progress_installments"] = in_progress
    if refreshed is not None:
        out["refreshed"] = refreshed
    if payment is not None:
        out["payment"] = payment
    return out


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
