---
tags: [card, ktc, points]
issuer: KTC
holders: [baiboon, nuta]
points: integer
---

# KTC UnionPay

KTC's UnionPay-network card, held by both [[../people/baiboon|Baiboon]] and [[../people/nuta|Nuta]]. It is a **points card**, but with a confirmed **category carve-out**: it earns **no points on supermarket transactions**.

## Earning rules

| Where | Points | Cashback |
|---|---|---|
| Supermarket merchants (e.g. `JAMPHA SAVEMART …`) | **none — `×0`** | not established — leave `% cb` unset |
| General spend | earns points (base rate not yet characterized — no multiplier / default `×1`) | not established — leave `% cb` unset |
| Fast food (MCC 5814), e.g. `CNX BC DOM L2 LS(6110) CHIANGMAI THA` = Bonchon at Chiang Mai airport | **none — `×0`** (by hand; the name doesn't show it) | not established |
| Petrol (`BANGCHAK …`, `BSRC-…`) | **earns** — confirmed on the 2026-09-27 …1346 statement | not established |

- **Supermarket exclusion** (per user, 2026-07-22): supermarket-category purchases earn **no points** on this card. `JAMPHA SAVEMART CO.,LTD. CHIANGMAI TH` is the confirmed example. Mark such rows `×0` and write a `Note` explaining why — `"Supermarket — KTC UnionPay earns no points on supermarket purchases."` — per [[../concepts/promotions|the exclusion-Note convention]].
- The exclusion is stated **for this card specifically**; behaviour on other KTC products is unknown. First confirmed on Baiboon's card — assumed to hold on Nuta's KTC UnionPay too (card-level rule), but not yet independently observed there.
- **Cashback** is not yet established on this card. Leave `% cb` **unset** on every row until the user documents a KTC UnionPay promo (never write an explicit `0`).
- Base rate: 1 point per ฿25 (KTC FOREVER), rounded once on the cycle's spend. The full exclusion list (rule 16: supermarkets, bakeries, fast food, public hospitals, cinemas, …) is in [[../promotions/ktc-forever|ktc-forever]]; the Sep 2026 statement pinned Bonchon as fast food and showed petrol earning.

## Billing cycle

KTC pattern: **bill cuts on the 27th, due ~15 days later** (e.g. cycle `2026-07-27` → due `2026-08-11`). See [[../concepts/bill-cycle-patterns|bill-cycle-patterns]]. `/add-transaction` infers this pair automatically when the dates are omitted.

## Notion / classification encoding

`scripts/repositories/cards/ktc-unionpay.yaml` and the `KTCUnionPay` class (`scripts/python/lib/earning/families.py`) encode what the merchant string shows: supermarket names, 7-Eleven / TrueMoney, transport and tolls. MCC-only exclusions (fast food, bakeries, public hospitals) still go `×0` **by hand** with a Note.

## See also

- [[_stubs|Card stub index]]
- [[../concepts/promotions]] — the promotion-driven cashback / exclusion model.
- [[../concepts/bill-cycle-patterns]] — the KTC 27th-cut pattern.
- Memory: `project_card_ktc_unionpay`.
