---
tags: [promotion, unionpay, ktc]
---

# UnionPay QR — 6% off at every merchant in Thailand taking UnionPay QR

UnionPay International's monthly offer "Get 6% off" at all merchants in Thailand that accept UnionPay QR, paid through the KTC Mobile app (ICBC and BOC TH apps too). Takumi and Baiboon use their [[../cards/ktc-unionpay|KTC UnionPay]] cards only this way. Tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] **per card number, per calendar month** from September 2026 (user, 2026-09-30).

> **Structured source of truth**: `scripts/python/lib/bureau/unionpay_qr.py` (the campaign), `instant.py` (the discount shape), `quota.py` + `unionpay_offer.py` (the monthly pool). Terms verbatim: [[../sources/unionpay-qr-terms-2026-09-30.txt|sources/unionpay-qr-terms-2026-09-30.txt]].

## Terms

| | |
|---|---|
| Discount | 6% off the price, paid by UnionPay QR with a card registered for the month |
| Per slip | at most ฿60 (reached at a ฿1,000 price) |
| Per card | 1 discounted slip a day; ฿300 a month |
| UnionPay's pool | 12,000 discounts a month nationwide, first come first served; 144,000 over the campaign |
| Months listed | Sep 2026 – Jan 2027 so far, one offer per month (144,000 ÷ 12,000 suggests twelve months) |
| Other | one UnionPay promotion per payment (the best applies); the discount isn't refunded with a refund |

**Each month is its own offer, and each card has to be registered for it** on UnionPay's page. The offer numbers: Sep `260722112617`, Oct `260723112620`, Nov `260723112621`, Dec `260723112622`, Jan `260723112623`.

## The discount is inside the charge

UnionPay takes the 6% off at payment and KTC charges the rest. So `ยอดชำระ` (amount paid) on the ledger row, like the statement line, is **already the net amount** (user, 2026-09-30: "the cashback is combined to the transaction charges, not separated"). A receipt or the app at payment time may show the price before the discount (terms, rule 4); the row takes what KTC charged.

So nothing about this campaign is credited later:
- **no `% cb`**: the `cashback` formula would promise a credit that never comes, and /post-cashback-credits would post one;
- **no tracker rows** in the cashback trackers, since nobody waits for money;
- **no credit rows.**

The Bureau row's `เงินคืนรวม` / `เงินคืนส่วน<name>` still show what each person saved. The class is an `InstantDiscountPromotion`, which reads the discount back from the net amount: an uncapped slip's discount is net × 6/94.

## Reading the ledger

- **Which rows are QR.** Takumi and Baiboon pay with KTC UnionPay by QR only (user, 2026-09-30), so every domestic purchase on their cards counts. Merchant strings ending `… CITY TH` / `CITY THA` are micro-merchants that take QR and little else. Online payments and merchants abroad don't count.
- **Which card.** The limits are per card number, and Baiboon's …2310 is a card of its own (user, 2026-09-30). …1346 carries Takumi's rows and Baiboon's `[บัตรหลัก]` shares; …2310 carries her other rows, the same split as the KTC statements (`lib.points_account`). Nuta's KTC UnionPay isn't registered.
- **Whether the discount was taken.** Prices at these merchants are whole baht, so a discounted slip's net is 94% of a whole number: ฿67.68 was ฿72 less ฿4.32; ฿50 had nothing off. A slip over ฿940 can't show it (a ฿60 discount fits any price), so the terms decide. A slip that shows no discount doesn't use the day's one discount.
- **One slip per charge.** A `[บัตรหลัก]` share and Takumi's part of the same charge are one slip (Bonchon at CNX airport, 3 Sep: ฿281.06 + ฿197.40 = ฿478.46, a ฿509 price). Its discount is split pro rata.
- **The day's discount** goes to the first slip, first come first served. On a date-only day with several slips, the one whose amount shows the discount goes first; otherwise the choice is a guess, and the sync says so.

