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
| `×2` | The card's **base** Thailand rate, and the fallback once the cycle's bonus quota is spent. Encoded as `points_default` on `scripts/repositories/cards/uob-world.yaml`. |

The base is `×2`, not `×1` — an unboosted UOB World row still earns double. Leaving the multiplier unset means `×1` in Notion's `คะแนนที่ได้จริง` formula, which would under-report; hence the explicit card-level default. See [[../concepts/points-and-multipliers]].

### The ≈฿20,000 per-cycle quota

Past roughly ฿20,000 of eligible spend in a cycle, rows drop from `×5` to `×2`. **No script enforces this** — `lib.promotions.classify` can't see cycle-to-date spend, so it returns `×5` for as long as the promo is active. Check the cycle total yourself on a heavy month; Feb 2026 and Apr 2026 both exceeded the quota and are dominated by `×2` rows as a result.

The row that straddles the boundary gets split by hand — one Notion row carries one multiplier checkbox, so a part-`×5` / part-`×2` charge can't be expressed. The user records the arithmetic in `Note` instead:

```
ยอดเกินมาจาก quota 20k เป็นจำนวน 729.55 บาท เหลือยอดที่ได้ 5 เท่า
```

Full detail, including whether the quota might be account-level rather than per-card, is in [[../promotions/uob-world-points]].

## Exclusions

- **Petrol** → `×0`. `petrol_exclusion: true`; UOB carries this across its whole range. See [[../concepts/promotions]].
- **Foreign merchant billed in THB** → `×0`, per the project-wide default rule. Observed on `APPLE.COM/BILL CORK IRL`, `Google YouTubePremium Mountain View USA`, `Flights on Booking.com Amsterdam NLD`.
- **7-11 / TrueMoney** → **no exclusion.** That rule is Krungsri-family only; UOB is unrelated, so `TMN 7-11` and `TMN ISERVICECCP` rows earn at the full `×5`. Don't copy the First Choice treatment over.

## Points redemption

Unlike [[uob-one]], this card has a real points balance that gets spent — e.g. `Major Combo set 1 ชุด` for 1,400 points (2026-05-19). Write redemptions with `points_redeemed`, `amount: 0`, `multiplier: "×0"` per [[../../.claude/skills/add-transaction/SKILL|/add-transaction]].

## Writing UOB World transactions

`auto_classify: true` now handles this card correctly — it resolves `×5` normally, `×0` on petrol and foreign-in-THB, and `×2` for dates outside the promo window. The one thing it cannot know is the quota, so:

1. Before writing a batch on a high-spend cycle, sum the cycle's eligible rows.
2. If the total is near or past ฿20,000, override the affected rows to `multiplier: "×2"` per-tx and explain in `Note`.

## Open questions

- Is the ฿20,000 quota **per-card or shared across Takumi's UOB account**? [[../future-app/product-shape]] anticipates household-wide quotas, which would change the arithmetic.
- Does Takumi hold this card as a primary in his own Cards DB? [[_stubs]] marks Takumi `✓` but his DB hasn't been enumerated row-by-row.
- The bonus may be older than `2025-01-01` — that date is the conservative boundary before the first observed `×5` row, not a sourced start date.

## See also

- `scripts/repositories/cards/uob-world.yaml` — the structured card entry.
- [[../promotions/uob-world-points]] — the `×5` bonus narrative.
- [[uob-one]] — the cashback-axis sibling on the same UOB account.
- [[uob-makro]] — the other UOB card with a non-standard multiplier (`÷4` on in-store Makro).
