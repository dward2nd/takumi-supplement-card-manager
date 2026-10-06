---
tags: [concept, procedure]
---

# Ledger reset — `Reset ยอดใช้จ่ายและคะแนน`

A single transaction row that drives one card's **outstanding balance** and **point balance** to exactly zero, so a cardholder can start a fresh record without deleting any history.

Introduced by [[../people/takumi|Takumi]] on his own cards on **2026-09-22**. The alternative he rejected was bulk-deleting old transactions; the reset row keeps every historical row intact and readable while making the card's headline numbers read zero going forward.

## Why a row works

Both of a card's headline numbers are **unfiltered sums over the card's whole transaction relation** — there is no date window, no cycle boundary, no paid/unpaid gate:

| Card property | Definition |
|---|---|
| `ยอดค้างชำระ` (outstanding) | `sum(ยอดชำระ)` over every related transaction — see [[../formulas/outstanding-balance]] |
| `คะแนนสะสม` (points) | `sum(คะแนนที่ได้จริง)` over every related transaction — see [[../formulas/points-realized]] |

Because nothing is filtered, one new row carrying the exact negation of each running total zeroes both. No historical row is touched.

## The two levers

**Balance** — `ยอดชำระ` is summed raw, so the reset row simply carries the negated balance.

**Points** — `คะแนนที่ได้จริง` subtracts `ใช้คะแนน` (points redeemed) *unconditionally*, outside the `ยอดชำระ > 0` earning gate. `ใช้คะแนน` is therefore a free-floating "remove N points" dial, and the reset row turns it to whatever cancels the card's accumulated total.

The subtlety: **the reset row earns points of its own.** If its `ยอดชำระ` lands positive, it passes the `> 0` gate and earns `floor(ยอดชำระ / บาทต่อ 1 คะแนน)`. That self-earned amount has to be added into `ใช้คะแนน` or the card settles a few points above zero.

## Recipe

For each card, read its current `ยอดค้างชำระ` (call it `B`), its current `คะแนนสะสม` (`P`), and its `บาทต่อ 1 คะแนน` (`R`). Then create one Transactions row:

| Property | Value |
|---|---|
| `Name` | `Reset ยอดใช้จ่ายและคะแนน` |
| `Card` | the card (relation — **required**, or the row affects nothing) |
| `ยอดชำระ` | `-B` |
| `ใช้คะแนน` | `P + (floor(-B / R) if -B > 0 else 0)` — leave empty when that is 0 |
| `Transaction Datetime` | the reset date |
| `Bill Cycle Date` / `Due Date` | **empty** (since 2026-10-06, see below) |
| `Processed` | ✅ true |
| `ชำระแล้ว` / `Credit Return` | ☐ false |
| multiplier checkboxes | all unticked (multiplier `1`) |

Leaving the multipliers unticked rather than ticking `×0` is the convention in Takumi's rows. It doesn't matter when `-B ≤ 0` (nothing earns), but when `-B > 0` the `×0` box would suppress the self-earned points and `ใช้คะแนน` would then drop the `floor(-B / R)` term. Pick one convention and keep it; the rows written on 2026-09-22 use *unticked*.

## The self-earn trap

The `+ floor(-B / R)` term in `ใช้คะแนน` is the easy thing to get wrong, and it only bites when the reset amount comes out **positive** — i.e. when the card was overpaid. Set `ใช้คะแนน = P` on such a row and the card settles at `floor(-B / R)` points instead of zero, which looks like a rounding glitch rather than a mistake.

It caught two of the first four rows (see below). Ticking `×0` is the alternative guard: it forces the earning term to zero, and then `ใช้คะแนน = P` is always right. The household convention is unticked + the correction term — but if you ever automate this, `×0` is the safer default because it removes `บาทต่อ 1 คะแนน` from the arithmetic entirely.

Note that a **negative** reset amount fails the `ยอดชำระ > 0` gate and earns nothing, so `ใช้คะแนน = P` is correct with no correction. Ten of the sixteen cards were in this case.

## Worked example — Takumi, 2026-09-22 → 09-23

All sixteen of Takumi's cards, each row named `Reset ยอดใช้จ่ายและคะแนน` and dated 2026-09-22. Takumi wrote the first four by hand; the remaining ten were written through `/add-transaction`.

