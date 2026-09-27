---
tags: [card, aeon, points, makro]
issuer: AEON
holders: [takumi, baiboon]
points: integer
---

# AEON World Mastercard

Takumi's primary card (statement number `5201`). Baiboon uses it through `[บัตรหลัก]` rows on [[../databases/baiboon-cards|her Cards DB]], mostly for Makro PRO orders. It is a **points** card: 1 point per 30 ฿ (`บาทต่อ 1 คะแนน = 30`), with no cashback programme. AEON's own cashback credits (`CASH BACK - CREDIT CARD PROMOTION`) go to whoever earned them; see [[../databases/takumi-bills]].

## AEON's MCC exclusions (from 11 Nov 2025)

AEON's [notification](https://www.aeon.co.th/aeon/news-events/notification-aeon-credit-cards-2025) withholds reward points on every AEON credit card except Big C:

| From | Excluded |
|---|---|
| 2025-11-11 | A list of MCCs, including **5199** (non-durable goods). **5411** (supermarkets) is not on it. |
| 2025-12-11 | Some foreign-registered merchants (EU/EEA, China, UK) |
| 2026-01-11 | 0% installment transactions |

A merchant string doesn't show its MCC, so only strings known to bill under an excluded code are encoded (user, 2026-09-28):

| Merchant string | MCC | Points |
|---|---|---|
| `WWW.MAKRO.PRO BANGKOK TH` | 5199 | **`×0`**, with Note |
| `HTTPS://WWW.MAKRO.PRO/ BANGKOK TH` | 5411 | earns normally (`×1`) |

The two strings are both Makro PRO, but the bank files them under different codes. Encoded as `points_excluded_merchants` in `scripts/repositories/cards/aeon-world.yaml`, so `auto_classify` and `/record-statement` apply it. On 2026-09-28 five past rows (Baiboon, 27 Jul–12 Aug 2026) were set to `×0`. The foreign-merchant and installment exclusions are not encoded yet.

## See also

- [[_stubs|Card stub index]]
- [[kbank-plustinum]] — Baiboon's other Makro card.
