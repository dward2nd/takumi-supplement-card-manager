---
tags: [card, ttb, cashback]
issuer: ttb
holders: [baiboon]
points: none
---

# ttb so smart

ttb's flat-rate cashback card. It is a **cashback card, not a points card** — it earns **no reward points at all**, so every transaction row is `×0`. Its earning is a flat **1% cashback** on eligible spend (per user, 2026-07-21).

## Earning rules

| Where | Cashback | Points |
|---|---|---|
| General eligible spend | **1%** (`% cb` = `0.01`) | none — `×0` |
| TrueMoney (`TMN*…`) | **excluded** — no cashback | `×0` |
| 7-11 (`…7-11…`) | **excluded** — no cashback | `×0` |
| Petrol stations (`PTT`/`BCP`/`BANGCHAK`/`ESSO`/`SHELL`/`CALTEX`) | **excluded** — no cashback | `×0` |
| Installment rows (`NN/NN`) | **excluded** — no cashback | `×0` |
| Foreign merchant billed in THB | **excluded** (general rule) | `×0` |

- **Cap**: the 1% is capped per cycle, but the household spends little on this card, so **the cap is intentionally not tracked** (per user, 2026-07-21). If usage grows, revisit — the cap would need block/cap math the current tier model can't express (cf. [[krungsri-now|Krungsri NOW]]).
- Zero-cashback rows leave `% cb` **unset** (never an explicit `0`), per project convention.

## Notion / classification encoding

The policy is machine-applied by `lib.promotions.classify`, split across two repository files:

- **`scripts/repositories/cards/ttb-so-smart.yaml`** — `points_default: "×0"` (no points, canonical) and `petrol_exclusion: true` (gas-station carve-out). `bill_cycle_pattern: ttb`.
- **`scripts/repositories/promotions/ttb-so-smart-cashback.yaml`** — the 1% base tier (`patterns: ["*"]`, `exclude_patterns: ["TMN", "7-11"]`) and `installment_rule: { rate: 0.0 }` to zero installment rows. Modeled as an open-ended, ongoing card-level policy (`effective_start: 2026-01-01`, no `effective_end`).

So `/add-transaction` with `auto_classify: true` fills `% cb`, the `×0` multiplier, and the exclusion Note automatically. Verified across mall / TMN / 7-11 / petrol / installment / foreign cases on 2026-07-21.

## Crediting mechanism — external savings account

ttb pays this cashback **directly into a linked savings account** (per user, 2026-07-21). It is **not** credited to the credit-card statement, so **no cashback credit row is ever posted on the card** — do not run `/post-cashback-credits` for ttb so smart, and the promo intentionally declares **no `crediting_schedule`**.

The `% cb` field on each row is therefore purely **informational**: it records how much cashback the purchase earned (paid out externally), and the read-only `cashback` formula (`% cb` × `ยอดชำระ`) reports the baht amount. Neither offsets the card's outstanding balance — that balance is the running sum of `ยอดชำระ` only.

## See also

- [[_stubs|Card stub index]]
- [[../concepts/promotions]] — the promotion-driven cashback model.
- Memory: `project_card_ttb_so_smart`.
