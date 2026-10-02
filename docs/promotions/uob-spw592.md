---
tags: [promotion, uob]
---

# UOB SPW592 — "ช้อปซูเปอร์ ยิ่งจ่าย ยิ่งคุ้ม" (supermarkets, Jul–Dec 2026)

A UOB supermarket campaign paid on the cardholder's pooled monthly spend, across every UOB card Takumi holds and every supplement on them, **except UOB Makro**. **Not registered** (user, 2026-10-01): the class is ready in the [[../concepts/promotion-bureau|Promotion Bureau]] (one row per month, `<year>M<month> — SPW592 cb ฿50/150`), but no rows exist, so nothing links to it. Register (SMS `SH`) and create the month's row with `/sync-promotion` to start tracking. July to September had only a few hundred baht of qualifying UOB spend, far under ฿4,000.

> **Structured source of truth**: `scripts/python/lib/bureau/spw592.py` (`SPW592Promotion`, a `LadderPromotion`).

- **Campaign**: `2026-07-01` → `2026-12-31`. Register once before spending, within the month you join: SMS `SH <last 12 digits>` to 4545111, or Rewards+ in UOB TMRW. Ref 26UC15.
- **Pays**: ฿50 at ฿4,000–9,999 a month, ฿150 from ฿10,000. One amount for the band reached; slips add up. At most ฿150 a month and ฿900 for the campaign (6 × ฿150).
- **Stores** (MCC 5411/5499), in store: Big C, Big C Mini, Don Don Donki, Foodland, Gourmet Market, GO Wholesale (`CFW-…`), Home Fresh Mart, Lotus's (PRIVÉ, go fresh), Mitsukoshi Depachika, No Brand, Rimping, Tops (Food Hall, Daily, Care), Villa Market.
- **Online**: only paid by card on Big C online, Freshket, GO Wholesale, Lotus's Shop Online, Tops Online and Villa Market Online.
- **Not**: Makro (not a participating store), e-wallet payments (`TMN LOTUS HYPER`), shops renting space inside, cash on delivery, bill payments, gift cards and top-ups, UOB i-Plan installments, cancelled charges.
- **Crediting**: within 60 days after the month, to a primary card the bank picks.
- **An overlay**, like [[uob-epw538|EPW538]]: UOB One rows keep UOB One's own `% cb`, and the ฿50/฿150 lives in the trackers (`marks_rows = False`). The bank says it can't combine with other promotions, and that only the best of overlapping promotions in a category pays. Whether it treats UOB One's own cashback as one is unknown.
- The page's second part redeems UOB Rewards points for 10% (`SP`, every time). UOB One is excluded from it, and it isn't tracked.

Source, read 2026-10-01: <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/super-spw592-1226.page> (terms in `…/super-spw592-1226.json`).
