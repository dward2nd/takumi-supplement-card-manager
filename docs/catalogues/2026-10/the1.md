---
tags: [catalogue-research, 2026-10]
researched: 2026-10-01
---

> **Research snapshot**: The 1 membership and the Central The 1 card — October 2026 research. Scope: The 1 points, member deals and network coupons; every Central The 1 card promotion; how the two differ. Read on **2026-10-01** from the official pages, for the October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions (HTML, JSON, posters) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# The 1: October 2026 (ต.ค. 69), membership and Central The 1 credit card

Researcher: `the1`. Fetched 1 Oct 2026, 02:59–03:35 Bangkok time. Raw files are in `research/the1/`: `list.json` (all 168 card promotions), `promo/`, `pc/` (T&C as text) and `img/` (posters).

**Sources and confidence tags**
- **[official-card]**: `centralthe1card.com`. This is the full `gcspromotion` JSON dump (168 promotions) plus the posters, which carry the tier tables and SMS codes.
- **[official-CRC]**: Central Retail's own sites, `centralfoodwholesale.co.th` (GO) and `central.co.th` (Central/Robinson). Fetched through r.jina.ai because Cloudflare blocks curl.
- **[official-T1]**: text inside the1.co.th's JS bundle. It is official but may be older than the April 2026 tier revamp.
- **[bank]**: the bank's own page.
- **[news]**: press release or news. **[3rd]**: other third-party sources.

