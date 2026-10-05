---
tags: [catalogue-research, 2026-10]
researched: 2026-10-05
---

> **Research snapshot**: offers that name no merchant, checked against a UNIQLO purchase — October 2026 research. Scope: each household card's own earning at UNIQLO (most likely MCC 5651 family clothing; 5691 / 5699 / 5311 checked as alternatives) in Chiang Mai, in store and at uniqlo.com / the UNIQLO app; all-spend, spend-threshold, online-spend, fashion-category, card-network and welcome offers from every Thai issuer, checked against a ฿3,000 / ฿6,000 / ฿12,000 UNIQLO spend; and whether the UNIQLO-named campaigns' "not combinable" clause kills a card's own cashback. Read on **2026-10-05** from the official pages and the repo, for the October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]].
> The raw dumps it mentions (HTML, JSON, posters) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# Offers that name no merchant, at UNIQLO — October 2026 (ต.ค. 69)

This continues [[all-spend]] (Makro), [[all-spend-hospital-spa]], [[all-spend-ticketing]] and [[all-spend-apple]]. The UNIQLO-named bank campaigns (UOB `UNO`, Krungsri `UNQ`, KBank `UQN`, ttb `UQCB`, KTC JCB and Krungsri JCB points) are in [[../../promotions/uniqlo-2026]] and the sibling UNIQLO reports; they appear here only where they interact with a card's own rate.

