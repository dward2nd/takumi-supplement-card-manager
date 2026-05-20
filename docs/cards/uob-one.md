---
tags: [card, uob, points-0x, cashback]
issuer: UOB
holders: [takumi, baiboon, nuta]
points: none
---

# UOB One

UOB's flagship cashback card. Takumi holds the primary; Baiboon and Nuta each carry a supplement card on the same account.

## Points

**This card earns no Notion-tracked points.** Every transaction written on a UOB One row gets the `×0` multiplier checked.

The card's "rewards" exist purely as cashback — there is no underlying points balance to redeem, so the `คะแนนที่ได้จริง` / `คะแนน unrealized` formulas always evaluate to zero on these rows. See [[../concepts/points-and-multipliers]] for how the multipliers feed the formulas (link will resolve once promoted from [[_stubs|the stub index]]).

## Cashback tiers

Cashback is computed as `% cb` × `ยอดชำระ`. The `% cb` field is **only present on Nuta's Transactions DS** ([[../databases/nuta-transactions]]); for Baiboon and Takumi UOB One transactions, we record the tier mentally / in `Note` but don't write a percent value.

The tiers, in priority order (first match wins):

| Tier | Rate | Merchant patterns                                                                                  |
|------|-----:|----------------------------------------------------------------------------------------------------|
| 10%  | 0.10 | BTS, MRT, AMZ                                                                                       |
| 5%   | 0.05 | `7-11` (the standalone string only — see carve-out below), WATSON, GRAB *Thailand only* (`WWW.GRAB.COM`, `GRABTAXI`) |
| 1%   | 0.01 | everything else not excluded                                                                        |
| 0%   | 0.00 | excluded transactions — see [[#General earning exclusions]]                                         |

### Carve-outs

- **TMN 7-11 ≠ 7-11.** The `TMN 7-11 BANGKOK TH` merchant string is a TrueMoney top-up performed at a 7-Eleven counter. It does **not** qualify for the 5% 7-11 tier. Falls through to 1%.
- **GRAB is Thailand-only.** Cross-border `GRAB` charges from neighbouring countries (e.g. `GRAB*SG`) drop to 1%. Confirm by country suffix in the merchant string.

## General earning exclusions

These apply on top of the tier table — they override the tier with `0%`:

1. **Foreign merchants billed in THB.** Country suffix in the merchant string (`US`, `USA`, `JP`, `SG`, etc.) is the tell. Example in the data: `X CORP. PAID FEATURES BASTROP US`. Whenever this rule fires on a UOB One row, the matching transaction page **must** carry a `Note` explaining "foreign merchant in THB — no cashback" (see [[../../.claude/skills/add-notion-transaction/SKILL]] rule 4c).
2. **UOB cards at petrol stations.** Strings containing `PT`, `BCP`, `ESSO`, `SHELL`, `CALTEX`, `PTT` typically fall here — confirm against the actual fuel merchant when in doubt. Same Note requirement.

The Notion formulas can't distinguish these cases from regular domestic THB charges, so the explicit `% cb = 0` and `Note` are how the data stays honest.

## Writing UOB One transactions

Always go through the [[../../.claude/skills/add-notion-transaction/SKILL|add-notion-transaction]] skill. The relevant fields:

- `multiplier: "×0"` — at batch level for the whole UOB One batch.
- `cashback_percent: <fraction>` — per-tx for Nuta (Baiboon/Takumi omit it). The CLI accepts raw fractions; pass `0.05` for 5%, not `5`.
- `Note: "<reason>"` — only on rows where the cashback is 0% for a reason other than the card's default policy (i.e. the exclusions section above).

## Open questions

- Does Takumi actually hold a UOB One primary? `_stubs.md` lists `?` for Takumi — should be confirmed once Takumi's Cards DB is enumerated.
- What's the monthly cashback cap, and where does it live in Notion? Not yet surfaced.

## See also

- [[_stubs|Card stub index]]
- [[../databases/nuta-transactions]] for the `% cb` / `cashback` schema
- [[../concepts/points-and-multipliers]] (TODO, promote when written) for how `×0` interacts with `คะแนนที่ได้จริง`
