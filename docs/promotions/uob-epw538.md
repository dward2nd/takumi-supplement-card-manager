---
tags: [promotion, uob]
---

# UOB EPW538 — "ช้อปออนไลน์ คุ้มทุกคลิก" (e-Commerce & e-Wallet, Jul–Sep 2026)

A UOB campaign paid on the primary cardholder's pooled monthly spend in named apps and wallets, across **every UOB card** Takumi holds and every supplement on them. Tracked in the [[../concepts/promotion-bureau|Promotion Bureau]], one row per month.

UOB runs the same campaign every quarter under a new code. The earlier runs (EPW913, EPW144, EPW243) are covered [[#The quarterly series|below]]. They live in the [[../databases/cashback-trackers|cashback trackers]] only, with no Bureau rows.

> **Structured source of truth**: `scripts/python/lib/bureau/epw538.py` (`EPW538Promotion`, a `LadderPromotion`). The Bureau page body is rendered from it.

- **Campaign**: `2026-07-01` → `2026-09-30`. Register once: SMS `EC <last 12 digits>` to 4545111, or Rewards+ in UOB TMRW.
- **Source**: <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/e-commerce-e-wallet-epw538-0926.page>, read 2026-09-28. The page renders its terms from `…/e-commerce-e-wallet-epw538-0926.json`; fetch that when the page shows "Loading…".

## Ladder

฿100 per whole ฿5,000 a month, up to ฿200 (so 2% on the first ฿10,000). ฿600 for the campaign, which is 3 × the monthly cap and never binds alone.

## What counts

Full-amount spend through Shopee, Lazada, TikTok, LINE Pay, LINE Shopping, Central App, King Power, ShopeePay and TrueMoney. TrueMoney counts at its partner stores (7-Eleven, McDonald's, Boots, Major Cineplex …), so `TMN 7-11` rows count. **Not**: LINE MAN via LINE Pay (`LINEPAY*PF_LINE MAN`, `LPTH*PF_LM_…`), ShopeeFood, bill payments, insurance, tax, utilities, Easy Pass, fuel through a wallet, Makro through TrueMoney, wallet top-ups, installments, cancelled charges.

## How the credit arrives, and why it looks random

Within 60 days after 30 Sep 2026, into **one** of Takumi's UOB cards; the bank picks which. The household split doesn't depend on which card: it's first come, first served over the pooled rows like NW3. Each holder's tracker row points at the UOB card carrying most of their eligible spend.

## One row, two campaigns

A `TMN 7-11` row on UOB One earns UOB One's 1% *and* counts here (same bank; user, 2026-09-28). EPW538 is an overlay, so it doesn't claim the row's `% cb` (`marks_rows = False`); that stays UOB One's. The bank's own terms add that when promotions in the same merchant category overlap, only the best one pays. Whether UOB treats its One-card cashback as such a promotion is not known.

## Months

| Month | Bureau row | Pooled (so far) | Credit |
|---|---|---|---|
| Sep 2026 | `2026M9 — EPW538 cb 2%` | synced after Takumi's statement was recorded | ฿100: Takumi ฿72.27, Baiboon ฿7.94, Nuta ฿19.79 (trackers, 2026-09-29) |

July and August have no Bureau rows. They were backfilled into the trackers with the earlier quarters (see below): July earns nothing, and August has tracker rows. Don't create Bureau rows for them. `/sync-promotion` would find August's tracker rows by title and re-split them first come, first served.

## The quarterly series

Same ladder, same nine apps, same exclusions every quarter. What changes is the code, the T&C reference and the registration keyword.

| Quarter | Code | Ref | SMS keyword | Terms |
|---|---|---|---|---|
| Oct–Dec 2025 | EPW913 | 25UA135 | `UWC` | [page](https://www.uob.co.th/personal/promotions/credit-cards/e-wallet-e-commerce-epw913-1225/e-wallet-e-commerce-epw913-1225.page): terms in the HTML, but the ladder and the app list are only in the banner image (`…-epw913-1225-1200.jpg`) |
| Jan–Mar 2026 | EPW144 | 26UA303 | `EC` | the page (`…/e-commerce-e-wallet-q126-epw144-0326.page`) renders blank; the terms are in its v1 JSON |
| Apr–Jun 2026 | EPW243 | 26UA303 | `EC` | [page](https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/e-commerce-e-wallet-epw243-0626.page), terms in its JSON |
| Jul–Sep 2026 | EPW538 | — | `EC` | above |

UOB's pages fill in their terms from JSON:

- **Current page paths** (`/personal/credit-cards/promotions/<category>/<name>.page`) read `/assets/web-resources/personal/credit-cards/promotions/<category>/<name>.json`.
- **Older paths** (`/personal/promotions/credit-cards/<name>/<name>.page`) read `/assets/web-resources/personal/credit-cards/promotions/v1/<name>.json`.
- **Every campaign**, with dates, is listed in `/assets/web-resources/personal/credit-cards/promotions/data-promotion.json`. That's how EPW144 was found once its page had gone.

The bank prints each month's credit as `CB E-WALLET AND E-COMMERCE <MON><YY>` (from Apr 2026 prefixed `CB-020`). All of a quarter's months post together, about two months after the quarter ends, each on a UOB card of the bank's choosing.

### Backfill, Oct 2025 – Aug 2026 (user, 2026-09-29)

Nobody had tracked these credits. The household's rules for the backfill:

- **No Bureau rows.** A Bureau row would need Takumi's transactions back to Oct 2025 in his ledger, and they aren't recorded there.
- **Takumi's part comes from the statements.** Each UOB statement is one bundled PDF covering every card and every holder, and one is attached to the friends' Bills rows each month (`ใบแจ้งยอด (PDF)`). Every line was screened with `EPW538Promotion`'s rules and assigned by card number. Friends' `[บัตรหลัก]` rows claim their lines on Takumi's primary cards, as in `/record-statement`. Nothing was written to Takumi's Transactions DB.
- **The statement's transaction date decides the month**, because that's the date the bank counts by. It often differs from the ledger's: the bank dates `TMN 7-11` a day later, so a 28 Feb row can count in March.
- **Refunds of eligible charges are netted in their own month.** Installment refunds (`2C2P *SHOPEE FULL REFUND …`) are not netted, because installments never counted. Pay-with-points credits (`PWP: …`) are not netted either: they aren't cancellations.
- **Split in proportion to each holder's eligible spend, not first come, first served.** The credit is the bank's actual one where it has posted. The statement-derived ladder matched it in all eight months that have one.
- **One tracker row per holder per month** with a non-zero share, named `<code> 2% 1—31 Oct`, with no `Promotion` link. The Note gives the spend, the pool and the bank's credit line. Takumi's rows are ticked once the credit has reached his card; the friends' rows are ticked when he pays them.
- **Baiboon's ฿8,009 counts as Takumi's.** It's a `(FOR SHOPEE)*(FOR SHOP` charge of 18 Nov 2025 on her World supplement `…1009`, and it's in no one's ledger: her Nov 2025 bill is ฿5,771.75 against ฿13,780.75 on the statement. It was never billed to her, so it counts toward Takumi's share.

| Month | Code | Pooled | Takumi / Baiboon / Nuta spend | Credit | Shares T / B / N |
|---|---|---|---|---|---|
| Oct 2025 | EPW913 | ฿10,505.87 | 5,140.62 / 5,365.25 / 0 | ฿200 (World, 24 Feb 2026) | 97.86 / 102.14 / — |
| Nov 2025 | EPW913 | ฿28,058.33 | 19,854.83 / 5,132.50 / 3,071.00 | ฿200 (World, 24 Feb 2026) | 141.53 / 36.58 / 21.89 |
| Dec 2025 | EPW913 | ฿9,151.44 | 5,568.44 / 2,289.00 / 1,294.00 | ฿100 (World, 24 Feb 2026) | 60.85 / 25.01 / 14.14 |
| Jan 2026 | EPW144 | ฿9,103.71 | 1,956.46 / 2,715.50 / 4,431.75 | ฿100 (One, 26 May 2026) | 21.49 / 29.83 / 48.68 |
| Feb 2026 | EPW144 | ฿5,716.46 | 154.96 / 1,486.00 / 4,075.50 | ฿100 (One, 26 May 2026) | 2.71 / 26.00 / 71.29 |
| Mar 2026 | EPW144 | ฿13,441.92 | 6,212.92 / 5,009.00 / 2,220.00 | ฿200 (World, 26 May 2026) | 92.44 / 74.53 / 33.03 |
| Apr 2026 | EPW243 | ฿13,630.14 | 3,729.22 / 8,050.67 / 1,850.25 | ฿200 (World, 20 Aug 2026) | 54.72 / 118.13 / 27.15 |
| May 2026 | EPW243 | ฿8,737.89 | 2,571.39 / 179.00 / 5,987.50 | ฿100 (One, 20 Aug 2026) | 29.43 / 2.05 / 68.52 |
| Jun 2026 | EPW243 | ฿4,719.41 | 2,631.41 / 0 / 2,088.00 | ฿0; none posted | — |
| Jul 2026 | EPW538 | ฿4,975.23 | 2,103.98 / 0 / 2,871.25 | ฿0 (฿24.77 short) | — |
| Aug 2026 | EPW538 | ฿5,480.35 | 2,217.35 / 294.00 / 2,969.00 | ฿100 expected, not yet posted | 40.46 / 5.36 / 54.18 |

Totals: Takumi ฿541.49, Baiboon ฿419.63, Nuta ฿338.88 (฿1,300). When the Q3 credit posts, tick Takumi's August row. If `AUG26` comes in other than ฿100, rescale the three August rows.
