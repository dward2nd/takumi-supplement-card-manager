---
name: sync-promotion
description: Bring one Promotion Bureau row up to date — screen every holder's linked transactions against the campaign's exclusions, split the bank's credit first come first served, write `เงินคืนรวม` / `เงินคืนส่วน<name>`, upsert each holder's `รายการติดตามเครดิตเงินคืนของ<name>` tracker row linked to it, and write the campaign summary into the Bureau page. Use when the user says "sync NW3", "update the Promotion Bureau for <promo>", "who gets how much of the NW3 cashback?", "create the tracker rows for this promotion", or links more transactions to a Bureau row and wants the split refreshed. Also lays out drift against the bank app's pooled-spend figure.
---

# sync-promotion

One Bureau row ([[../../../docs/databases/promotion-bureau|Promotion Bureau]]) = one promotion period (e.g. `2026M9 — NW3 cb 2%`). This skill keeps everything derived from that row consistent with the transactions linked to it.

## Primary execution path

```sh
echo '{"promotion":"2026M9 — NW3 cb 2%","bank_spend":36803.92}' \
  | uv run --project scripts/python scripts/python/sync-promotion/cli.py --dry-run
```

Always dry-run first and show the user the shares, `flagged`, `unlinked_candidates` and `drift`; then run without `--dry-run`.

| Field | Default | Meaning |
|---|---|---|
| `promotion` | — | Bureau row Name (exact), page ID or URL |
| `bank_spend` | — | The total of the bank app's eligible-transactions list for the promotion (Krungsri-family apps show one; other issuers unknown); adds a `drift` block: per-date totals to read against the app, dates whose total equals the gap, and repeated rows. (A single row equal to the gap is no lead: every even half of a split charge is one.) |
| `link_candidates` | `false` | Link the card's **eligible** unlinked rows in the period. Uncertain/excluded rows are never linked. Only on the user's say-so — linking is their judgment call |
| `replace_summary` | `false` | Rewrite the page body even if it already has content (it's written automatically only when empty) |

## What it does

1. **Resolves the campaign class** from the row's Name + dates (`lib.bureau.promotion_for`). No class → error: a new campaign needs a `BasePromotion` subclass first (see *New campaign* below).
2. **Reads linked rows** per holder from the Transactions side (a page's own relation list is cut off at 25), and checks them against the Bureau's `ยอดจาก<name>` rollups.
3. **Screens** each row with the campaign's `rules` → `flagged` (grouped by reason; `excluded` or `uncertain`). Informational only — links are the household's call. `cashback.if_flagged_rejected` shows the credit if the bank rejected every flagged row.
4. **Splits** the ladder credit **first come, first served** by `Transaction Datetime`; same-date rows share a straddled step pro rata (see [[../../../docs/concepts/promotion-bureau|the concept note]]). `boundary` shows the straddling group.
5. **Writes** `เงินคืนรวม` (only if empty) and each `เงินคืนส่วน<name>`. If `เงินคืนรวม` already holds a *different* figure, nothing downstream is written — a warning explains.
6. **Upserts trackers**: one row per holder with a positive share, titled by `tracker_title` (`NW3 2% 1—30 Sep`), dated the period start, `Card` = the holder's campaign card, `Promotion` = the Bureau row, `Expected Cashback` = the share. A ticked (settled) row is never changed. A same-titled row without a `Promotion` link is reported, not duplicated.
7. **Writes the page summary** (ladder, what counts, exclusions, crediting, split) when the page body is empty.

## Hard rules

- **Never edit transactions to close drift.** Report the gap and the candidate rows; the user fixes data from the statement (reconcile, don't correct).
- **Never alter pre-existing tracker rows** that aren't linked to this Bureau row.
- **Month still open → numbers are provisional.** Re-run after new rows are linked; `Expected Cashback` follows.

## New campaign

Subclass `BasePromotion` in `scripts/python/lib/bureau/<code>.py` — `code`, `card`, `campaign`, `tranches()`, `rules`, `ladder_rows`, `examples` (the bank's worked examples; the summary refuses to render if `tranches` disagrees), `inclusions`, `crediting` — and add it to `PROMOTIONS` in `lib/bureau/__init__.py`. Override `allocate`, `tracker_title` or `summary_blocks` only when the bank's shape needs it. Document the campaign in `docs/promotions/<id>.md`.
