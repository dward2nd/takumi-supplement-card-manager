---
tags: [catalogue-research, 2026-10]
researched: 2026-10-06
---

> **Research snapshot**: bank, card-network and wallet campaigns for a slip at **Jampha Savemart** (แจ่มฟ้า เซฟมาร์ท, statement name `JAMPHA SAVEMART CO.,LTD. CHIANGMAI TH`), October 2026 and anything announced for November. Scope: every issuer's campaign that a local supermarket slip (MCC 5411) *could* count toward: category campaigns by MCC, named-chain campaigns (to rule them out), channel rules, spend-threshold and all-spend ladders, and the campaigns that name Jampha itself. The store (branches, payment methods, own promotions) and base earning are in the companion reports. Read on **2026-10-06** from the official pages, for the October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions (HTML, JSON) stayed in that session's scratchpad (`/tmp/jbanks/`) and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# Jampha Savemart — bank and network campaigns, October 2026

**Confidence labels**:
- **verified**: the official page was read on 2026-10-06.
- **verified (earlier)**: read on the official page by an earlier October report (date given), not re-read today.
- **third-party only**: the only source is not the issuer or the merchant.
- **unverified**: an inference, or the household's own ledger evidence.

**How the household pays at Jampha** (user, 2026-10-06, first-hand): the only credit-card QR Jampha accepts is **UnionPay QR**. No issuer's in-app credit-card QR works there (Krungsri UCHOOSE, KTC Mobile Visa QR, UOB TMRW, K PLUS Scan to Pay, AEON Scan To Pay). Besides that, it takes **PromptPay** from bank accounts. A **physical card** (tap or insert) carries a **2% processing fee**. So every card campaign below pays at Jampha only:
- through a **physical card**, net of the 2% fee; or
- for a **UnionPay card**, through **UnionPay QR**, with no fee.

