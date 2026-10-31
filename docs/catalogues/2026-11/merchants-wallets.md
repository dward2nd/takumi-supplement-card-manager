---
tags: [catalogue-research, 2026-11]
researched: 2026-11-01
---

> **Research snapshot**: The merchants' own deals and wallets — Makro / Makro PRO, Shopee, Shell, PTT (OR), TrueMoney / ShopeePay / LINE Pay / Pao Tang and the government 60/40 — November 2026 research. Read on **2026-11-01** from the official pages, for the November 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages (Makro, GO Wholesale, Shopee, The 1, Shell, PTT). Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions stayed in the session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# Merchants & wallets — November 2026 (Makro · Shopee · Shell · PTT · wallets)

Researcher: `merchants-wallets`. Read Sun 1 Nov 2026 (1 พ.ย. 69) from about 01:40 local time; egress Hong Kong. Read-only; no Notion.
Confidence labels: **V** verified on the official page today · **R** my reading of official terms · **T** third-party only · **U** unverified.
Last month's report: [[../2026-10/merchants-wallets]].

Shell and PTT (both new pages) are long, so they live in a companion file: **[[fuel-stations]]**. This file covers Makro, Shopee, the wallets and the government scheme, and carries the headline list, lineage rows and site tricks for all of them.

## Headline changes vs October

1. **Makro PRO has a Q4 bank/wallet partner hub after all** — `https://www.makro.pro/th/fp/partnership` ("All Partnership 2026 - Q4"). October's report found none. It links UOB Makro (UMK26), CardX HY1 + POINTX 12/14%, KTC 13%, First Choice NW4, GSB, **Bangkok Bank `BNYB` (new, 1 Nov 69 – 28 Feb 70)**, **ShopeePay ฿200 off ฿3,000**, three 0% plans and TrueMoney (§1.1, §1.5).
2. **First Choice NW4 at Makro may count only through TrueMoney.** Makro PRO's copy of the NW4 terms says Makro joins "เฉพาะ การชำระด้วยบัตรเครดิตผ่านการผูกบนแอป True Money Wallet ที่หน้าสาขาเท่านั้น", and First Choice's own NW4 page excludes "MCC code 5199 อาทิ Makro และ Makro PRO". This contradicts the vault's note that `HTTPS://WWW.MAKRO.PRO/` (MCC 5411) counts. Baiboon's biggest Makro card is First Choice (฿125k May–Oct) — **flag for the bank researcher / lead** (§1.3).
3. **Makro "Instant Discount" 1–4 Nov only**: ฿280 off ฿17,000+ of participating items per receipt (app coupon) (§1.2).
4. **TrueMoney × Makro**: new **Pay Next / Pay Next Extra "whole basket up to 48 months"** on Makro PRO, 16 Oct – 31 Dec (18–25% interest, not 0%). Makro_THT ×2 points still has **no successor**. Pay Next 3% round 4 runs to 31 Dec, but the page header still says the campaign is full (§1.3).
5. **Shopee 11.11 "ลด ใหญ่ มาก"**: per Shopee's own App Store / Google Play text, **collect codes from Sun 8 Nov, use them Tue 10 – Fri 13 Nov**; ร้านโค้ดคุ้ม code up to ฿11,111 in the first 11 minutes, ฿11 deals at 11 time slots, free shipping from ฿0 (§2).
6. **Shell (new page)**: Shell GO+ in the Shell Asia app (1 point ≈ ฿0.20); the **V-Power Club per-litre discounts ended 31 Oct** with no November extension; the motorbike-friendly offers are the **biker deal (5 × V-Power ≥ ฿100 → 100 points)** and the **Shell Plus Package ฿299** (sold on Shopee/Lazada/TikTok). Descriptor `SHELL 0583F CO …` = site 0583, **CO = Company Owned** (vs `DO` dealer). Prices 29 Oct: FuelSave 95 ฿42.04, E20 ฿33.70 ([[fuel-stations]] §1).
7. **PTT (new page)**: blueplus+ (100 points = ฿20 at the pump; Café Amazon 1 pt/฿20); **Self Serve ฿1/L ended 31 Oct** with no extension posted; Smooth Bag stamps to 30 Nov need ฿1,000 fills; blueplus+ wallet ฿100 back on a first ≥ ฿300 payment to 15 Dec. `PTTST.C` = company station, `PTTST.D` = dealer, `PTTRM_` = PTT Retail Management ([[fuel-stations]] §2).
8. **Fuel tax cut**: excise on E20 and B20 cut for 28 Oct 69 – 27 Jan 70; both ≈ ฿33.50/L in Bangkok (news, **T**).
9. **Government 60/40 (เพิ่มเติม) ends Mon 30 Nov 69**; Makro, GO, Shell and PTT forecourts still don't qualify (§4).

---

# 1. Makro / Makro PRO (the merchant's own)

How read: `curl` of `https://www.makro.pro/th` → `__NEXT_DATA__` → `props.pageProps.dehydratedState.queries[0].state.data.flexiPage.components` (the `_flexiPage` copy has `data: null` for banner components now; read the dehydrated copy). Static pages `https://www.makro.pro/th/static/<handle>` carry their T&C in `props.pageProps.cmsData.attributes.description` (HTML).

