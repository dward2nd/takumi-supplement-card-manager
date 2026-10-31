---
tags: [catalogue-research, 2026-11]
researched: 2026-11-01
---

> **Research snapshot**: The 1 membership, the Central The 1 credit card, GO Wholesale's own deals and the network offers at Central Retail — November 2026 research. Read on **2026-11-01** from the official pages, for the November 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages (Makro, GO Wholesale, Shopee, The 1, Shell, PTT). Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions stayed in the session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# The 1 — November 2026 (พ.ย. 69): membership, Central The 1 card, GO Wholesale, networks at Central Retail

Researcher: `the1`. Read 1 Nov 2026, ≈ 09:00–12:00 Bangkok time.

- **Card list**: `POST https://www.centralthe1card.com/gcspromotion` returned **184 promotions** (168 on 1 Oct). Each page is `https://www.centralthe1card.com/promotion?modalId=<code>`. Tier tables and SMS codes were read from the posters (`/getattachment/<guid>/…webp`).
- **GO Wholesale**: the WordPress list `/wp-json/wp/v2/promotions` (240 items) fetched from inside headless Chrome, plus the rendered `/promotion/` page and `/store-location/`.
- **Membership**: the1.co.th (Nuxt bundle `40c7dd4.js` is the same file as in October, so the earn-rate text is unchanged), Caltex's The 1 page, central.co.th through r.jina.ai.
- **Networks**: Visa Thailand's perks API (captured over CDP), UnionPay's offer list, JCB's Thai campaign list, KTC's Visa × The 1 page. Mastercard Priceless was down for maintenance.

**Confidence labels**: **V** verified on the official page today · **R** my reading of official terms · **T** third-party only · **U** unverified.