## When the pool runs out: `Quotas Exceeded Date`

Once UnionPay's 12,000 are gone, nothing is discounted until the next month's offer opens. The ledger can't show when that happened, so the Bureau row carries it as **`Quotas Exceeded Date`**. From that day on the walk discounts nothing. On that day itself, only a slip whose amount shows the discount keeps it.

It gets there two ways:
1. **From UnionPay's page.** Every sync of the row (by hand, or the follow-up after a ledger write) reads the month's offer through UnionPay's API. "left N%" is `live`; "The budget for today has been used up" is `used up`. The first sync inside the month that sees `used up` writes that day. It's when it was first seen, so it can be later than when the pool actually ran out.
2. **From UnionPay's announcement.** UnionPay's Facebook page posts when a month is full. Pass the day as `quota_gone` to /sync-promotion. It replaces a later sighting.

A sighting that came late shows up as warnings: a slip before `Quotas Exceeded Date` whose amount shows no discount, although the terms give one.

## Months

| Month | …1346 (Takumi + Baiboon `[บัตรหลัก]`) | …2310 (Baiboon) | Pool |
|---|---|---|---|
| Sep 2026 | ฿200.04: Takumi ฿121.74, Baiboon ฿78.30 (of ฿3,797.96) | ฿124.32 (of ฿7,756.68) | gone **12 Sep** (UnionPay's Facebook post that day: "สิทธิ์ UnionPay QR เดือนก.ย. 69 เต็มแล้ว … เติมสิทธิ์อีกครั้ง 1 ต.ค. 69") |
| Oct 2026 | ฿225: Takumi ฿165, Baiboon ฿60 | ฿225.48 | gone **10 Oct** (user, that afternoon; offer `260723112620`. UnionPay's offer page still showed 0.86% left at 16:48, so the page lags the pool) |

September, as synced 2026-09-30 (Bureau rows created for September and October on both cards):
- …1346: BANGCHAK ฿940 (฿60), BSRC ฿686.20 (฿43.80), Bonchon ฿478.46 (฿30.54: Takumi ฿17.94, Baiboon ฿12.60), Baiboon's `[บัตรหลัก]` Savemart ฿1,604 (฿60, assumed: over ฿940), AUFU ฿89.30 (฿5.70).
- …2310: Savemart ฿5,913 (฿60, assumed), BCM Lamphun Hospital ฿67.68 (฿4.32), Grill Jung-San ฿1,078 (฿60, assumed), then nothing from 13 Sep. The ledger agrees with the 12 Sep date: the last discounted amounts are 9 Sep, and from 13 Sep the charges are whole prices.
- 1 Sep, …2310: BCM Lamphun Hospital ฿30 shows no discount, although it was the card's only slip that day. Either the card wasn't registered for September yet, or it wasn't paid by QR.

October, as of 2026-10-10: the pool ran out ten days in, two days sooner than September's. `Quotas Exceeded Date` is 10 Oct on both Bureau rows. A slip on the 10th still counts when its amount shows the discount; from the 11th, KTC UnionPay QR slips are whole prices until November's pool opens. While the offer page shows a sliver left, each sync warns that the date disagrees with the page. That warning is expected.

Earlier months look discounted too: Baiboon's `BANGCHAK …` ฿470 (฿500 less 6%, Feb–May 2026), `FRY THANK GRILL` ฿122.20 (Feb) and `SUPER SOUP` ฿122.20 (Aug). UnionPay ran similar QR offers before September. They aren't tracked.

## See also

- [[../cards/ktc-unionpay]] — the card; points (KTC FOREVER) are earned on the net amount.
- [[unionpay-mrt]] — UnionPay's other offer the household meets: 15% off MRT fares by contactless tap, also inside the charge.
- [[../concepts/promotion-bureau]] — the Bureau, shapes, per-card-number quotas.
- [[../databases/promotion-bureau]] — `Quotas Exceeded Date`.
