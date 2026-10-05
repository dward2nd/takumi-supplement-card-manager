---
tags: [catalogue-research, 2026-10]
researched: 2026-10-05
---

> **Research snapshot**: UNIQLO Thailand itself — October 2026 research. Scope: UNIQLO's Chiang Mai stores, the payment methods it takes, its own deals (limited offers, app and member coupons, events), wallets and BNPL, mall-level campaigns at the Chiang Mai malls that host it, government schemes, and the list of banks on UNIQLO's own promotion hub. Bank card campaigns themselves and all-spend card offers are out of scope (other researchers). Read on **2026-10-05** from the official pages, for the October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]].
> The raw dumps it mentions (HTML, JSON, posters) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# UNIQLO Thailand — stores, payment, own deals, wallets — October 2026 (ต.ค. 69)

Researcher: `uniqlo-merchant`. Read 5 Oct 2026 (5 ต.ค. 69). Read-only; no Notion. Egress was Hong Kong (`ipinfo.io/country` → HK); nothing needed a Thai IP.

Legend: **Confidence** = `verified (official page)` / `third-party only (<source>)` / `unverified`. "Reading" marks my inference from verified facts.

Related: [[../../promotions/uniqlo-2026|UNIQLO card campaigns (UNO, UNQ, UQN, UQCB, KTC points)]] — the bank terms, verified on 1 Oct.

## Summary for the page

- **Chiang Mai has two UNIQLO stores**, both mall units with their own room numbers, not counters inside a department store: **Central Chiangmai** (ex-Central Festival, Fa Ham, large store, floor 1) and **Central Chiangmai Airport** (floor 2). Reading: both should count for UOB's UNO, which excludes "branches in a department store".
- **In store** UNIQLO takes cash, Thai QR (bank apps), **Visa / Mastercard / JCB** credit and debit cards, Alipay and WeChat Pay. **No Amex.** It does **not** take QR payments funded by a credit card, and it does **not officially accept e-wallets** (TrueMoney, ShopeePay, Rabbit LINE Pay). **UnionPay isn't named** anywhere.
- **Online / app**: Visa, Mastercard, JCB cards (full payment only — no installments), cash on delivery, or Pay in Store. No QR, no wallets, no BNPL, no Amex, no foreign-issued cards.
- **UNIQLO's own money in October**: weekly **Limited Offers** (2–8 Oct, then each Friday–Thursday), some **app-member-only prices**, and four **฿100 coupons** (app download, in store or online; new member, newsletter and birthday, online only), each from ฿1,000. One coupon per order; an item bought with a coupon can be exchanged but not returned. **No 10.10 event**; UNIQLO TH's big sales are **11.11** and the **Arigato (Thank You) Festival** in late November, then **12.12**.
- **Wallets, UnionPay network offers, The 1, malls, government 60/40**: nothing that pays at UNIQLO in October.
- **UNIQLO's bank hub** names **six issuers**: CardX | SCB, KBank, Krungsri, KTC, ttb, UOB. The CardX page still shows a **1 Jul – 30 Sep 2026** campaign (UQC / UQB).
- **Logo**: Commons `File:UNIQLO logo.svg` (public domain, red square `#ed1d24`, white Latin "UNI / QLO"), or UNIQLO's own `https://asset.uniqlo.com/logotypes/uniqlo_roman.svg`.

## 1. Chiang Mai stores (and whether they're "in a department store")

UNIQLO's store locator lists **74 stores in Thailand**, **two of them in Chiang Mai**, both `OPEN` on 5 Oct. There's **no UNIQLO at MAYA, One Nimman, Promenada, Kad Suan Kaew or Jing Jai**, and no roadside store in Chiang Mai. The nearest other northern store is UNIQLO Central Chiangrai.

| Store (locator name) | Mall | Unit / floor | Address (verbatim) | Type | Hours (locator) | Services |
|---|---|---|---|---|---|---|
| **UNIQLO Central Chiangmai** (id 11400014) | **Central Chiangmai** (`เซ็นทรัล เชียงใหม่`), the ex-"Central Festival Chiangmai" on the Chiang Mai–Lampang superhighway, Fa Ham; opened 14 Nov 2013 (th.wikipedia list of Central malls). Anchor: Central Department Store | `ห้อง111 ชั้น1` (unit 111, floor 1) | `เซ็นทรัล เชียงใหม่ ห้อง111 ชั้น1 เลขที่ 99,99/1,99/2 ม.4 ต.ฟ้าฮ่าม อ.เมืองเชียงใหม่ จ.เชียงใหม่ 50000` | `LARGE_STORE` (`ร้านสาขาใหญ่`, large store) | Mon–Fri opens 11:00 (closing time blank in the data); Sat, Sun, holidays 10:00–22:00 | Pay In Store, Click & Collect, parking; 053-288-500 |
| **UNIQLO Central ChiangMai Airport** (id 11400012) | **Central Chiangmai Airport** (`เซ็นทรัล เชียงใหม่ แอร์พอร์ต`), Mahidol Rd, Hai Ya. Anchor: Robinson | `ห้อง254,255/1,255/2,255 ชั้น2` (units 254–255, floor 2) | `เซ็นทรัล เชียงใหม่ แอร์พอร์ต ห้อง254,255/1,255/2,255 ชั้น2 เลขที่ 2,252,252/1 ถ.มหิดล,วัวลาย ต.หายยา อ.เมืองเชียงใหม่ จ.เชียงใหม่ 50100` | `STANDARD_STORE` | Mon–Fri 11:00–21:00; Sat, Sun, holidays 10:00–21:00 | Pay In Store, Click & Collect, parking; 053-283-022 |

