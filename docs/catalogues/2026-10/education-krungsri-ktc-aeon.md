---
tags: [catalogue-research, 2026-10]
researched: 2026-10-22
---

> **Research snapshot**: university tuition — Krungsri group (Krungsri Card, First Choice, Central The 1, Lotus's), KTC and AEON — October 2026 research. Scope: what each of Baiboon's cards from these issuers pays on one semester's tuition at Chiang Mai University (มหาวิทยาลัยเชียงใหม่, CMU), a slip of ฿60,000–100,000 paid in late Oct or Nov 2026 (semester 2/2569): base points or cashback at an education MCC (8220, with 9399 and 8299 as alternatives), each issuer's no-points lists, all-spend campaigns, tuition installments, points-for-tuition burns, and student or parent offers. Read on **2026-10-22** from the official pages, for an October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] page. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions (HTML, JSON, PDFs, posters) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# University tuition — Krungsri group, KTC and AEON — October 2026 (ต.ค. 69)

Researcher: `education-krungsri-ktc-aeon` · researched 2026-10-22 · read-only. Other researchers cover CMU's own payment channels, UOB / KBank / ttb / CardX and the other banks, and offers that name no merchant.

**Legend.** ✓ counts · ✗ doesn't · ? unclear · 🏠 a household card. Confidence: **verified** (the issuer's own page read today) · **household** (the household's ledger shows it) · **third-party only** · **unverified**.

**The payment.** Baiboon pays one semester at CMU, over ฿60,000, most likely late Oct or Nov 2026. All her cards in scope are **supplements on Takumi's accounts**, so account-level caps and pooled ladders are shared with Takumi (and Nuta where she holds the same card).

**MCC assumptions** (CMU's channel is another researcher's question):
- **8220** (Colleges, Universities, Professional Schools) is the code a university charge normally carries. The working figures below use it.
- **8299** (Schools and Educational Services, not elsewhere classified) or **8211** (schools) if CMU's payment gateway posts under a generic education code. Every list below that names 8220 also names 8211–8299, so the answer is the same.
- **9399** (Government Services) if CMU's payment posts as a government body. CMU is an autonomous public university (`มหาวิทยาลัยในกำกับของรัฐ`), so this is possible.
- **Household evidence**: no tuition row exists in Baiboon's ledger (searched `UNIV`, `CMU`, `TUITION`, `มหาวิทยาลัย`, all rows ≥ ฿15,000). Takumi's `CHULALONGKORN UNIVERSITY BANGKOK` ฿33,500 (31 Jul 2026, KBank PLUSTINUM) realised 1,340 points = 1 per ฿25, so a Thai university charge did post as an ordinary card slip there; its MCC isn't recorded.

**Point values used.** Krungsri, KTC ฿0.10 · The 1 ฿0.125 · Lotus's coin ฿1 · First Choice ≈ ฿0.09–0.10 · AEON Happy Point: no published cash value.

---

## 0. At a glance

(being written)

---

## 1. Krungsri Card (VISA, JCB, Lady, NOW)

Baiboon holds supplements on Takumi's Krungsri VISA, JCB, Lady and NOW. Each product is its own card account, with its own caps and registrations, and every household Krungsri card is registered for every campaign ([[../../promotions/krungsri-card-2026]]). The listing JSON held **581 items** on 22 Oct; 13 match education words. Only one is for tuition.

### 1.1 Base points at an education MCC · verified

- Source: [กรุงศรี พอยต์ terms](https://www.krungsricard.com/th/krungsri-point) (`?a=1` was needed past the WAF, see *Site methods*).
- `การรับคะแนน "กรุงศรี พอยต์" 1 คะแนน เมื่อใช้จ่ายผ่านบัตรครบทุก 25 บาท ต่อเซลล์สลิป` → **0.4%** at ฿0.10 a point.
- **No education exclusion.** The no-points list (2.1–2.3) names cash, utilities, Bangchak fuel, funds, insurance, fees, foreign merchants and foreign-THB, transit 4111/4112/4131/4784, 7-Eleven and TrueMoney-linked spend (from 1 Aug 2026), fuel above ฿50,000 a month, and government MCCs.
- **Government MCCs are out**: `MCC 9211, 9222, 9223, 9311, 9399 … 9405 … 7802`, `โดยยกเว้น หมวดที่เกี่ยวข้องกับโรงพยาบาล มูลนิธิ องค์กรการกุศล และ/หรือสถานพยาบาลภายใต้การดูแลของรัฐ` (except hospitals, foundations, charities and state medical facilities). A university isn't in the carve-out, so **a CMU slip posted as 9399 earns 0 points**. 8220 / 8299 / 8211 earn normally.
- **NOW**: online rows that get the 5% earn no points (2.1.1); in-store rows earn 1 per ฿25.
- **Lady**: rows in LADY'S FASHIONISTA or LADY'S LIGHT PAY earn no points (2.1.2); tuition is in neither.

### 1.2 Tuition installment: 0% for 4 months on Krungsri Platinum (`family-with-kids-4-months`) · verified

- Page: [เลือกแบ่งจ่ายได้ 0%* 4 เดือน ค่าเทอม ที่สถาบันการศึกษาทั่วไทยที่ร่วมรายการ](https://www.krungsricard.com/th/promotion/family-with-kids-4-months) ("choose 0% for 4 months on tuition at participating institutions nationwide"). The page was edited on 22 Oct (`DocumentModifiedWhen` 2026-10-22T07:33).
- **Period**: spend `1 เม.ย. 69 – 31 ธ.ค. 69`; convert in UCHOOSE (link `kcc.gg/4zqw`) or by calling the card centre **by 31 Dec 69**. Covers both late-Oct and Nov payments.
- **Cards**: `เฉพาะสมาชิกบัตรเครดิต กรุงศรี วีซ่า แพลทินัม และ บัตรเครดิต กรุงศรี มาสเตอร์การ์ด แพลทินัมเท่านั้น` … `ในระบบ Visa และ Master`. The listing JSON's card field for this page holds only `บัตรเครดิต กรุงศรี แพลทินัม`.
  - 🏠 **Krungsri VISA**: qualifies **if it is a Krungsri Visa Platinum**. The household's tier isn't recorded (also open in [[krungsri-group]]) · unverified.
  - 🏠 **Krungsri JCB** ✗ (JCB network), **Krungsri Lady** ✗ (Lady Titanium), **Krungsri NOW** ✗ (NOW Platinum is its own product, not "Krungsri Mastercard Platinum"; reading).
- **What counts — no list of schools.** The title says "participating institutions", but the conditions define them by MCC only: `ยอดใช้จ่ายแบบชำระเต็มจำนวน บนหมวดการศึกษาภายใต้ MCC Code 8211, 8220, 8241 และ 8244 เท่านั้น ที่เป็นร้านค้าในประเทศไทยและเป็นสกุลเงินบาท`. Excluded by name: `Wall Street English, Berlitz, Gymboree และ Brainschool`.
  - **CMU qualifies if it posts as 8220** (or 8211/8241/8244). **Not if it posts as 8299 or 9399.** CMU isn't named anywhere (there is no list) · verified (terms) / unverified (CMU's MCC).
- **Amounts**: slips ≥ ฿1,000 each, combined ≥ ฿5,000; `จำกัดยอดรวมแบ่งจ่ายสูงสุดต่อรายการสูงสุด 100,000 บาท` (≤ ฿100,000 per conversion). A ฿60,000–100,000 semester fits in one conversion.
- **Timing**: `ต้องเป็นรายการที่เกิดขึ้นก่อนวันสรุปยอดบัญชีของเดือนนั้นๆ` and the conversion is made `ก่อนวันสรุปยอดบัญชี 3 วัน ในรอบบัญชีปัจจุบัน` — in the slip's own cycle, at least 3 days before its statement date. The household's Krungsri cycles close on the 5th, so a slip must post and be converted by about the 2nd; a slip dated 3–5 Nov would miss its cycle (reading). Paying between the 6th and the end of a month leaves time.
- **Points**: `สำหรับรายการที่แบ่งชำระเป็น 0% นาน 4 เดือนจะไม่ได้รับคะแนนสะสมปกติ` — **a 0% × 4 conversion forfeits the 0.4% points** (≈ ฿240–400 on ฿60,000–100,000).
- **Longer plans**: more than 4 months at `อัตราดอกเบี้ยพิเศษแบบคงที่ (Flat Rate) เริ่มต้นที่ 0.39% ต่อเดือน` (`Effective Rate` 7.01–16.00% a year), up to 10 months, **and these keep normal points**. 0.39% × 10 months = 3.9% of the slip in interest, against 0.4% of points: a loss.
- No registration code, no SMS number; no cashback.

### 1.3 Points → cashback at education MCCs (`PT26`, "พอยต์คืนคุ้ม") · verified

- Page: [พอยต์คืนคุ้ม แลกพอยต์รับเครดิตเงินคืน 10%*](https://www.krungsricard.com/th/promotion/point-cashback) (1 ม.ค. 69 – 31 ธ.ค. 69). Its MCC list [`MCC-Code-10percent-Y2026_04-08-26.pdf`](https://www.krungsricard.com/KrungsriCreditCard/media/html/MCC-Code-10percent-Y2026_04-08-26.pdf) has an **Education** group: `8211 ELEMENTERY AND SECONDARY SCHOOLS`, `8299 SCHOOLS AND EDUCATIONAL SERVICES`, **`8220 COLLEGES/UNIV/JC/PROFESSION`**, `8241`, `8244`, `8249`, all `THB / ALL`. 9399 isn't on it.
- Mechanic: after a full-payment slip at a listed MCC, redeem in UCHOOSE (search `PT26`) within the same month: 500 → ฿50, 1,000 → ฿100, 5,000 → ฿500; ≤ 500,000 points (฿50,000) **per primary account per day**; credited the next day. **Principal cards only** (`(บัตรหลัก)`): Takumi redeems the account's points against Baiboon's slip.
- Value: **฿0.10 a point**, the same as the standing `point-to-cash` page ("ทุก 1,000 พอยต์ = 100 บาท", 1 Sep 69 – 14 Jan 70). It is a cash-out at the normal rate, **not a gain**: the "10%" in the title means points worth 10% of their count.
- `installment-anything-points` ("ผ่อนอะไร ก็แลกพอยต์ได้ รับเครดิตเงินคืน 10%*", 1 Oct – 31 Dec 69) is the same ฿0.10 a point after any 0% or special-rate installment (USSD `*465*12840*<last 4>*<points>#`, within the month; ≤ 500,000 points per primary account for the campaign; principal only). It isn't a gain either. Its first condition limits it to `ร้านค้าที่ร่วมรายการ` (participating merchants), which contradicts its "any category" headline · verified (terms).
- `epr-kcc-points-to-installments` (3,000 points → 0% × 6, 1 Oct – 31 Dec) covers only hospitals (8062/8099/4119), hotels and airlines, and Shopee / Lazada / TikTok / LINE Shopping, slips ฿5,000–30,000 → **✗ for tuition**.

### 1.4 Krungsri NOW 5% online · verified

- Source: [NOW product page](https://www.krungsricard.com/th/product/creditcard/now) (1 ม.ค. 69 – 31 ธ.ค. 69).
- `รับเครดิตเงินคืน 5% เมื่อซื้อสินค้า/บริการผ่านเว็บไซต์หรือแอปพลิเคชัน`; `จำกัดการให้เครดิตเงินคืน เมื่อใช้จ่ายครบทุกๆ 500 บาท/เซลล์สลิป จำกัดเครดิตเงินคืนสูงสุด 300 บาท/เดือน` — ฿25 per whole ฿500, **฿300 a month per card account** (shared by Takumi and Baiboon; the Bureau's `krungsri_now.py`).
- Excluded: insurance, funds, travel; `การใช้จ่ายผ่าน QR Code`; utilities; transit and fuel; **`ยอดใช้จ่ายสำหรับหน่วยงานราชการ`** per the [MCC list](https://www.krungsricard.com/th/company/mcc) (9211, 9222, 9223, 9311, **9399**, 9405, 7802, with the hospital/charity carve-out); charities; cash; easyBills; Krungsri Smart Plan online installments. **No education exclusion.** Rows that get the 5% earn no points. `ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้`.
- **At CMU**: a card payment on CMU's website or app, posted as 8220/8299, earns **฿300** (the month's cap) if nothing else on the account has used it that month — 0.50% on ฿60,000, 0.30% on ฿100,000, and no points. A QR payment, an in-person swipe or a 9399 posting earns no 5%; an in-person 8220 swipe earns 0.4% in points instead.

### 1.5 ONQ3 online ladder · verified

- Page: [สายช้อปออนไลน์ ช้อปคุ้มมีคืน](https://www.krungsricard.com/th/promotion/online-shopping-cashback), 7 ส.ค. 69 – 30 พ.ย. 69; VISA, JCB, Lady (NOW excluded); registered (`ONQ3`, UCHOOSE).
- It counts **only** `Lazada, Shopee, TikTok Shop, LINE SHOPPING` and the e-wallet apps `TrueMoney, LINE Pay, ShopeePay`; ฿40 / ฿170 / ฿350 at ฿3,000 / 15,000 / 30,000 a month per primary account (principal + supplements pooled), ≤ ฿1,400 for the campaign; credited within 90 days to the principal.
- **A tuition card payment on CMU's own site doesn't count.** It counts only if CMU takes TrueMoney, LINE Pay or ShopeePay and Baiboon pays through one of them with Krungsri VISA/JCB/Lady: then ฿350 (0.58% at ฿60,000) if the month's ladder isn't already at the top tier. A TrueMoney-linked payment earns **no Krungsri points** (from 1 Aug 2026). Whether CMU takes any of these wallets is the CMU researcher's question.

### 1.6 Course-provider pages (not CMU) · verified

`education-installment` (`EDU2`, to 30 Oct), `ecc-tutor-house-star-maker` (`EDU3`, 1 Oct 69 – 31 Jan 70, SMS 06 1404 5555), `new-education-world`, `british-council`, `lets-mandarin`, `wall-street-installment`, `lnlingua-installment`, `go-smart` (to 31 Oct), and the education shops of `scan-installment` (Wall Street English, English Park, ECC, Bangkok Tutor House, Star Maker, Quality Kids) are **named tutoring and language schools**, 0% for 6–10 months plus cashback up to ฿35,000–45,000. **No university is on any of them.**

## 2. First Choice

One account: Takumi's Krungsri First Choice Visa Platinum with Baiboon's and Nuta's supplements, pooled for every campaign ([[../../promotions/first-choice-2026h2]]).

### 2.1 NW4 counts tuition · verified + household

- Page: [รูดก็ได้เงินคืน กดก็ได้แคชเบ็ค](https://www.firstchoice.co.th/promotion/firstchoice-cashback), 1 ต.ค. 69 – 31 ธ.ค. 69; registered (`NW4`, SMS 081-256-3333; the household was also auto-enrolled for Oct–Dec).
- Tiers, full-payment spend per calendar month, principal + supplements pooled: ฿5,000–9,999 → ฿50; **every whole ฿10,000 → ฿200 (2%)**; ≤ ฿2,000 a month and ≤ ฿6,000 for the campaign per primary account; credited to the principal.
- **Education isn't excluded, and there is no per-slip cap.** The exclusion list names marketplaces (→ ON4), delivery (→ DLV3), travel (→ TR3), insurance (→ IS4), MCC 5199, supermarket and fuel spend above ฿30,000 a month each, utilities 4900/9402, gold, financial services, all foreign spend, e-wallet top-ups, crypto, `รายการหักบัญชีอัตโนมัติรายเดือนรายปี` (monthly or yearly auto-debits), and:
  - `รายการที่เกี่ยวกับการชำระค่าใช้จ่ายที่เกี่ยวข้องกับหน่วยงานราชการ เช่น การชำระค่าภาษีต่างๆ หรือค่าใช้จ่ายต่างๆของหน่วยงานราชการ … หรือรายการที่เข้า MCC 9399, 9405 และ 7800` — **a CMU slip posted as 9399 gets no NW4.** Whether a public university's 8220 slip could be read as "expenses of a government agency" is the bank's call; the clause names MCCs, and 8220 isn't one (reading).
- **Headroom (household, Promotion Bureau `2026M10 — NW4 cb 2%`, read 22 Oct):** ฿18,161.88 pooled so far in October, ฿200 earned. A tuition slip in **October** adds: ฿61,260 → ฿79,421.88 → 7 steps = ฿1,400, **+฿1,200**; ฿102,100 → ฿120,261.88 → capped ฿2,000, **+฿1,800**. In **November** from zero: ฿61,260 → **฿1,200**; ฿102,100 → **฿2,000** (the cap, which leaves nothing for the rest of the household's November First Choice spend). The campaign cap (฿6,000) isn't in reach.
- **U PLAN keeps NW4.** A charge converted afterwards through U PLAN still counts toward NW4, once, as the full-amount slip (user, 2026-10-03; sure for 0% plans, [[../../concepts/installment-reward-campaigns]]) · household.

### 2.2 Points · verified

- `ยอดใช้จ่าย (รูดเต็มจำนวนและผ่อนสินค้า) ทุก 25 บาท รับคะแนนสะสม 1 คะแนน`, valid 5 years ([First Choice Rewards](https://www.firstchoice.co.th/firstchoice-rewards)). Burns ≈ ฿0.09–0.10 a point (330 → ฿30 Amazon, 300 → ฿30 7-Eleven, 1,000 → ฿100 donation) → **≈ 0.36–0.40%**.
- The four exclusion notices on that page ([MCC notice](https://www.firstchoice.co.th/getattachment/b040a615-8af1-476e-bc2c-655d419a1088/Notice-of-Exemption-from-Accumulated-Points-under-the-Designated-MCC.pdf): transit 4111/4112/4131/4784, EEA, China; AIA; 7-Eleven/TrueMoney and a fuel cap; MCC 5199) name **no education and no government MCC** — First Choice points even survive a 9399 posting.
- No points-for-tuition burn exists for this card (XU's 18% points-to-cashback is XU-only).

### 2.3 U PLAN "0% สั่งได้ทุกอย่าง" — 0% for 3 months on any slip · verified

- Page: [สมาร์ททุกการใช้จ่าย 0% สั่งได้ทุกอย่าง](https://www.firstchoice.co.th/promotion/epr-0-3month) (no end date shown; a standing UCHOOSE service). First Choice Visa Platinum and XU.
- Any full-amount slip ≥ ฿500, combined ≥ ฿3,000, dated before the statement date, converted in UCHOOSE (`แบ่งชำระรายเดือน` → `0% สั่งได้นาน 3 เดือน`) **by 20:00 on the statement date** of the current cycle. No upper limit stated. No education list needed: tuition qualifies like anything else.
- **Converted rows earn no First Choice points** (`จะไม่ได้รับคะแนนสะสมกรุงศรีเฟิร์สช้อยส์ รีวอร์ด`); NW4 is kept (§2.1). Excluded from conversion: business spend, funds/unit-link, utilities and auto-debits.
- Longer plans: 0.39% a month flat for 3–10 months (7.01–15.83% a year), done before the due date.
- The `epr-0-6month` "พอยท์ช่วยผ่อน" (3,000 points → 0% × 6) covers private hospitals, fashion and beauty, hotels and airlines, pets, sports, concerts → ✗ for tuition.
- The `epr-hospital` U PLAN (0% × 3 at 11 public hospitals incl. Maharaj Nakorn Chiang Mai) is medical only.

### 2.4 Nothing education-specific

The First Choice category "การศึกษา แว่นตา" holds only Wall Street English (0% up to 24 months) among education merchants. BLUE PLUS `BPCB` (฿500 per ฿100,000 from ฿300,000 in a month, [[../../promotions/first-choice-privilege-2026]]) needs a ฿300,000 month, out of reach for one semester.

---

## 3. Central The 1 (REDZ)

Baiboon and Takumi both hold REDZ (Krungsri Consumer, issued by `บริษัท เจเนอรัล คาร์ด เซอร์วิสเซส จำกัด`). The `gcspromotion` list held **186 promotions** on 22 Oct.

### 3.1 `ED1` "Education" — cashback per tuition slip at any educational institution · verified

- Promotion `education-202608` (open on the site as [centralthe1card.com/promotion?modalId=education-202608](https://www.centralthe1card.com/promotion?modalId=education-202608)); poster [`OL_Education_Jul26-1024-(1).webp`](https://www.centralthe1card.com/getattachment/48e4e6fa-5703-4c0f-9462-1e0d546d4991/OL_Education_Jul26-1024-(1).webp). Headline: `รับเครดิตเงินคืนสูงสุด 30,000 บาท* ที่ หมวดการศึกษาทุกที่ ทั่วไทย`; poster: `รับคืนคุ้ม ทั้งพอยท์และเครดิตเงินคืน ที่สถาบันการศึกษาทั่วไทย กับบัตรเครดิต เซ็นทรัล เดอะวัน` ("points and cashback at educational institutions nationwide").
- **Period: 1 ส.ค. 69 – 31 ธ.ค. 69** (spend). Cards: Central The 1 credit cards (`red|luxe|black|theblack`), so 🏠 **REDZ qualifies**.
- **Tiers, per full-payment slip** (`ยอดใช้จ่ายแบบเต็มจำนวน/เซลล์สลิป`):

  | Slip | Cashback | On a ฿60,000 / ฿100,000 tuition |
  |---|---|---|
  | ฿20,000–59,999 | ฿150 | — |
  | **฿60,000–149,999** | **฿700** | 1.17% / 0.70% |
  | ฿150,000–249,999 | ฿2,500 | — |
  | ≥ ฿250,000 | ฿6,000 | — |

- **Caps**: ฿6,000 per primary account a month, ฿30,000 per primary account for the campaign; supplements pool with the principal (Takumi's REDZ account); credited to the principal within 15 days of the merchant's settlement.
- **Registration**: once, `ลงทะเบียนภายในวันที่ทำรายการ ครั้งแรกครั้งเดียว` — in UCHOOSE or SMS **`ED1 <16-digit card number>` → 081-278-2222**, on or before the day of the payment; only spend from the registration onward counts. **Not in the household's registration lists** ([[../campaigns]]): register before paying.
- **Excluded**: `ยกเว้นรายการ เปลี่ยนยอดรูดเต็มเป็นยอดผ่อนชำระด้วยอัตราดอกเบี้ย 0%` — converting the slip to a 0% plan loses `ED1`. Only "0%" plans are named; Central The 1's U PLAN charges interest (§3.3), so a U PLAN conversion isn't named (reading, unconfirmed).
- **What counts as "education"**: no MCC list and no list of institutions is published. "หมวดการศึกษา … ทุกที่ทั่วไทย" reads as the education MCC group (8211–8299). **CMU qualifies if it posts as an education MCC; a 9399 posting very likely doesn't** (reading). With CMU's 2.1% fee inside the slip, any tuition from ฿58,766 to ฿146,914 lands in the ฿700 tier; with the fee as a separate slip, the tuition itself must be ฿60,000–149,999.
- The terms mention `คะแนนเดอะวันพิเศษ` (extra The 1 points) in condition 3, but the poster shows no points tier; read it as the card's normal points (below) · unverified.

### 3.2 REDZ points · verified

- [REDZ product page](https://www.centralthe1card.com/Product-Listing/product-detail-redz): `ทุกยอดใช้จ่าย 25 บาทต่อเซลล์สลิป ผ่าน Central The 1 REDZ Credit Card รับ 1 คะแนนเดอะวัน` outside the Central group → **0.5%** at ฿0.125 a point; supplement points go to the principal.
- Excluded: cash, Pay All, Payment on Call terms, 6211, 4900, **9211, 9222, 9223, 9311, 9399, 9402, 9405** (no hospital or education carve-out), transit, 2c2p e-wallet top-ups, AIA, fees, tax refunds, 7-Eleven and TrueMoney-linked spend (from 1 Aug 2026), EEA/China/foreign-THB, fuel above ฿50,000 a month. **No education exclusion.**

### 3.3 Installments · verified

- **No 0% plan for tuition at CMU.** The 0% pages name schools: `edu-sisb0-202604` (0% up to 6 months at SISB campuses, including `โรงเรียนนานาชาติสิงคโปร์เชียงใหม่`), `harrow-202601` (0% × 4), `rugby-202604` (0% × 6). `qr-Installment-202605` lists an "Education" category of partner tutoring schools.
- `u-plan-epr-202601` "U PLAN เปลี่ยนยอดรูดเต็ม ทุกการใช้จ่าย เป็นแบ่งชำระ 0.39%* นาน 10 เดือน": any slip ≥ ฿3,000 (or settled slips ≥ ฿500 combined to ≥ ฿3,000), flat 0.39% a month for 3–10 months (7.01–15.87% a year), converted before the due date, 1 Jan – 31 Dec 2026. Over 10 months that is 3.9% of the slip.
- `u-plan-202601` (0% × 3) is the 11-public-hospital medical U PLAN only.

---

## 4. Lotus's (Lotus's Beyond)

Takumi's Lotus's Beyond with Baiboon's supplement (issued by `บริษัท โลตัสส์ มันนี่ เซอร์วิสเซส จำกัด`); campaigns pool on Takumi's account. The sitemap held 1,614 URLs on 22 Oct.

### 4.1 Coins · verified

- [Coin calculation](https://www.lotussmoney.com/coin-calculation): `ทุก 50 บาท รับสูงสุด 0.25 คอยน์ เมื่อมียอดใช้จ่ายที่ร้านค้าอื่นๆ ทั่วโลก ครบทุก 50 บาท/เซลล์สลิป`; `1 โลตัสมันนี่คอยน์ = 1 บาท` (Lotus's cash coupon) → **0.5%** ([[../../cards/lotuss-beyond]]).
- Excluded: Bangchak, funds, unit-link, AIA, FX, foreign-THB, utilities, **`รายการหน่วยงานราชการ`** (government, no MCC list), transit, e-wallet top-ups, crypto, **`รายการผ่อนชำระสินค้า`** (installments), cash, fees. **No education exclusion.** A 9399 posting very likely earns nothing.

### 4.2 Campaigns · verified

- **LBS3** ([page](https://www.lotussmoney.com/promotion/credit-card/shopping/cashback-nationwide-bigticket)): home and building materials, electrical appliances, car service, Makro → ✗.
- **SMP1 / SMT2** ([page](https://www.lotussmoney.com/promotion/credit-card/shopping/cashback-nationwide)): department stores, fashion, cosmetics, mobile/IT and phone bills, bookshops and stationery (SE-ED, Naiin, Asia Books, Nanmee, Kinokuniya, B2S, OfficeMate …) → ✗ for tuition (a textbook bought at a bookshop would count).
- **Invited-only Q4 pages** (`เฉพาะสมาชิกบัตรที่ได้รับการเรียนเชิญ`, no registration, 1 Oct – 31 Dec, months Oct / Nov / Dec): **neither education nor government is excluded**. Both exclude `รายการผ่อนชำระ` (installments), e-wallets, hospitals, supermarkets, fuel, insurance, gold, funds, utilities and auto-debits.
  - [`small-ticket-a-q4-26`](https://www.lotussmoney.com/promotion-segment/credit-card/small-ticket-a-q4-26): per slip ฿125 (฿5,000–9,999), ฿250 (฿10,000–49,999), **฿1,250 (≥ ฿50,000)**; each tier at most twice a month; ≤ ฿3,250 a month, ≤ ฿9,750 per primary account.
  - [`small-ticket-b-q4-26`](https://www.lotussmoney.com/promotion-segment/credit-card/small-ticket-b-q4-26): ฿250 (฿10,000–19,999), ฿500 (฿20,000–49,999), **฿1,250 (≥ ฿50,000)**; ≤ ฿4,000 a month, ≤ ฿12,000.
  - **If Takumi's Lotus's account is invited to either, a tuition slip ≥ ฿50,000 earns ฿1,250** (2.08% on ฿60,000, 1.25% on ฿100,000), credited within 60 days after the campaign ends. Invitation shows only in UCHOOSE · verified (terms) / unverified (invitation).
  - Smaller invited pages: `shopping-matching-merchant-q426-a…d` (฿100 per ฿8,000, ≤ ฿200 a month), `happy-payday-oct26` (25–31 Oct, register from 10:00 on 25 Oct, first 2,000: ≥ ฿4,000 → ฿200), `shopping-shopplearn-a…e-q426` (monthly ladders).
- **Installments**: Lotus's education pages are course providers and SISB only (`การศึกษา` category: ECC, Wall Street English, Let's Mandarin, `go-smart`, `ผ่อนค่าเทอม 0%* ที่ SISB` 3 or 6 months). `lifestyle` (LS6, to 31 Oct) and `smart-down-payment` (SDP) need participating merchants. **No Lotus's tuition installment covers CMU.**

## 5. KTC

(being written)

## 6. AEON

(being written)

## 7. Students and parents

(being written)

## What couldn't be found

(being written)

## Site methods

(being written)