## 1.1 Makro PRO's Q4 "Partnership" hub — **new find** (`/th/fp/partnership`)

The homepage banner "All Partnership 2026 - Q4" opens https://www.makro.pro/th/fp/partnership. It lists every payment partner Makro PRO promotes for Oct–Dec. October's report said there was no bank-partner page; this is it. Tiles (label dates as printed on the tile):

| Tile | Label dates | Static page (`/th/static/…`) | Notes |
|---|---|---|---|
| UOB (header) + UOB grid | 1 Oct – 31 Dec 26 | `uob-makro-credit-card`, `uob-makro-26th-anniversary` | UOB Makro's 26th anniversary — bank researchers / `docs/promotions/uob-makro-gold-mission.md` |
| SCB CardX | 1 Oct – 31 Dec 26 | `cardx-scb-wealth-cashback-14-percent-makropro` | "รับเงินคืนสูงสุด 14%" (POINTX redemption) |
| KTC Cashback 13% | 1 Aug – 31 Dec 26 | `ktc-credit-card-cashback` | points → 13% credit |
| First Choice | 1 Oct – 31 Dec 26 | `first-choice-credit-card` | "รับเครดิตเงินคืนสูงสุด 6,000 บาท" |
| GSB | Jan – 31 Dec 26 | `gsb-cashback-5400thb` | up to ฿5,400 |
| **Bangkok Bank** | **1 Nov 26 – 28 Feb 27** | `bangkok-bank-credit-card` | **new** — see §1.5 |
| **ShopeePay** | 1 Oct – 31 Dec 26 (tile) | `get-thb-200-off-with-shopeepay-on-a-minimum-spend-of-thb-3000` | see §1.4 (T&C says 1–31 Oct) |
| First Choice 0% | 1 Oct 26 – 31 Jan 27 | `first-choice-credit-card-installment` | 0% up to 24 months |
| CardX 0% | 1 Oct 26 – 31 Jan 27 | `scb-cardx-electronics-installment` | 0% up to 10 months + points → up to ฿42,000 |
| KTC 0% | 1 Feb 26 – 31 Jan 27 | `ktc-credit-card-redeem-point` | points → 0% 3 months |
| TrueMoney: first payment | 7 Sep – 31 Dec 26 | `1st-time-pay-at-makropro-get-50-points` | see §1.3 |
| TrueMoney: Pay Next / Pay Next Extra whole basket up to 48 months | 16 Oct – 31 Dec 26 | flexi `pay-next-extra` | see §1.3 |

The bank tiles belong to the bank researchers; the ones not already in the repo are summarised in §1.5 so they can cross-check. **Confidence V** (official page, read 1 Nov).

## 1.2 Makro's own (points, Club, events)

### Makro PRO Point — standing earn rate (continuing)
- 1 point per ฿1,000 (0.1%); 1 point = ฿1 off. Unchanged from October. The homepage banner "Point Expiry (16 Sep – 31 Dec 26)" is still up: points due to expire must be used **by 31 Dec 69**. **V** (homepage JSON; banner `strapi-cdn…/uploads/Web_homepage_banner_TH_3a01c23a8a.jpg`).

