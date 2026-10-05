---
tags: [promotion, uob, makro]
---

# UOB Makro 26th anniversary "Gold Mission" — MPW823 / `UMK26` (Oct–Dec 2026)

UOB Makro's 26th-anniversary campaign, for **UOB Makro cardholders only**, 1 Oct – 31 Dec 2026. Every cap is per cardholder, with principal and supplements together. So Takumi's UOB Makro (…1649) and Baiboon's rows on it (her own and the `[บัตรหลัก]` ones) pool. **Registered by Takumi on 2026-10-03** (user). It's tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] with three quotas.

> **Structured source of truth**: `scripts/python/lib/bureau/uob_makro.py`.

| Mission | Class · Bureau row | Pays | Cap |
|---|---|---|---|
| 1 — Makro stores, every branch | `UOBMakroStoreMission` (bands) · `2026M10 — UMK26-1 cb ฿150/800/2,500`, one per month | the month's total: ฿150 from ฿50,000, ฿800 from ฿150,000, ฿2,500 from ฿400,000 | ฿7,500 campaign (never binding alone) |
| 2 — Makro PRO, **in the app** | `UOBMakroProMission` (per slip) · `2026M10 — UMK26-2 cb ฿150/500/1,200`, **one row for the whole campaign** (1 Oct – 31 Dec) | per slip: ฿150 for ฿10,000–29,999, ฿500 for ฿30,000–59,999, ฿1,200 from ฿60,000 | ฿3,600 campaign |
| 3 — other spend | `UOBMakroOtherMission` (band) · `2026M10 — UMK26-3 cb ฿300`, one per month | ฿300 for a month of ≥ ฿10,000 outside Makro | ฿900 campaign (never binding alone) |

- **Bonus**: doing all three missions at least once during the campaign adds a **฿1,000 Makro voucher**, mailed to the principal. All three together pay at most ฿12,000, or ฿13,000 with the voucher. **Draw**: every ฿1,000 on the card is one right for gold bars (4 / 2 / 1 baht) and Makro vouchers. Neither is money in the card account, so the Bureau doesn't track them.
- **Registration**: once, SMS `UMK26 <last 12 digits>` to 4545111, or Rewards+ in UOB TMRW.
- **Not counted**:
  - installments (UOB excludes the not-yet-billed balance; screened as *uncertain*);
  - cash advances and transfers;
  - fuel;
  - UOB Pay Anything;
  - e-wallets (`TMN MAKRO`, Rabbit LINE Pay);
  - gift cards and card top-ups;
  - funds and insurance (MCC 6211);
  - utilities (MCC 4900);
  - supermarkets (MCC 5411);
  - EasyBills (MCC 5999);
  - annual fees, interest, tax refunds and cancellations;
  - cigarettes, alcohol, infant formula and medicines.
- **Reading — MCC 5411**: the exclusion sits in one list shared by all three missions and the draw. Missions 1 and 2 name Makro and Makro PRO outright, so it's applied only to mission 3 (and the draw). `HTTPS://WWW.MAKRO.PRO/` posts as 5411.
- **Reading — app only**: mission 2 counts Makro PRO *app* orders. The statement string can't tell app from web, and the household orders in the app, so every Makro PRO row counts.
- **Crediting**: within 60 days after 31 Dec 2026, to the principal card. Not combinable with other promotions. Whether that touches the card's ×2 points on the 16th (`MMID`) isn't stated.
- **Rows keep `% cb` unset.** The amounts are fixed (`marks_rows = False`); the credit lives in the Bureau shares and the trackers.
- **Rows to create**: November's and December's `UMK26-1` and `UMK26-3` rows when those months start. `UMK26-2` has one row for the campaign.

Source, read 2026-10-03: <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/makro-26th-mpw823-1226.page>. It has no `.json` twin; render it headless.