**Legend.** 🏠 a household card. Confidence: **verified** (official page read today) · **verified (date)** (read on that date in an earlier October report, not re-read) · **repo-verified** (the repo's card YAML, promotion note or Bureau class, built from the bank's page) · **household** (the household's own ledger shows it) · **third-party only** · **unverified**. A **reading** is an inference from the terms, labelled as such.

**Point values used** (as in [[all-spend-ticketing]]): UOB Rewards ≈ ฿0.104 (UOB → The 1) · KTC, Krungsri, First Choice, KBank at a card terminal ฿0.10 · KBank via K PLUS ฿0.083 · The 1 ฿0.125 · LINE POINTS ฿1 · Lotus's coin ฿1 (coupon). AEON Happy Point and POINTX have no published cash value.

**October Bureau usage** (from `write-catalogue status`, 2026-10-05 snapshot): NW4 pooled ฿8,648 → ฿50 credited so far · UOB One 10%/5% ฿59.10 of ฿500 (month) · UOB One 1% ฿71 of ฿2,000 (cycle 25 Sep – 21 Oct) · UOB World ×5 ฿392 of ฿20,000 pooled (cycle 25 Sep – 21 Oct) · ttb so smart 1% ฿0 of ฿2,000 (cycle 27 Sep – 26 Oct) · Krungsri NOW 5% ฿0 of ฿300 · ONQ3, LBS3, ON4 ฿0 · KTC UnionPay QR …1346 (Takumi) ฿180 left of ฿300, …2310 (Baiboon) ฿139.80 left · AEON UnionPay 3% ฿1,929 left · UNO / UNQ / UQN / UQCB unused.

---

## 0. What UNIQLO accepts, and what its slips look like

**How UNIQLO Thailand takes payment** · verified ([Store | Payment](https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0Ie000000TPQl&l=en_US), [Online | Payment](https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0Ie000000TOqj&l=en_US), [card logos](https://faq-th.uniqlo.com/pkb_Home_UQ_TH?id=kA0Ie000000TOk4&l=en_US)):

- **In store**: cash; "QR Code Scan" (a Thai QR), with `※We apologize that QR code payment via credit card is not currently supported.`; `Credit and Debit Cards such as Visa, Mastercard, and JCB` (`American Express is currently not accepted`); Alipay; WeChat.
- **E-wallets**: `E-wallet services such as ShopeePay, TrueMoney Wallet, and Rabbit LINE Pay are not officially supported at our stores` (refunds go through the wallet provider, and a return must be the whole purchase).
- **Online (uniqlo.com and the app)**: credit/debit card, COD, or pay in store. The card page shows **only the Visa, Mastercard and JCB logos**; overseas-issued cards, Amex and QR aren't accepted; `Only one-time full payments are supported. Installment payments and interest-bearing installment plans are not available.`
- **So**:
  - **UnionPay doesn't work at UNIQLO.** Online, the logos are Visa, Mastercard and JCB only (verified). In store, the list says "such as" and doesn't name UnionPay (reading: not accepted). This rules out the household's KTC UnionPay and AEON UnionPay, **Bangkok Bank's UnionPay 2%**, and the **UnionPay QR 6%** (a credit-card QR payment, which UNIQLO says it doesn't support).
  - **Wallet routes are out.** These are UOB SPW796 through ShopeePay or TrueMoney, Krungsri ONQ3 through a wallet, KBank LINE Points' 3–5% through LINE Pay and AEON Rabbit's 5% through LINE Pay. The wallets aren't officially supported in store, and online takes no QR.
  - **No installments online.** Installments in store are the banks' own pay plans, which every all-spend offer below excludes.

**Chiang Mai branches** · verified (UNIQLO's store locator data, read today): `UNIQLO Central Chiangmai` (Central Chiangmai, room 111, 1st floor, a LARGE_STORE) and `UNIQLO Central ChiangMai Airport` (Central Chiangmai Airport, rooms 254–255, 2nd floor). Both are units in Central Pattana malls with their own room numbers, **not counters inside Central Department Store**. So UOB UNO's "ไม่รวมสาขาที่อยู่ใน department store" doesn't bite in Chiang Mai, and the slip carries UNIQLO's own MCC (reading).

**The household's UNIQLO history** (read from the ledgers today, read-only) · household:

| Date | Holder · card | Merchant string (verbatim) | Amount | What the household marked |
|---|---|---|---|---|
| 2026-09-21 | Baiboon · First Choice | `UNIQLO-CENTRAL CHIANGMA CHIANGMAI TH` | ฿990 | `% cb` 2% (NW3), 39 points (1 / ฿25) |
| 2025-06-12 | Baiboon · UOB World | `UNIQLO THAILAND CO.,LT Pathum Wan THA` (online; the company's Bangkok address) | ฿1,880 | **×5** (online bonus) |
| 2025-04-20 | Baiboon · UOB World | `UNIQLO-C.FESTIVAL CHIA CHIANGMAI THA` | ฿592 | ×2, Note `ไม่อยู่ในหมวดหมู่ให้คะแนน 5 เท่า` |
| 2025-03-09 | Baiboon · UOB World | `UNIQLO-C.FESTIVAL CHIA CHIANGMAI THA` | ฿790 | ×2, Note `ได้คะแนน 2 เท่า เนื่องจากไม่อยู่ในหมวดหมู่ที่ให้คะแนน 5 เท่า` |

- The in-store slip posts under UNIQLO's own name (`UNIQLO-<branch>`), not as the department store. `C.FESTIVAL CHIA` and `CENTRAL CHIANGMA` are the same mall: Central Festival Chiangmai, renamed Central Chiangmai.
- Online posts as `UNIQLO THAILAND CO.,LT Pathum Wan THA`: a Thai company billing in baht, so no "foreign-registered website" rule bites. UOB World paid it the e-commerce ×5.
- **MCC**: no issuer or lookup states it. 5651 (family clothing) is the reading; every rate below is the same at 5691 / 5699. Only a department-store posting (5311) would change anything: UOB Premier ×4 and Krungsri's `2x-platinum`. The Chiang Mai stores don't post that way.

---

## 1. At a glance — each household card at UNIQLO (own rate, no UNIQLO-named campaign)

Rates are on a full-payment card slip. The "≈ ฿" column is for one ฿3,000 / ฿6,000 / ฿12,000 slip. "Oct room" is what's left of the cap on 5 Oct.

| # | Card · 🏠 who | In store | Online (uniqlo.com / app) | ≈ ฿ on 3k / 6k / 12k | Cap · Oct room | What bites | Conf. |
|---|---|---|---|---|---|---|---|
| A1 | **Krungsri NOW** · 🏠 Takumi (Baiboon uses it) | 0.4% (1 pt / ฿25 a slip) | **5%**: ฿25 per whole ฿500 a slip; no points on the row | online **150 / 300 / 300** | ฿300 a month · **฿300 left** | online only (website or app), not in store, not by QR; Smart Plan installments ✗; its own "not combinable" line (§3) | verified (NOW page) · reading (uniqlo.com/app is "ผ่านเว็บไซต์หรือแอปพลิเคชัน") |
| A2 | **First Choice NW4** · 🏠 all three, pooled on Takumi's account | **2% at the margin**, in whole ฿10,000 steps of the month's pooled spend, + 1 pt / ฿25 | same | **+150 / +150 / +350** from today's ฿8,648 pool (crossing ฿10,000 turns ฿50 into ฿200) | ฿2,000 a month · ฿1,950 left | `แฟชั่น` is a named category; installments (loan line) ✗; foreign-registered websites ✗ (UNIQLO's isn't) | verified (NW4 page) · household (NW3's 2% on the Sep UNIQLO row) |
| A3 | **UOB World** · 🏠 Takumi, Baiboon | **×2 ≈ 0.83%** (fashion isn't a ×5 category) | **×5 ≈ 2.08%** | store 25 / 50 / 100 · online **62 / 125 / 250** | ×5 inside ฿20,000 a cycle shared by the account · ≈ ฿19,600 left | ×5 needs the network's e-commerce flag | household (store ×2, online ×5) · verified (2 Oct) |
| A4 | **UOB One** · 🏠 all three | **1%** | **1%** | 30 / 60 / 120 | ฿2,000 a cycle shared · ฿1,929 left | no fashion or department-store exclusion; only Makro, fuel, utilities … | verified (2 Oct) |
| A5 | **ttb so smart** · 🏠 Takumi, Baiboon | **1%** | **1%** | 30 / 60 / 120 | ฿2,000 a cycle per card account · ฿2,000 left | pay plan / so goood installments ✗; paid into a ttb savings account | verified (3 Oct) |
| A6 | **KBank PLUSTINUM** · 🏠 Takumi (Baiboon uses it at Makro) | **up to ×3**: 1 pt / ฿25 plus a monthly bonus on fashion, restaurant and department-store spend (5651 is listed) | same | 16 / 60 / 112 (0.5% / 1.0% / 0.9%); 1.2% at ฿8,000 | bonus ≤ 640 pts a month a person | the bonus counts the month's restaurant spend too, so it may already be used up; +฿200 e-coupon at ≥ ฿10,000 in the month; +Starbucks ฿400 at ≥ ฿30,000 (Season 3, register first) | **verified** (card page, §2.6) |
| A7 | **KBank LINE Points** · 🏠 Takumi | **1% LINE POINTS** | 1% | 30 / 60 / 120 | per cycle, 1% of the credit limit | on-top +50 at ฿5,000 / +200 at ฿15,000 in the month (registered); the LINE Pay 3–5% route is ✗ (§0) | verified (2 Oct) |
| A8 | UOB Premier · 🏠 Takumi, Baiboon | ×2 ≈ 0.83% | ×2 | 25 / 50 / 100 | — | ×4 only at MCC 5311 / 5309 (department store), which the Chiang Mai stores don't post as | verified (2 Oct) |
| A9 | Central The 1 REDZ · 🏠 Takumi, Baiboon | **0.5%** (1 The 1 pt / ฿25 a slip) | 0.5% | 15 / 30 / 60 | — | **UNIQLO isn't on the CPN ×3/×4 shop list** (§2.8) | verified |
| A10 | Lotus's Beyond · 🏠 Takumi (+Baiboon) | 0.5% (0.25 coin / ฿50) | 0.5% | 15 / 30 / 60 | — | **SMP1 names UNIQLO** in its fashion category but isn't registered; SMT2 ฿200 at ≥ ฿2,000 (first 500, register first) (§2.10) | verified |
| A11 | UOB Makro · 🏠 Takumi | ≈ 0.42% (1 pt / ฿25) | same | 12 / 25 / 50 | — | ×2 on the 16th with `MMID` | verified (2 Oct) |
| A12 | Krungsri VISA / JCB / Lady · 🏠 Takumi, Baiboon | 0.4% (1 pt / ฿25 a slip) | 0.4% | 12 / 24 / 48 | — | Krungsri JCB's 3× / 5× at UNIQLO is a named bonus ([[../../promotions/uniqlo-2026]]) | verified (2 Oct) |
| A13 | KTC Digital VISA / JCB / Mastercard · 🏠 Takumi | 0.4% (1 pt / ฿25; ×2 only in foreign currency) | 0.4% | 12 / 24 / 48 | — | KTC JCB's ×2–×5 UNIQLO bonus is named ([[../../promotions/uniqlo-2026]]) | verified (3 Oct) |
| A14 | KBank JCB / KBank Shopee · 🏠 Takumi | 0.4% (1 K Point / ฿25) | 0.4% | 12 / 24 / 48 | — | — | verified (2 Oct) |
| A15 | AEON Primo · 🏠 Takumi, Baiboon | 1 pt / ฿20 (no published value) | same | — | — | — | verified (3 Oct) |
| A16 | AEON World Mastercard · 🏠 Takumi, Baiboon | 1 pt / ฿30 (no published value) | same | — | — | its 5% is supermarkets only; **NTW1's fashion list doesn't name UNIQLO** (§2.9) | verified |
| A17 | AEON Next Gen · 🏠 Takumi, Baiboon | 0 | 5%, **≤ ฿50 a transaction** | online 50 / 50 / 50 | ≤ ฿1,000 a cycle | needs ≥ ฿500 of Scan To Pay in the same cycle; unused since Nov 2025 | verified (1 Oct) |
| A18 | CardX JCB · 🏠 Nuta | 1 POINTX / ฿25 (no published value) | same | — | — | JCB is accepted | third-party + household |
| ✗ | **KTC UnionPay** · 🏠 all three | **✗ UnionPay not accepted**; UnionPay QR 6% ✗ (no credit-card QR) | ✗ | — | (QR room …1346 ฿180, …2310 ฿139.80 unused here) | — | verified (UNIQLO's payment pages) |
| ✗ | AEON UnionPay · 🏠 Takumi, Nuta | ✗ (UnionPay; and 3% only in CNY/HKD/MOP/TWD) | ✗ | — | — | — | verified |
| ✗ | AEON Rabbit · 🏠 Takumi | 0 (no points since 11 Nov 2025) | 0 | — | — | its 5% is LINE Pay / Rabbit top-up only | repo-verified |
| ✗ | SPayLater · Grab PayLater · 🏠 | not a card; SPayLater could pay a merchant PromptPay QR, with no reward | — | — | — | — | reading |

**Best household card at UNIQLO without a UNIQLO campaign:**

- **Online**: Krungsri NOW. It's 5% up to ฿6,000 of slips a month, in whole ฿500 steps, and has ฿300 of room. Next is UOB World ×5 (≈ 2.1%).
- **In store**: First Choice. A slip that takes the pooled month past the next whole ฿10,000 earns ฿200; today ฿1,352 more does it. Next are UOB One or ttb so smart (1%) and KBank PLUSTINUM (up to 1.2% in points).
- **The UNIQLO-named campaigns pay more on a slip of ฿3,000 or more**: 5% (UNO, UNQ, UQCB) or 3.3% (UQN) at ฿3,000, and 5–8% at ฿10,000–12,000 (UNQ ฿800 on Krungsri JCB at ฿10,000 is the top). They're the sibling reports' subject. §3 is whether the card's own rate still comes on top.

---

## 2. Card by card (details behind §1)

### 2.1 Krungsri NOW — 5% online · verified
- [NOW page](https://www.krungsricard.com/th/product/creditcard/now), read today: `รับเครดิตเงินคืน 5% เมื่อซื้อสินค้า/บริการผ่านเว็บไซต์หรือแอปพลิเคชัน`, `สิทธิพิเศษนี้เฉพาะการซื้อสินค้า/บริการผ่านเว็บไซต์หรือแอปพลิเคชัน ไม่รวมการซื้อโฆษณาออนไลน์และการใช้จ่ายผ่าน QR Code`. Excluded categories are insurance, funds and travel; fashion isn't excluded. Smart Plan online installments are out. `สงวนสิทธิ์ยกเว้นการให้คะแนนสะสม กรุงศรี พอยต์ สำหรับทุกรายการใช้จ่าย` (on the rows that get the 5%). And `รายการส่งเสริมการขายนี้ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้`.
- Mechanics (repo, `krungsri_now.py`): ฿25 per whole ฿500 per slip, ≤ ฿300 per calendar month, booked as the bank's `CB <merchant>` row. So a ฿3,000 order → ฿150 and a ฿6,000 order → ฿300. Two ฿3,000 orders also make ฿300, the month's cap.
- **Reading**: an order on uniqlo.com or in the UNIQLO app, paid by card at checkout, is a website/app purchase. A store purchase isn't (it earns 1 pt / ฿25).

### 2.2 First Choice NW4 — 2% at the margin · verified
- [NW4 page](https://www.firstchoice.co.th/promotion/firstchoice-cashback), read today: the blurb lists `… ซูเปอร์มาร์เก็ต ห้างสรรพสินค้า แฟชั่น สกินแคร์ …`.
- **Exclusions**:
  - marketplaces (→ ON4) and delivery (→ DLV3);
  - gold and financial services;
  - `รายการใช้จ่ายในต่างประเทศ [Inter-Spending] ทุกประเภท รวมถึง รายการช้อปออนไลน์ผ่านเว็บไซต์ที่จดทะเบียนต่างประเทศ`;
  - e-wallet top-ups, insurance, utilities and auto-debits.
  - Nothing touches a Thai clothing store or uniqlo.com.
- **No "not combinable" line** on the page.
- **Ladder**: ฿50 at ฿5,000–9,999; ฿200 per whole ฿10,000; ≤ ฿2,000 a month. It's pooled over the three holders on Takumi's account (`nw4.py`), and the household is registered. On 5 Oct the pool was ฿8,648 → ฿50.
- **Base points**: 1 per ฿25 (First Choice Reward, ≈ ฿0.09–0.10).
- First Choice is a Visa, so UNIQLO takes it. There's no First Choice UNIQLO campaign: UNQ is Krungsri Card's, not First Choice's (see [[../../promotions/uniqlo-2026]]).

### 2.3 UOB World — ×2 in store, ×5 online · verified (2 Oct) + household
- 5 points per ฿25 on `การใช้จ่ายออนไลน์, e-wallet, หมวดร้านอาหาร, หมวดท่องเที่ยว, และเงินสกุลต่างประเทศ รวมสูงสุด 20,000 บาทต่อรอบบัญชี`, else ×2. The ×5 online needs `รายการที่ถูกกำหนดให้เป็นรายการ e-Commerce โดยมาสเตอร์การ์ดและวีซ่า`. The household's uniqlo.com row got ×5; its Chiang Mai store rows got ×2 (§0).
- ≈ ฿0.104 a point, so ×5 ≈ 2.08% and ×2 ≈ 0.83%. The ฿20,000 is shared by Takumi and Baiboon and counts every transaction (`uob_world.py`); ฿392 was used by 5 Oct.

### 2.4 UOB One 1% · verified (2 Oct)
- The 1% exclusion list (quoted in [[all-spend-hospital-spa]] §2.1) names Makro, fuel, utilities, funds and unit-linked, cash, unbilled installments, FX, fees, cancellations, business spend, foreign-THB and wallet top-ups. It has no fashion or department-store item.
- ฿2,000 a statement cycle, shared by the account (`uob_one.py`). Takumi's UOB One principal …4672 counts the same as the supplements.
- Re-read today ([UOB One page](https://www.uob.co.th/personal/credit-cards/cash-back/one-cash-back-credit-card.page)): the cashback section has **no "not combinable" line**. The only `ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นได้` on the page belongs to the SF cinema 1-free-1 benefit.

### 2.5 ttb so smart 1% · verified (3 Oct)
- `รับเครดิตเงินคืน 1% ทุกการใช้จ่ายผ่านบัตร … สูงสุด 2,000 บาท/บัญชีบัตร/รอบบัญชี`. Its exclusions (quoted in [[all-spend-ticketing]] §2.6) have no fashion item. Pay plan installments are out, and so is TrueMoney.
- Paid into a ttb savings account, not onto the card (`cards/ttb-so-smart.yaml`). Cycle 27 Sep – 26 Oct: ฿0 used.

### 2.6 KBank PLUSTINUM — the ×3 counts fashion · verified
- [PLUSTINUM page](https://www.kasikornbank.com/th/personal/creditcard/pages/plustinum.aspx), rendered today, verbatim: `รับคะแนน K Point รวมสูงสุด 3 เท่า เมื่อมียอดใช้จ่ายสะสมต่อเดือนผ่านบัตรในหมวดร้านอาหาร (MCC 5422, 5441, 5451, 5462, 5921, 0003, 5811, 5812, 5813, 5814), ห้างสรรพสินค้า (MCC 0001, 0002, 5310, 5311), และร้านค้าแฟชั่น (MCC 5137, 5139, 5611, 5621, 5631, 5641, 5651, 5655, 5661, 5681, 5691, 5697, 5698, 5699, 5949, 7251, 7296, 5948)`. **5651, 5691 and 5699 are all on it.**
- **It isn't a flat ×3.** The base is 1 per ฿25. The bonus is one tier a calendar month on the month's in-category spend:

  | In-category spend in the month | Bonus K Point |
  |---|---|
  | ≥ ฿2,000 | 40 (0.5×) |
  | ≥ ฿4,000 | 160 (1×) |
  | ≥ ฿6,000 | 360 (1.5×) |
  | ≥ ฿8,000 | 640 (2×, the cap) |

  - `จำกัดการรับคะแนน K Point พิเศษเพิ่มสูงสุด 640 คะแนน/ท่าน/เดือนปฎิทิน`. The bonus is credited by the 10th of the next month and expires after 2 years.
  - `ยอดใช้จ่ายและคะแนนสะสมจะคำนวณแยกกันระหว่างบัตรหลักและบัตรเสริม`. Full payment only (no Smart Pay).
  - Runs 7 Oct 2025 – **31 Dec 2026**.
- **At UNIQLO alone** (฿0.10 a point): ฿3,000 → 160 pts ≈ ฿16 (0.53%); ฿6,000 → 600 ≈ ฿60 (1.0%); ฿8,000 → 960 ≈ ฿96 (1.2%); ฿12,000 → 1,120 ≈ ฿112 (0.93%).
  - Restaurant spend on the card in the same month counts toward the same tiers. Takumi uses PLUSTINUM at small food shops, which aren't in the ledger, so the bonus left for UNIQLO is unknown.
- **On top, threshold gifts** (verified 2 Oct, [[all-spend-hospital-spa]] §3.3):
  - ≥ ฿10,000 in the month → a ฿200 Starbucks / BBQ / ฿260 SF coupon on the 15th (first come).
  - Season 3: register in K PLUS, then ≥ ฿30,000 in October → Starbucks ฿400.

### 2.7 KBank LINE Points, JCB, Shopee · verified (2 Oct)
- LINE Points: `รับ LINE POINTS 1%* ที่ร้านค้าออฟไลน์และออนไลน์อื่น ๆ`. Its exclusions (EEA/China, foreign-THB, utilities, tax, fees, insurance, funds, fuel, 5310, 5411 …) have no fashion code. The on-top (+50 at ฿5,000, +200 at ฿15,000 in the month, registered) counts the same spend. UQN gives this card no extra K Point (UNIQLO's KBank page).
- KBank JCB and KBank Shopee: 1 K Point per ฿25.

### 2.8 Central The 1 REDZ — UNIQLO isn't a ×3 shop · verified
- Outside the Central group REDZ earns `ทุกยอดใช้จ่าย 25 บาทต่อเซลล์สลิป … รับ 1 คะแนนเดอะวัน` ≈ 0.5% ([[the1]]).
- Its mall bonus `cpn-x3-202308` ("รับคะแนนเดอะวันสูงสุด x4* ณ ร้านค้าที่ร่วมรายการ ที่ ศูนย์การค้าเซ็นทรัล ทั่วประเทศ", to 31 Dec 2026) pays ×3 on REDZ, but only at listed shops. The shop list ([x4-202609.pdf](https://www.centralthe1card.com/getmedia/d85d8b10-d499-4b48-93a2-21c17ead3b8d/x4-202609.pdf), 8 pages, read today) names Central Chiangmai and Central Chiangmai Airport shops, but **not UNIQLO**. So REDZ stays at 0.5% at UNIQLO.

### 2.9 AEON — no category bonus at UNIQLO · verified
- **NTW1** (Everyday with AEON, AEON World) has a fashion category, but it's a named list: `หมวดสินค้าแฟชั่นและอุปกรณ์กีฬา (เฉพาะร้านค้าโซนพลาซ่าของห้างสรรพสินค้า) ได้แก่ Supersports, REV RUNNR, HOKA, H&M, ร้านค้าในเครือ CMG (…) และ ร้านค้าในเครือ ZARA GROUP (…)` ([NTW1 page](https://www.aeon.co.th/aeon/promotions/happy-monthly-with-aeon-2026/), read today). **No UNIQLO** → ✗.
- AEON World's 5% is supermarkets only. Primo and World earn 1 pt / ฿20 and 1 pt / ฿30; AEON's no-points list (5411 caps, 5814, 7999, 8062 …) has no clothing MCC (verified 3 Oct, [[apple-krungsri-ktc-aeon]]).
- Next Gen's 5% online is ≤ ฿50 a transaction and needs ≥ ฿500 of Scan To Pay in the same cycle.
- AEON 365 วัน (Next Gen, UnionPay; principal only): ≥ ฿3,000 full-pay spend in a month → food vouchers ≈ ฿190 the next month (verified 3 Oct, [[all-spend-apple]] §7). A ฿3,000 UNIQLO slip on Takumi's **AEON Next Gen** would complete it (reading: no category exclusion).

### 2.10 Lotus's Beyond — SMP1 names UNIQLO, but it isn't registered · verified
- [SMP1 page](https://www.lotussmoney.com/promotion/credit-card/shopping/cashback-nationwide), read today (1 Sep – 31 Dec 69): `สินค้าแฟชั่น อาทิ H&M, AIIZ, ZARA, Chanel, Louis Vuitton, UNIQLO, Decathlon, Anello`.
  - Per month, the single highest tier pays: ฿70 per whole ฿3,500 (≤ ฿350), or ฿450 per whole ฿25,000, or ฿2,600 from ฿150,000.
  - Caps: ฿2,600 a month. For the campaign, the headline says `สูงสุด 14,000 บาท/ บัญชีบัตรหลัก/ ตลอดรายการ` while the conditions say `ไม่เกิน 10,400 บาท` (the same mismatch [[krungsri-group]] §4.3 found). Neither binds at UNIQLO sizes.
  - Register (`SMP1`, UCHOOSE or SMS → 081-250-7777) within the day of the purchase, once for the campaign. **The household isn't registered** ([[../../promotions/lotuss-lbs3]] lists only LBS3).
- **SMT2** (same page): `เฉพาะ 500 สิทธิ์ ที่ลงทะเบียนผ่าน UCHOOSE สำเร็จ … ก่อนทำรายการ ระหว่างวันที่ 1 ต.ค. 2569 – 31 ต.ค. 2569` → ฿200 at ≥ ฿2,000 in the month. Check the rights left in UCHOOSE first.
- **At UNIQLO**: a ฿3,000 slip → SMT2 ฿200 (6.7%) + SMP1 ฿0 (under ฿3,500); ฿6,000 → ฿200 + ฿70 (4.5%); ฿12,000 → ฿200 + ฿210 (3.4%). Plus 0.25 coin per ฿50.
- Online at uniqlo.com counts too. Only marketplaces and foreign-registered sites are excluded, and the household's online UNIQLO slip posts as a Thai company (§0) (reading).
- `ไม่สามารถเข้าร่วมกับรายการส่งเสริมการขายอื่นได้ ผู้ถือบัตรไม่สามารถนำยอดใช้จ่ายที่เข้าร่วมรายการส่งเสริมการขายอื่นของบริษัทฯ มารวมคำนวณ…` sits in the **joint** SMP1/SMT2 conditions (`*/**ข้อกำหนดและเงื่อนไขรวม`), so SMP1 and SMT2 stack with each other (reading). It rules out counting the same spend in another Lotus's campaign, e.g. LBS3 (see §3).
- Lotus's runs no UNIQLO-named campaign, so for Lotus's Beyond this is the only UNIQLO money. It needs a registration the household hasn't made.

### 2.11 Krungsri VISA / JCB / Lady, KTC, UOB Makro, CardX · verified (2–3 Oct)
- **Krungsri Card**: 1 กรุงศรี พอยต์ per ฿25 a slip (฿0.10). The exclusions (7-Eleven/TrueMoney-linked, utilities, insurance, foreign-THB …) have no fashion item.
  - Krungsri's `2x-platinum` (×2 at department stores and supermarkets, Jul–Dec) needs a department-store MCC; UNIQLO's own stores don't post as one (reading).
  - `point-cashback` (PT26, points → cashback 10%) is the normal ฿0.10 a point, not a bonus.
- **KTC Digital VISA / JCB / Mastercard**: 1 pt / ฿25 (1,000 = ฿100). Rule (16) applies only to KTC UnionPay, and lists 5399 and 5411, not 5651 / 5691 / 5699 / 5311 ([[../../sources/ktc-forever-terms-2026-09-28.txt|KTC FOREVER terms]]). It doesn't matter here, since UnionPay isn't accepted.
- **UOB Makro**: 1 pt / ฿25.
- **CardX JCB**: 1 POINTX / ฿25.

---

## 3. The stacking question — does "ใช้ร่วมกับโปรโมชั่นอื่นไม่ได้" kill a card's own cashback?

**Short answer: no official clarification exists, but the clause appears in fewer places than assumed. The household's own statements show the banks paying both.** Plan on the card's base rate arriving on top, and flag one real risk: Krungsri NOW's 5% with UNQ.

### 3.1 What each UNIQLO-named campaign actually says (read today)

| Campaign | "Not combinable" line? | Verbatim · source |
|---|---|---|
| **UNO** (UOB) | **Yes**, in the general conditions covering all three parts | `ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้` — and `โดยไม่รวมสาขาที่อยู่ใน department store, รายการ UOB LADY LUXE PAY` · [uniqlo.com/…/uob](https://www.uniqlo.com/th/th/special-feature/cp/promotion/uob) |
| **UNQ** (Krungsri) | **Not in the cashback section.** It's in the two other sections: points → 10% cashback, and the JCB 3× / 5× points | cashback section ends at the registration line; `รายการส่งเสริมการขายนี้ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้` appears under `**เงื่อนไขการแลกคะแนนรับเครดิตเงินคืน 10%` and `*** เงื่อนไขรับกรุงศรี พอยต์สะสมสูงสุด 3 เท่า` · [uniqlo.com/…/krungsri](https://www.uniqlo.com/th/th/special-feature/cp/promotion/krungsri) |
| **UQN** (KBank) | **No** | exclusions are only `KBank Smart Pay 0% และ Smart Pay by Phone 0% รายการใช้จ่ายผ่านออนไลน์อื่นๆ ที่ไม่ร่วมรายการ และยอดใช้จ่ายที่ชำระเงินผ่าน E-Wallet`, cancellations and refunds · [uniqlo.com/…/kbank](https://www.uniqlo.com/th/th/special-feature/cp/promotion/kbank); KBank's own UQN page (rendered by a sibling researcher today) has no such line either |
| **UQCB** (ttb) | **No** | the terms carry no combination clause at all · [ttbbank.com/…/uniqlo-oct26](https://www.ttbbank.com/th/promotion/credit-card/shopping/uniqlo-oct26) |

This corrects [[../../promotions/uniqlo-2026]], which says "UOB, Krungsri and KBank all say their UNIQLO cashback can't combine with other promotions". On the pages read today, only UOB's UNO cashback says so.

### 3.2 What the card benefits say

- **UOB One 1%**: no clause in its cashback section (§2.4).
- **ttb so smart 1%**: no clause (§2.5).
- **First Choice NW4**: no clause (§2.2).
- **KBank PLUSTINUM ×3**: no clause (§2.6).
- **Krungsri NOW 5%**: **has one**: `รายการส่งเสริมการขายนี้ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้` ([NOW page](https://www.krungsricard.com/th/product/creditcard/now)).

### 3.3 The nearest thing to an official clarification

- **Lotus's (a Krungsri Consumer partner)** spells out what its clause means, on the SMP1/SMT2 page: `รายการส่งเสริมการขายนี้ไม่สามารถเข้าร่วมกับรายการส่งเสริมการขายอื่นได้ ผู้ถือบัตรไม่สามารถนำยอดใช้จ่ายที่เข้าร่วมรายการส่งเสริมการขายอื่นของบริษัทฯ มารวมคำนวณเพื่อรับสิทธิประโยชน์ในรายการส่งเสริมการขายนี้ได้อีก` ([page](https://www.lotussmoney.com/promotion/credit-card/shopping/cashback-nationwide)).
  - That limits it to spend already counted in **the same company's other promotions**. Read that way, UNO can't stop ttb's 1%, and UQCB can't stop UOB's.
- **No bank page found says** "ยกเว้นสิทธิประโยชน์ปกติของบัตร", or that the card's own cashback or points are kept or lost. Searches in Thai and English found nothing from UOB, Krungsri, KBank or ttb (not found).

### 3.4 Household evidence (the banks paid both)

- **Krungsri**: SUP1 and NOW both carry "not combinable" lines, and both paid on Baiboon's ฿4,159 Makro PRO slip on Krungsri NOW in September 2026 (฿120 + ฿200). J Dining and EAT both paid on one Sushiro slip ([[../../promotions/krungsri-card-2026]], "Stacking").
- **UOB**:
  - UOB One's 1% is credited within each statement cycle. July, August and September 2026 reproduce to the satang, including lines that also counted toward EPW538 ([[../../promotions/uob-one-2026]]). EPW538's terms carry a "not combinable / best one per category" line.
  - EPW-series credits were paid on Nuta's UOB One spend for Jan–May 2026 ([[../../promotions/uob-epw538]]), and no 1% claw-back has been seen.
  - UNO pays **within 60 days after 28 Feb 2027**, long after each cycle's 1% has posted.
- **ttb**: the so smart 1% goes to a savings account, separately from any card-statement campaign credit (`cards/ttb-so-smart.yaml`).

### 3.5 Verdict per pair (reading)

| Pair on one UNIQLO slip | Expect | Why |
|---|---|---|
| UNO + UOB One 1% | both | 1% is a card feature with no clause, credited per cycle months before UNO; household precedent with EPW |
| UNO + UOB World ×2 / ×5 points | both | points are the card's earning, not a promotion; no UOB page withholds points on UNO slips |
| UQCB + ttb so smart 1% | both | neither has a clause |
| UQN + KBank PLUSTINUM ×3 bonus / LINE Points 1% | both | neither has a clause; UQN itself adds K Point on top |
| UNQ + Krungsri points | both, except on the NOW card's online rows (no points there anyway) | UNQ's cashback section has no clause |
| **UNQ + Krungsri NOW 5% online** | **risk: maybe only one** | NOW's own clause; both are Krungsri Card per-slip credits on the same slip. Household precedent (NOW + SUP1, Sep 2026) says both paid. If only one pays, they tie at ฿3,000 and ฿6,000 (฿150, ฿300), and UNQ wins from ฿9,000 (฿450, then ฿700 at ฿10,000, against NOW's ฿300 monthly cap) |
| UNQ vs ONQ3 | n/a | ONQ3 counts only marketplaces and card payments through wallets. A uniqlo.com card payment is neither, so ONQ3 never pays at UNIQLO |
| Any UNIQLO campaign + First Choice NW4 | n/a | no UNIQLO campaign takes First Choice. NW4 alone on First Choice |

---

## 4. Offers that name no merchant, from every issuer

Checked against UNIQLO's payment rules (§0: Visa / Mastercard / JCB only, no wallets officially, no credit-card QR, no installments online) and its MCC (5651 most likely; own stores in Central Pattana malls, not department-store counters).

### 4.1 Ranked: what a UNIQLO slip earns from offers that name no merchant

| # | Offer · issuer | 🏠 | In store (Chiang Mai) | uniqlo.com / app | ≈ ฿ on 3k / 6k / 12k | Caps · conditions | Conf. |
|---|---|---|---|---|---|---|---|
| B1 | **Lotus's SMT2** (฿200 once at ≥ ฿2,000 in Oct) + **SMP1** ladder | 🏠 Takumi (Lotus's Beyond), **not registered** | ✓ (SMP1 names UNIQLO among its fashion examples) | ✓ (reading) | **200 / 270 / 410** | SMT2: first 500 accounts, register **before** spending, Oct only. SMP1: ฿70 per whole ฿3,500, highest tier only, ≤ ฿2,600/month. Installments, marketplaces ✗ | verified |
| B2 | **Krungsri NOW 5% online** | 🏠 Takumi | ✗ | ✓ | 150 / 300 / 300 | ฿300/month; ฿25 per whole ฿500 a slip; no points on the row | verified |
| B3 | **First Choice NW4** | 🏠 all three (pooled) | ✓ | ✓ | +150 / +150 / +350 (from today's ฿8,648) | 2% at the margin in whole ฿10,000 steps; ≤ ฿2,000/month | verified |
| B4 | **Krungsri `all-plaza`** — redeem points (≤ the slip) for **13% Mon–Thu / 15% Fri–Sun** cashback at plaza-zone shops of every Central mall, incl. Central Chiangmai and Central Chiangmai Airport | 🏠 Takumi's Krungsri VISA / JCB / Lady / NOW (principal accounts; Baiboon's supplement spend counts to his) | ✓ (UNIQLO's Chiang Mai stores are plaza-zone units — reading) | ✗ (Central App etc. excluded; uniqlo.com isn't a mall shop) | burn: ฿390 / ฿780 / ฿1,560 back for 3,000 / 6,000 / 12,000 points (15%), against ฿300 / ฿600 / ฿1,200 at the normal ฿0.10 | slip ≥ ฿1,000; redeem by USSD `*465*12581*<last 4>*<points>#` after paying, within the day; ≤ 100,000 points/month; credited within 90 days; department stores, e-wallets, installments excluded; 1 Oct – 31 Dec 69; no "not combinable" line | verified · reading (UNIQLO = plaza-zone shop) |
| B5 | **UOB World ×5 online** | 🏠 Takumi, Baiboon | ✗ (×2) | ✓ | online 62 / 125 / 250 | inside the shared ≈ ฿20,000/cycle quota | household + verified (2 Oct) |
| B6 | **Lotus's invited Q4 segments** (`small-ticket-a/b-q4-26`) | 🏠 Takumi, **if invited** (shows only in UCHOOSE) | ✓ (reading: no fashion exclusion) | ✓ (reading) | — / 125 / 250 (a: ฿125 at ฿5,000–9,999, ฿250 at ฿10,000–49,999 a slip) | invitation only; wallets, installments, hospitals ✗ | verified (2 Oct, [[all-spend-hospital-spa]] §3.1) · unverified (invitation) |
| B7 | **Central The 1 `TNL` "ช้อปคุ้ม ทุกคลิก"** — online category | 🏠 Takumi, Baiboon (REDZ), registration unknown | ✗ | ? (uniqlo.com in "หมวดช้อปออนไลน์ที่ร่วมรายการ" isn't stated) | **10 Oct only**: ×5 The 1 points on an online slip ≥ ฿5,000 ≈ 2.5% → — / 150 / 300; the cashback ladder needs ≥ ฿15,000 and 5 shops a month | register `TNL` (SMS → 081-278-2222 or UCHOOSE) within the day; ≤ 3,000 bonus points a day; Central-group shops excluded (UNIQLO isn't one); 1 Aug – 31 Oct 69 | verified (terms + poster) · unverified (uniqlo.com counts) |
| B8 | **KBank PLUSTINUM** ×3 bonus + monthly gifts | 🏠 Takumi | ✓ | ✓ | 16 / 60 / 112 in points; + ฿200 coupon if the month reaches ฿10,000 | §2.6 | verified |
| B9 | **AEON 365 วัน** (≥ ฿3,000 full-pay in a month → ≈ ฿190 of food vouchers) | 🏠 Takumi, Baiboon (AEON Next Gen; principal only) | ✓ (no category exclusion) | ✓ | ≈ 190 / 190 / 190 | Next Gen must be a network UNIQLO takes (it isn't UnionPay — reading); vouchers, not cash; pooled quotas | verified (3 Oct) |
| B10 | UOB One 1% · ttb so smart 1% | 🏠 | ✓ | ✓ | 30 / 60 / 120 | §2.4–2.5 | verified (2–3 Oct) |
| B11 | KBank LINE Points on-top | 🏠 Takumi | ✓ | ✓ | +50 LINE POINTS at ฿5,000, +200 at ฿15,000 in the month | registered; Sep–Dec | verified (2 Oct) |
| — | *Not held* | | | | | | |
| N1 | **ttb Disney 5× points** (dining, supermarkets, **online**, not e-wallet) | — | ✗ | ✓ ≈ 2% (at ฿0.10 a point; value unpublished) | 60 / 120 / 240 | needs 3 slips ≥ ฿1,000 in the cycle; bonus ≤ 3,000 pts/cycle | verified (1 Oct, [[all-spend]] B5) |
| N2 | **ttb all free Disney debit** 1% online (2% on 10 Oct) | — | ✗ | ✓ (UNIQLO takes Visa/Mastercard debit) | 30 / 60 / 120 (×2 on 10 Oct) | ≥ ฿2,000 online in the month; ≤ ฿300/account/month | verified (1 Oct, [[all-spend]] B9) |
| N3 | **Bangkok Bank Titanium** (Mastercard) tiered cashback instead of points | — | ✓ | ✓ | 15 / 30 / 60 (0.5% band) | per cycle 0.5% to ฿25,000 … 2% above ฿200,000; ≤ ฿2,000/card/cycle; counts Be Smart installments | verified (2 Oct) |
| N4 | ttb so fast / ttb reserve (1 pt / ฿10) | — | ✓ ≈ 1% | ✓ | ≈ 30 / 60 / 120 | so fast ≤ 20,000 pts/cycle; reserve 10,000 pts = ฿1,000 | verified (1 Oct) |
| N5 | **UOB KrisFlyer** bonus miles on fashion + dining + department stores (`CKF`) | — | ✓ (5651, 5691, 5699 listed) | ✓ (Thai merchant) | extra miles only per whole ฿20,000 a month in those categories | World Elite 1 mile/฿20, World 1 mile/฿25; ≤ ฿200,000/month; register first; 1 Aug 69 – 31 Jan 70 | verified ([page](https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/kf-bonus-mile-kpw630-0127.page)) |
| N6 | KTC Cash Back cards | — | ≤ 0.8% | ≤ 0.8% | ≤ 24 / 48 / 96 | — | verified (1 Oct) |
| N7 | ICBC ANY Mastercard 6% online | — | ✗ | ✓ | ≤ 30 a slip | — | verified (3 Oct, [[all-spend-apple]] §7) |
| ✗ | **Bangkok Bank UnionPay 2%** (≥ ฿2,000/month anywhere except China) | — | **✗ UNIQLO takes no UnionPay** | ✗ (logos: Visa, Mastercard, JCB) | 0 | the user's example offer doesn't work here | verified (BBL terms 1 Oct; UNIQLO's payment pages today) |
| ✗ | UnionPay QR 6% (KTC UnionPay) | 🏠 | ✗ (no credit-card QR) | ✗ | 0 | — | verified |
| ✗ | UOB SPW796 / Krungsri ONQ3 / LINE Pay routes | 🏠 | ✗ (wallets not officially supported) | ✗ (no wallets online) | 0 | — | verified |
| ✗ | Krungsri `2x-platinum` (×2 at department stores and supermarkets) · KTC `happiness-forever` (department-store zones) · UOB Premier ×4 (5311/5309) · Krungsri Signature ×5 at Central | 🏠 partly | ✗ (UNIQLO posts under its own name, not 5311) | ✗ | 0 | would matter only at a UNIQLO counter inside a department store | verified (pages) · reading (MCC) |
| ✗ | AEON NTW1 · Central The 1 CPN ×3 · CardX "Fashion" / "Fashion Brands" / "Sports Fashion" | 🏠 partly | ✗ (named lists without UNIQLO) | ✗ | 0 | — | verified |

### 4.2 Issuer sweep (what exists in October, and why it does or doesn't reach UNIQLO)

- **Krungsri Card** (507 listings today):
  - No all-spend or spend-threshold campaign.
  - `all-plaza` (B4) is the only offer that names no merchant and reaches a Chiang Mai UNIQLO store. It's a points burn.
  - `premium-plaza-fashion` (to 18%) covers Bangkok premium malls only (Central Embassy, Emporium, EmQuartier, Paragon, ICONSIAM …).
  - `point-cashback` (PT26) is the normal ฿0.10 a point.
- **First Choice**: NW4 (B3). RSF2's 3% "anywhere Visa" is for the loan-line cards only (not held) · verified (2 Oct).
- **Central The 1**: `TNL` (B7). `cpn-x3-202308` doesn't list UNIQLO (§2.8). REDZ's base is 0.5%.
- **Lotus's**: SMP1 + SMT2 (B1, unregistered); invited segments (B6).
- **KBank**: PLUSTINUM ×3 fashion bonus, monthly coupon, Season 3; LINE Points 1% + on-top. No all-spend cashback in the campaign list (verified 2–3 Oct).
- **UOB** (628 items in `data-promotion.json`, read today):
  - No all-spend or spend-threshold campaign for October.
  - Fashion appears only in **FPW356** "Fashion PWP" (points → 10–13% at named fashion brands; UNIQLO's own `PPF` is the UNIQLO-named version) and the KrisFlyer miles bonus (N5).
  - Q4 new-card offer: nobody qualifies (§4.4).
- **ttb**: so smart 1% (household). Disney 5× online (N1). The so fast / reserve base (N4). Joy of Shopping (10% points burn at participating malls, all 2026) is for points cards; so smart earns none · verified (1 Oct, [[../../promotions/ttb-2026]]).
- **CardX / SCB** (CardX's search index, read through a sibling researcher's dump today):
  - Public offers that name no merchant are King Power card offers (not held) and welcome offers.
  - The October threshold offers are **invitation-only**:
    - `CDM3` "ใช้ CardX ใบโปรด รับกาแฟแก้วโปรด": Starbucks ฿200–600 at ฿10,000 / ฿30,000;
    - `cc-jump-retail-high-cb-oct-2026`: ฿500 at ฿50,000 … ฿2,500 at ฿200,000, plus Starbucks ฿200 for ≥ ฿5,000 on 25–31 Oct.
  - Whether Nuta was invited shows only in the CardX app (unverified).
- **KTC**: no all-spend or threshold campaign. The department-store and shopping category pages (read today) list only department-store, mall-specific (outside Chiang Mai) and named-brand offers. Its UNIQLO money is KTC JCB's named ×2–×5 (sibling report).
- **AEON**: 365 วัน (B9); NTW1 ✗; no all-spend cashback.
- **Bangkok Bank** (147 slugs in the sibling's dump): UnionPay 2% ✗ (network); Titanium (N3). "Retail_Fashion" is a named-brand points burn (sibling report).
- **GSB, Krungthai, CIMB, KKP, TISCO, LH Bank**: no all-spend campaign found (verified 2 Oct, [[all-spend-hospital-spa]] §3.9). GSB Online Festival counts partner online/delivery/wallet spend only.
- **Card networks**:
  - **UnionPay**: unusable at UNIQLO.
  - **Visa and Mastercard**: their Thai offer feeds had nothing fashion-wide or UNIQLO on 3 Oct (57 Visa perks, 72 Priceless offers: travel, dining, shopping abroad) · verified (3 Oct, [[apple-wallets-networks-welcome]] §3).
  - **JCB**: Thailand's listing (`specialoffers.jcb`) timed out today, directly and through r.jina.ai. On 3 Oct it had 55 entries and no all-spend offer.

### 4.3 Welcome offers a UNIQLO spend helps complete

Eligibility is as analysed in [[apple-wallets-networks-welcome]] §4 (verified 3 Oct unless marked):
- Takumi and Baiboon hold UOB, KBank, KTC, ttb, Krungsri Card, First Choice, Central The 1, Lotus's and AEON.
- Nuta holds supplements only (UOB One, AEON UnionPay, First Choice, CardX JCB, KTC UnionPay).
- **Check the new card's network**: UNIQLO takes Visa, Mastercard and JCB only.

| Offer | Window | Spend needed | Reward | ฿3k / ฿6k / ฿12k at UNIQLO completes? | Who | Conf. |
|---|---|---|---|---|---|---|
| **Krungsri Card** (website application) | approved 1 Oct 69 – 31 Jan 70 | ≥ ฿5,000 + e-Statement (or a Grab/LINE MAN/Shopee link), or ≥ ฿7,000, within 30 days | VR ROAM bag ฿2,590 | ✗ / **✓ (with e-Statement)** / ✓ | Nuta | verified (3 Oct); "ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้" |
| **GSB Welcome No.5** | applied with e-Statement 1 Mar – 31 Dec 69 | ≥ ฿5,555 within 55 days, principal | Caggioni 20" case ฿5,290 (5,555 GSB points) | ✗ / ✓ / ✓ | all three | verified (3 Oct) |
| **Lotus's** new card | applied 1 Sep – 30 Nov 69 | ≥ ฿8,000 within 60 days + e-Statement | Pochacco 20" case ฿5,590 | ✗ / ✗ / ✓ (and SMP1 names UNIQLO) | Nuta | verified (3 Oct) |
| **Central The 1 REDZ** | applications 1 Aug – 31 Oct 69 | ฿8,000–29,999 / ≥ ฿30,000 within 45 days | bag ฿2,590 / 24" case ฿6,990 | ✗ / ✗ / ✓ (bag) | Nuta | verified 1 Oct only (GO's copy); not on the centralthe1card.com list today |
| **CardX** first principal (`C6902030`) | approved by 31 Dec 69, via the CardX app | ≥ ฿5,000 within 30 days | Starbucks ฿500 (+ ฿1,000 for a 3-cycle auto-debit) | ✗ / ✓ / ✓ (CardX JCB is accepted) | Baiboon | verified (3 Oct); live in the index today |
| **Bangkok Bank AirAsia** | 1 Aug 69 – 31 Jul 70 | ฿100 per ฿5,000 within 60 days | ≤ ฿200 | 0 / 100 / 200 | all three (new to BBL) | verified (1 Oct) |
| **Bangkok Bank M Visa** (M LUXE / M LIVE) | 1 Jul – 31 Dec 69 | ≥ ฿10,000 within 60 days | CAGGIONI suitcase ฿4,590 | ✗ / ✗ / ✓ | all three | verified (1 Oct) |
| KBank `NCCS260871` | approved 1 Aug 69 – 31 Jan 70 | ≥ ฿15,000 / ≥ ฿30,000 within 30 days | 5,000 / 12,000 K Point | ✗ alone | Nuta | verified (3 Oct) |
| ttb so smart / so fast / absolute / Disney | approved by **31 Oct 69** | ≥ ฿15,000 within 30 days, full pay | ฿500 + 1% / 7,500 pts / bags | ✗ alone | Nuta | verified (3 Oct) |
| KTC JCB new principal | applied 1 Sep – 31 Dec 69 | 3 transactions within 30 days | GrabFood ฿500 (5 × ฿100) | ✓ any 3 slips | Baiboon, Nuta (reading) | verified (3 Oct) |
| UOB One / World Q4 | applied 1 Oct – 31 Dec 69 | ≥ ฿5,000 within 60 days | ฿2,000 / ฿1,500 | — | nobody (all hold UOB) | verified (3 Oct) |

---

## 5. What this means for the UNIQLO page's plan

- **The card's own rate rarely beats the UNIQLO campaigns on a slip of ฿3,000 or more.** It mostly decides the tie-breaks:
  - **Online, under ฿3,000 or on top**: Krungsri NOW (5%) is the best household card on uniqlo.com/app; its ฿300 a month is untouched. Paying ≥ ฿3,000 on NOW also earns UNQ (฿150 per ฿3,000) unless NOW's "not combinable" bites (§3).
  - **In store**: First Choice is worth +฿150 on a slip that takes the pooled month past ฿10,000 (NW4). UOB One and ttb so smart add 1% on top of UNO and UQCB. KBank PLUSTINUM adds up to 1.2% in points on top of UQN.
- **Lotus's SMT2 is the best offer that names no merchant for a small UNIQLO spend** (฿200 on ≥ ฿2,000, 6.7% at ฿3,000). It needs registration **before** spending and is first come, first served (500 accounts). Lotus's has no UNIQLO-named campaign, so it doesn't clash with one.
- **Krungsri's `all-plaza`** lifts Krungsri points to ฿0.13–0.15 at the Chiang Mai stores (Fri–Sun best). It beats UNQ's own points → 10% option. Show it as "ถ้ามีคะแนนเหลือ" (if points are left), without anyone's balance.
- **Bangkok Bank UnionPay 2% doesn't apply.** UNIQLO takes no UnionPay, so the page shouldn't suggest it. Neither do the household's KTC UnionPay / UnionPay QR or any wallet route.
- **New cards**: for Nuta, ฿6,000 at UNIQLO completes the Krungsri Card bag (with e-Statement) and the GSB case. ฿12,000 adds Lotus's case and REDZ's bag (REDZ applications close 31 Oct).

## What couldn't be found

- **UNIQLO's MCC**: no issuer or lookup states it. 5651 is the reading, and every listed fashion MCC gives the same answer.
- **An official clarification of "not combinable"** vs a card's own cashback or points: none from UOB, Krungsri, KBank or ttb (§3). Only Lotus's wording scopes it to the same company's promotions.
- **UnionPay at UNIQLO stores**: the store page says "such as Visa, Mastercard, and JCB". UnionPay isn't named, and no store-side confirmation was found (online is Visa/Mastercard/JCB only).
- **Whether uniqlo.com is in Central The 1 TNL's "หมวดช้อปออนไลน์"**, and whether the household's REDZ is registered for TNL.
- **JCB's Thai offer listing**: unreachable today.
- **Lotus's invitations and CardX's invite-only October offers**: they show only in UCHOOSE / the CardX app.
- **AEON Next Gen's network**: whether it's a network UNIQLO takes wasn't checked.

## Site methods

- **UNIQLO's bank pages** (`uniqlo.com/th/th/special-feature/cp/promotion/<bank>`) return 403 to curl even with a cookie jar, but **`r.jina.ai/<url>`** reads them in full, with the terms text, not just the banners.
- **UNIQLO's FAQ** (`faq-th.uniqlo.com/pkb_Home_UQ_TH?id=<article>&l=en_US`) reads through r.jina.ai. The payment articles are `kA0Ie000000TPQl` (store), `kA0Ie000000TOqj` (online) and `kA0Ie000000TOk4` (cards). The accepted-card logos are an image (`/servlet/rtaImage?…`) that curl downloads.
- **Store list**: UNIQLO's store-locator JSON (a sibling researcher saved it as `st-local-0.json`) gives each store's mall, room and floor, and so whether a branch is a mall unit or a department-store counter.
- **Krungsri mall-wide points burns** (`/th/promotion/all-plaza`, `/premium-plaza-fashion`) read with plain curl; the mall list and the exclusions (department stores, Central App, e-wallets) are plain text, and the USSD redemption code is in the table. The Krungsri listing JSON has **no UNQ entry**: Krungsri publishes UNQ only on UNIQLO's site.
- **UOB's `data-promotion.json`** has no UNO entry either (UNO lives on UNIQLO's site); the KrisFlyer fashion bonus (`kf-bonus-mile-kpw630-0127`) has a working `.json` twin with its MCC list.
- **Central The 1 TNL's poster** (`/getattachment/a02ec1e3-…/AW-NTW-NationwideQ3_26-Online_WEB1024.webp`) carries the SMS number (`TNL` → 081-278-2222) and the 5-shops rule, which the terms text words differently.
- **Reuse sibling dumps**: on 5 Oct the CardX search index (`cx-live.json`, 1,000 hits sorted by expiry), Bangkok Bank's full listing (`bbl-all.txt`) and UNIQLO's store list were already in `scratchpad/uniqlo-banks-a/`; filtering them saved re-rendering.
- **JCB** (`specialoffers.jcb`) timed out both directly and through r.jina.ai on 5 Oct.
- **KBank PLUSTINUM's ×3 MCC list** is in the rendered card page (headless Chrome, desktop UA, `--virtual-time-budget=25000`), under "รายละเอียดและเงื่อนไข" of "PLUS K Point X3".
