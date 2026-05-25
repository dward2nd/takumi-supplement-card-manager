---
tags: [card, lotus, points, fractional-points]
issuer: Lotus
holders: [baiboon]
points: fractional
---

# Lotus's Beyond

Lotus-group co-brand card. One of the few cards in the household whose earning model **does not fit** the Notion `×N`/`÷N` multiplier enum — the issuer awards **fractional points**, not just integer multiples of a base rate.

## Earning rules

| Where | Rate |
|---|---|
| General (anywhere else)                                                  | **50 ฿ → 0.25 pts** |
| At Lotus stores (card-tap) OR `TMN*LOTUS HYPER BANGKOK TH` (TrueMoney top-up at Lotus) | **50 ฿ → 1.5 pts** |

Notes:

- The "at Lotus" bonus applies to **both** physical card-tap purchases at Lotus and TrueMoney top-ups whose merchant string is `TMN*LOTUS HYPER BANGKOK TH`. This is unlike the UOB One `TMN 7-11` carve-out, where the TrueMoney top-up is *not* treated as 7-Eleven.
- Fractional points are the issuer's real rule, not a Notion artefact. The points balance on a statement will be fractional and accumulate over many small transactions.

## Notion encoding

The Notion multiplier enum (`×0` / `×2` / `×3` / `×4` / `×5` / `÷4`) cannot express either of Lotus's Beyond's true rates literally:

- 50 ฿ → 0.25 pts is `0.005 pts per baht` — not a clean multiple of the standard 1 pt / 25 ฿ rate.
- 50 ฿ → 1.5 pts is `0.03 pts per baht` — same problem.

### Known Notion-side limitation: no fractional-point support

**The Notion model does not currently represent fractional points at all.** The `บาทต่อ 1 คะแนน` (baht-per-1-point) field on Cards is a plain integer/number, the multiplier checkboxes only multiply integer amounts, and the `คะแนนที่ได้จริง` formula's output is the integer point figure. There is no per-row field that encodes "this row earned 0.25 pts" or "this row earned 1.5 pts".

The practical consequences for Lotus's Beyond in the Notion vault:

- The realised-points formula will *not* reflect Lotus's real fractional accumulation. Any computed cycle/lifetime point total on Notion side under-reports the real balance.
- The user reconciles point balances against the bank's actual statement, not against the Notion formula, on this card specifically.
- There is no need to "fix" this in Notion. The phase-2 app models points as a numeric `RewardRule.value` (no integer constraint) — see [[../future-app/data-model-target]] — which closes the gap. Until the migration, the Notion side stays approximate and the user keeps Lotus's Beyond point-totals in their head.

This limitation is catalogued in [[../concepts/known-divergences]]. See also [[../concepts/points-and-multipliers#approximation-caveat]].

## See also

- [[_stubs|Card stub index]]
- [[../concepts/points-and-multipliers]] — explains the Notion enum + its limitations.
- Memory: `project_points_earning_complexity` — the cross-card framing.
