---
tags: [promotion, uniqlo, uob, krungsri, kbank, ttb, ktc]
---

# UNIQLO card campaigns, Oct 2026 – Feb 2027 — UNO, UNQ, UQN, UQCB (and KTC's points)

Five banks run a UNIQLO campaign from 1 October 2026. Four pay cashback per slip and are tracked in the [[../concepts/promotion-bureau|Promotion Bureau]], one row per quota per calendar month. KTC's pays only points (see [[#Points, not Bureau campaigns]]). Read 2026-10-01. UNIQLO's pages give the tiers and dates only in their banner images, so the numbers below were read off the banners. The household's only UNIQLO row before this was Baiboon's ฿990 `UNIQLO-CENTRAL CHIANGMA CHIANGMAI TH` on First Choice (21 Sep 2026).

> **Structured source of truth**: `scripts/python/lib/bureau/uniqlo.py`.

| Code | Bank | Per slip | Monthly cap | Quota per | Register |
|---|---|---|---|---|---|
| **UNO** | UOB, every card | ฿150 per whole ฿3,000 (up to ฿450); ฿800 from ฿12,000 | ฿800 (฿4,000 campaign) | cardholder: every UOB card and supplement pooled | SMS `UNO` **every time**, within the day of the purchase |
| **UNQ** | Krungsri Card, every card | ฿150 / ฿300 / ฿450 at ฿3,000 / 6,000 / 9,000; from ฿10,000 ฿800 on Krungsri JCB, ฿700 on the others | ฿800 JCB, ฿700 others | primary card account (one row per card) | once, UCHOOSE or SMS `UNQ`, within the day |
| **UQN** | KBank, every card | ฿100 / 200 / 300 at ฿3,000 / 6,000 / 9,000; ฿600 from ฿12,000 | ฿600 (฿3,000 campaign) | **each card** (one row per KBank card) | once, before spending: K PLUS or SMS `UQN` |
| **UQCB** | ttb, every card | ฿150 per whole ฿3,000 (up to ฿450); ฿800 from ฿12,000 | ฿800 (฿4,000 campaign) | person: primary and supplements pooled | once, ttb touch or SMS `UQCB` |

All four run 1 Oct 2026 – 28 Feb 2027. Each campaign cap is 5 × the monthly one, so it never binds alone. Every row keeps `% cb` unset, because a fixed credit per slip isn't a rate.

## Readings

- **All four are registered.** UQN was registered on 2026-10-01 (user), and a KBank registration covers every KBank card, so it has a row per card (`2026M10 — UQN KBank JCB cb ฿100–600`, …). UQN counts only spend after registering.
- **KBank counts each card separately** unless its terms say otherwise (user, 2026-10-01). UQN's page caps it at "600 บาท / ท่าน / เดือน" (per person), and the household follows the user's rule over that wording, so the Bureau keeps `2026M10 — UQN KBank JCB cb ฿100–600` and so on, one per KBank card.
- **UOB's registration is per visit.** An unregistered slip earns nothing, and a sync can't tell whether one was registered, so a linked UOB UNIQLO row is only as good as the SMS sent that day. UNIQLO stores inside a department store and UOB LADY LUXE PAY don't count.
- **ttb reads like its hypermarket campaign.** The page's boilerplate speaks of "the highest slip per round". It's read as each slip earning its own tier, as the household read BMG ([[ttb-2026]]).
- **Not combinable.** UOB, Krungsri and KBank all say their UNIQLO cashback can't combine with other promotions. None of the household's other campaigns names UNIQLO.

## Points, not Bureau campaigns

These pay bonus points that the bank credits later as separate points lines. The household books those as `[คะแนนพิเศษ]` rows when a statement shows them ([[../concepts/points-and-multipliers]]). Nothing is marked on the purchase row.

- **KTC JCB**, 1 Jul – 31 Dec 2026, no registration named: monthly spend per card at UNIQLO, MUJI, COMME des GARÇONS, ISSEY MIYAKE and BEAMS earns ×2 at ฿3,000–9,999, ×3 at ฿10,000–99,999 and ×5 at ฿100,000–300,000. The bonus is capped at 48,000 points and ฿300,000 of spend a month per person, and credited within 60 days after the month. Only Takumi holds KTC JCB. KTC's other UNIQLO offer (1 Oct 2026 – 28 Feb 2027) turns KTC FOREVER points into 13–18% cashback per slip, with an SMS every time. It's a redemption, not an earning.
- **Krungsri JCB Platinum** earns 3× Krungsri points at UNIQLO and a list of Japanese brands (LOFT, MATSUKIYO, NITORI, TSURUHA …), 1 Oct 2026 – 31 Dec 2027, no minimum and no registration, at most 400 bonus points a month per account.
- **KBank UQN** adds +200 / 400 / 600 K Point on the ฿3,000 / 6,000 / 9,000 tiers, capped at 1,200 a month and 6,000 for the campaign. The KBank LINE Points card and Titanium Mastercard get none.
- **UOB's and ttb's points halves** redeem points for 10–13% (UOB `PPF`) or 12% (ttb `UQBP`). UOB One and ttb so smart are excluded or earn no points.

Sources, read 2026-10-01: <https://www.uniqlo.com/th/th/special-feature/cp/promotion/uob>, <https://www.uniqlo.com/th/th/special-feature/cp/promotion/krungsri>, <https://www.uniqlo.com/th/th/special-feature/cp/promotion/ktc>, <https://www.uniqlo.com/th/th/special-feature/cp/promotion/kbank>, <https://www.ttbbank.com/th/promotion/credit-card/shopping/uniqlo-oct26>. UNIQLO's site answers plain requests with 403; fetch with a browser's headers and a cookie jar, and retry.
