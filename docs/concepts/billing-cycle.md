---
tags: [concept, temporal]
---

# Four date axes on every transaction

Each row in any Transactions DB has **four** date fields, modelled as independent properties because they answer different questions:

| Field                  | What it captures                                                |
|------------------------|-----------------------------------------------------------------|
| `Transaction Datetime` | When the holder physically swiped the card (datetime, with time). |
| `Process Date`         | When the bank posted/cleared the charge. Often later than swipe.|
| `Bill Cycle Date`      | The statement (cycle) cut-off date this transaction lands on.   |
| `Due Date`             | The date the resulting bill is due to be paid.                  |

## Why four

Two physical events (swipe, bank-post) and two accounting events (cycle cut-off, payment due) are all relevant but they don't reduce to each other:

- Swipe-to-post lag matters for fraud watch.
- Bill Cycle Date determines which monthly statement (and which `Bills` row) the transaction belongs to.
- Due Date drives Card rollups (`วันครบกำหนดชำระ`) which surface "what's coming due soon" on the Cards DB.

## Views built on these

Each Transactions DB has multiple views that *group by* a different date axis:

- `วันเวลาใช้จ่าย` — grouped by `Transaction Datetime`
- `วันประมวลผล` — grouped by `Process Date`
- `วันตัดรอบบิล` — grouped by `Bill Cycle Date`
- (no view grouped by `Due Date`, but Cards rolls it up)

## Relation to Bills

Two ways a transaction is tied to a billing period:

1. `Bill Cycle Date` on the Transaction (a date) — the cycle cut-off.
2. The `Bills` row whose `วันตัดรอบบิล` matches that date for that card.

These are linked *by convention*, not by a Notion relation (Bills' `Card` is a SELECT, not a relation — see [[known-divergences]]). A reconciliation script could verify "for each Bill, the sum of unpaid Transactions in the matching cycle equals `ยอดชำระ`". Such a script would belong in `scripts/`.

## Phase 2 model (resolved 2026-05-21)

[[../future-app/product-shape]] preserves the four-date model. The new field names align with phase-2 conventions:

| Notion (today)          | Phase-2 field      | Notes                                                          |
|-------------------------|--------------------|----------------------------------------------------------------|
| `Transaction Datetime`  | `swipedAt`         | unchanged semantics                                            |
| `Process Date`          | `processedDate`    | `null` while `status = pending`                                |
| `Bill Cycle Date`       | `billCycleDate`    | may be the *next* cycle for cross-cycle refund adjustment rows |
| `Due Date`              | `dueDate`          | unchanged semantics                                            |

All four are first-class columns in the UI (not buried behind tabs as in Notion's view layer). The reconciliation script described above also lives natively in the new app as the "tx-sum vs. bill-amount delta" prompt on each bill — see [[../future-app/product-shape#Bills & reconciliation]].

## See also

- [[payment-lifecycle]] — the orthogonal status axis.
- [[../future-app/product-shape]] — phase-2 product spec.
