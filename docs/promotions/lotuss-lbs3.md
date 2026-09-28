---
tags: [promotion, lotuss]
---

# Lotus's LBS3 — "ช้อปของใหญ่จัดเต็ม" (Sep–Dec 2026)

Lotus's credit card cashback on big-ticket categories: home décor and building materials, electrical appliances, car service, and Makro through every channel. It's pooled per calendar month on Takumi's Lotus's Beyond account, supplements included. Tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] from September 2026 (user, 2026-09-29).

> **Structured source of truth**: `scripts/python/lib/bureau/lbs3.py` (`LBS3Promotion`).

- **Only the single highest tier pays** ("เพียงระดับสูงสุดระดับเดียวเท่านั้น"):
  - ฿80 per whole ฿5,000, at most 4 (฿320);
  - or ฿500 per whole ฿30,000, at most 5 (฿2,500);
  - or ฿3,500 from ฿300,000.

  So ฿29,999 earns ฿320 and ฿30,000 earns ฿500.
- **Caps**: ฿3,500 a month and ฿14,000 for the campaign, per primary account.
- **Excluded**:
  - anything sold by Lotus's, and every other supermarket and convenience store (Makro excepted);
  - marketplaces and wallets;
  - Boots, Watsons and direct sales;
  - installments;
  - foreign and foreign-registered merchants.
- **Registration** counts from the registration day (UCHOOSE or SMS `LBS3`).
- **LMK2** isn't tracked: ฿5,000 for the first 100 accounts past ฿800,000 at Makro PRO.
- **`% cb` is left unset**, as on every Lotus's row. The money goes in the Bureau and trackers.
- **Coins vs cashback**: `WWW.MAKRO.PRO` (MCC 5199) earns no Lotus's coins, but does count toward LBS3.

Source, read 2026-09-29: <https://www.lotussmoney.com/promotion/credit-card/shopping/cashback-nationwide-bigticket>.
