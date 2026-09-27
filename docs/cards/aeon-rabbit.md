---
tags: [card, aeon, points]
issuer: AEON
holders: [takumi]
points: none-since-2025-11-11
---

# AEON Rabbit

Takumi's own card (statement number `9908`), Platinum tier. Standard AEON cycle: bill cycle day 10, due day 2 of the next month.

## No reward points since 11 Nov 2025

AEON [stopped awarding points](https://www.aeon.co.th/aeon/news-events/notification-rabbit-platinum-credit-card-2025) on AEON Rabbit Platinum for **every** transaction from 11 Nov 2025. Rows before that still earn at `บาทต่อ 1 คะแนน = 20`.

- Encoded as `points_excluded_merchants: [{prefix: "*", effective_from: 2025-11-11}]` in `scripts/repositories/cards/aeon-rabbit.yaml`, so `/record-statement` gives every new row `×0` with the Note `AEON Rabbit earns no reward points on any transaction since 11 Nov 2025.`
- Takumi reset the card's points with `Reset ยอดใช้จ่ายและคะแนน` on 2026-09-22 (see [[../concepts/ledger-reset]]) and adjusts that balance by hand. On 2026-09-28, the 56 statement charges recorded after the reset (all dated from 11 Nov 2025) were set to `×0`.

## Cashback

AEON Rabbit Platinum's [standing benefits](https://www.aeon.co.th/aeon/cards/aeon-rabbit-platinum-card) (user, 2026-09-28):

| Channel | Merchant string | Cashback |
|---|---|---:|
| LINE Pay | `LINEPAY*LP_LINEPAY BANGKOK`, `LINEPAY*LP_LINE MAN WO BANGKOK` | 5% |
| Rabbit card auto top-up (BTS) | `BANGKOK SMARTCARD SYSTEM` | 5% |
| MRT Purple Line card top-up | not seen yet | 1% |

- **Caps:** ฿50 cashback per transaction and ฿1,000 per primary card per cycle.
- **Excluded:** digital-wallet top-ups.
- **Paid as:** `CASH BACK - CREDIT CARD PROMOTION`, credited within 2 billing cycles.
- **Encoded in:** `scripts/repositories/promotions/aeon-rabbit-cashback.yaml` (5% tier). The 1% tier waits for a real merchant string, and the caps aren't enforced.
- **Applied:** on 2026-09-28, Takumi's DS gained `% cb` / `cashback`, and the 56 rows since the restart were set to 5% (฿100.75 on the 2026-09-10 cycle).
- **Not double counting:** the formula is the expected cashback; the bank's actual credit arrives later as its own row.

AEON's wider MCC exclusions (see [[aeon-world-mastercard]]) are covered by this card-wide rule anyway.

## See also

- [[_stubs|Card stub index]]
- [[aeon-world-mastercard]]
