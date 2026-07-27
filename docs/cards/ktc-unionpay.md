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

- **Supermarket exclusion** (per user, 2026-07-22): supermarket-category purchases earn **no points** on this card. `JAMPHA SAVEMART CO.,LTD. CHIANGMAI TH` is the confirmed example. Mark such rows `×0` and write a `Note` explaining why — `"Supermarket — KTC UnionPay earns no points on supermarket purchases."` — per [[../concepts/promotions|the exclusion-Note convention]].
- The exclusion is stated **for this card specifically**; behaviour on other KTC products is unknown. First confirmed on Baiboon's card — assumed to hold on Nuta's KTC UnionPay too (card-level rule), but not yet independently observed there.
- **Cashback** is not yet established on this card. Leave `% cb` **unset** on every row until the user documents a KTC UnionPay promo (never write an explicit `0`).
- General-spend base points rate (baht per point) is **not yet characterized** — capture it here when a statement or the user confirms it.

## Billing cycle

KTC pattern: **bill cuts on the 27th, due ~15 days later** (e.g. cycle `2026-07-27` → due `2026-08-11`). See [[../concepts/bill-cycle-patterns|bill-cycle-patterns]]. `/add-transaction` infers this pair automatically when the dates are omitted.

## Notion / classification encoding

**Not machine-applied.** There is no `scripts/repositories/cards/ktc-unionpay.yaml` and no promotion YAML, so `auto_classify` won't touch these rows — classify supermarket rows **by hand** (`multiplier: ×0` + explanatory `Note`). Promote to a repository card/promo file if KTC UnionPay's rules grow enough to warrant machine classification (cf. [[ttb-so-smart|ttb so smart]]'s two-file encoding).

## See also

- [[_stubs|Card stub index]]
- [[../concepts/promotions]] — the promotion-driven cashback / exclusion model.
- [[../concepts/bill-cycle-patterns]] — the KTC 27th-cut pattern.
- Memory: `project_card_ktc_unionpay`.
