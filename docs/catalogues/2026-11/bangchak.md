---
tags: [catalogue-research, 2026-11]
researched: 2026-11-01
---

> **Research snapshot**: Bangchak (and BSRC, Bangchak's ex-Esso stations) — November 2026 research. Read on **2026-11-01** from the official pages, for the November 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] page `Bangchak — Nov 2026` (Makro, GO Wholesale, Shopee, The 1, Shell, PTT and Bangchak). Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions stayed in the session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

Labels: **V** verified on the official page today · **R** my reading of official terms · **T** third-party only · **U** unverified. "Read today by the X researcher" means another November researcher saved the official page earlier on 1 Nov and I re-read their copy.

Page letter for the lineage table: **D** (Bangchak; **B** is AIS Bill Payment), alongside M G S T F P.

## 0. The household at Bangchak (ledgers, read-only, 2026-11-01)

`fetch-transactions` with `name_contains` `BANGCHAK` / `BSRC` across the three ledgers, card IDs mapped with `lib.cards.card_titles_by_id` (60 rows incl. credit lines, Mar 2025 – Oct 2026).

- **Baiboon** (Chiang Mai, plus trips): `BANGCHAK-PEMPOON PETRO…`, `BANGCHAK BGN-MAHIDOL…`, `BANGCHAK BGN-CHANGPHUE…`, `BANGCHAK BGN-SUPER HIGHWA…`, `BANGCHAK-INTHANON THAN…`, `BANGCHAK-THAITANAGROUP…`, `BANGCHAK-PANDA STAR OI…`, `BSRC-SUSCO-MAE SA`, `BSRC-SRITHONG(WATJEDYO…`, `BSRC-RUNGRUEANGSAP 369`, `BSRC-PHAAPOOM ENERGY LAMPHUN`, and on trips `BANGCHAK-MAETHA PHITSANULOK`, `BSRC-T C H DEVELOPMENT NONGKHAI`, `BANGCHAK-KORNSARN CO-OP CHAIYAPHUM`. Slips ฿90–1,350, mostly ฿300–500 before Aug 2026 and ฿600–1,000 since (she now fills to the campaign minimums).
  - 2025 – May 2026: **KTC UnionPay** (14 slips), UOB Premier / World / One (earn nothing at fuel), First Choice.
  - Since Jul 2026: **ttb so smart** (BCG) and **Krungsri JCB** (Bangchak 1% + BC3P/BXP), First Choice for the odd top-up.
- **Takumi**: **KTC UnionPay** at `BANGCHAK BGN-CHANGPHUE` **฿940 on 3 Aug, 1 Sep and 1 Oct 2026** (= ฿1,000 × 0.94, the UnionPay QR 6% at its ฿60-a-slip cap, early each month before the pool runs out); `BSRC-SDA-WAT CHET YOD` ฿686.20 (= ฿730 × 0.94) on 2 Sep; **Krungsri Lady** ฿800 (18 Aug, 12 Sep) and ฿700 (18 Oct) at the same two stations.
- **Nuta**: no Bangchak row (she fills at PTT in Bang Saen).

**What the ledger proves** (household evidence, label **R**):

| Fact | Rows |
|---|---|
| **Bangchak and BSRC stations take UnionPay QR, and the 6% applies** | KTC UnionPay ฿470 = ฿500 × 0.94 at PEMPOON (7 Mar, 5 May), INTHANON THAN (9 May), BGN CHANGPHUE (13 Apr), THAITANAGROUP (8 Feb); ฿488.80 = ฿520 × 0.94 at BGN SUPER HIG (8 Apr); ฿940 at BGN-CHANGPHUE; ฿686.20 at BSRC-SDA-WAT CHET YOD. Whole-baht slips (฿450 in Sep–Dec 2025, ฿500 on 18 Apr / 20 May) show months or days without the discount. |
| **Krungsri's "1%" pays ฿7 per whole ฿700, not 1%** | Baiboon's JCB ฿1,000 at `BSRC-T C H DEVELOPMENT` (13 Oct) got `BANGCHAK SPECIAL DISCOUNT OF 1 %` **−฿7** on 14 Oct, not ฿10. This settles the rounding question left open in [[../../promotions/krungsri-card-2026]] (a ฿1,000 slip earns one step). |
| **BSRC slips count as Bangchak** for Krungsri (1%, BC3P) and **ttb BCG** | Krungsri: BSRC-PHAAPOOM, BSRC-SRITHONG, BSRC-T C H all got the 1% line. ttb: `CB BANGCHAK AUG26` −฿54 = 3 × ฿18 for BGN-SUPER HIGHWA ฿870, BGN-MAHIDOL ฿800 and **BSRC-PHAAPOOM ฿600**. |
| The Krungsri 1% posts **within the cycle**, the day after the fill | 18 Oct → 19 Oct, 13 Oct → 14 Oct, 14 Sep → 15 Sep. |
| ttb BCG is paid as `CB BANGCHAK <MON><YY>` about seven weeks later | Aug → 17 Sep (−฿54, booked to Takumi), Sep → 19 Oct (−฿18). |

### Promotion Bureau, November (from `write-catalogue` `status: "2026-11"`, read 03:00 on 1 Nov)

| Bureau row | Period | Spent | Credit | Cap | **Left** |
|---|---|---|---|---|---|
| `2026M11 — Bangchak700 Krungsri JCB cb 1%` | cycle 5 Oct – 4 Nov | ฿1,000 (Baiboon) | ฿7 | ฿21 | **฿14** (two more ฿700 slips by 4 Nov) |
| `2026M11 — Bangchak700 Krungsri Lady cb 1%` | 5 Oct – 4 Nov | ฿700 (Takumi) | ฿7 | ฿21 | **฿14** |
| `2026M11 — Bangchak700 Krungsri VISA cb 1%` | 5 Oct – 4 Nov | — | — | ฿21 | **฿21** |
| `2026M12 — Bangchak700 Krungsri JCB / Lady / VISA cb 1%` | cycle 5 Nov – 4 Dec | — | — | ฿21 each | **฿21 each** |
| `2026M11 — BXP Krungsri JCB / Lady / VISA cb 2.5%` | 1–30 Nov | — | — | ฿52.50 each | **฿52.50 each** |
| `2026M11 — BCG cb 3%` (ttb so smart, Takumi + Baiboon pooled) | 1–30 Nov | — | — | ฿72 | **฿72** (4 slips) |
| `2026M11 — UnionPay QR …1346 cb 6%` / `…2310 cb 6%` (KTC UnionPay) | 1–30 Nov | — | — | ฿300 each | **฿300 each** |

UnionPay's November QR offer `260723112621`: **99.83% of the pool left at 03:05 on 1 Nov** (`flushProcess`: `show` 1, `totalCount` 10,000). October's pool ran out on 10 Oct, September's on 12 Sep. **V**

## 1. Headline changes vs October

1. **Nothing at Bangchak ended on 31 Oct.** Every bank campaign at Bangchak runs into December or later: Krungsri Bangchak700 / BXP (to 31 May 2027; BXP round 1 to 31 Jan), ttb BCG (31 Dec), Lotus's Bangchak 3% (31 Dec), KTC's four Bangchak pages (31 Dec; the 9-point Hi Premium coupon to 28 Feb 2027), KBank's points-at-Bangchak (31 Dec).
2. **New for November, invited only: Lotus's ดีต่อใจ fuel `CGS11`** — 20% on one Lotus's card slip ≥ ฿500 at a fuel station (MCC 5541; "อาทิ BANGCHAK, SHELL, PTT"), ≤ ฿100, first 2,000 registrants, registration from 10:00 today. §2.4.
3. **KTC JCB's ฿45 e-coupon resets**: October's 8,000 coupons ran out ("สิทธิ์เดือนตุลาคม เต็มจำนวนแล้ว" on the page today); November has a new 8,000. §2.2.
4. **Bangkok Bank's Bangchak / Caltex rebate ends 30 Nov 2026** and no successor is posted (its promotion feed has no other fuel rebate today). §2.6.
5. **Lotus's coins at fuel end 1 Dec** — irrelevant at Bangchak, where Lotus's already gives no coins (the 3% replaces them).
6. Confirmed from the ledger: Krungsri's "1%" is **฿7 per whole ฿700** (a ฿1,000 slip earned ฿7).

## 2. Bank and network campaigns at Bangchak

### 2.1 Krungsri Card — Bangchak700 (card benefit) + BXP (registered), 1 Oct 2026 – 31 May 2027

Source: https://www.krungsricard.com/th/promotion/bangchak (read today by the Krungsri researcher; I re-read the full terms) · **V**

| Card group | ต่อ 1, card benefit (no registration) | ต่อ 2 (UCHOOSE registration) | Total at ฿700 |
|---|---|---|---|
| **Platinum group**: Krungsri VISA Platinum, Mastercard Platinum, **JCB Platinum**, **Lady Titanium**, HomePro Visa Platinum, AIA Visa Platinum (+ Doctor Card for ต่อ 1) — the household's **Krungsri VISA, JCB, Lady** | **1%**: ฿7 per whole ฿700 a slip; fuel counted ≤ **฿2,100 per primary account per statement cycle** (primary + supplements) → ≤ **฿21 a cycle** | **`BXP`**: ฿17.50 per whole ฿700 a slip (2.5%), ≤ **฿52.50 per primary account per calendar month** (primary + supplements) | **฿24.50 (3.5%)** |
| **Signature group**: Krungsri Private Banking, Exclusive Signature, Siam Takashimaya Finesse (invitation), **Krungsri Signature**, **Krungsri JCB Ultimate** | **3%**: fuel ≤ ฿3,500 a cycle → ≤ **฿105 a cycle** | **`BXS`**: ฿14 per whole ฿700 (2%), ≤ **฿42 a month** | **฿35 (5%)** |

- **Not eligible**: Krungsri NOW, Siam Takashimaya (non-Finesse), corporate, TCC Privilege, HomePro Corporate. **V**
- **Registration (ต่อ 2 only)**: UCHOOSE app, search `BXP` (Signature group: `BXS`), "once per round": **round 1 = 1 Oct 2026 – 31 Jan 2027, round 2 = 1 Feb – 31 May 2027 — register again for round 2**. Register on or before the day of the fill. UCHOOSE only (no SMS is offered). The household's cards are registered for round 1 ([[../../promotions/krungsri-card-2026]]). **V**
- **Networks**: ต่อ 1 counts only spend "ในระบบของ Visa, Master Card และ JCB"; BXS counts Visa and JCB only; BXP Visa, Mastercard and JCB. Full-amount payments only. A UnionPay QR or a wallet payment doesn't count. **V**
- **Per slip, whole steps, slips never add up** ("ยอดใช้จ่ายแต่ละรายการ ไม่สามารถนำมาสะสมหรือรวมกันได้"). A ฿600 fill earns nothing; ฿1,000 earns one step (ledger, §0). **V/R**
- **Crediting**: ต่อ 1 within the same cycle (statement line `BANGCHAK SPECIAL DISCOUNT OF 1 %`, posted the next day, §0); BXP/BXS within 30 days after month-end, to the primary account (statement text in Sep was `CB12_BC3P CAMPAIGN …` / `CP12_BC3P …` for the predecessor). **V**
- **No points** on these slips ("สงวนสิทธิ์ยกเว้นการให้คะแนนสะสมปกติ"); Krungsri's points terms exclude Bangchak anyway (`/th/krungsri-point` item 2.1, per [[all-spend]]). **V**
- **Exclusions**: LPG (gas) stations, payments through e-wallet apps, Krungsri Consumer installment plans. **"Not combinable with other promotions"** is in the general conditions box that covers both parts. **V**
- **BSRC (ex-Esso) stations count** (ledger, §0). **R**
- Caps are **per primary account** — Baiboon's JCB supplement and Takumi's JCB share one ฿21 / ฿52.50. Each product (VISA, JCB, Lady) is its own account, so the household has three of each.

**Other Krungsri items at Bangchak** (krungsricard.com, all **V**):
- `gas-lover`: **899 points (normally 1,100) → ฿100 fuel e-voucher** at Bangchak, PT, Susco and Sinopec Susco; UCHOOSE → คะแนนสะสม → สินค้าและบัตรกำนัล; voucher valid 30 days; 1 Jan – 31 Dec 2026; all Krungsri cards incl. NOW. ≈ ฿0.111 a point. https://www.krungsricard.com/th/promotion/gas-lover
- `bangchak-points`: **1,000 Krungsri points → 500 Bangchak points** (Green Miles), via UCHOOSE (U MALL → Point แลก → โอนคะแนนบัตร) or the Bangchak app; minimum 1,000, steps of 1,000, ≤ 500,000 a day; 1 Jan – 31 Dec 2026. At Green Miles' 500 → ฿100 coupon (§3) that's ฿0.10 a point, and the coupon needs a ฿1,000 fill. https://www.krungsricard.com/th/promotion/bangchak-points
- `point-cashback` (PT26): points → statement credit at ฿0.10 a point for MCC 5541/5542 spend in the same month. Bangchak slips on Krungsri earn no points themselves; whether PT26 can be used on a slip that already earned Bangchak700 / BXP isn't stated (the Bangchak page's "not combinable" line suggests not). **R** · https://www.krungsricard.com/th/promotion/point-cashback