**Status tags:** **NEW** (starts in Oct or wasn't in the Sep draft) · **CONT** (continues unchanged) · **ENDED 30 Sep** · **SUCC** (October successor).

**Diff against the 30 Sep snapshot:** every promotion that continues has **byte-identical T&C**, so nothing was changed mid-campaign.
- 18 promotions were removed on 30 Sep. The ones that matter here: Tops Cashback (TOPS3), Tops 58th Anniversary stickers, Tops Care Cashback Q3, SuperSports Monthly Q3, GO Pick The Deal, CMG Fashion (Jul), and "30% points super burn".
- Only one promotion is new since 30 Sep: **Central App Monthly Q4**.
- The other October promotions were already pre-published on 30 Sep: TOPS4, Tops Care Q4, SuperSports Q4, Muji MJT2, good goods GG2, Tops Online Prime Plus, CPN "ก้าวรับพอยท์", T1 MAGICAL DAY, and Thai Airways T1TG2.
- No PWB4, no October Robinson Payday and no Midnight Sale 4 had been published by 03:30.

---

## 0. Most important changes vs September

1. **T1 MAGICAL DAY, 1–13 Oct (CRCT1).** Registration opens **today, 1 Oct, at 09:00** in UCHOOSE and is limited to the first 2,500 successful registrations per pack.
   - XL: one slip ≥ ฿4,000 at Central, Robinson, SuperSports, **GO Wholesale**, Thai Watsadu, BnB, Auto1, Power Buy or OfficeMate. It pays a ฿1,000 Magic e-Voucher (25%) plus a ฿2,000 CRC Exclusive Pack.
   - S: one slip ≥ ฿1,000 at Muji, Tops (all formats), Tops Care, Matsukiyo or B2S. It pays ฿200 plus a ฿500 pack.
   - This is the biggest October item. Details in §B1.
2. **Tops: TOPS3 ended; TOPS4 runs 1 Oct–31 Dec** with identical tiers and caps. The ฿300 bonus now needs ≥ ฿3,000 in **each of Oct, Nov and Dec**. Tops Care uses the same code and pool. The 58th-anniversary stickers ended.
3. **SuperSports Q4 (1 Oct–31 Dec)** is identical to Q3.
4. **New in October:**
   - Muji cashback MJT2.
   - good goods GG2, which has Chiang Mai branches (Jing Jai Market and Chiang Mai Airport).
   - Central App Monthly Q4: ฿150 off at ≥ ฿3,000, ฿500 off at ≥ ฿5,000, or 5% for REDZ.
   - CPN "ก้าวรับพอยท์": walk 5,000 steps and get 500 points from the mall, plus 500 more from the card.
   - **Central Gift Card Big Bonus (CGT2)**, 1 Oct–15 Jan.
   - Central/Robinson **Run Challenge** coupons (membership-type).
   - Tops Online Prime Plus.
   - Thai Airways T1TG2.
5. **Monthly codes rolled over:** Shell **SE9 → SE10**, and Starbucks/Boost e-coupon **SO10**. SO10 gives a ฿100 e-coupon for a ≥ ฿100 slip at Starbucks in Central malls, including Central Chiangmai and Chiang Mai Airport. It was missing from the Sep draft.
6. **Still running:** GWS3, CMN3 (to 5 Oct), RPAY9 (to 4 Oct), Central App Midnight Sale (to 5 Oct), TWD4, PWB3 (to 7 Oct), B2SN, OFMN, CMK2, EAT, CPN dining (a fresh 4,500-right pool for October), BDN, Grab, LINE MAN, STC, PTT, EVT2, TNL (Double Day ×5 on **10 Oct**), Mastercard Friday, and Visa ฿500 (to 31 Oct).
7. **Ended or ending on the GO/membership side:** GO Pick The Deal ended 30 Sep. GO **The 1 PAYDAY ends today (1 Oct)**. The Sep Point Festival and its bank-transfer bonus ended 22 Sep. No October transfer bonus was found.
8. **Corrections to the Sep draft:**
   - EVT2 is ฿50 per full ฿1,000 per month (5%), not "1–1,999 → 50".
   - B2S also pays ฿30 on a ≥ ฿600 slip (once a month).
   - TNL's poster says 5 **shops**, but its T&C says 5 **transactions**, and the caps differ (see §B8).
   - Two Sep-draft items were missing: the Thai Watsadu e-coupons (฿100 or ฿200, all year) and the Starbucks SO-code e-coupon.
9. **Shopee and Makro:** the Central The 1 card has **no promotion at either** in October. Neither appears in any of the 168 promotions except inside exclusion clauses, and Krungsri's Shopee promos don't include Central The 1. Makro is CP Axtra, so it earns no The 1 points.

---

## A. The 1 membership (the1.co.th, The 1 app)

### A1. How points are earned: member only vs with the card

Base member rates come from the1.co.th's own T&C text **[official-T1]**:
- **1 point per ฿25** at Central, Robinson, Muji, B2S, SuperSports, Tops (all formats), Central Food Hall, FamilyMart, Matsumoto Kiyoshi, Baan & Beyond and CMG.
- **1 point per ฿50** at Power Buy, Thai Watsadu, OfficeMate and some CMG branches.
- These points count only when you give your phone number or The 1 QR at the till.

The card-side rates come from each promotion's T&C **[official-card]**.

| Where | Member only (any payment) | With REDZ | With LUXE / BLACK / THE BLACK | Source |
|---|---|---|---|---|
| Central / Robinson dept stores | 1 / ฿25 | ×3 (3 / ฿25) + up to 5% off regular-price goods | ×4, up to 10% off | REDZ product page; CPN x4 T&C |
| CPN mall "plaza zone" shops (Central Chiangmai, Central Chiangmai Airport, 1,400+ brands) | 1 / ฿25 (fashion, F&B, cosmetics…) or 1 / ฿50 (IT, furniture, jewellery, clinics) | ×3: 1 card base + 1 card extra + 1 CPN (give your The 1 number) | ×4 on spend up to ฿300,000/month, ×3 above that | `cpn-x3-202308` |
| Tops / Tops Food Hall / Tops Daily / Tops Online | 1 / ฿25 | ×3 (2 extra from the card + 1 regular from giving your number) | ×3, plus 5% off at Tops Food Hall/Fine Food (LUXE+ only) | TOPS4 T&C |
| GO Wholesale (GO membership linked to The 1) | **1 / ฿100** | **10 / ฿100** (9 from the card + 1 from GO) | same | GO page `the1-creditcard-point`; GWS3 |
| Thai Watsadu / BnB | 1 / ฿50 (Thai Watsadu is in the1.co.th's 1-per-฿50 list; BnB not listed) | 4 / ฿50 (all tiers) | same | TWD4 T&C; [official-T1] |
| Power Buy | **1 / ฿50** (cash or other cards) | **4 / ฿50** | same | iPhone 18 T&C says so explicitly |
| OfficeMate | **1 / ฿50** (cash or other cards) | **4 / ฿50** | same | OFMN T&C says so explicitly |
| SuperSports, B2S, Muji, good goods | 1 / ฿25 | ×3 | ×4 | SSP / B2SN / MJT2 / GG2 T&C |
| Matsukiyo | 1 / ฿25 | no multiplier stated in CMK2 | – | the1.co.th; CMK2 |
| Caltex (partner) | 1 / litre of fuel; engine oil 5 / ฿25; burn 800 = ฿100 at the pump; max 100 L per fill, 2 fills a day, 400 L a month | – | – | caltex.com **[official partner]** |
| REDZ anywhere outside the group | – | 1 / ฿25 | 1 / ฿25 | REDZ product page |

**What REDZ's base 1 / ฿25 excludes** **[official-card]**:
- 7-11 in every channel (from 1 Aug 2026).
- Spend through a card linked to TrueMoney Wallet (from 1 Aug 2026).
- Foreign merchants charging in THB (from 1 Jul 2025).
- Utilities, tax and government fees, mass transit, tolls, `2c2p *E WALLET TOP UP`, AIA premiums and unit-linked funds.
- Petrol (MCC 5541/5542/5983/5172) counts only up to ฿50,000 a month.

**Points and supplement cards.** Card points on **Baiboon's REDZ supplement go into the primary account's The 1 (Takumi's)**. When a rate is split, e.g. Tops ×3 = 2 from the card + 1 from the number given at the till, the 1× goes to **whichever The 1 number is given at the till** [TOPS4 T&C].

**Points expire** 2 years after the year they were earned, cut on 31 Dec. The 1 Exclusive points never expire [official-T1].

### A2. What a point is worth

- **Standard: 800 points = ฿100 cash coupon** in the app. The minimum is 800, so one point is worth **฿0.125** [official-T1]. A REDZ earn rate of 3 / ฿25 is therefore ≈ 1.5%, 4 / ฿50 ≈ 1.0%, 10 / ฿100 ≈ 1.25%, and 1 / ฿25 ≈ 0.5%.
- **Better burn rates open in October:**

| Burn | Rate | ฿ per point | Who | Period | Source |
|---|---|---|---|---|---|
| **GO The 1 Super Wednesday** | 800 pts → ฿200 off a receipt ≥ ฿2,500 | **0.25** | Any GO member linked to The 1 (no card needed) | Every Wednesday: claim Wed, use Wed–Sun. 300 rights per round, 1 per member. Oct: 7, 14, 21, 28 | [official-CRC] |
| GO The 1 PAYDAY | 1,500 → ฿400 off ≥ ฿4,500 | 0.267 | Member | 25 Sep–**1 Oct** (ends today). 1,000 rights, 1 per member | [official-CRC] |
| Robinson Payday point burn | 1,000 → ฿150 cash coupon (The 1 app) | 0.15 | Member | 23 Sep–4 Oct. 3 per member, 3,000 in total | central.co.th [official-CRC] |
| Level 2 special rate | 2,000 → ฿300 | 0.15 | Level 2 members | From the Apr 2026 revamp | [news] |
| Power Buy redeem (card) | Fri–Sun: 5,000 pts per ฿5,000 → 15% off. Mon–Thu: 12.5% off with points = purchase | 0.15 / 0.125 | T1 card | 11 Sep–1 Nov. 5 per The 1 number, 2,500 in total | [official-card] |
| SuperSports redeem (card) | Points = purchase. ฿800–2,999 → 13%. ≥ ฿3,000 → 15% Mon–Fri, 18% Sat–Sun | 0.13–0.18 | T1 card, name must match The 1 | 1 Oct–31 Dec | [official-card] |
| Central Beauty Bonus / Robinson Beauty Privilege (card) | ≥ 800 pts per slip → up to 15% Fri–Sun, 12.5% Mon–Thu, + store coupons up to 10% | ≤ 0.15 | T1 card | CDS to **31 Oct**; RBS 1 Sep–14 Jan 2027 | [official-card] |
| OfficeMate redeem (card) | Points = purchase → 12.5% (slip ≥ ฿800) | 0.125 | **Primary cardholder only**, in store | to 31 Dec | [official-card] |
| Power Buy iPhone 18 Pro/Pro Max | Every 10,000 pts → REDZ/LUXE 15% (฿1,500), BLACK 18%, THE BLACK 20%. Max 100,000 pts | 0.15–0.20 | T1 card, names must match | 12 Sep–31 Oct | [official-card] |
| Watch & Jewellery Fairs (Central / Robinson) | Up to 28% off with points, + up to 10% on installments | – | T1 card | to **11 Oct** | [official-card] |

### A3. Tiers and perks

The April 2026 revamp introduced four levels **[news: thansettakij, brandbuffet, biznewsupdate]**. The Exclusive retention rule is also in the1.co.th's text [official-T1].
- **Level 1:** "5% discount in Central Retail" (the press release gives no mechanics), plus earn and burn.
- **Level 2 (≥ ฿50,000 a year at CRC):** 2,000 pts → ฿300 coupon, and 10% off in your birthday month.
- **Level 3 (≥ ฿125,000):** **×2 points every Wednesday**, ×10 on your birthday, 10% off in your birthday month, and special deals and services.
- **The 1 Exclusive (≥ ฿250,000 at CRC, or ≥ ฿400,000 at CRC plus participating mall stores):** parking up to 6 h free, lounge, up to ×6 points on a day you choose, ×25 on your birthday, and points that never expire.
  - Card-side **Extra Point Day**: Exclusive members holding a T1 card get ×4 (card) + ×2 on the chosen day, capped at 500 bonus points a month and 4,000 rights a month (1 May–31 Dec) [official-card].
  - GO: ฿300 coupon at ≥ ฿12,000, Exclusive only [official-CRC].
- **The household's levels are unknown.** Check in the app.

### A4. Member deals in October (no card required unless noted)

- **GO The 1 Super Wednesday** and **PAYDAY**: see A2 and §D.
- **GO "The 1 Hug the Earth":** buy ≥ 5 packs of Namthip water (550 ml ×12, 1.5 L ×6 or 350 ml ×12) and get **+100 points**. Register first at `go.the1.co.th/UohD/566spxnq`. 30 Sep–27 Oct, in store and in the app. [official-CRC] NEW
- **Robinson Payday point burn:** 1,000 → ฿150, to 4 Oct (A2). The central.co.th page says "สมาชิก เดอะวัน รับคูปองส่วนลด…" and credits the cashback to CT1/CFC. The card site's poster says the coupons are for T1 card members. **Whether a non-T1 payer gets the store coupon is unconfirmed.**
- **Central Run Challenge / Robinson Run Challenge (1–31 Oct):** show 5 km run in the past 7 days at Customer Service → coupons ฿300 at Central or ฿400 at Robinson (1,500 rights). Show 10 km → ฿620 + extras (1,500 rights). Coupons are stored in the **Central App** and usable at Central, Central App and Robinson. [official-CRC] NEW
- **CPN "ก้าวรับพอยท์" (1–31 Oct):**
  - Walk 5,000 steps in the **Central X** app at a Central mall and get **500 The 1 points from the mall**. The mall's own conditions weren't found.
  - Card extra (T1 card): spend ≥ ฿500 per slip at plaza-zone shops and get **+500 more**. Register at the mall's redemption counter the same day. 1 per card number, 1,500 in total. Supplements can register; their points go to the primary. [official-card] NEW
- **The 1 Point Festival 2026** (1–22 Sep) **ENDED**. Nothing similar is announced for October [news].
- **Double-point days for members:** only Level 3 Wednesdays (×2) and the Exclusive chosen day. No October-wide member double-point event was found.

### A5. Moving bank points into The 1

| From | Rate | Where / limits | October bonus | Source |
|---|---|---|---|---|
| **Krungsri Point** (Krungsri VISA, JCB, Lady, NOW) | **1,000 → 800 The 1** | UCHOOSE → POINT TRANSFER → The 1. Minimum 1,000, steps of 1,000. Max 500,000 per primary account per day. **Primary card only**, Thai nationals | none found | krungsricard.com [bank] |
| **First Choice Reward** | 1,000 → 800 | UCHOOSE → บัญชี → คะแนนสะสม → The1. Primary card only | none found | firstchoice.co.th [bank] |
| **UOB Rewards** | UOB World / Premier / other cards: **1,200 → 1,000**. Infinite, Reserve, Zenith, PRVI: 1,000 → 1,000. **UOB One and UOB Makro are excluded** | At a Central dept-store cashier or customer service (instant, can go to anyone's The 1), or TMRW / website / LINE (about 3 days) | none found | uob.co.th [bank] |
| KBank K Point | Only a search snippet says The 1 is a K Point partner; KBank's page shows no rate | – | – | **unverified** |
| KTC FOREVER, AEON, CardX | No transfer to The 1 found | – | – | – |
| Central The 1 REDZ | Already The 1 points, moved automatically | – | – | [official-card] |


### A6. Card-network coupons in the The 1 app (any issuer)

- **Central Retail × Mastercard Friday** (every Friday, 2 Jan–25 Dec) [official-card]:
  - Claim a ฿100 e-coupon in the The 1 app and use it the same Friday, 08:00–22:00.
  - Needs ≥ ฿1,000 after store discounts, paid **in full** with any **Thai-issued Mastercard** (credit, debit or prepaid).
  - Central App version: code **PMC261** on the Sep-26 poster. Whether October uses a new code is unconfirmed.
  - Valid at Central, Robinson, SuperSports, CMG, Tops (all), Tops Care, Pet'N Me, Matsukiyo, **GO** (1 per GO member number), Thai Watsadu, BnB, Auto1, Power Buy, OfficeMate, B2S, Chat & Shop and Central App.
  - **Limit:** 1 coupon a week in weeks 1 and 4–5 of the month, 2 a week in weeks 2–3. Quota 3,350 or 5,230 a week.
  - **Oct Fridays:** 2, 9, 16, 23, 30. If weeks are counted by date, 9 and 16 Oct are the two-coupon weeks (my inference).
  - **Household Mastercards:** REDZ, KTC Mastercard, AEON World Mastercard, Krungsri Lady and Krungsri NOW.
- **Mastercard × Central Midnight Sale** (23 Sep–**5 Oct**): ≥ ฿30,000 on one slip with any Mastercard at a Central dept store → ฿1,500 Central gift card. 1 per ID, 250 in total. [official-CRC]
- **CRC × Visa: ฿500 The 1 Cash Coupon** (21 Aug–**31 Oct**) [official-CRC and KTC page]:
  - Register once in the The 1 app. Then **tap-pay** with a Visa (credit, debit or prepaid) for ≥ ฿5,000 accumulated at **≥ 2 different CRC stores**.
  - The time window conflicts: **within 3 days of registering** (GO page) or **the same day** (KTC page). Doing it in one day is safe.
  - Online, Chat & Shop and Personal Shopper don't count. Each brand group counts as one store.
  - The card name must match the The 1 account, so each person can earn one coupon with a Visa in their own name. That includes supplement cards, which carry the supplement holder's name.
  - First 11,000 in the whole campaign; the remaining quota is unknown. The coupon arrives within 45 days (GO) or 30 days (KTC) and must be used within 10 days.
  - **Household Visas:** Krungsri VISA (Takumi, Baiboon supp), KTC Digital VISA, First Choice (Visa; Takumi, Baiboon and Nuta supps). REDZ is a Mastercard, so it doesn't count.

---

## B. Central The 1 credit card (General Card Services / Krungsri Consumer)

Household: **REDZ** (Takumi …2611 + Baiboon's supplement). REDZ is a Mastercard.

**Registration:** register each code by SMS `<CODE> <16-digit card no.>` to **081-278-2222**, or in **UCHOOSE**. Some codes must be registered *before* spending, others on the day; noted per item.

**Pooling:** supplement spend is pooled with the primary for cashback and caps, and cashback lands on the primary. The exceptions are CPN dining and ก้าวรับพอยท์, where each card number has its own quota.

**Everyday REDZ privileges** (to 31 Dec 2026) [official-card, REDZ page]:
- ×3 points + up to 5% off regular-price goods at Central, Central App, Robinson, SuperSports, CMG, Muji, M&S and good goods.
- ×3 at Tops. 10 / ฿100 at GO. **×2 points when buying gift cards.**
- Annual fee waived with ≥ ฿100,000 spend a year. Income from ฿15,000 a month.

### B1. T1 MAGICAL DAY: 1–13 Oct · CRCT1 · NEW (announced in Sep)

- **Register CRCT1 in UCHOOSE from 1 Oct 09:00, before spending.** Register once per pack (XL and S separately). Each pack goes to the **first 2,500 successful registrations**.
- **XL Pack:** ≥ ฿4,000 on **one slip** at one of Central, Robinson, SuperSports, **GO Wholesale**, Thai Watsadu, BnB, Auto1, Power Buy or OfficeMate. Online and UCHOOSE QR Payment count. Reward: **Magic e-Voucher ฿1,000** + **CRC Exclusive Pack ฿2,000**.
  - The pack is these coupons:
    - Central ฿100 (≥ ฿1,000) and Central ฿200 (≥ ฿3,000)
    - Robinson ฿200 (≥ ฿1,500)
    - SuperSports ฿220 (≥ ฿2,000)
    - **GO ฿100 (≥ ฿3,000, pay with T1 card, in store only)**
    - TWD/BnB ฿150 (≥ ฿3,000 on home décor/repair)
    - Auto1 ฿100 (≥ ฿2,000)
    - Power Buy ฿230 (≥ ฿8,000 on appliances; the PDF text also says 220) and Power Buy ฿600 (≥ ฿18,000)
    - OfficeMate ฿100 (≥ ฿1,500)
- **S Pack:** ≥ ฿1,000 on one slip at Muji, Tops Food Hall, Tops, Tops Daily, Tops Care, Matsukiyo or B2S. Reward: **e-Voucher ฿200** + pack ฿500. The pack is Muji ฿100 (≥ ฿1,000), Tops ฿80 (≥ ฿1,500), Tops ฿120 (≥ ฿2,000), Matsukiyo ฿100 (≥ ฿1,200) and B2S ฿100 (≥ ฿1,000).
- **Excluded:** 0% 3-month installments, gift cards, e-wallets and other QR apps, Central Embassy, Central U-Tapao, Central Village, Central Khon Kaen Campus, and "ร้านค้าอื่นๆ ที่ไม่ได้อยู่ในห้างสรรพสินค้าเซ็นทรัล".
- **Delivery:** supplement spend counts, but vouchers go only to the **primary's UCHOOSE**, within 15 days after 13 Oct once the merchant settles. They are **usable to 15 Nov**, and each is valid 60 minutes after you press "use" at the till. Any balance must be paid with a T1 card.
- **Unconfirmed:** the Magic e-Voucher's own minimum spend and excluded stores. The website poster returns 404; the GO page carries the same poster, which I checked.
- Sources: `?modalId=cen-retail-202610`; pack PDF `/getmedia/5cffafa6-…/CRC-Exclusive-pack_2.pdf`; GO page. [official-card, official-CRC]

### B2. Supermarkets

**GO Wholesale · GWS3:** see **§D** (CONT, 1 Aug–31 Oct).

**Tops Store & Online · TOPS4 · 1 Oct–31 Dec 2026 · SUCC of TOPS3** [official-card, poster read]
- **Where:** Tops Food Hall, Tops and Tops Daily (all branches), Tops Online, and **Tops Care** (code TOPS4 too). Cashback and caps are pooled with LOOKS.
- **Cashback per slip:**
  - ฿1,000–4,999: ฿30 per ฿1,000 (3%)
  - ฿5,000–14,999: ฿170 (≤ 3.4%)
  - ≥ ฿15,000: ฿600 (≤ 4%)
  - Remainders are dropped. Full pay and installments both count, after discounts.
- **Caps:** ฿600 per primary account per month, ฿1,800 per campaign.
- **Bonus ฿300:** ≥ ฿3,000 per month in **each of Oct, Nov and Dec**. Register on the day of your first spend. Paid within 7 days after the campaign.
- **Points:** ×3 per ฿25 (2 from the card + 1 by giving your The 1 number).
- **LUXE / BLACK / THE BLACK only:** 5% off regular-price items at Tops Food Hall and Tops Fine Food. **REDZ doesn't get it.**
- **Excluded:** tenant shops, restaurants, mail order, commercial buying, non-EDC payments and every e-wallet. The T&C says "ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้".
- **Changes vs Sep:** the tiers are identical. The Tops 58th-anniversary sticker offer (฿50 sticker at ≥ ฿2,000) **ENDED 30 Sep**.
- Sources: `?modalId=top-cashback-202610`, `?modalId=top-care-202610`.

**Tops Online Prime Plus (1 Oct–31 Dec)** · NEW. Discount on the Tops Prime Plus+ subscription when paid with a T1 card: 1 month ฿139 (from ฿149), 6 months ฿699 (from ฿799), 12 months ฿999 (from ฿1,199). Quotas apply. Prime Plus members earn ×4 points per ฿25 on Tops Online. [official-card]

**Tops / Tops Food Hall on GrabMart:** ฿150 off, 1 per card, to 31 Oct. **LUXE+ only, REDZ can't use it.** CONT.

### B3. Department stores and malls (Chiang Mai: Central Chiangmai; Robinson at Central Chiangmai Airport)

Robinson is still at Central Chiangmai Airport and is due to convert to "Central The Store" in 2027 [3rd: Wikipedia].

- **Central Midnight Sale 3 · CMN3 · 23 Sep–5 Oct** · CONT [official-card, poster read]
  - Central dept stores, Chat & Shop, Central LIVE. Coupons and cashback are for **T1 card members**.
  - Store coupon is per day accumulated; card cashback is per slip:

    | Spend | Store coupon | Card cashback |
    |---|---|---|
    | ฿3,000 | ฿100 | ฿100 |
    | ฿10,000 | ฿700 | ฿350 |
    | ฿30,000 | ฿2,400 | ฿1,200 |
    | ฿50,000 | ฿5,000 (฿5,500 for The 1 Exclusive) | ฿2,500 |

  - Cashback cap ฿2,500 per slip and ฿25,000 per account.
  - **LUXE/BLACK/THE BLACK only:** +฿2,000 at ≥ ฿50,000 per slip.
  - Excluded: Central App, Muji, 0% installments, tenant shops outside the department store.
- **Robinson Payday 9 · RPAY9 · 23 Sep–4 Oct** · CONT [official-card]
  - Coupon per day accumulated, cashback per slip:

    | Spend | Store coupon | Card cashback |
    |---|---|---|
    | ฿2,000 | ฿100 | ฿50 |
    | ฿10,000 | ฿600 | ฿350 |
    | ฿20,000 | ฿1,700 | ฿800 |
    | ≥ ฿50,000 | ฿5,000 | ฿2,500 |

  - The 25–27 Sep bonus points are over. **No October Payday has been published yet.**
- **Central App / central.co.th Midnight Sale · to 5 Oct** · CONT. ฿150 off at ≥ ฿3,000 (no limit), ฿500 off at ≥ ฿5,000 (1,500 a month), ฿1,000 off at ≥ ฿10,000 (300 in total), **or** 10% (**REDZ 5%**) off regular-price items. No registration.
- **Central App Monthly Q4 · 1 Oct–31 Dec** · NEW [official-card, poster read]. ฿150 off at ≥ ฿3,000 (unlimited), **฿500 off at ≥ ฿5,000** (1,500 a month, 4,500 in total), **or** up to 10% off regular-price items (**REDZ 5%**). There's **no ฿1,000 tier**. Many brands are excluded (Apple, Samsung, Dyson items…). It can't be combined with other card discounts. Source: `?modalId=cen-app-monthly-202610`.
- **Central Gift Card Big Bonus · CGT2 · 1 Oct 2026–15 Jan 2027** · NEW [official-CRC]
  - Buy Central gift cards per slip at a Central dept store (0% installments excluded):

    | Gift cards bought | Digital coupon | T1 card cashback |
    |---|---|---|
    | ฿5,000 | ฿100 | ฿100 (4%) |
    | ฿20,000 | ฿450 | ฿450 (4.5%) |
    | ฿50,000 | ฿1,200 | ฿1,200 (4.8%) |
    | ฿500,000 | ฿12,200 | ฿12,200 |
    | ฿1,000,000 | ฿24,500 | ฿24,500 |

  - Cashback cap ฿24,500 per account. The digital coupon works to 29 Jan 2027, but **not** in Beauty Gallery, B2S, SuperSports, Central Food Hall, Tops or Power Buy.
  - REDZ also earns ×2 points on gift-card purchases (REDZ page).
  - **Robinson Gift Card Big Bonus** (same dates): ฿2,000 → ฿50 + ฿50; ฿40,000 → ฿900 + ฿900; ฿60,000 → ฿1,400 + ฿1,400; ฿300,000 → ฿7,200 + ฿7,200; ฿500,000 → ฿12,200 + ฿12,200. **SMS code not found.**
- **Chat & Shop points** (to 31 Jan 2027) · CONT. Central (CSC2): ฿3,000–5,999 → 500 store + 500 card points; ≥ ฿6,000 → 1,000 + 1,000. Robinson (RSC2): ฿2,500–4,999 → 400 + 400; ≥ ฿5,000 → 800 + 800. Register before buying.
- **Beauty:** Central Beauty Bonus to **31 Oct**, Robinson Beauty Privilege to 14 Jan 2027. See A2. · CONT.
- **Watch & Jewellery Fairs** (Central / Robinson) to **11 Oct**. · CONT.
- **CPN plaza zone ×3 points (REDZ)** to 31 Dec · CONT. Participating shops in Chiang Mai are listed in `/getmedia/d85d8b10-…/x4-202609.pdf` (Central Chiangmai, Central Festival Chiangmai, Central Chiangmai Airport).
- **ก้าวรับพอยท์**: see A4. NEW.
- **good goods · GG2 · 1 Oct–31 Dec** · NEW [official-card, poster read]
  - Branches include **Jing Jai Market, Chiang Mai** and **Chiang Mai Airport** (plus CentralWorld, Phuket Floresta, Pattaya, Krabi, Dusit Central Park). Online and department-store counters are excluded.
  - Full pay only. Discount **REDZ 5%** (LUXE+ 10%) on regular-price items. Points ×3 (LUXE+ ×4).
  - Cashback ฿100 per ฿2,000 per slip, or ฿500 at ≥ ฿10,000. Cap ฿500 per slip and ฿1,500 per account. Register once, on the day of your first spend.
- **Mastercard × Central Midnight Sale** ฿1,500 gift card: see A6.

### B4. Home and IT

- **Thai Watsadu / BnB home · TWD4 · 25 Sep 2026–7 Jan 2027** · CONT [official-card, poster read]
  - Full pay: 3% off regular-price items (**all tiers, REDZ included**). Or 0%: ≥ ฿1,500 for 3 months, ≥ ฿2,000 for 4, ≥ ฿3,000 for 6, ≥ ฿5,000 for 10 (appliances max 6), with up to 10% off selected items.
  - Points 4 per ฿50.
  - Cashback on **accumulated spend per account per day**, supplement included:

    | Full pay per day | Cashback | 0% installments per day | Cashback |
    |---|---|---|---|
    | ฿8,000–14,999 | ฿100 | ฿10,000–19,999 | ฿150 |
    | ฿15,000–34,999 | ฿200 | ฿20,000–44,999 | ฿400 |
    | ฿35,000–69,999 | ฿550 | ฿45,000–79,999 | ฿1,000 |
    | ฿70,000–149,999 | ฿1,200 | ฿80,000–129,999 | ฿1,800 |
    | ฿150,000–349,999 | ฿3,000 | ฿130,000–339,999 | ฿3,000 |
    | ≥ ฿350,000 | ฿8,000 | ≥ ฿340,000 | ฿8,000 |

  - Caps ฿8,000 a day and ฿40,000 per account. Construction materials: no 1.5% card fee and 0% for 4 months. Register the same day.
- **Thai Watsadu / BnB e-coupons (1 Feb–31 Dec)** · CONT, missing from the Sep draft [official-card]. Scan in UCHOOSE: **฿200 off a slip ≥ ฿5,000** and **฿100 off a slip ≥ ฿3,000**. 2 of each per primary account per month; 5,000 of each per month nationwide.
- **Power Buy · PWB3 · 9 Jul–7 Oct** · CONT, then **PWB4 from 8 Oct** (T&C of the iPhone promo says so; details not published) [official-card]
  - Full pay 3% off regular-price appliances, **or** 0% up to 10 months with up to 18% off appliances and 2% off IT. Extra ฿2,000 off at ≥ ฿200,000 installment when redeeming 1,900 points.
  - Cashback per installment slip: ฿9,000–14,999 → ฿140; ฿15,000–34,999 → ฿270; ฿35,000–44,999 → ฿800; ฿45,000–99,999 → ฿1,100; ฿100,000–249,999 → ฿2,600; ≥ ฿250,000 → ฿6,600. Caps ฿6,600 per slip and ฿40,000 per account.
  - Chiang Mai Power Buy branches (from the iPhone list): **Central Festival Chiangmai** and **Chiang Mai Jaeng Hua Lin**.
- **Power Buy points redemption (11 Sep–1 Nov):** see A2 · CONT.
- **iPhone 18 Pro / Pro Max at Power Buy (12 Sep–31 Oct)** · CONT. Points redemption (A2), 5% extra off plus 0% up to 10 months, installment cashback from ≥ ฿9,000 per slip (up to ฿6,600 per slip). The Chiang Mai branches above sell it.
- **Auto1 · AUT2 (1 Jul–31 Dec)** · CONT. 5% off full pay, or 0% up to 10 months with installment cashback: ฿5,000–9,999 → ฿120; ฿10,000–19,999 → ฿280; ฿20,000–29,999 → ฿600; ฿30,000–49,999 → ฿1,000; ≥ ฿50,000 → ฿2,000. Free 38-point car check with the card.
- **Central Retail 0% (all year):** up to 10 months at Central, Robinson, Tops, Muji, Matsukiyo, SuperSports, TWD, BnB, Auto1, Power Buy, OfficeMate and B2S.

### B5. Specialty stores

- **B2S Store + Online · B2SN · 1 May–31 Dec** · CONT, with a correction [official-card, poster read]
  - **REDZ ×3, 5% off** (LUXE+ ×4, 10%).
  - **฿30 on a slip ≥ ฿600** (5%): 1 per primary account per month, first 800 a month.
  - **+฿100 per ฿3,500 per slip:** cap ฿500 per slip and ฿5,000 per account.
  - Register in **UCHOOSE only, before spending**.
- **OfficeMate Store + Online · OFMN · 1 May–31 Dec** · CONT [official-card]
  - **REDZ 3% off** (LUXE 3%, BLACK/THE BLACK 5%). Points 4 per ฿50.
  - Cashback per slip (full pay or installments): ฿5,000–9,999 → ฿100; ฿10,000–24,999 → ฿250; ฿25,000–49,999 → ฿700; ≥ ฿50,000 → ฿1,500. Caps ฿1,500 per slip and ฿30,000 per account.
  - Redeem 12.5% (primary only). 0% storewide up to 10 months. Register before spending. OfficeMate Plus and some branches are excluded.
- **SuperSports + CRC Sports · Monthly Q4 · 1 Oct–31 Dec** · SUCC (identical to Q3) [official-card, poster read]
  - **REDZ 5% off regular-price items, ×3** (LUXE+ 10%, ×4). 0% for 3 months at ≥ ฿1,500.
  - "Up to ฿400" coupon to press for in the UCHOOSE app; tiers not stated.
  - Redeem points 13–18% (A2). **SuperSports Online is excluded.** No registration code.
- **Muji · MJT2 · 1 Oct–31 Dec** · NEW [official-card, poster read]
  - **REDZ 5% off, ×3** (LUXE+ 10%, ×4).
  - Cashback per slip: ฿2,500–4,999 → ฿50; ฿5,000–9,999 → ฿150; ≥ ฿10,000 → ฿400. Caps ฿400 per slip and ฿1,200 per account. 0% 3-month installments excluded. Register on the day.
  - Muji 0% up to 10 months continues all year.
- **Matsukiyo · CMK2 · 1 Jul–31 Dec** · CONT. 5% cashback on every full ฿800 per slip (฿40 per ฿800), cap ฿200 per primary account per month. 0%: 3 months at ≥ ฿1,500, 6 months at ≥ ฿5,000.
- **Others (brief), CONT:**
  - CMG Fashion Mass (Crocs, FitFlop, G2000, Guess, Hush Puppies, Lee, MLB, Skechers, Wrangler…; plaza zone): up to ฿1,000 cashback, to **31 Oct**.
  - CMG Watch (Garmin by CMG, G-Shock): up to 5%, to 31 Dec.
  - Dyson: up to 3%, to 30 Nov.
  - REV Edition (HOKA, Saucony, Champion…): 10% + up to ฿1,500, to 31 Dec.
  - Clarins Skin Suites: up to ฿18,000, to 31 Dec. Posters are in `img/`.

### B6. Dining and delivery

- **อิ่มคุ้มฟิน · EAT · 1 Jul–31 Oct** · CONT [official-card, poster read]
  - Up to 10% off at 120+ restaurants (MK, Sizzler, Sushiro, S&P, Yayoi, Oishi, Greyhound, Kiew Kai Ka…). Kiew Kai Ka's T&C names Chiang Mai branches (Jing Jai, Nimman).
  - Cashback: **฿100 on a slip ≥ ฿1,000** (once a month; ฿400 per campaign), **+฿100 when you have 3 slips ≥ ฿1,000 in a month** (฿400 per campaign). Max ฿200 per primary account per month.
  - Excluded: delivery apps and e-wallets. No stacking with other promotions. Register in UCHOOSE before or on the day.
  - This looks like a Krungsri Consumer-wide campaign: it excludes Krungsri Corporate cards. **Whether REDZ …2611 was registered alongside the Krungsri Cards is unconfirmed.**
  - The restaurant PDF says "up to 23%"; the T1 poster says 13%.
- **CPN Dining "มื้อนี้ดีลดี" · 10 Sep–31 Oct** · CONT, new October pool [official-card]
  - Plaza-zone restaurants at **Central Chiangmai** (the only Chiang Mai mall in the list).
  - Slip ≥ ฿800 → ฿100 cashback. Register the receipt and card at the mall's redemption point **on the day**.
  - Caps ฿100 per card per slip per day and ฿200 per card per month. **4,500 rights for 1–31 Oct**, all branches.
  - **Supplements register separately with their own quota**; the cashback goes to the primary.
  - Chiang Mai freebies (50 each): CHO (Salmon Avocado Roll at ≥ ฿800) and ไอดินกลิ่นครก (half grilled chicken at ≥ ฿800). Saemaeul 10% at ≥ ฿1,200 in October.
  - If card promos overlap, register for only one.
- **Buffet / grill / shabu · BDN · 1 Jul–31 Dec** · CONT. Slip ≥ ฿1,200 → ฿100 (once a month, ฿600 per campaign). Restaurant perks up to 25% (Sukishi, Shabu Chain, Oshinei…). Register once.
- **iberry group** (1 Sep–31 Dec) · CONT. **IBR**: ≥ ฿800 → ฿50 (once a month, ฿200 total). **IBR2**: ≥ ฿1,500 → ฿120 (once a month, ฿480 total).
- **Starbucks** · CONT, with the monthly code:
  - **STC** (1 Sep–31 Dec): buy or top up ≥ ฿1,000 per slip → ฿50. Caps ฿100 a month, ฿400 per campaign. Register in UCHOOSE.
  - **Starbucks / Boost e-coupon · SO10 for October** (1 Jan–31 Dec, **re-register every month from the 1st**, first 1,500 a month): **a slip ≥ ฿100** at participating Starbucks **inside Central malls, including Central Chiangmai and Central Chiangmai Airport** → **฿100 e-coupon** in UCHOOSE.
    - 1 per primary account per store type per month. Arrives within 30 days and expires 90 days after the end of the month it's received.
    - Missing from the Sep draft.
- **Grab (1 Sep–31 Dec)** · CONT. Pay via **GrabPay with the T1 card selected**. One use a month per Grab account for each of T1DIN and T1CAR. Not combinable with Grab promos.
  - **T1TRY**: new users, ฿80 off GrabFood ≥ ฿250. 20 a month.
  - **T1DIN**: ฿60 off GrabFood ≥ ฿350 at partner shops. 1,800 a month.
  - **T1CAR**: ฿50 off rides ≥ ฿250. 550 a month.
- **GrabFood Dine-out · T1DINE (1 Aug–31 Jan 2027)** · CONT. ฿120 off ≥ ฿800 via GrabPay with the T1 card. 1 a day, 4 a month per account, 600 a month nationwide.
- **LINE MAN (1 May–31 Dec)** · CONT. Select the T1 card. One use a month per LINE MAN account for T1EAT and T1CAR.
  - **T1NEW**: new users, ฿80 off ≥ ฿250 food. 500 in total.
  - **T1EAT**: ฿60 off ≥ ฿350 food. **90 a day**.
  - **T1CAR**: ฿50 off rides ≥ ฿200. **10 a day**.
- **Bangkok-only** (skip for Chiang Mai): T1 Exclusive Bites and Taste of Sensation (Central Embassy), Jumbo Seafood 40%, hotel dining, T1 Sunday × Central Park, CVP luxury ×3 + 30% (BLACK / THE BLACK).

### B7. Fuel and EV

- **PTT · code `PTT` · 1 Jun–31 Oct** · CONT [official-card, poster read]. Slips ≥ ฿1,000 at PTT Station:
  - 2–3 fills a month: 3% (฿30 per slip, max ฿90 a month).
  - ≥ 4 fills a month: 4% (฿40 per slip, max ฿160 a month).
  - Register once, on the day of the first fill.
- **Shell · SE10 for October** · SUCC of SE9 (all-year campaign, monthly code) [official-card, poster read]. Slip ≥ ฿100 → ฿100 cashback, 1 slip per primary account per month. **First 1,500 successful registrants each month; registration opens on the 1st.** Register today.
- **EV charging · EVT2 · 1 Aug–31 Oct** · CONT, with a correction [official-card, poster read]. 5% (฿50) per full ฿1,000 per month spent in charging apps (EA Anywhere, Elexa, Evolt, EV Station PluZ, Onion, Reversharger…). Caps ฿150 a month and ฿450 per campaign.

### B8. Online outside the group

- **ช้อปคุ้มทุกคลิก · TNL · 1 Aug–31 Oct** · CONT [official-card]
  - Accumulated monthly full-pay spend in the "participating online-shopping category":

    | Monthly online spend | Cashback |
    |---|---|
    | ฿15,000–49,999 | ฿100 |
    | ฿50,000–99,999 | ฿400 |
    | ฿100,000–199,999 | ฿950 |
    | ≥ ฿200,000 | ฿2,500 |

  - **The documents disagree:** the poster says caps of ฿2,500 a month and ฿7,500 in total, and "ต้องมียอดจาก 5 **ร้านค้า**ขึ้นไป/เดือน". The T&C text says caps of ฿2,300 and ฿6,900 and "5 **รายการ**ขึ้นไป/เดือน". The safe reading is ≥ 5 different shops.
  - **Double Day ×5 points on 10 Oct**: slip ≥ ฿5,000 → 1 base + 4 extra points per ฿25. Caps 3,000 points per day and 9,000 per campaign.
  - Excluded: installments, foreign currency or foreign-provider sites, gold, insurance, transit (Grab is allowed), 7-11, TrueMoney Lotus's/Makro, e-wallet top-ups (MCC 6540), easyBills, and **every Central Group channel**.
  - **No merchant list is published, so whether Shopee or Lazada count is unconfirmed.**
- **Shopee / Makro / Lazada / TikTok:** no Central The 1 promotion at any of them.

### B9. Health, beauty, pets, insurance and education (brief, CONT)

- Happy Health & Beauty Fest **HBF** (hospitals, beauty and spa anywhere; to **31 Oct**). Accumulated per month: ฿15,000–49,999 → ฿100; ฿50,000–119,999 → ฿450; ฿120,000–249,999 → ฿1,400; ≥ ฿250,000 → ฿3,500. Caps ฿3,500 a month and ฿10,500 in total.
- Happy Health Together (hospitals, to 31 Dec). Pets: vet and pet-shop cashback up to ฿450, 10% off at partners, Pet'N Me 0%. Education up to ฿30,000. Insurance up to ฿17,500. HBO Max 33%. Thai Ticket Major ฿100. Beauty clinics 0% + up to ฿40,000 (to 31 Oct).

### B10. Travel (brief)

- **Thai Airways T1TG2 (1 Oct–31 Dec) · NEW:** ฿1,000 off per seat (max 2) on round trips **from Bangkok** to Asia, Australia or Europe. Mastercard T1 only. 400 seats a month.
- **Qatar (1 Oct–31 Mar) · NEW:** up to 10% at `qatarairways.com/krungsri`.
- **Continuing:** Agoda Mastercard 16% (`agoda.com/thmastercard`, to 31 Mar 2027), Trip.com, Klook, Traveloka, AirAsia MOVE, EVA, STARLUX, Emirates, Thai Airways "Rise to Gold", overseas spend (Japan and worldwide), Lotte Duty Free (Korea to 31 Oct, Vietnam), Takashimaya SG, Premium Outlets Japan, Go Hotel.
- Not examined in detail.

### B11. Installments

Central Retail 0% up to 10 months. U PLAN: convert spend to 0.39% × 10 months, foreign spend, medical bills. QR Installment through UCHOOSE. Tops Care and Pet'N Me 0% up to 6 months. Robinson Beauty 0% for 10 months. Power Buy iPhone 0% up to 10 months. GO 0% for 3 months (≥ ฿1,500, participating items). SuperSports 0% for 3 months. All CONT.

### B12. Ended 30 Sep (no successor unless noted)

- TOPS3 → **TOPS4**. Tops Care Q3 → **Tops Care Q4 (TOPS4)**. SuperSports Q3 → **Q4**. CMG Fashion Jul → the Aug version continues to 31 Oct.
- Ended with no successor: Tops 58th Anniversary stickers, GO Pick The Deal "แปะอะไรก็ลด", "30% points super burn", AIA installments, Life Insurance ONTOP, Qatar (Apr–Sep) → new Qatar (1 Oct), Bangkok Airways (Aug–Sep), Centara Holiday Fest, Hanam BBQ, BAR A Q Plaza, Siriraj hospital, Snobbish, Blue by Alain Ducasse, mooncakes.
- **LUXE upgrade offer** (REDZ → LUXE, first-year fee waived) **runs to 31 Oct**. It needs income ≥ ฿100,000 a month; LUXE's fee is ฿4,000 (฿2,000 per supplement), waived at ≥ ฿400,000 a year. CONT.

---

## C. Differences to tell the household

### C1. Card, membership or network?

| Needs | Deals |
|---|---|
| **Central The 1 card** | Every centralthe1card.com cashback and discount: GWS3, TOPS4, TWD4, TWD e-coupons, CMN3 (store coupon too), RPAY9 cashback, PWB3/4, B2SN, OFMN, CMK2, MJT2, GG2, SuperSports 5%, Central App Q4 and Midnight Sale, T1 MAGICAL DAY, EAT, BDN, IBR, CPN dining, Grab and LINE MAN codes, STC, SO10, SE10, PTT, EVT2, TNL, CGT2, AUT2, the card half of ก้าวรับพอยท์. Also the **card point multipliers** (×3 / 4 per ฿50 / 10 per ฿100) and the **card-only point-burn discounts** (Power Buy 15%, SuperSports 13–18%, OfficeMate 12.5%, Beauty 15%, Watch fair, iPhone) |
| **The 1 membership only** (pay with anything) | Base points (1 / ฿25, 1 / ฿50, 1 / ฿100 at GO); **GO Super Wednesday** and **The 1 PAYDAY** point burns; Hug the Earth +100; Robinson Payday 1,000 → ฿150 burn; Level and Exclusive perks; Run Challenge coupons (Central App); the mall half of ก้าวรับพอยท์ (Central X app); Caltex points |
| **Card network, any issuer, via the The 1 app** | Mastercard Friday ฿100 (any Mastercard: REDZ, KTC MC, AEON World MC, Krungsri Lady, Krungsri NOW); Mastercard × Midnight Sale gift card ฿1,500 (to 5 Oct); **Visa ฿500 tap-pay** (any Visa: Krungsri VISA, KTC Digital VISA, First Choice; **not REDZ**) |

**Points pay twice with REDZ.** At Tops, CPN and GO, part of the card multiplier only comes if you **also give your The 1 number**: the regular 1× at Tops and CPN, the GO 1 point. Always show The 1 at the till when paying with REDZ.

### C2. Effective reward rate (point value ฿0.125)

| Where | Member, paying with another card | REDZ | Main REDZ promo on top (October) |
|---|---|---|---|
| GO Wholesale | 0.125% (1 / ฿100) | **1.25%** (10 / ฿100) | GWS3 ≈ 1.17–1.5% per slip ≥ ฿3,000; **Magic XL 1–13 Oct** |
| Tops | 0.5% | **1.5%** | TOPS4 3–4% (+ ฿300 bonus); Magic S |
| Central / Robinson / CPN plaza | 0.5% (plaza IT/furniture 0.25%) | **1.5%** + 5% off regular price | CMN3 / RPAY9 to 4–5 Oct; Magic XL |
| Thai Watsadu / BnB | 0.25% | **1.0%** + 3% off (full pay) | TWD4 daily tiers; e-coupons ฿100 / ฿200 |
| Power Buy / OfficeMate | 0.25% | **1.0%** + 3% off | PWB3 (to 7 Oct), PWB4 (8 Oct, TBA); OFMN |
| SuperSports / B2S / Muji / good goods | 0.5% | **1.5%** + 5% off | B2SN, MJT2, GG2 |
| Anywhere else | – | 0.5% (1 / ฿25; excludes 7-11, TrueMoney, foreign-THB, utilities) | TNL online; EAT; fuel codes |

Using points at GO Super Wednesday (฿0.25) doubles every figure above.

### C3. REDZ vs LUXE / BLACK / THE BLACK in October

- Discount and points gap:
  - Central App (Q4 and Midnight Sale): **5% vs 10%**.
  - SuperSports, B2S, Muji and good goods: **5% and ×3 vs 10% and ×4**.
  - CPN plaza: **×3 vs ×4**.
- Given to higher tiers only:
  - Tops Food Hall / Fine Food 5% off: **LUXE+ only**. Tops on GrabMart ฿150: **LUXE+ only**.
  - CMN3: **+฿2,000** at ≥ ฿50,000 per slip, LUXE / BLACK / THE BLACK only.
  - OfficeMate: REDZ = LUXE = 3%, BLACK / THE BLACK 5%.
  - Power Buy iPhone burn: REDZ = LUXE 15% per 10,000 pts, BLACK 18%, THE BLACK 20%.
  - BLACK / THE BLACK only: CVP luxury ×3 + 30% burn cashback (Bangkok, Phuket), Mastercard Dining, Selfridges. LUXE+: fine-dining (Okura, JW Marriott, Mezzaluna…), Black Tie limo, VitalLife and similar.
- **No gap** on GWS3, TOPS4 cashback, TWD4 (3% for all), PWB3, EAT, CPN dining, T1 MAGICAL DAY or the fuel/EV/Grab codes.
- The **LUXE upgrade offer ends 31 Oct** (income ≥ ฿100,000 a month).

### C4. Combining: what the T&C actually say

- **Explicitly not combinable** with "other promotions" (the wording is ambiguous: other card promos on the same spend): TOPS4, OFMN, CMK2, STC, EAT, BDN, and the Central App Q4 / Midnight Sale discounts (no second card discount). CPN dining says: if card promos overlap, register for **one**.
- **No such clause:** GWS3, CRCT1 (Magic Day), TWD4, PWB3, B2SN, MJT2, CMN3, RPAY9, TNL, PTT, SE10, EVT2, CGT2. Whether Magic Day and TOPS4 both pay on one Tops slip isn't stated.
- **Designed to stack:** CMN3 and RPAY9 store coupons plus card cashback; TWD4's 3% plus daily cashback plus points; SuperSports 5% plus the points burn. **Mastercard Friday** is a CRC coupon. When you pay the rest with REDZ, the card promos compute cashback **after discounts**.
- **GO specifics:** paying by QR or e-wallet loses the 10-point rate and GWS3. The GO coupons (Mastercard Friday, the Magic pack's ฿100) are 1 per GO member number or receipt.
- **Caps are per primary account** (Takumi + Baiboon pooled): GWS3, TOPS4, TWD4, B2SN, MJT2, GG2, SO10, SE10, EAT, BDN, and Magic Day (one XL and one S per account).
- **Per card number** (Baiboon's supplement gets its own): CPN dining (฿200 a month each), ก้าวรับพอยท์ (500 points each).
- **Per person** (name must match The 1): Visa ฿500 and the point burns at SuperSports and Power Buy iPhone. OfficeMate's 12.5% burn is primary cardholder only.
- **Timing:** CMN3, RPAY9, the Midnight Sale app and the Mastercard gift card end on **4–5 Oct**. Magic Day runs to **13 Oct**. For a large department-store buy on 1–4 Oct, CMN3 or RPAY9 plus Magic XL both apply unless the T&C say otherwise; they don't forbid it.

---

## D. GO Wholesale items (also for the GO page)

Card slips post as `CFW-CHIANGMAI …`.

| Item | Mechanic | Period | Who | Status | Source |
|---|---|---|---|---|---|
| **GWS3** | Per slip, in store + GO app: ฿3,000–7,499 → ฿35; ฿7,500–29,999 → ฿95; ฿30,000–119,999 → ฿400; every ฿120,000 → ฿1,800. Caps ฿9,000 per slip per primary account per month and ฿27,000 per campaign. Full pay + installments, after discounts. Register SMS `GWS3` on the day of the first spend. 0% 3 months at ≥ ฿1,500 (participating items). **No changes** | 1 Aug–31 Oct | T1 card | CONT | `?modalId=go-who-202608` [official-card, poster read] |
| **T1 card points** | 10 per ฿100 per slip (9 card + 1 via the GO member number linked to The 1). Excludes installments, QR and e-wallets, alcohol, cigarettes, infant formula; bulk limits (1–40 units per barcode on 9 staple groups) | to 31 Dec | T1 card | CONT | GO `the1-creditcard-point` |
| **T1 MAGICAL DAY XL** | GO slip ≥ ฿4,000 → **฿1,000 Magic e-Voucher + ฿2,000 CRC pack** (the pack includes **GO ฿100 off a receipt ≥ ฿3,000**, paid with a T1 card, in store, valid 1 Oct–15 Nov). Register **CRCT1** in UCHOOSE **from 1 Oct 09:00**, first 2,500 | 1–13 Oct | T1 card | NEW | GO page + card site |
| **Mastercard Friday** | ฿100 coupon (The 1 app) on ≥ ฿1,000, any Mastercard, full pay. **1 per GO member number** | Fridays to 25 Dec | Any Mastercard | CONT | card site; GO page |
| **Visa ฿500** | Tap-pay Visa ≥ ฿5,000 at ≥ 2 CRC stores; GO counts as one store (not online) | to 31 Oct | Any Visa | CONT | GO `crc-visa-aug2026` |
| **The 1 Super Wednesday** | 800 pts → ฿200 off a receipt ≥ ฿2,500. Claim Wednesday, use Wed–Sun. 300 rights per round, 1 per member. Link `offers.onelink.me/H3Sq/hubcfw55` | 7 Jan–27 Dec (Oct: 7, 14, 21, 28) | GO member linked to The 1 | CONT | GO `the1-super-wednesday` |
| **The 1 PAYDAY** | 1,500 pts → ฿400 off ≥ ฿4,500. 1,000 rights, 1 per member | 25 Sep–**1 Oct** | Member | **ends today**; October round not announced | GO `the1-pay-day` |
| **The 1 Hug the Earth** | Buy ≥ 5 packs of Namthip water → +100 The 1 points. Register at `go.the1.co.th/UohD/566spxnq` first | 30 Sep–27 Oct | Member | NEW | GO `the1-hug-the-earth` |
| **The 1 Exclusive coupon** | ฿300 off a receipt ≥ ฿12,000, 1,000 a month | 1 Jan–31 Dec | Exclusive only | CONT | GO `the1-exclusive` |
| Fresh-vegetable coupon (GO's own) | Buy listed vegetables ≥ ฿300 per receipt → ฿90 coupon. 14 per member number | 30 Sep–13 Oct | GO member | NEW | GO `fresh-vegetable-coupon` |
| T1 card sign-up gift | Apply for REDZ, get a suitcase worth up to ฿6,990 (not relevant; the household holds REDZ) | 1 Aug–31 Oct | new applicants | CONT | GO `the1-acquisition-mar26` |
| **GO Pick The Deal** (฿65 card coupon at ≥ ฿3,500, stickers) | – | 19 Aug–30 Sep | – | **ENDED**, no successor on GO or the card site | card site diff |
| Member point rate | 1 per ฿100 if the GO membership is linked to The 1 | – | Member | – | GO page |

**GO worked example with REDZ** (a ฿4,000 slip, 1–13 Oct, CRCT1 registered), assuming the promos stack (the T&C doesn't forbid it):
- GWS3: ฿35.
- Points: 400 ≈ ฿50 (฿100 if burned at Super Wednesday).
- Magic e-Voucher: ฿1,000, plus the ฿2,000 coupon pack.
- **≈ 27% plus the pack.** Possible once per primary account.

After 13 Oct, a ฿3,000 slip gives ≈ 1.17% + 1.25% points ≈ 2.4%.

---

## E. Suggested October plan for REDZ in Chiang Mai

For the lead's Thai page; numbers are from the sections above.

1. **1 Oct at 09:00: register CRCT1 (both XL and S) in UCHOOSE.** Also today: **SE10** (Shell, first 1,500) and **SO10** (Starbucks, first 1,500). Then make one XL slip ≥ ฿4,000 by 13 Oct (GO, Central, Robinson, Thai Watsadu or Power Buy) and one S slip ≥ ฿1,000 (Tops, Muji, Matsukiyo or B2S).
2. **Tops:** register TOPS4 and keep **≥ ฿3,000 every month in Oct, Nov and Dec** for the ฿300 bonus. Show the The 1 number to get the full ×3.
3. **GO:** keep slips ≥ ฿3,000 (GWS3), link the GO membership to The 1, and burn points on **Wednesdays** (800 → ฿200).
4. **Big department-store buy:** do it by 4 Oct (RPAY9) or 5 Oct (CMN3) so it also counts as the Magic XL slip.
5. **Thai Watsadu:** keep slips ≥ ฿5,000 to use the ฿200 e-coupon (twice a month), and daily totals ≥ ฿8,000 for TWD4.
6. **Visa ฿500:** each person can tap-pay their own Visa ≥ ฿5,000 across two CRC stores in one day, e.g. Tops + GO (quota unknown). **Mastercard Friday:** one coupon per The 1 account each Friday, two on 9 and 16 Oct.
7. **Central Chiangmai dining:** slips ≥ ฿800 in the plaza zone → register at the counter the same day. Takumi and Baiboon each get their own ฿200 a month.
8. **10 Oct:** TNL Double Day ×5 for an online slip ≥ ฿5,000 (outside Central Group).

---

## F. Not found / unconfirmed

1. **PWB4** (Power Buy from 8 Oct): named in the iPhone T&C, not yet published.
2. **October Robinson Payday / Central Midnight Sale 4**: not published at 03:30. RPAY9 and CMN3 end 4 and 5 Oct.
3. **GO The 1 PAYDAY October round**: not announced. The Sep round ends 1 Oct.
4. **Magic e-Voucher usage rules** (minimum spend, excluded stores): not published. The card site's poster attachment returns 404; I read the GO copy.
5. **Robinson Gift Card Big Bonus SMS code**: not on the page.
6. **Mastercard Friday Central App code for October**: the Sep poster shows PMC261.
7. **Visa ฿500**: remaining quota of the 11,000; "within 3 days" (GO) vs "same day" (KTC); coupon delivery 45 vs 30 days.
8. **TNL**: 5 shops vs 5 transactions; caps ฿2,500 / ฿7,500 vs ฿2,300 / ฿6,900; whether Shopee or Lazada count.
9. **The 1 app member-only October content** (Tops member deals, app-wide double points, point sales): the app isn't publicly readable and none was found in news. No October "10.10" The 1 event found.
10. **Household's The 1 levels**; whether Baiboon has her own The 1 account; whether REDZ …2611 and the supplement are registered for Krungsri Consumer-wide codes (EAT, BDN).
11. **Bank → The 1**: KBank K Point rate (search snippet only), ttb (page is JS-only, not read), KTC, AEON and CardX (no transfer found). **No October transfer bonus** from any source.
12. **Robinson Payday store coupon**: whether non-T1 payers get it. central.co.th says "สมาชิกเดอะวัน"; the card poster says card members.
13. **CPN ก้าวรับพอยท์ mall-side conditions** (Central X): not found.
14. **Level 1 "5% discount"** mechanics: the press release gives none.
15. **EAT**: the list PDF says "up to 23%", the poster says 13%. Chiang Mai participation beyond Kiew Kai Ka isn't checked restaurant by restaurant.
16. The T&C say "no stacking" but it's ambiguous which promotions count as "other" (TOPS4 × Magic Day).

## G. Key URLs

- Card list API: `POST https://www.centralthe1card.com/gcspromotion`. Pages are `https://www.centralthe1card.com/promotion?modalId=<code>`. Codes used: `cen-retail-202610`, `go-who-202608`, `top-cashback-202610`, `top-care-202610`, `top-online-prime-202610`, `cen-app-monthly-202610`, `cen-app-mid-202609`, `cen-mid-202609`, `rbs-payday-202609`, `twd-bnb-202609`, `twd-bnb-all-202602`, `pwd-store-202607`, `pwd-redeem-point-202609`, `pwd-iphone18-202609`, `b2s-store-online-202605`, `ofm-store-online-202605`, `ssp-202610`, `muji-202610`, `cmk-matsukiyo-202607`, `good-good-202610`, `cpn-202610`, `cpn-x3-202308`, `cpn-dinning-202609`, `full-eat-202607`, `shabu-202607`, `iberry-202609`, `starbucks-202609`, `starbucks-boot-juice-bar-202601`, `grab-202609`, `grabfood-dineout-202608`, `line-man-202605`, `ppt-202606`, `shell-2026`, `ev-station-202608`, `nationwide-202608`, `cen-retail-202601` (Mastercard Friday), `extra-point-day-202605`, `cds-new-202607`, `rbs-new-202607`, `health-fest-202608`, `luxe-upgrade-202607`, `thai-airways-202610`.
- Poster base: `https://www.centralthe1card.com/getattachment/<guid>/<file>.webp` (listed in `research/the1/imglist.txt`).
- REDZ product page: `https://www.centralthe1card.com/Product-Listing/product-detail-redz`.
- GO: `https://centralfoodwholesale.co.th/promotion/` and `…/the1-super-wednesday/`, `…/the1-pay-day/`, `…/the1-hug-the-earth/`, `…/the1-exclusive/`, `…/the1-creditcard-point/`, `…/crc-visa-aug2026/`, `…/fresh-vegetable-coupon/`, and the Magic e-Voucher page.
- Central/Robinson: `https://www.central.co.th/e-shopping/instore-promo`, `…/central-gift-card-big-bonus-24sep26`, `…/robinson-gift-card-big-bonus-29oct26`, `…/robinson-payday-11-sep-2026`, `…/central-run-challenge`, `…/robinson-run-challenge`, `…/mastercard-x-central-midnight-sale-5`, `…/mns3ct1`.
- Bank transfers: `https://www.krungsricard.com/th/promotion/the-one-point`, `https://www.firstchoice.co.th/promotion/the1-transfer`, `https://www.uob.co.th/personal/promotions/creditcard/the1/the1-point-transfer.page`. KTC's Visa page: `https://www.ktc.co.th/promotion/shopping/the1app-x-visa`.
- The 1: `https://www.the1.co.th/the1-membership` (rates are in `research/the1/nuxt/40c7dd4.js`). Tier news: thansettakij.com/social-biz/655978, brandbuffet.in.th/?p=292836, biznewsupdate.com/2026/04/the-1-4.html. Point Festival: siamturakij.com. Caltex: `https://www.caltex.com/th/motorists/rewards-and-offers/the-1-card.html`.