The household's UnionPay cards are **KTC UnionPay** (Takumi's …1346, which also carries Baiboon's `[บัตรหลัก]` rows; Baiboon's own …2310; Nuta has one too, not registered for the QR offer) and **AEON UnionPay** (Takumi's; Nuta uses it). None of Baiboon's other cards is UnionPay.

---

## 0. The answer

### 0.1 What pays at Jampha, ranked

Values are what the household gets back **after the 2% fee**, for one ฿10,000 slip and for ฿30,000 in a month. "Fee" is 2% of the card slip; UnionPay QR has none. Base points are left out (see the base-earning report).

| # | Campaign | Card · channel | ฿10,000 slip | ฿30,000 / month | Caps | Registration | Confidence |
|---|---|---|---|---|---|---|---|
| 1 | **AEON × Jampha "ช้อปปุ๊บ รับปั๊บ"**: a gift for a day's spend at Jampha, Lamphun branches only (§2.3) | any AEON credit card · physical card (UnionPay QR on AEON UnionPay: unclear) | ≥ ฿4,500 in a day → Anello backpack (list ฿2,490) − ฿200 fee; or, at ≥ ฿1,200, a tumbler (฿299) − ฿24 on a ฿1,200 slip | one gift per card per day, so several visit days × AEON cards | 1 per card number per day; **120 backpacks and 900 tumblers for the whole campaign** | claim at the AEON counter in **Big C Lamphun** the same day, with the slip | verified (terms) · **unclear whether Baiboon's branch is one of the three** |
| 2 | **UnionPay QR "Get 6% off"** (§3.1) | KTC UnionPay · UnionPay QR in KTC Mobile | **฿60** (0.6%), no fee | ฿60 per card per visit day; at most ฿300 per card (…1346 and …2310 each) | 1 discounted slip per card per day, ฿300 per card per month; UnionPay's pool: **34% left at 18:47 on 6 Oct** | each card registered for October on UnionPay's page | verified (API) |
| 3 | **Krungsri HALO** (§4.1.3) | Krungsri VISA · physical card | ฿255 Bar B Q Plaza voucher − ฿200 fee = **+฿55**; only a ≥ ฿500 Jampha slip is needed (fee ฿10) | same ฿255: one a month | 1 voucher per primary account a month, **2 for the whole campaign (Aug–Oct)**; first 4,500 accounts in October | registered (all Krungsri campaigns) | verified |
| 4 | **KBank HYP** (§4.5.1) | KBank JCB, KBank PLUSTINUM · physical card | ฿75 − ฿200 = **−฿125** | ฿700 − ฿600 = **+฿100** (฿50,000 → +฿250) | ฿1,250 a month, ฿5,000 for the campaign | once, by **31 Oct**; not on the household's list | verified |
| 5 | **First Choice NW4** (§4.1.2) | First Choice · physical card | ฿200 − ฿200 = **฿0** | ฿600 − ฿600 = **฿0**, only while the ฿30,000 monthly supermarket allowance is unused | supermarket spend counts to ฿30,000 a month per primary account, **shared with Makro PRO, Tops, Big C …** | auto-enrolled | verified |
| 6 | KBank PLUSTINUM Season 3 + monthly e-coupon (§4.5.3) | KBank PLUSTINUM · physical card | ≥ ฿10,000 → ฿200 coupon − ฿200 = **฿0** | ≥ ฿30,000 → Starbucks ฿400 + ฿200 coupon − ฿600 = **฿0** | 1 a month | **re-register for October**; status unknown | verified |
| — | **Points cash-outs**: KTC `JFM` (names Jampha, §2.1), KBank `BCB`, Krungsri PT26 | KTC (incl. KTC UnionPay by QR, reading) · KBank · Krungsri, physical card | points equal to the slip → 10% back, or ฿0.10 a point | no cap (JFM, BCB) | — | JFM and BCB every slip; PT26 in UCHOOSE | verified |
| — | Lucky draws: JCB Japan Season 3, BTS draw, KBank Visa × Maroon 5 (§3.3, §4.1.2, §4.5.4) | JCB / Visa · physical card | one draw right a slip (≥ ฿1,000 or ≥ ฿1,500) for ฿200 of fees | — | — | registered (Krungsri `JCLD`, BTS); KBank JCB and Maroon 5 in K PLUS | verified |

What this means:
- **UnionPay QR on KTC UnionPay stays the default.** It's the only way to pay with a card without the fee. KTC UnionPay earns no points at MCC 5411, so anything past the 6% earns nothing.
- **Spread the discounted slips over both cards.** The 6% applies to **one slip per card per day**. Baiboon already splits a visit into 2–4 slips, so the first slip ≥ ฿1,000 on …2310 and the first on …1346 each take ฿60, and the rest take nothing. On 1 Oct 2026 her ledger has two Jampha slips (฿14,875 and ฿14,815) on the same card (…2310, neither is `[บัตรหลัก]`), so at most one of them was discounted. **unverified** (ledger reading).
- **October's UnionPay pool is going fast.** It read 34.26% left at 18:47 on 6 Oct. September's ran out on 12 Sep. Use it in the next few days; November's offer (`260723112621`) opens on 1 Nov.
- **The gift campaign is the one big item**, if Baiboon's Jampha is one of the three Lamphun branches and stock is left (it started 15 Aug). The gift is in kind, and AEON puts the backpack at ฿2,490.
- **A physical card only pays when the campaign beats 2%.** Only HYP at ฿30,000 or more a month does, plus HALO's ฿255 if a small slip covers the supermarket leg. NW4 and PLUSTINUM only break even.
- **The points cash-outs** (KTC `JFM`, KBank `BCB`, Krungsri PT26) value a point at ฿0.10, which is par for KTC points (1,000 = ฿100, [[../../promotions/ktc-forever|KTC FOREVER]]). They turn points into cash at Jampha but add nothing. Paid through UnionPay QR on KTC UnionPay, `JFM` would stack with the 6% (reading).

### 0.2 Notable "doesn't qualify"

Every big supermarket campaign this quarter is a **named-chain list with no catch-all**. Jampha is on none of these lists:
- **Krungsri SUP1/SUP2**: Big C, Makro by UCHOOSE scan only, Makro PRO, Tops, Gourmet, GO.
- **KTC 13% supermarket**: Big C, Donki, GO, Golden Place, Lotus's, Makro, Mitsukoshi, UFM.
- **AEON World 5% and NTW1**: both list their supermarkets.
- **UOB SPW592**: it states MCC 5411/5499, but only at the named stores, and Rimping is the one Chiang Mai name.
- **UOB Premier PRS**, **CardX HY1, SU1/SU2 and PAYDAY**, **ttb SPM and BGO**, **Bangkok Bank BSUP**, **GSB "ช้อปซูเปอร์คุ้ม"**, **Central The 1 TOPS4 and GWS3**.

Two other groups miss for other reasons:
- **Lotus's** SMP1, SMT2, LBS3, LAN and QRT4 and the invited Q4 segments all exclude supermarkets, or pay only at Lotus's. UOB Makro's Gold Mission excludes MCC 5411.
- **The channel campaigns** can't be used at Jampha:
  - Krungsri NOW 5% is online only.
  - ONQ3, UOB SPW796 and QRT4's wallet leg need a wallet payment.
  - KTC VISA Scan to Pay needs the KTC Mobile Visa QR.
  - AEON Next Gen's Scan To Pay qualifier needs AEON's own QR.
  - UnionPay's 3% NFC offer has an empty pool, and a tap would carry the fee anyway.

---

## 1. The store and how its slips look to a bank

- **Jampha Savemart is a regional chain, not one shop.** The company register lists **25 branches, 18 in Chiang Mai and 7 in Lamphun**, with the head office at 166/1 ถนนอินทยงยศ, อำเภอเมืองลำพูน. Source: dataforthai.com's branch list (`company-branch/0515552000264`), read by the store researcher on 2026-10-06. **third-party only**. The store report has the details. The point here is that "ทุกสาขา" (KTC) and a Lamphun-only list (AEON) are different things.
- **MCC 5411.** The household treats it as a supermarket. KTC UnionPay pays no points on it (KTC rule 16, MCC 5411), and every row since July carries `×0` with the Note "Supermarket — KTC UnionPay earns no points on supermarket purchases." **unverified** (household evidence, not a statement MCC).
- **The 2% fee seems to sit inside the card charge.** Two of Baiboon's First Choice slips on 5 Jul 2026 were **฿6,120 each**, which is ฿6,000 + 2%. So a campaign sees the fee-inclusive amount and counts it as spend: the fee isn't a separate bank fee, which campaigns exclude. **unverified** (ledger reading).
- **Splitting slips.** Baiboon's visits run ฿8,000–30,000, often split into 2–4 slips the same day. Three campaigns care:
  - **Per-slip campaigns** (none qualify here) lose by it.
  - **Monthly ladders** (HYP, NW4) don't care.
  - **KTC's `JFM`** says the spend can't be split into several slips "to get the right" (`ไม่สามารถแยกยอดใช้จ่ายเป็นหลายเซลส์สลิปเพื่อรับสิทธิ์`). It has no cap, so splitting gains nothing there anyway.
  - **The UnionPay QR offer gives one discounted slip per card per day**, so splitting only helps across cards.
- **PromptPay through TrueMoney** (the `TMN*PROMPTPAY…` rows in the ledgers) would turn a Jampha payment into a TrueMoney transaction. The slip would lose MCC 5411 and could only count toward wallet campaigns (ONQ3, SPW796). Whether TrueMoney lets a linked credit card pay a merchant's PromptPay QR, at what fee, and whether those campaigns count it, wasn't researched. **unverified**.

---

## 2. Campaigns that name Jampha

### 2.1 KTC `JFM` — "โปรโมชั่นที่ แจ่มฟ้า เซฟมาร์ท กับบัตรเครดิต KTC" · **qualifies** · verified

- **Pays**: redeem **KTC FOREVER points equal to the slip** (satang rounded up) for a **10% credit**, which is ฿0.10 a point.
- **Where**: `แจ่มฟ้า เซฟมาร์ท ทุกสาขา` (every branch).
- **Cards**: every KTC credit card except ROYAL ORCHID PLUS, CASH BACK, the blood-centre card, VISA CORPORATE and government cards. **KTC UnionPay isn't excluded.**
- **Registration**: every slip, **on the same day**:
  - SMS `JFM <16-digit card number>` → 0613845000, or the form at `ktc.promo/jamphasavemart`.
  - The page's note says to enter the amount with its decimals (e.g. 4500.50), which suggests the form asks for the amount.
  - KTC's confirmation reply is required.
- **Caps**: "ไม่จำกัดยอดแลกคะแนน" (no limit). Each registered card is counted on its own.
- **Period**: 1 Mar – 31 Dec 2026. Credited within 60 days after each calendar month; full-amount slips only.
- **Jampha verdict: qualifies.** It's a cash-out at par, not a bonus: KTC values a point at ฿0.10 anyway, and its supermarket and department-store burns elsewhere run 13–18%.
- **UnionPay QR**: whether a payment by KTC UnionPay through UnionPay QR counts isn't stated. It posts as a card charge at Jampha, so it probably does. **unverified** (reading).
  - If it counts, it stacks with the 6%, since UnionPay's "one promotion per payment" covers UnionPay's own offers. Points would equal the net (discounted) slip.
- **Net of the fee**: through UnionPay QR, no fee (reading). Through a physical KTC card, −2%, so it gives 8% back for 10% of the slip in points.
- Source: https://www.ktc.co.th/promotion/shopping/department-stores-shopping-complexes/jampha-savemart (sitemap `lastmod` 29 Apr 2026).

### 2.2 KTC — "โปรโมชั่นที่ ห้างแจ่มฟ้าช้อปปิ้งมอลล์ จ.ลำพูน" · **qualifies only at the Lamphun mall** · verified

- **Pays**: a **10% discount** when you use KTC FOREVER points equal to the slip ("แลกรับส่วนลดเพิ่ม 10%"), every day, with no cap.
- **Registration**: none ("รับสิทธิ์ได้ไม่ต้องลงทะเบียน").
- **Where**: `ห้างแจ่มฟ้าช้อปปิ้งมอลล์ จ.ลำพูน` only.
- **Exclusions**: gift cards, alcohol, medicine and tenant shops; split slips don't earn extra rights.
- **Period**: 1 Mar – 31 Dec 2026.
- **Jampha verdict**: it applies at the Lamphun shopping mall, not at the Savemart branches. Like 2.1, it values a point at par.
- Source: https://www.ktc.co.th/promotion/shopping/department-stores-shopping-complexes/jampha

### 2.3 AEON — "ช้อปปุ๊บ รับปั๊บ กับบัตรเครดิตอิออน" (Jampha) · **qualifies at three Lamphun locations** · verified

- **Pays, per card number per day** (spend adds up over the day):

  | Day's spend at Jampha | Gift | Limit |
  |---|---|---|
  | ≥ ฿1,200 | Eco-Friendly Tumbler 400 ml (list value ฿299) | 1 per card number per day; **900 for the whole campaign** |
  | ≥ ฿4,500 | Anello Regular Backpack (list value ฿2,490) | 1 per card number per day; **120 for the whole campaign** |

  The terms don't say whether a ≥ ฿4,500 day also gets the tumbler.
- **Where**: `ร้านแจ่มฟ้า สาขาที่ร่วมรายการ (เฉพาะหน้าสาขาเท่านั้น)`, in store only:
  - `ศูนย์การค้าแจ่มฟ้าช้อปปิ้งมอลล์และแจ่มฟ้าเซฟมาร์ท ลำพูน สาขาจตุจักร`
  - `แจ่มฟ้าเซฟมาร์ท สาขานิคมอุตสาหกรรมลำพูน`
  - `แจ่มฟ้าเซฟมาร์ท สาขาลำพูน`
- **Cards**: every AEON credit card except corporate cards. Full amount only; **not through an e-wallet**.
- **Excluded**: refunds, top-up cards, cash coupons, vouchers, gift cards and part deposits.
- **How to claim**: show the slip at **AEON's counter in Big C Lamphun** ("ลงทะเบียน ณ อิออน สาขาบิ๊กซีลำพูน") **on the day of purchase**. Gifts go while stock lasts.
- **Period**: 15 Aug – 31 Oct 2026.
- **Jampha verdict**: it **qualifies if Baiboon shops at one of the three Lamphun locations**. The statement name says `CHIANGMAI`, which may just be the terminal's city, and the chain has 18 Chiang Mai branches, so **which branch she uses decides it**. The campaign ran seven weeks before this research, so backpack stock may be gone.
- **Household cards**: AEON World Mastercard (Takumi's primary, which Baiboon spends on as `[บัตรหลัก]`), AEON Next Gen, AEON Primo and AEON UnionPay.
  - **Physical card**: −2% fee.
  - **AEON UnionPay through UnionPay QR**: no fee, but whether AEON counts a QR slip as "ชำระเต็มจำนวน" card spend (it isn't an e-wallet), and whether AEON's app can make a UnionPay QR payment at all, are both **unverified**.
- **Net of the fee**: a ฿1,200 slip costs ฿24 for a ฿299 tumbler; a ฿4,500 slip costs ฿90 for a ฿2,490 backpack.
- Source: https://www.aeon.co.th/aeon/promotions/shop-get-2026/ (the page also lists the Chaisang/Ekkaphap edition, `shop-get-chaisang-2026`, for other provinces).

### 2.4 Nobody else names Jampha

Checked on 6 Oct, with no hit:
- the promotion indexes: Krungsri's listing JSON (518 items), UOB's `data-promotion.json` (632), CardX's search index (1,000), centralthe1card.com (175), the KBank campaign list (217, dump of 5 Oct), and ttb's shopping listing;
- the sitemaps of First Choice, Lotus's and GSB;
- a Thai web search.

KTC also runs a regional local-supermarket list (`supermarket-upc`, SMS `RSM`, 1 May 2026 – 28 Feb 2027: points → 10% at Big One Chumphon, Chaisang Singburi, Saengthong Rayong and Wan Rayong). Jampha isn't on it.

---

## 3. Card networks

### 3.1 UnionPay QR "Get 6% off" · **qualifies** · verified

- **Pays**: 6% off, at most **฿60 a slip** (reached at ฿1,000).
- **Limits**: **1 discounted slip per card per day**, **฿300 per card per month**. UnionPay's pool is 12,000 discounts a month nationwide, first come first served.
- **Cards**: paid through KTC Mobile (or the ICBC and BOC TH apps); the household uses KTC UnionPay.
- **Registration**: each card, each month, on UnionPay's page.
- **Pool status** (`lib.bureau.unionpay_offer`, 6 Oct 18:47 Bangkok):

  | Month | Offer | State |
  |---|---|---|
  | October | `260723112620` | **live, 34.26% left** |
  | November | `260723112621` | not started |
  | December | `260723112622` | not started |

  September's pool ran out on 12 Sep. At October's pace (about 66% used in six days), October's may run out around 9–10 Oct. That's an estimate.
- **The discount is inside the charge**: the ledger row is the net amount ([[../../promotions/unionpay-qr|UnionPay QR]]).
- **The ฿300 per card is shared** with every other UnionPay QR slip that month (fuel, CMEx, restaurants).
- **Jampha verdict: qualifies.** Jampha takes UnionPay QR, and the household's September rows on both cards are discounted Jampha slips (฿1,604 on …1346 and ฿5,913 on …2310, both 6 Sep).
- **Net**: no fee. KTC UnionPay earns no points at MCC 5411.
- Tracked: `unionpay_qr.py` in the [[../../concepts/promotion-bureau|Promotion Bureau]], per card number.
- Source: UnionPay's offer API (`marketing.unionpayintl.com/h5Promote/v1/coupon/flushProcess`, offer 260723112620); terms in [[../../promotions/unionpay-qr]].

### 3.2 UnionPay "Mobile Payment Instant Discount 3% OFF" (NFC, `260226111820`) · **doesn't pay** · verified

- **Terms**: a UnionPay card in a phone wallet, tapped in store; 3% off, at most ฿100 a transaction, ฿600 a month.
- **Pool**: the API read **`percent` 0.0** on 6 Oct, so it's empty or not yet reset.
- **At Jampha**: a tap is a card payment, so the 2% fee would apply. Whether KTC UnionPay can be added to a phone wallet is unverified.

UnionPay's Thai offer list on 6 Oct (17 offers) has nothing else for supermarkets.

### 3.3 JCB "ลุ้นเปย์ไป JAPAN Season 3" · **qualifies (draw rights only)** · verified

- **Pays**: one draw right for each slip of **≥ ฿1,000** at any merchant, in Thailand or abroad; 1 Oct 2026 – 31 Jan 2027. The prizes are three Japan tours.
- **Registration**:
  - **Krungsri JCB**: register `JCLD` in UCHOOSE once (registered: all Krungsri campaigns).
  - **KBank JCB** (Baiboon's): register in K PLUS.
- **Net**: a physical card costs 2%, so ฿20 or more per right. Not worth paying the fee for a draw.
- Sources:
  - Krungsri: https://www.krungsricard.com/th/promotion/jcb-go-japan-season3
  - KBank: https://www.kasikornbank.com/th/promotion/creditcard/pages/jcb-luckydraw.aspx
  - JCB's list: `specialoffers.jcb/…/thailand/ajax.json`, item 95599.

### 3.4 Visa and Mastercard

- **No supermarket offer that names no merchant** was found. Read 1 Oct by [[ktc-aeon-other-banks-networks]]: the Visa offers are travel and luxury; Mastercard Friday and Visa × Central Retail are Central Retail only. **verified (earlier)**
- Not re-read on 6 Oct.

---

## 4. By issuer

Each entry: code · cards · mechanic and tiers · caps · period · registration · channel · **Jampha verdict** · **net of the 2% fee** · source · confidence.

### 4.1 Krungsri group

#### 4.1.1 Krungsri Card

| Campaign | Cards · mechanic | Caps · period · registration | Jampha verdict | Net of the fee | Source · confidence |
|---|---|---|---|---|---|
| **SUP1** "ช้อปซูเปอร์มาร์ชั้นนำ รับเครดิตเงินคืนสูงสุด 3%" | all Krungsri cards; per slip ฿1,500–3,999 → ฿35, ≥ ฿4,000 → ฿120 | ฿120 per primary account a month; 1 Aug – **31 Oct**; registered | **doesn't**: `ซูเปอร์มาร์เก็ตที่ร่วมรายการ … ได้แก่` Big C (all formats, bigc.co.th), Makro (UCHOOSE scan only), Makro Pro, Tops, Gourmet Market, Go Wholesale; no catch-all | — | https://www.krungsricard.com/th/promotion/supermarket-shopping · verified |
| **SUP2** | ฿700 at ฿60,000 a month at the same stores | first 1,200 a month; not registered; to 31 Oct | **doesn't**: same named list | — | same · verified |
| **HALO** | see 4.1.3 | | **qualifies** | | |
| **JSU** "Supermarket รับเครดิตเงินคืนคุ้มสูงสุด 10%" | Krungsri JCB; ฿100 per slip ≥ ฿1,000 | ฿100 a day, ฿200 a month, ฿600 for the campaign (+฿100 for every month); 1 Aug – 31 Oct; registered | **doesn't**: UFM Fuji Super, Mitsukoshi Depachika, TAKA Marche, Tops (all formats), Gourmet Market, Villa Market, Foodland | — | https://www.krungsricard.com/th/promotion/supermarket-jcb · verified |
| **2× points** (Krungsri Platinum) | double Krungsri points at listed department stores and supermarkets | 120 extra points a month at supermarkets; 1 Jul – 31 Dec | **doesn't**: `ซูเปอร์มาร์เก็ตที่ร่วมรายการ ได้แก่ Big C, Lotus’s, Tops และ Gourmet Market` | — | https://www.krungsricard.com/th/promotion/2x-platinum · verified |
| **PT26** "พอยต์คืนคุ้ม" | Krungsri points → cashback at ฿0.10 (500 → ฿50 … 5,000 → ฿500) for spend at the listed MCCs, which include 5411 and 5499; redeem in UCHOOSE within the month of the spend | ≤ 500,000 points a day; primary cards only; 1 Jan – 31 Dec 2026 | **qualifies**: MCC-based, no store list | a cash-out at par; the slip itself is −2% on a physical card | https://www.krungsricard.com/th/promotion/point-cashback · verified (MCC list read 1 Oct) |
| **JCLD** (JCB Japan Season 3) | see 3.3 | | **qualifies** (draw) | −2% per right | verified |
| **BTS draw** (Krungsri VISA pool) | 1 right per Visa slip ≥ ฿1,500 | 10 rights a month per company; round 3 counts 1 Oct – 15 Nov; registered | **qualifies** (draw) | −2% per right | [[../../promotions/first-choice-2026h2]] · verified (earlier) |
| **ONQ3** | online and wallet ladder ฿40 / ฿170 / ฿350 | to 30 Nov; registered | **doesn't**: only Lazada, Shopee, TikTok Shop, LINE SHOPPING and card payments through TrueMoney, LINE Pay or ShopeePay; Jampha takes no wallet (§1, PromptPay route unverified) | — | [[krungsri-group]] §3.3 · verified (earlier, 1 Oct) |
| **NOW 5% online** | ฿25 per ฿500 online slip | standing | **doesn't**: online only; QR excluded | — | [[krungsri-group]] §1.2 · verified (earlier) |

No new Krungsri supermarket campaign starts in October or November; the listing JSON was read on 6 Oct. SUP1, SUP2, JSU and HALO all end on 31 Oct, and no successor is published yet.

#### 4.1.2 First Choice

**NW4 "รูดก็ได้เงินคืน กดก็ได้แคชเบ็ค"** · **qualifies (supermarket allowance)** · verified
- **Cards**: First Choice Visa Platinum. Takumi's primary and Baiboon's and Nuta's supplements pool on one primary account.
- **Pays, per calendar month of full-amount spend**: ฿5,000–9,999 → ฿50; ฿200 per whole ฿10,000; ฿2,000 at most a month, ฿6,000 for the campaign.
- **The supermarket allowance**: `ยอดการใช้จ่ายสะสมในหมวดซูเปอร์มาร์เก็ต เช่น บิ๊กซี, โลตัส, ท็อปส์ …` counts only up to **฿30,000 a month per primary account**.
  - The stores are examples (`เช่น`) of a category, so Jampha falls inside the allowance.
  - It's **shared** with Makro PRO (`HTTPS://WWW.MAKRO.PRO/`, 5411), Tops, Big C and GO on the same account.
  - Spend over ฿30,000 is ignored; spend up to it counts normally.
- **Exclusions**: e-wallet top-ups, not wallet payments. The rebate counts spend after discounts.
- **Period and registration**: 1 Oct – 31 Dec 2026; NW4, auto-enrolled.
- **Channel**: a physical card only at Jampha.
- **Jampha verdict: qualifies.**
- **Net of the fee: about 0.** ฿10,000 → ฿200 rebate − ฿200 fee. Once the month's ฿30,000 supermarket allowance is used up, −2%.
  - NW3's old rule that dropped supermarket slips over ฿10,000 is gone. That rule is why Baiboon's July First Choice slips were ≤ ฿6,120.
- Source: https://www.firstchoice.co.th/promotion/credit-card-supermarket (and `/promotion/firstchoice-cashback`). Tracked: `nw4.py`; its supermarket matcher (`_SUPERMARKET`) doesn't list `SAVEMART`, so a First Choice Jampha slip would be counted without the ฿30,000 cap until it's added.

**BTS draw (First Choice pool)**: one right per Visa slip of ≥ ฿1,500 (10 a month); round 3 counts 1 Oct – 15 Nov. **qualifies** (draw), −2% per right. verified (earlier)

**ON4 / DLV3 / IS4 / TR3**: these cover marketplaces, delivery, insurance and travel. **doesn't**

#### 4.1.3 Krungsri HALO — "ปรับใหม่ง่ายขึ้น 2 เดือนเท่านั้น ใช้ครบ 3 หมวด" · **qualifies** · verified

- **Cards**: Krungsri VISA only (Visa network). The household has Takumi's primary and Baiboon's supplement.
- **Pays**: spend ≥ **฿6,000 in a month across all three of dining, supermarket and fuel**, counting only slips ≥ ฿500 and with each category used, → a **Bar B Q Plaza e-voucher worth ฿255**.
- **The supermarket category is by MCC**: `หมวดซูเปอร์มาร์เก็ต คือ ร้านค้าที่จดทะเบียน ภายใต้ MCC 5411,5499,5422,5441,5451,5921,5333`. Makro and Grab are excluded.
- **Caps**: 1 voucher per primary account a month, **2 for the whole campaign** (1 Aug – 31 Oct); first 4,500 accounts in October.
- **Period and registration**: September and October rounds (1 Sep – 31 Oct); `HALO` in UCHOOSE once. Registrations from 1 Aug carry over.
- **Crediting**: vouchers arrive in UCHOOSE within 90 days of the campaign's end, usable to 15 May 2027.
- **Stacking**: "สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่น ๆ ได้" (can be combined).
- **Jampha verdict: qualifies**, as the supermarket leg.
- **Net of the fee**:
  - The supermarket leg needs only one ≥ ฿500 slip: ฿10 of fee for a ฿255 voucher, once the dining and fuel legs and the ฿6,000 total are met.
  - A ฿10,000 Jampha slip gives ฿255 − ฿200 = +฿55.
  - Any other supermarket without a fee meets the leg as well.
  - Whether the household's two vouchers were already used in August and September isn't recorded.
- Source: https://www.krungsricard.com/th/promotion/visa-everyday-spend

#### 4.1.4 Central The 1 card (Baiboon's REDZ supplement)

| Campaign | Jampha verdict | Source · confidence |
|---|---|---|
| TOPS4, GWS3, Extra Point Day, T1 MAGICAL DAY | **doesn't**: Central Retail stores, Tops or GO only | centralthe1card.com `gcspromotion`, 175 items, 6 Oct · verified |
| any supermarket or all-spend cashback | none published | same · verified |

#### 4.1.5 Lotus's (Lotus's Beyond)

| Campaign | Mechanic | Jampha verdict | Source · confidence |
|---|---|---|---|
| **SMP1 / SMT2** | ladder ฿70 per ฿3,500 …; ฿200 at ฿2,000 in October | **doesn't**: excludes `ทุกซูเปอร์มาร์เก็ต ไฮเปอร์มาร์เก็ต และร้านสะดวกซื้อ` | [[../../promotions/lotuss-smp1]] · verified (earlier, 5 Oct) |
| **LBS3** | big-ticket ladder | **doesn't**: excludes other supermarkets (Makro excepted) | [[../../promotions/lotuss-lbs3]] · verified (earlier) |
| **LAN** | at Lotus's only | **doesn't** | [[../../promotions/lotuss-lan]] |
| **QRT4** | 10% (≤ ฿10) per ฿100 slip in fashion, department stores, private hospitals, restaurants and home, by Tap & Go, UCHOOSE QR or TrueMoney | **doesn't**: supermarkets aren't among the five categories, and Jampha takes neither channel | [[../../promotions/lotuss-qrt4]] · verified (earlier) |
| invited Q4 segments (`small-ticket-a/b-q4-26` …) | per-slip and monthly ladders | **doesn't**: exclude hyper- and supermarkets | [[ticketing-krungsri-ktc-aeon]] · verified (earlier) |

### 4.2 KTC

| Campaign | Cards · mechanic | Caps · period · registration | Jampha verdict | Net of the fee | Source · confidence |
|---|---|---|---|---|---|
| **`JFM`** Jampha Savemart | see 2.1 | | **qualifies** | cash-out at par; no fee by QR (reading) | verified |
| Jampha Shopping Mall (Lamphun) | see 2.2 | | mall only | | verified |
| **"ช้อปซูเปอร์ คุ้มเวอร์ยกบ้าน"** (MKTHM-0549) | points = slip → **13%** | 30,000 points per cardholder a month; 1 Aug – 31 Dec; register every slip at `ktc.promo/supermarket2026` | **doesn't**: `สาขาที่ร่วมรายการ` in store are Big C (+mini, Food Service), Donki, Go Wholesale, Golden Place, Lotus's (Prive, go fresh), Makro (KTC Mobile scan or TrueMoney only), Mitsukoshi Depachika, UFM Fuji Super; online Big C, Freshket, GO, Lotus's, Makro PRO; no catch-all | — | https://www.ktc.co.th/promotion/shopping/supermarkets-convenience-stores/supermarket · verified |
| **KTC VISA Scan to Pay** (MKTHM-0653) | 3 slips ≥ ฿1,000 a month → ฿150 | ฿750 for the campaign; 1 Aug – 31 Dec; no registration | **doesn't**: named (Big C, Foodland, Go Wholesale, Gourmet, Lotus's, MaxValu, Rimping, Tops), and it needs the KTC Mobile Visa QR, which Jampha doesn't take | — | …/supermarket-scan-to-pay · verified |
| regional supermarkets 10% (`RSM`) | points = slip → 10% | 1 May 2026 – 28 Feb 2027 | **doesn't**: Chumphon, Singburi and Rayong stores only | — | …/supermarket-upc · verified |
| points → 0% × 3 at supermarkets (`FCS`) | points worth 20% of a ≥ ฿1,500 slip → 0% × 3 | 16 Feb 2026 – 31 Jan 2027 | **doesn't**: Big C, Foodland, GO, Lotus's, Makro PRO | — | …/supermarket-point-installment · verified |
| KTC JCB ×4 (Donki, UFM, Villa) | — | 10 Aug – 31 Dec | **doesn't** | — | …/jcbx4 · verified |
| **UnionPay QR 6%** | see 3.1 | | **qualifies** | no fee | verified |
| base points | KTC UnionPay: **none at MCC 5411** (rule 16); KTC Visa, Mastercard and JCB earn normally | | (base earning) | | [[../../promotions/ktc-forever]] |

### 4.3 AEON

| Campaign | Cards · mechanic | Caps · period · registration | Jampha verdict | Net of the fee | Source · confidence |
|---|---|---|---|---|---|
| **"ช้อปปุ๊บ รับปั๊บ"** at Jampha | see 2.3 | | **qualifies at the three Lamphun locations** | gift worth ฿299 / ฿2,490 for 2% of the slip | verified |
| **AEON World Mastercard 5%** (card benefit) | 5% at listed supermarkets | ฿500 per primary card per cycle (11th–10th); 1 Apr 2026 – 31 Jan 2027 | **doesn't**: `เฉพาะซูเปอร์มาร์เก็ตที่ร่วมรายการ ได้แก่ Big C, Big C Online, Lotus's, Lotus's shop online, Foodland, Villa Market, Tops Supermarket, Gourmet Market & Home Fresh Mart, Central Food Hall และ Makro Pro เท่านั้น` | — | https://www.aeon.co.th/aeon/cards/aeon-world-mastercard · verified |
| AEON World points at supermarkets | points on MCC 5411/5310 spend count only to **฿10,000 per card per cycle** | | (base earning) | | same · verified |
| **NTW1** "ใช้ทุกวัน รับทุกเดือน" | ฿120 at ฿10,000–29,999, ฿340 from ฿30,000 of pooled category spend per cycle | ฿340 per national ID per cycle; 11 Jul 2026 – 10 Mar 2027; registered on AEON World | **doesn't**: `หมวดซูเปอร์มาร์เก็ต ได้แก่ BigC, Tops, Tops Food Hall, Tops daily, Gourmet Market, Foodland, Go Wholesale และ Makro PRO` | — | https://www.aeon.co.th/aeon/promotions/happy-monthly-with-aeon-2026/ · verified |
| AEON Visa Platinum 3% | listed supermarkets | ฿300 a cycle | **doesn't** (named); card not held | — | [[all-spend]] · verified (earlier) |
| AEON Next Gen 5% online | needs ≥ ฿500 of **Scan To Pay** in the cycle | | **doesn't help**: Jampha doesn't take AEON's QR, so a Jampha slip can't meet the qualifier | — | [[all-spend]] · verified (earlier) |
| AEON UnionPay 3% | CNY / HKD / MOP / TWD spend only | | **doesn't** | — | [[../../promotions/aeon-2026]] |

### 4.4 UOB

| Campaign | Cards · mechanic | Caps · period · registration | Jampha verdict | Source · confidence |
|---|---|---|---|---|
| **SPW592** "ช้อปซูเปอร์ ยิ่งจ่าย ยิ่งคุ้ม" | all UOB cards except UOB Makro; ฿50 at ฿4,000–9,999, ฿150 from ฿10,000 a month; part 2: points = slip → 10% (`SP`, not UOB One) | ฿150 a month, ฿900 for the campaign; 1 Jul – 31 Dec; SMS `SH` each month (**not registered**) | **doesn't**: `MCC code 5411, 5499 … สำหรับการซื้อที่หน้าร้านที่ Big C, Big C Mini, Don Don Donki, Foodland, Gourmet Market, GO Wholesale, Home Fresh Mart, Lotus’s, Lotus’s PRIVÉ, Lotus’ go fresh, Mitsukoshi Depachika, No Brand, Rimping, Tops …, Villa Market`; the MCC and the store list both have to match | `super-spw592-1226.json` · verified |
| **UOB Premier `PRS`** 5% | listed supermarkets, slip ≥ ฿800 | ฿500 a month; not registered | **doesn't**: Tops, Central Food Hall, Gourmet, Home Fresh Mart, Villa, Foodland | [[all-spend]] · verified (earlier) |
| **SPW796** | e-commerce and wallet ladder | | **doesn't**: named apps and wallets only | [[../../promotions/uob-epw538]] · verified (earlier) |
| **UOB Makro Gold Mission `UMK26`**, mission 3 | other spend ≥ ฿10,000 a month → ฿300 | | **doesn't**: excludes `MCC 5411` | [[../../promotions/uob-makro-gold-mission]] · verified (earlier) |
| UOB One 1%, UOB World ×2 (supermarkets ≤ ฿100,000 a cycle), UOB Premier | base earning | | physical card, −2% against the base rate (base-earning report) | |

UOB's index (632 items) has no new supermarket campaign starting in October or November (read 6 Oct).

### 4.5 KBank

#### 4.5.1 `HYP` — "ช้อป Supermarket ทุกจังหวัดทั่วไทย" (ACCS260883) · **qualifies** · verified

- **Stores**: `ทุกร้านค้าในหมวด Supermarket รวมช่องทาง online (MCC 5411, 5333)`, every supermarket by MCC. The FAQ adds "และ QR Credit Card Scan to Pay". **Excluded**: Makro and Makro PRO, Smart Pay, liquor departments, gift cards, tenant shops, other platforms, and e-wallet payments.
- **Pays, part 1** (monthly accumulation, full amount):

  | Accumulated a month | Cashback | Effective |
  |---|---|---|
  | ฿5,000 – 14,999 | ฿75 | 1.5% → 0.5% |
  | ฿15,000 – 29,999 | ฿300 | 2.0% → 1.0% |
  | ฿30,000 – 49,999 | ฿700 | 2.33% → 1.4% |
  | ≥ ฿50,000 | ฿1,250 | 2.5% at ฿50,000 |

  Caps: ฿1,250 a month and ฿5,000 for the campaign.
- **Part 2**: +฿3,000 at ≥ ฿300,000 a month (out of reach).
- **Part 3**: K Point equal to the slip → 10% (15% for The Wisdom / The Premier); SMS `BCB` (or `SYP`) every time, up to 300,000 points.
- **Cards**: every KBank card except business, corporate, Fleet and ThaiBev. Principal and supplement both count, "ยอดใช้จ่ายจะพิจารณาตามหมายเลขบัตรที่ลงทะเบียน" (each registered card number on its own). So the household reads it **per card**, in line with [[../../promotions/kbank-makro|KBank's per-card rule]]: Baiboon's KBank JCB and the PLUSTINUM she uses each have their own ladder.
- **Period and registration**: **15 Jul – 31 Oct 2026**. Register once in K PLUS or by SMS `HYP <last 12 digits>` → 4545888. **Not on the household's registration list**; HYP isn't one of the registered KBank campaigns (MKR, UQN).
- **Crediting**: within 60 days after 31 Oct.
- **Channel**: Jampha doesn't take KBank's QR, so only a physical card works.
- **Jampha verdict: qualifies.**
- **Net of the fee**:

  | Month at Jampha on one card | Rebate | Fee | Net |
  |---|---|---|---|
  | ฿10,000 | ฿75 | ฿200 | **−฿125** |
  | ฿15,000 | ฿300 | ฿300 | 0 |
  | ฿30,000 | ฿700 | ฿600 | **+฿100** |
  | ฿50,000 | ฿1,250 | ฿1,000 | +฿250 |

  So it pays only if one card carries ≥ ฿30,000 of supermarket spend in October.
- **Successor**: none in KBank's list (5 Oct).
- Source: https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-supermarket.aspx (rendered headless 6 Oct).

#### 4.5.2 `BCB` — "ร้านค้าในหมวด Supermarket แลกคะแนน K Point เท่ายอดใช้จ่าย รับเครดิตเงินคืน 10%" (ACCS260210) · **qualifies (points cash-out)** · verified

- **Pays**: K Point equal to the slip → 10% credit (฿0.10 a point), at any shop in the Supermarket category, with no minimum.
- **Registration**: SMS `BCB <last 12 digits> <amount>` → 4545888 every time (฿3 an SMS).
- **Crediting**: within 7 working days.
- **Cards**: excludes Titanium, business, corporate and LINE POINTS cards. Points of principal and supplement cards can't be pooled.
- **Period**: the header says 1 Mar 2026 – 28 Feb 2027; the body still carries last year's "1 มี.ค. 68 – 28 ก.พ. 69".
- **Net of the fee**: physical card only, so −2% on the slip; the points come out at ฿0.10.
- Source: https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-supermarket-redeempoint.aspx

#### 4.5.3 PLUSTINUM "ยิ่งใช้ยิ่งพลัสชัวร์" Season 3 and the monthly e-coupon · **qualifies (all spend)** · verified

- **Cards**: KBank PLUSTINUM and KBank Mastercard Platinum.
- **Season 3**:
  - Spend ≥ **฿30,000 in a month** → Starbucks e-Coupon ฿400. Register in K PLUS **every month**; October is the last (1 Aug – 31 Oct).
  - ≥ ฿150,000 over the campaign → 2 Coral Lounge passes.
  - Spend counts in full, with no supermarket exclusion.
- **Monthly e-coupon** (Jul – Dec):
  - ≥ **฿10,000 a month** → claim a ฿200-class coupon on the 15th of the next month in K PLUS.
  - 10,000 rights a month; principal and supplement counted separately.
- **Net of the fee**:

  | Jampha spend on the card | Rewards | Fee | Net |
  |---|---|---|---|
  | ฿10,000 | ฿200 coupon | ฿200 | 0 |
  | ฿30,000 | ฿400 + ฿200 | ฿600 | 0 |

  Only spend that tops up a month already near the threshold makes it pay.
- **Registration**: unknown for October.
- Sources: https://www.kasikornbank.com/th/promotion/creditcard/pages/plustinum-promotion.aspx · …/plustinum-event.aspx

#### 4.5.4 KBank Visa × Maroon 5 draw (to 31 Oct) and KBank JCB Japan Season 3

- **Maroon 5**: one right per ฿1,000 of any spend on KBank Visa (PLUSTINUM), registered in K PLUS.
- **JCB Japan Season 3**: see 3.3.
- **Both qualify** (draws only), at −2% per right. verified
- Source: https://www.kasikornbank.com/th/promotion/creditcard/pages/special-concert.aspx

**MKR** (Makro) and **UQN** (UNIQLO) are named-merchant campaigns. **doesn't**

### 4.6 CardX / SCB (the household's CardX JCB is Takumi's account, not one of Baiboon's cards)

| Campaign | Mechanic | Jampha verdict | Source · confidence |
|---|---|---|---|
| **HY1 / HYP / HY2** | per slip ฿40 / 200 / 720 at hypermarkets | **doesn't**: Makro, GO, Big C, Lotus's and their online shops | [[../../promotions/cardx-hypermarket]] · verified (earlier) |
| **SU1 / SU2** "ช้อปซูเปอร์ฯ คืนคุ้มเวอร์" (C6902055) | per slip ฿35 / 120 / 520 at ฿1,500 / 4,000 / 15,000; POINTX 13% / 17% | **doesn't**: `ช้อปที่ร้าน ได้แก่ Big Song, Dear Tummy, Don Don Donki, Flying Tiger Copenhagen, Golden Place, Gourmet Market, Lemon Farm, Mitsukoshi Depachika, Rimping, Sentosa, Tops, Tops Daily, Villa Market`; it also excludes "QR Payment credit card". The index's card list includes `JCPSPL` / `JCBSPL`, so CardX JCB is eligible after all ([[kbank-cardx-uob-ttb]] had inferred "no JCB" from a banner) | CardX search index, 6 Oct · verified |
| **PAYDAY supermarket** (`PDT` / `PDL` / `PDG`) | ฿100 on ≥ ฿1,500, 25th to month-end | **doesn't**: Tops, Lotus's, Gourmet | same · verified |
| "ใช้จ่ายทุกไลฟ์สไตล์" (C6901862) · "หยิบบัตรรับความคุ้ม" (C6901440) | ≤ ฿300 a card / ฿80 a slip ≥ ฿500 at "ร้านค้าทั่วไปที่ร่วมรายการตาม MCC Code" | **doesn't apply**: these are for SCB KING POWER Mastercard holders (`MCAKPG`, `MCAKPR`), not the household's card; they end 31 Oct | same · verified |

### 4.7 ttb (ttb so smart: Takumi's …7368, Baiboon's …0864)

| Campaign | Mechanic | Jampha verdict | Source · confidence |
|---|---|---|---|
| **SPM** "ช้อปคุ้ม ณ ซูเปอร์มาร์เก็ตชั้นนำที่ร่วมรายการ" (= `tops-oct26`) | per slip ฿1,000–4,999 → ฿20, ฿5,000–14,999 → ฿120, ≥ ฿15,000 → ฿500; ฿1,000 per person for the campaign; 1 Oct – 31 Dec; SMS `SPM` → 4899777 | **doesn't**: `ซูเปอร์มาร์เก็ตที่ร่วมรายการ`: Dear Tummy, Donki, Foodland, Golden Place, Gourmet Market, Mitsukoshi, Rimping, Super Cheap, TOPS, Villa Market, No Brand (+ Freshket, TOPS Online, Villa Online) | https://www.ttbbank.com/th/promotion/credit-card/shopping/supermarket-oct26 · verified |
| **BGO** | hypermarket per slip | **doesn't**: Big C and GO only | [[../../promotions/ttb-2026]] · verified (earlier) |
| **BCG / CTG** | **fuel**: 3% of a ฿600+ slip (฿18) at **B**angchak (`BCG`) / **C**altex (`CTG`), ฿72 a month each; 1 Jul – 31 Dec | **doesn't**: fuel only | [[../../promotions/ttb-2026]] · verified (earlier) |
| **ttb so smart 1%** (card benefit) | 1% on everything not excluded; supermarkets aren't excluded | **counts**: physical card, 1% − 2% = **−1%** | base earning |

ttb's shopping listing (69 tiles, 6 Oct) has no other supermarket campaign.

### 4.8 Bangkok Bank, GSB and others (no household card)

| Campaign | Mechanic | Jampha verdict | Source · confidence |
|---|---|---|---|
| **BSUP** "ช็อปซูเปอร์ฯคุ้ม" | points: 1,000 per ฿1,000 → ฿130 (13%; 15% Pinnacle / Infinite) | **doesn't**: Makro, Makro PRO, Big C, Donki, Dear Tummy, Gourmet, Foodland, Lotus's, MaxValu, Rimping, Tops, Villa; ends 31 Oct; primary cards only | [[ktc-aeon-other-banks-networks]] §1.3 · verified (earlier, 1 Oct) |
| Bangkok Bank Titanium | per-cycle ladder; supermarkets count to ฿20,000 | would count by MCC; not held | [[all-spend]] · verified (earlier) |
| Bangkok Bank UnionPay 2% | ≥ ฿2,000 a month anywhere except China, ≤ ฿1,000 a month | would count, by UnionPay QR too (reading); **not held** | [[all-spend]] · verified (earlier) |
| GSB "ช้อปซูเปอร์คุ้ม" | per slip ฿40 / 150 / 450 | **doesn't**: named (Lotus's, Big C, Tops, MaxValu, Gourmet, Villa, Foodland, Golden Place) | [[ktc-aeon-other-banks-networks]] §1.4 · verified (earlier) |
| Krungthai, ICBC, BOC, KKP, TISCO, LH, CIMB | nothing for supermarkets ([[ktc-aeon-other-banks-networks]] §5) | — | verified (earlier) |

---

## 5. Shared quotas

- **UnionPay QR 6%**: ฿300 per card a month, shared with every UnionPay QR slip that month (Bangchak, CMEx, restaurants). UnionPay's nationwide pool is first come, first served.
- **NW4's ฿30,000 supermarket allowance**: shared across the First Choice account with Makro PRO (5411), Tops, Big C and GO. Fuel has its own ฿30,000.
- **Krungsri HALO**: 2 vouchers per primary account for the whole of Aug–Oct.
- **KBank HYP**: ฿1,250 a month and ฿5,000 for the campaign, read per card number. It excludes Makro, so it doesn't collide with `MKR`.
- **The AEON gift**: per card number per day, from a campaign-wide stock (120 backpacks, 900 tumblers).
- **KTC `JFM`**: no cap; it draws on the card's own KTC FOREVER points.
- **HY1** pays once across Makro, GO and hypermarkets, and **SUP1's** ฿120 covers its named stores. Neither counts Jampha.
- **AEON World's ฿500 a cycle** and **NTW1** don't count Jampha either.

## 6. November and after

| Item | State on 6 Oct |
|---|---|
| UnionPay QR November (`260723112621`) and December (`…622`) | listed, not started; each card needs a new registration each month |
| KTC `JFM` and the KTC Jampha mall offer | run to 31 Dec 2026 |
| NW4 | runs to 31 Dec, monthly |
| Successors of Krungsri SUP1/SUP2/JSU/HALO, KBank HYP and PLUSTINUM Season 3, Bangkok Bank BSUP, and the AEON Jampha gift | all end 31 Oct; none published |
| JCB Japan Season 3 | to 31 Jan 2027 |
| BTS draw round 3 | to 15 Nov |

## 7. Open questions

1. **Which Jampha branch Baiboon uses.** The AEON gift (§2.3) covers only the three Lamphun locations; KTC `JFM` covers every branch.
2. **Whether AEON UnionPay can pay by UnionPay QR at Jampha, and whether AEON counts it** for the gift (§2.3). That would avoid the 2% fee.
3. **Whether KTC counts a UnionPay QR slip for `JFM`** (§2.1).
4. **Whether HALO's two vouchers** (Aug–Oct) were already earned, and whether HYP, PLUSTINUM Season 3 (October) and the KBank JCB Japan draw are registered.
5. **Whether the 2% fee shows in the bank's slip amount** for every card. The ฿6,120 First Choice slips say yes for First Choice; it's unconfirmed for the others.
6. **The PromptPay-through-TrueMoney route** (§1), not researched.
7. **Whether a card network's rules let Jampha add the fee at all.** Not researched; if they don't, the issuer could take a complaint. **unverified**

## 8. Registration cheat-sheet (for a Jampha slip)

| Code | Issuer · card | How | When |
|---|---|---|---|
| UnionPay QR October | KTC UnionPay …1346, …2310 | UnionPay's offer page, offer 260723112620 | before paying; again for November (…621) |
| `JFM` | any KTC card | SMS `JFM <16 digits>` → 0613845000, or `ktc.promo/jamphasavemart` | every slip, the same day |
| AEON gift | any AEON card | show the slip at AEON, Big C Lamphun | the same day |
| `HALO` | Krungsri VISA | UCHOOSE | registered (Aug carries over) |
| `HYP` | KBank JCB, KBank PLUSTINUM | K PLUS or SMS `HYP <12 digits>` → 4545888 | once, by 31 Oct |
| `BCB` | KBank | SMS `BCB <12 digits> <amount>` → 4545888 | every redemption |
| PLUSTINUM Season 3 | KBank PLUSTINUM | K PLUS | for October |
| `NW4` | First Choice | auto-enrolled | — |
| `JCLD` · KBank JCB Japan | Krungsri JCB · KBank JCB | UCHOOSE · K PLUS | once |
