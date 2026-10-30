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
- **A refund can post before its charge.** `REFUND TRANSACTION 15,807.50` is printed on 01/10, on the 10 Oct statement. AEON's call centre ties it to a cancelled `HTTPS://WWW.MAKRO.PRO/` order of 10 Oct, posted 12 Oct, which falls in the 10 Nov cycle (2026-10-21). Both rows are `×0`, each Note names the other, and the charge carries `Process Date` 12 Oct. The refund is billed on the 10 Nov cycle with its charge, so the two cancel in one cycle (user, 2026-10-30). The 10 Nov statement will show whether the charge really posts.
- **A credit balance prints as `0.00 Baht` due.** That refund left AEON World at −฿15,701.78. The parser rebuilds the signed figure from `BALANCE BROUGHT FORWARD` + the card's `SUBTOTAL`. The 10 Oct statement has no bill on either side (user, 2026-10-30; see [[../databases/takumi-bills#Credit balances|takumi-bills → Credit balances]]). All four of its lines in Baiboon's ledger bill on the 10 Nov cycle: the refund, `ANTHROPIC* CLAUDE SUB` ฿725.72 and the two `CASH BACK - CREDIT CARD PROMOTION` credits (−฿120, −฿500). Her 10 Nov cycle is ฿32,156.72 before any new lines. The 10 Nov statement brings the −฿15,701.78 forward, and its own lines are her 10 Nov rows less those four. /record-statement will report the four as `not_on_statement`, together −฿15,701.78, which is exactly the brought-forward balance. That is expected, not drift.

The [[../concepts/promotion-bureau|Bureau]] can't pair a `REFUND TRANSACTION` with its charge. The line doesn't match the supermarket patterns of AEON WM 5% or NTW1, so it isn't netted, and a cancelled charge still counts as spend there. The bank does net it. For NTW1 this one makes no difference. NTW1 counts by transaction date (AEON's call centre, 2026-10-24), and the cancelled order (10 Oct) and its refund (1 Oct) both fall in 11 Sep–10 Oct. That period clears ฿30,000 without them, so it pays ฿340. The same statement's ฿120 is NTW1 for 11 Jul–10 Aug, not a reduced credit for the cycle closing 10 Sep as this note first guessed. See [[../promotions/aeon-2026#NTW1 by transaction date (2026-10-24)|aeon-2026]].

## See also

- [[_stubs|Card stub index]]
- [[kbank-plustinum]] — Baiboon's other Makro card.
