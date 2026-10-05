---
tags: [card, lotus, points, fractional-points]
issuer: Krungsri
holders: [takumi, baiboon]
points: fractional
---

# Lotus's Beyond

Lotus-group co-brand card, issued through Lotus Money Service — a Krungsri Consumer partner, so the card repo files it under `issuer: Krungsri` (user, 2026-09-27). It stays exempt from the Krungsri 7-11 / TrueMoney points exclusion (CP ALL), and Takumi pays it by auto-debit like the rest of the family — see [[../databases/takumi-bills#payments|takumi-bills → Payments]]. The issuer awards **fractional coins**, which the ledger holds since 2026-10-05 through the card's `คะแนนต่อ 1 หน่วย` and a `×6` box (below).

## Earning rules

| Where | Rate |
|---|---|
| General (anywhere else)                                                  | **50 ฿ → 0.25 pts** |
| At Lotus stores (card-tap) OR `TMN*LOTUS HYPER BANGKOK TH` (TrueMoney top-up at Lotus) | **50 ฿ → 1.5 pts** |

Notes:

- The "at Lotus" bonus applies to **both** physical card-tap purchases at Lotus and TrueMoney top-ups whose merchant string is `TMN*LOTUS HYPER BANGKOK TH`. This is unlike the UOB One `TMN 7-11` carve-out, where the TrueMoney top-up is *not* treated as 7-Eleven.
- Fractional points are the issuer's real rule, not a Notion artefact. The points balance on a statement will be fractional and accumulate over many small transactions.

### How the statement counts coins (verified 2026-10-05)

Decoded from the 5 Sep 2026 statement (Takumi's …3471 plus the untracked supplement …6524). Each line earns per whole ฿50 of its own amount, floored line by line: `floor(ยอดชำระ / 50)` blocks. A ฿46.75 line earns nothing. The coin summary prints two figures:

| Printed | Rule | 5 Sep 2026 |
|---|---|---|
| normal | 0.25 a block, every charge line | 56 blocks → 14.00 |
| special | 1.25 a block, Lotus's lines only (`LOTUS'S …`, `LOTUSS …`) | 49 blocks → 61.25 |

So a Lotus's line earns 1.5 a block in all, and every line's coins are a whole number of **quarter-coins**. The flooring has the same shape as [[../formulas/points-realized|`คะแนนที่ได้จริง`]]: floor first, then multiply. With `บาทต่อ 1 คะแนน` = 50, a row's formula points are its quarter-coins at the general rate. Takumi's 16 ledger points on that cycle are his 16 blocks. In quarter-coins, the Lotus's rate is ×6. The `TMN*LOTUS HYPER` case isn't on this statement and is still unverified.

## Notion encoding (since 2026-10-05)

The ledger counts **coins**, fractions included, through two additions made on all three holders' DBs (user, in the Notion UI):

| Where | Property | Lotus's Beyond |
|---|---|---|
| Cards | `คะแนนต่อ 1 หน่วย` (points per unit; number, empty = 1) | `0.25` |
| Cards | `บาทต่อ 1 คะแนน` | `50` (Baiboon's was 200 until 2026-10-05) |
| Transactions | `×6` (checkbox) | ticked on rows at Lotus's |
| Transactions | `คะแนนต่อ 1 หน่วย` (rollup of the card's field) | — |

So a row earns `floor(ยอดชำระ / 50) × (6 at Lotus's, else 1) × 0.25`: ฿151 at Lotus's = 4.5 coins, ฿52 elsewhere = 0.25. The formula multiplies by the per-unit figure *after* the supplements' outer floor, so a quarter-coin survives it, and every card with the field empty earns exactly what it did before (checked row by row on 2026-10-05: of 3,642 rows only Takumi's ten Lotus's Beyond earning rows changed, 16 → 15.25). See [[../formulas/points-realized]].

`auto_classify` ticks `×6` on Lotus's merchants (`LOTUS'S …`, `LOTUSS …`, `TMN*LOTUS HYPER …`, a `[บัตรหลัก]` prefix allowed; reason `+lotus-coins`) and `×0` on the coin exclusions below — `LotussBeyond` in `scripts/python/lib/earning/families.py`.

The card's `คะแนนสะสม` was set to the 5 Sep 2026 statement's 287.5 coins with a `[ปรับคะแนน] ยอดคะแนนคงเหลือตามใบแจ้งยอด 2026-09-05` row (+272.25), like every other card ([[../concepts/points-and-multipliers#Statement balance rows]]). `/audit-rewards` compares the coins too; a cycle's gap includes the untracked supplement …6524, whose spend sits in Takumi's ledger as one `โอนยอดจากบัตรเสริม` lump at `×0` (60 coins on 5 Sep 2026).

## Coin exclusions

From the card's coin terms (8 Jul 2025 – 31 Dec 2027, <https://www.lotussmoney.com/credit-card/platinum-beyond>, pasted by the user 2026-10-05): no coins on Bangchak stations; mutual funds; unit-linked and AIA insurance; currency exchange at Krungsri counters; baht charges at merchants registered abroad; utilities (MCC 4900: MEA, MWA, NT …); government (MCC 9211, 9222, 9223, 9311, 9399, 9402, 9405); public transport and tolls (MCC 4111, 4112, 4131, 4784: BTS, MRT, SRT, Easy Pass, M Pass); e-wallet top-ups; digital assets, crypto and forex; installments; cash advances, interest and fees; phone (MCC 4814), computer network and data services (4816), and wholesale non-durables (5199).

`auto_classify` sets `×0` with a Note (reason `+lotus-coins-exclusion`) on the ones a merchant string shows: Bangchak (`BANGCHAK`, `BCP`, `BSRC`), phone operators (`AIS`, `AWN`, `TRUE MOVE` / `ONLINE` / `ISERVICE`, `DTAC`), utilities, `WWW.MAKRO.PRO` (5199; `HTTPS://WWW.MAKRO.PRO/` is 5411 and earns), `AIA`, transport and tolls, top-ups, installments, and foreign-in-THB. The rest are `×0` by hand.

Phone bills earn no coins but count toward [[../promotions/lotuss-smp1|SMP1 / SMT2]] (`AMP*AIS SERVICESPaymen BANGKOK TH`, 1 Oct 2026).

## Campaigns

- [[../promotions/lotuss-lbs3|LBS3]] — big-ticket categories, Sep–Dec 2026.
- [[../promotions/lotuss-smp1|SMP1 / SMT2]] — shopping categories, Sep–Dec 2026 and October 2026; registered.

## See also

- [[_stubs|Card stub index]]
- [[../concepts/points-and-multipliers]] — the multiplier boxes and `คะแนนต่อ 1 หน่วย`.
- Memory: `project_points_earning_complexity` — the cross-card framing.
