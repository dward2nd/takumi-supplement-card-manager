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