| Card | `ยอดชำระ` | `ใช้คะแนน` | `Bill Cycle Date` | `Due Date` |
|---|---:|---:|---|---|
| UOB World | `4387.67` | `11055` | 2026-09-25 | 2026-10-15 |
| UOB Premier | `-727.999999999996` | `10671` | 2026-09-25 | 2026-10-15 |
| UOB One | `99` | *(empty)* | 2026-09-25 | 2026-10-15 |
| Grab PayLater | `-564` | `1106` | 2026-10-01 | 2026-10-07 |
| KTC UnionPay | `-6641.45` | `238` | 2026-09-27 | 2026-10-12 |
| KTC Digital VISA | `-244` | `1515` | 2026-09-27 | 2026-10-12 |
| KTC Mastercard | `0` | `536` | 2026-09-27 | 2026-10-12 |
| Krungsri JCB | `-5455.6` | `2426` | 2026-10-05 | 2026-10-25 |
| Krungsri VISA | `-3864.3` | `2051` | 2026-10-05 | 2026-10-25 |
| Krungsri NOW | `-4222.29` | `22` | 2026-10-05 | 2026-10-25 |
| Central The 1 Redz | `-25` | `336` | 2026-10-05 | 2026-10-25 |
| AEON Primo | `-2855` | `1504` | 2026-10-10 | 2026-11-02 |
| AEON Rabbit | `-485.42` | `871` | 2026-10-10 | 2026-11-02 |
| AEON Next Gen | `-598` | *(empty)* | 2026-10-10 | 2026-11-02 |

`SPayLater` and `KTC JCB` were already at 0 balance / 0 points and got no row — a reset row for them would be a no-op.

Points to read off this table:

- **A positive amount means the card was overpaid.** Three of Takumi's four hand-written rows were positive, which reads backwards until you internalise the sign flip. His ledger had no activity after 2025-06-11 and had drifted net-overpaid on the UOB cards.
- **`KTC Mastercard` carries amount `0`.** Its balance was already zero but it held 536 points, so the row exists purely to run `ใช้คะแนน`. Amount `0` fails the `> 0` gate, so it earns nothing — exactly what's wanted.
- **`-727.999999999996` is float noise** from negating an accumulated sum. Harmless, and evidence the figure was computed rather than typed. `AEON Next Gen` leaves a comparable ~2×10⁻¹² residue for the same reason.
- **No bill-cycle dates** (user, 2026-10-06: "to avoid confusion … I want to use the sum aggregation to see if every bill cycle ends up with 0 Baht of balance"). The rows were first written with the card's open cycle (`lib.bill_cycle.active_cycle`), which put the reset amount into that cycle's sum. Grab PayLater, for example, had a cycle holding nothing but its reset row. On 2026-10-06 all 14 rows had `Bill Cycle Date` and `Due Date` cleared, and every closed cycle in Takumi's ledger then summed to ฿0.00. Card balances and points are unaffected, being unfiltered sums. The points scripts treat a `Reset …` row as before every statement whatever its dates (`lib.points_balance`). One side effect: the Cards DB's `วันตัดรอบบิล` / `วันครบกำหนดชำระ` rollups (latest date, read by `/summarize-overview`) fall back to the newest real row: AEON Next Gen and AEON Primo show 2025-06-10, Grab PayLater 2025-03-31, Central The 1 Redz 2026-09-05. A new reset row is written without dates.

### Two rows needed correcting

Takumi's hand-written rows hit the self-earn trap and a sign slip. Both were fixed on 2026-09-23 via `/update-transaction`:

| Card | Field | Was | Now | Why |
|---|---|---:|---:|---|
| UOB World | `ใช้คะแนน` | `10880` | `11055` | `+4387.67` self-earned `floor(4387.67 / 25)` = 175 pts, leaving the card at 175 instead of 0 |
| Grab PayLater | `ยอดชำระ` | `564` | `-564` | sign slip — the pre-reset balance was `+564`, so `+564` doubled it to `1128` instead of cancelling |

The Grab PayLater fix corrected the point balance as a side effect: flipping the sign dropped the row below the `> 0` gate, removing the 56 points it had been self-earning.

## When not to do this

A reset row is indistinguishable from a real charge to everything downstream. Before running one on a card, check:

- **Live debt.** Zeroing `ยอดค้างชำระ` on a card that genuinely owes the bank destroys the household's record of what's owed. The supplement holders' cards are the live ones — see the caution in [[supplement-card-model]]. Takumi's own ledger was dormant, which is what made it safe.
- **Bills.** A reset row with a `Bill Cycle Date` would be summed by `/prepare-bill` into that cycle's draft exactly like a purchase; written without dates (above), it falls in no cycle. On [[../databases/baiboon-bills|Baiboon]]'s and [[../databases/nuta-bills|Nuta]]'s cards that silently corrupts the next bill. Takumi's Bills DB (added 2026-09-27) takes the statement's printed total rather than summing his rows — see [[../databases/takumi-bills]] — so the exposure still doesn't exist on his side.
- **Statement reconciliation.** `/audit-bill` will report the reset row as a Notion row with no matching statement line, forever.

This is a deliberate exception to the house rule in `CLAUDE.md` and `/audit-bill` that Notion's calculated balance is reconciled against the bank, never edited to match it. A reset is the holder declaring a new epoch for their own record — not a correction.

## Phase 2

The target app should model this as an explicit **ledger epoch** (a per-card "balance and points start from zero as of date D") rather than a magic transaction, so that resets are visibly different from spending and can't leak into bill totals or statement audits. See [[../future-app/product-shape]].
