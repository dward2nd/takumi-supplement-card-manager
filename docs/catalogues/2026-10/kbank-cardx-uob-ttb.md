---
tags: [catalogue-research, 2026-10]
researched: 2026-10-01
---

> **Research snapshot**: KBank, CardX / SCB, UOB and ttb — October 2026 research. Scope: these four issuers at Makro, GO Wholesale, Shopee and notable Central Retail stores. Read on **2026-10-01** from the official pages, for the October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions (HTML, JSON, posters) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# banks-a: KBank, CardX/SCB, UOB and ttb, October 2026 (ต.ค. 69)

Scope: Makro (in store and Makro PRO), GO Wholesale (`CFW-<BRANCH> …`), Shopee, plus Central Retail stores where something stands out.
Researched 2026-10-01, 03:00–03:45 ICT, from official pages only. No Notion reads or writes, no repo edits.
Raw dumps are in `…/scratchpad/research/banks-a/` (`kb_*.dom.txt`, `uob_*.json`, `cxp_*.txt`, `ttb_*.nd.txt`, `gw_*.dom.txt`, `img/`).

**How the sources were read**

- **KBank**: kasikornbank.com blocks curl (Akamai), so pages were rendered in headless Chrome.
- **UOB**: each promotion page has a `.json` twin, and `/assets/web-resources/personal/credit-cards/promotions/data-promotion.json` lists every campaign with its dates.
- **ttb**: Next.js `__NEXT_DATA__`.
- **CardX**:
  - Promotion pages are a single-page app, and their content bucket (`cdx-prod-ssc-frontend…/content/…`) returns CloudFront 403 even from inside Chrome.
  - The full text therefore comes from CardX's own site search index. The page's front-end queries `kong-prod-frontend.cardx.co.th/indexes/promotion/search` with its public key, and the results are the same CMS documents the page renders.
  - That text was cross-checked against the CardX banner images and against GO Wholesale's own copy of the terms.
- **GO Wholesale**: Cloudflare blocks curl, so the pages were rendered in headless Chrome. The WordPress REST list is `/wp-json/wp/v2/promotions`.

Confidence labels: **V** = verified on the issuer's official page or data; **V-idx** = verified from CardX's own CMS index plus its banner or GO's page (the page itself couldn't render); **U** = unverified.

---

## 0. The important changes vs September

| # | What | Sep 2026 | Oct 2026 |
|---|---|---|---|
| 1 | **KBank ช้อป MAKRO `MKR`** | ฿100 per ฿10,000 a month, cap ฿200/month (฿400 campaign). In store only through **K Scan to Pay** | **New round 1 Oct–31 Dec**: ≥ ฿10,000 → ฿100, ≥ ฿20,000 → ฿240. Cap ฿240/month, ฿720 for the campaign. **A normal card swipe now counts in store** ("ใช้จ่ายผ่านบัตรเครดิตกสิกรไทย หรือสแกนจ่ายด้วย K Scan to Pay"). Re-register `MKR` |
| 2 | **CardX Makro `MR1`** (per slip ฿35–900) | ended 30 Sep | Successor: **CardX hypermarket `HY1`** (1 Oct–31 Dec). Per slip ฿40 / ฿200 / ฿720 at ฿3k / ฿10k / ฿30k, cap ฿1,440/month and ฿4,320 for the campaign. Covers **Makro in store + Makro PRO**, GO Wholesale, Big C, Lotus's. No QR-only rule. JCB is on the card belt |
| 3 | **CardX supermarket `SP1`** (GO included) | ended 30 Sep | GO now falls under `HY1` (above). New **`SU1`** covers Tops, Rimping, Villa, Gourmet… (not GO, not Makro; the card belt excludes JCB) |
| 4 | **UOB EPW538** e-commerce/e-wallet | ended 30 Sep | Successor: **SPW796 "ช้อปออนไลน์ คุ้มทุกคลิก" (Q4)**. Same ladder (฿100 per ฿5,000 a month, ฿200/month, ฿600 campaign), same apps, same SMS **`EC`** → 4545111, same ref 26UA303. The registration window is 1 Oct–31 Dec, so re-register |
| 5 | **UOB OLQ3** online 0% installments + cashback | ended 30 Sep | Successor: **`OLQ4`** (IPW756), 1 Oct–31 Dec, identical ladder ฿100–2,000 |
| 6 | **UOB MPW692** (Makro PRO 37th) | ended 29 Sep | **No UOB Makro/Makro PRO campaign for October in UOB's index** (as of 1 Oct 03:00). Makro i-Plan MPW611 also ended 30 Sep with no successor |
| 6a | **Update 3 Oct: UOB MPW823**, the UOB Makro 26th "Gold Mission" (1 Oct – 31 Dec, SMS `UMK26`) | new | It wasn't in the 1 Oct sweep; the user found it on 3 Oct. Terms in [[../campaigns]] (UOB) and on the `Makro — Oct 2026` page · [page](https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/makro-26th-mpw823-1226.page) |
| 7 | **ttb Hypermarket `BMG`** (Big C, GO, **Makro PRO**) | ended 30 Sep | Successor: **`BGO`** (1 Oct–31 Dec, same ฿50/100/450/1,500 tiers, ฿1,500 cap). **Big C + GO Wholesale only: Makro PRO dropped** |
| 8 | **ttb Shopee code** | `TTBSEP` | **`TTBOCT`** ฿200 off ≥ ฿2,000. New: Shopee Premium `TTBPREM10` ฿650/฿2,500 and **`10TTBPREM` ฿1,800/฿6,000 on 10 Oct only** |
| 9 | CardX Shopee | — | **`CARDXSAT`** every Saturday from 3 Oct (฿170 off ≥ ฿1,500) and Shopee Mall **`CXSPM10`** ฿300 off ≥ ฿2,000 |
| 10 | KBank Double Day `DBD` | 8–10 Sep round | **Final round 9–11 Oct**. KBank-Shopee card still excluded |
| 11 | ttb supermarket | none | New **`SPM`** (Tops, Rimping, Villa…), per slip ฿20 / ฿120 / ฿500, cap ฿1,000 |
| 12 | Continuing unchanged | KBank HYP (to 31 Oct), UOB SPW592 (to 31 Dec, SMS `SH` monthly), UOBSUN (Sundays), UOB Makro ×2 on the 16th (`MMID`), KBank-Shopee card ×5/×10, ttb so smart 1% (฿2,000/cycle), UOB One 1% (฿2,000/cycle), UOB World ×5 (first ฿20k/cycle) | same |

