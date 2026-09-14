---
tags: [concept, technical-debt]
---

# Known divergences in the Notion schema

Inconsistencies between the three card universes (Takumi / Baiboon / Nuta) and between databases within a universe. None are bugs — most are deliberate or historical — but all are worth knowing.

## 1. Bills' `Card` is a SELECT, not a relation

The single biggest divergence. In all three Transactions databases, `Card` is a **relation** to the corresponding Cards DB. In both Bills databases (Baiboon, Nuta), `Card` is a **`select`** with a hardcoded option list.

Consequences:

- No two-way navigation from a Bill row to the related Card row.
- No rollup from Bills back to Cards.
- Adding a new card requires editing the SELECT options *and* inserting a Cards row.
- A typo silently disconnects.

Why it's like this (inferred): Notion's relation UI is heavier than a select for what's essentially a one-pick-from-known-list value, and Bills don't need bidirectional analytics the way Transactions do.

**Resolve in phase 2**: foreign key from Bill → Card.

## 2. Takumi has no Bills DB

[[../people/takumi|Takumi]]'s universe has only Cards + Transactions. [[../people/baiboon|Baiboon]] and [[../people/nuta|Nuta]] have the full [[three-database-trinity]].

Why (inferred): Takumi is also the primary holder receiving the bank's actual statements, so the per-cycle reconciliation surface that Bills provides is less useful for him. Or simply: he built his system first, and Bills came later.

