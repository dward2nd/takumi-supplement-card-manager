---
tags: [concept, state-machine]
---

# Payment lifecycle of a transaction

Every transaction row carries three independent boolean state flags:

| Flag           | Notion checkbox | Meaning |
|----------------|------------------|---------|
| `Processed`    | `Processed`      | The bank has posted (cleared) the authorization. |
| `ชำระแล้ว`      | `ชำระแล้ว`        | The holder has paid the bill that contains this transaction. |
| `Credit Return`| `Credit Return`  | The transaction was refunded / charged back. |

Plus `Bill Cycle Date` ties a transaction to the statement it lands on (see [[billing-cycle]]).

## State diagram (informal)

```
[ created ]
    │
    │  (sometimes hours, sometimes days)
    ▼
[ Processed ✓ ]      ← bank posts the charge
    │
    │  ┌── Credit Return ✓  (refunded; effectively unwinds the row)
    │  │
    │  ▼
    │ [ refunded / chargeback ]
    │
    │  bill cycle closes, statement issued
    ▼
[ ชำระแล้ว ✓ ]        ← holder paid the bill
```

A `Credit Return = true` transaction is left in the database — it isn't deleted. Its `ยอดชำระ` may stay positive (the original charge) with `Credit Return` acting as the offset signal, or it may be entered as a negative refund row depending on the user's habit. (Worth confirming with the user as a separate clarification.)

## Phase 2 model (resolved 2026-05-21)

[[../future-app/product-shape]] pins the future shape:

- The three boolean flags collapse into one `Transaction.status` enum: `pending` → `processed` → `paid`, or terminal `refunded`. The `Bill.paid` flag and per-transaction "paid" signal unify too.
- **A refund creates a new negative-amount `Transaction` row** (the "adjustment row") **and** flips the original transaction's status to `refunded`. Both representations co-exist deliberately — the negative row preserves bank-statement reality; the status flip lets reporting find "transactions that were refunded" without re-joining.
- **Cross-cycle refunds** — when the refund posts in a bill cycle later than the original transaction's cycle, the adjustment row's `billCycleDate` is set to the **next** cycle, treating it as an advance payment that reduces the next bill. Banks commonly handle late refunds this way; the model expresses it directly.

## How the flags interact with rollups

- `คะแนนสะสม` on a Card sums `คะแนนที่ได้จริง` from related transactions. Whether `Credit Return = true` rows contribute to that sum is determined by the formula body of `คะแนนที่ได้จริง` (see [[../formulas/points-realized]]) — decode when needed.
- `ยอดค้างชำระ rollup` sums `ยอดชำระ` — the [[../formulas/outstanding-balance]] formula on Cards likely subtracts paid amounts.

## Relation to Bills

The Bills DB tracks the bank-issued statement as a whole, with its own `จ่ายแล้ว` checkbox. So there are **two** "is it paid?" signals in the system:

- `ชำระแล้ว` on individual Transactions, and
- `จ่ายแล้ว` on the Bill that contains them.

These should be kept in sync but Notion has no mechanism to enforce that. A migration target should unify them.
