---
tags: [catalogue-research, 2026-10]
researched: 2026-10-05
---

> **Research snapshot**: UNIQLO — UOB, KBank, ttb, CardX / SCB, other banks and the card networks — October 2026 research. Scope: every payment promotion at UNIQLO Thailand in October 2026 from UOB, KBank, ttb, CardX / SCB, Bangkok Bank and the other Thai banks outside the Krungsri group, KTC and AEON, plus Visa, Mastercard, JCB and UnionPay (and JCB-card offers at UNIQLO in Japan, briefly). Read on **2026-10-05** from the official pages, for the October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions (HTML, JSON, posters) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# UNIQLO — UOB, KBank, ttb, CardX and other banks — October 2026 (ต.ค. 69)

🏠 = a card the household holds. Household cards in scope: UOB One / World / Premier / Makro (Takumi's accounts; Nuta only UOB One), KBank JCB / LINE Points / PLUSTINUM / Shopee, ttb so smart, CardX JCB (Nuta). The Bureau declarations are in `scripts/python/lib/bureau/uniqlo.py`; the household reading is [[../../promotions/uniqlo-2026]]. Krungsri, First Choice, KTC and AEON are in a sibling report; UNIQLO's own deals and the wallets in another; all-spend offers in [[all-spend-uniqlo]].

**Confidence labels**: **V** = verified on the official page (bank's own page, or UNIQLO's copy of the bank's terms) · **T** = third-party only · **U** = unverified / inferred.

## At a glance

| Code | Issuer | Per slip | Monthly cap | Campaign cap | Register | Period | Conf. |
|---|---|---|---|---|---|---|---|
| **UNO** | UOB 🏠 | ฿150 per whole ฿3,000 (≤ ฿450); ฿800 from ฿12,000 | ฿800 | ฿4,000 per cardholder (primary + supplements) | SMS `UNO <last 12>` → 4545111 or Rewards+, **every time, within the day** | 1 Oct 26 – 28 Feb 27 | V |
| **UQN** | KBank 🏠 | ฿100 / 200 / 300 at ฿3,000 / 6,000 / 9,000; ฿600 from ฿12,000 (+200 / 400 / 600 K Point) | ฿600 "/ ท่าน" | ฿3,000 | once, before spending: K PLUS or SMS `UQN <last 12>` → 4545888 | 1 Oct 26 – 28 Feb 27 | V |
| **UQCB** | ttb 🏠 | ฿150 per ฿3,000 (≤ ฿450); ฿800 from ฿12,000 | ฿800 / ท่าน | ฿4,000 / ท่าน | once: ttb touch or SMS `UQCB <last 12>` → 4899777 | 1 Oct 26 – 28 Feb 27 | V |
| **UQC** (new) | CardX / SCB WEALTH 🏠 | ฿120 per whole ฿3,000; **฿700 from ฿10,000** | ฿700 / ท่าน | ฿3,500 / ท่าน | once: CardX app/web or SMS `UQC <last 12>` → 4545777 | 1 Oct 26 – 28 Feb 27 | V |

Points-for-cashback halves at UNIQLO: UOB `PPF` 10% (13% on Reserve/Infinite/Zenith), CardX `UQB` 10% (20% on SCB WEALTH at weekends), ttb `UQBP` 12%. Mall-wide points cash-outs that reach UNIQLO stores: KBank `BCB` 10% (incl. Central Pattana malls, so both Chiang Mai stores), GSB `GSPD` 13% (Bangkok/Pattaya malls only).

Cashback per slip, as a share of the slip, at the break points:

| Slip | UOB UNO | ttb UQCB | KBank UQN | CardX UQC |
|---|---|---|---|---|
| ฿3,000 | ฿150 (5.0%) | ฿150 (5.0%) | ฿100 (3.3%) + 200 K Point | ฿120 (4.0%) |
| ฿6,000 | ฿300 (5.0%) | ฿300 (5.0%) | ฿200 (3.3%) + 400 K Point | ฿240 (4.0%) |
| ฿9,000 | ฿450 (5.0%) | ฿450 (5.0%) | ฿300 (3.3%) + 600 K Point | ฿360 (4.0%) |
| ฿10,000 | ฿450 (4.5%) | ฿450 (4.5%) | ฿300 (3.0%) + 600 K Point | **฿700 (7.0%)** |
| ฿12,000 | **฿800 (6.7%)** | **฿800 (6.7%)** | ฿600 (5.0%) | ฿700 (5.8%) |

UNIQLO's own hub, <https://www.uniqlo.com/th/th/special-feature/cp/promotion> ("Credit Card Promotion 1 ต.ค. 2569 – 28 ก.พ. 2570", "สิทธิพิเศษเมื่อซื้อสินค้าตั้งแต่ 3,000 บาทขึ้นไปที่ร้านสาขาหรือออนไลน์สโตร์"), lists exactly six banks: **CardX | SCB, KBank, Krungsri, KTC, ttb, UOB**. Its ttb page is new since 1 Oct. Other slugs tried on 5 Oct: `scb`, `bbl`, `bangkokbank`, `gsb`, `ktb`, `citi`, `amex`, `jcb`, `aeon`, `mastercard`, `lhbank` → 404; `central`, `firstchoice`, `visa`, `unionpay` → only Akamai 403s (not resolved).

## 1. UOB — UNO (cashback), Top Spender, PPF (points → cashback)

Source: <https://www.uniqlo.com/th/th/special-feature/cp/promotion/uob> (UNIQLO's copy of UOB's terms + banner, UOB ref `26UC75`), read 2026-10-05. **V**. Matches the repo facts.

**UOB's own site doesn't list it.** UOB's `data-promotion.json` (628 items on 5 Oct) has no entry naming UNIQLO; the related fashion-points page FPW356 (below) doesn't list UNIQLO either. UNIQLO's page is the only official copy found.

Period **1 Oct 2026 – 28 Feb 2027**. Cards: every Thai-issued UOB credit card except business cards 🏠 (UOB One, World, Premier, Makro).

### ต่อที่ 1 — cashback per slip (`UNO`)

| Spend per sales slip | Cashback |
|---|---|
| every whole ฿3,000 (under ฿12,000) | ฿150 — so ฿150 / 300 / 450 |
| ฿12,000 or more | ฿800 |

- Caps: **฿800 a month**; **฿4,000 per cardholder for the campaign** ("จำกัดเครดิตเงินคืนสูงสุด 4,000 บาท/ลูกค้า/ตลอดรายการ (รวมทุกประเภทบัตรเครดิตทั้งบัตรหลักและบัตรเสริม)").
- Pooling: spend on a primary card and its supplements billed to the same holder is counted in the primary's account; a holder with several primary cards has them pooled. So all three people's UOB UNIQLO slips share Takumi's ฿800 a month.
- Registration: **every time, within the transaction day**. Send SMS `UNO <last 12 digits>` to **4545111**, or use Rewards+ in UOB TMRW (free). The banner says "ก่อนชำระเงินผ่านบัตร" (before paying). UOB Reserve and UOB Infinite need no registration. Registration also enters you for Top Spender.
- Exclusions: UNIQLO **"สาขาที่อยู่ใน department store"** (see the finding below), UOB LADY LUXE PAY, and charges cancelled later. Full-amount spend only, counted by transaction date. The repo also excludes e-wallets and i-Plan; UNIQLO's copy names neither, but "เต็มจำนวน" (full amount) rules out installments.
- Crediting: within **60 days after the campaign ends** (28 Feb 2027), to a primary card the bank chooses.
- **Not combinable** ("ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้"). Open question: whether this withholds UOB One's own card cashback on the same slip.

### ต่อที่ 2 — Top Spender

The 5 highest UOB spenders at UNIQLO over the campaign (minimum ฿10,000) each get a 20-inch suitcase worth ฿6,800 (1 per cardholder, 5 in all; ties go to whoever reached it first). Delivered within 60 days after the campaign.

### ต่อที่ 3 — points for cashback (`PPF`)

| Card | Cashback for points equal to the net slip |
|---|---|
| UOB Reserve, UOB Infinite, UOB Zenith | 13% |
| other UOB cards | 10% |

- Minimum ฿500 a slip. At most **50,000 points per cardholder a month**, across every participating fashion brand.
- Register **every time, within the transaction day**: SMS `PPF <last 12 digits> <slip amount>` → 4545111, or Rewards+. It doesn't apply retroactively.
- **Excluded cards**: every supplement, business cards, KrisFlyer World Elite / World, Royal Orchid Plus Preferred / ROP, **UOB One**, UOB Simple, UOB Lazada, **UOB Makro**, TMRW. Of the household's UOB cards only Takumi's own 🏠 **UOB World** and 🏠 **UOB Premier** can use it, at 10%.
- Credited within 60 days after the end of the month of registration.
- Same `PPF` code as UOB's general fashion-brand redemption FPW356 (<https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/fashion-pwp-fpw356-0227.page>, 1 Mar 2026 – 28 Feb 2027, ref `26UB33`). Its brand list (CLUB21, PP Group, Pacifica, H&M, COS, ZARA group, Jaspal …) has no UNIQLO, so UNIQLO's page is what adds it.

### Finding: the department-store exclusion

- **UOB publishes no list of excluded UNIQLO branches.** Neither UNIQLO's UOB page nor UOB's site names one.
- The clause is UOB's fashion boilerplate. FPW356 carries word for word the same "ไม่รวมสาขาที่อยู่ใน department store, รายการ UOB LADY LUXE PAY…". There it is aimed at brands with counters inside department stores, where the department store's till takes the payment.
- **No other bank's UNIQLO page has such a clause.** KBank, ttb, CardX, Krungsri and KTC all say "ทุกสาขา".
- **UNIQLO Thailand's store list** (store-locator API, 74 stores on 5 Oct) shows every store as UNIQLO's own unit with its own POS. They are mall tenants in Central, The Mall, Robinson Lifestyle, Terminal 21, Seacon, Siam Paragon and others, and roadside stores. None is a counter on a department store's sales floor.
- **The two Chiang Mai stores**:
  - **UNIQLO Central Chiangmai** (large store, room 111, 1F, Central Chiangmai, formerly Central Festival Chiangmai). Baiboon's September slip posted as `UNIQLO-CENTRAL CHIANGMA CHIANGMAI TH`, a UNIQLO merchant name and not the department store's.
  - **UNIQLO Central ChiangMai Airport** (rooms 254–255, 2F).
- **MAYA has no UNIQLO.**
- The stores most open to the argument are those named after a department-store group: UNIQLO Robinson Buriram / Chachoengsao / Kanchanaburi / Srisaman, and The Mall Bangkae / Bangkapi / Korat / Ngamwongwan / Thapra. They are still tenant units in the malls.
- **Reading (U)**: no Chiang Mai UNIQLO store looks excluded. The clause should only bite if a slip is charged under a department store's merchant name. Check the merchant name on the first UOB UNIQLO row.

## 2. KBank — UQN (cashback + K Point), plus BCB (K Point → 10% in malls)

### UQN

Sources: KBank's page <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-uniqlo.aspx> (short link `kasikornbank.com/k_uniqlo`, Campaign Code `ACCS261169`, rendered headless 2026-10-05) and UNIQLO's copy <https://www.uniqlo.com/th/th/special-feature/cp/promotion/kbank> (text + banner). **V**. Matches the repo facts.

Period **1 Oct 2026 – 28 Feb 2027**. Cards: every KBank credit card 🏠 (JCB, LINE Points, PLUSTINUM, Shopee) except business cards, corporate cards, Fleet Card and Xpress Cash.

| Spend per sales slip | Cashback | Extra K Point |
|---|---|---|
| ฿3,000 – 5,999 | ฿100 | 200 |
| ฿6,000 – 8,999 | ฿200 | 400 |
| ฿9,000 – 11,999 | ฿300 | 600 |
| ฿12,000 or more | ฿600 | — (none) |

- Caps: cashback **฿600 / ท่าน / month**, **฿3,000 for the campaign**; extra points **1,200 / ท่าน / month**, **6,000 for the campaign**. The page says per person ("ท่าน"); the household counts KBank per card ([[../../promotions/uniqlo-2026]]).
- Registration: **once, before spending** ("กรุณารอได้รับข้อความตอบกลับก่อนทำรายการ"). Use K PLUS → Privilege & Offer → Missions For You, or SMS `UQN <last 12 digits>` → **4545888** (example `UQN 012345678910`). If you registered in K PLUS, the SMS isn't needed. Registration runs 1 Oct 2026 – 28 Feb 2027.
- No extra K Point on the KBank **LINE POINTS** card 🏠 or the Titanium Mastercard.
- Not counted: KBank Smart Pay 0% / Smart Pay by Phone 0% installments; other online channels outside the campaign; payments through e-wallets (TrueMoney, Rabbit LINE Pay, ShopeePay …); cancelled, returned or never-billed charges.
- Crediting: cashback and extra points **within 60 days after the campaign ends**.
- No "not combinable" line. Every UNIQLO store and UNIQLO online counts; no branch exclusion.

### BCB — K Point for 10% cashback at shopping centres (reaches UNIQLO)

Source: <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-complex.aspx>, read 2026-10-05. **V** for the terms. That UNIQLO counts is **U**: the page doesn't name shops.

- Mechanic: 10% cashback for K Point equal to the spend, at **any EDC shop inside a participating shopping centre**. The centres include **Central Pattana (CPN)** (so Central Chiangmai and Central ChiangMai Airport), Central Embassy, Fashion Island, Future Park, Zpell, ICONSIAM, Mega Bangna, Siam Paragon, Terminal 21 ×4, The Mall Lifestore, Robinson Lifestyle, True Digital Park and others. UNIQLO has stores in all of these.
- No minimum. At most 100,000 points / ท่าน / month.
- Register **every time, within the day**: SMS `BCB <last 12 digits> <points = spend>` → 4545888.
- Period 1 Aug – 31 Dec 2026. Credited within 60 days after the month's end.
- Not on KBank LINE POINTS, Titanium, business cards or Xpress Cash. So 🏠 KBank JCB, PLUSTINUM and Shopee qualify.
- Same exclusions as UQN (Smart Pay, e-wallets). The page has no "not combinable" line, so it reads as stacking on top of UQN's cashback (U).

Other KBank pages checked (217 campaigns via `GetAllMainCcCampaign`):
- The fashion installment page (`shopping-fashion-installment.aspx`, 1 Sep – 30 Nov) doesn't name UNIQLO.
- K Point 15% at department stores (`ccpromo-burnpoint-depart.aspx`) is department stores only.

## 3. ttb — UQCB (cashback) and UQBP (points → 12%)

Sources: ttb's page <https://www.ttbbank.com/th/promotion/credit-card/shopping/uniqlo-oct26> (`__NEXT_DATA__`, live 29 Sep 2026 – 28 Feb 2027) and UNIQLO's new copy <https://www.uniqlo.com/th/th/special-feature/cp/promotion/ttb> (text + banner), read 2026-10-05. **V**. Matches the repo facts.

Period **1 Oct 2026 – 28 Feb 2027**. Cards: every ttb personal credit card (old TMB and Thanachart cards included, ttb Global House, ttb Disney), primary and supplement 🏠 (ttb so smart). Corporate cards are out.

| Spend per sales slip | Cashback |
|---|---|
| every ฿3,000 | ฿150 (up to ฿450) |
| ฿12,000 or more | ฿800 |

- Caps: **฿800 / ท่าน / month**, **฿4,000 / ท่าน for the campaign**, every primary card and supplement together ("คำนวณบัตรหลักทุกใบและบัตรเสริมร่วมกัน").
- Registration: **once** for the whole campaign, before or on the transaction day: ttb touch, or SMS `UQCB <last 12 digits>` → **4899777**. ttb reserve infinite is enrolled automatically.
- New detail vs the repo: **only registered cards count** ("คำนวณเฉพาะบัตรเครดิตบัตรหลักและบัตรเสริมที่ทำการลงทะเบียนร่วมรายการเท่านั้น"). Register each card number that will be used, supplements included. A registered supplement's spend counts even when the primary didn't register.
- Several primary cards: the cashback goes to the one primary with the highest spend (ties: the highest-ranked card).
- Wording: "ธนาคารจะนำยอดใช้จ่ายสูงสุดต่อเซลล์สลิปในแต่ละรอบรายการมาคำนวณ" (the highest slip per round). The household reads it as each slip earning its own tier.
- Excludes business spend, cancelled charges and returned goods. A slip must post before the statement cut date.
- Crediting: within **60 days after each month's end**.
- No "not combinable" line on either copy.
- **Points half `UQBP`**: every 1,000 ttb rewards plus points → 12% cashback, on a slip ≥ ฿3,000, points ≤ the slip. Max 12,000 points / primary account / month and 60,000 for the campaign. SMS `UQBP <points> <last 12 digits>` → 4899777 **every time**. Primary cards only. 🏠 ttb so smart earns no points, so it doesn't apply.

## 4. CardX / SCB — UQC (cashback) and UQB (POINTX → cashback) — new

Source: CardX's page <https://www.cardx.co.th/credit-card/promotion/uniqlo-oct26-usc06> (promotion code `C6901917`, published 30 Sep 2026, updated 3 Oct), read through CardX's search index (hit id 9928) plus its banner, 2026-10-05. **V**. New: the repo had no CardX UNIQLO campaign, and the Bureau has no class for it.

**UNIQLO's CardX page is stale.** <https://www.uniqlo.com/th/th/special-feature/cp/promotion/cardx> still shows the ended **1 Jul – 30 Sep 2026** run: ฿100 per whole ฿3,000, ฿700 from ฿12,000; ฿700 / month and ฿2,100 for the campaign; POINTX 10% / 12%. The codes are the same and the numbers are worse. Go by CardX's page.

Period **1 Oct 2026 – 28 Feb 2027**. Cards: every CardX card and SCB WEALTH by CardX card (SCB PRIVATE BANKING, SCB FIRST, SCB PRIME), including old SCB-faced cards 🏠 (CardX JCB, Nuta). Thai UNIQLO stores and online only.

### คุ้ม 1 — cashback per slip (`UQC`)

| Spend per sales slip (after discounts) | Cashback |
|---|---|
| every whole ฿3,000 (under ฿10,000) | ฿120 — so ฿120 / 240 / 360 |
| **฿10,000 or more** | ฿700 |

- Caps: **฿700 / ท่าน / month**, **฿3,500 / ท่าน for the campaign**, all of a person's cards together.
- Registration: **once** for the whole campaign: CardX app (QR) or website, or SMS `UQC <last 12 digits>` → **4545777**, and wait for the confirmation. **Only spend on a registered card counts.**
- Excludes every installment (CardX ดีจังแบ่งชำระ, app and call-centre conversions), cancelled charges and business use.
- Crediting in two rounds:
  - spend 1 Oct – 30 Nov 2026 → credited by **31 Jan 2027**;
  - spend 1 Dec 2026 – 28 Feb 2027 → credited by **30 Apr 2027**.
  - It shows on the next statement.
- The October terms have no "not combinable" line (the July run had one).

### คุ้ม 2 — POINTX for cashback (`UQB`)

| Card | Mon – Fri | Sat – Sun |
|---|---|---|
| SCB WEALTH by CardX | 10% | **20%** |
| every other CardX card (except CardX / SCB FAMILY PLUS) 🏠 | 10% | 10% |

- Use POINTX points equal to the slip (whole baht). Max **50,000 points / ท่าน / month**. Only points still on the card used count; points moved into the POINTX app don't.
- Register **every time, within the transaction day**: app or website, or SMS `UQB <last 12 digits> <slip amount>` → 4545777.

### CardX JCB in Japan (travel)

CardX's JCB travel page <https://www.cardx.co.th/credit-card/promotion/jcb-traveling-intrip-feb26-plc11> (`C6900558`) keeps a standing **3% cashback on yen spend in Japan**, 1 Jan – 31 Dec 2026, capped at ฿2,000 per card number per statement cycle. It covers UNIQLO stores in Japan paid in yen on 🏠 CardX JCB. The same page's Marui / Sapporo Mitsukoshi coupon lists UNIQLO and GU as **excluded** brands. **V**.

## 5. Other banks

- **Bangkok Bank: nothing at UNIQLO.** All 165 listing pages were read via the in-page API (11 categories, 5 Oct); no title names UNIQLO. The fashion points cash-out (<https://www.bangkokbank.com/th-TH/Personal/Cards/Credit-Cards/Promotions/Retail_Fashion_260501-270430>) pays 12% / 15% (SMS `BFHS`, 1 May 2026 – 30 Apr 2027), but its poster lists 30 brands (H&M, ZARA group, COS, Jaspal, Pacifica, PP Group, CLUB21 …) and **no UNIQLO**. **V**.
- **GSB: no UNIQLO offer by name. Its mall points cash-out reaches some UNIQLO stores (U).**
  - Page: <https://www.gsb.or.th/promotions/shoppingcenter69/>, 1 Jan – 31 Dec 2026.
  - 13% cashback for GSB Reward Points equal to the spend, at tenant shops in Fashion Island, Terminal 21 (Asok, Korat, Rama 3, Pattaya), Future Park & ZPELL, MBK, The Nine, Paradise Park and The Crystal group.
  - Minimum ฿1,000 a slip; at most 100,000 points a card a month.
  - SMS `GSPD#<last 12>#<points>` → 0625965522, every time.
  - Department stores are out.
  - UNIQLO has stores at Fashion Island, Terminal 21 Asok / Rama 3 / Pattaya and Zpell & Future Park. **None in Chiang Mai.**
  - GSB's other September/October pages don't mention UNIQLO.
- **Amex Thailand: nothing.** The `lifestyle`, `travel` and `explore-asia` promotion pages don't mention UNIQLO. **V** (5 Oct).
- **Krungthai (KTB)** issues its cards through KTC (sibling report). **Citi** cards are now UOB's. **LH Bank, ICBC (Thai), CIMB Thai, TISCO, Kiatnakin**: no UNIQLO offer turned up in Thai web searches, and UNIQLO's hub lists none of them. Their sites weren't crawled; LH Bank's and ICBC's promotion URLs tried returned 404. **U**.

## 6. Card networks

- **Visa Thailand: nothing at UNIQLO.** All 57 perks were read on 5 Oct, from the POST `offers/api/portal/portal/perks/` captured over CDP. The closest are Global Blue (tax-free) and Mitsui Outlet Park. **V**.
- **Mastercard: not read.** Priceless Specials (`specials.priceless.com/th-TH`) showed a site-maintenance page all day, and its search API redirected. A Thai web search found no Mastercard UNIQLO offer. **U**.
- **UnionPay: no UNIQLO offer.** UnionPay International's Thai list has 12 merchants. Two generic offers could apply at a UNIQLO till, if the store accepts the method:
  - **QR 6%** (`260723112620`, 1–31 Oct): 6% off, at most ฿60 a slip, once a day, ฿300 a card a month. Register the card on UnionPay's page first. Pay through KTC Mobile, ICBC or BOC TH mobile banking. Pool 12,000 uses a month; **48.9% left on 5 Oct**. "Merchants that support UnionPay QR Code": UNIQLO's acceptance is unknown. Only one UnionPay promotion per transaction. This is the household's KTC UnionPay offer (Bureau-tracked).
  - **NFC 3%** (`260226111820`, 1 Mar – 31 Dec 2026): 3% off with a UnionPay card tapped from a phone wallet. At most ฿100 a transaction and ฿600 a month. October's pool shows **0% left**.
  - **V** for both offers. Whether they work at UNIQLO is **U**.
- **JCB Thailand: nothing at UNIQLO.** The Thai listing (`ajax.json`, 57 entries) was read through WebFetch, because this machine's TLS to specialoffers.jcb fails (curl and Chrome both). **V** (secondary read).
  - **JCB in Japan**: JCB's Thai-language Japan listing (`/th/campaign/output/d/east-asia/japan/ajax.json`, 40 entries) has no UNIQLO or GU offer. Its shopping offers are Don Quijote, drugstores, department stores and Mitsui Outlet Park.
  - KBank's JCB / Visa Japan pages (Isetan, Mitsukoshi, Bic Camera, Don Quijote, Matsumoto Kiyoshi, Mitsui Outlet, Ragtag) don't include UNIQLO either.
  - So **there is no JCB "5% off" at UNIQLO Japan**. At UNIQLO Japan the household gets only its cards' foreign-spend rules: CardX JCB 3% on yen (above), and KBank JCB's 10% applies in Korea, Taiwan and Hong Kong only (`jcb-cashback.aspx`, ≥ ฿20,000 a country, to 10 Nov 2026).

## 7. November

**No bank has pre-announced a November UNIQLO offer.** UOB's JSON has no item starting in November; KBank's 217 campaigns, CardX's live index and ttb's listing have none either. The four cashback campaigns above already run to 28 Feb 2027 and cover November. UNIQLO's November event (its "Thank You Festival" / ARIGATO pattern of past years) is the merchant researcher's to confirm.

## 8. Planning notes for the household (reading, U)

- **UOB at exactly ฿12,000** (6.7%) and **CardX at ฿10,000–11,999** (7.0% → 5.8%) are the best single-slip rates in this report. ttb matches UOB. KBank is lowest but adds K Point and leaves `BCB` open.
- **UOB needs an SMS every visit; the others don't.** An unregistered UOB slip earns nothing. UOB pools every UOB card the three hold into Takumi's ฿800 a month; ttb pools per person; CardX caps per person; KBank per card (household rule).
- **Points cash-outs stack on the slip's other side.** Takumi's UOB World / Premier `PPF` 10%. KBank `BCB` 10% (any KBank card but LINE Points) at both Chiang Mai stores. CardX `UQB` 10% on Nuta's CardX JCB. They need points on the card used. UOB's `PPF` and UNO share the "not combinable" line, so whether one slip can take both is unclear.
- **Bureau gap**: `lib/bureau/uniqlo.py` has no CardX `UQC` class (฿120 / 3,000, ฿700 from ฿10,000, ฿700 a month, two crediting rounds). Propose adding one if Nuta plans a CardX JCB UNIQLO slip.

## Site methods (new this session)

- **uniqlo.com (Akamai) blocks curl and headless Chrome from this machine, but `r.jina.ai/<url>` reads the bank pages**, text included. Fetch them **one at a time**: parallel jina requests got Akamai 403s, and they cleared when retried sequentially with a few seconds between them. The banners (`im.uniqlo.com/global-cms/spa/<res…>fr.jpg`) download with plain curl.
- **UNIQLO's bank index** is `/th/th/special-feature/cp/promotion` (no slug). A bank page can lag a quarter behind (CardX on 5 Oct), so check the bank's own page.
- **UNIQLO store list**: `https://map.uniqlo.com/th/api/storelocator/v1/th/stores?limit=100&RESET=true&lang=english&offset=0&r=storelocator` (limit ≤ 100; 300 returns HTTP 500). It returns all 74 Thai stores with type, address and room number.
- **KBank page by short link**: `kasikornbank.com/k_uniqlo` renders headless (desktop UA) to `…/pages/shopping-uniqlo.aspx`. `document.body.innerText` misses the collapsed T&C; `textContent` has it.
- **CardX**: search the index for the merchant's English name (`uniqlo` → 4 hits). The Thai name returns typo-tolerant noise. The `slugName` gives the page URL `cardx.co.th/credit-card/promotion/<slug>`.
- **Visa perks** is a POST: `{"siteId":"www.visa.co.th","perkTypeRequests":[{"perkType":"OFFERS","locale":"th_TH","pageRequest":{"index":0,"limit":1000},"perkArguments":{"offerType":"U"}}]}`. A bare GET returns 500. Capture it over CDP (`Network.getResponseBody`).
- **specialoffers.jcb**: when this machine's TLS fails, **WebFetch** still reads `…/thailand/ajax.json` and `…/d/east-asia/japan/ajax.json` (the Japan path is `east-asia/japan`, not `japan`).
- **UnionPay `getCoupon`** needs a browser-like `User-Agent` (Python's default gets 403), as `lib.bureau.unionpay_offer` already notes.
- **Bangkok Bank posters** load from inside the page: fetch `/-/media/…jpg` and return base64 over CDP. The fashion merchant list is only in the poster.
