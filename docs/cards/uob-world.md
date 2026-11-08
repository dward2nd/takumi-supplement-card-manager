---
tags: [card, uob, points-5x, points-2x]
issuer: UOB
holders: [takumi, baiboon]
points: "×5 bonus / ×2 base"
cashback: none
---

# UOB World

UOB's premium points card. Takumi holds the primary; Baiboon carries a supplement on the same account. Promoted from [[_stubs]] on 2026-08-20 when the earning rules were finally written down.

**This is a points card, not a cashback card.** `% cb` stays unset on every UOB World row — there is no promotion granting cashback here and there never has been. If you find yourself about to write a `% cb` value on this card, something is wrong.

## Points

Two tiers, both of which **predate the promotions system** (user, 2026-08-20):

| Multiplier | Meaning |
|---|---|
| `×5` | The standing bonus, active in Baiboon's data since **2025-01-28**. Encoded as [[../promotions/uob-world-points]]. |
| `×0` | Petrol, foreign merchants billed in THB, and **e-wallet top-ups** (`2C2P *SHOPEEPAY (TOP …`; user, 2026-09-28): the `UOBCard` family and the `UOBWorldBonus` Bureau class both know them. |
| `×2` | The card's **base** Thailand rate, and the fallback once the cycle's bonus quota is spent. Encoded as `points_default` on `scripts/repositories/cards/uob-world.yaml`. |

The base is `×2`, not `×1` — an unboosted UOB World row still earns double. Leaving the multiplier unset means `×1` in Notion's `คะแนนที่ได้จริง` formula, which would under-report; hence the explicit card-level default. See [[../concepts/points-and-multipliers]].

### The ฿20,000 per-cycle quota

Per account (Takumi + Baiboon together), counting every transaction, first come, first served; ×5 only on the bank's bonus categories (online, e-wallet, dining, travel, foreign currency). Enforced since 2026-09-28 by the Promotion Bureau (one row per cycle). The row the quota ends in keeps ×5 and gives back its over-quota part through `ใช้คะแนน`. Full detail in [[../promotions/uob-world-points]].

**The 25 Oct 2026 statement** (`/audit-rewards`, 2026-11-08; fixed 2026-11-09). UOB printed 4,164 earned and the ledger gave 4,410 (+246). The quota is ฿20,000 of *spend*, as the household has always read it (user, 2026-11-09: "it caps on the total spending up to 20,000 Baht, regardless of whether a particular transaction gains points or not"). The statement adds two details the Bureau doesn't model:
- **Which spend.** UOB counts the spend *posted* in the statement period (25 Sep – 24 Oct), not the bill cycle. `ANTHROPIC* CLAUDE SUB SAN FRANCISCO` ฿3,669.72 is dated 24 Sep, posted 25 Sep (the September statement date) and billed on 2026-09-25, and it counted toward October: ฿22,480.97 posted in all. The Bureau's `2026M10 — UOB World ×5` groups by bill cycle, found ฿18,811.25 and left every row at ×5.
- **How the bonus is worked out.** On the ฿20,000 as a whole: 1,764 base (2 per ฿25, each row rounded down) + 20,000 ÷ 25 × 3 = 2,400 bonus = 4,164, exactly as printed. The household's per-row split (rows past the quota at ×2, the straddling row giving back ⌊over × 3 / 25⌋) gives 4,134, because every row rounds down.

Whether non-earning rows count toward the ฿20,000 can't be told from this statement: its only one, `APPLE.COM/BILL` ฿69, posted after the quota was full. Baiboon's `WWW.MAKRO.PRO BANGKOK TH` ฿16,850 (11 Oct) earned the bonus, so UOB has no Makro PRO exclusion.

The fix, as the user chose it for this cycle (2026-11-09): `/record-statement` stamped the 32 October rows' `Process Date`, all of them already on the right bill cycle, and a `[ปรับคะแนน] โบนัส ×5 เกินโควต้า 20k รอบบิล 2026-10` row (฿0, `×0`, `ใช้คะแนน` 246, billed 2026-10-22) holds the cap, since the points formula can't cap. The rows keep ×5, and the Bureau row is unchanged. The audit is `ok` and the card holds the printed 21,782. A later cycle whose posted spend passes ฿20,000 while its bill cycle doesn't (or the other way round) needs the same row by hand, until the Bureau counts by posting date.

## Exclusions

- **Petrol** → `×0`. A rule of `UOBCard` (`lib/earning`); UOB carries this across its whole range. See [[../concepts/promotions]].
- **Foreign merchant billed in THB** → `×0`, per the project-wide default rule. Observed on `APPLE.COM/BILL CORK IRL`, `Google YouTubePremium Mountain View USA`, `Flights on Booking.com Amsterdam NLD`.
- **7-11 / TrueMoney** → **no exclusion.** That rule is Krungsri-family only; UOB is unrelated, so `TMN 7-11` and `TMN ISERVICECCP` rows earn at the full `×5`. Don't copy the First Choice treatment over.

## Points redemption

Unlike [[uob-one]], this card has a real points balance that gets spent — e.g. `Major Combo set 1 ชุด` for 1,400 points (2026-05-19). Write redemptions with `points_redeemed`, `amount: 0`, `multiplier: "×0"` per [[../../.claude/skills/add-transaction/SKILL|/add-transaction]].

Points also pay for restaurant slips through [[../promotions/uob-dining-pwp-2026|UOB Dining PWP 2026]] (20% back on Fri–Sun slips of ฿1,500 or more, on Takumi's primary card only). Uses are logged on the promotion note (Sushiro, 30 Oct 2026).

## Writing UOB World transactions

`auto_classify: true` now handles this card correctly — it resolves `×5` normally, `×0` on petrol and foreign-in-THB, and `×2` for dates outside the promo window. The one thing it cannot know is the quota. Since 2026-09-28 that doesn't need a manual step: after every write, [[../../.claude/skills/add-transaction/SKILL|/add-transaction]] (and `/update-transaction`, `/record-statement`) re-syncs the cycle's `UOB World ×5` Bureau row. It sets rows past the ฿20,000 to `×2` with the quota Note, and sets the straddling row's `ใช้คะแนน` give-back ([[../concepts/promotion-bureau#Kept in step with the ledger]]). A cycle with no Bureau row yet isn't enforced; the write reports it as `missing`.

## Open questions

- Does Takumi hold this card as a primary in his own Cards DB? [[_stubs]] marks Takumi `✓` but his DB hasn't been enumerated row-by-row.
- The bonus may be older than `2025-01-01` — that date is the conservative boundary before the first observed `×5` row, not a sourced start date.

## See also

- `scripts/repositories/cards/uob-world.yaml` — the structured card entry.
- [[../promotions/uob-world-points]] — the `×5` bonus narrative.
- [[../promotions/uob-dining-pwp-2026]] — paying for restaurant slips with points.
- [[uob-one]] — the cashback-axis sibling on the same UOB account.
- [[uob-makro]] — the other UOB card with a non-standard multiplier (`÷4` on in-store Makro).