### Makro Club (paid, ฿1,299/yr) — continuing, unchanged
- T&C (https://www.makro.pro/th/static/t-n-c-for-makro-club) still says: **1 PRO Point per ฿100 on participating items (1%)**, capped at **1,500 points a month and 10,000 a year**, then back to 1 per ฿1,000; 100 points on first sign-up (use within 30 days); 50 points in the birthday month; 7-day full refund. **V**.
- **Club × TrueMoney**: 1% in PRO Points, **max 50 points per member a month**, when you spend **฿5,000+ a month** with Pay Next / Pay Next Extra at a branch, or through TrueMoney on any Makro PRO channel (banner `True_Money_TH_aa0b800967.jpg`). **V** (banner).
- Partner perks on the Club page (https://www.makro.pro/th/fp/makro-club-join-now): TrueMoney (above), SLC & S'RENE, **Bangchak** ("คูปองส่วนลดแทนเงินสดเติมน้ำมันบางจากไฮพรีเมี่ยม" — a cash-discount coupon for Bangchak Hi Premium fuel; value not printed), Better Vision, MorDee, and **new: Cockpit** ("ส่วนลดพิเศษเมื่อซื้อยางรถยนต์", a special discount on tyres; value not printed). **V** (banners); amounts **not found**.

### "Instant Discount" — 1–4 Nov 69 only (new)
- Banner: **"ยิ่งช้อป ยิ่งคุ้ม รับส่วนลด 280.-* เมื่อซื้อสินค้าที่ร่วมรายการครบ 17,000.-/ใบเสร็จ"** — ฿280 off when you buy **participating items** of **฿17,000+ per receipt**, 1–4 Nov 69 ("4 วันเท่านั้น"). It links to the app's Loyalty Reward Centre (`deep_link_value=loyalty-reward-campaign`), so it's an app-collected coupon. The "*" means there may be lower tiers; the full ladder and whether it's store, app or both weren't readable without logging in. 1.6% at the ฿17,000 floor.
- Banner `strapi-cdn…/uploads/ID_5095_Instant_Discount_Inbetween_TH_ebf93a1da8.jpg`. **V** (banner) for the ฿280 / ฿17,000 line; other tiers **U**.

### Referral and new-customer pack
- **New-customer pack "RAK MAK MAKRO x LYKN"** (https://www.makro.pro/th/fp/live-like-a-pro-makro): still live, posters labelled 1 Oct – 30 Dec: ฿100 off ฿1,000 on a first app order (1 per MMID), free "ส่งด่วน" delivery on a first order of ฿500+, 1 point buys a ฿1 item (new customers). A new "Prize 1 THB | Stack All items (28 Oct – 10 Nov 26)" block refreshes the ฿1 items. **V**. Little use to the household (existing members).
- **Referral "ชวนปั๊บ รับพอยท์"**: the page still shows the banner "37th Anniversary | Referral Program **(Oct 26)**" (up to 30 PRO Points per friend). No November-dated referral banner found; whether it still pays in November is **U** (T&C behind login at `account.makro.pro/en/account/referral-program`).

### November price campaigns (not payment offers)
- Makro Mail 23 (28 Oct – 10 Nov), Seasonal Hamper (1–30 Nov, `fp/seasonal-hamper`), Mega Deals Hit Early (30 Oct – 2 Nov), "Thai Help Thai Plus" product collection (28 Oct – 10 Nov, `fp/thai-helps-thai` — still a price-cut collection, **not** the government 60/40), Diwali (28 Oct – 10 Nov), Gold Container daily deals, Gone Forever Deals, HORECA Quality Products (to 1 Nov). **V** (homepage JSON).
- **No 11.11 or payday campaign on Makro PRO** (handles `fp/1111`, `fp/11-11`, `fp/makro-11-11`, `fp/payday` → 404). **V** (404s).

## 1.3 TrueMoney at Makro (wallet / Pay Next)

| Offer | Period | Mechanic | Caps | Conf. |
|---|---|---|---|---|
| **Pay Next / Pay Next Extra — "ผ่อนได้ทั้งตะกร้า นานสูงสุด 48 เดือน"** (installments on the whole basket) | **16 Oct – 31 Dec 69** | On Makro PRO checkout pick TrueMoney → "ผ่อนชำระด้วย เพย์ เน็กซ์" (up to 5 months) or "เพย์ เน็กซ์ เอ็กซ์ตร้า" (up to 48 months). **Not 0%**: 18–25% a year reducing balance (the step-3 screenshot shows 4 months at 18.86%, 6 at 20.09%, 12 at 21.25%, 18 at 19.36%). | — | **V** (flexi `pay-next-extra`, posters `seasonal_3d865fb176.jpg`, `education_Artboard_1_*`) |
| Pay Next / Extra **3% cashback**, round 4 | 1 Oct – 31 Dec 69 | 3% back on each Pay Next / Extra payment ≥ ฿100 at participating shops | ฿100 per registration round (shared across both), 20,000 rights a round; not combinable (clause 8) | **V** terms; the page header still says "ขออภัยสิทธิ์เข้าร่วมแคมเปญเต็มแล้ว" (full) on 1 Nov — round 3 is the one marked full in the body, so whether round 4 still has rights is **U**. https://www.truemoney.com/a/paynext-extra-promotion-02/ |
| Pay Next Extra 0% up to 48 months on appliances + cashback ฿100–2,000 a slip | 1 Mar – 31 Dec 69 | unchanged from October (tiers ฿3,000–80,001+) | ฿4,200 per ID a month; 2,750 rights in all | **V** (listing title) https://www.truemoney.com/a/promotion-makro-02/ |
| First TrueMoney payment → 50 PRO Points | TrueMoney's page: 15 Feb – 31 Dec 69 (in store or app). **Makro PRO's own T&C: 7 Sep – 31 Dec 69, Makro PRO app/web only** | ≥ ฿1,000 net per receipt, first-ever TrueMoney payment on Makro PRO; register on the activity page first | 1 per ID card; points within **60 working days** (Makro's page; TrueMoney's says by the 15th of next month) | **V** (both pages; they differ on channel and timing) https://www.makro.pro/th/static/1st-time-pay-at-makropro-get-50-points |
| Card linked in TrueMoney at Makro (`TMN MAKRO`) | since 15 Oct 68 | no fee, no minimum | — | **V** https://www.truemoney.com/a/makro-promotion-04/ |
| Makro_THT ×2 PRO Points | ended 30 Sep | **no successor** on 1 Nov (TrueMoney's list still shows the ended page) | — | **V** |

**First Choice NW4 at Makro — check this (bank-side, found on Makro PRO's First Choice page).** Makro PRO's copy of the NW4 terms (https://www.makro.pro/th/static/first-choice-credit-card) adds: **"หมายเหตุ: สำหรับแมคโคร เข้าร่วมรายการเฉพาะ การชำระด้วยบัตรเครดิตผ่านการผูกบนแอป True Money Wallet ที่หน้าสาขาเท่านั้น"** — at Makro, NW4 counts **only** First Choice paid through a card **linked in TrueMoney at a branch** (`TMN MAKRO`). First Choice's own NW4 page (https://www.firstchoice.co.th/promotion/firstchoice-cashback) lists "หมวดการใช้จ่ายใน MCC code 5199 อาทิ Makro และ Makro PRO" among the exclusions. The vault (`docs/promotions/first-choice-2026h2.md`) says `HTTPS://WWW.MAKRO.PRO/` (MCC 5411) counts within the ฿30,000 supermarket cap — the two official pages suggest Makro (store **and** PRO) may not count at all except through `TMN MAKRO`. Baiboon put ฿125k of Makro on First Choice May–Oct. **R** (my reading of two official pages); the bank researcher should confirm with Krungsri / the UCHOOSE eligible list.

## 1.4 Other wallets and QR at Makro

### ShopeePay at Makro — ฿200 off ฿3,000 (existing users) / 5% off ฿500 (new users)
- Pay by **ShopeePay QR in the ShopeePay app** ("สแกนจ่าย" Makro's ShopeePay QR, or show your ShopeePay QR to the cashier), then pick the code before confirming. Funding: ShopeePay Wallet, linked bank, **credit/debit card** or **SPayLater**.
- **Existing ShopeePay users: ฿200 off ≥ ฿3,000** (6.7% at the floor); **new users: 5% off ≥ ฿500** (cap not stated). 1 use per ShopeePay account per code. **2,000 rights (new) + 5,000 (existing) for the campaign.** Makro only.
- **Dates conflict**: the tile on Makro PRO's partnership page and the poster say **1 Oct – 31 Dec 69**; the T&C text on the page (published 8 Oct) says **"1 ตุลาคม 2569 - 31 ตุลาคม 2569 (หรือจนกว่าสิทธิ์จะหมด)"** with a stray editor note "[NM2.1]". Treat November as **U** until the code shows in the ShopeePay app.
- Household angle: a card funding ShopeePay usually posts as a ShopeePay/Shopee descriptor, not Makro; most bank Makro campaigns and NW4 exclude e-wallets. SPayLater interest 0–25% a year.
- URL https://www.makro.pro/th/static/get-thb-200-off-with-shopeepay-on-a-minimum-spend-of-thb-3000 · tile `Deals_Carousel_1_TH_baa4e9cc3a.png`. **V** (page) / dates **U**.

### Not found at Makro
- LINE Pay / Rabbit LINE Pay, Alipay+, Pao Tang: no Makro promotion found.
- **UnionPay QR** at Makro: still **not confirmed** — no Makro page names UnionPay among payment methods; the Makro PRO checkout screenshots show only "คิวอาร์โค้ด/โอนชำระเงินผ่านธนาคาร", TrueMoney (wallet / Pay Next / Pay Next Extra), "บัตรเครดิต / เดบิต" and "ชำระผ่านบิล".

## 1.5 Bank partner tiles on Makro PRO (for the bank researchers to cross-check)

Read from the static pages on 1 Nov; I didn't verify against the banks' own sites except where noted.

- **Bangkok Bank `BNYB` — NEW, 1 Nov 69 – 28 Feb 70**: redeem Thank You Rewards points equal to the slip for credit at participating stores (store and online): **฿800–1,499 → 12%**, **฿1,500+ → 15%**, **฿5,000+ → 18% (Pinnacle, Infinite, Leader Platinum only)**. Max **50,000 points per person a month** across cards and stores. Full payment only (no installments); primary cards only (not Titanium, AirAsia, M Visa, supplements). **Register by SMS on the day of the purchase: `BNYB <16-digit card>` to 4712008** (฿3 per SMS). Credit within 90 days. https://www.makro.pro/th/static/bangkok-bank-credit-card · **V** (Makro PRO page). Not a household card.
- **GSB "ช้อปซูเปอร์คุ้ม"**, 1 Jan – 31 Dec 69: per-slip at supermarkets/hypermarkets ฿2,000–5,999 → ฿40, ฿6,000–14,999 → ฿150, ฿15,000+ → ฿450; cap ฿450 a month, ฿5,400 a campaign per person; e-wallets excluded; SMS `GS#<last 12>` to 0625965522. https://www.makro.pro/th/static/gsb-cashback-5400thb · **V** (Makro page).
- **KTC points → 13%**, 1 Aug – 31 Dec 69: register each time at `ktc.promo/supermarketY26` on the day; max 30,000 points a month per cardholder. **V** (Makro page). Household: KTC cards (but KTC cards can't be swiped at Makro stores per the vault; this is Makro PRO).
- **CardX / SCB `HY1`** (same tiers as GO: ฿40 / 200 / 720 a slip; ฿1,440 a month, ฿4,320 total; +฿3,000 at ฿300,000, 150 rights) and POINTX → **12% Mon–Thu / 14% Fri–Sun**, max 50,000 points a month and 150,000 a campaign; 0% 4 months on ฿2,000+. **V** (Makro page). Household: Nuta's CardX JCB.
- **First Choice NW4** — see the TrueMoney note in §1.3. **UOB Makro UMK26** — already in `docs/promotions/uob-makro-gold-mission.md` (the page excludes "การใช้จ่าย ณ สถานบริการน้ำมัน" and e-wallets such as TrueMoney).

---

# 2. Shopee (Thailand) — platform, ShopeePay, SPayLater, Coins

Shopee's own campaign pages (`shopee.co.th/m/…`) are still captcha-walled; the official sources are Shopee Thailand's **App Store / Google Play listing text and screenshots** and the **Help Center API** (`help.shopee.co.th/api/inhouse/hc/mobile/v1/article?id=<id>`).

## 2.1 Shopee 11.11 "ลด ใหญ่ มาก" — Wed 11 Nov 69 (new)
- **App Store** (id959841453, version 3.85.26 of 28 Oct): "ใส่ตระกร้ารอช้อปกับ 11.11 ลด ใหญ่ มาก ช้อปสนุกสุดคุ้มกับส่วนลดร้านโค้ดคุ้ม 11,111 บาท ส่งฟรี* 0.- พร้อมดีลเด็ด 11 บาท 11 เวลา … **เก็บโค้ดส่วนลด ตั้งแต่วันที่ 8 พฤศจิกายน และใช้ในวันที่ 10-13 พฤศจิกายนนี้**". Google Play carries the same text ("Shopee 11.11 ลด ใหญ่ มาก ส่วนลดร้านโค้ดคุ้ม 11,111.- มาพร้อมดีลเด็ด 11 บาท"). **V**.
  - **Collect codes from Sun 8 Nov; use Tue 10 – Fri 13 Nov.**
  - **ร้านโค้ดคุ้ม (Xtra) code "สูงสุด 11,111.-" in the first 11 minutes ("11 นาทีแรก")**; the voucher card in the screenshot reads "ส่วนลดร้านโค้ดคุ้มสูงสุด 11,111.- · ร้านโค้ดคุ้ม Xtra · ใช้ได้ 11 พ.ย. 69". The percentage and minimum spend aren't shown. (Another screenshot headline reads "ส่วนลดร้านโค้ดคุ้ม 1,111.-", so the ฿11,111 is the top of a range.)
  - **"ดีลเด็ด 11.-" at 11 time slots** (flash tabs 00:00 / 12:00 / 18:00 / 20:00 shown), **free shipping from ฿0 at ร้านโค้ดคุ้ม shops** ("ส่งฟรี* ร้านโค้ดคุ้ม ขั้นต่ำ ฿0 · ร้านค้าที่กำหนด · ใช้ได้ 11 พ.ย. 69"), a "โค้ดลดจากพาร์ทเนอร์" tab (the bank-code hub), new-customer ฿1 deals and codes up to ฿300.
  - Screenshots are marketing mock-ups — **U** for any figure not in the listing text.
- For comparison (not Shopee): **Lazada 11.11 runs 10 Nov (20:00) – 13 Nov 69** (Lazada's Google Play text). **V**.
- Bank 11.11 codes: KTC's `shopee-1111` page and others — bank researchers.

## 2.2 Shopee Payday (November)
- Not announced on 1 Nov. Pattern: the 25th of the month (Wed 25 Nov), with codes at 00:00 and 12:00; June 2569 ran 25–27 Jun (Thairath). **T**. Bank Payday codes run "from the 25th to month-end" (e.g. KTC `KTCPAYDAY` ฿300 off ฿2,000, all 2569 — October report).

## 2.3 Shopee Coins and Shopee Rewards (standing, re-read 1 Nov)
- **1 Coin = ฿1** in the app, at partner shops and ShopeeFood; Coins expire (details behind the article link). Article [80515](https://help.shopee.co.th/portal/4/article/80515). **V**.
- **Shopee Rewards** tiers per half-year (1 Jan–30 Jun, 1 Jul–31 Dec): Classic 0 · **Silver 6 orders / ฿1,500 · Gold 24 / ฿7,500 · Platinum 50 / ฿30,000**; points reset each half-year. Article [80413](https://help.shopee.co.th/portal/4/article/80413). **V** (unchanged).

## 2.4 ShopeePay and SPayLater
- **ShopeePay Payment Channel Promotion**: automatic extra discount for eligible users paying by ShopeePay Wallet or ShopeePay bank debit; stacks with other codes; first come first served; not refunded on returns ([183609](https://help.shopee.co.th/portal/4/article/183609)). No November amounts published. **V** (mechanism).
- **ShopeePay at Makro**: ฿200 off ≥ ฿3,000 / 5% off ≥ ฿500 (see §1.4 — dates conflict). This is the only ShopeePay merchant offer found for the six pages.
- **SPayLater** scans merchant PromptPay QRs ([183049](https://help.shopee.co.th/portal/4/article/183049)); lender **Monee (Capital) Co., Ltd.** ([183503](https://help.shopee.co.th/portal/4/article/183503)); interest 0–25% a year (Makro's ShopeePay T&C). No November SPayLater campaign text found; the 11.11 screenshots show no SPayLater figure this time.
- **shopeepay.co.th/marketing** is still an empty shell. **V**.

## 2.5 Shell on Shopee
- **Shell Plus Package** (฿299 / ฿599 / ฿1,699, valid 6 months) is sold on Shopee, Lazada, TikTok and Shell Plus Official since 23 Sep 69 — a fuel/café discount pack bought online and used at the pump. Details in [[fuel-stations]] §1.4. **V**.

---

# 3. Shell and PTT

See **[[fuel-stations]]** (Shell GO+, V-Power Club, Shell Plus Package, Shell Café, descriptors, payments, prices; blueplus+, OR's own November offers, descriptors, payments, provincial prices; logos).

---

# 4. Wallets and government

## 4.1 TrueMoney
- At Makro: §1.3. At **Shell / PTT**: TrueMoney's promotion list (https://www.truemoney.com/promotion/, read through r.jina.ai) has **no Shell, PTT, Bangchak or Caltex entry** on 1 Nov. **V**.
- **Linked Visa → any PromptPay shop QR** (`TMN*PROMPTPAY30` on statements): https://www.truemoney.com/debit-credit-card/promptpay/ still reads "ผูกบัตรเครดิต / เดบิต VISA … ใช้จ่ายร้านค้าพร้อมเพย์ได้แล้ว … ไม่มีขั้นต่ำ ไม่มีค่าธรรมเนียม … (ร้านไม่รับบัตรก็จ่ายได้)". **Visa only**. The page shows no ฿30 first-scan offer today (October's ฿30-to-31 Dec came from a third party). **V** (page) / ฿30 offer **U**.
- **"เติมเงินเข้าทรูมันนี่ ใช้บัตรเครดิตเติมเงินเข้าวอลเล็ทได้แล้ว"** (credit-card top-up into the wallet) is listed "1 ธ.ค. 69 - เป็นต้นไป" on TrueMoney's promotion list, but the page (https://www.truemoney.com/a/redirect-fundin/) was posted 7 Jan 2026, so the year is probably a typo for 68 (a standing feature, not a December launch); it has no terms. Note for the bank researchers: most cards exclude e-wallet top-ups. **U**.
- Pay Next / Pay Next Extra 3% (round 4, ฿100 a round) and the whole-basket installment offer: §1.3.

## 4.2 LINE Pay / Rabbit LINE Pay
- https://pay-th.line.me/portal/th/about/promotions → "ไม่พบโพสต์" (no posts), as in September and October. **V**.

## 4.3 Pao Tang / ไทยช่วยไทย พลัส (60/40) (เพิ่มเติม)
- Official site (https://www.ไทยช่วยไทยพลัส.th/home via r.jina.ai): use **1 Oct – 30 Nov 69**, 06:00–23:00 face to face (06:00–21:00 for food delivery); right confirmation closed 15 Oct. State pays 60%, ≤ ฿200 a day, ฿1,000 per person for the scheme (October report). **V**.
- **Eligible shops**: non-juristic operators (not franchise convenience stores), non-juristic ธงฟ้า shops, village-fund and community-enterprise shops, non-juristic public-transport operators, mass transit, and small juristic persons with 2567 revenue ≤ ฿1.8M; goods = food, drinks, general goods and public transport; no massage/spa/nail/hair, lottery, alcohol, tobacco, vouchers or cash cards. **V**.
- **Makro, GO Wholesale, Shell and PTT stations: not eligible** (large juristic companies; dealer stations are companies too). Small non-juristic vendors inside a station could be. **R**.
- **No further phase announced** for December on the official site. **V** (as of 1 Nov).

## 4.4 Fuel prices and subsidies
- Excise cut on **E20 (−฿5.60/L) and B20 (−฿5.50/L), 28 Oct 69 – 27 Jan 70**; Bangkok pump prices from 28/29 Oct: E20 ฿33.50 (PTT) / ฿33.70 (Shell), B20 ฿33.50. "เป็นระยะเวลาเบื้องต้น 3 เดือน … โดยมีผลวันที่ 28 ตุลาคม 2569"; the oil fund also cut its compensation, so B20 fell ฿3.69 (from ฿37.19) and E20 ฿2.19 (from ฿35.69) to ฿33.50. **T** (https://www.bangkokbiznews.com/economics/1258170, 27 Oct 69) + **V** (both companies' price lists).

---

# 5. What ends this month / announced for December

**Ends in November**
- Makro **Instant Discount** ฿280 / ฿17,000: **1–4 Nov**.
- Makro PRO collections (Makro Mail 23, Thai Help Thai Plus collection, Diwali, Fresh Explorer…): 10–12 Nov. Seasonal Hamper: 30 Nov.
- **ShopeePay at Makro**: T&C says it ended 31 Oct; tile says 31 Dec — check the app.
- **Shopee 11.11**: collect from 8 Nov, use 10–13 Nov. Payday ≈ 25 Nov (not announced).
- **PTT Smooth Bag stamps**: collect to **30 Nov** (redeem to 15 Dec).
- **blueplus+ Café Amazon 6-cup → KFC mission**: 1–30 Nov.
- **60/40 (เพิ่มเติม)**: **30 Nov**.

**Ended 31 Oct (look for successors)**
- Shell V-Power Club per-litre discounts (Gold ฿0.40 / Champion ฿1 a litre) — no extension published.
- Shell V-Power free Select water (1 Sep – 31 Oct).
- **PTT Self Serve ฿1/L** — no extension posted by 1 Nov (it was extended monthly before; check the blueplus+ app).
- PTT big-vehicle ฿0.60/L (200 L), TOP SECRET cap; Toyota ×3 registration closed (use 5 Nov – 31 Jan).
- Makro referral "(Oct 26)" banner — no November version seen.

**Into December or beyond**
- Makro: Pay Next whole-basket (to 31 Dec), Pay Next 3% round 4 (to 31 Dec), Pay Next Extra 0% 48 months + cashback (to 31 Dec), TrueMoney first payment 50 points (to 31 Dec), new-customer pack (to 30 Dec), **PRO Points expiring must be used by 31 Dec**, Bangkok Bank BNYB (to 28 Feb 70), GSB (to 31 Dec), KTC 13% (to 31 Dec), CardX HY1 (to 31 Dec).
- Shell: biker deals, GO+ sign-up 100 points, café GO+ ฿59 drinks (to 31 Dec); café combo (to 15 Jan 70); café "23rd" (to 30 Sep 70); Shell Plus Package (6 months from purchase).
- PTT: T-shirt for 150 L+ (1 Nov – 31 Dec), blueplus+ wallet ฿100 first payment (to 15 Dec), Blue Day Friday ×2 (to 25 Dec), CardX sign-up points (to 31 Dec), K Point 20% (to 31 Dec), "100 points = ฿20" (to 31 Dec 69).
- **Nothing December-specific announced** yet by Makro, Shopee (12.12), Shell or OR on 1 Nov.

---

# 6. Not found / couldn't read

- **Makro**: Instant Discount's other tiers and channel (app login); referral T&C (login); Makro Club partner perk values (Bangchak, Cockpit); whether **UnionPay QR** is accepted at Makro stores (no Makro page lists payment networks; checkout shows only bank QR/transfer, TrueMoney, card, bill payment); whether ShopeePay's ฿200 code runs in November.
- **Pay Next 3% round 4 availability**: the TrueMoney page header still says "สิทธิ์เต็มแล้ว".
- **Shopee**: 11.11 voucher percentages and minimums, the partner-code hub, November Payday — captcha wall on `shopee.co.th/m/*`. Coins expiry detail sits behind a link in article 80515.
- **ShopeePay / LINE Pay**: no promotion pages with content.
- **Shell / PTT**: see [[fuel-stations]] §4 (GO+ earn rate, blueplus+ fuel earn table, F/S/L meaning, MCC, Self Serve November, station-level QR acceptance).
- TrueMoney's ฿30 first Visa-PromptPay scan offer: not on TrueMoney's own page.

---

# 7. Lineage rows (for `campaigns.md`)

Pages: **M** Makro · **G** GO Wholesale · **S** Shopee · **T** The 1 · **F** Shell · **P** PTT.

| Campaign | Pays | Oct 2026 | Nov 2026 | Pages | predecessor → successor |
|---|---|---|---|---|---|
| Makro PRO partnership hub (`fp/partnership`) | index of bank/wallet tiles | not found in Oct | found; Q4 2026 | M | — |
| Bangkok Bank **BNYB** (Makro PRO tile) | points → 12% (฿800+) / 15% (฿1,500+) / 18% (฿5,000+, top cards); 50,000 pts/month | — | **new, 1 Nov 69 – 28 Feb 70**; SMS `BNYB <16 digits>` to 4712008 | M | — |
| GSB ช้อปซูเปอร์คุ้ม (Makro PRO tile) | ฿40 / 150 / 450 per slip; ฿450/month, ฿5,400 total | running | continues to 31 Dec | M (G?) | — |
| ShopeePay at Makro | ฿200 off ฿3,000 (existing) / 5% off ฿500 (new) | 1–31 Oct (T&C) | tile says to 31 Dec; T&C not updated | M | — |
| Makro Instant Discount | ฿280 off ฿17,000+ (participating items) | — | 1–4 Nov | M | — |
| Makro_THT (TrueMoney ×2 points) | — | ended 30 Sep | no successor | M | ended |
| Pay Next / Extra whole-basket installments (Makro PRO) | up to 48 months, 18–25% p.a. | from 16 Oct | continues to 31 Dec | M | — |
| TrueMoney Pay Next 3% round 4 | 3%, ฿100 a round | started 1 Oct | continues to 31 Dec ("full" banner) | M | round 3 → round 4 |
| Makro referral "ชวนปั๊บ รับพอยท์" | ≤ 30 pts per friend | Oct | no Nov banner | M | ? |
| Makro Club (+ Cockpit perk) | 1% in points; partner perks | running | continues; Cockpit tyre perk added | M | — |
| Shopee 10.10 → **11.11** | platform codes (Xtra up to ฿11,111), ฿11 deals, free shipping | 10.10 (9–12 Oct) | **collect 8 Nov, use 10–13 Nov** | S | 10.10 → 11.11 |
| Shopee Payday | platform codes | not announced | not announced (≈ 25 Nov) | S | — |
| Shell GO+ sign-up | 100 pts (≈ ฿20) | running | to 31 Dec | F | — |
| Shell V-Power Club Gold/Champion | ฿0.40 / ฿1 per litre, ≥ ฿1,000 | to 31 Oct | **ended**, no extension | F | ended |
| Shell biker deals | 5 × V-Power ≥ ฿100 → 100 pts | running | to 31 Dec | F | — |
| Shell Plus Package (Shopee/Lazada/TikTok) | prepaid discount pack ฿299/599/1,699 | from 23 Sep | on sale | F S | — |
| Shell V-Power free water | ≤ 4 bottles / ฿500 | 1 Sep – 31 Oct | ended | F | ended |
| Shell Café 23rd / GO+ ฿59 / combo | drink deals | from 1 / 15 Oct | continue | F | — |
| PTT Self Serve ฿1/L | ฿1 a litre, no minimum | extended to 31 Oct | **no Nov extension posted** | P | ? |
| PTT Smooth Bag stamps | 5 × ฿1,000 standard fuel → bag | 1 Oct – 30 Nov | continues (redeem to 15 Dec) | P | — |
| PTT big vehicles: 200 L → ฿0.60/L · 150 L → T-shirt | per receipt | ฿0.60/L 20 Sep – 31 Oct | T-shirt 1 Nov – 31 Dec | P | ฿0.60/L → T-shirt |
| blueplus+ wallet first payment | ฿100 back on ≥ ฿300 | from 15 Oct | to 15 Dec | P | — |
| blueplus+ Blue Day Friday ×2 | 2× points (terms not read) | running | to 25 Dec | P | — |
| blueplus+ Café Amazon 6 cups → KFC | coupon | — | 1–30 Nov | P | — |
| KBank K Point → 20% at OR shops | points redemption | running | to 31 Dec | P | — |
| ไทยช่วยไทยพลัส 60/40 (เพิ่มเติม) | 60% state share | 1 Oct – 30 Nov | ends 30 Nov | M G F P (none eligible) | → nothing announced |
| E20/B20 excise cut | −฿5.60 / −฿5.50 a litre | from 28 Oct | to 27 Jan 70 | F P | — |

---

# 8. New site tricks (for `research-methods.md`)

- **makro.pro's homepage banners now live in the dehydrated React Query state**: `props.pageProps.dehydratedState.queries[0].state.data.flexiPage.components[*].data`; the `_flexiPage` copy has `data: null` for `TOP_BANNERS` / `IN_BETWEEN_BANNERS` / `MARKETING_CAROUSEL`. Static T&C pages (`/th/static/<handle>`) carry their HTML in `props.pageProps.cmsData.attributes.description`. The bank hub is `/th/fp/partnership`.
- **shell.co.th is Adobe AEM: append `.model.json`** to any page path (`/th_th/customer/<path>.model.json`) for the full content as JSON; `/th_th/customer/_jcr_content/root/header/inherited_copy.model.json` lists every page (133 links). Fuel prices are an **XLSX** linked from the fuel-price page model (`…/fuel-price-update-thailand.xlsx`, history `…/thailand-data-historic.xlsx`); read with `openpyxl`. The help-centre FAQ is a JS widget that doesn't render headless.
- **OR (PTT) fuel prices**: SOAP `POST https://orapiweb.pttor.com/oilservice/OilPrice.asmx` with `SOAPAction: "http://www.pttor.com/CurrentOilPrice"` (body `<CurrentOilPrice xmlns="http://www.pttor.com"><Language>th</Language></CurrentOilPrice>`) for Bangkok, and `GetOilPriceProvincial` (`<Language>th</Language><DD>1</DD><MM>11</MM><YYYY>2026</YYYY><Province>เชียงใหม่</Province>`) for each district of a province. pttor.com's `/wp-json/` returns a maintenance page; the HTML listing `https://www.pttor.com/th/promotion` (and each `/promotion/<slug>`) is plain curl.
- **blueplus.com** (Next.js, client-rendered): r.jina.ai reads `/benefit/point/list` (earn rates), `/faqs`, `/news-and-promotion/promotion/list` (titles and dates); the detail pages need an id the listing doesn't expose.
- **App Store lookup JSON** (`itunes.apple.com/lookup?id=959841453&country=th`) gives Shopee's campaign text (`description`) and screenshot URLs; swap `392x696bb` for `780x1688bb` for readable screenshots. The **Shell Asia** listing (id1539429518) says in-app fuel payment is Malaysia/Singapore only.
- **Wikimedia**: the Shell pecten is an English-Wikipedia local file (`File:Shell logo.svg`, not on Commons); `upload.wikimedia.org` thumbnails only come in standard widths (`960px-` works, `800px-` returns 400). No 429 on 1 Nov.
- **The household's ledgers settle "does the station take this card"**: `fetch-transactions` with `name_contains: "SHELL"` / `"PTT"` and the rows' `card_ids` (KTC UnionPay at Shell CO stations, 7 slips).
