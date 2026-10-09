---
tags: [card, ktc, points, unionpay]
issuer: KTC
holders: [takumi, baiboon, nuta]
product: KTC UnionPay Diamond
points: integer
---

# KTC UnionPay

KTC's UnionPay-network card: Takumi's principal (…1346) and supplements held by [[../people/baiboon|Baiboon]] (…2310) and [[../people/nuta|Nuta]]. All three are **KTC UnionPay Diamond** since the upgrade (user, 2026-10-02; filed as `สูง (Signature)` in the Cards DBs, name unchanged). KTC FOREVER's rules cover every KTC UnionPay type, so the earning below didn't change. It is a **points card**, but with a confirmed **category carve-out**: it earns **no points on supermarket transactions**.

## Earning rules

| Where | Points | Cashback |
|---|---|---|
| Supermarket merchants (e.g. `JAMPHA SAVEMART …`) | **none — `×0`** | UnionPay QR 6% off, inside the charge — `% cb` unset |
| General spend | earns points (base rate not yet characterized — no multiplier / default `×1`) | UnionPay QR 6% off, inside the charge — `% cb` unset |
| Fast food (MCC 5814), e.g. `CNX BC DOM L2 LS(6110) CHIANGMAI THA` = Bonchon at Chiang Mai airport | **none — `×0`** (by hand; the name doesn't show it) | UnionPay QR 6% off |
| Petrol (`BANGCHAK …`, `BSRC-…`) | **earns** — confirmed on the 2026-09-27 …1346 statement | UnionPay QR 6% off |

- **Supermarket exclusion** (per user, 2026-07-22): supermarket-category purchases earn **no points** on this card. `JAMPHA SAVEMART CO.,LTD. CHIANGMAI TH` is the confirmed example. Mark such rows `×0` and write a `Note` explaining why — `"Supermarket — KTC UnionPay earns no points on supermarket purchases."` — per [[../concepts/promotions|the exclusion-Note convention]].
- The exclusion is stated **for this card specifically**; behaviour on other KTC products is unknown. First confirmed on Baiboon's card — assumed to hold on Nuta's KTC UnionPay too (card-level rule), but not yet independently observed there.
- **Cashback: UnionPay QR 6% off**, monthly from Sep 2026 ([[../promotions/unionpay-qr|unionpay-qr]]). Takumi (…1346) and Baiboon (her own …2310) pay with this card by QR only. UnionPay takes the discount off at payment, so `ยอดชำระ` is already the net amount KTC charged (฿67.68 for a ฿72 price), and nothing is credited later. Leave `% cb` **unset** on every row (never an explicit `0`); the Promotion Bureau's `UnionPay QR …1346` / `…2310` rows track who saved what, and whether the month's pool has run out.
- Base rate: 1 point per ฿25 (KTC FOREVER), rounded once on the cycle's spend. The full exclusion list (rule 16: supermarkets, bakeries, fast food, public hospitals, cinemas, …) is in [[../promotions/ktc-forever|ktc-forever]]; the Sep 2026 statement pinned Bonchon as fast food and showed petrol earning.

## Billing cycle

KTC pattern: **bill cuts on the 27th, due ~15 days later** (e.g. cycle `2026-07-27` → due `2026-08-11`). See [[../concepts/bill-cycle-patterns|bill-cycle-patterns]]. `/add-transaction` infers this pair automatically when the dates are omitted.

## Notion / classification encoding

`scripts/repositories/cards/ktc-unionpay.yaml` and the `KTCUnionPay` class (`scripts/python/lib/earning/families.py`) encode what the merchant string shows: supermarket names, 7-Eleven / TrueMoney, transport and tolls. MCC-only exclusions (fast food, bakeries, public hospitals) still go `×0` **by hand** with a Note.

## See also

- [[_stubs|Card stub index]]
- [[../concepts/promotions]] — the promotion-driven cashback / exclusion model.
- [[../concepts/bill-cycle-patterns]] — the KTC 27th-cut pattern.
- [[../promotions/unionpay-qr]] — the UnionPay QR 6% discount, per card number.
- [[../promotions/unionpay-mrt]] — UnionPay's 15% off MRT fares by contactless tap; this card qualifies, though it's used by QR only.
- Memory: `project_card_ktc_unionpay`.
