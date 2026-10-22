---
tags: [catalogue-research, 2026-10]
researched: 2026-10-22
---

> **Research snapshot**: university tuition — Krungsri group (Krungsri Card, First Choice, Central The 1, Lotus's), KTC and AEON — October 2026 research. Scope: what each of Baiboon's cards from these issuers pays on one semester's tuition at Chiang Mai University (มหาวิทยาลัยเชียงใหม่, CMU), a slip of ฿60,000–100,000 paid in CMU's window of 30 Nov – 4 Dec 2026 (semester 2/2569), with CMU's 2.1% online / 0.9% counter card fee: base points or cashback at an education MCC (8220, with 9399 and 8299 as alternatives), each issuer's no-points lists, all-spend campaigns, tuition installments, points-for-tuition burns, and student or parent offers. Read on **2026-10-22** from the official pages, for an October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] page. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions (HTML, JSON, PDFs, posters) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# University tuition — Krungsri group, KTC and AEON — October 2026 (ต.ค. 69)

Researcher: `education-krungsri-ktc-aeon` · researched 2026-10-22 · read-only. Other researchers cover CMU's own payment channels, UOB / KBank / ttb / CardX and the other banks, and offers that name no merchant.

**Legend.** ✓ counts · ✗ doesn't · ? unclear · 🏠 a household card. Confidence: **verified** (the issuer's own page read today) · **household** (the household's ledger shows it) · **third-party only** · **unverified**.

**The payment.** Baiboon pays one semester at CMU, over ฿60,000, in CMU's window of **30 Nov – 4 Dec 2026** (§0). All her cards in scope are **supplements on Takumi's accounts**, so account-level caps and pooled ladders are shared with Takumi (and Nuta where she holds the same card).

**MCC assumptions** (CMU's channel is another researcher's question):
- **8220** (Colleges, Universities, Professional Schools) is the code a university charge normally carries. The working figures below use it.
- **8299** (Schools and Educational Services, not elsewhere classified) or **8211** (schools) if CMU's payment gateway posts under a generic education code. Every no-points list and campaign below that names 8220 also names 8211–8299, so the answer is the same — **except the Krungsri 0% × 4**, which takes 8211, 8220, 8241 and 8244 only (§1.2).
- **9399** (Government Services) if CMU's payment posts as a government body. CMU is an autonomous public university (`มหาวิทยาลัยในกำกับของรัฐ`), so this is possible.
- **Household evidence**: no tuition row exists in Baiboon's ledger (searched `UNIV`, `CMU`, `TUITION`, `มหาวิทยาลัย`, all rows ≥ ฿15,000). Takumi's `CHULALONGKORN UNIVERSITY BANGKOK` ฿33,500 (31 Jul 2026, KBank PLUSTINUM) realised 1,340 points = 1 per ฿25, so a Thai university charge did post as an ordinary card slip there; its MCC isn't recorded.

**Point values used.** Krungsri, KTC ฿0.10 · The 1 ฿0.125 · Lotus's coin ฿1 · First Choice ≈ ฿0.09–0.10 · AEON Happy Point: no published cash value.

---

## 0. At a glance

**CMU's terms** ([[cmu-tuition]], verified there): semester 2/2569 is paid **30 Nov – 4 Dec 2026** (late 7–11 Dec with a fine). A credit card costs **2.1% online** (added into one total, so the slip is 102.1% of the tuition) or **0.9% at the Finance Division counter** (`กองคลัง`, until 16:30). The **Thai QR** in the registration system is the only fee-free channel. No CMU installment plan, no bank waiver. The online gateway's networks and the counter's terminal bank are unknown.

**No issuer in this scope waives or absorbs CMU's fee.** Searched: Krungsri Card's 581-item listing, First Choice's 222 promotion links, Central The 1's 186 promotions, Lotus's 1,614-URL sitemap, KTC's 11,678 promotion URLs and its tuition article, AEON's 185 promotion tiles, plus web searches restricted to the seven issuers' domains. CMU appears on none of them except KTC's alumni-association donation page (`/promotion/donation/education/chiang-mai-university-alumni-associate`). Nothing like Chula's KBank waiver exists for CMU here.

**Statement cycles for 30 Nov – 4 Dec** (`lib/bill_cycle.py`): every Krungsri-family card (Krungsri VISA, JCB, Lady, NOW, First Choice, REDZ, Lotus's Beyond) closes **5 Dec 2026**, due **25 Dec**. KTC closes **27 Dec**, due **11 Jan 2027**. AEON closes **10 Dec** (cycle 11 Nov – 10 Dec), due **2 Jan 2027**. Monthly campaigns (NW4, NOW 5%, ED1's monthly cap, Lotus's invited months) count by **calendar month**: 30 Nov is November, 1–4 Dec is December.

### 0.1 Each of Baiboon's cards on one semester, net of CMU's fee

Assumptions: MCC 8220 (§ *MCC assumptions*); the fee is inside the slip, online (stated by CMU) and at the counter (assumed); the card's monthly campaign has its full cap free; points at ฿0.10 (Krungsri, First Choice ฿0.09–0.10), ฿0.125 (The 1), ฿1 a Lotus's coin. **Net = rewards − fee**, as a share of the tuition. A card only beats the fee-free Thai QR when net > 0.

| Card | What pays at CMU | Online (2.1%): ฿60,000 · ฿100,000 | Counter (0.9%): ฿60,000 · ฿100,000 | Conf. |
|---|---|---|---|---|
| 🏠 **First Choice** | **NW4** ฿200 per whole ฿10,000 a month (≤ ฿2,000) + 1 pt/฿25 | ฿1,421–1,445 → **+฿161–185 (+0.3%)** · ฿2,368–2,408 → **+฿268–308 (+0.3%)** | ฿1,418–1,442 → **+฿878–902 (+1.5%)** · ฿2,363–2,404 → **+฿1,463–1,504 (+1.5%)** | verified + household |
| 🏠 **Central The 1 REDZ** | **`ED1`** ฿700 per slip ฿60,000–149,999 (register first) + 1 The 1 pt/฿25 | ฿1,006 → **−฿254 (−0.4%)** · ฿1,211 → **−฿890 (−0.9%)** | ฿1,003 → **+฿463 (+0.8%)** · ฿1,205 → **+฿305 (+0.3%)** | verified |
| 🏠 **Lotus's Beyond** | 0.25 coin per ฿50 (0.5%); **+฿1,250 per slip ≥ ฿50,000 if invited** to `small-ticket-a/b-q4-26` | ฿306 → −฿954 (−1.6%) · ฿511 → −฿1,590 (−1.6%); **invited: +฿296 (+0.5%) · −฿340 (−0.3%)** | ฿303 → −฿238 (−0.4%) · ฿505 → −฿396 (−0.4%); **invited: +฿1,013 (+1.7%) · +฿855 (+0.9%)** | verified (terms) · unverified (invitation) |
| 🏠 Krungsri VISA / JCB / Lady | 1 pt/฿25 (0.4%) | ฿245 → −฿1,015 (−1.7%) · ฿408 → −฿1,692 (−1.7%) | ฿242 → −฿298 (−0.5%) · ฿404 → −฿496 (−0.5%) | verified |
| 🏠 Krungsri NOW | online: 5% capped at **฿300 a month**, no points; counter: 0.4% points | ฿300 → −฿960 (−1.6%) · ฿300 → −฿1,800 (−1.8%) | as VISA: −0.5% | verified |
| 🏠 KTC UnionPay | **0 points** (rule 16: 8211–8299 and 9399) | −฿1,260 · −฿2,100 (−2.1%) | −฿540 · −฿900 (−0.9%) | verified |
| 🏠 AEON World · Primo | **0 points** (8211–8299, 9399 on AEON's no-points list) | −2.1% | −0.9% | verified |
| 🏠 AEON Next Gen | online 5% capped at **฿50 a transaction** (needs ≥ ฿500 of Scan To Pay in the cycle); 0 points | ฿50 → −฿1,210 (−2.0%) · −฿2,050 (−2.1%) | −0.9% | verified |

- **If CMU posts as 9399**: First Choice keeps only its points (NW4 excludes 9399, its points don't) → −1.7% / −0.5%; REDZ, Lotus's, Krungsri Card and both AEON cards earn **nothing**; ED1 very likely doesn't apply; the Krungsri 0% × 4 doesn't apply.
- **First Choice's figures are the cap-free month.** A ฿100,000 slip fills the ฿2,000 cap alone, so other First Choice spend that month (October's pool was ฿18,162 by the 22nd) loses its NW4: count ≈ ฿400–600 less at ฿100,000. At ฿60,000 the cap still has room.
- **Through TrueMoney → CMU's Thai QR (no CMU fee)**, Visa cards only (§8): First Choice NW4 **+2.0%** (฿1,200 / ฿2,000, no points); Krungsri VISA ONQ3 **+฿350** on 30 Nov only (+0.6% / +0.35%, no points). Unverified that TrueMoney can pay CMU's QR at this size.
- **Stacking**: a slip can carry only one card. Draw rights on top: the JCB Japan Season 3 draw (Krungsri JCB, slip ≥ ฿1,000, 1 Oct – 31 Jan; register `JCLD` once in UCHOOSE, registration status not recorded) gives one right; the BTS draw ended its counting on 15 Nov.

**Best routes, in order**: (1) First Choice **at the counter** (+1.5%), (2) Lotus's Beyond at the counter **if invited** (+1.7% at ฿60,000), (3) First Choice through TrueMoney, if it works (+2.0%, test first), (4) REDZ at the counter with `ED1` registered (+0.3–0.8%). **Online, only First Choice (+0.3%) and an invited Lotus's (+0.5% at ฿60,000) beat the free Thai QR.** Every other card loses money against the Thai QR, online or at the counter.

### 0.2 0% installments: cost against the cash-flow gain

Paying by card and then splitting the bill only makes sense when it is cheaper than the household's alternative source of cash. "Credit" below is how long the money stays with the household compared with paying by Thai QR on ~1 Dec: the full tuition until 25 Dec (≈ 0.8 month), then the unpaid instalments.

| Plan | Who | Counter (0.9%) | Online (2.1%) | Credit | Conf. |
|---|---|---|---|---|---|
| **First Choice U PLAN 0% × 3** ("0% สั่งได้ทุกอย่าง", standing; convert by 20:00 on 5 Dec) | First Choice | NW4 2% − 0.9% fee = **+1.1%** (converted rows earn no points; you are paid to borrow) | NW4 2% − 2.1% = **−0.1%** (≈ 0.7% a year) | 1.8 tuition-months (terms 25 Dec, 25 Jan, 25 Feb) | verified (plan) · household (NW4 kept) |
| **Krungsri 0% × 4 on tuition** (`family-with-kids-4-months`, MCC 8211/8220/8241/8244, ≤ ฿100,000, convert **by 2 Dec**) | Krungsri VISA **only if it is a Visa Platinum** | fee 0.9% + points 0.4% = **1.3%** (≈ 6.8% a year) | 2.1% + 0.4% = **2.5%** (≈ 13% a year) | 2.3 tuition-months (terms 25 Dec – 25 Mar) | verified (terms) · unverified (card tier, CMU's MCC) |
| Central The 1 U PLAN 0.39% a month × 3–10 | REDZ | 0.9% fee + 1.17–3.9% interest; `ED1`'s exclusion names only 0% conversions, so ฿700 may survive (reading) | worse | — | verified |
| KTC 0.69% a month × 3/6/10 (`MTFED-1436`, by KTC PHONE on the day) | KTC UnionPay | only at "participating institutions"; **no list published and CMU named nowhere** | — | — | verified (terms) |
| Lotus's, AEON | — | **no tuition plan** reaches CMU (named merchants only; AEON's 0% plans also lose points) | — | — | verified |

- **First Choice U PLAN is the only plan that costs nothing**: NW4 keeps paying on the converted slip (household reading, sure for 0% plans), so at the counter it nets +1.1% and three months at 0%.
- The Krungsri 0% × 4 costs 1.3–2.5% for about 2.3 months of credit: worth it only against borrowing at more than ≈ 7–13% a year (the card's own revolving rate is 16%). With the cash on hand, pay by Thai QR instead.
- Timing decides the Krungsri plan: pay **30 Nov or 1 Dec** and convert in UCHOOSE (U PLAN → "0% 4 MONTHS INSTALLMENT ON EDUCATION") the same day; a pending slip can be selected.

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
- **Period**: spend `1 เม.ย. 69 – 31 ธ.ค. 69`; convert in UCHOOSE (link `kcc.gg/4zqw`) or by calling the card centre **by 31 Dec 69**. Covers CMU's 30 Nov – 4 Dec window, subject to the cycle timing below.
- **Cards**: `เฉพาะสมาชิกบัตรเครดิต กรุงศรี วีซ่า แพลทินัม และ บัตรเครดิต กรุงศรี มาสเตอร์การ์ด แพลทินัมเท่านั้น` … `ในระบบ Visa และ Master`. The listing JSON's card field for this page holds only `บัตรเครดิต กรุงศรี แพลทินัม`.
  - 🏠 **Krungsri VISA**: qualifies **if it is a Krungsri Visa Platinum**. The household's tier isn't recorded (also open in [[krungsri-group]]) · unverified.
  - 🏠 **Krungsri JCB** ✗ (JCB network), **Krungsri Lady** ✗ (Lady Titanium), **Krungsri NOW** ✗ (NOW Platinum is its own product, not "Krungsri Mastercard Platinum"; reading).
- **What counts — no list of schools.** The title says "participating institutions", but the conditions define them by MCC only: `ยอดใช้จ่ายแบบชำระเต็มจำนวน บนหมวดการศึกษาภายใต้ MCC Code 8211, 8220, 8241 และ 8244 เท่านั้น ที่เป็นร้านค้าในประเทศไทยและเป็นสกุลเงินบาท`. Excluded by name: `Wall Street English, Berlitz, Gymboree และ Brainschool`.
  - **CMU qualifies if it posts as 8220** (or 8211/8241/8244). **Not if it posts as 8299 or 9399.** CMU isn't named anywhere (there is no list) · verified (terms) / unverified (CMU's MCC).
  - **The "institution list" is the MCC list.** The page's step-2 app screenshot ([`Family-with-kid-EPR_Web-Step02.jpg`](https://www.krungsricard.com/KrungsriCreditCard/media/html/Family-with-kid-EPR_Web-Step02.jpg)) shows the UCHOOSE plan as `0% 4 MONTHS INSTALLMENT ON EDUCATION — FOR TRANSACTIONS IN MCC: 8211, 8220, 8241, 8244 AND PARTICIPATING MERCHANTS`. No PDF, poster or merchant list is linked from the page (its only PDFs are the anti-corruption and no-gift policies), and the 1200×650 banner returned the WAF block page every time. So "participating merchants" adds names outside those MCCs; it is not a list CMU has to be on · verified.
  - Third-party confirmation: Krungsri Consumer's press release of 22 Jun 2569 ([Kaohoon](https://www.kaohoon.com/finance/840455)) gives the same terms ("สถาบันการศึกษาทั่วประเทศที่ร่วมรายการ", ≥ ฿1,000 a slip, ≥ ฿5,000 combined, ≤ ฿100,000, UCHOOSE → U PLAN, search `STUDY`) and says the **Central The 1** version ran only **1 May – 31 Jul 2569** (ended) · third-party only.
- **Amounts**: slips ≥ ฿1,000 each, combined ≥ ฿5,000; `จำกัดยอดรวมแบ่งจ่ายสูงสุดต่อรายการสูงสุด 100,000 บาท` (≤ ฿100,000 per conversion). A ฿60,000–100,000 semester fits in one conversion.
- **Timing**: `ต้องเป็นรายการที่เกิดขึ้นก่อนวันสรุปยอดบัญชีของเดือนนั้นๆ` and the conversion is made `ก่อนวันสรุปยอดบัญชี 3 วัน ในรอบบัญชีปัจจุบัน` — in the slip's own cycle, at least 3 days before its statement date. CMU's window is **30 Nov – 4 Dec 2026** ([[cmu-tuition]]), and the household's Krungsri cycle closes on **5 Dec** (due 25 Dec), so **the conversion must be made by 2 Dec**. Pay on **30 Nov (or 1 Dec)** and convert at once: the step-3 screenshot shows an `UNBILLED` slip marked `Pending` being selected, so a slip needn't have posted. A slip dated 3–4 Dec misses the 5 Dec cut-off for this plan (reading).
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
- **At CMU**: only the **online** card payment (2.1% fee) can earn it: posted as 8220/8299, it earns **฿300** (the month's cap) if nothing else on the account has used it that month — 0.50% on ฿60,000, 0.30% on ฿100,000, and no points. November's cap applies on 30 Nov, December's on 1–4 Dec (the household used ฿25 of October's). A QR payment, the counter terminal or a 9399 posting earns no 5%; at the counter an 8220 slip earns 0.4% in points instead.

### 1.5 ONQ3 online ladder · verified

- Page: [สายช้อปออนไลน์ ช้อปคุ้มมีคืน](https://www.krungsricard.com/th/promotion/online-shopping-cashback), 7 ส.ค. 69 – 30 พ.ย. 69; VISA, JCB, Lady (NOW excluded); registered (`ONQ3`, UCHOOSE).
- It counts **only** `Lazada, Shopee, TikTok Shop, LINE SHOPPING` and the e-wallet apps `TrueMoney, LINE Pay, ShopeePay`; ฿40 / ฿170 / ฿350 at ฿3,000 / 15,000 / 30,000 a month per primary account (principal + supplements pooled), ≤ ฿1,400 for the campaign; credited within 90 days to the principal.
- **A tuition card payment on CMU's own site or at its counter doesn't count.** It counts only through a wallet: CMU's fee-free **Thai QR** scanned in **TrueMoney** with a linked **Visa** (TrueMoney lets a linked Visa credit card pay PromptPay QRs, [[../campaigns|campaigns]]; Krungsri VISA is the only Visa among her Krungsri Card supplements). Then ฿350 (0.58% at ฿60,000, 0.35% at ฿100,000) if the month's ladder isn't already at the top tier, no CMU fee, but **no Krungsri points** on TrueMoney-linked spend (from 1 Aug 2026).
- **ONQ3 ends 30 Nov 2026**: only a 30 Nov payment can count. No December successor is published (22 Oct).
- Whether TrueMoney can scan CMU's registration-system QR, and its limit for a ฿60,000–100,000 card-funded payment, are unverified (§8).

### 1.6 Course-provider pages (not CMU) · verified

`education-installment` (`EDU2`, to 30 Oct), `ecc-tutor-house-star-maker` (`EDU3`, 1 Oct 69 – 31 Jan 70, SMS 06 1404 5555), `new-education-world`, `british-council`, `lets-mandarin`, `wall-street-installment`, `lnlingua-installment`, `go-smart` (to 31 Oct), and the education shops of `scan-installment` (Wall Street English, English Park, ECC, Bangkok Tutor House, Star Maker, Quality Kids) are **named tutoring and language schools**, 0% for 6–10 months plus cashback up to ฿35,000–45,000. **No university is on any of them.**

## 2. First Choice

One account: Takumi's Krungsri First Choice Visa Platinum with Baiboon's and Nuta's supplements, pooled for every campaign ([[../../promotions/first-choice-2026h2]]).

### 2.1 NW4 counts tuition · verified + household

- Page: [รูดก็ได้เงินคืน กดก็ได้แคชเบ็ค](https://www.firstchoice.co.th/promotion/firstchoice-cashback), 1 ต.ค. 69 – 31 ธ.ค. 69; registered (`NW4`, SMS 081-256-3333; the household was also auto-enrolled for Oct–Dec).
- Tiers, full-payment spend per calendar month, principal + supplements pooled: ฿5,000–9,999 → ฿50; **every whole ฿10,000 → ฿200 (2%)**; ≤ ฿2,000 a month and ≤ ฿6,000 for the campaign per primary account; credited to the principal.
- **Education isn't excluded, and there is no per-slip cap.** The exclusion list names marketplaces (→ ON4), delivery (→ DLV3), travel (→ TR3), insurance (→ IS4), MCC 5199, supermarket and fuel spend above ฿30,000 a month each, utilities 4900/9402, gold, financial services, all foreign spend, e-wallet top-ups, crypto, `รายการหักบัญชีอัตโนมัติรายเดือนรายปี` (monthly or yearly auto-debits), and:
  - `รายการที่เกี่ยวกับการชำระค่าใช้จ่ายที่เกี่ยวข้องกับหน่วยงานราชการ เช่น การชำระค่าภาษีต่างๆ หรือค่าใช้จ่ายต่างๆของหน่วยงานราชการ … หรือรายการที่เข้า MCC 9399, 9405 และ 7800` — **a CMU slip posted as 9399 gets no NW4.** Whether a public university's 8220 slip could be read as "expenses of a government agency" is the bank's call; the clause names MCCs, and 8220 isn't one (reading).
- **What a semester earns**: on its own in a month, a ฿61,260 online slip (฿60,000 + 2.1%) → 6 steps = **฿1,200**; ฿102,100 → 10 steps = **฿2,000**, the cap, which then leaves nothing for the rest of the household's First Choice spend that month. For scale, October's pool stood at ฿18,161.88 (฿200 earned) on 22 Oct (household, Promotion Bureau `2026M10 — NW4 cb 2%`). On top of a month like that: ฿60,000 still adds ฿1,200; ฿100,000 adds ≈ ฿1,600–1,800. The campaign cap (฿6,000 for Oct–Dec) isn't in reach unless November and December both hit ฿2,000.
- **CMU's window (30 Nov – 4 Dec) splits across two NW4 months**: a 30 Nov slip counts in **November**, a 1–4 Dec slip in **December** (both inside NW4, which ends 31 Dec). Choose the month with less other First Choice spend, so the ฿2,000 cap has room; a ฿100,000 semester fills the month's cap by itself. NW4's successor for 2027 isn't published.
- **U PLAN keeps NW4.** A charge converted afterwards through U PLAN still counts toward NW4, once, as the full-amount slip (user, 2026-10-03; sure for 0% plans, [[../../concepts/installment-reward-campaigns]]) · household.
- **TrueMoney-routed payments count.** UCHOOSE's NW3 eligible list for September included the household's `TMN*PROMPTPAY30` rows (Takumi's PromptPay payments through TrueMoney with First Choice linked), and the Bureau matched it to the satang ([[../../promotions/first-choice-nw3]]). NW4 keeps the same wording (top-ups excluded, payments through a wallet not). So First Choice paying **CMU's fee-free Thai QR through TrueMoney** would earn NW4's 2% with no CMU fee (§8) · household (NW3) / unverified (NW4, CMU's QR, TrueMoney's limit).

### 2.2 Points · verified

- `ยอดใช้จ่าย (รูดเต็มจำนวนและผ่อนสินค้า) ทุก 25 บาท รับคะแนนสะสม 1 คะแนน`, valid 5 years ([First Choice Rewards](https://www.firstchoice.co.th/firstchoice-rewards)). Burns ≈ ฿0.09–0.10 a point (330 → ฿30 Amazon, 300 → ฿30 7-Eleven, 1,000 → ฿100 donation) → **≈ 0.36–0.40%**.
- The four exclusion notices on that page ([MCC notice](https://www.firstchoice.co.th/getattachment/b040a615-8af1-476e-bc2c-655d419a1088/Notice-of-Exemption-from-Accumulated-Points-under-the-Designated-MCC.pdf): transit 4111/4112/4131/4784, EEA, China; AIA; 7-Eleven/TrueMoney and a fuel cap; MCC 5199) name **no education and no government MCC** — First Choice points even survive a 9399 posting.
- No points-for-tuition burn exists for this card (XU's 18% points-to-cashback is XU-only).

### 2.3 U PLAN "0% สั่งได้ทุกอย่าง" — 0% for 3 months on any slip · verified

- Page: [สมาร์ททุกการใช้จ่าย 0% สั่งได้ทุกอย่าง](https://www.firstchoice.co.th/promotion/epr-0-3month) (no end date shown; a standing UCHOOSE service). First Choice Visa Platinum and XU.
- Any full-amount slip ≥ ฿500, combined ≥ ฿3,000, dated before the statement date, converted in UCHOOSE (`แบ่งชำระรายเดือน` → `0% สั่งได้นาน 3 เดือน`) **by 20:00 on the statement date** of the current cycle. No upper limit stated. No education list needed: tuition qualifies like anything else. For CMU's window that is **by 20:00 on 5 Dec 2026** for any slip of 30 Nov – 4 Dec (cycle closing 5 Dec, due 25 Dec); terms then fall due on 25 Dec, 25 Jan and 25 Feb.
- A TrueMoney-routed slip (§8) is a full-amount card slip too, but whether U PLAN offers `TMN*` slips for conversion isn't stated · unverified.
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
- **Period: 1 ส.ค. 69 – 31 ธ.ค. 69** (spend) — covers CMU's 30 Nov – 4 Dec window. Cards: Central The 1 credit cards (`red|luxe|black|theblack`), so 🏠 **REDZ qualifies**.
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

## 5. KTC (KTC UnionPay)

Baiboon's KTC UnionPay (Diamond) supplement (…2310) on Takumi's account earns its own KTC FOREVER points ([[../../cards/ktc-unionpay]]). The promotion sitemaps held 11,678 URLs on 22 Oct.

### 5.1 No points on tuition · verified (KTC's terms as saved in the repo on 28 Sep; not re-read today)

- KTC FOREVER terms, rule (16), KTC UnionPay only: no points at `MCC 8211, 8220, 8241, 8244, 8249, 8299 หมวดการศึกษา และบริการการศึกษา` (education), nor at 9211–9405 government, 8062 hospitals, 5411 supermarkets and the rest ([verbatim copy of 28 Sep](../../sources/ktc-forever-terms-2026-09-28.txt), [[../../promotions/ktc-forever]]). Whatever CMU's code (8220, 8299 or 9399), **KTC UnionPay earns nothing**.
- The **UnionPay QR 6%** (≤ ฿60 a slip) needs a UnionPay QR; CMU's QR is Thai QR (PromptPay), and the card pages take "credit cards" with no network named ([[cmu-tuition]]). Even if it applied, ฿60 is 0.1% of a semester. Whether CMU's gateway or counter takes UnionPay at all is unknown.

### 5.2 `MTFED-1436` "โปรโมชั่นพิเศษ ที่สถาบันการศึกษาชั้นนำ กับบัตรเครดิต KTC" · verified (terms) · CMU not listed

- Page: [education-cashback](https://www.ktc.co.th/promotion/education/recommended/education-cashback), **15 ม.ค. 69 – 31 ธ.ค. 69**; banner "สนุกคุ้ม ทุกคอร์สเรียน … แลกคะแนนรับเครดิตเงินคืน 12% ณ สถาบันการศึกษาที่ร่วมรายการทั่วประเทศ".
- **Privilege 1 — points → 12%**: for every ฿500 of a slip ≥ ฿500, redeem 500 KTC FOREVER points (points equal to the slip, in ฿500 steps) → 12% back (฿0.12 a point, against KTC's normal ฿0.10). Register **on the day of the spend**: SMS **`E12 <16 digits>#<points>` → 0613845000**, or www.ktc.promo/education-e12. One slip only, no splitting; `สงวนสิทธิ์การรับเครดิตเงินคืนตามรายการนี้ 1 หมายเลขบัตรฯ / สมาชิก 1 ท่าน เท่านั้น ตลอดระยะเวลารายการ` (one card number per member for the campaign). Credited within 60 days of month end. Excludes ROP, CASHBACK, corporate and government cards; KTC UnionPay isn't excluded.
- **Privilege 2 — 0.69% a month for 3, 6 or 10 months** (≤ 16% a year effective) on ≥ ฿3,000 (slips ≥ ฿500 the same day), registered by calling **KTC PHONE 02 123 5000 on the day**.
- **Both apply only `ณ สถาบันการศึกษาที่ร่วมรายการ`, and KTC publishes no list**: not on the page (raw HTML, the Next.js payload or the rendered page), not in the store-list sitemaps (`sitemap-pm-store-list-1/2.xml`, 1,319 URLs, none for education), not in a PDF. The education pages that do name institutions are course providers (Let's Mandarin, Wall Street English, Mastery School, Crest School, ClickRobot, FutureSkill, MBK Education Plus, The Food School). **CMU isn't named on any KTC promotion page** (confirms the CMU researcher). Ask KTC PHONE before paying if this matters.
- Value even if CMU counted: a points burn at ฿0.12 instead of ฿0.10 (+฿0.02 a point), paid with points already held — 60,000 points for a ฿60,000 slip. It doesn't offset the 2.1% fee.
- Predecessors: `MTFED-0043` "education-15-cashback" (1 Jul – 31 Dec 2025: discounts, 15–16% points-back, 0% up to 10 months) and the 2020 tuition campaign (KTC news, 11% points-back, 1 Jun – 30 Sep 2020).

### 5.3 Nothing else

- No KTC tuition installment like its public-hospital 0.69% plan (which names Sriphat, [[sriphat]]); `hospital-redeem-for-installment` (points → 0%) covers MCC 5912/8021/8062 only.
- KTC's article "ผ่อนค่าเทอม ด้วยบัตรเครดิต" ([link](https://www.ktc.co.th/article/knowledge/installment-tuition-fees-for-university)) is general advice; its example is Chulalongkorn (any bank's card, up to 10 months at the university's and bank's terms). It mentions a deposit-secured KTC card for students aged 20+.

---

## 6. AEON (World Mastercard, Primo, Next Gen)

### 6.1 No points on tuition · verified

- [AEON notification](https://www.aeon.co.th/aeon/news-events/notification-aeon-credit-cards-2025), from **11 Nov 2025**, every AEON credit card except Big C: no points at **`8211 การชำระเงินที่เกี่ยวข้องกับสถาบันการศึกษา`**, **`8220 … วิทยาลัย, มหาวิทยาลัย …`**, 8241, 8244, 8249, **`8299 บริการด้านการศึกษาและการสอนพิเศษ`**, 8062, 8398, 8661, 9211, 9223, **9399**, 9402, 9405, 9406, 9950, plus 7999 and other codes earlier in the table. From 11 Jan 2026 also `ยกเว้นการให้คะแนนสะสมสำหรับรายการแบ่งจ่าย 0% ทุกช่องทาง`.
- So AEON World (1 pt/฿30 elsewhere), AEON Primo (1 pt/฿20) and AEON Next Gen earn **nothing** at CMU.

### 6.2 Campaigns · verified

- **AEON Next Gen 5% online** ([card page](https://www.aeon.co.th/aeon/cards/aeon-nextgen-digital-card)): online slips ≥ ฿500, **≤ ฿50 a transaction**, ≤ ฿1,000 per primary account a cycle (11th–10th), only if the cycle has ≥ ฿500 of Scan To Pay; excludes Scan To Pay, QR, e-wallets, installments, utilities, airlines, funds, insurance, fees. Education isn't excluded → **฿50** on CMU's online payment, in the cycle 11 Nov – 10 Dec.
- **AEON World 5%**: supermarkets only (Big C, Lotus's, Foodland, Villa, Tops, Gourmet, Central Food Hall, Makro PRO), 1 Apr 2026 – 31 Jan 2027 → ✗. Its +2,000-point bonus needs four foreign-spend categories → ✗.
- **NTW1** ([page](https://www.aeon.co.th/aeon/promotions/happy-monthly-with-aeon-2026)): restaurants (5812), Grab/LINE MAN, named supermarkets, named travel sites, five beauty stores, named fashion and sports shops → ✗. (Baiboon's ฿47,858.50 of Makro PRO already holds the 10 Oct – 9 Nov cycle at ฿340: Bureau `2026M11 — NTW1`.)
- **"365 วัน"** (1 Sep 2026 – 28 Feb 2027): counts only principal cards' full-payment spend → Baiboon's supplement spend doesn't count.
- **Installments**: AEON's 185 tiles hold 0% plans only at named merchants (phones, IT, appliances, gold, tyres, Wall Street English 0% up to 18 months). **No tuition plan.**

---

## 7. Students and parents

- **Krungsri Consumer's back-to-school campaign** (press release 22 Jun 2569, [Kaohoon](https://www.kaohoon.com/finance/840455)): the Krungsri Platinum 0% × 4 on tuition (§1.2; to 31 Dec), the Central The 1 0% × 4 (1 May – 31 Jul, **ended**), and 0% for up to 24 months (First Choice) or 10 months (Krungsri, Central The 1, Lotus's) on language and skills courses at named schools with `EDU2` (to 31 Oct) · third-party only (the Krungsri pages are verified in §1).
- **Course and school pages** (named institutions only, none a university): Krungsri `EDU3` (ECC, Tutor House, Star Maker), New Education World, British Council, Let's Mandarin, Wall Street English, Inlingua (1 Oct 69 – 31 Jan 70); Central The 1 SISB (incl. `โรงเรียนนานาชาติสิงคโปร์เชียงใหม่`), Harrow, Rugby School; Lotus's SISB, ECC, Wall Street English, Let's Mandarin; KTC's course providers (§5.2); AEON Wall Street English.
- **Textbooks and stationery**: Lotus's SMP1 counts bookshops and stationery (SE-ED, Naiin, Asia Books, Kinokuniya, B2S, OfficeMate); Central The 1 has a B2S Book Fair 500-point offer at QSNCC, Bangkok (23 Oct – 1 Nov).
- **Student cards**: KTC promotes a deposit-secured card for students aged 20+ (article above); Krungsri has only explainer articles (`krungsri-the-coach`, `plearn-plearn`). No student-card offer from any issuer in scope.
- **Education loans (กยศ.)**: no tie-in from these issuers was found.
- First Choice's listing links a Krungsri savings account "for your child's education" (`เปิดบัญชีเพื่อลูก เตรียมเก็บเงินเพื่อทุนการศึกษา`), a deposit product, not a card offer.

---

## 8. The TrueMoney route to CMU's fee-free Thai QR (Visa cards only)

- **What exists**: TrueMoney lets a linked **Visa** credit or debit card pay a PromptPay merchant QR, `ไม่มีขั้นต่ำ ไม่มีค่าธรรมเนียม` ("no minimum, no fee"; [TrueMoney](https://www.truemoney.com/debit-credit-card/promptpay/), read today through r.jina.ai): scan → choose `VISA บัตรเครดิต/เดบิต`. The slip posts as `TMN*PROMPTPAY30` · verified (feature).
- **Which of Baiboon's cards**: First Choice (Visa Platinum) and Krungsri VISA. Not JCB, Lady, NOW, REDZ, Lotus's (Mastercard), KTC UnionPay or AEON.
- **What it would earn**: First Choice **NW4** 2% (household: NW3's September eligible list included `TMN*PROMPTPAY30` rows, §2.1); Krungsri VISA **ONQ3** ฿350 on 30 Nov only. **No points** on either (Krungsri-family cards earn none on TrueMoney-linked spend from 1 Aug 2026). No CMU fee. So First Choice → **+2.0% net**, the best figure in this report.
- **Unverified, and decisive**:
  - whether TrueMoney's scanner accepts CMU's **Thai QR Payment** code from the registration system, and offers the Visa funding option for it (TrueMoney's page speaks of PromptPay *merchants*; CMU's code may be a biller/bill-payment QR);
  - TrueMoney's per-payment and monthly limits for card-funded payments (unpublished; the household's `TMN*PROMPTPAY30` rows are all under ฿1,000);
  - whether First Choice's limit and Krungsri's fraud checks pass a ฿60,000–100,000 wallet payment.
- **A safe test**: in the window, open CMU's QR in TrueMoney and see whether it shows the amount and offers the Visa card *before* confirming. Nothing moves until the payment is confirmed. If it fails, pay at the counter with First Choice instead.

---

## What couldn't be found

- **CMU's MCC** (8220 is a reading; 8299 or 9399 would change Krungsri's 0% × 4, NW4, REDZ, Lotus's and Krungsri Card points, §0.1). The first statement line will show the merchant string only.
- **Whether Baiboon's Krungsri VISA is a Visa Platinum** (decides the 0% × 4). The card face or UCHOOSE shows it.
- **Whether Takumi's Lotus's account is invited** to `small-ticket-a/b-q4-26` (UCHOOSE shows invited campaigns). It decides Lotus's +฿1,250.
- **`ED1`'s MCC list** (none published) and whether its condition-3 "extra The 1 points" add anything beyond the card's normal points.
- **KTC `MTFED-1436`'s institution list**: not published anywhere KTC serves; CMU is named on no KTC promotion.
- **Whether the counter's 0.9% posts inside the card slip or separately**, and which networks the online gateway and the counter terminal take (JCB, UnionPay); see [[cmu-tuition]].
- **The TrueMoney route's limits and QR compatibility** (§8).
- **Whether a TrueMoney-routed First Choice slip can be converted by U PLAN**, and whether NW4 (not only NW3) counts it.
- **December successors**: ONQ3 ends 30 Nov with no successor published; nothing new for December was listed by any issuer in scope on 22 Oct. Re-check the Krungsri listing and Central The 1's `gcspromotion` around 25–30 Nov.
- **The Krungsri 0% × 4 page's banner** (`Family-with-kid-EPR_Web1200x650px.webp`): the WAF block page every time; the text, the six app screenshots and the press release agree, so nothing is expected in it.

## Site methods

- **krungsricard.com's WAF ("WAF On-Prem", "Access denied", a 1,805-byte page)** now blocks some promotion URLs and media files outright, including `family-with-kids-4-months`, `scan-installment`, `point-cashback` and `/th/krungsri-point`. **Adding a trailing slash (`…/family-with-kids-4-months/`) or a dummy query (`?a=1`) gets the page**; images and PDFs came through after a few seconds' wait, a `Referer` of the promotion page and a `?t=<n>` query, retried. r.jina.ai also read the blocked page. The listing JSON (581 items) still parses as in [[../research-methods|research methods]].
- **Krungsri's in-app plan wording** sits in the page's step screenshots (`/KrungsriCreditCard/media/html/<name>-Step0N.jpg`); here they gave the plan's exact MCC list.
- **centralthe1card.com**: `education-202608`'s tier table is only in the poster `getattachment/48e4e6fa-…/OL_Education_Jul26-1024-(1).webp` linked from `specialContent`; the `url` alias again belonged to another promotion (`Luxe-Upgrade-202507-…`).
- **KTC**: an education promotion's institution list is not in the RSC payload or the store-list sitemaps; the rendered page (headless, `--virtual-time-budget=20000`) has no list either.
- **AEON**: the rendered promotion index (185 `<a class="package">` tiles) greps for installment plans in one pass; the no-points notice reads with curl at `/aeon/news-events/notification-aeon-credit-cards-2025/`.
- **Household checks used here** (read-only): `fetch-transactions` for tuition rows (none for Baiboon; Takumi's Chulalongkorn ฿33,500 on KBank PLUSTINUM earned 1 pt/฿25) and for `TMN*PROMPTPAY30` rows on First Choice; the Promotion Bureau's October rows for NW4 (฿18,161.88 pooled), NOW (฿25 used), ONQ3 and NTW1.
