---
tags: [concept, temporal]
---

# Four date axes on every transaction

Each row in any Transactions DB has **four** date fields, modelled as independent properties because they answer different questions:

| Field                  | What it captures                                                |
|------------------------|-----------------------------------------------------------------|
| `Transaction Datetime` | When the holder physically swiped the card (datetime, with time). |
| `Process Date`         | When the bank posted/cleared the charge. Often later than swipe. Written only from a statement's POST column, by `/record-statement` (UOB so far); until then it's inferred, never stored (see below).|
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

## Posting dates (`Process Date`)

UOB One's cashback periods count by **posting date** ([[../promotions/uob-one-2026|UOB One 2026]]), so the ledger now keeps it (user, 2026-09-28):

- **From the statement.** `/record-statement` writes each line's POST date into `Process Date`, on every row the line accounts for: a friend's row, a `[บัตรหลัก]` share, Takumi's row or remainder. The UOB parser reads the POST column; other issuers' parsers don't yet.
- **Before the statement comes, inferred.** The date is worked out when needed and never written, so an actual posting date is always a statement's (`BillCycle.inferred_posting` / `lib.bill_cycle.posting_date`):
  - **UOB cards:** the next working day. UOB doesn't post on weekends or Thai public holidays: a 22 Oct 2026 charge posts 26 Oct, because 23 Oct is Chulalongkorn Day.
  - **Other issuers:** the next day. They post on weekends and holidays.
  - **TrueMoney (`TMN …`) and Agoda charges:** the next working day on any card.

### Points: real-time or per cycle

**UOB grants reward points in real time**, as each charge posts (user, 2026-09-28). The app balance moves on posting day. The statement's `UOB REWARDS POINT SUMMARY` ("Regular Points Earned") counts the lines *posted* in the statement window, the same window as UOB One's cashback: a charge posted on the statement date shows on the next statement. Checked against UOB World and UOB Makro for Aug and Sep 2026: the ledger formula, `floor(ยอดชำระ / 25) × multiplier` per line, reproduces UOB's figures. Your Anthropic charge posted 25 Sep, so its 730 points belong on October's statement. Other issuers grant points per cycle, at the statement. Because granting is real-time, UOB can only enforce UOB World's ฿20,000 bonus cap after the fact. June's and July's negative "Points Adjustment" figures (−1,298 and −599) may be that clawback; this is to verify with May's statement.

### How banks round points

UOB rounds per statement line, `floor(line / 25) × multiplier`, exactly like the ledger formula. KBank, KTC and Krungsri round **once on the cycle's spend** at each rate: `floor(Σ / 25) × multiplier`. Checked 2026-09-28 against KBank (Aug), KTC (Aug) and Krungsri Visa (Sep). Because the ledger rounds each row down, it runs a few points short on those cards every cycle (KTC Digital VISA Aug: 65 against 71). [[../../.claude/skills/audit-rewards/SKILL|/audit-rewards]] reports this separately as `rounding`.

