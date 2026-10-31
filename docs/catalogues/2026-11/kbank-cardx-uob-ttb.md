---
tags: [catalogue-research, 2026-11]
researched: 2026-11-01
---

> **Research snapshot**: KBank, CardX / SCB, UOB and ttb at Makro (stores + Makro PRO), GO Wholesale, Shopee, Central Retail / Tops / The 1 tie-ins, Shell and PTT, plus these issuers' all-spend and fuel-MCC campaigns there — November 2026 research. Read on **2026-11-01** from the official pages, for the November 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages (Makro, GO Wholesale, Shopee, The 1, Shell, PTT). Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions stayed in the session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# KBank, CardX / SCB, UOB and ttb — November 2026 (พ.ย. 69)

Read 2026-11-01, 01:40–03:30 ICT, from the issuers' own pages only (no Notion reads or writes).

**How the sources were read**

- **UOB**: `data-promotion.json` (666 items; 260 live in November) and each page's `.json` twin. `makro-26th-mpw823-1226` now has a twin too.
- **KBank**: headless Chrome with a desktop agent; the full list from `GetAllMainCcCampaign` (231 campaigns). The T&C boxes are collapsed, so `innerText` misses them: strip the saved `outerHTML` instead.
- **CardX**: the rebuilt Next.js site **renders in headless Chrome now** (it didn't in October): the catalogue `/th-TH/credit-card/promotion` (17 pages, 198 tiles, paged by clicking) and each detail page with full T&C. So CardX figures are **V** this month, not "V-idx".
- **ttb**: headless Chrome, `__NEXT_DATA__`. The first navigation was **not** blocked this time (no warm-up needed). Listings `/th/promotion/credit-card/<shopping|auto>?page=N`.

Confidence labels: **V** verified on the official page today · **R** my reading of official terms · **T** third-party only · **U** unverified.

November dates: **Saturdays** 7, 14, 21, 28 · **Sundays** 1, 8, 15, 22, 29 · **11.11 = Wednesday** · 10–12 Nov = Tue–Thu · **16 Nov = Monday** (UOB Makro ×2 day) · Payday 25–30 Nov · **27 Nov = Friday** (last Friday).

---

## 1. Headline changes vs October

| # | What | Oct 2026 | Nov 2026 |
|---|---|---|---|
| 1 | **KBank supermarket `HYP`** (ended 31 Oct) | ฿75 / 300 / 700 / 1,250 a month at ฿5k / 15k / 30k / 50k | **Successor `TSU`** "ช้อป Supermarket ทุกจังหวัดทั่วไทย", **1 Nov 2026 – 28 Feb 2027**: the same four tiers, ฿1,250/month, **฿5,000 for the campaign**; +฿3,000 a month at ฿300k (฿12,000). MCC 5411/5333 incl. online and QR Credit Card Scan to Pay; **Makro and Makro PRO excluded**. New SMS **`TSU` → 4545888** (HYP's registration doesn't carry over) |
| 2 | **KBank PLUSTINUM Season 3** (≥ ฿30k → Starbucks ฿400) | last month | **No Season 4.** `plustinum-promotion.aspx` now redirects to the promotion index and nothing replaces it in KBank's list. The monthly **≥ ฿10,000 → e-coupon on the 15th** (`plustinum-event`) continues to 31 Dec |
| 3 | **KBank Double Day `DBD`** | final round 9–11 Oct | **New round, 10 Nov – 13 Dec** (windows **10–12 Nov** and 11–13 Dec): ฿70 / 220 / 500 / **1,250** at ฿5k / 15k / 30k / **70k** in the window; ฿1,250/month, ฿2,500 campaign; **LINE MAN and LINE Pay at Lazada/TikTok/LINE MAN now count**. Earlier `DBD` registrants are in automatically. KBank-Shopee card still excluded |
| 4 | **UOB Makro PRO double day** | **MPW838 "Makro PRO 10.10"** ran 9–12 Oct (published 7 Oct): ฿100 at ฿6k / ฿220 at ฿12k a slip, 250 rights each | **An 11.11 edition isn't published yet** (1 Nov). UOB has run one every month since March (3.3–10.10), each published 1–3 days before. Watch ~7–9 Nov |
| 5 | **UOB Makro i-Plan** (MPW611 ended 30 Sep) | — | **MPW827 "Buy Now Pay Later at Makro Store Q4'26"**: same i-Plan 0.70%/0.50% a month for 4/6/10 months, any UOB card, Makro stores |
| 6 | **UOB Shell / Caltex `USC` / `SCP`** (SPW109) | not in October's reports | **Runs 1 Feb 2026 – 31 Jan 2027**: cashback per whole ฿800 a slip at Shell or Caltex — **UOB Premier 3%, UOB World 2%, other UOB cards 1%** — plus points burn 800 points → ฿64 (8%). Register `USC` once → 4545111. The only one of these four issuers with a **Shell** campaign |
| 7 | **UOB Year-End Online Shopping `NL`** (YPW847) | — | **New, 1 Nov – 31 Dec**: UOB Rewards points = slip → **15%** at Lazada / Shopee / TikTok, slip ≥ ฿1,000, 5,000 points a month; **UOB One and UOB Makro excluded**; SMS each time |
| 8 | **CardX ShopeeFood `CARDXOCT`** | to 31 Oct | **No November ShopeeFood page** in CardX's catalogue |
| 9 | **CardX POINTX online `OSD`** | 14% / 20% on 9–11 Oct, 25–31 Oct | Page re-dated 29 Oct – 31 Dec: **14%**, **20% on 10–12 Nov (11.11) and 25–30 Nov** |
| 10 | **ttb codes** | `TTBOCT`, `TTBPREM10`, `10TTBPREM` | **`TTBNOV`** ฿200 / ฿2,000 · **`TTBPREM11`** ฿650 / ฿2,500 · **`11TTBPREM` ฿1,800 / ฿6,000 on 11 Nov only** (20 rights) |
| 11 | **ttb so smart at Makro** | 1% | **No 1% at Makro from 3 Nov** (statement notice); the card page's Thai exclusion list now reads "รายการใช้จ่ายผ่าน Makro". Makro PRO isn't named (§2.4) |
| 11a | **CardX `OEC`** online + wallet ladder (missed in October) | ran from 1 Oct | ฿70 / 300 / 1,000 / 1,800 at ฿5k / 20k / 60k / 100k a month at Shopee, Lazada, TikTok, LINE Shopping, ShopeePay, TrueMoney, LINE Pay; **register monthly from the 1st, 00:00, 1,000 rights** (`OEC` → 4545777); to 31 Jan 2027 |
| 12 | Continuing unchanged | KBank MKR, CardX HY1 / SU1 / CARDXSAT / CXSPM, UOB UMK26 / SPW796 / SPW592 / UOBSUN / OLQ4, ttb BGO / SPM / CTG / BCG | same; **CardX `HYP` ฿3,000 bonus is full** ("สิทธิ์เต็มแล้ว") |

No issuer of the four has a campaign at **PTT** for the household's cards. The only PTT item is KBank's **Blue Credit Card** (PTT co-brand, not held): K Point = slip → **20%** at PTT Station, Café Amazon, EV Station PluZ (`BCC` each time).


---

## 2. Makro (แม็คโคร): stores and Makro PRO

Statement strings: stores `MAKRO_…`; Makro PRO `HTTPS://WWW.MAKRO.PRO/` (MCC 5411) or `WWW.MAKRO.PRO` (MCC 5199); through TrueMoney `TMN MAKRO`.

### 2.1 KBank: "ช้อปเยอะคุ้มกว่า ที่ MAKRO" `MKR` (ACCS261217) · **continuing, unchanged** · **V**

- **Period**: 1 Oct – 31 Dec 2026, spend counted per calendar month. Makro stores by KBank card (swipe/tap) or K Scan to Pay, and Makro PRO online.
- **Cards**: every KBank credit card except business, juristic, Fleet and ThaiBev; each card number counts on its own (household reading, [[../../promotions/kbank-makro]]). LINE POINTS card forfeits its LINE POINTS on spend counted here.

| ต่อ | Monthly spend | Pays | Cap |
|---|---|---|---|
| 1 | ≥ ฿10,000 | ฿100 (1.0%) | ฿240/month, ฿720 campaign |
| 1 | ≥ ฿20,000 | ฿240 (1.2%) | |
| 2 | each ฿300,000 (spend after registering) | +฿1,500 | ฿3,000/month, ฿9,000 campaign |
| 3 | K Point = slip | 10% (`BCB <12> <amount>` → 4545888 each time) | |

- **Registration**: once, K PLUS or SMS `MKR <12>` → **4545888** (household registered on every KBank card, Oct).
- **Excluded**: Smart Pay 0% / Smart Pay By Phone, liquor department, gift cards, redemption goods, tenant shops, Makro via Shopee/Lazada/TikTok, e-wallets (`TMN MAKRO`).
- **Crediting**: within 60 days after 31 Dec. Smart Pay 0% × 3 on a Makro / Makro PRO slip ≥ ฿50,000 is offered.
- Page header and tiers re-read today: <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-makro.aspx>.
- **KBank `TSU` (§3.1) explicitly excludes "MAKRO และ MAKRO PRO (MCC 5199)"**, and KBank's double-day `DBD` counts only Shopee/Lazada/TikTok/LINE MAN: MKR is KBank's only Makro money this month.
- **PLUSTINUM**: Season 3 (≥ ฿30k → Starbucks ฿400) ended 31 Oct with no Season 4 (page redirects to the index). The monthly e-coupon continues (see §3.3).

### 2.2 UOB · **V**

**UOB Makro 26th "Gold Mission" `UMK26`** (MPW823, 1 Oct – 31 Dec; UOB Makro card only; registered 3 Oct) — unchanged; the page now has a `.json` twin:

| Mission | What counts | Pays | Cap (campaign) |
|---|---|---|---|
| 1 | Makro stores, monthly total | ฿150 at ฿50,000–149,999 · ฿800 at ฿150,000–399,999 · ฿2,500 from ฿400,000 | ฿7,500 |
| 2 | **Makro PRO app**, per slip | ฿150 at ฿10,000–29,999 · ฿500 at ฿30,000–59,999 · ฿1,200 from ฿60,000 | ฿3,600 |
| 3 | other spend (not MCC 5411, not fuel, not e-wallet …), monthly | ฿300 from ฿10,000 | ฿900 |
| bonus | all three missions done at least once | ฿1,000 Makro voucher | 1 |
| draw | every ฿1,000 on the card | 1 right (gold bars 4/2/1 baht, Makro vouchers); new UOB Makro cards approved 1 Oct–31 Dec get +10 rights | — |

Principal + supplements pool; ฿12,000 cashback cap across missions; not combinable; credit within 60 days after 31 Dec to the principal card. SMS `UMK26 <12>` → **4545111**. <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/makro-26th-mpw823-1226.page>

**Makro PRO double day** — **11.11 not published (1 Nov)**. October's edition for reference: **MPW838 "Makro PRO 10.10"**, 9–12 Oct, published 7 Oct, UOB Makro card only, Makro PRO web/app, per slip ฿6,000–11,999 → ฿100 (SMS `MP101 <12>`) or ≥ ฿12,000 → ฿220 (`MP102 <12>`) → 4545111; 250 rights per tier, 1 per person, not combinable, excludes cigarettes/alcohol/infant formula/medicines. The series has run 3.3, 4.4, 6.6, 7.7, 8.8, 9.9, 10.10 (index rows `makro-pro-3-3-mpw333` … `makro-10-10-mpw838`), so an 11.11 edition is likely but **unconfirmed**. Look again around 7–9 Nov.

**MPW827 "ผ่อนสบาย ทั้งรถเข็น" (Buy Now Pay Later at Makro Store Q4'26)** — the i-Plan successor of MPW611: any UOB card (not business), Makro stores, **interest-bearing** 0.70%/month (฿2,000–49,999 a slip) or 0.50%/month (≥ ฿50,000), 4/6/10 months (effective 9.56–15.37% a year). Not a saving. <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/makro-mpw827-1226.page> · **V**

**MPW841 Makro Hamper (Season's Greeting 2027)**, 9 Oct 2026 – 5 Jan 2027: gift hampers paid by UOB i-Plan at participating Makro branches → per slip ฿5,000 / 15,000 / 30,000 → ฿120 / 500 / 1,200 on UOB Makro (cap ฿4,800 per account) or ฿100 / 400 / 1,000 on other UOB cards (cap ฿4,000). SMS `MH27 <12>` → 4545111. Hampers only. **V**

**UOB Makro card standing benefits** (card page re-read): 1 point per ฿100 in stores, per ฿25 on Makro PRO and elsewhere; **×2 on the 16th** (`MMID <12>` → 4545111 once) — **16 Nov is a Monday**; Pay with Points at Makro; **1% cashback at Shell/Caltex per ฿800 slip** (see §6). New-card offer (not for the household, who already hold UOB cards): ≥ ฿20,000 in 60 days → 12,000 points + ฿1,000 Makro voucher (≥ ฿5,000 → 6,000 + ฿500), 1 Jun – 31 Dec. <https://www.uob.co.th/personal/credit-cards/rewards/uob-makro-rewards-credit-card.page> · **V**

**UOB One / UOB World at Makro** (card pages re-read): UOB One's 1% and UOB World's points both exclude "ยอดใช้จ่ายในห้างแม็คโคร" (Makro stores) and petrol stations. **SPW796 excludes TrueMoney at Makro** ("ยกเว้น Makro"), so `TMN MAKRO` earns no SPW796. UOB One's own 1% on `TMN MAKRO` (e-wallet) is the household's reconciled reading, not a page statement. **V** (exclusions) / **R** (TMN route)

**UOB Cash Plus "Special Weekend x Makro"** (SPW852, 17 Oct – 28 Dec): Cash Plus loan card, not a credit card; not held.

### 2.3 CardX: `HY1` hypermarkets (C6902056) · **continuing** · **V** (page rendered today)

- 1 Oct – 31 Dec 2026. In store: Big C (all formats), GO WHOLESALE, Lotus's (PRIVE, go fresh), **Makro**. Online: Big C Online, Freshket, GO WHOLESALE APP, Lotus's online, **Makro Pro**.

| Per slip (full amount) | Cashback | Effective |
|---|---|---|
| ฿3,000 – 9,999 | ฿40 | 1.33% → 0.40% |
| ฿10,000 – 29,999 | ฿200 | 2.00% → 0.67% |
| ≥ ฿30,000 | ฿720 | 2.40% at ฿30,000 |

- Cap ฿1,440 per person per month, ฿4,320 for the campaign (all CardX cards). Register once: app/web or SMS `HY1 <12>` → **4545777** (Nuta's CardX JCB registered).
- **`HYP` +฿3,000 at ฿300,000: "สิทธิ์เต็มแล้ว" (rights full)**.
- `HY2`: POINTX = slip → 12% Mon–Thu / 14% Fri–Sun, 50,000 points/month, SMS `HY2 <12> <amount>` each time.
- Excludes every instalment type, ShopeePay, Rabbit LINE Pay, business use. TrueMoney not named (household reads `TMN MAKRO` as uncertain).
- Credited within 60 days after 31 Dec. <https://www.cardx.co.th/th-TH/credit-card/promotion/top-hypermarket-oct26-usc02>

**CardX JCB "ลุ้นเปย์ ไป JAPAN Season 3"** (1 Oct 2026 – 31 Jan 2027): CardX JCB Platinum only; every slip ≥ ฿1,000 (Thailand or abroad) = 1 draw right for three Japan tour packages (≈ ฿745,400 total). Register once `JC <12>` → 4545777. Applies to Nuta's card at any merchant, Makro included. <https://www.cardx.co.th/th-TH/credit-card/promotion/jcb-luckydraw-ss3-oct26-plc14> · **V**

**CardX `OEC` online ladder (§4.2) excludes Makro.**

### 2.4 ttb · **V**

- **ttb so smart 1% no longer pays at Makro.** The card page's Thai exclusion list for the 1% now includes **"รายการใช้จ่ายผ่าน Makro"** (spend via Makro), between TrueMoney Wallet and foreign-registered merchants; the English list beside it hasn't been updated. The page gives no start date; the 27 Oct statement notice in the vault says **from 3 Nov 2026** ([[../../promotions/ttb-2026]]). **Neither text names Makro PRO**: "ผ่าน Makro" can be read to cover the app, but the page doesn't say. Treat Makro PRO on ttb so smart as **probably excluded, unconfirmed**. Purchases on **1–2 Nov** still fall before the change. <https://www.ttbbank.com/th/personal/credit-cards/card-type/ttb-so-smart>
- **`BGO`** (hypermarkets) covers Big C and GO Wholesale only — no Makro, no Makro PRO (re-read; unchanged).
- So **no ttb money at Makro from 3 Nov** (Baiboon's ฿85k on ttb so smart at Makro, May–Oct, now earns nothing). ttb so goood 0% × 3 on slips ≥ ฿1,000 still exists but forfeits the 1% anyway.

---

## 3. GO Wholesale (โก โฮลเซลล์, `CFW-<BRANCH> …`)

### 3.1 KBank: "ช้อป Supermarket ทุกจังหวัดทั่วไทย" `TSU` · **new; successor of HYP** · **V**

- **Period**: **1 Nov 2026 – 28 Feb 2027**, spend per calendar month, register 1 Nov – 28 Feb.
- **Stores**: every shop in the Supermarket category, **MCC 5411 and 5333**, including online and **QR Credit Card Scan to Pay** (FAQ). GO Wholesale (5411) and Tops qualify; **Makro and Makro PRO (MCC 5199) are excluded by name**.

| ต่อ | Monthly spend (registered card) | Pays | Effective |
|---|---|---|---|
| 1 | ฿5,000 – 14,999 | ฿75 | 1.50% at ฿5,000 |
| 1 | ฿15,000 – 29,999 | ฿300 | 2.00% |
| 1 | ฿30,000 – 49,999 | ฿700 | 2.33% |
| 1 | ≥ ฿50,000 | ฿1,250 | 2.50% |
| 2 | ≥ ฿300,000 | +฿3,000 | — |
| 3 | K Point = slip | 10% | no minimum |

- **Caps**: ต่อ 1 ฿1,250 per person per month, **฿5,000 for the campaign** (so four maxed months); ต่อ 2 ฿3,000/month, ฿12,000.
- **Registration**: once, **K PLUS or SMS `TSU <12>` → 4545888**, wait for the reply before spending. HYP's registration doesn't carry over (new code).
- **Cards**: all KBank credit cards except business, juristic, Fleet and ThaiBev. Principal and supplement both count, **by the registered card number** (FAQ). LINE POINTS card forfeits LINE POINTS on counted spend.
- **ต่อ 3 (`BCB <12> <amount>` → 4545888, each time)**: excludes the LINE POINTS card, **every KBank Mastercard**, Xpress Cash, **KBank UnionPay and KBank JCB** cards. K Points of the KBank-Shopee card can't be pooled with other cards.
- **Excluded**: Makro/Makro PRO, Smart Pay 0% and Smart Pay By Phone, liquor, gift cards (incl. e-gift), redemption goods, tenant shops, other platforms (Shopee, Lazada, TikTok), e-wallets (TrueMoney, Rabbit LINE Pay, ShopeePay, LINE PAY).
- **Crediting**: within 60 days after 28 Feb 2027 (ต่อ 3: 60 business days).
- <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-supermarket.aspx>
- **Shared quota**: the same ladder counts GO + Tops + every other supermarket together (pages G and T).

### 3.2 KBank: GO Wholesale Smart Pay 0% × 3 · **continuing to 31 Dec** · **V**

Slip ≥ ฿1,500 at GO Wholesale, KBank Smart Pay 3 months (1 Jul – 31 Dec 2026). Converted spend doesn't count for TSU. <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-go-wholesale-installment.aspx>

### 3.3 KBank PLUSTINUM monthly e-coupon · **continuing to 31 Dec** · **V**

PLUSTINUM / Visa Platinum (old) / Mastercard Platinum: ≥ ฿10,000 full-amount spend in a calendar month (all the person's cards together) → claim **one** e-coupon in K PLUS **on the 15th of the next month, 09:00–23:59**, first come: BBQ Plaza ฿100 (4,000 rights) · Starbucks ฿200 (3,000) · BBQ Plaza ฿200 (2,000) · SF ฿260 (1,000). Principal and supplement counted separately. Any merchant, so GO / Makro / Shopee spend counts. November spend → claim 15 Dec. <https://www.kasikornbank.com/th/promotion/creditcard/pages/plustinum-event.aspx>

### 3.4 CardX `HY1` · **continuing** · **V**

GO in store and GO WHOLESALE APP count (see §2.3): ฿40 / 200 / 720 per slip at ฿3k / 10k / 30k, ฿1,440/month. **Shared quota with Makro (page M).** CardX `SU1` doesn't include GO.

### 3.5 UOB SPW592 "ช้อปซูเปอร์ ยิ่งจ่าย ยิ่งคุ้ม" · **continuing to 31 Dec** · **V** (index dates)

฿50 at ฿4,000–9,999 / ฿150 from ฿10,000 a month (cap ฿150/month, ฿900 campaign), GO Wholesale in store and online, Tops, Rimping, Big C, Lotus's …; **no Makro**; every UOB card except UOB Makro, principal + supplements pooled. **SMS `SH <12>` → 4545111 every month you join, before spending** — not registered by the household. Points 10% (`SP`, not UOB One/Makro). <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/super-spw592-1226.page>

### 3.6 ttb `BGO` hypermarkets · **continuing** · **V**

| Per slip | BGO | + so smart 1% (GO still earns it) |
|---|---|---|
| ฿3,000 – 4,999 | ฿50 | 2.67% at ฿3,000 |
| ฿5,000 – 19,999 | ฿100 | 3.00% at ฿5,000 |
| ฿20,000 – 99,999 | ฿450 | 3.25% at ฿20,000 |
| ≥ ฿100,000 | ฿1,500 | — |

Big C and GO Wholesale (in store + online), 1 Oct – 31 Dec; **฿1,500 per person for the whole campaign**, principal + supplements pooled; e-wallets excluded; register once `BGO <12>` → **4899777** (household registered); credit within 60 days after 31 Dec. The page still carries "highest slip per round" boilerplate (household reads each slip). Updated 28 Oct but terms unchanged. <https://www.ttbbank.com/th/promotion/credit-card/shopping/hypermarket-oct26>

---

## 4. Shopee

### 4.1 KBank · **V**

- **Double Day Double Deal `DBD`** (ACCS260929), **new round 10 Nov – 13 Dec**; November window **10, 11, 12 Nov**:

  | Cumulative in the window | Cashback | Effective |
  |---|---|---|
  | ฿5,000 – 14,999 | ฿70 | 1.40% |
  | ฿15,000 – 29,999 | ฿220 | 1.47% |
  | ฿30,000 – 69,999 | ฿500 | 1.67% |
  | ≥ ฿70,000 | ฿1,250 | 1.79% |

  - Shopee, Lazada, TikTok **and LINE MAN**, plus LINE Pay at Lazada/TikTok/LINE MAN; **Smart Pay 0% counts at the pre-conversion amount**. Excludes ShopeeFood, Shopee Utilities, insurance, utilities, TikTok Ads, non-Thai-registered sellers, TrueMoney and other wallets.
  - Cap ฿1,250 per person per month, ฿2,500 for the round (all cards under one name; credited to the card with the highest spend), within 60 days after 13 Dec.
  - **Cards: not the KBank-Shopee card**, business, juristic, Xpress Cash, Fleet.
  - Register once, K PLUS or `DBD <12>` → **4545888**, 1 Nov – 13 Dec; **8.8 / 9.9 / 10.10 registrants are already in**.
  - Lower than October's ladder (฿70 at ฿3,000 then): the entry tier is now ฿5,000.
  - <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-online-double-day.aspx>
- **KBank-Shopee card** (standing, re-read): ≥ ฿10,000 Shopee spend in a cycle → ×5 on the first ฿5,000 (≤ 1,000 points) and **×10 on ฿5,001–10,000** (≤ 2,000 points); below ฿10,000 → ×5 on the first ฿5,000 only; ×2 at other online shops; **Shopee Coins 1%** (≤ 50 Coins/month, Shopee username registered with the bank); 1,000 K Point → ฿150 Shopee code. <https://www.kasikornbank.com/th/personal/creditcard/pages/kbank-shopee.aspx>
- **LINE POINTS on-top** (KBank LINE Points card, to 31 Dec): +50 at ฿5k–14,999 / +200 at ≥ ฿15k a month, ≤ 800 in total. Continuing. <https://www.kasikornbank.com/th/promotion/creditcard/pages/linepoints-promotion.aspx>
- **No KBank Shopee 11.11 code** in KBank's 231-campaign list (only DBD).

### 4.2 CardX / SCB · **V**

- **`CARDXSAT` "Shopee Every Saturday"** (3 Oct – 26 Dec): ฿170 off ≥ ฿1,500 (before discounts, excl. shipping), Shopee app, 1 per order per card account per day, **100 rights per Saturday from 00:00**. November Saturdays: **7, 14, 21, 28**. Cards: all CardX and SCB WEALTH by CardX. <https://www.cardx.co.th/th-TH/credit-card/promotion/shopee-oct26-onc05>
- **Shopee Mall** (1 Oct – 31 Dec): all CardX cards **`CXSPM11`** ฿300 off ≥ ฿2,000, 1 per card account per month, 400 rights/month; CardX Mastercard / SCB FIRST **`MCSPMALL11`** ฿225 off ≥ ฿1,500. <https://www.cardx.co.th/th-TH/credit-card/promotion/shopee-mall-oct26-onc05>
- **`OEC` "ผูกบัตร ช้อป Online ไม่สะดุด"** (1 Oct 2026 – 31 Jan 2027) — **not in October's report**:

  | Monthly total (all registered cards) | Cashback |
  |---|---|
  | ฿5,000 – 19,999 | ฿70 |
  | ฿20,000 – 59,999 | ฿300 |
  | ฿60,000 – 99,999 | ฿1,000 |
  | ≥ ฿100,000 | ฿1,800 |

  - Shopee, Lazada, TikTok Shop, LINE Shopping, Amaze; wallets Google Pay (tap in store only), LINE Pay, ShopeePay, TrueMoney. Excludes wallet top-ups, **Lotus's, Makro**, delivery apps (Grab, LINE MAN, Robinhood, ShopeeFood).
  - Cap ฿1,800/month, ฿7,200 campaign, 1 right per person per month; **register every month: `OEC <12>` → 4545777, opens the 1st at 00:00, 1,000 rights a month** (first come).
  - Credit within 60 days after each round (1 Oct – 30 Nov; 1 Dec – 31 Jan) to the card used last.
  - <https://www.cardx.co.th/th-TH/credit-card/promotion/e-commerce-cb-oct26-onc05>
- **POINTX online `OSD`** ("ช้อป Online ปักหมุดแลกรับคุ้ม", page re-dated 29 Oct – 31 Dec): POINTX = slip → **14%**; **20% on 10–12 Nov (11.11) and 25–30 Nov** (Payday), and 11–13 Dec. Shopee, Lazada, TikTok, LINE Shopping …, ShopeeFood/Grab/LINE MAN, wallet purchases (not top-ups), OTAs. 5,000 points per person per day; `OSD <12> <amount>` → 4545777 each time, same day; credited within 90 days after round 3 (Nov–Dec). Excludes FAMILY PLUS. <https://www.cardx.co.th/th-TH/credit-card/promotion/thematic-day-jun26-onc05>
- **ShopeeFood**: the `shopee-food-aug26-usc05` page (`CARDXAUG/SEP/OCT` ฿50 off ≥ ฿280, `CARDXNEW`) ended 31 Oct; **no November page** (`…-nov26-…` 404; not in the catalogue).
- **PAYDAY online** (`BPD` ฿3,000 on a ฿150k slip; `OXP` +2,000 POINTX at ฿20k): their old pages (`high-value-interspnd-apr26-onc05`, `mix-payday-apr26-onc05`) **404 on the rebuilt site**, though the PAYDAY hub still links them; not verified for November. **U**
- **0% instalments at Shopee** (`e-commerce-ipp0-jan26-onc05`): 404 on the rebuilt site. **U**
- No CardX 11.11-specific Shopee code (11 Nov is a Wednesday, so CARDXSAT doesn't fall on it).

### 4.3 UOB · **V**

- **`SPW796` "ช้อปออนไลน์ คุ้มทุกคลิก"** (1 Oct – 31 Dec): ฿100 per whole ฿5,000 a month, ฿200/month, ฿600 campaign; Shopee, Lazada, TikTok, LINE Shopping, Central App, King Power, ShopeePay, TrueMoney (partner stores, **not Makro**), LINE Pay; principal + supplements pooled into Takumi's account; `EC <12>` → 4545111 once. Unchanged. <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/shopping-online-spw796-1226.page>
- **`YPW847` "ช้อปออนไลน์ คุ้มส่งท้ายปี"** (**new, 1 Nov – 31 Dec**): UOB Rewards points = slip → **15%** at Lazada, Shopee, TikTok, **slip ≥ ฿1,000**, full amount; cap **5,000 points per cardholder per month** (all cards, all brands) → ≤ ฿750/month. SMS **`NL <12> <amount>` → 4545111 every time, on the purchase day**, or Rewards+. **Excludes UOB One, UOB Makro**, Simple, Lazada, Grab, KrisFlyer, ROP, TMRW; **UOB World and UOB Premier qualify**. "Not combinable with other promotions." Credit within 60 days after the month. <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/year-end-online-shopping-ypw847-1226.page>
- **`UOBSUN`** (SPW558, 5 Jul – 27 Dec): ฿300 off ≥ ฿2,500 a slip **every Sunday** (Nov **1, 8, 15, 22, 29**), 50 rights per Sunday from 00:00, 1 per Shopee member per Sunday. <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/shopee-code-spw558-1226.page>
- **Double Day Happy Deal** (DPW673): ≥ ฿65,000 on Lazada + Shopee + TikTok within **10–12 Nov** → Snoopy 20" trolley (฿6,800), 1 per cardholder per month, **first 100 to register**; register **after** spending, within the window: `DAY <12>` → 4545111. Next: 11–13 Dec. <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/doubleday-campaign-dpw673-1226.page>
- **Shopee Mall × Mastercard** (SPW846, 1 Oct – 31 Dec): Mastercard's own code — **฿225 off ≥ ฿1,500 at Shopee Mall, once a month**, for Thai personal Mastercard Platinum / Titanium / World / World Select / World Elite (UOB One and UOB World are `5432…` Mastercard). UOB's page doesn't print the code; CardX's page names Mastercard's codes **`MCSPMALL11`** (Nov), so that is very likely the same network code (**R**). The page's "ต่อ 2" is SPW796 again (same `EC`). <https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/shopee-mall-x-mastercard-spw846-1226.page>
- **`OLQ4`** (IPW756, 1 Oct – 31 Dec): 0% up to 10 months at online merchants + ฿100–2,000 per instalment slip ≥ ฿10,000; +฿200 GrabFood for a Lazada/Shopee/TikTok instalment ≥ ฿10,000 made on the **25th–31st** (principal only). Unchanged. <https://www.uob.co.th/personal/credit-cards/promotions/ipp/ipponline-ipw756-1226.page>
- **UOB World ×5** (card page re-read): ×5 per ฿25 on online (network e-commerce flag), e-wallet, dining, travel, FX, first ฿20,000 a cycle, then ×2.
- **No UOB 11.11 Shopee code** published. October had a "Double Day 10.10" IPP page (`ipp/double-day.page`, DPW675, 9–11 Oct); no 11.11 version yet.

### 4.4 ttb · **V**

| Code | Discount | Min. order | Window | Rights |
|---|---|---|---|---|
| **`TTBNOV`** | ฿200 | ฿2,000 **after shipping and all discounts** | 1–30 Nov | 1 per card number per month; 412 a month |
| **`TTBPREM11`** | ฿650 | ฿2,500 (Shopee Premium items; full amount or 0% pay plan ≤ 10 months) | 1–30 Nov | 1 per card per order; 150 a month |
| **`11TTBPREM`** | ฿1,800 | ฿6,000 (Shopee Premium) | **11 Nov only** | **20 that day** |

All ttb credit cards, principal and supplement. Not combinable with other promotions (`TTBNOV` box). <https://www.ttbbank.com/th/promotion/credit-card/shopping/shopee-alwayson-jul26> · <https://www.ttbbank.com/th/promotion/credit-card/shopping/shopping-shopeepremium-oct26>

- ttb Disney credit card only (not held): Shopee Payday ฿250 off ≥ ฿1,000 on 25–30 Nov (430 rights/month), and ฿250 off ≥ ฿2,000 monthly (200 rights); codes not printed on the pages.
- ttb so smart 1% applies at Shopee (cap ฿2,000/cycle; TrueMoney excluded).

### 4.5 11.11 at a glance (these four issuers)

| Issuer | 11.11 item | Household card |
|---|---|---|
| KBank | `DBD` ladder 10–12 Nov (฿70–1,250) | PLUSTINUM, JCB, LINE Points (not KBank-Shopee) |
| CardX | POINTX **20%** (`OSD`) 10–12 Nov; `OEC` monthly ladder | Nuta's CardX JCB |
| UOB | Double Day trolley ≥ ฿65,000 (10–12 Nov, `DAY`); `NL` 15% points (World/Premier); `UOBSUN` on Sun 8 Nov / 15 Nov | One, World, Premier |
| ttb | **`11TTBPREM` ฿1,800 / ฿6,000, 11 Nov only** | so smart |

---

## 5. The 1 / Central Retail (Tops, Central, Robinson)

### 5.1 Tops / supermarkets

- **KBank `TSU`** (§3.1) counts Tops (MCC 5411), shared quota with GO.
- **CardX `SU1`** (1 Oct – 31 Dec, unchanged, **V**): per slip ฿1,500–3,999 → ฿35 · ฿4,000–14,999 → ฿120 · ≥ ฿15,000 → ฿520; ฿1,040/month, ฿3,120 campaign; Tops, Tops Daily, Tops online, **Rimping**, Villa, Gourmet, Donki, Lemon Farm, Golden Place, Mitsukoshi, Sentosa, Big Song, Dear Tummy, Flying Tiger; excludes QR Payment credit card, ShopeePay, Rabbit LINE Pay; `SU1 <12>` → 4545777. `SU2` POINTX 13% Mon–Thu / **17% Fri–Sun** (60,000 points campaign). <https://www.cardx.co.th/th-TH/credit-card/promotion/supermarket-ntw-oct26-usc02>
- **CardX PAYDAY supermarket** (25 May – 31 Dec): ฿100 on a slip ≥ ฿1,500 at **Tops (`PDT`)**, Lotus's (`PDL`), Gourmet Market (`PDG`) during **25–30 Nov**; register each month from the 25th 00:00 (500 rights per store); ฿300/month across stores, ฿2,400 campaign. <https://www.cardx.co.th/th-TH/credit-card/promotion/payday-supermarket-may26-usc02> · **V**
- **UOB `SPW592`** (§3.5): Tops, Rimping, GO pooled; `SH` monthly; not registered.
- **ttb `SPM`** (1 Oct – 31 Dec, unchanged, **V**): per slip ฿1,000–4,999 → ฿20 · ฿5,000–14,999 → ฿120 · ≥ ฿15,000 → ฿500; ฿1,000 per person for the campaign; Tops / Tops Online, **Rimping**, Foodland, Villa, Gourmet, Donki, Golden Place, Mitsukoshi, Dear Tummy, Super Cheap, No Brand, Freshket; `SPM <12>` → 4899777. Not GO. <https://www.ttbbank.com/th/promotion/credit-card/shopping/supermarket-oct26>
- **UOB Premier 5% supermarkets (`PRS`)**: not re-read today (the card page path returned 404); not registered by the household.

### 5.2 Central / Robinson department stores and Central malls

- **KBank** K Point → **12%** (15% Wisdom/Premier) at Central and Robinson (all branches), SMS each time; 20,000 points/month; excludes Supersports, Power Buy, B2S, **Tops**. To 31 Dec. <https://www.kasikornbank.com/th/promotion/creditcard/pages/ccpromo-burnpoint-depart.aspx> · **V** · KBank "79th Anniversary Central Chidlom" ends **2 Nov** (Bangkok).
- **CardX PAYDAY Central–Robinson**: slip ≥ ฿3,000 on **25–30 Nov** → ฿200 gift voucher at the store's Customer Service the same day (Central 1,000 / Robinson 550 rights a month). <https://www.cardx.co.th/th-TH/credit-card/promotion/central-robinson-payday-apr26-usc06> · **V** · CardX "Central 79th" and "Central Rama 9" end 2 Nov.
- **UOB**: Central Instant Discount (points → up to 15%, all 2026); **CPN generic** (points → up to 13% at Central malls, all 2026); **Central Beauty Bonus 15%** (CPW826, 1 Nov 2026 – 14 Jan 2027, Beauty Gallery); Robinson `RBS` 12%; **UOB Rewards → The 1 point transfer** (OPW634, all 2026; rate not read); Central 79th (to 2 Nov). Index dates **V**; terms not re-read.
- **ttb**: Central ฿5,000 → ฿500 GC / Robinson ฿3,000 → ฿300 GC, Fri–Sun, 2 Oct – 27 Dec (continuing); **Central malls (CPN plaza zone) Magic Gift Card** 30 Oct 2026 – 3 Jan 2027: Dining ≥ ฿3,000 → ฿100, Fashion/Sport ≥ ฿10,000 → ฿800, Electronics/Beauty clinic/Education ≥ ฿30,000 → ฿3,000, one per day, at the mall's counter, The 1 member number needed (<https://www.ttbbank.com/th/promotion/credit-card/shopping/cpn-oct26>); **Central App 1–13 Nov** (not read in detail); ttb rewards plus → The 1 transfer (`the1-jan26`; ttb so smart earns no points, so N/A).

---

## 6. Shell (petrol)

Household fills are ≈ ฿450–800 a slip, so the per-slip minimums below decide everything.

### 6.1 UOB: "ยิ่งเติม ยิ่งคุ้ม ที่ Caltex / Shell" (SPW109, ref 26UA294) · **V** (terms JSON + poster)

- **Period**: **1 Feb 2026 – 31 Jan 2027**. Participating Shell and Caltex stations.
- **ต่อ 1 — cashback per whole ฿800 per slip** (remainders under ฿800 don't count):

  | UOB card | Cashback | Per ฿800 |
  |---|---|---|
  | Reserve, Infinite, PRVI Miles (with ≥ ฿50,000 other spend that month) | 10% (else 3%) | ฿80 |
  | Zenith, **Premier**, KrisFlyer World Elite | **3%** | ฿24 |
  | Lady Solitaire, KrisFlyer World, **World** | **2%** | ฿16 |
  | **other UOB cards** | **1%** | ฿8 |

  - Spend counted ≤ **฿3,200 per cardholder per month** and ≤ ฿1,600 per slip (all cards, principal + supplements pooled into the principal).
  - **Register once before fuelling**: SMS **`USC <12>` → 4545111** or Rewards+ (Reserve/Infinite automatic). Spend before registering doesn't count.
  - Credit within 60 days after the month, to the principal card.
  - The card exclusion list (business, **UOB One**, Simple, ROP, Grab, Lazada, Mercedes, **UOB Makro**, KrisFlyer, TMRW) sits in **ต่อ 2's box**. For ต่อ 1, UOB One and UOB Makro would be "other UOB cards" at 1% — the UOB Makro card page itself advertises "1% at Shell or Caltex per ฿800 slip". **R** for UOB One.
- **ต่อ 2 — points burn**: 800 points per whole ฿800 per slip → ฿64 (8%), or ฿120 (15%) on Reserve / Infinite / PRVI Miles; ≤ 3,200 points per cardholder per month; **SMS `SCP <12> <amount>` → 4545111 every time, the same day**. Not UOB One / UOB Makro / the cards listed above.
- **Household reading**: a ฿500 fill earns nothing; a ฿800 fill on UOB World = ฿16 (+ ฿64 if burning 800 points), on Premier ฿24. UOB cards earn **no points** at petrol stations (World, One, Makro card pages re-read).
- <https://www.uob.co.th/personal/promotions/credit-cards/shell-caltex-cash-back-spw109-0326/shell-caltex-cash-back-spw109-0326.page> (terms in `/assets/web-resources/personal/credit-cards/promotions/v1/shell-caltex-cash-back-spw109-0326.json`; SMS codes only in the poster `…-d.webp`).
- Related, **not Shell**: UOB "Caltex Friday Surprise 50%" (CPW747): last Friday of the month (**27 Nov**), 4 Bangkok Caltex stations, fill ≥ ฿1,000 + 1,000 points → ฿500 Star CASH card; principals only (not UOB One/Makro). Bangkok only.

### 6.2 KBank · **V**

- **No KBank Shell campaign** in the 231-campaign list (the fuel category holds PTT Blue card, Bangchak points, tyre/service instalments, EV charging).
- KBank cards earn K Point at petrol, **capped at 800 points per merchant category per cycle** at fuel (MCC 5541/5542, 9752 …) and at hypermarkets/supermarkets (K Point conditions). <https://www.kasikornbank.com/th/promotion/credit-card/reward-points/pages/condition.aspx>

### 6.3 CardX · **V**

CardX's "น้ำมัน และ EV" category is **empty** (1 Nov). Only all-spend items apply: CardX JCB draw `JC` (slip ≥ ฿1,000 → 1 right).

### 6.4 ttb · **V**

No Shell campaign. ttb so smart's 1% **excludes all petrol stations**. ttb's fuel campaigns are Caltex `CTG` and Bangchak `BCG` only (3% of a ≥ ฿600 slip, ฿18 a slip, 4 slips/month, to 31 Dec, `CTG`/`BCG <12>` → 4899777; unchanged).

---

## 7. PTT (PTT Station / PTTST)

### 7.1 KBank: Blue Credit Card (PTT co-brand) · **V** · not held by the household

"เติม-ช้อป-กิน คุ้มกว่า": K Point = slip → **20%** at **PTT Station**, Café Amazon, Fit Auto, found & found, Jiffy (EDC, full amount) and EV Station PluZ, **Blue Credit Card only**, 16 Apr – 31 Dec 2026, no minimum; SMS **`BCC <12> <amount>` → 4545888** each time, same day; credit within 60 days after the month. <https://www.kasikornbank.com/th/promotion/creditcard/pages/blue-promotion.aspx> · hub <https://www.kasikornbank.com/th/promotion/creditcard/pages/blue-highlight-promotion.aspx>

Other KBank cards: no PTT campaign; K Point at fuel capped at 800 points per cycle (§6.2).

### 7.2 UOB · **V**

No PTT campaign. UOB cards earn **no points or cashback at petrol stations** (card pages). SPW109 is Shell/Caltex only. (`BPW743` Bangkok Insurance motor-insurance instalments give a PTT fuel card — insurance, not fuel spend.)

### 7.3 CardX · **V**

No PTT campaign (fuel category empty). CardX JCB draw `JC` needs ≥ ฿1,000 a slip (Nuta's PTT fills are ฿500).

### 7.4 ttb · **V**

No PTT fuel campaign; so smart's 1% excludes petrol. **EV only**: `EVC` 3% (≤ ฿90/month, ฿1,080 campaign) on ≥ ฿500 a month at EA Anywhere, EleXA, Evolt and **EV Station PluZ** (PTT's EV chargers), 1 Jan – 31 Dec 2026; SMS `EVC <12>` → 4899777. Not relevant to petrol fills. <https://www.ttbbank.com/th/promotion/credit-card/auto/evstation-jan26>

---

## 8. What ends this month / what's announced for December

**Ends in November** (in scope): ttb Central App (13 Nov); KBank / CardX / UOB / ttb Central 79th and Central Rama 9 (2 Nov); UOB ONESIAM (30 Nov); CardX `OEC` round 1 closes 30 Nov (credit by end Jan); November windows of KBank `DBD` and UOB Double Day (10–12 Nov).

**Announced for December**: KBank `DBD` 11–13 Dec; UOB Double Day 11–13 Dec; CardX `OSD` 20% on 11–13 Dec and 25–31 Dec; `TTBDEC`, `TTBPREM12`, **`12TTBPREM` (12 Dec only)**; `CXSPM12` / `MCSPMALL12`; `CARDXSAT` last Saturday 26 Dec; `UOBSUN` last Sunday 27 Dec; ttb Central/Robinson gift cards to 27 Dec; UOB Caltex Friday Surprise round 3 on 25 Dec.

**Ending 31 Dec**: KBank MKR, PLUSTINUM e-coupon, GO 0%, LINE Points on-top; CardX HY1 / SU1 / PAYDAY / Shopee Mall / OSD; UOB UMK26, SPW796, SPW592, OLQ4, YPW847, MPW827, SPW846; ttb BGO, SPM, CTG, BCG, `shopee-alwayson`, Shopee Premium. **Running into 2027**: KBank `TSU` (28 Feb), KBank supermarket `BCB` (28 Feb), UOB Shell/Caltex SPW109 (31 Jan), UOB Makro Hamper (5 Jan), CardX `OEC` and JCB draw (31 Jan), ttb CPN Magic Gift Card (3 Jan).

## 9. Not found / couldn't read

1. **UOB Makro PRO 11.11** (MPW8xx): not in `data-promotion.json` on 1 Nov. Past editions were published 1–3 days ahead.
2. **UOB / KBank / CardX 11.11 Shopee codes**: none published by the issuers. Only ttb has an 11.11 code (`11TTBPREM`).
3. **ttb so smart at Makro PRO**: the card page says only "รายการใช้จ่ายผ่าน Makro", with no date; the statement notice gives 3 Nov. Whether Makro PRO is covered isn't stated anywhere I could read. Web search found no public ttb notice.
4. **CardX `BPD` / `OXP` (PAYDAY online) and Shopee 0% instalments**: their pages 404 on the rebuilt site.
5. **CardX ShopeeFood November code**: no page.
6. **Fuel campaigns at Shell or PTT** from KBank (other than the Blue card), CardX and ttb: none exist in their current lists.
7. **UOB Premier `PRS`** and **UOB → The 1 transfer rate**: not re-read (Premier card page path 404 to curl).
8. **KBank PLUSTINUM Season 4**: none; Season 3's URL redirects to the index.
9. **ttb welcome offer**: the so smart page still shows the 1 Jul – 31 Oct round; the `new-card` listing returned no tiles.
10. **Mastercard Shopee Mall code on UOB's page**: not printed; `MCSPMALL11` comes from CardX's page.

## 10. Lineage rows

| Campaign | Pays | Oct 2026 | Nov 2026 | Pages | predecessor → successor |
|---|---|---|---|---|---|
| KBank **TSU** "ช้อป Supermarket ทุกจังหวัด" | ฿75 / 300 / 700 / 1,250 at ฿5k / 15k / 30k / 50k a month; +฿3,000 at ฿300k; MCC 5411/5333 incl. QR scan; no Makro | — | **new, 1 Nov 2026 – 28 Feb 2027**; `TSU` → 4545888 | G T | HYP → **TSU** |
| KBank MKR | ฿100 at ฿10k, ฿240 at ฿20k a month | continues | continues to 31 Dec | M | — |
| KBank PLUSTINUM Season 3 | ≥ ฿30k → Starbucks ฿400 | last month | **ended, no successor** | M G | Season 3 → none |
| KBank PLUSTINUM monthly e-coupon | ≥ ฿10k → e-coupon on the 15th | continues | continues to 31 Dec | M G S | — |
| KBank **DBD** | ฿70 / 220 / 500 / 1,250 at ฿5k / 15k / 30k / 70k in the window; LINE MAN added | final round 9–11 Oct | **new round 10–12 Nov, 11–13 Dec** | S | DBD (Aug–Oct) → DBD (Nov–Dec) |
| KBank Blue card `BCC` | K Point → 20% at PTT Station, Café Amazon, EV PluZ | — | continues to 31 Dec (Blue card only) | **P** | — |
| KBank K Point fuel cap | ≤ 800 points/cycle at fuel and supermarkets | — | standing | F P | — |
| CardX HY1 / HYP / HY2 | per slip ฿40 / 200 / 720; HYP full | continues | continues; **HYP rights full** | M G | — |
| CardX SU1 / SU2 | per slip ฿35 / 120 / 520 | continues | continues | T | — |
| CardX **OEC** | ฿70 / 300 / 1,000 / 1,800 at ฿5k / 20k / 60k / 100k a month online + wallets; no Makro | (missed in Oct) | 1 Oct 2026 – 31 Jan 2027; `OEC` monthly from the 1st | S | — |
| CardX OSD | POINTX → 14%, 20% on special days | 9–11 Oct, 25–31 Oct | 20% on 10–12 Nov, 25–30 Nov | S | — |
| CardX CARDXSAT · CXSPM | ฿170 / ฿1,500 Saturdays · ฿300 / ฿2,000 | CXSPM10 | **CXSPM11**, MCSPMALL11 | S | — |
| CardX ShopeeFood | ฿50 / ฿280 | CARDXOCT | **none** | S | CARDXOCT → none |
| CardX JCB draw `JC` | slip ≥ ฿1,000 → 1 right (Japan tours) | — | 1 Oct 2026 – 31 Jan 2027 | M S F P | — |
| UOB UMK26 | missions 1–3 | continues | continues | M | — |
| UOB Makro PRO double day | ฿100 / ฿220 per slip (UOB Makro) | **MPW838 10.10** (9–12 Oct) | 11.11 not published | M | 9.9 MPW765 → 10.10 MPW838 → ? |
| UOB **MPW827** Makro i-Plan | 0.70% / 0.50% a month, 4–10 months | — | Q4 page, to 31 Dec | M | MPW611 → MPW827 |
| UOB MPW841 Makro hamper | ฿100–1,200 per hamper slip by i-Plan | — | 9 Oct 2026 – 5 Jan 2027 | M | Hamper 2026 SPW934 → MPW841 |
| UOB **SPW109** Shell/Caltex `USC` / `SCP` | 1% / 2% / 3% (10%) per ฿800 slip; points 8% | (not catalogued) | to 31 Jan 2027 | **F** | SPW371 (2025) → SPW109 |
| UOB **YPW847** `NL` | points = slip → 15% at Lazada/Shopee/TikTok, ≥ ฿1,000 | — | **new, 1 Nov – 31 Dec** | S | — |
| UOB SPW846 Shopee Mall × Mastercard | ฿225 / ฿1,500 (Mastercard code) + SPW796 | — | 1 Oct – 31 Dec | S | — |
| UOB SPW796 · SPW592 · UOBSUN · OLQ4 · DPW673 | as October | continue | continue | S G T | — |
| UOB Caltex Friday Surprise CPW747 | ฿1,000 fill + 1,000 points → ฿500 Star CASH, last Friday | 30 Oct | 27 Nov, 25 Dec (Bangkok) | — | — |
| ttb so smart 1% at Makro | 1% | earns | **excluded from 3 Nov** | M | — |
| ttb BGO · SPM · CTG · BCG | as October | continue | continue | G T | — |
| ttb Shopee codes | ฿200 / ฿2,000 · ฿650 / ฿2,500 · ฿1,800 / ฿6,000 | TTBOCT, TTBPREM10, 10TTBPREM | **TTBNOV, TTBPREM11, 11TTBPREM (11 Nov)** | S | — |
| ttb CPN Magic Gift Card | ฿100 / 800 / 3,000 per slip in Central malls | — | 30 Oct 2026 – 3 Jan 2027 | T | — |
| ttb `EVC` | 3% at EV chargers incl. EV Station PluZ | — | all 2026 | P (EV only) | — |

## 11. New site tricks

- **CardX's rebuilt site renders in headless Chrome now** (1 Nov, HK egress): the catalogue `/th-TH/credit-card/promotion` has 17 pages of tiles; click the page numbers over CDP and collect `a[href*="/credit-card/promotion/"]` (198 tiles). Category tabs (`น้ำมัน และ EV`, `โปรออนไลน์`, `ซูปเปอร์มาเก็ต`) filter the list. Detail pages `/th-TH/credit-card/promotion/<slug>` carry the full T&C in `innerText` after ≈ 15 s. A missing page returns a 158-character "not found" body.
- **KBank's T&C accordions are hidden**, so `document.body.innerText` misses them: strip the saved `outerHTML` instead (the "เงื่อนไข" blocks and FAQ answers are all there). The page title appears three times; the body starts at its second occurrence.
- **KBank's list**: `postToAPI(backendCcURLMain+"/GetAllMainCcCampaign",{pkg:encryptJWT({value01:0,value02:orderBy,value03:400})})` returns a JSON string (231 rows); `orderBy` is a page global ("วันที่ใหม่-เก่า").
- **ttb**: the first headless navigation got `__NEXT_DATA__` without a warm-up on 1 Nov. The `new-card` listing returned `total_records: 0`.
- **UOB's older-path pages** (`/personal/promotions/credit-cards/<slug>/<slug>.page`) have their twin at `…/promotions/v1/<slug>.json` (SPW109); SMS codes that the JSON lacks are on the `-d.webp` poster.
- **A card page's Thai and English exclusion lists can diverge**: ttb so smart's Thai list added Makro while the English list didn't. Read the Thai one.