**Resolved in phase 2**: every cardholder gets a Bills view; the asymmetry disappears. See [[../future-app/product-shape#Bills & reconciliation]].

## 3. `หมวดหมู่` (categories) is Takumi-only

Only [[../databases/takumi-transactions]] has a category relation. Baiboon and Nuta have nothing equivalent.

If categories become useful for transparency to the friends (e.g. "you spent ฿X on food this month"), promote this to the supplement schemas.

**Resolved in phase 2**: `Category` is universal across all three holders, single-tag, required (with an `Other / Uncategorized` fallback). See [[../future-app/product-shape#Categories]].

## 4. Point multipliers diverge

Takumi has `×3`; supplement holders have `÷4`. See [[points-and-multipliers]] for the full matrix.

**Resolved in phase 2**: `Transaction.rewardRules` is a polymorphic JSON array (`{type: "multiplier", value: 5}`, etc.); any holder can carry any rule type. The Takumi-`×3` / supplement-`÷4` asymmetry collapses.

## 5. Cashback is Baiboon + Nuta, not Takumi

[[../databases/baiboon-transactions]] and [[../databases/nuta-transactions]] both have `% cb` and `cashback`; [[../databases/takumi-transactions]] does not. Baiboon's DS was extended to match Nuta's on 2026-05-25 (originally only Nuta's had cashback). See [[cashback]].

**Resolved in phase 2**: cashback joins multipliers inside `Transaction.rewardRules` (`{type: "cashback", percent: 5}`). Any holder's transaction can carry zero or more rules of either kind. The remaining Takumi gap disappears.

## 6. Cards-DB property labels lag

The relation property on [[../databases/nuta-cards]] is internally labelled `รายการใช้จ่ายผ่านบัตรของใบบุญ` (Baiboon's transactions) even though it actually points at Nuta's transactions DB. Likely a copy-paste artefact when Nuta's universe was cloned from Baiboon's. Cosmetic, but worth flagging.

## 7. Bills sort direction inconsistency

[[../databases/baiboon-bills]] sorts unpaid bills by `วันตัดรอบบิล` **desc**; [[../databases/nuta-bills]] sorts **asc**. Minor UI nit.

## 8. `Card` SELECT option lists differ between Baiboon and Nuta

The hardcoded option lists in the two Bills DBs aren't identical — Baiboon's includes `Krungsri NOW`, `Lotus's Beyond`, `ttb so smart`; Nuta's includes `AEON UnionPay`, `CardX JCB`. That's actually correct (each person has different cards) but reinforces why a relation would be preferable to a select.

## 9. Takumi's Cards DB omits `ธนาคาร/บริษัท`

[[../databases/takumi-cards]] has no issuer column. Baiboon's and Nuta's do. Probably an oversight or "I know my own cards' issuers without a column".

## 10. Notion does not support fractional points

The point-earning side of the schema is integer-only. `บาทต่อ 1 คะแนน` (baht per 1 point) on Cards is a plain integer; the multiplier checkboxes (`×0 / ×2 / ×3 / ×4 / ×5 / ÷4`) only scale integers; the realised-points formula `คะแนนที่ได้จริง` rounds to an integer. There is no per-row field that encodes "this row earned 0.25 pts".

This bites exactly one card in the current household — [[../cards/lotuss-beyond|Lotus's Beyond]], whose real rate is **50 ฿ → 0.25 pts** (general) and **50 ฿ → 1.5 pts** (at Lotus stores). The Notion-side realised-points formula will perpetually under-report this card's accumulation. The user reconciles Lotus's Beyond's point balance against the bank statement directly, not against the formula.

There is no point fixing this in Notion — the multiplier-checkbox shape can't be coaxed into representing 0.25× per row, and inventing a new fractional column would compound the divergence between Takumi / Baiboon / Nuta. See the broader framing in [[points-and-multipliers#approximation-caveat]].

**Resolved in phase 2**: `RewardRule.value` is a plain number (no integer constraint). See [[../future-app/data-model-target]] and the `RewardRule` shape in [[../future-app/product-shape]].

## 11. A card's title is spelled twice, and the two can disagree on case

A card's name lives in two independent places in Notion: the **Cards DS page title** and the **Bills `Card` SELECT option** (divergence 1 is why there are two at all). Nothing keeps them in sync, and for one card they differ:

| Where | Spelling |
|---|---|
| Baiboon's Cards DS page title | `Krungsri VISA` |
| Baiboon's + Nuta's Bills `Card` SELECT | `Krungsri Visa` |
| `scripts/repositories/cards/krungsri-visa.yaml` → `name` | `Krungsri Visa` |

Found 2026-08-27 while adding a transaction to that card. It matters because the two spellings are consumed by different code paths that cannot both be satisfied by one string:

- `lib.cards.find_card` resolves the **Cards DS title** (exact) to build a transaction's `Card` relation → needs `Krungsri VISA`.
- `/prepare-bill` validates against the **Bills SELECT** option list → needs `Krungsri Visa`.
- `lib.card_repo.by_name` joins on the YAML `name` → and used to be case-sensitive, so `Krungsri VISA` silently missed, dropping the card's `bill_cycle_pattern` and its `truemoney_711_points_exclusion` / `installment_rewards_upfront` flags. A `TMN*` row or an `NN/NN` term on this card would then have earned points it shouldn't.

`/prepare-bill` needs **both** spellings in a single call — it validates the SELECT with `card_name` and then hands that same string to `find_card` — so until 2026-09-09 the card could not be drafted at all. The failure surfaced when the first Krungsri Visa bill was drafted (cycle 2026-09-05): `CardNotFoundError: no card titled exactly 'Krungsri Visa' … Substring candidates: ['Krungsri VISA']`.

**Mitigated on the code side; the Notion data still diverges.** Both resolvers now fall back to a case-insensitive match that refuses ambiguity:

- `card_repo.by_name` — three passes (exact → apostrophes folded → case-insensitive).
- `lib.cards.find_card` — two passes (exact → case-insensitive), added 2026-09-09 for the reason above.

Case folding cannot reintroduce what strictness guards against (`UOB One` vs `UOB World` differ by more than case), and an ambiguous fold still raises. The YAML deliberately keeps `Krungsri Visa` — matching the Bills SELECT — which means the README's "exact Cards DS title" rule is satisfied only up to case for this one card.

Renaming either side in Notion would still fix it properly at the source; until then, either spelling resolves everywhere, so don't "correct" the YAML to `Krungsri VISA` — it would buy nothing and desynchronize it from the Bills SELECT.