**Central The 1 card registration**: SMS `<CODE> <16-digit card number>` to **081-278-2222**, or free in **UCHOOSE** (keyword given per item). Every code counts spend only **after** the confirmation SMS arrives. Supplement spend (Baiboon's REDZ supplement) pools with Takumi's primary account, and cashback lands on the primary.

**Household fit**: REDZ (Mastercard) is Takumi's primary plus Baiboon's supplement; Nuta holds no Central The 1 card. GO Wholesale has a **Chiang Mai branch** (201 หมู่ 7 ต.สุเทพ อ.เมืองเชียงใหม่, 052-079-553) and two in Chonburi: **Amata** (103/69 หมู่ 12 ต.นาป่า อ.เมืองชลบุรี, 033-265-255, the nearest to Bang Saen) and South Pattaya. Central Retail in Chiang Mai: Central Chiangmai (Festival) and Central Chiangmai Airport (with Robinson). Source: `centralfoodwholesale.co.th/store-location/` **V**.

---

## 1. Headline changes vs October

**Successors found**
1. **GWS3 → GWS4** (GO, 1 Nov 2026 – 31 Jan 2027): identical tiers ฿35 / 95 / 400 / 1,800 and caps (฿9,000 a slip a month, ฿27,000 a campaign). **Register `GWS4` again** (081-278-2222). GO's own copy titles it "1 พ.ย. 69 – 1 ม.ค. 70", but its body and the card site say **31 Jan 2027**.
2. **SE10 → SE11** (Shell, ฿100 back on one slip ≥ ฿100, first 1,500 a month; December's code is already printed: SE12).
3. **SO10 → SO11** (Starbucks / Boost ฿100 e-coupon, first 1,500 a month; December: SO12).
4. **PTT (`PTT` code, 3–4% at ≥ ฿1,000) → "กรุงศรีเปย์เซฟ II"** (Krungsri PaySave II, `ksc-202610`, 1 Nov 2026 – 28 Feb 2027): **PTT Station 5%** on a fill ≥ ฿1,000, **฿50 a slip a day, ฿100 a month**; it also replaces **EAT** (dining 10% on ≥ ฿1,000, ฿300 a month) and adds travel 3%. Registered once in UCHOOSE, keyword `SAVE`.
5. **EVT2 → EVT3** (EV charging, 1 Nov 2026 – 28 Feb 2027): ฿50 / 100 / 150 at ฿1,000 / 2,000 / 3,000 a month, ฿600 a campaign (was ฿450). PTT's **EV Station PluZ** app counts.
6. **TNL → TYE** "ช้อปข้ามปีกับ T1" (online category ladder, 1 Nov 2026 – 28 Feb 2027): ฿100 / 350 / 850 / 2,000 at ฿15k / 50k / 100k / 200k a month, ≥ 5 shops a month; Makro online and QR at Makro are excluded.
7. **CMN3 / RPAY9 / Midnight Sale → Central 79th Anniversary `CDS79` (to 2 Nov) · Robinson Payday 10 `RPAY10` (ends today) · Robinson Season of Giving `RBS1` (2–24 Nov)**.
8. **Central App Midnight Sale → Central App 11.11 Marathon Sale** (1–13 Nov): ฿150 / 500 / **1,000 / 2,000** off at ฿3k / 5k / 10k / 20k, or REDZ 5%.
9. **PWB3 → PWB4** is now published (8 Oct 2026 – 6 Jan 2027), with changed top tiers.
10. **Power Buy / Central Beauty points burns → "Super Burn Day"** at Central and Robinson (1 Nov – 31 Dec): burn points equal to the purchase → **20% off Sat–Sun, 13% other days**.

**New in November**
- **GWSE** (GO 3rd anniversary, 14 Oct – 24 Nov): **+฿300** once total GO spend on the card reaches **฿50,000** in the period. Published mid-October; not in October's report.
- **GWNY** (GO New Year baskets, 28 Oct 2026 – 5 Jan 2027): ฿40–1,600 per slip on hampers, chicken essence and bird's nest only.
- **CPN Year End** (all Central malls' plaza zones incl. both Chiang Mai Centrals, 30 Oct 2026 – 3 Jan 2027): ฿100 / 300 / **2,000** per slip at ฿5k / 10k / 50k; register at the mall counter the same day; supplements get their own quota.
- **Krungsri × Central Retail `CRC`** (not the Central The 1 card — Krungsri VISA/JCB/Lady/NOW): ≥ ฿10,000 accumulated in November at Central Retail stores including **GO** → **฿2,000** cashback; **SMS only, from 07:00 on 1 Nov, first 2,200 registrants**. See §4.3. **Time-critical.**
- GO's member coupons for its 3rd anniversary: **1,000 points → ฿250 off ≥ ฿3,000**, and **800 → ฿150 off ≥ ฿1,500** of fresh / frozen A Choice / Super Save goods.
- GO **"The 1 Super Burn Weekend"** (Fri–Sun, 1,000 points → ฿200 off ≥ ฿2,500, 4 Sep – 27 Dec) is live in GO's WordPress but not linked from the list page; October's report missed it.

**Ended 31 Oct with no successor found**
- **CRC × Visa ฿500 The 1 cash coupon** (KTC's page now says "โปรโมชั่นหมดอายุ"; GO lists it as 21 Aug – 31 Oct). No November Visa offer at Central Retail on Visa's portal, GO or the card site.
- **T1 MAGICAL DAY** (1–13 Oct), **HBF** Happy Health & Beauty Fest, **CPN dining "มื้อนี้ดีลดี"**, **ก้าวรับพอยท์**, the LUXE upgrade offer, the iPhone 18 Power Buy page, **KTC Visa ฿750 at GO**, **Krungsri SUP1/SUP2** (→ Krungsri's GO/Tops **SU1/SU2**, see §4.3), **KBank HYP** (→ **TSU**, §4.3).
- GO: **The 1 Hug the Earth** (27 Oct), the mid-month **Extra Point** (800 points at ฿8,000, 16–25 Oct), **The 1 PAYDAY** October round (25–31 Oct). No November PAYDAY posted yet (Sep ran 25 Sep – 1 Oct, Oct 25–31 Oct).
- **Caltex × The 1** (earn 1 point a litre, burn 800 → ฿100 at the pump) runs **to 30 Nov 2026** on Caltex's page — watch for a renewal.

---

## 2. The 1 membership (no Central The 1 card needed)

### 2.1 Earn and point value — unchanged

The the1.co.th bundle is byte-identical to October's (`40c7dd4.js`), so the base rates in [[../2026-10/the1|October's report §A1–A3]] stand: **1 point per ฿25** at Central, Robinson, Tops, Muji, B2S, SuperSports, Matsukiyo, CMG; **1 per ฿50** at Power Buy, Thai Watsadu, OfficeMate; **1 per ฿100 at GO** (membership linked to The 1). Standard burn **800 points = ฿100** (฿0.125 a point). **R**

Standing app rewards shown on the1.co.th today: Starbucks e-coupon for 800 points, Major Cineplex ticket for 1,290, SF ticket for 1,490, Welcome coupons worth ฿2,000 on first app login. **V** (`the1.co.th` home banners; they're evergreen.)

### 2.2 Better point burns in November

| Burn | Rate | ฿ a point | Where / who | Period | Limits | Conf. |
|---|---|---|---|---|---|---|
| **GO Super Wednesday** | 800 → ฿200 off a receipt ≥ ฿2,500 | **0.25** | GO, any member linked to The 1 | Wednesdays 4, 11, 18, 25 Nov (claim Wed, use Wed–Sun) | 300 rights a round, 1 per member | V `…/promotion/the1-super-wednesday/` |
| **GO 3rd-anniversary coupon 1** | 1,000 → ฿250 off ≥ ฿3,000 | **0.25** | GO member | title 28 Oct – 10 Nov; body says claim and use **14 Oct – 24 Nov** | 2,000 rights, 1 per member | V (dates conflict) `…/promotion/the1-3rdanniversary/` |
| GO 3rd-anniversary coupon 2 | 800 → ฿150 off ≥ ฿1,500 of fresh food / frozen A Choice / Super Save | 0.1875 | GO member | 28 Oct – 10 Nov | 2,000 rights, 1 per member | V same page |
| **GO Super Burn Weekend** | 1,000 → ฿200 off ≥ ฿2,500 | 0.20 | GO member | Fri–Sun, 4 Sep – 27 Dec | 300 a round, 1 per member | R — live in GO's WordPress (`the1-super-burn-weekend`, modified 28 Sep), not linked from the list page |
| GO The 1 Exclusive coupon | ฿300 off ≥ ฿12,000 (no points) | — | The 1 Exclusive only | all 2026 | 1,000 a month | V `…/the1-exclusive/` |
| GO The 1 PAYDAY | 1,500 → ฿400 off ≥ ฿4,500 | 0.267 | GO member | Oct round 25–31 Oct **ended**; Nov round not posted | 1,000 rights | V (Oct) |
| **Central & Robinson Super Burn Day** (card) | points = purchase → **20% off Sat–Sun, 13% other days**; 800–10,000 points a slip | **0.20 / 0.13** | **Central The 1 card only**, at Central and Robinson stores incl. KIS, UCHOOSE QR; not Central App, Muji, gift cards, Central Embassy / U-Tapao / Village | 1 Nov – 31 Dec | balance paid with the card; can stack with card cashback and special points, **not** with another points-burn discount | V `?modalId=cen-rbs-202611` |
| SuperSports redeem (card) | points = purchase → 13–18% | 0.13–0.18 | T1 card | to 31 Dec | | V `ssp-202610` (continues) |
| OfficeMate redeem (card) | 12.5% | 0.125 | T1 primary only | to 31 Dec | | V `ofm-store-online-202605` |
| Power Buy redeem (card) | 15% Fri–Sun / 12.5% Mon–Thu | | T1 card | **ends today, 1 Nov** | | V `pwd-redeem-point-202609` |
| Caltex at the pump | 800 → ฿100 off fuel | 0.125 | any member, ID card at participating Caltex | to **30 Nov 2026** | ≤ 100 L a fill, 2 fills a day, 400 L a month | V caltex.com |

**Takeaway**: the GO burns at ฿0.25 a point (Wednesday 800 → ฿200; anniversary 1,000 → ฿250) double a point's value; the card's Super Burn Day pays ฿0.20 on Central/Robinson weekend slips.

### 2.3 Member deals (no card)

- **Robinson Season of Giving** (2–24 Nov, all Robinson branches incl. Central Chiangmai Airport): discount stickers "up to 20%" (+ up to ฿90 more with participating cards), **2,000 The 1 points** for using all 3 sticker colours with ≥ ฿5,000 accumulated over the campaign, a car draw entered by burning The 1 points (T1 card holders get 10 rights per ฿1,000 slip without burning), and on **20–22 Nov** a ฿5,000 Robinson gift card at ≥ ฿80,000 (1 per member). **V** central.co.th `robinson-season-of-giving-30-oct26` (via r.jina.ai); sticker mechanics at the store.
- **GO fresh-vegetable coupon** (28 Oct – 10 Nov): ≥ ฿300 of listed vegetables per receipt → ฿90 coupon; **14 per member** over the round. **V** `…/fresh-vegetable-coupon/`.
- **GO weekly price deals** "GO ฉลองครบรอบ 3 ปี" (28 Oct – 3 Nov) and the 3rd-anniversary e-catalogue (28 Oct – 10 Nov): prices, not payment offers. **V**
- **Caltex × The 1**: 1 point a litre, 5 points per ฿25 of engine oil (≤ ฿4,000 a month), burn as above; **valid to 30 Nov 2026**. **V** `caltex.com/th/motorists/rewards-and-offers/the-1-card.html`.
- **No member-wide November point event** (Point Festival, 11.11 double points, Robinson 11.11 burn) was found. The 1 app's own feed isn't public: the1.co.th's `/the1today/articles/<n>` and `/rewards/<uuid>` pages (≈ 24,000 and ≈ 700 in the sitemap) render client-side and returned only the home banners. **U**

### 2.4 Fuel partners: Shell and PTT

- **Caltex** is The 1's only fuel partner on the1.co.th (listed in the The 1 BIZ partner text and a success story) and on Caltex's own page. **V**
- **Shell**: no tie with The 1 found — not on the1.co.th, not in search. Shell's only Central-group link is the **card** code SE11 (§3.3). **U** (absence)
- **PTT**: a PTT Blue Card ↔ The 1 point transfer existed (MGR Online 2016, "สุขทุกการโอน โดนทุกคะแนน": 1,000 The 1 → 500 Blue Card; 500 Blue → 500 The 1). Nothing current confirms it; the1.co.th only says points can be transferred to partners "including … gas station" without naming them. **T, dated** — treat as unconfirmed. The card side has PTT via PaySave II (§3.3).

---

## 3. Central The 1 credit card (General Card Services / Krungsri Consumer)

### 3.1 GO Wholesale (card)

| Item | Mechanic | Caps | Register | Period | Conf. |
|---|---|---|---|---|---|
| **GWS4** | per slip, in store and GO app, full pay and installments after discounts: **฿3,000–7,499 → ฿35; ฿7,500–29,999 → ฿95; ฿30,000–119,999 → ฿400; every ฿120,000 → ฿1,800** | ฿9,000 a slip per primary account a month; **฿27,000 a campaign** | **`GWS4` → 081-278-2222** or UCHOOSE, on or before the first spend day | **1 Nov 2026 – 31 Jan 2027** (GO's title says 1 Jan; body and card site say 31 Jan) | V `?modalId=go-wholesale-202611`; GO `t1-cashback-27000-nov26` |
| **T1 points at GO** | **10 points per ฿100 a slip** = 9 from the card (supplement's go to the primary's The 1) + 1 from the GO member number linked to The 1 | — | — | ongoing | V (GWS4 T&C) |
| **GWSE** (3rd anniversary) | **+฿300 once total spend reaches ฿50,000** over the period (full pay + installments, store + online) | ฿300 per primary account | **`GWSE`** → 081-278-2222 / UCHOOSE | **14 Oct – 24 Nov** | V `?modalId=go-wholesale-202610`; GO `t1cc-anniversary-oct26` |
| **GWNY** (New Year baskets) | per slip, **only hampers / chicken essence / bird's nest** from the catalogue: ฿3,000–5,999 → GO ฿200 off + **฿40**; ฿6,000–9,999 → ฿500 + **฿100**; ฿10,000–29,999 → ฿1,100 + **฿200**; ฿30,000–59,999 → ฿3,900 + **฿700**; ≥ ฿60,000 → ฿9,000 + **฿1,600** (store discount + card cashback) | card cashback ฿8,000 per primary account (primary + supplement together), credited within 60 days after the end; the GO discount column is under GO's own hamper terms (e-wallets excluded), and whether it needs the card isn't stated | **`GWNY`** → 081-278-2222 / UCHOOSE; the poster says before the purchase, the T&C "by the purchase day" (counts from confirmation) | 28 Oct 2026 – 5 Jan 2027 | V `?modalId=go-wholesale-new-202610` (poster); GO `t1cc-hamper-oct26` |
| 0% for 3 months | participating items, ≥ ฿1,500 a slip | | | ongoing | V |
| Card sign-up (new applicants) | GO e-coupons up to ฿5,500 | | | 1 Nov 2026 – 31 Mar 2027 | V GO `signup-ct1-gws-nov26` (not for the household) |

- **Exclusions (GWS4/GWSE/GWNY)**: tenant shops, restaurants, mail order, commercial buying, non-EDC transactions, **every e-wallet**. No "not combinable" line in GWS4, GWSE or GWNY. **R**
- **Crediting**: GWS4 within 7 days of the merchant's billing; GWSE within 7 days after 24 Nov. **V**

### 3.2 Tops, department stores, malls (Chiang Mai: Central Chiangmai, Central Chiangmai Airport + Robinson)

- **TOPS4** continues (1 Oct – 31 Dec): per slip ฿30 per ฿1,000 · ฿170 at ฿5,000–14,999 · ฿600 at ≥ ฿15,000; ฿600 a month, ฿1,800 a campaign; **+฿300 for ≥ ฿3,000 in each of Oct, Nov and Dec**; ×3 points. Its box says "ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ". **V** `top-cashback-202610`
- **Central 79th Anniversary `CDS79`** (6 Oct – **2 Nov**, Central stores + Chat & Shop): store coupon per day ฿100 / 700 / 3,500 + card cashback per slip **฿100 / 600 / 2,500** at ฿3,000 / 15,000 / 50,000; ฿2,500 a slip, ฿25,000 an account. **V** `cen-anniver-202610`. Mastercard extra: one slip ≥ ฿100,000 on any Mastercard → 100,000 The 1 points (30 rights). **V** `cen-79-anv-mastercard-202610`
- **Robinson Payday 10 `RPAY10`** (22 Oct – **1 Nov, today**): coupon + card cashback ฿50 / 350 / 800 / 2,500 at ฿2k / 10k / 20k / 50k. **V** `rbs-payday-202610`
- **Robinson Season of Giving `RBS1`** (**2–24 Nov**, all Robinson incl. Chat & Shop, Robinson LIVE):
  - ฿50 discount sticker for each T1 slip ≥ ฿2,000 (used on a later ≥ ฿2,000 T1 slip).
  - Store coupon per day + **card cashback per slip: ฿10,000 → ฿500 + ฿300; ฿20,000 → ฿1,300 + ฿700; ≥ ฿50,000 → ฿3,500 + ฿2,500**. Cashback ≤ ฿2,500 a slip, ≤ ฿25,000 an account; credited within 3 days of billing.
  - 10 draw rights per ฿1,000 slip (car DEEPAL S05 MAX).
  - Register **`RBS1` → 081-278-2222** (Central The 1 First Choice loan card → 061-404-5555), on the day. **V** `?modalId=rbs-sea-202611`
- **Central App 11.11 Marathon Sale** (1–13 Nov, Central App / central.co.th, no registration): ฿150 off ≥ ฿3,000 (unlimited); **฿500 off ≥ ฿5,000** (1,500 a month); **฿1,000 off ≥ ฿10,000** (250 in all); **฿2,000 off ≥ ฿20,000** (50 in all) — or **REDZ 5%** off regular-price items. Many brands excluded (Apple, Samsung, Dyson items, MUJI, gift cards…); no second card discount. **V** `cen-app-202611`. Central App Monthly Q4 (same lower tiers) continues to 31 Dec.
- **CPN Year End** "Disney A Celebration of Wonders" (30 Oct 2026 – 3 Jan 2027, **plaza zone of every Central mall** incl. Central Chiangmai and Central Chiangmai Airport, + Esplanade Ratchada): per slip **฿5,000–9,999 → ฿100; ฿10,000–49,999 → ฿300; ≥ ฿50,000 → ฿2,000**, full pay, no points burn. Register receipt + slip + card at the mall's redemption counter **the same day**. Cap ฿2,000 a slip per card; **supplements register separately with their own quota**, cashback to the primary within 60 days of the end. Excludes Central Retail shops (Tops, Central, Robinson, SuperSports, Power Buy, B2S, Matsukiyo, CMG brands, good goods…), e-wallets, Atome/Pace, app payments. "Choose only one promotion if card promotions overlap." **V** `?modalId=cpn-year-202610`
- **CPN plaza ×3 (REDZ)** continues to 31 Dec. **V** `cpn-x3-202308`
- Continuing: **CGT2** Central Gift Card Big Bonus and Robinson's (to 15 Jan 2027; code still not printed), **MJT2** Muji, **GG2** good goods (Jing Jai Market and Chiang Mai Airport), **SuperSports Q4**, **B2SN**, **OFMN**, **CMK2**, Chat & Shop points, Robinson Beauty (to 14 Jan), Tops Care, Tops Prime Plus, Dyson (to **30 Nov**). New, outside Chiang Mai or niche: Tops / Tops Online New Year baskets, KIS 100 points, CMG Skechers 15% + up to ฿1,000, Grand Opening Central Rama 9 (to 2 Nov), Central 79th Extra (Bangkok stores, to 2 Nov). **V** (dates from today's list)

### 3.3 Fuel and EV — for the Shell and PTT pages

| Item | Mechanic | Caps | Register | Period | Conf. |
|---|---|---|---|---|---|
| **SE11 — Shell** | full-pay fuel slip **≥ ฿100 at any Shell station → ฿100** cashback (no adding up slips) | **1 slip per primary account a month**; **first 1,500 successful registrants a month**; counts only spend after registration | **`SE11` → 081-278-2222**, or UCHOOSE search **`SHL`**; registration opens **on the 1st of every month**, re-register monthly (Dec: `SE12`) | Nov 2026 (programme 1 Jan – 31 Dec 2026) | V `?modalId=shell-2026` (poster lists SE1–SE12) |
| **PaySave II — PTT Station** ("เติมเซฟ") | **5% on a fill ≥ ฿1,000 a slip** at PTT Station | **฿50 a slip a day, ฿100 a month** per primary account (supplement pooled) → 2 qualifying fills a month | **once, UCHOOSE keyword `SAVE`** (the T&C also mentions SMS; no number printed) | **1 Nov 2026 – 28 Feb 2027** | V `?modalId=ksc-202610` |
| PaySave II — part 2 bonus | **฿500 a month** at ≥ ฿50,000 a month across the PaySave merchants in **≥ 2 categories** (PTT counts up to ฿10,000 a month) | ฿2,000 a campaign | same | same | V (poster); the T&C also has a "฿2,000 at ฿50,000" sentence — poster's ฿500 a month governs |
| **EVT3 — EV charging** | MCC 5552 or the EA Anywhere, Elexa, evolt, **EV Station PluZ** (PTT/OR), ONION, Sharge apps: ฿1,000–1,999 → ฿50; ฿2,000–2,999 → ฿100; ≥ ฿3,000 → ฿150 a month | ฿150 a month, **฿600 a campaign** | **`EVT3`** → 081-278-2222 / UCHOOSE, on the day | 1 Nov 2026 – 28 Feb 2027 | V `?modalId=ev-station-202611` |
| REDZ base points at fuel | 1 per ฿25, but petrol MCCs count only to ฿50,000 a month | | | | R (Oct REDZ terms) |

- **PaySave II's other legs** (same registration): **dining 10%** on a slip ≥ ฿1,000 at 120+ chains (MK, Sizzler, Sushiro, Yayoi, Kiew Kai Ka, Pepper Lunch, The Pizza Company…), ฿100 a slip a day, ฿300 a month; **travel 3%** per ฿5,000 slip at hotels in Thailand, AirAsia, Lion Air, Nok Air, Bangkok Airways, Thai VietJet, Trip.com, Traveloka, Gother (poster cap ฿900 a campaign; T&C says ฿150 per ฿5,000 and ฿1,200). Excludes e-wallets, food-delivery apps, Krungsri installment plans, foreign currency. Its box says "**ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้**". **V**
- **The household's fills (฿450–800) don't reach PaySave II's ฿1,000**; SE11 pays on any fill ≥ ฿100.
- **PaySave II is "บัตรเครดิตในกลุ่มกรุงศรี" wording but its box says "สิทธิพิเศษนี้เฉพาะบัตรเครดิต เซ็นทรัล เดอะวัน เท่านั้น"** — Krungsri Card may run its own PaySave; that's the Krungsri researcher's page. **R**

### 3.4 Shopee and Makro (card)

- **Shopee**: no Central The 1 promotion at Shopee. "Shopee" appears in today's 184 items only inside exclusions (ShopeePay, ShopeeFood). **V** (full-text search of the dump)
- **TYE** (online ladder, see §1.6) names no merchant list; whether Shopee counts as "หมวดช้อปออนไลน์ที่ร่วมรายการ" isn't stated. **U**. Excludes installments, foreign currency/providers, gold, insurance, transit except Grab, 7-11, TrueMoney Lotus's/Makro, **Makro online and QR at Makro**, MCC 6540 top-ups, easyBills, every Central Group channel, travel, beauty & spa, **fuel**. Register **`TYE` → 081-278-2222**, ≥ 5 shops a month, ฿2,000 a month, ฿8,000 a campaign, credited within 90 days. **V** `?modalId=shop-t1-202611`
- **Makro**: nothing for the Central The 1 card (Makro is CP Axtra; no The 1 points). **V**

### 3.5 Other card items (brief)

- **Mastercard Friday** continues (to 25 Dec; see §5).
- **Starbucks**: **SO11** (any slip ≥ ฿100 at participating Starbucks / Boost Juice → ฿100 e-coupon; Starbucks inside Central malls incl. **Central Chiangmai and Central Chiangmai Airport** (and Central Chonburi), Boost at Central Chiangmai and Chiang Mai Airport; app top-ups and online excluded; 1 per primary account per store type a month; **first 1,500 registrants a month**; register `SO11` → 081-278-2222 or UCHOOSE **`SBO`**, from the 1st) **V** `starbucks-boot-juice-bar-202601`; **STC** top-up ฿50 continues to 31 Dec.
- **PWB4** Power Buy (8 Oct 2026 – 6 Jan 2027): 3% off full pay, or 0% up to 10 months with up to 18% off appliances / 2% IT; installment cashback per slip ฿9,000–14,999 → ฿140; ฿15,000–34,999 → ฿270; ฿35,000–44,999 → ฿800; **฿45,000–69,999 → ฿1,100; ฿70,000–249,999 → ฿1,800**; ≥ ฿250,000 → ฿6,600; caps ฿6,600 a slip, ฿40,000 an account; ×4 per ฿50; register `PWB4`. **V** `?modalId=pwd-202610`
- **TWD4** Thai Watsadu / BnB (to 7 Jan 2027) and the UCHOOSE e-coupons (to 31 Dec) continue; the 16th-anniversary Super Big Sale ended today. **V**
- Continuing dining: BDN buffets, IBR/IBR2 iberry, Grab (T1DIN, T1CAR), GrabFood Dine-out, LINE MAN, GrabFood Mega Sale 10% code (to 30 Nov). **EAT ended → PaySave II dining.** **V**
- **Ended 31 Oct**: HBF, CPN dining, ก้าวรับพอยท์, LUXE upgrade, Central Beauty Bonus, iPhone 18 Power Buy, EVT2, TNL, PTT, GWS3, T1 MAGICAL DAY. **V** (absent from today's list)

---

## 4. GO Wholesale (page **G**)

### 4.1 GO's own and The 1 member items

See §2.2 (Wednesday ฿0.25, anniversary 1,000 → ฿250 and 800 → ฿150, Super Burn Weekend, Exclusive ฿300, PAYDAY not posted), §2.3 (fresh-vegetable ฿90 coupon, weekly price deals). Members earn 1 point per ฿100 in store and in the GO app. **V**

### 4.2 Central The 1 card at GO

See §3.1: **GWS4**, **GWSE +฿300 at ฿50,000** (to 24 Nov), **GWNY** hampers, **10 points per ฿100**, Mastercard Friday (REDZ is a Mastercard).

### 4.3 Bank promotions GO re-posts for November (cross-check for the bank researchers)

| Bank / code | Mechanic at GO | Caps | Register | Period | Conf. |
|---|---|---|---|---|---|
| **Krungsri × Central Retail `CRC`** | **≥ ฿10,000 accumulated → ฿2,000** at Central, Robinson, SuperSports, Tops / Food Hall / Fine Food, **GO Wholesale**, Thai Watsadu, BnB, Power Buy — **stores only** (GO online, Central App, Tops Online, Tops Daily excluded) | ฿2,000 per primary account; **1 account per person; first 2,200 registrations**; spend on a second registered card doesn't count | **SMS only: `CRC <16 digits>` → 081-927-9999**, from **07:00 on 1 Nov**, before spending | **1–30 Nov** | V GO `kccxcrc-cashback-nov26` |
| ↳ eligible cards | every Krungsri card incl. JCB Platinum and **NOW**; **excludes Central The 1, Lotus's and First Choice** | | | | V |
| ↳ stacking | "ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้" | | | | V |
| **Krungsri SU1** (GO + GO app + Tops) | per slip ฿1,500–4,999 → ฿30; ฿5,000–11,999 → ฿110; ≥ ฿12,000 → ฿250 | ฿250 a month per primary account | UCHOOSE (once) | 1 Nov 2026 – 31 Jan 2027 | V GO `kcc-cashback-nov26` |
| **Krungsri SU2** | ≥ ฿50,000 a month → ฿500 | first 1,200 a month | UCHOOSE | same | V; "สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่น ๆ ได้" |
| ↳ code clash | CardX also has `SU1` / `SU2` (Oct–Dec) — always give the number | | | | |
| Krungsri **GOH** (hampers) | hampers / chicken essence / bird's nest per slip: ≥ ฿10,000 → ฿100 (50 rights); ≥ ฿30,000 → ฿400 (50 rights) | | UCHOOSE `GOH` | 28 Oct 2026 – 5 Jan 2027 | V GO poster |
| **KBank `TSU`** (HYP's successor) | supermarkets (MCC 5411/5333), monthly: ฿5,000–14,999 → ฿75; ฿15,000–29,999 → ฿300; ฿30,000–49,999 → ฿700; ≥ ฿50,000 → ฿1,250; + ฿3,000 at ≥ ฿300,000 a month; **Makro and Makro PRO excluded**; Shopee/Lazada/TikTok and e-wallets excluded | ฿1,250 a month, ฿5,000 a campaign (+ ฿12,000 for the ฿300k step) | **`TSU <last 12>` → 4545888** or K PLUS | 1 Nov 2026 – 28 Feb 2027 | V GO `kbank-cashback-nov26` |
| ↳ KBank BCB | K Point = slip → 10% (SMS `BCB <12> <amount>` → 4545888 every time); not on Mastercard KBank cards, LINE POINTS | | | same | V |
| CardX **HY1** | ฿40 / 200 / 720 per slip | | `HY1` → 4545777 | 1 Oct – 31 Dec | V (continues) |
| ttb **BGO** | ฿50 / 100 / 450 / 1,500 per slip | ฿1,500 a campaign | `BGO` → 4899777 | 1 Oct – 31 Dec | V (continues) |
| UOB **SPW592** | up to ฿900 | | | 1 Jul – 31 Dec | V (continues; household not registered) |
| AEON **NTW1** | up to ฿340 a cycle | | | 11 Jul 2026 – 10 Mar 2027 | V (continues) |
| KTC points → 13% cashback | | | | 1 Aug – 31 Dec | V (continues) |
| KTC Visa ฿750 · Krungsri SUP1/2 ฿2,100 · KBank HYP ฿5,000 · Visa ฿500 | — | | | **ended 31 Oct** | V (GO list dates) |

### 4.4 GO effective rates with REDZ in November (point value ฿0.125, or ฿0.25 at a Wednesday / anniversary burn)

| Slip | GWS4 | Points (10 / ฿100) | Total | With a ฿0.25 burn |
|---|---|---|---|---|
| ฿3,000 | ฿35 (1.17%) | 300 pts ≈ ฿37.5 (1.25%) | ≈ 2.4% | ≈ 3.7% |
| ฿7,500 | ฿95 (1.27%) | 750 ≈ ฿94 | ≈ 2.5% | ≈ 3.8% |
| ฿30,000 | ฿400 (1.33%) | 3,000 ≈ ฿375 | ≈ 2.6% | ≈ 3.8% |

Plus GWSE's ฿300 once at ฿50,000 (to 24 Nov), and **Mastercard Friday ฿100** on any slip ≥ ฿1,000 (Fridays 6, 13, 20, 27 Nov; 1 per GO member number). For comparison, a **Krungsri card under `CRC`** pays ฿2,000 on the first ฿10,000 of November store spend across Central Retail (20%), if the household got one of the 2,200 registrations.

---

## 5. Card networks at Central Retail

| Offer | Mechanic | Period | Status | Conf. |
|---|---|---|---|---|
| **Central Retail × Mastercard Friday** | ฿100 e-coupon from the The 1 app (Central App code **PMC261**) on ≥ ฿1,000 after store discounts, paid in full with any Thai-issued Mastercard (credit/debit/prepaid); use the same Friday 08:00–22:00; 1 a week in weeks 1 and 4–5, 2 a week in weeks 2–3; 3,350 / 5,230 coupons a week; name must match the The 1 account; **1 per GO member number** at GO | 2 Jan – **25 Dec 2026**; **Nov Fridays 6, 13, 20, 27** | continues | V `?modalId=cen-retail-202601` |
| Mastercard × Central 79th | one slip ≥ ฿100,000 → 100,000 The 1 points, 30 rights | to 2 Nov | ending | V |
| **Visa × Central Retail ฿500** | — | 21 Aug – 31 Oct | **ended, no successor** (KTC page "หมดอายุ"; nothing on Visa's perks API — 60 offers, none at Central Retail, fuel, Makro or Shopee) | V |
| UnionPay | no Central Retail offer in UnionPay's Thai list; the standing QR 6% (`260723112621…23`) and phone-NFC 3% apply wherever UnionPay is accepted — **whether Central Retail stores take UnionPay QR is unconfirmed**. An "EV Charging Station" offer (`260615112440`) exists (for the PTT researcher) | | — | V (list) / U (acceptance) |
| JCB | none of JCB's 55 Thai campaigns names Central Retail, Shell, PTT, Makro or Shopee | | — | V |
| Mastercard Priceless | site under maintenance on 1 Nov | | not read | — |

**Household Mastercards for Friday**: REDZ, KTC Mastercard, AEON World Mastercard, Krungsri Lady, Krungsri NOW, UOB One / UOB World (`5432…`).

---

## 6. What needs registering today (1 Nov) and first-N quotas

| Code | Card | Where | Quota | How |
|---|---|---|---|---|
| **CRC** | a **Krungsri** card (VISA/JCB/Lady/NOW — not REDZ, not First Choice) | Central Retail stores incl. GO, Tops, Robinson | **first 2,200 registrations, opened 07:00 today**; 1 account per person | SMS only `CRC <16>` → **081-927-9999** |
| **SE11** | REDZ | Shell | **first 1,500 a month** | `SE11 <16>` → 081-278-2222 / UCHOOSE `SHL` |
| **SO11** | REDZ | Starbucks / Boost | **first 1,500 a month** | `SO11 <16>` → 081-278-2222 / UCHOOSE `SBO` |
| **GWS4** | REDZ | GO | none stated | `GWS4 <16>` → 081-278-2222 (on or before first slip) |
| GWSE | REDZ | GO (to 24 Nov) | none | `GWSE <16>` → 081-278-2222 |
| PaySave II | REDZ | PTT Station, restaurants, travel | none stated | UCHOOSE keyword `SAVE` (once) |
| EVT3 · TYE · RBS1 (from 2 Nov) · GWNY | REDZ | EV · online · Robinson · GO hampers | none | 081-278-2222 / UCHOOSE |
| TOPS4 | REDZ | Tops | — | already registered in Oct if used; the ฿300 bonus needs ≥ ฿3,000 in Nov too |
| GO Super Wednesday | The 1 member | GO | 300 a round | The 1 app, Wednesdays 4/11/18/25 Nov |
| GO anniversary coupons | The 1 member | GO | 2,000 each | The 1 app, `the1.onelink.me/UohD/d1vagsi2` |

There is **no Magic Day–style pack** this month (T1 MAGICAL DAY ran 1–13 Oct only).

---

## 7. What ends this month / announced for December

- **Ends in November**: CDS79 and Central 79th Mastercard (2 Nov) · RPAY10, TWD 16th anniversary, Power Buy redeem (1 Nov) · Central App 11.11 (13 Nov) · RBS1, **GWSE** (24 Nov) · GO anniversary coupons (10 Nov, or 24 Nov per the body) · fresh-veg coupon (10 Nov) · **Caltex × The 1 (30 Nov)** · Dyson (30 Nov) · GrabFood Mega Sale code (30 Nov).
- **December already printed**: **SE12** (Shell), **SO12** (Starbucks); TOPS4's ฿300 bonus needs ≥ ฿3,000 in December too; Super Burn Day and Central App Monthly Q4 run to 31 Dec; Mastercard Friday ends **25 Dec**; GO Super Wednesday to 27 Dec, Super Burn Weekend to 27 Dec.
- **Running into 2027**: GWS4 (31 Jan), GWNY (5 Jan), CPN Year End (3 Jan), PWB4 (6 Jan), TWD4 (7 Jan), CGT2 (15 Jan), PaySave II / EVT3 / TYE (28 Feb), Krungsri SU1/SU2 at GO (31 Jan), KBank TSU (28 Feb).

---

## 8. Not found / couldn't read

1. **GO The 1 PAYDAY for November** — not posted (Oct round 25–31 Oct). By pattern, ≈ 25 Nov – 1 Dec. **U**
2. **The 1 member-wide November event** (Point Festival, 11.11 double points, bank-transfer bonus) — none found; the app's content isn't public. Tried the1.co.th pages and sitemap, banner JSON, Thai web search. **U**
3. **Visa × Central Retail successor** — none on Visa's perks API, GO, KTC or the card site.
4. **Mastercard Priceless** — maintenance page all session; Mastercard-side November Central offers beyond the card site's two are unread.
5. **PTT Blue Card ↔ The 1** transfer — only 2016 news; current status unknown. **Shell ↔ The 1** — no tie found.
6. **PaySave II SMS number** — the T&C says "UCHOOSE หรือ SMS" but prints no number; the poster shows UCHOOSE `SAVE` only. Travel cap conflict (poster ฿900 vs T&C ฿1,200); part-2 wording conflict (poster ฿500 a month vs a T&C sentence "฿50,000 → ฿2,000").
7. **GO anniversary coupon 1 dates** (title 28 Oct – 10 Nov vs body 14 Oct – 24 Nov); **GWS4 end date** (GO title 1 Jan vs body/card site 31 Jan).
8. **Krungsri SU1/SU2 SMS code and number** — GO's copy says UCHOOSE only; the Krungsri researcher should confirm.
9. **Whether Central Retail stores accept UnionPay QR** (for KTC UnionPay's 6%).
10. **Whether TYE counts Shopee**; whether CRC and SU1 pay on the same GO slip (CRC's box says not combinable; SU1's says combinable).
11. **CGT2 / Robinson Gift Card SMS code** — still only "ลงทะเบียนผ่าน SMS" in the text.

---

## 9. Lineage rows (for `campaigns.md`)

Pages: **M** Makro · **G** GO Wholesale · **S** Shopee · **T** The 1 · **F** Shell · **P** PTT.

| Campaign | Pays | Oct 2026 | Nov 2026 | Pages | predecessor → successor |
|---|---|---|---|---|---|
| GWS3 → **GWS4** | GO per slip ฿35 / 95 / 400 / 1,800 + 10 pts / ฿100 | GWS3 (ended 31 Oct) | GWS4 1 Nov 2026 – 31 Jan 2027, same tiers and caps | G T | GWS3 → GWS4 |
| **GWSE** | GO +฿300 at ฿50,000 accumulated | new 14 Oct | to 24 Nov | G T | — |
| **GWNY** | GO hampers ฿40–1,600 per slip (+ GO's own ฿200–9,000 off) | new 28 Oct | to 5 Jan 2027 | G T | — |
| SE10 → **SE11** → SE12 | Shell ฿100 on ≥ ฿100, first 1,500 a month | SE10 | SE11 | F T | monthly code |
| SO10 → **SO11** → SO12 | Starbucks / Boost ฿100 e-coupon, first 1,500 | SO10 | SO11 | T | monthly code |
| PTT · EAT → **PaySave II** (`ksc-202610`) | PTT Station 5% at ≥ ฿1,000 (฿50 a slip-day, ฿100 a month); dining 10% (฿300 a month); travel 3%; +฿500 a month at ฿50,000 in 2 categories | PTT, EAT (ended 31 Oct) | 1 Nov 2026 – 28 Feb 2027, UCHOOSE `SAVE` | P T | PTT + EAT → PaySave II |
| EVT2 → **EVT3** | EV charging ฿50 / 100 / 150 a month (EV Station PluZ counts) | EVT2 | 1 Nov 2026 – 28 Feb 2027, ฿600 a campaign | P T | EVT2 → EVT3 |
| TNL → **TYE** | online ladder ฿100 / 350 / 850 / 2,000, ≥ 5 shops; Makro excluded | TNL | 1 Nov 2026 – 28 Feb 2027 | S T | TNL → TYE |
| CMN3 / RPAY9 → **CDS79**, **RPAY10**, **RBS1** | dept-store coupon + card cashback | CMN3, RPAY9 (ended 4–5 Oct) | CDS79 to 2 Nov; RPAY10 to 1 Nov; RBS1 2–24 Nov | T | — |
| Central App Midnight → **Central App 11.11** | ฿150 / 500 / 1,000 / 2,000 off or REDZ 5% | Midnight to 5 Oct; Monthly Q4 | 11.11: 1–13 Nov; Q4 continues | T | — |
| **CPN Year End** | plaza zone ฿100 / 300 / 2,000 per slip, per card | CPN dining, ก้าวรับพอยท์ (ended) | 30 Oct 2026 – 3 Jan 2027 | T | — |
| **Super Burn Day** (`cen-rbs-202611`) | Central / Robinson points burn 20% Sat–Sun, 13% other days | Power Buy / Beauty burns | 1 Nov – 31 Dec | T | — |
| PWB3 → **PWB4** | Power Buy installment ฿140–6,600 | PWB4 unpublished | published: 8 Oct 2026 – 6 Jan 2027 | T | PWB3 → PWB4 |
| TOPS4 | Tops 3–4% + ฿300 for 3 months | continues | continues to 31 Dec | T | — |
| The 1 PAYDAY (GO) | 1,500 → ฿400 at ≥ ฿4,500 | 25–31 Oct | not posted | G T | monthly |
| Super Wednesday (GO) | 800 → ฿200 at ≥ ฿2,500 | continues | continues to 27 Dec | G T | — |
| **Super Burn Weekend** (GO) | 1,000 → ฿200 at ≥ ฿2,500, Fri–Sun | (missed) | 4 Sep – 27 Dec | G T | — |
| **GO 3rd anniversary coupons** | 1,000 → ฿250 at ≥ ฿3,000; 800 → ฿150 at ≥ ฿1,500 fresh/frozen | new | to 10 Nov (or 24 Nov) | G T | — |
| Hug the Earth · Extra Point (GO) | +100 / +800 points | to 27 Oct / 16–25 Oct | ended | G T | — |
| Fresh-vegetable coupon (GO) | ฿90 on ≥ ฿300 | 30 Sep – 13 Oct | 28 Oct – 10 Nov | G | round to round |
| Caltex × The 1 | 1 pt a litre, 800 → ฿100 | continues | **ends 30 Nov** | T | — |
| Visa × Central Retail | ฿500 at ≥ ฿5,000 tap, 2 stores | 21 Aug – 31 Oct | **ended, no successor** | G T | — |
| Mastercard Friday | ฿100 coupon on ≥ ฿1,000 | continues | continues to 25 Dec | G T | — |
| **Krungsri × CRC `CRC`** | ≥ ฿10,000 at Central Retail stores → ฿2,000; first 2,200; SMS 081-927-9999 | — | 1–30 Nov | G T | — |
| SUP1 / SUP2 → **SU1 / SU2** (Krungsri, GO + Tops) | ฿30 / 110 / 250 per slip (฿250 a month); ฿500 at ฿50,000 (first 1,200) | SUP1/SUP2 (ended 31 Oct) | 1 Nov 2026 – 31 Jan 2027 | G T | code clash with CardX SU1/SU2 |
| HYP → **TSU** (KBank) | supermarkets ฿75 / 300 / 700 / 1,250 a month; Makro out | HYP (ended 31 Oct) | 1 Nov 2026 – 28 Feb 2027, `TSU` → 4545888 | G T | HYP → TSU |
| **GOH** (Krungsri, GO hampers) | ฿100 / ฿400 at ฿10k / 30k, 50 rights each | — | 28 Oct 2026 – 5 Jan 2027 | G | — |

---

## 10. New site tricks (for `research-methods.md`)

- **GO's WordPress API from inside Chrome** worked as documented, and it lists items **not linked from the list page** (the Super Burn Weekend). Fetch `/wp-json/wp/v2/promotions?per_page=100&page=N&_fields=id,date,modified,slug,link,title,content` in-page, then filter on `modified`. GO re-posts the **Krungsri** and **KBank** monthly campaigns with full terms (`kccxcrc-cashback-nov26`, `kcc-cashback-nov26`, `kbank-cashback-nov26`) a few days before the banks' own pages.
- **GO posters**: an in-page `fetch()` → base64 over CDP pulls `/wp-content/uploads/…jpg` that curl can't reach (Cloudflare).
- **Visa Thailand perks**: the body that works is `{"siteId":"www.visa.co.th","perkTypeRequests":[{"requestIdentifier":null,"perkType":"OFFERS","locale":"th_TH","pageRequest":{"index":0,"limit":1000},"perkArguments":{"offerType":"U"}}]}` (captured with `Network.requestWillBeSent` over CDP); `{}` gets "Validation failure".
- **centralthe1card.com** pre-publishes items that start later (RBS1 appeared on 1 Nov with a 2 Nov start); the Shell and Starbucks posters print **all twelve monthly codes** for the year.
- **KTC promotion pages** print "โปรโมชั่นหมดอายุ" when a cross-merchant offer has ended — a quick way to confirm an end without the merchant's site.
- **the1.co.th** sitemap lists ≈ 24,000 `/the1today/articles/<n>` and ≈ 700 `/rewards/<uuid>` URLs, but both render client-side to the home page for an anonymous visitor; the homepage banners come from `/master/banner/json/th/banner.json`.
