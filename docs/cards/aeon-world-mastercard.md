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

## Cancelled orders, late posting and credit balances

A cancelled order's refund doesn't name the merchant: it reads `REFUND TRANSACTION`, for the order's amount. The 10 Oct 2026 statement shows three quirks at once:

- **Purchases post one to four days late.** AEON prints both dates (`06/10/2026 08/10/2026 …`), and the bill follows the posting date. Rows dated in the last days before the 10th often bill on the next cycle. Baiboon's two `HTTPS://WWW.MAKRO.PRO/` orders of 10 Oct, Nuta's Alipay ฿755.48 of 10 Oct, and Takumi's MRT, `BANGKOK SMARTCARD SYSTEM` and LINEPAY rows of 9–10 Oct weren't on it. They were moved to the 10 Nov cycle (user, 2026-10-21).
- **A refund can post before its charge.** `REFUND TRANSACTION 15,807.50` is printed on 01/10, on the 10 Oct statement. It refunds Baiboon's cancelled `HTTPS://WWW.MAKRO.PRO/` ฿15,982.50 order of 10 Oct, which posted 12 Oct on the 10 Nov cycle. AEON's call centre named the order and its posting date (2026-10-21), and the user named the amount (2026-11-01). The refund is ฿175 less than the order, and the app still counts the order in full. On 1 Nov the app showed ฿16,349.22 of credit used: the 10 Oct statement's −฿15,701.78 plus both 10 Oct orders (฿16,068.50 + ฿15,982.50). The order is `×0` like its refund, and each Note names the other. The 10 Nov statement will show whether the last ฿175 comes back.
  - From 2026-10-20 to 2026-11-01 the ledger held a separate ฿15,807.50 "cancelled order", sized to match the refund. The app never showed it, and it was archived on 2026-11-01. A −฿15,982.50 cancellation row went with it, since it would have counted the refund twice.
- **A credit balance prints as `0.00 Baht` due.** That refund left AEON World at −฿15,701.78. The parser rebuilds the signed figure from `BALANCE BROUGHT FORWARD` + the card's `SUBTOTAL`. The statement's lines stay in their own cycle, and a `[ยอดยกมาจากรอบ 2026-10]` pair carries the credit across (user, 2026-11-01). Its +฿15,701.78 leg is on the 10 Oct cycle, which then nets to ฿0 and gets no bill. Its −฿15,701.78 leg is on the 10 Nov cycle, where the 10 Nov statement prints the credit as `BALANCE BROUGHT FORWARD`. Both legs are `×0`. Baiboon's four lines on the 10 Oct statement are the refund, `ANTHROPIC* CLAUDE SUB` ฿725.72 and the two `CASH BACK - CREDIT CARD PROMOTION` credits (−฿120, −฿500). Her 10 Nov cycle is ฿16,349.22 before any new lines, the app's figure. From 2026-10-30 to 2026-11-01 those four lines were billed on the 10 Nov cycle instead, with no pair. See [[../databases/takumi-bills#Credit balances|takumi-bills → Credit balances]].

The [[../concepts/promotion-bureau|Bureau]] can't pair a `REFUND TRANSACTION` with its charge: the line doesn't match the supermarket patterns of AEON WM 5% or NTW1. So this refund is linked by hand to NTW1's `2026M10`, where it nets off Baiboon's other charges in the period (`net_refunds`): 11 Sep–10 Oct counts ฿16,243.50, under ฿30,000, so NTW1 pays ฿120 (user, 2026-11-01). The terms exclude cancelled charges. AEON's call centre had quoted ฿340 on 2026-10-24, which counts both orders in full. AEON's NTW1 credit for that period will confirm it. The sync flags the linked refund as "not counted", which is informational only. AEON WM 5%'s `2026M10` doesn't link it (฿32,051), since 5% of either figure is over the ฿500 cap. NTW1 counts by transaction date (AEON's call centre, 2026-10-24). The same statement's ฿120 is NTW1 for 11 Aug–10 Sep, not a reduced credit for the cycle closing 10 Sep as this note first guessed. See [[../promotions/aeon-2026#NTW1 by transaction date (2026-10-24)|aeon-2026]].

## See also

- [[_stubs|Card stub index]]
- [[kbank-plustinum]] — Baiboon's other Makro card.
