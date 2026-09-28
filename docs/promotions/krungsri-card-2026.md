---
tags: [promotion, krungsri]
---

# Krungsri Card campaigns, 2026 — ONQ3, SUP1, PTT2, EAT, Bangchak/BC3P, J Dining, NOW online

Krungsri caps its card campaigns **per primary card account**, and each card product is its own account with its own registration and its own cap. September 2026 shows it: SUP1 paid ฿120 on each of Krungsri VISA, JCB, Lady and NOW. Every household Krungsri card is registered for every campaign and tracked per card (user, 2026-09-29). So the [[../concepts/promotion-bureau|Promotion Bureau]] keeps **one row per card per period**, e.g. `2026M9 — SUP1 Krungsri JCB cb 3%` (`CardAccount`, `lib/bureau/accounts.py`). Tracked from September 2026.

Krungsri rows never carry `% cb`. The bank credits each campaign as its own statement line (`CB15_ SUP1 CAMPAIGN …`, `CB12_BC3P CAMPAIGN …`, `CB22_EAT_10MASS DN …`, `CB <merchant>`), and the household books that line as a row. So every class here writes the Bureau and the trackers only (`marks_rows = False`).

> **Structured source of truth**: `scripts/python/lib/bureau/` — `onq3.py`, `sup1.py`, `ptt2.py`, `eat.py`, `bangchak.py`, `jdining.py`, `krungsri_now.py`.

| Campaign | Cards | Period | Pays | Cap per account |
|---|---|---|---|---|
| **ONQ3**, online shopping | VISA, JCB, Lady (NOW excluded) | 7 Aug – 30 Nov | one amount per month: ฿40 from ฿3,000, ฿170 from ฿15,000, ฿350 from ฿30,000 at Lazada, Shopee, TikTok Shop, LINE SHOPPING, and card payments through TrueMoney, LINE Pay and ShopeePay | ฿350/month |
| **SUP1**, supermarkets | VISA, JCB, Lady, NOW | 1 Aug – 31 Oct | per slip at Big C, Tops, Gourmet, Go Wholesale, Makro PRO: ฿35 (฿1,500–3,999) or ฿120 (฿4,000+) | ฿120/month |
| **PTT2**, PTT Station | VISA, JCB, Lady, NOW | 1 Jul – 31 Oct | per slip: ฿30 (฿900–1,199) or ฿60 (฿1,200+) | ฿90/month |
| **EAT** (the household's "DN"), dining | VISA, JCB, Lady, NOW | 1 Jul – 31 Oct | ฿100 for the month's first slip of ฿1,000+ at a participating restaurant, +฿100 at the third | ฿200/month |
| **Bangchak** 1% (card benefit, no registration) | VISA, JCB, Lady (NOW excluded) | 1 Jun – 30 Sep | ฿8 per whole ฿800 on each Bangchak slip ("1%"), BSRC stations included | ฿32/**statement cycle** |
| **BC3P** (Bangchak ต่อ 2) | VISA, JCB, Lady | 1 Jun – 30 Sep | ฿24 per whole ฿800 on each Bangchak slip | ฿48/month |
| **J Dining** | JCB | 1 Jan – 30 Sep | ฿30 per whole ฿1,000 on each restaurant slip, worldwide | ฿150/month |
| **NOW** online (card benefit) | NOW | 1 Jan – 31 Dec | ฿25 per whole ฿500 on each online slip | ฿300/month |

SUP2 (฿700 at ฿60,000 a month) isn't registered on any card (user).

## Readings

- **Fixed amounts per slip.** SUP1, PTT2, BC3P, the Bangchak 1%, J Dining and NOW pay per slip, never on a sum (`SlipCreditPromotion`); the month's cap is claimed first come, first served. EAT counts slips (`SlipCountPromotion`): the first and third qualifying slips of the month earn ฿100 each.
- **Restaurants and online shops.** Neither can always be told from the merchant string. EAT, J Dining and NOW link only names they recognise. A row the household links by hand counts, as long as it clears the minimum slip.
- **Bangchak comes in two parts, both from ฿800 a slip.** The card's own "1%" is ฿8 per whole ฿800 of a slip, so a ฿600 fill-up earns nothing. The bank's `BANGCHAK SPECIAL DISCOUNT OF 1 %` lines show it: ฿800 gave −฿8, and ฿970 gave −฿8 rather than ฿9.70. It's capped per statement cycle, not per month, and credited within the cycle. BC3P is capped per calendar month. Both withhold the card's normal points, as `KrungsriPetrolCampaign` already does. BSRC-branded stations count: August's `CB12_BC3P` ฿24 on Baiboon's JCB came from `BSRC-PHAAPOOM` ฿800.
- **Stacking.** SUP1 and NOW both paid on Baiboon's ฿4,159 Makro PRO slip on Krungsri NOW (฿120 + ฿200). J Dining and EAT both paid on the ฿1,342 Sushiro slip (฿30 + ฿100).

## September 2026 (reconciled with Baiboon's hand-made trackers)

| Row | Split | Baiboon's tracker |
|---|---|---|
| SUP1 VISA / JCB / Lady / NOW | ฿120 each (Baiboon) | ฿120 each, ticked ✓ |
| ONQ3 VISA | ฿40 (Baiboon, Shopee) | `Shopee ONQ3` ฿40 ✓ |
| EAT JCB | ฿100 (Sushiro) | `DN 10%` ฿100, ticked ✓ |
| J Dining JCB | ฿30 (Sushiro) | ฿30, ticked ✓ |
| NOW | ฿200 (Makro PRO ฿4,159) | `NOW 5%` ฿200, ticked ✓ |
| BC3P JCB | **฿48**: 14 Sep ฿970 → 24, 26 Sep ฿1,350 → 24; 20 Sep ฿600 is under ฿800 | `BC3P 3%` **฿32**, ticked — left alone, flagged |
| Bangchak 1% JCB, cycle billed 5 Oct | **฿16**: ฿8 each for 14 and 26 Sep; not 20 Sep's ฿600 | `Bangchak 1% 1–30 Sep` **฿32**, ticked — left alone, flagged |

The two flagged ones need a look at the October statement. ฿32 is the Bangchak 1% cap, not BC3P's. The bank had already credited ฿8 of the 1% by 15 Sep (`BANGCHAK SPECIAL DISCOUNT OF 1 %`, for 14 Sep). The sync leaves a ticked tracker as it is and only warns.

Sources, read 2026-09-29: <https://www.krungsricard.com/th/promotion/online-shopping-cashback>, <https://www.krungsricard.com/th/promotion/supermarket-shopping>, <https://www.krungsricard.com/th/promotion/ptt>, <https://www.krungsricard.com/th/promotion/dining-cashback-deal>, <https://www.krungsricard.com/th/promotion/bangchak>, <https://www.krungsricard.com/th/product/creditcard/krungsri-jcb> (J Dining, from the user), <https://www.krungsricard.com/th/product/creditcard/now>.
