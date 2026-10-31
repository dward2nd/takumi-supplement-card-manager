---
tags: [promotion, unionpay, aeon, ktc, transit]
---

# UnionPay MRT — 15% off Blue and Purple Line fares

UnionPay International's offer at the MRT (BEM): **15% off every fare** on the Blue and Purple Lines, no minimum, when a participating UnionPay credit card is tapped at the gate by EMV contactless. Recorded 2026-10-09 (user), first on Takumi's [[../cards/_stubs|AEON UnionPay]] (`MRT-BEM BANGKOK TH` ฿50.15, a ฿59 fare). Tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] from October 2026 on Takumi's AEON UnionPay …2918, per calendar month (user, 2026-11-01).

> **Structured source of truth**: `scripts/python/lib/bureau/unionpay_mrt.py` (`UnionPayMRT2918`, an `InstantDiscountPromotion`), with the pool as `AnnouncedPool` in `quota.py`.

> **Terms verbatim**: [[../sources/unionpay-mrt-terms-2026-10-09.txt|sources/unionpay-mrt-terms-2026-10-09.txt]]. UnionPay's page: <https://m.unionpayintl.com/cardholderServ/serviceCenter/merchant/1134436148216?type=1>; BEM's: <https://metro.bemplc.co.th/Promotion-Detail?pid=9550>. Promotion code `260309111895`.

## Terms

| | |
|---|---|
| Period | 16 Mar – 31 Dec 2026 |
| Discount | 15% off the normal fare, per trip (tap in and tap out on the Blue or Purple Line), no minimum. A ฿20 fare is charged ฿17 |
| Cards | AEON-UnionPay Platinum, KTC UnionPay, KTC PROUD UnionPay, Bangkok Bank UnionPay Platinum, KBank UnionPay and Xpress Cash UnionPay, ICBC (Thai) UnionPay |
| Per card | at most ฿550 of discount a month, pre-authorisations included |
| UnionPay's pool | 86,000 discounts a month, 860,000 over the campaign, first come first served. A pre-authorisation and a settlement each use one |
| Excluded | buying tickets or topping up at the counter; any other UnionPay offer on the same payment (the best one applies). Other issuers' offers can stack |
| Refunds | refund the amount paid only; the discount counts as used |

No registration is mentioned, unlike [[unionpay-qr|UnionPay QR]].

## The discount is inside the charge

As with [[unionpay-qr|UnionPay QR]], the statement and the bank's app show the fare **after** the discount (terms, rule 7; user, 2026-10-09: "the cashback is combined in the transaction (if eligible), not separated"). So `ยอดชำระ` (amount paid) is the net figure, and nothing is credited later: leave `% cb` unset, add no tracker row and no credit row. The Bureau's `เงินคืน…` fields still show what each person saved.

## Reading the ledger

- **Whether the discount was taken.** MRT fares are whole baht, so a discounted settlement is 85% of a whole number: ฿50.15 is ฿59 less ฿8.85, ฿14.45 a ฿17 fare, ฿38.25 a ฿45 one. An amount in satang that isn't 85% of a whole number had nothing off. A whole-baht amount can't tell you: it's either an undiscounted fare or a multiple of ฿20 with 15% off (฿20 → ฿17). Takumi's `MRT-BEM` ฿17 of 11 Oct 2026 could have been a ฿17 fare at full price (the Blue Line's lowest). The user confirmed it was a ฿20 fare with ฿3 off (2026-10-12).
- **When it counts.** By the date the bank posts the settlement, not the travel date (rule 4). One settlement can bundle several trips over one or more days, which is why MRT lines often arrive later than the ride. If the pool has run out by the posting date, there is no discount (rule 6). The user checked on 2026-10-09 that October's pool was not used up.
- **Which cards the household can use.** Takumi's and Nuta's AEON UnionPay and the KTC UnionPay cards all qualify. Takumi and Baiboon pay with KTC UnionPay by QR only, so in practice it's the AEON UnionPay cards that tap at the gate.
- **Not AEON's own cashback.** AEON UnionPay's 3% is for spend in CNY, HKD, MOP or TWD ([[aeon-2026]]), so a Thai MRT fare doesn't count toward it.

## In the Promotion Bureau

One row per calendar month for Takumi's AEON UnionPay …2918: `2026M10 — UnionPay MRT …2918 cb 15%` (user, 2026-11-01: "register the 15% cashback at MRT for Takumi's AEON UnionPay"). The ฿550 is per card number, so friends' `[บัตรหลัก]` taps on …2918 share it; Nuta's own supplement number would be a separate card and isn't tracked. KTC UnionPay isn't tracked here: Takumi and Baiboon pay with it by QR only, and a payment takes one UnionPay offer.

- **Which rows count**: `MRT-BEM …` only. A whole-baht amount that isn't 85% of a whole number shows no discount and uses none of the ฿550; the sync warns about it.
- **The month** is the row's transaction date, not the settlement's posting date the terms use. They differ only for a settlement posting across a month end.
- **UnionPay's pool** isn't in the offer API the QR offer uses (promotion code `260309111895` returns nothing, checked 2026-11-01). So `Quotas Exceeded Date` is set by hand from UnionPay's announcement: `/sync-promotion` with `quota_gone`.
- **Follows the ledger**: `/add-transaction` and the other writers re-sync the month's row after an AEON UnionPay write, like every Bureau campaign.

| Month | …2918 | Pool |
|---|---|---|
| Oct 2026 | ฿21.15 on ฿119.85 of fares: ฿50.15 (฿8.85 off) and ฿14.45 (฿2.55) on 9 Oct, ฿38.25 (฿6.75) on 10 Oct, ฿17 (฿3) on 11 Oct | not used up on 9 Oct (user) |
| Nov 2026 | row created 2026-11-01, nothing yet | |