October dates: **Saturdays** 3, 10, 17, 24, 31 · **Sundays** 4, 11, 18, 25 · **10.10 = Saturday** · 9 Oct = Friday · **16 Oct = Friday** (UOB Makro ×2 day) · Payday 25–31 Oct.

---

## 1. Makro (แม็คโคร): in store and Makro PRO

### 1.1 KBank: "ช้อปเยอะคุ้มกว่า ที่ MAKRO" (campaign ACCS261217) · **changed (new round)** · **V**

- **Period**: 1 Oct–31 Dec 2026, spend accumulated **per calendar month**.
- **Channel**:
  - Makro stores by KBank credit card (swipe/tap) **or** K Scan to Pay in K PLUS.
  - Makro PRO online.
  - Page and FAQ: "MAKRO โดยชำระผ่านบัตรเครดิตกสิกรไทย และ ช่องทางออนไลน์ MAKRO PRO". September's FAQ required K Scan to Pay; October's doesn't.
- **Cards**: all KBank credit cards except business, corporate, Fleet and ThaiBev.
  - Household: **KBank PLUSTINUM** (Takumi's card, which Baiboon uses at Makro), KBank JCB, KBank LINE Points, KBank-Shopee.
  - The LINE POINTS card forfeits its LINE POINTS on spend counted here.

| ต่อ | Accumulated / month | Cashback | Effective |
|---|---|---|---|
| 1 | ≥ ฿10,000 | ฿100 | 1.00% |
| 1 | ≥ ฿20,000 | ฿240 | 1.20% (best at exactly ฿20,000) |
| 2 | every ฿300,000 | +฿1,500 | 0.50% |
| 3 | K Point = slip amount | 10% | no minimum, no limit on number of redemptions |

- **Caps**:
  - ต่อ 1: ฿240 per person per month, ฿720 for the campaign.
  - ต่อ 2: ฿3,000 per person per month, ฿9,000 for the campaign.
  - September's caps were ฿200/฿400 and ฿6,000/฿12,000.
  - Spend is counted per registered card number (FAQ); principal and supplement both count.
- **Registration**:
  - K PLUS, or SMS `MKR <last 12 digits>` → **4545888**, once, with the reply received between 1 Oct and 31 Dec.
  - ต่อ 1 counts spend before or after registering; ต่อ 2 counts only spend after it.
  - ต่อ 3: SMS `BCB <12 digits> <amount>` → 4545888 after each purchase. Excludes the LINE POINTS card, Titanium and Xpress Cash.
- **Crediting**: ต่อ 1–2 within 60 days after 31 Dec; ต่อ 3 within 7 days after the campaign ends.
- **Special**:
  - KBank Smart Pay 0% for 3 months on a Makro or Makro PRO slip of ≥ ฿50,000 (instalment ≥ ฿16,666.67/month). Claim it in K PLUS after the charge posts and at least 3 business days before the statement date.
  - The converted slip earns no K Point, but the page says its full amount still counts for ต่อ 1–3.
- **Excluded**:
  - KBank Smart Pay 0% / Smart Pay By Phone (generally), liquor department, gift cards, redemption items, tenant shops.
  - Other platforms (Shopee, Lazada, TikTok) and e-wallet payments (Rabbit LINE Pay, ShopeePay).
- **URL**: <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-makro.aspx>. Poster checked: "เซฟต้นทุน รับคืนคุ้ม ที่ makro · รวมสูงสุด 9,720 บาท · 1 ต.ค. 69 – 31 ธ.ค. 69".

### 1.2 KBank: card programmes that also pay on Makro spend · **V**

- **PLUSTINUM "ยิ่งใช้ยิ่งพลัสชัวร์ Season 3"** (1 Aug–31 Oct; **October is the last month**):
  - Spend ≥ ฿30,000 in the calendar month → Starbucks e-Coupon ฿400 (≈ 1.33%).
  - **Re-register in K PLUS for October before spending.** Cap ฿1,200 for the season.
  - ≥ ฿150,000 cumulative (one registration) → 2 × Coral Lounge (฿2,800; Chiang Mai airport included).
  - Counts full-amount spend, Smart Pay and cash advances; excludes gold shops, funds, unit-linked insurance, crypto and FX notes.
  - Principal and supplement are counted separately. Coupons appear in K PLUS within 30 business days of month-end.
  - Stacks with MKR: ฿30k at Makro on PLUSTINUM = ฿240 + Starbucks ฿400.
  - <https://www.kasikornbank.com/th/promotion/creditcard/pages/plustinum-promotion.aspx>
- **PLUSTINUM monthly e-coupon** (Jul–Dec 2026; 10,000 rights a month):
  - Spend ≥ ฿10,000 a month → claim on the **15th of the next month** in K PLUS (Starbucks ฿200 / BBQ Plaza ฿100–200 / SF ฿260), 1 per person per month.
  - <https://www.kasikornbank.com/th/promotion/creditcard/pages/plustinum-event.aspx>

### 1.3 CardX: "คุ้มยกแพ็ก รับคืนแรง ที่ไฮเปอร์มาร์เก็ต" (C6902056) · **new; successor of MR1 (Makro) and SP1 (GO)** · **V-idx**

- **Period**: 1 Oct–31 Dec 2026.
- **Stores**:
  - In store: **Makro**, GO WHOLESALE, Big C (all formats), Lotus's (PRIVE, go fresh).
  - Online: **Makro PRO**, GO WHOLESALE app, Big C Online, Lotus's online, Freshket.
- **Payment**: full amount by CardX / SCB WEALTH by CardX credit card, or CardX FLEX.
  - The terms name no QR requirement; September's MR1 required scanning in SCB EASY / CardX app in store.
  - The card belt on the page includes **CardX JCB Platinum**, so Nuta's CardX JCB looks eligible (the text says "ทุกประเภท").
- **Excluded**: every instalment type (ดีจัง 0% etc.), ShopeePay, Rabbit LINE Pay, business use, cancelled charges.

| Per sales slip (full amount) | Cashback | Effective |
|---|---|---|
| ฿3,000 – 9,999 | ฿40 | 1.33% → 0.40% |
| ฿10,000 – 29,999 | ฿200 | 2.00% → 0.67% |
| ≥ ฿30,000 | ฿720 | 2.40% at ฿30,000 |

- **Caps**: ฿1,440 per person per month (all cards together), ฿4,320 for the campaign. The best month is two slips of exactly ฿30,000.
- **Bonus**:
  - Cumulative full-amount spend ≥ ฿300,000 over the campaign → +฿3,000 (1 per person, **150 rights in total**, credit cards only).
  - Register SMS `HYP <12 digits>` → 4545777 (this is CardX's `HYP`, not KBank's).
- **POINTX redemption**:
  - Points = slip amount → **12% Mon–Thu / 14% Fri–Sun**.
  - Cap 50,000 points per person per month, 150,000 for the campaign. Excludes FAMILY PLUS and FLEX.
  - Register each time, the same day: SMS `HY2 <12 digits> <amount>` → 4545777, or the app/web.
- **Registration**: once, via the CardX app/web or SMS `HY1 <12 digits>` → **4545777** (CardX FLEX: `FHY`).
- **Crediting**: within 60 days after 31 Dec, shown on the next statement.
- **Also offered**: ดีจัง 0% for 4 months (converted amount loses points and cashback).
- **Sources**:
  - Banner "คุ้มยกแพ็ก รับคืนแรง 7,320 บาท + 14%" with BigC · freshket · GO · Lotus's · makro · makro PRO logos (`img/hyper_banner_small.jpg`).
  - Page: <https://www.cardx.co.th/credit-card/promotion/top-hypermarket-oct26-usc02>.
  - GO's copy: <https://centralfoodwholesale.co.th/promotion/scb-cashback-oct26/> (re-rendered 1 Oct).

### 1.4 CardX: ended

- **MR1/MR2** (Makro/Makro PRO 37th anniversary, 22 Jul–30 Sep): **ended**.

### 1.5 UOB · **V**

- **MPW692** (Makro PRO 37th, per slip ฿120–1,200) ended 29 Sep. **MPW765** Makro PRO 9.9 (8–11 Sep, UOB Makro only, ≤ ฿220) ended.
  - **No October Makro or Makro PRO campaign exists in UOB's promotion index** (`data-promotion.json`, checked 1 Oct 03:00).
  - Pattern: UOB ran a UOB-Makro-only Makro PRO "double day" each month (3.3, 4.4, 6.6, 7.7, 8.8, 9.9; max ฿220), each published 1–2 days before. A 10.10 edition is plausible but **unconfirmed**.
- **MPW611 "ผ่อนสบาย ทั้งรถเข็น"** (Makro i-Plan 0.70%/0.50% a month, 1 Jan–30 Sep): **ended**, no successor listed.
- **UOB Makro card**, standing benefits (<https://www.uob.co.th/personal/credit-cards/rewards/uob-makro-rewards-credit-card.page>):
  - Earning:
    - 1 point per ฿100 in Makro stores.
    - 1 point per ฿25 on Makro PRO and other spend.
    - Other supermarkets/hypermarkets (MCC 5411) earn 1 point per ฿25, up to ฿100,000 a cycle.
  - **×2 points on the 16th** (Makro stores, Makro PRO and other spend; not non-Makro MCC 5411):
    - Register once with SMS `MMID <12 digits>` → 4545111; it applies from the month of registration.
    - Bonus points arrive within 60 days of month-end. **16 Oct is a Friday.**
  - Cap 150,000 points per account per calendar year.
  - Redemption: 5,500 points = ฿500 Makro voucher; Pay with Points at Makro 9 points = ฿1 (TMRW).
  - Status: continuing.
- **UOB One**: its 1% excludes "ยอดใช้จ่ายในห้างแม็คโคร" (Makro stores) per the card page. Makro PRO earns 1% by the household's own data (docs). 10%/5% unchanged; ฿500/month and ฿2,000/cycle caps unchanged.
  - <https://www.uob.co.th/personal/credit-cards/cash-back/one-cash-back-credit-card.page>
- **UOB World**: the card page excludes "ยอดใช้จ่ายในห้างแม็คโคร" from points, i.e. ×0 in store.
- **SPW592 supermarkets** excludes Makro and the UOB Makro card (see GO).
- **UOB Cash Plus "Special Weekend x Makro"** (CPW654, 18 Jul–12 Oct): a Cash Plus (loan card) offer, not a credit card; the household doesn't hold one.

### 1.6 ttb · **V**

- **No ttb Makro campaign in October.**
  - `BGO` covers Big C and GO Wholesale only; September's `BMG` Makro PRO leg is gone.
  - Also, `BGO`'s Big C / GO rules don't mention Makro in store at all, and September's didn't count it either.
- **ttb so smart 1%** applies at Makro (cap ฿2,000/cycle; Makro isn't in the exclusion list).
- **ttb so goood 0% for 3 months** on any slip ≥ ฿1,000 (in ttb touch, 04:00–21:00), but converted spend loses the 1%.

---

## 2. GO Wholesale (โก โฮลเซลล์, `CFW-<BRANCH> …`)

GO's own card-promotion list (WP REST, 1 Oct) shows these for October: CardX `scb-cashback-oct26`, ttb `ttb-cashback-oct26` and Central The 1 Magic e-Voucher (the1 agent), plus the continuing KBank ฿5,000 (HYP), KBank 0%, UOB ฿900 (SPW592), AEON, Krungsri and KTC.

### 2.1 KBank: supermarket `HYP` (ACCS260883) · **continuing, ends 31 Oct** · **V**

| Accumulated / month | Cashback | Effective |
|---|---|---|
| ฿5,000 – 14,999 | ฿75 | 1.50% |
| ฿15,000 – 29,999 | ฿300 | 2.00% |
| ฿30,000 – 49,999 | ฿700 | 2.33% |
| ≥ ฿50,000 | ฿1,250 | 2.50% |
| ≥ ฿300,000 | +฿3,000 | — |

- **Caps**: ฿1,250/month and ฿5,000 for the campaign; the bonus is ฿3,000/month and ฿12,000 for the campaign.
- **Stores**: every MCC 5411/5333 supermarket, **including online and QR Credit Card Scan to Pay** (FAQ).
- **Excluded**: Makro/Makro PRO, Smart Pay, liquor, gift cards, tenant shops, other platforms, e-wallets.
- **K Point redemption**: 10% (`BCB`) or 15% for The Wisdom/The Premier (`SYP`).
- **Registration**: once, K PLUS or `HYP <12>` → 4545888, between 15 Jul and 31 Oct.
- **Cards**: all KBank cards except business, corporate, Fleet and ThaiBev.
- **Crediting**: within 60 days after 31 Oct.
- <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-supermarket.aspx>
- Separately, the **supermarket K Point 10%** (`BCB`, ACCS260210) runs 1 Mar 2026–28 Feb 2027 (<…/shopping-supermarket-redeempoint.aspx>).
  - K Points on the KBank-Shopee card can't be pooled with other cards' points.

### 2.2 KBank: GO Wholesale Smart Pay 0% for 3 months · **continuing** · **V**

- Slip ≥ ฿1,500. Header dates 1 Jul–31 Dec; the T&C says 1 Aug–31 Dec 2026.
- <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-go-wholesale-installment.aspx>

### 2.3 CardX: `HY1` hypermarket · **new (replaces SP1 at GO)** · **V-idx**

- See 1.3: per slip ฿40 / ฿200 / ฿720 at ฿3k / ฿10k / ฿30k; ฿1,440/month and ฿4,320 for the campaign; +฿3,000 at ฿300k (`HYP`); POINTX 12%/14% (`HY2`).
- **GO in store + GO WHOLESALE app** both count.
- GO's page (<https://centralfoodwholesale.co.th/promotion/scb-cashback-oct26/>, "รับเครดิตเงินคืนสูงสุด 4,320 บ. … 1 ต.ค.–31 ธ.ค. 2569") carries the same tiers, codes and caps.
- September's page announced a new Oct–Dec GO promotion paying up to ฿4,320; **this is it** (฿4,320 = the `HY1` cap).

### 2.4 CardX: `SU1` supermarket · **new** · **V-idx** · GO **not** included (see §4)

### 2.5 UOB: SPW592 "ช้อปซูเปอร์ ยิ่งจ่าย ยิ่งคุ้ม" · **continuing to 31 Dec** · **V**

- **ต่อ 1** (spend accumulated per month; no minimum per slip; slips combine):
  - ฿4,000–9,999 → ฿50 (1.25% at ฿4,000).
  - ≥ ฿10,000 → ฿150 (1.50%).
  - Cap ฿150 per cardholder per month, ฿900 for the campaign.
- **ต่อ 2**: UOB Rewards points = slip amount → **10%**.
  - SMS `SP <12> <amount>` → 4545111 each time, on the day. Cap 50,000 points a month.
  - **Excludes UOB One**, UOB Makro, Simple, Lazada, Grab, KrisFlyer, ROP and TMRW. **UOB World and UOB Premier qualify.**
- **Stores** (MCC 5411/5499):
  - In store: **GO Wholesale**, Big C (+Mini), Don Don Donki, Foodland, Gourmet Market, Home Fresh Mart, Lotus's (PRIVÉ, go fresh), Mitsukoshi Depachika, No Brand, **Rimping**, **Tops** / Tops Daily / Tops Care / Tops Food Hall, Villa Market.
  - Online: Big C online, Freshket, **GO Wholesale**, Lotus's Shop Online, Tops Online, Villa Online.
  - **No Makro.**
- **Excluded**: e-wallets (TrueMoney, Rabbit LINE Pay, ShopeePay), COD, tenant shops, bill payments, gift cards, top-ups, i-Plan instalments, cancelled charges. Counted by transaction date.
- **Cards**: all UOB credit cards except business and **UOB Makro**.
  - Principal and supplements pool into the principal; several principal cards pool together.
  - So Takumi's One, World and Premier and the friends' supplements share ฿150/month.
- **Registration**: ต่อ 1 needs SMS `SH <12>` → 4545111 or Rewards+ **once in each month you want to join, before spending** (Reserve/Infinite are automatic).
- **Crediting**: within 60 days after the end of each registered month, into a principal card of UOB's choosing.
- <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/super-spw592-1226.page> (terms in the `.json` twin).
- The UOB Makro card at GO earns 1 point per ฿25 (MCC 5411), with no ×2 on the 16th.

### 2.6 ttb: Hypermarket `BGO` · **successor of BMG** · **V**

| Per sales slip | BGO | + so smart 1% |
|---|---|---|
| ฿3,000 – 4,999 | ฿50 (1.67%) | 2.67% |
| ฿5,000 – 19,999 | ฿100 (2.00%) | 3.00% |
| ฿20,000 – 99,999 | ฿450 (2.25%) | 3.25% |
| ≥ ฿100,000 | ฿1,500 (1.50%) | 2.50% |

- **Period**: 1 Oct–31 Dec 2026.
- **Stores**: **Big C and GO Wholesale**, in store and online (Big C Online, GO Wholesale Online). **Not Makro PRO.** E-wallet payments are excluded.
- **Cap**: ฿1,500 per person for the whole campaign, all hypermarkets together. All principal cards and supplements are pooled; Takumi's …7368 and Baiboon's …0864 share it.
- **Registration**: once, before or on the day, via ttb touch or SMS **`BGO <12 digits>` → 4899777** (ttb reserve infinite is automatic).
- **Crediting**: within 60 days after 31 Dec, to the principal card with the highest spend.
- **Reading**: the boilerplate still says "ธนาคารจะนำยอดใช้จ่ายสูงสุดต่อเซลล์สลิปในแต่ละรอบรายการมาคำนวณ". The household reads each slip as earning its own tier (docs/promotions/ttb-2026.md, BMG).
- **Cards**: all ttb credit cards (incl. Global House, Disney), principal and supplement.
- <https://www.ttbbank.com/th/promotion/credit-card/shopping/hypermarket-oct26>, confirmed by GO's copy <https://centralfoodwholesale.co.th/promotion/ttb-cashback-oct26/> ("สูงสุด 1,500 บ.… BGO … 4899777").
- `SPM` supermarkets (§4) **doesn't include GO**.

---

## 3. Shopee

### 3.1 KBank · **V**

- **KBank-Shopee card** (standing, unchanged):
  - K Point per ฿25 at Shopee:
    - If the cycle's Shopee spend is ≥ ฿10,000: ×5 on the first ฿5,000 (≤ 1,000 points), **×10 on ฿5,001–10,000** (≤ 2,000 points), ×1 above that.
    - If it is < ฿10,000: ×5 on the first ฿5,000, ×1 on ฿5,001–9,999 (≤ 199 points).
  - Other online shops and ShopeeFood: ×2; everything else ×1.
  - ShopeePay-linked, coupon, top-up and bill spend is excluded.
  - **Shopee Coins 1%** (max 50 a month; the Shopee username must be registered with the bank; credited within 60 days of month-end).
  - **1,000 K Point → ฿150 Shopee code.**
  - <https://www.kasikornbank.com/th/personal/creditcard/pages/kbank-shopee.aspx>
- **Double Day Double Deal `DBD`** (ACCS260929): **October round = 9, 10, 11 Oct**, the final round. The campaign runs 7 Aug–11 Oct.

  | Cumulative Shopee + Lazada + TikTok in the window | Cashback | Effective |
  |---|---|---|
  | ฿3,000 – 7,999 | ฿70 | 2.33% |
  | ฿8,000 – 19,999 | ฿220 | 2.75% |
  | ฿20,000 – 49,999 | ฿600 | 3.00% |
  | ≥ ฿50,000 | ฿1,600 | 3.20% |

  - Cap ฿1,600/month, ฿4,800 for the campaign.
  - Counts full-amount **and Smart Pay 0%** spend.
  - Excludes ShopeeFood, Shopee Utilities, insurance, utilities, TikTok ads and **e-wallet payments (LINE Pay, TrueMoney)**.
  - **Cards: excludes the KBank-Shopee card**, Titanium, business, Xpress Cash and Fleet. Takumi's PLUSTINUM, JCB and LINE Points qualify.
  - Register once (K PLUS or SMS `DBD <12>` → 4545888) by 11 Oct; an Aug/Sep registration covers the whole campaign.
  - Credited within 60 days after 11 Oct, to the registered card with the highest spend.
  - <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-online-double-day.aspx>
  - KBank's own promo search for "Shopee" returns only this campaign: there's **no KBank Shopee 10.10 code**.
- **KBank LINE POINTS card on-top** (NCCS261123, 1 Sep–31 Dec):
  - Monthly spend ฿5,000–14,999 → 50 points; ≥ ฿15,000 → 200 points. Cap 200/month and 800 in total.
  - **+800 bonus** at ฿80,000 cumulative.
  - Counts spend that earns the normal 1% LINE POINTS, plus insurance, fuel and supermarket spend; not the 5% LINE MAN / LINE Pay spend.
  - Register once in K PLUS (counts back to the 1st of that month).
  - <https://www.kasikornbank.com/th/promotion/creditcard/pages/linepoints-promotion.aspx>

### 3.2 CardX / SCB · **V-idx** (SCB debit: **V**)

- **`CARDXSAT` "Shopee Every Saturday"** (C6901909): **every Saturday, 3 Oct–26 Dec** (October: 3, 10, 17, 24, 31).
  - ฿170 off an order ≥ ฿1,500 (before discounts, excluding shipping), 11.3%.
  - 1 per order per card account per day; **100 rights a day**, released at 00:00.
  - Shopee app only; standard logistics; the usual gold, milk and voucher exclusions.
  - Card belt includes JCB. <https://www.cardx.co.th/credit-card/promotion/shopee-oct26-onc05>
- **Shopee Mall** (C6902086, 1 Oct–31 Dec):
  - All CardX cards: **`CXSPM10`** (Oct) / `CXSPM11` / `CXSPM12`, ฿300 off ≥ ฿2,000 (15%), 1 per card account per month, 400 rights a month.
  - CardX **Mastercard** / SCB FIRST: `MCSPMALL10` / 11 / 12, ฿225 off ≥ ฿1,500 (15%), 1 per month.
  - <https://www.cardx.co.th/credit-card/promotion/shopee-mall-oct26-onc05>
- **POINTX online "ช้อป Online ปักหมุดแลกรับคุ้ม"** (C6901047, 1 Jun–31 Dec):
  - Points = slip amount → **14%**; **20% on Special Days**: Double Day **10.10 = 9–11 Oct**, **Payday 25–31 Oct**.
  - Cap 5,000 points per person per day. Categories include Shopee, ShopeePay (purchases), ShopeeFood, Lazada and TikTok. Excludes FAMILY PLUS.
  - Register each time, the same day: SMS `OSD <12> <amount>` → 4545777.
  - Replaces September's description (14%/20%, `ONR1`–`ONR5`); the ONR multi-point scheme wasn't re-checked.
- **PAYDAY online** (C6900741, to 31 Dec): a single slip ≥ ฿150,000 on 25–31 Oct at Shopee, Lazada, TikTok or TrueMoney (purchases) → ฿3,000. 100 rights a month; register monthly from the 25th with SMS `BPD <12>`.
- **PAYDAY POINTX** (C6900747): cumulative ≥ ฿20,000 on 25–31 Oct at Shopee, Lazada, TikTok, LINE Shopping, ShopeePay, TrueMoney or LINE Pay (top-ups included) → +2,000 POINTX. 500 rights; SMS `OXP <12>` monthly.
- **0% instalments** (C6900062, all 2026): Shopee 3 months ≥ ฿1,500, 6 months ≥ ฿3,000, 10 months ≥ ฿5,000. Participating shops only; no codes allowed with it.
- **ShopeeFood** (C6901419, to 31 Oct): `CARDXOCT` ฿50 off ≥ ฿280 (2 per person per month, 1,600 rights a month).
- iPhone 18 via Shopee (to 31 Oct): the page says the quota is already used up.
- **SCB debit Mastercard × Shopee** (1 Apr 2026–31 Mar 2027): ฿120 off ≥ ฿900 (13.3%), 1 per card per month, 690 rights a month. The code is shown at shopee.co.th/m/scb-debit-promotion.
  - <https://www.scb.co.th/th/personal-banking/promotions/debit-cards/lets-promotion-shopee.html>
  - Also, SCB debit POINTX ×5 on all spend (1 Sep–31 Dec, ≤ 1,000 points a month).

### 3.3 UOB · **V**

- **SPW796 "ช้อปออนไลน์ คุ้มทุกคลิก" (Shopping Online Q4'26)**: **successor of EPW538; this is the "SPW796" September's page mentioned.**
  - **Period**: 1 Oct–31 Dec 2026.
  - **Ladder**: ฿100 per full ฿5,000 accumulated in the month, max ฿200/month (2% on the first ฿10,000), **฿600 for the campaign**.
  - **Apps**:
    - Shopee, Lazada, TikTok, LINE Shopping, Central App, King Power, **ShopeePay**, TrueMoney and LINE Pay.
    - TrueMoney counts at its partner stores (7-Eleven, McDonald's, Boots …) except **Makro**.
  - **Excluded**: LINE MAN via LINE Pay, ShopeeFood via ShopeePay, bill payments, insurance, tax, utilities, Easy Pass, fuel via any wallet, wallet top-ups (TrueMoney, ShopeePay, LINE Pay), cancelled charges.
    - Full-amount only, so instalments don't count. Counted by transaction date.
  - **Pooling**: principal and supplements pool into the principal, across all principal cards; Takumi, Baiboon and Nuta share one ladder.
  - **Registration**: once with SMS **`EC <12 digits>` → 4545111** or Rewards+ in UOB TMRW, **within 1 Oct–31 Dec**. It's unclear whether an EPW538 registration carries over, so re-send `EC`. Reserve/Infinite are automatic.
  - **Crediting**: within 60 days after 31 Dec, into one principal card of UOB's choosing.
  - The overlap clause (best single promotion in the same merchant category) and "not combinable" are unchanged from EPW538.
  - Page: <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/shopping-online-spw796-1226.page>. Terms: `/assets/web-resources/personal/credit-cards/promotions/shopping-lifestyle/shopping-online-spw796-1226.json`. Poster checked (`img/spw796_m.png`).
- **`OLQ4` online 0% instalments + cashback** (IPW756, 1 Oct–31 Dec; ref 26IC73):
  - 0% up to 10 months at participating online merchants (≥ ฿2,000 a slip, ≥ ฿500 a month).
  - Cashback for 0% ≥ 4 months on participating items, per slip:

    | Instalment slip | Cashback | Effective |
    |---|---|---|
    | ฿10,000–19,999 | ฿100 | 1.0% |
    | ฿20,000–29,999 | ฿250 | 1.25% |
    | ฿30,000–49,999 | ฿400 | 1.33% |
    | ฿50,000–99,999 | ฿900 | 1.8% |
    | ≥ ฿100,000 | ฿2,000 | 2.0% |

  - Cap ฿20,000 per cardholder.
  - **+฿200 GrabFood code** for a Lazada, Shopee or TikTok instalment ≥ ฿10,000 made on the **25th–31st** (1 per cardholder, principal only).
  - Register once: SMS `OLQ4 <12>` → 4545111.
  - Credited within 90 days after 31 Dec. Not combinable with other UOB 0% promotions.
  - Merchant list:
    - Marketplaces: Lazada, Shopee, TikTok.
    - Home & Furniture online, including **Thai Watsadu**.
    - Excludes new iPhone, Apple Store, **Power Buy, Central Online, Robinson Online**, Gourmet Market, and IT/mobile shops.
  - <https://www.uob.co.th/personal/credit-cards/promotions/ipp/ipponline-ipw756-1226.page>
- **`UOBSUN`** (SPW558, 5 Jul–27 Dec; **continuing**):
  - ฿300 off ≥ ฿2,500 per slip (12%), **every Sunday** (4, 11, 18, 25 Oct). 50 rights per Sunday, released 00:00; 1 per Shopee member per Sunday; full amount only.
  - <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/shopee-code-spw558-1226.page>
- **Double Day Happy Deal** (DPW673; the October window is **9–11 Oct**, then 10–12 Nov and 11–13 Dec):
  - Cumulative ≥ ฿65,000 on Lazada, Shopee and TikTok within the window → Snoopy 20" trolley (฿6,800 value). 1 per cardholder per month, **first 100 registrants a month**.
  - Register **after** spending, within the window: SMS `DAY <12>` → 4545111.
  - <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/doubleday-campaign-dpw673-1226.page>
- **UOB World ×5** (standing): ×5 per ฿25 on online (Visa/Mastercard e-commerce), e-wallet, dining, travel and FX for the first ฿20,000 a cycle, then ×2. Shopee is a bonus category.
  - <https://www.uob.co.th/personal/credit-cards/rewards/uob-world-credit-card.page>
- **UOB One 1%** (standing): e-wallet 1%; caps unchanged.
- **FD4 food delivery** (FPW815, 1 Oct–31 Dec; ShopeeFood, LINE MAN, Robinhood):
  - Cashback up to ฿100/month and ฿300 for the campaign (SMS `FD4 <12>` → 4545111). **The rate and threshold aren't stated on the page or poster.** Marginal to Shopee.
- **Not found**: a UOB Shopee **10.10** code or a 10.10 IPP page. September's 9.9 IPP "DD99" was a one-off page, and nothing like it has been published for October.

### 3.4 ttb · **V**

- **`TTBOCT`** (shopee-alwayson-jul26, codes TTBJUL…TTBDEC):
  - ฿200 off ≥ ฿2,000 per order (10%). The minimum is **after shipping and all discounts**.
  - 1 per card number per order per month; 412 rights a month. All ttb cards, principal and supplement.
  - <https://www.ttbbank.com/th/promotion/credit-card/shopping/shopee-alwayson-jul26>
- **Shopee Premium** (new, 1 Oct–31 Dec; full amount or 0% pay plan ≤ 10 months; Shopee Premium-tagged items only):
  - **`TTBPREM10`** (Oct): ฿650 off ≥ ฿2,500 (26%), 1 per card per order, 150 rights a month.
  - **`10TTBPREM`: 10 Oct only**, ฿1,800 off ≥ ฿6,000 (30%), 20 rights.
  - <https://www.ttbbank.com/th/promotion/credit-card/shopping/shopping-shopeepremium-oct26>
- **ttb so smart 1%**: continuing (฿2,000/cycle cap per card account; TrueMoney excluded).

### 3.5 10.10 at a glance (these four issuers)

| Issuer | 10.10 item | Household card |
|---|---|---|
| KBank | `DBD` cashback ladder, 9–11 Oct (฿70–1,600) | PLUSTINUM, JCB, LINE Points (not KBank-Shopee) |
| CardX | 10 Oct is a **Saturday** → `CARDXSAT` ฿170/฿1,500; POINTX **20%** on 9–11 Oct (`OSD`) | Nuta's CardX JCB |
| UOB | Double Day trolley ≥ ฿65,000 (9–11 Oct, `DAY`); `UOBSUN` on Sun 11 Oct | One, World, Premier |
| ttb | `10TTBPREM` ฿1,800/฿6,000, Shopee Premium, 10 Oct only; `TTBOCT` monthly | so smart |

No other 10.10-specific Shopee code from these issuers appeared on their official pages as of 1 Oct.

---

## 4. Central Retail stores (only what stands out)

### 4.1 Tops (supermarket)

- **ttb `SPM`** (1 Oct–31 Dec):
  - Per slip ฿1,000–4,999 → ฿20; ฿5,000–14,999 → ฿120; ≥ ฿15,000 → ฿500 (3.33%, or **4.33% with the 1%**).
  - Cap ฿1,000 per person for the campaign.
  - Stores: TOPS / TOPS Online, **Rimping**, Foodland, Villa, Gourmet, Donki, Golden Place, Mitsukoshi, Dear Tummy, Super Cheap, No Brand, Freshket.
  - SMS `SPM <12>` → 4899777. `tops-oct26` is the same campaign. **V** <https://www.ttbbank.com/th/promotion/credit-card/shopping/supermarket-oct26>
- **CardX `SU1` "ช้อปซูเปอร์ฯ คืนคุ้มเวอร์"** (C6902055, 1 Oct–31 Dec):
  - Per slip ฿1,500–3,999 → ฿35 (2.33%); ฿4,000–14,999 → ฿120 (3.0%); ≥ ฿15,000 → ฿520 (3.47%). Cap ฿1,040/month and ฿3,120 for the campaign; SMS `SU1`.
  - POINTX = slip: 13% Mon–Thu / **17% Fri–Sun** (`SU2`, 60,000 points for the campaign).
  - Stores: Tops, Tops Daily, Tops online, **Rimping**, Villa, Gourmet, Donki, Lemon Farm, Golden Place, Mitsukoshi, Sentosa, Big Song, Dear Tummy, Flying Tiger.
  - Excludes **QR Payment credit card**, ShopeePay and Rabbit LINE Pay.
  - **The card belt image is named `…no_jcb…`**, so CardX JCB is probably not eligible; the text doesn't say. **V-idx**
- **CardX PAYDAY supermarket** (25th–end of month, to 31 Dec):
  - ฿100 on a slip ≥ ฿1,500 (6.7%) at **Tops `PDT`**, Lotus's `PDL` and Gourmet `PDG`.
  - Register monthly from the 25th, 00:00 (500 rights per store per month). Cap ฿300/month across stores, ฿2,400 for the campaign. **V-idx**
- **UOB SPW592** and **KBank HYP** both include Tops (see GO).

### 4.2 Central / Robinson department stores

- **ttb**, Fri–Sun, 2 Oct–27 Dec; claim at Customer Service the same day:
  - Central: ฿5,000 slip → ฿500 gift card (10%), cap ฿1,000, 1,388 rights.
  - Robinson: ฿3,000 → ฿300 (10%), cap ฿600, 675 rights.
  - Both exclude Tops, Central Food Hall, Power Buy, Supersports, B2S, Baan & Beyond, online and pay plans.
  - Central App: ฿400 off ≥ ฿4,000 (5–11 Oct, 100 rights). **V**
- **UOB**:
  - Central Midnight Sale #3 (23 Sep–**5 Oct**): ฿100 per ฿4,000 slip (2.5%), cap ฿600 (SMS `CEN` once). Points = spend → **15% for UOB Premier** (and Reserve, Infinite, Lady, Mercedes), 12% for others.
  - Central Instant Discount (all 2026): Premier 15%, World 12%; principal cards only; UOB One and UOB Makro excluded; 100,000 points for the campaign.
  - Robinson points 12% (`RBS`, 10,000 points a month). **V**
- **KBank** K Point at Central, Robinson, central.co.th and the Central app: 12% (15% Wisdom/Premier). SMS `CD` each time; 20,000 points a month; excludes Tops, Power Buy, B2S, Supersports and Baan & Beyond. **V**

### 4.3 Thai Watsadu

- **KBank** (1 Sep–31 Dec):
  - Per full-amount slip: ฿10,000 → ฿120 (1.2%) … ≥ ฿200,000 → ฿3,800 (SMS `H3`, cap ฿40,000).
  - 0% 6–10 months: ฿150–4,800 (`HF3`).
  - K Point 12%.
  - The Visa 4% discount code ended 30 Sep. **V** (September's draft had this as news-only.)
- **UOB OLQ4** includes Thai Watsadu online.

### 4.4 Power Buy

- UOB OLQ4 **excludes** Power Buy. UOB's IPP Power Buy Q3 runs to 7 Oct.
- CardX has Power Buy / Power Mall appliance offers (Oct–Dec, up to ฿42,000). Not read in detail.

---

## 5. Registration cheat-sheet (household cards)

| Issuer | Needed for October | How |
|---|---|---|
| KBank | **`MKR` (new round)**, once | K PLUS or `MKR <12>` → 4545888 |
| KBank | `HYP` (if not yet), `DBD` (by 11 Oct) | same number; once per campaign |
| KBank | PLUSTINUM Season 3, **re-register for October** | K PLUS |
| KBank | `BCB <12> <amount>` for each K Point redemption | 4545888 |
| CardX (Nuta) | **`HY1`** once; `HYP` once (฿300k bonus); `HY2` each time | → 4545777 or CardX app |
| CardX (Nuta) | `SU1` once (JCB likely ineligible); `OSD` each time; `BPD` / `OXP` / `PDT` monthly from the 25th | → 4545777 |
| UOB (Takumi) | **`EC` (SPW796)** once in Q4; **`SH` every month**; **`OLQ4`** once; `DAY` after spending 9–11 Oct; `MMID` once (if not already); `FD4` once; `SP` / `RBS` / `CEN` as used | → 4545111 or Rewards+ in TMRW |
| ttb | **`BGO`** once; `SPM` once | ttb touch or → 4899777 |

---

## 6. Not found / unconfirmed

1. **UOB Makro / Makro PRO October campaign**: none in UOB's index as of 1 Oct 03:00. A 10.10 "Makro PRO double day" for UOB Makro cards (≤ ฿220, like 3.3–9.9) is plausible, **unconfirmed**.
2. **UOB Makro i-Plan** (MPW611 ended 30 Sep): no successor listed.
3. **UOB 10.10 IPP** (like 9.9's `DD99`) and any UOB Shopee 10.10 code: not published.
4. **SPW796 registration carry-over**: the terms say register once during 1 Oct–31 Dec. Whether an EPW538 `EC` registration still counts is unknown, so re-send `EC`.
5. **CardX card eligibility**: JCB for `HY1` and the Shopee codes is inferred from the card-belt images (JCB Platinum shown). JCB's exclusion from `SU1` is inferred from the `…no_jcb` belt. Neither is stated in the text.
6. **CardX pages**: they couldn't be rendered because the CDN returns 403 on `/content/`. The terms come from CardX's CMS search index, the banners and GO's page. Worth a manual look in the CardX app.
7. **UOB FD4** (ShopeeFood): the cashback rate and threshold aren't stated.
8. **KBank**:
   - A K Point → Shopee code for **non-KBank-Shopee** cards: not verified.
   - HYP's successor after 31 Oct: unknown.
   - No KBank 10.10 Shopee code exists (the site search shows only DBD).
9. **KBank MKR**: the page says the Makro 0% 3-month conversion still counts in full for ต่อ 1–3, while the general Smart Pay exclusion says otherwise. Taken as written.
10. **ttb `BGO` wording**: "highest slip per round" vs each slip earning its own tier. The household's reading is each slip (docs).
11. **SCB debit at Makro / GO**: nothing on SCB's debit promotions list.
12. **Shopee's own 10.10 bank-partner codes** (the Shopee site has a captcha): not checked here.
13. **CardX POINTX `ONR1`–`ONR5`** multi-point redemption (in September's draft): not re-checked.

## 7. Sources (all read 2026-10-01)

**KBank**

- <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-makro.aspx>
- …/shopping-supermarket.aspx
- …/shopping-online-double-day.aspx
- …/shopping-go-wholesale-installment.aspx
- …/shopping-supermarket-redeempoint.aspx
- …/plustinum-promotion.aspx
- …/plustinum-event.aspx
- …/linepoints-promotion.aspx
- …/ccpromo-burnpoint-depart.aspx
- …/homedecor-thaiwatsadu.aspx
- …/shopping-complex.aspx
- <https://www.kasikornbank.com/th/personal/creditcard/pages/kbank-shopee.aspx>
- Index: <https://www.kasikornbank.com/th/promotion/creditcard/pages/index.aspx>

**CardX** (content via `kong-prod-frontend.cardx.co.th/indexes/promotion/search`)

- <https://www.cardx.co.th/credit-card/promotion/top-hypermarket-oct26-usc02>
- …/supermarket-ntw-oct26-usc02
- …/shopee-oct26-onc05
- …/shopee-mall-oct26-onc05
- …/thematic-day-jun26-onc05
- …/high-value-interspnd-apr26-onc05
- …/mix-payday-apr26-onc05
- …/e-commerce-ipp0-jan26-onc05
- …/shopee-food-aug26-usc05
- …/payday-supermarket-may26-usc02
- Banners on `cdx-prod-ssc-frontend.cardx.co.th` (saved in `img/`)

**SCB**

- <https://www.scb.co.th/th/personal-banking/promotions/debit-cards/lets-promotion-shopee.html>
- …/debit-pointx-x5.html

**UOB** (page + `.json` twin)

- Promotion pages under `https://www.uob.co.th/personal/credit-cards/promotions/`:
  - …/shopping-lifestyle/shopping-online-spw796-1226.page
  - …/ipp/ipponline-ipw756-1226.page
  - …/shopping-lifestyle/shopee-code-spw558-1226.page
  - …/shopping-lifestyle/super-spw592-1226.page
  - …/shopping-lifestyle/doubleday-campaign-dpw673-1226.page
  - …/shopping-lifestyle/makro-mpw611-0926.page
  - …/dining/food-delivery-fpw815-1226.page
  - …/shopping-lifestyle/central-midnight-cpw717-1026.page
  - …/shopping-lifestyle/robinson-rpw460-1226.page
- Card pages:
  - <https://www.uob.co.th/personal/credit-cards/rewards/uob-makro-rewards-credit-card.page>
  - …/rewards/uob-world-credit-card.page
  - …/cash-back/one-cash-back-credit-card.page
- Index: <https://www.uob.co.th/assets/web-resources/personal/credit-cards/promotions/data-promotion.json>

**ttb**

- Shopping promotions under `https://www.ttbbank.com/th/promotion/credit-card/shopping/`:
  - hypermarket-oct26
  - supermarket-oct26
  - tops-oct26
  - shopee-alwayson-jul26
  - shopping-shopeepremium-oct26
  - central-oct26
  - robinson-oct26
  - centralapp-oct26
- Card page: <https://www.ttbbank.com/th/personal/credit-cards/card-type/ttb-so-smart>

**GO Wholesale**

- <https://centralfoodwholesale.co.th/promotion/scb-cashback-oct26/>
- <https://centralfoodwholesale.co.th/promotion/ttb-cashback-oct26/>
- `…/wp-json/wp/v2/promotions` (list)