- **Sources**: UNIQLO store-locator API `https://map.uniqlo.com/th/api/storelocator/v1/th/stores?limit=100&RESET=true&lang=local&offset=0&r=storelocator` (the data behind <https://map.uniqlo.com/th/th/>); the mall's former name and opening date are from th.wikipedia's list of Central Group malls.
- **Confidence**: verified (official API). The ex-Festival identity is third-party only (Wikipedia), but it matches the Fa Ham address. Older lists still use both names: Central The 1's CPN shop list (Sep 2026) names "เซ็นทรัล เฟสติวัล เชียงใหม่" and "เซ็นทรัล เชียงใหม่" side by side.

**Department-store status, for UOB's UNO.** UNIQLO's UOB page excludes "สาขาที่อยู่ใน department store" (branches located in a department store). That's UNIQLO's own copy of the UOB terms, at <https://www.uniqlo.com/th/th/special-feature/cp/promotion/uob>.

- **Reading: both Chiang Mai stores count for UNO.** Each is a mall tenant unit with its own room number (`ห้อง111 ชั้น1`, `ห้อง254–255 ชั้น2`). Neither is a concession inside Central Department Store at Central Chiangmai or inside Robinson at Central Chiangmai Airport.
- **No list of excluded branches is published.** Neither UOB nor UNIQLO lists which branches the exclusion covers. The UNO campaign isn't even in uob.co.th's own promotion list (`data-promotion.json`, 628 items on 5 Oct). It appears only on UNIQLO's site.
- **No store in the locator is marked as inside a department store.** If the exclusion bites anywhere, the likely candidates by name are the five "The Mall" stores (Bangkae, Bangkapi, Korat, Ngamwongwan, Thapra) and the four Robinson Lifestyle stores (Srisaman, Buriram, Chachoengsao, Kanchanaburi). None is in Chiang Mai.
- **Confidence**: room numbers verified (official API). "Not inside a department store" is a reading; ask at the till if in doubt.

### 1.1 How they appear on statements

- The household's only UNIQLO row so far is Baiboon's ฿990 `UNIQLO-CENTRAL CHIANGMA CHIANGMAI TH` (21 Sep 2026).
  - `UNIQLO-CENTRAL CHIANGMA` is 23 characters, the usual cut of the merchant-name field. "…CHIANGMAI" and "…CHIANGMAI AIRPORT" both cut to the same string, so the row could be **either store**.
  - **Unverified** which. The slip or Baiboon can say.
- The `UNIQLO-<MALL>` shape means UNIQLO's own merchant ID, so it's a standalone store's slip. A UNIQLO paid at a department-store till would post under the store's name (`CENTRAL …` / `ROBINSON …`), which is presumably why banks exclude those branches. **Reading**, not verified.
- How **online orders** post (UNIQLO Online, or a payment gateway's name) is **unknown**. No household row exists yet.

### 1.2 New and closed stores

- **UNIQLO Central Krabi** opened **25 Sep 2026** (locator comment "เปิดให้บริการแล้ว"; <https://www.uniqlo.com/th/th/special-feature/cp/new-store/central-krabi>). There's nothing new in the north.
- **UNIQLO Central Rayong** has been temporarily closed since 29 Sep because of flooding (locator comment). UNIQLO's site also warns of flood-related delivery delays in some areas.

## 2. Payment methods

### 2.1 In store

From UNIQLO's FAQ "ร้านสาขา | การชำระเงิน" (stores | payment), <https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0Ie000000TPQl&l=th>:

| Method | Accepted? | Note |
|---|---|---|
| Cash | yes | |
| QR scan (`สแกนคิวอาร์โค้ด`) | yes | "ขออภัยที่ขณะนี้ยังไม่สามารถรับสแกนคิวอาร์โค้ดจากบัตรเครดิตได้": **QR payments funded by a credit card are not accepted**. The store QR is KBank's: the Pay in Store FAQ treats "สแกนคิวอาร์โค้ดจากแอปพลิเคชัน KBANK" differently from other banks' apps. |
| Credit and debit cards | yes: "**Visa, Mastercard, JCB เป็นต้น**" (Visa, Mastercard, JCB, etc.) | **American Express not accepted.** UnionPay is not named. |
| Alipay, WeChat Pay | yes | For visitors' wallets |
| E-wallets: ShopeePay, TrueMoney Wallet, Rabbit LINE Pay | **not officially supported** | UNIQLO's reason: refunds take longer, the customer has to chase them with the wallet provider, and a return must be of the whole receipt. |

- **Confidence**: verified (official FAQ).
- **UnionPay cards (KTC UnionPay, AEON UnionPay)**: **unverified**. The FAQ's "etc." leaves room, and the store QR is KBank's, but no UNIQLO or UnionPay page names UnionPay at UNIQLO. A third-party search found nothing either way. Try the card at the till; don't plan on it.
- **UnionPay QR** (the 6% offer on KTC UnionPay, [[../../promotions/unionpay-qr]]) is a card-funded QR. UNIQLO says it takes no credit-card QR, so **reading: UnionPay QR 6% can't be used at UNIQLO.**
- **JCB is accepted** in store and online, which matters for KTC JCB's ×2–×5 points and the Krungsri JCB tiers ([[../../promotions/uniqlo-2026]]).

### 2.2 Online and app (uniqlo.com/th, UNIQLO Thailand app)

- **Payment options depend on delivery**, per FAQ "ออนไลน์ | การชำระเงิน", <https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0Ie000000TOqj&l=th>:
  - **Home delivery**: credit/debit card, cash on delivery, or Pay in Store.
  - **Click & Collect**: credit/debit card or Pay in Store.
  - **Not accepted**: Amex, cards issued by banks abroad, and QR payment online.
- **Card networks**: FAQ "การชำระเงินด้วยบัตรเครดิตและบัตรเดบิต", <https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0Ie000000TOk4&l=th>.
  - Its network image shows **Visa, Mastercard and JCB only**. Debit cards starting 462287 (Visa) and 559888 (Mastercard) have been refused since 31 Jan 2025.
  - **Full payment only**: "ยังไม่สามารถเลือกวิธีการชำระเงินแบบ 'การชำระเงินแบบแบ่งจ่าย' และ 'การชำระเงินพร้อมดอกเบี้ยแบบผ่อนชำระ'" (installment plans aren't available yet).
  - One card per order. The card is charged when the order ships from the warehouse.
  - The name on the card must match the account. Under-18s can't use a supplement card or a family member's card.
- **Pay in Store**, <https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0Ie000000TOPY&l=th>:
  - Order online, then pay **within 2 hours** at the chosen store by card, QR (no credit-card QR) or cash. The order then ships (home or Click & Collect).
  - Gift cards can't be used, and the trouser-hemming option isn't available with it.
  - Cancellation is possible within 30 minutes for cash, card or KBank-app QR; other banks' QR payments can't be cancelled.
  - Reading: a Pay-in-Store card payment is a store slip, so in-store bank campaigns should treat it as one.
- **No BNPL** of any kind (SPayLater, TrueMoney Pay Next, Atome …) is offered at checkout. **No wallets online.**
- **Delivery fee**, FAQ "เกี่ยวกับการจัดส่งแบบมาตรฐาน", <https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0fR00000014O9&l=th>, and the packaging-fee FAQ, <https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0fR00000014Pl&l=th>:
  - Home delivery is **free from ฿990**, counted **before** coupon discounts. Below that there's a **฿100** fee per order, which UNIQLO's newer copy calls a packaging fee (`ค่าบรรจุภัณฑ์`). Orders can't be combined to reach ฿990.
  - Delivery takes 1–4 days outside greater Bangkok. Couriers are DHL, LEX (Lazada Express) and J&T (FAQ <https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0Ie000000TOqk&l=th>).
- **Click & Collect**, <https://www.uniqlo.com/th/th/special-feature/click-and-collect>:
  - **Free, no minimum**, at every store, both Chiang Mai stores included (locator flag).
  - Collect within 14 days of arrival. Items can be tried on and exchanged at the store.
  - **Same Day Click & Collect** covers only 40 Bangkok-area stores and is **suspended for now** ("ขณะนี้ ไม่มีการจัดส่งแบบ Same day Click & Collect ชั่วคราว"); collection takes 2–3 working days instead.
- **The app** is "UNIQLO Thailand" (UNIQLO CO., LTD., App Store id 867497451, v26.7.1 of 30 Sep 2026).
  - The app and website were relaunched on **23 Sep 2026**. Everyone must reset their password. Wishlists and carts from before 23 Sep were wiped; unexpired coupons survived. <https://www.uniqlo.com/th/th/special-feature/cp/new-app-web-features>.
- **Confidence**: verified (official FAQ and pages) throughout.

## 3. UNIQLO's own deals in October 2026

### 3.1 Limited Offers (weekly price cuts)

- **Schedule**: Limited Offers change every **Friday**, with new prices from about 01:00 on the start day. Week 1 is **2–8 Oct 2026** (Fri–Thu), which puts the later weeks at 9–15, 16–22, 23–29 Oct and 30 Oct – 5 Nov (reading from the weekly pattern).
- **Where**: the Digital Flyer, "Weekly News 2 ต.ค. 69 – 8 ต.ค. 69", <https://www.uniqlo.com/th/th/special-feature/cp/digital-flyer>, and the Limited Offers list, <https://www.uniqlo.com/th/th/feature/limited-offers/women> (28 items in women's on 5 Oct).
- **Examples, 2–8 Oct**:
  - Sweat full-zip hoodie and pullover ฿1,290 → **฿990**.
  - Barrel / Baggy Barrel jeans ฿1,290 → **฿990**.
  - Denim and stretch shorts ฿790 → **฿590**.
  - Jersey Easy pants ฿790 → ฿590.
  - Sweater polo ฿790 → ฿590.
  - Some items are marked "ออนไลน์เท่านั้น" (online only).
- **App-member prices**: a few items are tagged **"ราคาเฉพาะสมาชิกแอป"** (app-member price). This week: the windproof stand-collar blouson ฿1,490 → **฿1,290** for app members, 2–8 Oct.
- **Price Down** (permanent markdowns): <https://www.uniqlo.com/th/th/feature/sale/women>.
- **Confidence**: verified (official pages).

### 3.2 Coupons (members and the app)

From App Benefits, <https://www.uniqlo.com/th/th/special-feature/app-benefit> (published 24 Sep 2026), and FAQ "ฉันจะได้รับคูปองจากยูนิโคล่ได้อย่างไร?", <https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0Ie000000TOPV&l=th>. The minimum spend fell from ฿1,500 to **฿1,000** on 22 Sep 2026.

| Coupon | Value | Min. spend | Where usable | Who gets it | Validity |
|---|---|---|---|---|---|
| **New App download coupon** (`คูปองสำหรับการดาวน์โหลดแอปครั้งแรก`) | ฿100 | ฿1,000 | **online or in store** | First download of the app plus first registration or link to an online account | 30 days from issue; arrives at first app login |
| **Online Welcome Coupon** (`คูปองต้อนรับสมาชิกใหม่`), new from 22 Sep 2026 | ฿100 | ฿1,000 | online only | First-ever UNIQLO account (existing members don't get it) | 30 days |
| **E-Newsletter coupon** | ฿100 | ฿1,000 | online only | App member subscribing to the newsletter for the first time | to the end of the next month; arrives the next day (FAQ: 1–2 working days) |
| **Birthday coupon** | ฿100 | ฿1,000 | online only | App member with a birth date registered | the birth month; issued on the 1st (1–2 working days if registered during the month) |
| **StyleHint coupon** | ฿100 | ฿1,000 | online or in store | Download StyleHint and log in with the UNIQLO account | 30 days |
| Other coupons | — | — | — | shown in the app under สมาชิก → คูปอง | — |

- **Rules for every coupon**:
  - One coupon per order; coupons can't be combined.
  - **An item bought with a coupon can be exchanged but not returned for a refund.**
  - Used in the cart (online). In store the app coupon is shown at the till (reading from "ใช้ได้ทั้งออนไลน์สโตร์ และทางร้านสาขา", usable both online and in store).
  - Free shipping is counted on the total **before** the coupon.
- **Household angle**:
  - Anyone without a UNIQLO app account (each person needs their own) can take **฿100 off a ฿1,000+ in-store slip** in Chiang Mai, once, with the app-download coupon. The StyleHint coupon gives a second in-store ฿100.
  - **Bank tiers count on the charged amount** (reading). A coupon can pull a ฿3,000 slip down to ฿2,900, below UNO's, UQN's, UNQ's and UQCB's ฿3,000 first tier. Apply a coupon only when the slip stays at or above the tier.
- **Confidence**: verified (official pages).

### 3.3 Events: 15th anniversary, and what's coming in November

- **15th anniversary in Thailand.** UNIQLO opened its first Thai store in September 2011.
  - Page: "LifeWear, 15 Years with Thailand", <https://www.uniqlo.com/th/th/special-feature/cp/anniversary> (published 21 Sep 2026), with monthly "Updated News" from June. The October and November entries say "เร็วๆ นี้" (coming soon).
  - **No anniversary discount, coupon or gift** is on the page so far; it's product storytelling (UV, AIRism, jeans). Third-party: brandbuffet.in.th (May 2026) frames it as a sustainability and brand campaign.
  - **Confidence**: verified (official page), with no money in it yet.
- **No 10.10 event.** UNIQLO TH's site has no 10-10 page, and nothing was found in news or in archived URLs. Shopee's 10.10 isn't UNIQLO's (no official Shopee store, §3.4). **Confidence**: unverified as an absence; checked on the site, in the Wayback captures since 2024 and in news.
- **November pattern, from past years** (dates for 2026 not announced):

  | Event | 2024 | 2025 | 2026 so far |
  |---|---|---|---|
  | **11.11 "Double date"** | `special-feature/11-11` live from ~8 Nov | **7–13 Nov 2025** | `special-feature/11-11` exists, currently a generic promotion list |
  | **ARIGATO FESTIVAL** (`Thank You Festival`, UNIQLO's 感謝祭) | ~22–28 Nov 2024 (first-day and last-day posts 22 / 28 Nov) | **21 Nov – 4 Dec 2025** (KTC's window) | **29 May – 4 Jun 2026** (spring edition) |
  | **12.12 "Double date"** | `special-feature/12-12` posts from 6–10 Dec 2024 | **12–18 Dec 2025** | — |

  - Sources: KTC's UNIQLO pages <https://www.ktc.co.th/promotion/shopping/apparel-bags-shoes/uniqlo-special> (2025 windows: "Double date 11/11 (7 พ.ย. 68 - 13 พ.ย. 68), ARIGATO FESTIVAL (21 พ.ย. 68 - 4 ธ.ค. 68) และ Double date 12/12 (12 ธ.ค. 68 - 18 ธ.ค. 68)"; that redemption paid 13% / 16% / 20% at ฿3,000 / 5,000 / 8,000 per slip with SMS `UNQ`) and <https://www.ktc.co.th/promotion/shopping/apparel-bags-shoes/uniqlo-arigato> (29 May – 4 Jun 2026). The 2024 rows come from Wayback captures of `uniqlo.com/th/th/special-feature/thank-you`, `/11-11` and `/12-12`, whose `utm_term` values carry the post dates.
  - Third-party (marketeeronline, brandbuffet): Arigato Festival 24–30 Nov 2023 and 2–8 Jun 2023.
  - **Reading for the plan**: expect **11.11 around 6–12 Nov** and an **Arigato Festival in the last week of November 2026**. Banks have re-run event-only boosts then (KTC's 13–20%), so a big UNIQLO purchase may be better left to November.
  - **Confidence**: past dates verified (KTC's official pages, UNIQLO's archived URLs); 2026 dates unverified.

### 3.4 Other own offers checked

- **Shopee / Lazada / LINE shops**: **no official UNIQLO store found**.
  - UNIQLO's own pages name only its stores, uniqlo.com and the UNIQLO app as sales channels; Krungsri's page says "ร้านค้ายูนิโคล่ ทุกสาขา และ ออนไลน์สโตร์ www.uniqlo.com หรือ แอป UNIQLO".
  - Lazada appears in UNIQLO's FAQ only as a courier (LEX).
  - A web search found only third-party resellers. Shopee and Lazada search pages were captcha-walled, so they couldn't be read directly.
  - **Confidence**: unverified (absence).
- **Gift cards**: <https://www.uniqlo.com/th/th/special-feature/gift>. No October bonus found. Gift cards can't pay a Pay-in-Store order.
- **Student discount, recycle coupon, alteration offers**: none found.
  - RE.UNIQLO takes clothes for donation at every store ("Warmth for all"), with no coupon in return.
  - RE.UNIQLO STUDIO repairs and embroidery are paid services: 10 baht per letter after the 10th, per <https://www.uniqlo.com/th/th/special-feature/re-uniqlo>.
- **New-email-subscriber ฿100** is the same coupon as in §3.2. The home-page tile <https://www.uniqlo.com/th/th/member/e-news/subscription> says "รับคูปองมูลค่า 100 บาท* สำหรับสมาชิกอีเมลใหม่".
- **Collaborations** (product drops, not payment deals): UNIQLO : C, Uniqlo U, JW ANDERSON, Comptoir des Cotonniers; UT: KAWS UNIVERSE, Disney × Formula 1, mofusand, Sanrio, CHIIKAWA, MANGA UT Shueisha 100th, Monchhichi, Stitch in Thailand (hub nav, 5 Oct).
- **VAT refund for tourists**: not relevant.

## 4. Wallets and BNPL at UNIQLO

| Wallet / BNPL | At UNIQLO? | October offer at UNIQLO | Confidence |
|---|---|---|---|
| **TrueMoney** (wallet, Pay Next, linked cards) | Not officially accepted in store (FAQ above); not online | **None.** No UNIQLO page among TrueMoney's promotions (search on truemoney.com via r.jina.ai). Pay Next's 3% round (1 Oct – 31 Dec, see [[merchants-wallets]]) needs a participating shop; UNIQLO isn't one as far as anything shows. | verified (UNIQLO FAQ); offer absence unverified |
| **ShopeePay / SPayLater** | Not officially accepted. SPayLater can technically scan a merchant's PromptPay QR (Shopee Help Center 183049), but UNIQLO discourages wallets because refunds are slow | None | verified (FAQ); technical QR use is a reading |
| **Rabbit LINE Pay / LINE Pay** | Not officially accepted | None (LINE Pay's promotions page was empty on 30 Sep, per [[merchants-wallets]]) | verified (FAQ) |
| **Alipay / WeChat Pay** | **Accepted** in store | None for Thai users. Alipay+ is for inbound wallets. | verified (FAQ) |
| **UnionPay QR** (KTC Mobile, 6% offer) | Card-funded QR isn't accepted | **Not usable** (reading). October's 6% pool (offer `260723112620`) was 48.9% left on 5 Oct, for wherever it does work. | reading from verified facts |
| **UnionPay mobile NFC 3%** (Apple Pay / Huawei Pay / Samsung Pay … with a UnionPay card, "【Thailand】UnionPay Mobile Payment Instant Discount 3% OFF", offer `260226111820`, 1 Mar – 31 Dec 2026) | Only if UNIQLO's terminals take UnionPay contactless — unverified | 3% off, up to ฿100 a transaction, 3 a day and 6 (฿600) a month, no registration; **pool reads 0% left on 5 Oct** (`flushProcess` percent 0.0; UnionPay's page then shows the budget used up). Whether the household's KTC / AEON UnionPay cards can be added to a phone wallet at all is unknown. | verified (UnionPay API); usability unverified |
| **KBank QR / MAKE by KBank / other bank apps** | Paying the store's Thai QR from a bank account works | None found | verified (FAQ) |
| **dolfin** | not checked (believed closed) | — | unverified |

- UnionPay offer data: `GET https://marketing.unionpayintl.com/h5Promote/v1/merchant/getMerchantList?countryCode=764&pageIndex=1&pageSize=50&insCode=299990156&language=en` lists 17 offers (Thai and regional). **None names UNIQLO.** Terms come from `POST …/coupon/getCoupon`.
- **Bank terms also shut wallets out**: KBank's UQN excludes "ยอดใช้จ่ายที่ชำระเงินผ่าน E-Wallet (เช่น True Money, Rabbit Line Pay, ShopeePay เป็นต้น)" (spend paid through an e-wallet), per <https://www.uniqlo.com/th/th/special-feature/cp/promotion/kbank>. **Pay UNIQLO with the card itself.**

## 5. Mall-level campaigns (Central Chiangmai, Central Chiangmai Airport)

- **The 1 points at UNIQLO: no.**
  - UNIQLO isn't a Central Retail brand, and it's **not on CPN's list of The 1 participating shops** in Central malls. That list is `x4-202609.pdf`, 8 pages, read in full, used by the REDZ ×3/×4 plaza-zone offer; source <https://www.centralthe1card.com/getmedia/d85d8b10-d499-4b48-93a2-21c17ead3b8d/x4-202609.pdf>.
  - So giving a The 1 number at UNIQLO earns nothing, and Central The 1 cards (REDZ) earn only their base 1 point per ฿25 there ([[the1]]).
  - **Confidence**: verified (official list; UNIQLO is absent).
- **CPN "ก้าวรับพอยท์" (1–31 Oct)**: walk 5,000 steps in the **Central X** app at a Central mall and get 500 The 1 points from the mall.
  - The **card extra** (+500 points for a REDZ slip of ฿500 or more) counts only "ร้านค้าที่สะสมและแลกพอยต์เดอะวันได้ … (โซนพลาซา)" (shops that earn and burn The 1 points, plaza zone).
  - **Reading: a UNIQLO slip doesn't qualify**, since UNIQLO isn't on that list. Check at customer service if it matters.
  - Source: `?modalId=cpn-202610` on centralthe1card.com.
- **Central Department Store / Robinson events** (Central Midnight Sale to 5 Oct, Robinson Payday to 4 Oct, Central App Monthly Q4) count only **inside** the department stores. UNIQLO is a separate tenant, so they **don't apply** ([[the1]] §B3).
- **CPN mall-wide October campaigns for Chiang Mai** (spend-and-get e-coupons, Central X app deals) **couldn't be read**: centralpattana.co.th puts up an AWS WAF captcha for curl, r.jina.ai and headless Chrome, and has no recent Wayback captures. Nothing found in news either. **Unverified / not found.** The Central X app or the mall's customer-service desk is the place to check.
- **Bank × mall campaigns**:
  - UOB's mall-wide ones in October (CPN Generic points → up to 13%, Weekend Surprise) don't name UNIQLO, and Weekend Surprise covers restaurants only.
  - UOB's Central Rama 9 grand opening (6 Oct – 2 Nov) is in Bangkok.
  - Details belong to the bank researchers.

## 6. Government programmes

- **"ไทยช่วยไทย พลัส (60/40) (เพิ่มเติม)"**, 1 Oct – 30 Nov 2026 (details in [[merchants-wallets]] §1.4): eligible shops are non-juristic operators, small juristic persons with revenue up to ฿1.8M, Blue Flag (ธงฟ้า) and community shops, and the like.
  - **UNIQLO isn't eligible.** It's run by UNIQLO (Thailand) Co., Ltd., a large company, from mall units, and nothing lists it as a participant.
  - **Confidence**: reading from the official criteria.
- **Easy E-Receipt / tax-deduction shopping**: **no scheme runs in October–December 2026**. Past rounds ran in January–February.
  - UNIQLO's FAQ has a tax-invoice category (`ใบกำกับภาษี / VAT Refund`); whether it issues e-tax invoices wasn't checked. That would matter only if a 2027 round is announced.
  - **Confidence**: third-party only (news search).

## 7. UNIQLO's bank promotion hub (for cross-checking the bank researchers)

- **Hub**: <https://www.uniqlo.com/th/th/special-feature/cp/promotion>, titled "Credit Card Promotion", with the banner "1 ต.ค. 2569 - 28 ก.พ. 2570".
- **Strap**: "สิทธิพิเศษเมื่อซื้อสินค้าตั้งแต่ 3,000 บาทขึ้นไปที่ร้านสาขาหรือออนไลน์สโตร์" (privileges on purchases from ฿3,000 in store or online).
- **Six issuers**, each with a page published 30 Sep 2026 17:00 GMT:

| Bank (as named) | Page | Codes / dates seen in the page text | Notes |
|---|---|---|---|
| **CardX \| SCB** | `/promotion/cardx` | `UQC`: cashback, register once, SMS → 4545777. `UQB`: POINTX → up to 12% cashback, SMS every slip → 4545777. **Period in the text: 1 Jul – 30 Sep 2026** | Still linked from the hub on 5 Oct with the **expired** Q3 text. CardX's own site should be checked for an October successor (bank researchers). Not in [[../../promotions/uniqlo-2026]]. |
| **KBank** | `/promotion/kbank` | `UQN` (K PLUS or SMS → 4545888), 1 Oct 2026 – 28 Feb 2027, ฿600 a month, ฿3,000 for the campaign; extra K Point up to 1,200 a month | Excludes KBank Smart Pay 0% and **e-wallet payments (TrueMoney, Rabbit LINE Pay, ShopeePay)** |
| **Krungsri** | `/promotion/krungsri` | See below | The JCB Ultimate 5× line is newer than [[../../promotions/uniqlo-2026]] |
| **KTC** | `/promotion/ktc` | KTC JCB ×2 / ×3 / ×5 points, 1 Jul – 31 Dec 2026. KTC FOREVER points → cashback: SMS **`UNQ`** + 16 digits → **0613845000**, or `ktc.promo/uniqlo2026`, on each day you spend, 1 Oct 2026 – 28 Feb 2027 | KTC's redemption code is also `UNQ`: the same letters as Krungsri's, sent to a different number |
| **ttb** | `/promotion/ttb` | 1 Oct 2026 – 28 Feb 2027. Cashback for registered cards (ttb touch or SMS). Points: 1,000 ttb rewards plus → 12% cashback, from ฿3,000 a slip, up to 12,000 points a month | The codes are only in the banner image (repo: `UQCB`, `UQBP`) |
| **UOB** | `/promotion/uob` | See below | Excludes branches in a department store and UOB LADY LUXE PAY. UNO is **not** in uob.co.th's own promotion JSON. |

- **Krungsri** (`/promotion/krungsri`):
  - **Cashback**, `UNQ` (UCHOOSE, or SMS → 081-927-9999, register once): ฿150 per ฿3,000. From ฿10,000: 8% (฿800) on Krungsri JCB, 7% (฿700) on the others.
  - **Points → 10% cashback** via UCHOOSE, 1 Jan – 31 Dec 2026.
  - **Krungsri JCB Platinum 3×**, 1 Oct 2026 – 31 Dec 2027, up to 400 bonus points a month.
  - **Krungsri JCB Ultimate 5×** from **21 Oct 2026**, up to 1,600 bonus points a month.
- **UOB** (`/promotion/uob`):
  - **Cashback**, `UNO` (SMS → 4545111 or TMRW Rewards+, **every time**, within the day): ฿150 per ฿3,000, or ฿800 from ฿12,000; ฿800 a month, ฿4,000 for the campaign.
  - **Top Spender**: 5 × 20-inch luggage (฿6,800) for the top spenders, minimum ฿10,000.
  - **Points**: `PPF` → 10–13% cashback.
- **Help lines on the hub**: CardX 1468 / SCB 02-777-7777, K-Contact 02-888-8888, Krungsri 02-646-3555, KTC 02-123-5000, ttb 1428, UOB 0-2285-1555.
- **Confidence**: verified (official pages, read through r.jina.ai).

## 8. Logo for the cover

- **Wikimedia Commons**: `File:UNIQLO logo.svg`.
  - It exists: 204×203 SVG, <https://upload.wikimedia.org/wikipedia/commons/9/92/UNIQLO_logo.svg>, licence "Public domain" (trademarked).
  - It's the **red square (`#ed1d24`) with white Latin "UNI / QLO"** on two lines. It has **no katakana**.
  - The Latin + katakana double square is `File:Uniqlo logo Japanese.svg` (1000×444). There's also a `File:UNIQLO logo (Japanese).svg`.
- **UNIQLO's own**: <https://asset.uniqlo.com/logotypes/uniqlo_roman.svg> (256×256 viewBox, `fill="red"`, white letters; curl works). The favicon is `…/uniqlo_roman.ico`.
- **Brand colour**: UNIQLO red, `#ED1D24` (Commons file); UNIQLO's own SVG uses pure `red` (`#FF0000`).
- **For the cover**: the square logo on a white plate. **Icon**: 👕.

## 9. Not found / unconfirmed

1. Which Chiang Mai store Baiboon's ฿990 row came from (the descriptor is truncated).
2. Whether UNIQLO's terminals take **UnionPay** cards or UnionPay contactless.
3. Which branches UOB's "department store" exclusion covers (no list published anywhere).
4. CPN mall-wide October campaigns at the two Chiang Mai malls (site behind a captcha).
5. 2026 dates for 11.11, the Arigato Festival and 12.12 (not announced on 5 Oct).
6. How UNIQLO online orders appear on statements.
7. Whether CardX has an October UNIQLO successor to UQC / UQB (the hub still shows the Q3 text).

## Site methods (for [[../research-methods|research methods]])

- **uniqlo.com/th** (Akamai): curl with full browser headers and a cookie jar, and headless Chrome, both got **403 "Access Denied"** from the Hong Kong egress on 5 Oct. **`r.jina.ai/<url>` reads every page** (promotion hub, bank pages, Digital Flyer, Limited Offers, App Benefits, anniversary) in full.
  - Parallel requests trip a 403 too. Fetch **one at a time**, retry after ~8 s, and treat a reply under ~2 KB as a block.
  - The product tiles carry the price window ("โปรโมชันพิเศษ ตั้งแต่ 2 ต.ค. 2026 - 8 ต.ค. 2026", "ราคาเฉพาะสมาชิกแอป").
- **Store locator API** (no block, plain curl): `https://map.uniqlo.com/th/api/storelocator/v1/th/stores?limit=100&RESET=true&lang=local&offset=0&r=storelocator`.
  - It returns all 74 stores with `name`, `address`, `storeType`, opening hours, `clickAndCollectFlag`, `payAtStoreFlag` and `businessStatusShortComment` (new and closed stores).
  - Use `limit=100`: paging with `offset=50` returned the first page again. Provinces come from `/th/api/storelocator/v1/th/states?r=storelocator&lang=local`. The path pattern is in the locator's `static/js/main.*.js`.
- **faq-th.uniqlo.com** (Salesforce knowledge base) reads through r.jina.ai.
  - Articles open by `?id=<kA0…>&l=th`. Category listings open by `?l=th&c=category_uq_th:UQTH_CAT06_01` (payments; `CAT07_01` delivery, `CAT02_04` coupons, `CAT04_01` stores). Search is `?q=<term>&l=th&fs=Search&pn=1`.
  - Images (the accepted-card logos) come from `/servlet/rtaImage?eid=…` with plain curl.
- **Past event dates**: UNIQLO doesn't keep old event pages. **KTC's UNIQLO pages** (found by grepping KTC's promotion sitemaps for `uniqlo`) quote UNIQLO's event windows (Double date 11/11, ARIGATO FESTIVAL, 12/12). The **Wayback CDX** of `uniqlo.com/th/th/*`, filtered on `festival|thank|11-11|12-12`, dates past campaigns from their `utm_term` values.
- **Does UNIQLO earn The 1?** Grep CPN's participating-shop PDF (`x4-202609.pdf`, linked from `?modalId=cpn-x3-202308` on centralthe1card.com) after `pdftotext -layout`.
- **centralpattana.co.th** returns an AWS WAF captcha ("Human Verification") to curl, r.jina.ai and headless Chrome, and has no useful Wayback captures from Aug 2026 on. Mall campaigns need the Central X app or the user.
