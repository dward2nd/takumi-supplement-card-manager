---
tags: [promotion, uniqlo, uob, krungsri, kbank, ttb, ktc]
---

# UNIQLO card campaigns, Oct 2026 – Feb 2027 — UNO, UNQ, UQN, UQCB, UQC (and KTC's points)

Six banks run a UNIQLO campaign from 1 October 2026. Five pay cashback per slip and are tracked in the [[../concepts/promotion-bureau|Promotion Bureau]], one row per quota per calendar month; CardX's `UQC` was read on 5 Oct and joined the Bureau that day (see [[#CardX UQC]]). KTC's pays only points (see [[#Points, not Bureau campaigns]]). Read 2026-10-01. UNIQLO's pages give the tiers and dates only in their banner images, so the numbers below were read off the banners. The household's only UNIQLO row before this was Baiboon's ฿990 `UNIQLO-CENTRAL CHIANGMA CHIANGMAI TH` on First Choice (21 Sep 2026).

> **Structured source of truth**: `scripts/python/lib/bureau/uniqlo.py`.

| Code | Bank | Per slip | Monthly cap | Quota per | Register |
|---|---|---|---|---|---|
| **UNO** | UOB, every card | ฿150 per whole ฿3,000 (up to ฿450); ฿800 from ฿12,000 | ฿800 (฿4,000 campaign) | cardholder: every UOB card and supplement pooled | SMS `UNO` **every time**, within the day of the purchase |
| **UNQ** | Krungsri Card, every card | ฿150 / ฿300 / ฿450 at ฿3,000 / 6,000 / 9,000; from ฿10,000 ฿800 on Krungsri JCB, ฿700 on the others | ฿800 JCB, ฿700 others | primary card account (one row per card) | once, UCHOOSE or SMS `UNQ`, within the day |
| **UQN** | KBank, every card | ฿100 / 200 / 300 at ฿3,000 / 6,000 / 9,000; ฿600 from ฿12,000 | ฿600 (฿3,000 campaign) | **each card** (one row per KBank card) | once, before spending: K PLUS or SMS `UQN` |
| **UQCB** | ttb, every card | ฿150 per whole ฿3,000 (up to ฿450); ฿800 from ฿12,000 | ฿800 (฿4,000 campaign) | person: primary and supplements pooled | once, ttb touch or SMS `UQCB` |
| **UQC** | CardX, every card | ฿120 per whole ฿3,000 (up to ฿360); ฿700 from ฿10,000 | ฿700 (฿3,500 campaign) | person (Nuta's CardX JCB, billed on its own) | once per card, CardX app or SMS `UQC` → 4545777 |

All five run 1 Oct 2026 – 28 Feb 2027. Each campaign cap is 5 × the monthly one, so it never binds alone. Every row keeps `% cb` unset, because a fixed credit per slip isn't a rate.

## Readings

- **UNO, UNQ, UQN and UQCB are registered; UQC isn't** (Nuta's CardX JCB, 5 Oct). UQN was registered on 2026-10-01 (user), and a KBank registration covers every KBank card, so it has a row per card (`2026M10 — UQN KBank JCB cb ฿100–600`, …). UQN counts only spend after registering.
- **KBank counts each card separately** unless its terms say otherwise (user, 2026-10-01). UQN's page caps it at "600 บาท / ท่าน / เดือน" (per person), and the household follows the user's rule over that wording, so the Bureau keeps `2026M10 — UQN KBank JCB cb ฿100–600` and so on, one per KBank card.
- **UOB's registration is per visit.** An unregistered slip earns nothing, and a sync can't tell whether one was registered, so a linked UOB UNIQLO row is only as good as the SMS sent that day. UNIQLO stores inside a department store and UOB LADY LUXE PAY don't count.
- **ttb counts only registered card numbers** (re-read 2026-10-05): each card used, supplements included, must be registered with `UQCB`; the cashback goes to the primary card with the highest spend.
- **ttb reads like its hypermarket campaign.** The page's boilerplate speaks of "the highest slip per round". It's read as each slip earning its own tier, as the household read BMG ([[ttb-2026]]).
- **Not combinable — only UNO says it** (corrected 2026-10-05; [[../catalogues/2026-10/all-spend-uniqlo|research]] §3). UOB's UNO carries "ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้". On UNIQLO's Krungsri page the line sits only in the points boxes (points → 10%, JCB 3×/5×), not in UNQ's cashback box. KBank's UQN and ttb's UQCB have no such line. No bank says whether a card's own cashback (UOB One 1%, ttb so smart 1%) is withheld; the household's statements show banks paying both on other campaigns, so the plan counts the card's rate on top. The one real risk is UNQ with Krungsri NOW's 5% on an online slip, since NOW's own terms carry the clause.
- **Lotus's SMP1 names UNIQLO** in its fashion category (not registered), and the household's First Choice NW4 counts fashion; neither is a UNIQLO campaign.
- **The Chiang Mai stores** (Central Chiangmai, ex-Festival, and Central Chiangmai Airport) are mall units with their own rooms, not counters inside a department store, so UNO's department-store exclusion shouldn't bite there (a reading; UOB publishes no list). UNIQLO takes only Visa, Mastercard and JCB, so no UnionPay card or wallet route applies ([[../catalogues/2026-10/uniqlo]]).

## Points, not Bureau campaigns

These pay bonus points that the bank credits later as separate points lines. The household books those as `[คะแนนพิเศษ]` rows when a statement shows them ([[../concepts/points-and-multipliers]]). Nothing is marked on the purchase row.

- **KTC JCB**, 1 Jul – 31 Dec 2026, no registration named: monthly spend per card at UNIQLO, MUJI, COMME des GARÇONS, ISSEY MIYAKE and BEAMS earns ×2 at ฿3,000–9,999, ×3 at ฿10,000–99,999 and ×5 at ฿100,000–300,000. The bonus is capped at 48,000 points and ฿300,000 of spend a month per person, and credited within 60 days after the month. Only Takumi holds KTC JCB. KTC's other UNIQLO offer (1 Oct 2026 – 28 Feb 2027) turns KTC FOREVER points equal to the slip into **13% / 16% / 18%** cashback at ฿3,000 / 5,000 / 8,000 a slip, unlimited, with an SMS `UNQ <16 digits>#<amount>` → **061-384-5000** every slip (the same letters as Krungsri's `UNQ`, another number); KTC CASH BACK and ROP cards are excluded. It's a redemption, not an earning. KTC JCB Ultimate adds nothing at UNIQLO (re-read 2026-10-05).
- **Krungsri JCB Platinum** earns 3× Krungsri points at UNIQLO and a list of Japanese brands (LOFT, MATSUKIYO, NITORI, TSURUHA …), no minimum and no registration, at most 400 bonus points a month per account. The offer runs 1 Oct 2026 – 31 Dec 2027, but **UNIQLO is in it only to 28 Feb 2027**. Krungsri JCB Ultimate earns 5× (1,600 bonus points) from 21 Oct 2026 (re-read 2026-10-05).
- **KBank UQN** adds +200 / 400 / 600 K Point on the ฿3,000 / 6,000 / 9,000 tiers, capped at 1,200 a month and 6,000 for the campaign. The KBank LINE Points card and Titanium Mastercard get none.
- **UOB's and ttb's points halves** redeem points for 10–13% (UOB `PPF`) or 12% (ttb `UQBP`). UOB One and ttb so smart are excluded or earn no points.

## CardX UQC

CardX runs its own round, read 2026-10-05 from <https://www.cardx.co.th/credit-card/promotion/uniqlo-oct26-usc06> (UNIQLO's CardX page still shows the ended Jul–Sep round):

- `UQC`: ฿120 per whole ฿3,000 a slip, **฿700 from ฿10,000**; ฿700 a month and ฿3,500 for the campaign per person; register once per card (CardX app or SMS `UQC <last 12>` → 4545777); installments excluded; credited by 31 Jan 2027 (Oct–Nov spend) and 30 Apr 2027 (Dec–Feb). 1 Oct 2026 – 28 Feb 2027.
- `UQB`: POINTX equal to the slip → 10% (SCB WEALTH 20% at weekends), SMS every time.
- Nuta's CardX JCB is the household's only CardX card and isn't registered (5 Oct). The Bureau tracks it as `CardXUniqloPromotion` in `lib/bureau/uniqlo.py`, one row a month from `2026M10 — UQC cb ฿120–700` (created 2026-10-05, user). Its rows only count once the card is registered.

Sources, read 2026-10-01: <https://www.uniqlo.com/th/th/special-feature/cp/promotion/uob>, <https://www.uniqlo.com/th/th/special-feature/cp/promotion/krungsri>, <https://www.uniqlo.com/th/th/special-feature/cp/promotion/ktc>, <https://www.uniqlo.com/th/th/special-feature/cp/promotion/kbank>, <https://www.ttbbank.com/th/promotion/credit-card/shopping/uniqlo-oct26>. UNIQLO's site answers plain requests with 403; fetch with a browser's headers and a cookie jar, and retry.
