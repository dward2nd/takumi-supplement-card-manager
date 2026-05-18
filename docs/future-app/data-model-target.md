---
tags: [future, data-model]
---

# Phase-2 data model target (stack-agnostic)

The future application replaces Notion entirely. This note sketches the target relational shape — **without** committing to a database engine, ORM, or runtime.

## Entities

```
┌──────────────┐         ┌────────────────────┐
│   Person     │1───*   │  PrimaryAccount    │
│  - id        │         │  - id              │
│  - displayName │       │  - issuerId        │
│  - role:      │         │  - accountNumberHash│
│    primary    │         │  - creditLimit     │
│   |supplement │         │  - holderPersonId  │  → Person
└──────┬───────┘         └─────────┬──────────┘
       │                            │
       │                       1    │   *
       │                            ▼
       │                  ┌────────────────────┐
       │                  │  Card              │     supplement card
       │      *           │  - id              │     (or primary card)
       └──────────────────│  - primaryAccountId│
                          │  - holderPersonId  │  → Person
                          │  - productNameId   │  → CardProduct
                          │  - networkId       │  → CardNetwork
                          │  - premiumTier     │
                          │  - bahtPerPoint    │
                          │  - pointsPerCycle  │ (boolean)
                          │  - allocatedLimit  │ (per-holder share)
                          └─────────┬──────────┘
                                    │
                              1     │    *
                                    ▼
                          ┌────────────────────┐
                          │  Transaction       │
                          │  - id              │
                          │  - cardId          │
                          │  - categoryId      │ (nullable)
                          │  - amountBaht      │
                          │  - pointsRedeemed  │
                          │  - swipedAt        │ (datetime)
                          │  - processedDate   │
                          │  - billCycleDate   │
                          │  - dueDate         │
                          │  - status: enum    │ (pending|processed|paid|refunded)
                          │  - rewardRules: [] │ (replaces ×0/×2/×3/×4/×5/÷4 + %cb)
                          │  - note            │
                          └─────────┬──────────┘
                                    │
                              *     │    1
                                    ▼
                          ┌────────────────────┐
                          │  Bill              │
                          │  - id              │
                          │  - cardId          │  ← FK (not select!)
                          │  - cycleDate       │
                          │  - amountBaht      │
                          │  - paid: bool      │
                          │  - statementFile   │
                          │  - paymentEvidence │
                          └────────────────────┘

      ┌────────────────────┐
      │  CardProduct       │  catalogue, e.g. UOB Premier
      │  - id              │
      │  - name            │
      │  - issuerId        │
      └────────────────────┘

      ┌────────────────────┐
      │  Issuer            │  e.g. UOB, KTC, Krungsri
      └────────────────────┘

      ┌────────────────────┐
      │  CardNetwork       │  JCB, Mastercard, VISA, UnionPay, Unspecified
      └────────────────────┘
```

## Key differences from Notion-as-built

1. **`Bill.cardId` is a real FK**, not a SELECT. Resolves [[../concepts/known-divergences|divergence #1]].
2. **`Card` is a child of `PrimaryAccount`** (a missing entity in Notion). One PrimaryAccount holds many Cards (primary + supplements), each belonging to a `Person`.
3. **Reward rules are first-class**, replacing the parallel checkbox columns and `% cb` with a polymorphic structure. A `Transaction` carries zero or more `RewardRule` applications (`{type: "multiplier", value: 5}`, `{type: "cashback", percent: 1.0}`).
4. **One `Transaction.status` enum** replaces three boolean flags (`Processed` / `ชำระแล้ว` / `Credit Return`). The state diagram in [[../concepts/payment-lifecycle]] becomes the enum's transition rules.
5. **`Category` is universal**, not Takumi-only. Backfill optional but supported.
6. **Bill ⟷ Transaction relation** is materialised (not just "Bills.วันตัดรอบบิล == Transactions.Bill Cycle Date matches for the same Card") — simplifies reconciliation.

## Open questions for the user

- Should `PrimaryAccount` be exposed at the UI level, or only used internally?
- Granularity of `RewardRule`: one row per applied rule, or a JSON column on Transaction?
- Should `Card` carry a per-cycle quota (e.g. "the ×5 promo only applies to first ฿10,000")?
- Is "Credit Return" a *transition* (transaction → refunded) or an *adjustment row* (a new negative transaction)?

These are not blockers for the vault. They'll be resolved at phase-2 planning.

## See also

- [[migration-considerations]] — what we do about existing Notion data.