### 2.2 KTC — four Bangchak campaigns, all at "สถานีบริการน้ำมันบางจากที่ร่วมรายการทั่วประเทศ"

Read with curl today from https://www.ktc.co.th/promotion/auto-gas-ev/gas-station-ev-charger (23 fuel/EV pages; five Bangchak URLs, one of them the hub `bangchak-x-jcb` "3 สิทธิพิเศษ"). Terms are in the RSC chunks. **V**

| Campaign | Cards | Mechanic | Minimum | Caps | Registration | Period · credit |
|---|---|---|---|---|---|---|
| **`BC` — points → 15%** (`bangchak-cashback`) | every KTC card with KTC FOREVER points (not ROP, Cash Back, Blood Centre, Visa Corporate, government, PROUD) | redeem KTC FOREVER points: **every 100 points → ฿15** (15%), up to the slip amount; satang rounded up | **฿900 a slip**, net of discounts, MCC 5541, one slip (no splitting) | none stated; per card | once: SMS **`BC <16-digit card>` → 0613845000**, or the web form, on or before the day; confirmation SMS needed | **1 Oct – 31 Dec 2026** · within 60 days after each calendar month |
| **KTC JCB 5% e-coupon** (`bangchak-jcb`) | **KTC JCB** (all types) | **฿45 cash-back e-coupon** in KTC Mobile per slip | **฿900 a slip**, net, MCC 5541 | **8,000 coupons a month nationwide, 24,000 over the campaign**; no per-card limit stated. **October's 8,000 ran out** ("สิทธิ์เดือนตุลาคม เต็มจำนวนแล้ว") | none, but **KTC Mobile must be installed before the fill** (no back-dating); tap the coupon within its validity | 1 Oct – 31 Dec 2026 · credit within 5 working days of tapping; only stations whose terminal takes JCB |
| **Hi Premium e-coupon for spending** (`bangchak-e-coupon-hi-premium`) | all KTC credit cards (not Visa Corporate, government, PROUD) | **฿100 Bangchak Hi Premium e-coupon** in KTC Mobile | spend **฿1,200 a slip**, net | **40,000 coupons a month, 120,000 over the campaign** | none; KTC Mobile before the fill; accept the coupon within 10 days | 1 Oct – 31 Dec 2026 · coupon valid 10 days, usable on a **Hi Premium fill ≥ ฿1,000** |
| **Hi Premium e-coupon for 9 points** (`bangchak-e-coupon`) | every KTC card with KTC FOREVER points | **9 points → ฿100 off** a Bangchak Hi Premium fill (the banner: "แลก 9 คะแนน รับส่วนลด 100 บาท"); unlimited redemptions, 1 coupon a slip | Hi Premium fill **≥ ฿1,000** a slip; the balance must be paid with a KTC credit card | none stated | redeem in KTC Mobile → แลกคะแนน; show the QR to the attendant; coupon valid **7 days**; screenshots refused | **15 May 2026 – 28 Feb 2027** |

