---
tags: [promotion, bangkok-bank, unionpay]
---

# BBL UnionPay 2%: all-spend cashback (1 Jul 2026 – 30 Jun 2027)

Bangkok Bank's standing offer on its UnionPay credit card. Takumi opened the card (`BBL UnionPay`, UnionPay Platinum) in November 2026 with a supplement for Baiboon (user, 2026-11-26). Nuta holds none. It is tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] as `<year>M<month> — BBL UnionPay cb 2%`, one row per calendar month.

> **Structured source of truth**: `scripts/python/lib/bureau/bbl_unionpay.py` (`BBLUnionPayCashback`, a `CreditCapPromotion` with a monthly minimum).

## Terms

From the [card page](https://www.bangkokbank.com/th-TH/Personal/Cards/Credit-Cards/Bangkok-Bank-UnionPay-Credit-Card), read on 2026-10-01 ([[../catalogues/2026-10/all-spend|October all-spend research]]) and again for the [[../catalogues/2026-11/all-spend|November research]]. A re-read on 2026-11-26 timed out from this machine, so the user saved the page as a PDF, and its full terms were checked line by line on 2026-11-27. They matched the earlier readings. The PDF added the details below: TC 30/31, the posting date taken from the principal's statement, the 4% offer's own cap, the general terms and the fee waiver.

| Spend in the month (principal + supplement) | Cashback credit |
|---|---|
| under ฿2,000 | nothing |
| ฿2,000 or more | **2% of all of it** |
| cap | **฿1,000 a month per customer** (reached at ฿50,000); ฿12,000 for the programme (12 × ฿1,000, so never binding alone) |

The window is 1 Jul 2026 to 30 Jun 2027, up to 23:59 on the last day.

- **What counts:** spend in Thailand and abroad except China, online and in store. No registration is needed.
- **Not counted** (with the MCCs the bank names):
  - Alipay and WeChat Pay;
  - spending in China;
  - securities and funds (MCC 6211);
  - insurance (MCC 5960, 6300, 6381, 6399);
  - cash advances (MCC 6010, 6011, or TC 30, 31);
  - interest (TC 11–13) and fees of every kind (MCC 6012, 4829);
  - fines (MCC 9222);
  - tax (MCC 7276, 9311);
  - Bangkok Bank installments (Be Smart, which UnionPay cards can't use anyway);
  - cancelled charges, and goods returned later (TC 41, 43);
  - foreign-currency purchases (`รายการซื้อเงินตราต่างประเทศ`).

  A tourist tax refund (`ภาษีเพื่อการท่องเที่ยว (Tax refund)`) is taken off the month's spend. Fuel, supermarkets, Makro PRO, Shopee and TrueMoney payments all count: the terms name no other e-wallet than Alipay and WeChat Pay.
- **China:** a separate **4%** once spending in China in CNY reaches ฿5,000 a month. Online spend and THB-billed spend in China don't count toward it. It has its own cap: ฿1,000 a month and ฿12,000 for the programme. The terms state each offer's cap separately and don't say whether the two are shared. Not modelled: the household has no China spend on this card.
- **Foreign spend** is converted at the rate of its posting date, as printed on the **principal** card's statement.
- **Crediting:** within 60 days after the statement date (`ภายใน 60 วันหลังจากสรุปยอดบัญชี`), against the card balance. Some conditions apply:
  - The credit can't be cashed out or transferred to anyone else.
  - It goes only to a cardholder who still holds the card and has no missed payment or breach of the card terms up to the day it's credited.
  - The bank can take it back if a qualifying charge is cancelled later.
- **Points:** Thank You Rewards, 1 point per ฿25 at home and abroad. The terms list the points and the cashback side by side and never say one replaces the other, so rows keep earning points (`บาทต่อ 1 คะแนน` = 25 on both Cards rows). Bangkok Bank Titanium's terms, by contrast, give cashback instead of points.
- **Annual fee:** waived in the first year, and in later years once the card is used for ฿5,000 in a year.

## How the household reads it

- **One quota per month for Takumi's account.** Takumi's and Baiboon's rows pool, and the bank credits Takumi's card. Baiboon's share is paid to her like the other primary-card credits ([[../concepts/promotion-bureau|trackers]]).
- **Calendar month by transaction date** is an assumption. The terms say only "a month" (`ต่อเดือน`), and the card's statement closes on the 10th. The full PDF (2026-11-27) doesn't settle this either. If the first statement shows the bank counting by statement cycle, switch the class to `period_basis = "bill_cycle"`.
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
