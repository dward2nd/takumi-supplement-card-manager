---
tags: [promotion, points, ktc]
---

# KTC FOREVER — how KTC cards earn points

KTC's points programme for every KTC card: Takumi's KTC Digital VISA, KTC JCB and KTC UnionPay (…1346), and Baiboon's own KTC UnionPay (…2310), which gets its own PDF and its own points. The full terms, as the user copied them from KTC on 2026-09-28, are kept verbatim in [[../sources/ktc-forever-terms-2026-09-28.txt|sources/ktc-forever-terms-2026-09-28.txt]]. KTC's website doesn't show them; its pages point to the card networks' MCC manuals.

## Earning

- `ยอดใช้จ่าย … ทุก 25 บาท รับคะแนน 1 คะแนน` (1 point per ฿25 spent), on every KTC Visa, Mastercard, JCB and UnionPay card. 1,000 points are worth ฿100.
- `คะแนน KTC FOREVER จะคำนวณทุกครั้งเมื่อมีรายการ Posting … และปรากฎตามรอบการออกใบแจ้งยอด` (points are calculated as each charge posts, and appear on the statement cycle).
  - On the Aug 2026 statements, flooring the cycle's spend once, `floor(Σ / 25)`, reproduces KTC's figures: Digital VISA 71. Flooring each row gives 65.
  - So [[../../.claude/skills/audit-rewards/SKILL|/audit-rewards]] treats KTC as rounding per cycle, and `/record-statement` adds a `[ปรับคะแนน] ปัดเศษคะแนนรอบบิล` row for the difference.
- Installments earn per term.
- Petrol (MCC 5541/5542) counts only up to ฿30,000 per card per month.

## What earns nothing (terms §2)

| Rule | Cards | What |
|---|---|---|
| (3) | all KTC | 7-Eleven in any channel, including paying through TrueMoney Wallet |
| (9) | all | cash advances, utilities (MCC 4900), funds, unit-linked insurance, interest, penalties, fees, cancelled charges, refunds |
| (10) | all | baht charges at foreign or foreign-registered merchants |
| (11)–(12) | Visa / Mastercard / UnionPay | merchants in the 31 EEA countries; merchants registered in mainland China |
| (16) | **KTC UnionPay** | MCC 8398 charities, 8661 religious bodies, 4899 pay TV, 4900 utilities, **5411 supermarkets and grocers**, 9211/9222/9223/9311/9399/9402/9405 government, 1520 contractors, 4121 taxis, 4215 couriers, 4814 telecom, 5399 general merchandise, **5462 bakeries**, **5499 miscellaneous food shops**, **5814 fast food**, 7832 cinemas, 7999 recreation, **8062 public hospitals**, education (8211, 8220, 8241, 8244, 8249, 8299) |
| (17) | all | public transport and tolls: MCC 4111 (BTS, MRT, ferries), 4112 (SRT), 4131 (BMTA buses), 4784 (Easy Pass / M-Pass expressway tolls); credit card on delivery |
| (2), (4)–(8), (13)–(15) | Mastercard / Visa / Senior | government MCCs, Lotus's go fresh, Makro, TrueMoney-linked cards, payment agents, New Zealand and Japanese travel MCCs, B2B suppliers. None of these are household cards |

## What the classifier knows

The ledger has no MCCs, so only rules that show in the merchant string are encoded (`KTCCard`, `KTCUnionPay` in `lib/earning/families.py`):
- **All KTC cards:** 7-Eleven and TrueMoney (`TMN …`); tolls and public transport (`EXPRESSWAY`, `EASY PASS`, `M-PASS`, `BTS`, `MRT`).
- **KTC UnionPay:** supermarket names (Savemart, Lotus's, Big C, Tops, Rimping and others).

The rest (bakeries, fast food, public hospitals, cinemas, …) depends on the MCC, so those rows get `×0` by hand with a Note, as Baiboon's Savemart rows already have.

## Aug 2026: Baiboon's …2310

KTC paid 61 points. Rounded per cycle, the ledger's `×1` rows give 90 (85 per row, 65 after her own `ปรับคะแนนให้ตรงกับปัจจุบัน` −20 row). So KTC paid nothing on roughly ฿714–738 of that spend. Rule (16) accounts for it:
- `CENTER FOR MEDICAL EXC` ฿423: CMU's public hospital, MCC 8062.
- `BAKERY IN THE ROOM` ฿30: a bakery, MCC 5462.
- Fast-food or food-shop rows (MCC 5814 / 5499) for the rest.

Which food rows those are can't be pinned down without MCCs, so the ledger is left as it is (reconcile, don't correct).

## Sep 2026 statements (2026-09-27)

- **Takumi's …1346:** KTC paid 68. Only one subset of the ×1 lines gives exactly that: `BANGCHAK …` ฿940 + `BSRC-…` ฿686.20 + `AUFU` ฿89.30 = ฿1,715.50 → floor(÷25) = 68. So:
  - **Petrol earns** on KTC UnionPay (up to the ฿30,000 monthly cap). No petrol exclusion on this card.
  - `CNX BC DOM L2 LS(6110) CHIANGMAI THA` (฿478.46) earned nothing. It's **Bonchon**, the fried-chicken chain, at the Chiang Mai airport domestic terminal (user, 2026-09-29): fast food, MCC 5814, rule (16). The airport isn't the reason; no KTC rule names airports, and airport merchants earn elsewhere (`KFC-12335(C.AIRPORT CH …)` at ×5 on another card). Takumi's ฿281.06 and Baiboon's `[บัตรหลัก]` ฿197.40 halves are `×0` with a Note. With them at ×0 the ledger gives 67 + a 1-point cycle-rounding row = 68, exact.
  - The descriptor doesn't say Bonchon (`BC`), so the classifier can't see it. Mark it by hand if it recurs.
- **Takumi's …5549 (Mastercard) and …0581 (Digital VISA):** exact (61 and 0). KTC also moved 2,000 points from 0581 to 5549 and 22 from 1346 to 2310 (`adjusted` on each summary). `/sync-points-balance` set every card to its printed balance.
- **Baiboon's …2310:** KTC paid 50; her rows give 77 once the three lines missing from her ledger were added (BCM LAMPHUN HOSPITAL ฿50, BCM CHAING KAN ฿380 + ฿84). Still open, like August. The Lamphun Hospital rows (฿30, ฿67.68, ฿50) are likely MCC 8062; the rest needs MCCs.