- The 9-point page's headline still says "ทุก 1,000 คะแนน = ส่วนลด 100 บาท", but the offer box, the T&C ("สมาชิกสามารถใช้ 9 คะแนนแลกรับโค้ดส่วนลด…") and the banner all say **9 points**. **V**
- KTC's `BC` page says KTC–Bangchak co-brand cards keep their own 1% at Bangchak. **V**
- KTC caps points and cash back on MCC 5541/5542 at **฿30,000 per card per month** (from 1 Apr 2026). **V**
- **KTC JCB "ลุ้นเปย์ ไป JAPAN Season 3" (`JLD`)** is advertised on the JCB page: register **`JLD <16 digits>` → 0613845000**, 1 Oct 2026 – 31 Jan 2027, each KTC JCB slip ≥ ฿1,000 = one draw right (three Japan tour packages for two). **V**
- **Stacking**: no KTC page says the four don't combine. A ฿1,000 Hi Premium fill paid with KTC JCB, using a 9-point coupon (pay ฿900 net), still meets the ฿900 net floor of the JCB coupon and of `BC`. **R**, not tested.
- **Which household card?** Takumi's KTC JCB / Digital VISA / Mastercard / UnionPay and Baiboon's KTC UnionPay supplement all have KTC FOREVER points (no points balance recorded here). A KTC UnionPay slip paid by **UnionPay QR** is still a KTC card slip, so a ฿1,000 fill at ฿940 net clears the ฿900 floor of `BC`. **R**
- **Inthanin** (Bangchak's coffee chain, in many stations): KTC **499 points → one iced drink ≤ ฿65** (espresso, americano, Thai tea latte, green tea latte, cocoa), KTC Mobile only, all branches except Skylane, 1 Mar 2026 – 28 Feb 2027. **V** · https://www.ktc.co.th/promotion/dining-restaurants/desserts-beverages/inthanin-coffee

URLs: https://www.ktc.co.th/promotion/auto-gas-ev/gas-station-ev-charger/bangchak-cashback · …/bangchak-jcb · …/bangchak-e-coupon-hi-premium · …/bangchak-e-coupon · …/bangchak-x-jcb

### 2.3 ttb — `BCG`, 1 Jul – 31 Dec 2026

Source: https://www.ttbbank.com/th/promotion/credit-card/auto/bangchak-jul26 (read today by the bank researcher, headless) · **V**

| Card | Pays | Cap |
|---|---|---|
| every ttb credit card (incl. ttb so smart, TMB / Thanachart cards, Global House, Disney), primary and supplement | **3% of a slip ≥ ฿600, at most ฿18 a slip** | **4 slips (฿72) per person a month** |
| the same, for a primary cardholder with a **ttb DRIVE car loan or ttb home loan** in good standing | **5%, at most ฿30 a slip** | 4 slips (฿120) a month |

- Register once: ttb touch, or SMS **`BCG <last 12 digits>` → 4899777**; ttb reserve infinite is automatic. Supplements' spend pools into the primary's account (only cards that registered). **V**
- Credit within 60 days after the month; statement text `CB BANGCHAK <MON><YY>` (ledger). **V**
- So ฿18 is the most any household fill earns, from ฿600 up: **3% at ฿600, 2.6% at ฿700, 1.8% at ฿1,000**. A ฿500 fill earns nothing. ttb so smart's own 1% excludes petrol. **R**
- BSRC counts (ledger, §0). **R**

### 2.4 Lotus's (Lotus's Beyond)

**Bangchak 3%** (card benefit), 1 Jan – 31 Dec 2026 · https://www.lotussmoney.com/announcement-corporate/bangchak-2026 (read today by the Krungsri researcher) · **V**
- **Lotus's Platinum Beyond 3%**, Platinum Rewards 2%, on fuel products at Bangchak, counted on **at most ฿700 a slip** and **3 slips per primary-account cycle** (by posting date) → **≤ ฿63 a cycle** (Beyond), ≤ ฿42 (Rewards).
- No Lotus's coins on Bangchak fuel. LPG and non-fuel products excluded. **E-wallet payments excluded**: LINE Pay, TrueMoney Wallet, AirPay, Blue Connect, ShopeePay, GB Prime Pay.
- The station is recognised by **the name on the slip and in Lotus's system** ("คำนวณจากยอดใช้จ่ายและชื่อปั๊มน้ำมัน ที่ปรากฏบนเซลล์สลิป"). Whether a `BSRC-…` slip is recognised isn't stated: prefer a `BANGCHAK…` station for this card. **R/U**
- Takumi's card; Baiboon books Lotus's slips as `[บัตรหลัก]` rows.

**ดีต่อใจ "เติมดีต่อใจ" — fuel category `CGS11`**, **1–30 Nov 2026**, invited cardholders only · https://www.lotussmoney.com/promotion-segment/credit-card/deetorjai-joy-nov26 (read today by the Krungsri researcher) · **V**
- **20% on one slip ≥ ฿500 at MCC 5541 ("อาทิ BANGCHAK, SHELL, PTT"), at most ฿100 per slip per primary account per month** → a ฿500 fill earns ฿100.
- **Register before the fill, from 10:00 on 1 Nov, first 2,000 per month per category**, in UCHOOSE (or SMS `CGS11`; number not printed on the page I read — Lotus's SMS line is 081-250-7777 per the Krungsri researcher, **R**). Register again every month. Spend counts from the registration day.
- Invitation: Lotus's cardholders with ≥ 3 slips of ≥ ฿100 during 1–15 Oct were to be told by end-October. **R** (Krungsri researcher)
- Credit within 30 days after 30 Nov. No "not combinable" line on the page; whether it stacks with the Bangchak 3% isn't stated. **R**

### 2.5 KBank — points at Bangchak, 1 Jan – 31 Dec 2026

Source: https://www.kasikornbank.com/th/promotion/creditcard/pages/bangchak.aspx (headless Chrome today) · **V**
- **Pay with K Point at the pump: every 1,000 points = ฿100**, or **10% off by redeeming points equal to the spend** (a ฿500 fill → 500 points for ฿50 off). Both are ฿0.10 a point. Points under 1,000 can't be used for the first option; the discount option is full-amount payments only.
- **Not eligible: KBank Titanium, LINE Points card**, business and corporate cards. Takumi's PLUSTINUM, JCB and Shopee cards qualify; his LINE Points card doesn't.
- No registration printed; how the redemption is made (EDC "pay with points" at the station) isn't described on the page. **U**
- KBank earns K Point at fuel at 1/฿25 with **≤ 800 points a cycle** at supermarkets + fuel ([[all-spend]] §3). No KBank cashback campaign at Bangchak in its 231-campaign list today (the fuel category holds Auto1, B-Quik, Autobacs, Cockpit, Fit Auto installments, EV charging and the Blue (PTT) card). **V**

### 2.6 Bangkok Bank — Gas Cash Rebate (Bangchak and Caltex), 1 Dec 2025 – **30 Nov 2026**

Source: https://www.bangkokbank.com/th/personal/cards/credit-cards/promotions/gas-cash-rebate-251201-261130 (read today headless by the KTC/AEON researcher) · **V**

| Card | Credit per whole ฿800 of a slip |
|---|---|
| Pinnacle, Infinite, Bangkok Bank M LEGEND | **10%** (฿80) |
| Platinum Leader, M LUXE | 3% (฿24) |
| all other Bangkok Bank cards, M LIVE | 2% (฿16) |

- Each whole ฿800 = one right; **≤ 6 rights per card account per cycle** (primary + supplements, all stations), first come by transaction date. No registration. Credited on the statement of the cycle. **V**
- **Excluded**: UnionPay cards, Corporate / Purchasing, fleet cards, and **Bangkok Bank American Express at Bangchak**. Slips under ฿800 earn normal points instead; a slip that earned the rebate earns no points. **V**
- **Ends 30 Nov 2026.** No successor is in the bank's promotion feed today (`promotions.allpromo.th.json`, 232 items; its other "gas" items are BEM tollway and MRT). **V**
- No household card. Best in the market for **฿800 slips** on a top-tier card.

### 2.7 First Choice

- **NW4** (1 Oct – 31 Dec): fuel counts toward the pooled ladder up to **฿30,000 a month**; ฿200 per whole ฿10,000 → **2% at the margin** for a household that already passes the steps. **V** (Krungsri researcher)
- First Choice earns points at fuel (1 pt/฿25, fuel ≤ ฿50,000 a month per [[all-spend]]); **1,000 First Choice (or XU) points → 500 Green Miles** via the Bangchak app (min 1,000, steps of 1,000, ≤ 500,000 a day; primary card's mobile number must match). **V** · https://www.firstchoice.co.th/promotion/bangchak-transfer (read today by the Krungsri researcher)
- No Bangchak cashback campaign. **V**

### 2.8 Nothing at Bangchak (checked today)

| Issuer / network | What I checked | Result |
|---|---|---|
| **UOB** | `data-promotion.json` (666 items, the bank researcher's dump) | no Bangchak item; the only fuel promotion is Shell/Caltex `SPW109`. UOB cards earn nothing at petrol. **V** |
| **CardX** | catalogue `/th-TH/credit-card/promotion`, category "น้ำมัน และ EV", headless | "ขออภัย ไม่พบผลลัพธ์" — the category is empty. **V** |
| **AEON** | 195 index tiles (KTC/AEON researcher) | no fuel campaign; AEON's all-spend campaigns exclude "หมวดน้ำมัน". **V** |
| **GSB** | promotions sitemap (514 pages) | no fuel page. **V** |
| **Central The 1 card** | `gcspromotion` list (184 items, The 1 researcher) | fuel: `shell-2026` only; no Bangchak. **V** |
| **Visa / Mastercard / JCB / UnionPay merchant offers** | Visa perks, Priceless, JCB ajax.json, UnionPay merchant list (KTC/AEON researcher's dumps) | no Bangchak / BSRC offer. UnionPay's general QR 6% (not merchant-named) applies — §2.9. **V** |
| **Krungsri NOW** | Bangchak page | excluded from Bangchak700/BXP; earns its normal 1/฿25 at Bangchak per [[all-spend]]. **V/R** |

### 2.9 UnionPay QR 6% (KTC UnionPay) — November offer `260723112621`, 1–30 Nov

- 6% off, **≤ ฿60 a slip, one discounted slip per card per day, ≤ ฿300 per card a month**, pay methods merchant QR (`02`) and consumer QR (`07`) from KTC Mobile (also ICBC / BOC TH apps); register each card for November on UnionPay's page. **V** (KTC/AEON researcher: https://marketing.unionpayintl.com/offer-promote/?language=en&insCode=299990156#/offer?offerNo=260723112621)
- **Pool: 99.83% left at 03:05 today** — use it early; October's ran out on the 10th.
- Bangchak and BSRC stations in Chiang Mai take it (§0). A UnionPay QR payment doesn't count for Krungsri, ttb or Lotus's campaigns (different cards) and BBL excludes UnionPay cards.

## 3. Bangchak's own programme

- **Who runs the stations** (Bangchak's subsidiaries page, headless today, **V**): **BGN = บริษัท บางจากกรีนเนท จำกัด (Bangchak Green Net)**, a Bangchak subsidiary; **BSRC = บริษัท บางจาก ศรีราชา จำกัด (มหาชน)** (Bangchak Sriracha, the former Esso Thailand), delisted from the SET on 12 Dec 2025 after Bangchak's tender offer (Bangchak newsroom, sitemap titles 1744/1778/1795). https://www.bangchak.co.th/th/contact/company-subsidiaries
- **Statement descriptors** (ledger, **R**): `BANGCHAK BGN-<site>` = a station run by Bangchak Green Net (MAHIDOL, CHANGPHUE, SUPER HIGHWAY…); `BANGCHAK-<dealer>` = a dealer-owned Bangchak station (PEMPOON PETRO, THAITANAGROUP, INTHANON THAN, PANDA STAR OIL, MAETHA, KORNSARN CO-OP); `BSRC-<dealer>` = an ex-Esso station now under the Bangchak brand. All three count as Bangchak for Krungsri and ttb (§0). `BANGCHAK SPECIAL DISCOUNT OF 1 %` is Krungsri's card-benefit credit, not a station.
- **Membership: Bangchak Green Miles (บางจากกรีนไมลส์)**, now app-only ("แบบดิจิทัล ไร้บัตร"); the banks call its points "Bangchak Points". App **"Bangchak"** (App Store id 459028545, v4.2.12 of 1 Oct 2026; Android `com.bangchak.android`): join, earn, redeem, transfer and donate points; e-coupons for fuel, Inthanin coffee and FURiO lubricants; partner deals; birthday gift; station finder. **V** (App Store listing)
  - **Redemption: 500 points → ฿100 fuel e-coupon** ("ปกติ 500 คะแนน แลกได้ 100 บาท"). The 20th-anniversary rate (500 → ฿120 on a ≥ ฿1,000 fill; claim 1 Jul – 30 Sep, use by 31 Oct 2026) **has ended**. **T** (Bangkok Biz News, https://www.bangkokbiznews.com/economics/1245843; Sanook, Thansettakij)
  - **"ขึ้นเท่าไหร่ คืนเท่านั้น"**: on the first day of a pump-price rise, members who fill get bonus points worth the rise. **V** (App Store text; Bangchak newsroom item 1854)
  - **Earn rate: not found.** bcpgreenmiles.com (the programme site) returns 403 to curl, headless Chrome and r.jina.ai; no news item states points per baht. **U**
  - Transfers in: Krungsri 1,000 → 500, First Choice 1,000 → 500 (§2.1, §2.7). Neither beats using the card's own cash campaigns.
- **Bangchak promotions for November**: **none found.** Bangchak's newsroom (latest 29 Oct) has no pump promotion; its "โปรโมชั่น" link (bangchakmarketplace.com/promotion) returns 404; bcpgreenmiles.com is blocked. Past patterns: ฿5/L off Hi Premium over long weekends and New Year (Oct 2025, 30 Dec 2025 – 4 Jan 2026), ฿1/L off for Green Miles members on 20 Aug 2026. **U** — check the app.
- **Makro Club partner perk**: a Bangchak Hi Premium cash-discount coupon (value not printed). **V** ([[merchants-wallets]])
- **Prices** (Bangchak's API `oil-price.bangchak.co.th/ApiOilPrice2/th`, Bangkok retail from 29 Oct 2026 05:00, **V**): Gasohol 95 S EVO **฿41.54**, Gasohol 91 S EVO ฿41.17, E20 S EVO ฿33.50, E85 S EVO ฿31.63, **Hi Premium 98 Plus ฿48.55**, Hi Diesel S ฿42.54, **Hi Premium Diesel Plus ฿49.05**, Diesel B20 ฿33.50. Chiang Mai is slightly higher (provincial price not read). Self-service stations sell ฿0.30/L below full service (newsroom 1854, Mar 2026, **T**).
  - So KTC's ฿100 Hi Premium coupon on a ฿1,000 fill makes Hi Premium 98 cost about ฿43.70 a litre — still **more than Gasohol 95 at ฿41.54**. It only pays for someone who buys Hi Premium anyway. **R**
- **Payment methods**: no Bangchak page lists them (the corporate site is behind Radware; the help pages weren't found). From the evidence: Visa, Mastercard, JCB cards (the bank campaigns; Krungsri **JCB** slips went through at PEMPOON, MAETHA, BSRC-PHAAPOOM, BSRC-SRITHONG and BSRC-T C H, but KTC warns that only stations whose terminal takes JCB qualify), **UnionPay QR** (ledger), e-wallets LINE Pay, TrueMoney, AirPay, Blue Connect, ShopeePay, GB Prime Pay (named in Lotus's exclusion line, so at least some stations take them). TrueMoney's own promotion list has no Bangchak deal ([[merchants-wallets]]). PromptPay: not confirmed. **R/U**

## 4. Ranked answer: a ฿500 fill and a ฿700 fill (November 2026)

Values are money back per slip; "pts" adds the card's normal points where they're earned. Caps per month (or cycle) in brackets. All need the card's registration where shown.

### ฿500 fill — the household's cards

| # | Card · who | Gets | % | Conditions |
|---|---|---|---|---|
| 1 | **Lotus's Beyond** · Takumi — *if invited to ดีต่อใจ* | ฿100 (`CGS11`) + ฿15 (Bangchak 3%)? | 20% (+3% if they stack) | one slip a month; register `CGS11` in UCHOOSE before filling, first 2,000; stacking unstated |
| 2 | **KTC UnionPay, paid by UnionPay QR** · Takumi, Baiboon | **฿30 off** + KTC pts on ฿470 | 6% + ≈0.4% | ≤ ฿300 a card a month, 1 a day, while the pool lasts (gone by the 10th–12th in Sep/Oct); register the card for November |
| 3 | **Lotus's Beyond** (Bangchak 3%) · Takumi | ฿15 | 3% | 3 slips a cycle; prefer a `BANGCHAK…` station |
| 4 | **First Choice** · all three | NW4 ≈ ฿10 + pts | ≈2% + ≈0.36% | pooled ladder, fuel ≤ ฿30k a month |
| 5 | KBank PLUSTINUM / JCB / Shopee · Takumi (Baiboon PLUSTINUM) | pts 1/฿25 | ≈0.4% | ≤ 800 pts a cycle at fuel + supermarkets |
| 6 | KTC Digital VISA / Mastercard / JCB · Takumi | pts | ≈0.4% | `BC` 15% burn and the JCB ฿45 coupon need ≥ ฿900 |
| 7 | AEON World · Takumi | pts 1/฿30 | value unpublished | |
| — | **Krungsri VISA / JCB / Lady** | **฿0, no points** | 0% | need a whole ฿700 → fill ฿700 instead (§ below) |
| — | **ttb so smart** | **฿0** | 0% | BCG needs ฿600 → fill ฿600 for ฿18 (3%) |
| — | UOB One / World / Premier / Makro | nothing | 0% | |

### ฿700 fill — the household's cards

| # | Card · who | Gets | % | Caps |
|---|---|---|---|---|
| 1 | Lotus's Beyond · Takumi — *if invited (`CGS11`)* | ฿100 + ฿21? | 14.3% (17.3%) | once a month |
| 2 | **KTC UnionPay via UnionPay QR** · Takumi, Baiboon | **฿42 off** + pts | 6% | ฿300 a card a month, pool |
| 3 | **Krungsri VISA / JCB / Lady** (BXP registered) · Takumi, Baiboon (JCB, VISA supplements) | **฿7 + ฿17.50 = ฿24.50**, no points | **3.5%** | per account: 1% ≤ ฿21 a cycle (3 slips), BXP ≤ ฿52.50 a month (3 slips) → **9 slips a month across VISA, JCB, Lady** |
| 4 | Lotus's Beyond (3%) · Takumi | ฿21 | 3% | 3 slips a cycle (฿63) |
| 5 | **ttb so smart** (BCG) · Takumi, Baiboon | ฿18 | 2.6% | 4 slips a month, pooled (฿72) |
| 6 | First Choice · all three | NW4 ≈ ฿14 + pts | ≈2.4% | |
| 7 | KBank / KTC (card) / AEON World | pts | ≈0.4% | |
| — | UOB | nothing | | |

**Fill size by card** (so no slip is wasted): Krungsri **exactly ฿700 or ฿1,400** (a ฿1,000 fill earns the same ฿24.50 as ฿700); ttb **฿600** (฿18 is the cap); Lotus's **≤ ฿700** (the excess earns nothing); KTC UnionPay QR **up to ฿1,000** (฿60 cap); KTC JCB / `BC` from **฿900**.

### Best in the market (any card)

| Fill | Best offer | Value |
|---|---|---|
| ฿500 | Lotus's ดีต่อใจ `CGS11` (invited) | ฿100 (20%), once a month |
| ฿500 | UnionPay QR 6% (KTC UnionPay, ICBC, BOC TH cards) | ฿30 |
| ฿600 | ttb card + ttb car/home loan (BCG 5%) | ฿30 (5%) |
| ฿700 | Krungsri Signature / Exclusive Signature / JCB Ultimate / Private Banking (3% + BXS 2%) | ฿35 (5%) |
| ฿800 | **Bangkok Bank Pinnacle / Infinite / M LEGEND** (to 30 Nov) | **฿80 (10%)**, 6 a cycle |
| ฿900 | KTC JCB ฿45 e-coupon (5%), first 8,000 a month; KTC `BC` 15% points burn | ฿45 |
| ฿1,000 Hi Premium | KTC 9-point coupon ฿100 (10%) | but Hi Premium costs ≈17% more a litre than Gasohol 95 |

## 5. What ends this month / announced for December

- **30 Nov**: Bangkok Bank Gas Cash Rebate (no successor posted); Lotus's ดีต่อใจ November round (`CGS11`; a December round is to be announced — re-register monthly); UnionPay's November QR offer (December's `260723112622` is listed, "not started"); BXP's November cap resets on 1 Dec.
- **4 Nov**: Krungsri Bangchak700 cycle closes (฿14 left on JCB and Lady, ฿21 on VISA); the next cycle runs 5 Nov – 4 Dec.
- **1 Dec**: Lotus's coins stop at all fuel stations (Bangchak already earned none).
- **31 Dec**: ttb BCG (and CTG), Lotus's Bangchak 3%, KTC `BC`, KTC JCB ฿45 coupon, KTC Hi Premium coupon for spending, KBank points at Bangchak, Krungsri `gas-lover` and `bangchak-points`, First Choice NW4. Watch for 2027 renewals in late December.
- **31 Jan 2027**: BXP round 1 — **register BXP again for round 2 (1 Feb – 31 May)**; KTC `JLD`.
- **28 Feb 2027**: KTC 9-point Hi Premium coupon; KTC Inthanin 499-point drink.

## 6. Not found / couldn't read

- **bcpgreenmiles.com** (Green Miles' site, privilege page linked from Bangchak's price API): 403 to curl, headless Chrome and r.jina.ai. So the **earn rate**, current member privileges and any November member deal are missing. www.bangchak.co.th pages behind Radware ("validate.perfdrive.com") open in headless Chrome but not to curl; the corporate site has no promotions section.
- **Bangchak's November pump promotions**: none in the newsroom, web search found none. **Not found.**
- **Payment methods** at Bangchak (PromptPay, Green Miles wallet): no official page found. No "Green Miles wallet" exists in the app description.
- **Lotus's `CGS11` SMS number** isn't on the page text; whether `CGS11` stacks with the Bangchak 3%.
- **KBank's points-at-Bangchak channel** (EDC pay-with-points or app) isn't described.

## 7. Lineage rows

| Campaign | Pays | Oct 2026 | Nov 2026 | Pages | predecessor → successor |
|---|---|---|---|---|---|
| Krungsri Bangchak700 (card "1%") | ฿7 per whole ฿700, ≤ ฿21 a cycle | live | live (to 31 May 2027) | D | Bangchak 1% (฿8/฿800) → Bangchak700 |
| Krungsri `BXP` / `BXS` | ฿17.50 / ฿14 per whole ฿700, ≤ ฿52.50 / ฿42 a month | round 1 | round 1 (to 31 Jan; round 2 1 Feb – 31 May) | D | BC3P → BXP |
| ttb `BCG` | 3% of ≥ ฿600, ≤ ฿18 a slip, 4 a month | live | live (to 31 Dec) | D | — |
| Lotus's Bangchak 3% | 3% on ≤ ฿700 a slip, 3 a cycle | live | live (to 31 Dec) | D | — |
| Lotus's ดีต่อใจ fuel `CGS11` | 20% of one ≥ ฿500 slip, ≤ ฿100 | (Oct round) | **new round, invited** | F P D | monthly |
| KTC `BC` points → 15% | ฿15 per 100 pts, ≥ ฿900 | live | live (to 31 Dec) | D | — |
| KTC JCB ฿45 e-coupon (5%) | ≥ ฿900 a slip, 8,000 a month | full in Oct | new 8,000 (to 31 Dec) | D | a 4% JCB e-coupon ran 1 Jul – 30 Sep (search snippet of KTC's English page, **T**) → 5% |
| KTC Hi Premium e-coupon (spend ฿1,200) | ฿100 Hi Premium coupon | live | live (to 31 Dec) | D | — |
| KTC Hi Premium e-coupon (9 pts) | ฿100 off a ≥ ฿1,000 Hi Premium fill | live | live (to 28 Feb 2027) | D | — |
| KBank Bangchak points | 1,000 pts = ฿100 / 10% for points | live | live (to 31 Dec) | D | — |
| BBL Gas Cash Rebate | 2/3/10% per whole ฿800, 6 a cycle | live | **ends 30 Nov** | D | no successor posted |
| Krungsri `gas-lover` | 899 pts → ฿100 e-voucher | live | live (to 31 Dec) | D | — |
| UnionPay QR 6% | ≤ ฿60 a slip, ฿300 a month | pool out 10 Oct | `260723112621`, 99.83% left 1 Nov | F D | monthly |

## 8. Logo

- **Commons: `commons:Bangchak Corporation logo.svg`** — the current leaf mark with the lower-case green "bangchak" wordmark, horizontal, 512 × 259 SVG (uploaded 2024-02-19). The 960 px thumbnail renders cleanly (`upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Bangchak_Corporation_logo.svg/960px-Bangchak_Corporation_logo.svg.png`, 960 × 487 PNG with transparency, 33 KB; downloaded and viewed today, no rate limit). **V**
- English Wikipedia also has the stacked version, `File:Bangchak Corporation Logo since November 2022.png` (300 × 245, a local en-wiki file, not on Commons) — the same mark, so the Commons SVG is the current logo. **V**
- **Bangchak's own files** (Download Center, https://www.bangchak.co.th/th/download-center/bangchak-logo, headless): `https://www.bangchak.co.th/storage/document/logo/Color-Logo-Horizontal.png` (7026 × 2111 PNG, 88 KB), `…/Color-Logo-Vertical.png`, `…/horizontal-en.svg` (SVG), `…/vertical-en.svg`, plus `.ai` files and `logo-system.pdf`. The `/storage/` paths **download with plain curl** (no Radware challenge). The horizontal PNG renders the same mark on white. **V**
- Recommended for the cover: the Commons SVG (horizontal) on the white plate; the official `Color-Logo-Vertical.png` if a square-ish mark fits better.
- Icon suggestion: ⛽.

## 9. New site tricks

- **bangchak.co.th** sits behind Radware Bot Manager (curl is redirected to `validate.perfdrive.com`), but **headless Chrome over CDP opens its pages** (subsidiaries, newsroom, app page). `sitemap.xml` reads with curl (779 URLs, no promotion section). **Fuel prices**: `https://oil-price.bangchak.co.th/ApiOilPrice2/th` (JSON, plain curl) — yesterday / today / tomorrow per product, with the effective time.
- **bcpgreenmiles.com** blocks everything tried (curl, headless, r.jina.ai). The App Store lookup (`itunes.apple.com/lookup?id=459028545&country=th`) gives the programme's own description.
- **KTC**: the fuel category page lists every live fuel campaign's slug; a page's headline can be stale while its offer box, T&C and banner agree (the 9-point coupon). Read the banner (`/upload/promotion-…-dt-…webp`) when they disagree.
- **CardX** category tabs: an empty category renders "ขออภัย ไม่พบผลลัพธ์" — a reliable "nothing here" signal (the bank researcher's earlier click had captured the "ทั้งหมด" tiles instead).
- **The ledger settles per-slip rounding**: a slip that isn't a whole multiple of the step (Baiboon's ฿1,000 → ฿7) shows how a bank rounds; look for one before guessing.
