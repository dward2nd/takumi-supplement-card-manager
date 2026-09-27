---
tags: [promotion, uob]
---

# UOB EPW538 — "ช้อปออนไลน์ คุ้มทุกคลิก" (e-Commerce & e-Wallet, Jul–Sep 2026)

A UOB campaign paid on the primary cardholder's pooled monthly spend in named apps and wallets, across **every UOB card** Takumi holds and every supplement on them. Tracked in the [[../concepts/promotion-bureau|Promotion Bureau]], one row per month.

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
| Sep 2026 | `2026M9 — EPW538 cb 2%` | ฿3,337.50 (Baiboon ฿513.50, Nuta ฿2,824.00) | ฿0: under the first ฿5,000; Takumi's UOB statement not recorded yet (2026-09-28) |

July and August have no Bureau rows. Create them with `/sync-promotion` (`start`/`end`) if the household wants them tracked.
