---
tags: [promotion, krungsri]
---

# Krungsri Card campaigns, 2026 — ONQ3, SUP1, PTT2, EAT, Bangchak/BC3P → BXP, LOTA/LOTB, UNQ, J Dining, NOW online

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

### From October 2026 (read 2026-10-01)

> **Structured source of truth**: `bxp.py`, `lotus_exclusive.py`, and `uniqlo.py` for UNQ ([[uniqlo-2026]]).

| Campaign | Cards | Period | Pays | Cap per account |
|---|---|---|---|---|
| **Bangchak700**, the card's "1%" (no registration) | VISA, JCB, Lady (NOW excluded) | 1 Oct 2026 – 31 May 2027 | ฿7 per whole ฿700 on each Bangchak slip | ฿21/**statement cycle** (฿2,100 of fuel) |
| **BXP** (Bangchak ต่อ 2) | VISA, JCB, Lady | 1 Oct 2026 – 31 May 2027, registered per round (round 1 to 31 Jan, round 2 from 1 Feb) | ฿17.50 per whole ฿700 on each Bangchak slip | ฿52.50/month |
| **LOTA**, Lotus's | VISA, JCB, Lady, NOW | 1 Aug – 31 Oct 2026 | per slip at Lotus's, Lotus's Go Fresh, lotuss.com: ฿35 (฿1,500–4,999) or ฿150 (฿5,000+) | ฿150/month |
| **LOTB**, Lotus's bonus | VISA, JCB, Lady, NOW | 1 Aug – 31 Oct 2026, registered before spending | ฿450 on one slip of ฿40,000+; first 1,800 accounts nationwide a month | ฿450/month |
| **UNQ**, UNIQLO | VISA, JCB, Lady, NOW | 1 Oct 2026 – 28 Feb 2027 | ฿150 / 300 / 450 per slip from ฿3,000 / 6,000 / 9,000; from ฿10,000 ฿800 (JCB) or ฿700 | ฿800 JCB, ฿700 others /month |

- **The Bangchak campaign was replaced on 1 Oct 2026.** The page now shows steps of ฿700 where it had ฿800, a card-benefit cap of ฿21 a cycle (was ฿32), and BXP at ฿17.50 a step up to ฿52.50 a month (BC3P was ฿24 up to ฿48). The card's "1%" is read as ฿7 per whole ฿700 per slip, as the old ฿8 per ฿800 was paid; the first `BANGCHAK SPECIAL DISCOUNT OF 1 %` lines of October will confirm it. The code is `Bangchak700` because the cycle billed 5 Oct 2026 (5 Sep – 4 Oct) already has `2026M10 — Bangchak <card> cb 1%` rows from the old terms. Two rows with one name would be ambiguous. Spend on 1–4 Oct falls in the new terms' first, partial cycle (1–4 Oct, billed 5 Oct).
- **LOTB isn't registered** on any card (user, 2026-10-01), so it has a class but no Bureau rows; BXP, LOTA and UNQ are registered on every card.
- **LOTA and LOTB stack** on one slip and combine with other promotions. The household's Lotus's spend has gone on Lotus's Beyond, KTC and UOB, never on a Krungsri card, so there's nothing to backfill for Aug–Sep. TrueMoney payments (`TMN*LOTUS`) are excluded as e-wallet spend.
- **UNQ pays ฿800 only on Krungsri JCB cards** (฿700 on the rest), and the JCB's monthly cap is ฿800 to match.

GO Wholesale's statement name is `CFW-<branch> …` (Central Food Wholesale, e.g. `CFW-CHIANGMAI 1 CHIANGMAI TH`); SUP1 matches it since 2026-09-30.

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

Re-read 2026-10-01: ONQ3, SUP1/SUP2 and PTT2 unchanged; <https://www.krungsricard.com/th/promotion/bangchak> now carries the Oct 2026 – May 2027 terms (Bangchak700, BXP); <https://www.krungsricard.com/th/promotion/lotus-exclusive> (LOTA, LOTB).
