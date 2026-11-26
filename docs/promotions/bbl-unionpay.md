---
tags: [promotion, bangkok-bank, unionpay]
---

# BBL UnionPay 2%: all-spend cashback (1 Jul 2026 – 30 Jun 2027)

Bangkok Bank's standing offer on its UnionPay credit card. Takumi opened the card (`BBL UnionPay`, UnionPay Platinum) in November 2026 with a supplement for Baiboon (user, 2026-11-26). Nuta holds none. It is tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] as `<year>M<month> — BBL UnionPay cb 2%`, one row per calendar month.

> **Structured source of truth**: `scripts/python/lib/bureau/bbl_unionpay.py` (`BBLUnionPayCashback`, a `CreditCapPromotion` with a monthly minimum).

## Terms

Read from the [card page](https://www.bangkokbank.com/th-TH/Personal/Cards/Credit-Cards/Bangkok-Bank-UnionPay-Credit-Card) on 2026-10-01 ([[../catalogues/2026-10/all-spend|October all-spend research]]) and again for the [[../catalogues/2026-11/all-spend|November research]]. A re-read on 2026-11-26 timed out from this machine.

| Spend in the month (principal + supplement) | Cashback credit |
|---|---|
| under ฿2,000 | nothing |
| ฿2,000 or more | **2% of all of it** |
| cap | **฿1,000 a month per customer** (reached at ฿50,000); ฿12,000 for the programme (12 × ฿1,000, so never binding alone) |

- **What counts:** spend in Thailand and abroad except China, online and in store. No registration is needed.
- **Not counted** (with the MCCs the bank names):
  - Alipay and WeChat Pay;
  - spending in China;
  - securities and funds (MCC 6211);
  - insurance (MCC 5960, 6300, 6381, 6399);
  - cash advances (MCC 6010, 6011);
  - interest (TC 11–13) and fees (MCC 6012, 4829);
  - fines (MCC 9222);
  - tax (MCC 7276, 9311);
  - Bangkok Bank installments (Be Smart, which UnionPay cards can't use anyway);
  - cancelled charges and refunds (TC 41, 43);
  - foreign-currency purchases. A tax refund comes off the spend.

  Fuel, supermarkets, Makro PRO, Shopee and TrueMoney payments all count.
- **China:** a separate **4%** on ฿5,000+ a month spent in China in CNY (not online), inside the same ฿1,000. Not modelled: the household has no China spend on this card.
- **Foreign spend** is converted at the posting date's rate.
- **Crediting:** within 60 days after the statement date (`ภายใน 60 วันหลังจากสรุปยอดบัญชี`), against the card balance.
- **Points:** Thank You Rewards, 1 point per ฿25 at home and abroad. The page doesn't say the cashback replaces them, so rows keep earning points (`บาทต่อ 1 คะแนน` = 25 on both Cards rows).

## How the household reads it

- **One quota per month for Takumi's account.** Takumi's and Baiboon's rows pool, and the bank credits Takumi's card. Baiboon's share is paid to her like the other primary-card credits ([[../concepts/promotion-bureau|trackers]]).
- **Calendar month by transaction date** is an assumption. The page says "a month", and the card's statement closes on the 10th. If the first statement shows the bank counting by statement cycle, switch the class to `period_basis = "bill_cycle"`.
- **Below ฿2,000 nothing earns.** Every row that month has `% cb` unset. Once the month passes ฿2,000, the next sync gives every row in it 2%, first come, first served, until the ฿1,000 runs out. The row the cap runs out on, and every row after it, has `% cb` unset.

## Changes from NW4, UOB One 1% and ttb so smart 1%

No earlier round of this programme is in the vault. Compared with the household's other all-spend cashback:

- **Rate:** a flat 2% of the whole month once it reaches ฿2,000.
  - NW4: ฿50 at ฿5,000–9,999, then ฿200 per whole ฿10,000.
  - UOB One and ttb so smart: 1% from the first baht.
- **Cap:** ฿1,000 a month.
  - NW4: ฿2,000 a month.
  - UOB One 1% and ttb so smart: ฿2,000 a statement cycle.
- **Period:** a calendar month, like NW4 (assumed, see above). UOB One 1% and ttb so smart count by statement cycle.
- **What counts:** fuel, supermarkets, e-wallet payments and foreign spend all count.
  - NW4 leaves out marketplaces, delivery apps, travel, Makro, foreign spend and e-wallet top-ups.
  - UOB One and ttb so smart leave out fuel.
  - ttb so smart also leaves out 7-Eleven and TrueMoney.
- **Registration:** none. NW4 needs it.
- **Crediting:** within 60 days after the statement date, onto the card.
  - NW4: within 60 days after each month-end.
  - UOB One: on the statement.
  - ttb so smart: into a ttb no fixed account.
- **Points:** kept alongside the cashback. UOB One earns none.

## Bureau rows

`2026M11 — BBL UnionPay cb 2%` and `2026M12 — BBL UnionPay cb 2%` were created on 2026-11-26, with no transactions on the card yet. Create each following month's row as the month starts, through `2027M6`.
