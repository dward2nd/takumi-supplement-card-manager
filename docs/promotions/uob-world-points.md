---
tags: [promotion, uob-world, points-5x]
---

# UOB World ×5 points bonus (standing)

UOB World's `×5` points bonus. Unlike [[uob-one-2026]] this is **not** a cashback promotion — UOB World pays no cashback at all. What the promo carries is a **points multiplier**, and it is the first entry in the repository to use the promotion mechanism for the points axis rather than the `% cb` axis.

> **Structured source of truth**: `scripts/repositories/promotions/uob-world-points.yaml`.
> This page is the *narrative*. The card-level facts — base rate, petrol exclusion, the quota caveat — live in `scripts/repositories/cards/uob-world.yaml`; see [[../cards/uob-world]].

- **Effective**: `2025-01-01` → open-ended (`effective_end: null`).
- **Card**: [[../cards/uob-world]] (Takumi primary; Baiboon supplement).
- **Cashback**: none, ever. `% cb` stays unset on every UOB World row.

## Why the dates are what they are

**The effective dates are reconstructed, not sourced from issuer T&Cs.** This rule predates the promotions system entirely (user, 2026-08-20: *"Maybe the special point rules had existed before the promotion system was made"*), so there was no YAML to read and no announcement to cite. `effective_start` was instead derived from Baiboon's transaction history: the earliest `×5` row on the card is dated **2025-01-28**, and `×5` is the dominant multiplier in every month since. `2025-01-01` is the conservative month boundary before that first observation.

`effective_end` is `null` because the user confirmed the bonus is still running (*"I didn't say the card promotion has run out"*). If it does lapse, set the end date via [[../../.claude/skills/update-promotion/SKILL.md|/update-promotion]] rather than deleting the file — the historical reading matters for re-classifying old rows.

## The two tiers

| Multiplier | When | Where it's encoded |
|---|---|---|
| `×5` | Bonus, while this promo is active **and** the cycle's quota is unspent | `promotions/uob-world-points.yaml` → `points_default` |
| `×2` | The card's **base** Thailand rate — and the fallback once the quota is spent | `cards/uob-world.yaml` → `points_default` |

Note that the base is `×2`, not `×1`. An unboosted UOB World row still earns double, so leaving the multiplier unset (which Notion reads as `×1`) would under-report. This is why the card carries an explicit `points_default`.

Historical rows confirm both tiers in the user's own words — `UOB World default ×2 multiplier (Thailand merchant)` on April 2026 rows, against `UOB World ×5 multiplier for May 25 bill cycle (special promo…)` on others.

## The ≈฿20,000 per-cycle quota — a known gap

Once a cycle's eligible spend passes roughly **฿20,000**, further rows drop from `×5` to `×2`, and the row straddling the boundary is **split by hand**. The evidence is in the Notion notes, verbatim:

```
ได้คะแนน 2 เท่าเพราะเต็มโควต้า 20k แล้ว
ยอดเกินมาจาก quota 20k เป็นจำนวน 729.55 บาท เหลือยอดที่ได้ 5 เท่า
```

**No script enforces this.** `lib.promotions.classify(card, date, merchant)` is a pure function of those three arguments — it has no view of cycle-to-date spend, so while this promo is active it returns `×5` unconditionally. Two consequences:

1. On a high-spend cycle, `auto_classify` will over-report. Check the cycle total before trusting it. Feb 2026 and Apr 2026 both blew the quota (`×2` dominates those two months).
2. The straddling-row split can't be automated at all under the current schema — one Notion row carries one multiplier checkbox, so a part-`×5` / part-`×2` charge is a manual judgment call. See [[../concepts/known-divergences]] on the integer-only points model.

Making this enforceable would mean giving `classify` a cycle-spend argument (or moving quota logic to a caller that has it), plus a `points_quota` block in the promotion schema. Deliberately not built — see *Open questions*.

## Exclusions

The promo does not override the project-wide exclusions:

- **Foreign merchant billed in THB** → `×0`. Fires before tier resolution.
- **Petrol stations** → `×0`, via `petrol_exclusion: true` on the card. UOB carries this exclusion across its whole range.

The petrol path was **wrong until 2026-08-20**: it returned `promo.points_default or card_points_default`, which on this card meant a petrol row was classified `×5` while the very same branch wrote a Note saying it earned nothing. Latent for every other card because they all set `points_default: "×0"`. Now both petrol branches in `lib.promotions` force `×0` explicitly.

## Points redemption

UOB World has a real points balance, and it gets redeemed — e.g. a `Major Combo set 1 ชุด` row for 1,400 points. Redemptions are written with `points_redeemed`, `amount: 0`, and `multiplier: "×0"`; see [[../../.claude/skills/add-transaction/SKILL.md|/add-transaction]]'s `ใช้คะแนน` conventions.

## Open questions

- **Is the ฿20,000 quota per-card or per-account?** Baiboon is one of several holders on Takumi's UOB account, and [[../future-app/product-shape]] explicitly anticipates household-wide shared quotas. If it's account-level, the quota is consumed faster than a per-card reading suggests. Unresolved.
- **Is the quota measured on eligible spend or total spend?** The reconstruction above assumes eligible (positive-amount, non-`×0`) rows.
- **What is the real `effective_start`?** `2025-01-01` is inferred from first observation, not sourced. Baiboon's data begins around then, so the bonus may well be older than the ledger.
- **Does `×5` apply to foreign-currency (non-THB) charges?** All observed `×0` foreign rows were THB-billed, so the genuine-foreign-currency case is untested on this card.

## See also

- `scripts/repositories/promotions/uob-world-points.yaml` — the structured source of truth.
- [[../cards/uob-world]] — card-level facts and the quota caveat.
- [[../concepts/promotions]] — the cross-cutting promotion model.
- [[../concepts/points-and-multipliers]] — why the multiplier is a checkbox enum and not a number.
- [[uob-one-2026]] — the cashback-axis counterpart on a sibling UOB card.
