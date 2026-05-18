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

## How the flags interact with rollups

- `คะแนนสะสม` on a Card sums `คะแนนที่ได้จริง` from related transactions. Whether `Credit Return = true` rows contribute to that sum is determined by the formula body of `คะแนนที่ได้จริง` (see [[../formulas/points-realized]]) — decode when needed.
- `ยอดค้างชำระ rollup` sums `ยอดชำระ` — the [[../formulas/outstanding-balance]] formula on Cards likely subtracts paid amounts.

## Relation to Bills

The Bills DB tracks the bank-issued statement as a whole, with its own `จ่ายแล้ว` checkbox. So there are **two** "is it paid?" signals in the system:

- `ชำระแล้ว` on individual Transactions, and
- `จ่ายแล้ว` on the Bill that contains them.

These should be kept in sync but Notion has no mechanism to enforce that. A migration target should unify them.
