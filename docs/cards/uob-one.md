---
tags: [card, uob, points-0x, cashback]
issuer: UOB
holders: [takumi, baiboon, nuta]
points: none
---

# UOB One

UOB's flagship cashback card. Takumi holds the primary; Baiboon and Nuta each carry a supplement card on the same account.

## Points

**This card earns no Notion-tracked points.** Every transaction written on a UOB One row gets the `×0` multiplier checked. This is a card-level rule, not promo-driven.

The card's "rewards" exist purely as cashback — there is no underlying points balance to redeem, so the `คะแนนที่ได้จริง` / `คะแนน unrealized` formulas always evaluate to zero on these rows. See [[../concepts/points-and-multipliers]].

## Cashback

Cashback comes from the **active promotion**, not from a permanent card policy. See [[../concepts/promotions]] for the general model.

**Currently active**: [[../promotions/uob-one-2026]] (effective `2026-01-01` → `2026-12-31`; extended from 2025 with identical terms).

The tier table, carve-outs, exclusions, installment rule, and cashback-crediting workflow all live in the promotion note. When the issuer renews for 2027, branch a new promotion note rather than mutating the existing one.

The `% cb` field is on Baiboon's and Nuta's Transactions DSes (added 2026-05-25 — see [[../databases/baiboon-transactions]] / [[../databases/nuta-transactions]]). Takumi's DS has no `% cb`; for Takumi UOB One transactions, the cashback tier is recorded in `Note` for now.

## Writing UOB One transactions

Always go through the [[../../.claude/skills/add-transaction/SKILL|/add-transaction]] skill. The relevant fields:

- `multiplier: "×0"` — at batch level for the whole UOB One batch.
- `cashback_percent: <fraction>` — per-tx for Baiboon and Nuta (Takumi omits it). Raw fractions; `0.05` for 5%.
- `Note` — only on rows where the cashback departs from the active promotion's headline rate for a reason (excluded merchant, installment treatment, etc.).

Then run [[../../.claude/skills/post-cashback-credits/SKILL|/post-cashback-credits]] at cycle close to write the three tier-split credit rows, and finally [[../../.claude/skills/prepare-bill/SKILL|/prepare-bill]] to draft the bill.

## Open questions

- Does Takumi actually hold a UOB One primary? `_stubs.md` lists `?` for Takumi — should be confirmed once Takumi's Cards DB is enumerated.
- Monthly cashback cap (account-level or card-level?) — not yet surfaced from the issuer T&Cs.

## Phase 2 model

In the new app ([[../future-app/product-shape]]):

- The active promotion's tier table seeds the card's **auto-classifier rules**. When a transaction is added on UOB One, the app matches the merchant string against the tier patterns and pre-fills the cashback `RewardRule` (e.g. `{type: "cashback", percent: 5}` for a `7-11` charge that isn't `TMN 7-11`).
- The user can **override per row** when the auto-classification is wrong — the override stays as the row's reward rule; no fight with the engine.
- The carve-outs (TMN 7-11, GRAB cross-border, foreign-in-THB, petrol stations) are encoded as **exclusion patterns** that force the row to `{type: "cashback", percent: 0}` with the explanation auto-filled into `Note`.
- Cashback is **universal** in phase 2 — Takumi's UOB One transactions also carry the `{type: "cashback", percent: N}` rule (Baiboon and Nuta already track `% cb` per row in Notion as of 2026-05-25; phase 2 closes the gap for Takumi).
- The monthly cashback cap (one of the open questions above) becomes a **`PrimaryAccount`-level shared quota** if account-wide, or a **`Card`-level quota** if per-card — see [[../concepts/cashback]] and [[../future-app/data-model-target]].
- Promotions in phase 2 become first-class entities (effective dates, tier rules, exclusions), and the auto-classifier reads the currently-active promo per card per transaction date.

## See also

- [[_stubs|Card stub index]]
- [[../promotions/uob-one-2026]] — the active promotion's full terms.
- [[../concepts/promotions]] — the cross-cutting promotion concept.
- [[../databases/nuta-transactions]] for the `% cb` / `cashback` schema (Notion-as-built).
- [[../concepts/points-and-multipliers]] for how `×0` interacts with `คะแนนที่ได้จริง`.
- [[../future-app/product-shape]] for the phase-2 auto-classifier this tier table feeds into.
