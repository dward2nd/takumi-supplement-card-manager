---
tags: [catalogue-research, 2026-11]
researched: 2026-11-01
---

> **Research snapshot**: AIS bill payment — November 2026 research. Read on **2026-11-01** from the official pages, for the November 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] page `AIS Bill Payment — Nov 2026`. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions stayed in the session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# AIS bill payment — November 2026

A new page about a bill, not a shop: Takumi's AIS postpaid bill (and any AIS Fibre bill, prepaid top-ups and add-on packages), paid every month. The question is which card and which channel return the most on a ฿2,000 (or ฿500) bill. Confidence labels: **V** verified on the official page today · **R** my reading of official terms · **T** third-party only · **U** unverified. Point values follow [[all-spend]]: Krungsri ฿0.08 · First Choice ≈ ฿0.09 · K Point ฿0.10 · KTC ฿0.10 · UOB ≈ ฿0.104 · The 1 ฿0.125.

## 1. Headline

1. **Krungsri NOW in the myAIS app is still the best regular choice: 5% (฿100 on ฿2,000)**, but its ฿300 a month is shared with Baiboon's online spending on the same account (§2.3). Pay ฿2,000, not ฿1,999: it counts whole ฿500 blocks.
2. **KBank Smart Bill Pay** (new to the vault, 1 Oct – 31 Dec): bind a KBank card (PLUSTINUM, LINE Points or Shopee; not KBank JCB) as the auto-debit for AIS and/or AIS Fibre → **฿100 per provider** after 3 consecutive debits (≤ ฿900). Apply in K PLUS or at 02-888-8888 by **31 Dec** (§2.1).
3. **KTC `BIL`** (to 31 Mar 2027): one SMS (`BIL <16 digits>` → **061-384-5000**), then every AIS bill of ≥ ฿399 paid in myAIS or at an AIS shop turns **399 KTC points into ฿50** (฿0.125 a point instead of ฿0.10). This is AIS's own only bank deal listed today (§2.2).
4. **AEON Rabbit through LINE Pay** and **AEON Next Gen online** both pay 5% but **at most ฿50 a payment** (§2.5, §2.6). Good for a ฿500–1,000 bill; half-rate on ฿2,000 unless the bill is paid in two parts.
5. **The cards that earn nothing on an AIS bill**: KBank LINE Points (its terms exclude MCC 4814, so the `LP_AIS` payments very likely earned no LINE POINTS), KTC UnionPay (no points at 4814), every AEON points card (no points at 4814), Lotus's Beyond (no coins; SMP1 only). §3.
6. **Ended, no successor**: Lotus's **SMT2** (฿200 at ฿2,000 in October; the 1 Oct AIS bill counted); **CLICX × AIS Points ×10** (18 Jun – 31 Aug 2026). A 2025 **AIS Bill × SCB CardX** POINTX 10/15% round (`PTE1` / `PTE5`, 15 Jul – 30 Sep 2025) has no 2026 round.
7. **New customers only**: a first **CardX** principal card approved by 31 Dec gives a **Starbucks ฿1,000 e-Coupon** for setting up an AIS (or AIS Fibre) auto-debit (§2.7).

## 2. How the household pays AIS today (ledger, read-only, 1 Nov)

Takumi's Transactions DB, `name_contains` `AIS` (`/fetch-transactions`; multipliers read from the rows):

| Date | Card | Descriptor | ฿ | What came back |
|---|---|---|---:|---|
| 2026-10-22 | UOB World | `AMP*AIS SERVICESPackag BANGKOK TH` | 80.25 | `×5` |
| 2026-10-19 | KTC Digital VISA | `AMP*AIS SERVICESTopup BANGKOK TH` | 20 | points only |
| 2026-10-08 | Krungsri NOW | `AMP*AIS SERVICESPaymen BANGKOK TH` | 500 | `CB AMP*AIS SERVICESPaymen BANGKOK` −25 |
| 2026-10-01 | Lotus's Beyond | `AMP*AIS SERVICESPaymen BANGKOK TH` | 2,000 | `×0` (no coins, MCC 4814); counted for SMP1 and SMT2 (SMT2's ฿200 is in the Bureau) |
| 2026-09-08 | Krungsri NOW | `AMP*AIS SERVICESPaymen BANGKOK TH` | 2,000 | `CB …` −100 |
| 2026-09-08 | KBank LINE Points | `LP_AIS SERVICE BANGKOK` | 700 | — |
| 2026-08-31, 08-16 | KTC Digital VISA | `AMP*AIS SERVICESTopup BANGKOK THA` | 20 each | — |
| 2026-08-08 | KBank LINE Points | `LP_AIS SERVICE BANGKOK` | 900 + 100 | — |
| 2026-08-08 | UOB World | `AMP*AIS SERVICESPaymen BANGKOK` | 350 | `×5` (the Aug cycle reconciles with the ledger formula, [[../../promotions/uob-world-points]]) |
| 2025-04 – 05 | AEON Rabbit | `LINEPAY*LP_AIS SERVICE BANGKOK THA` | 20–128 | (before the 5% LINE Pay rows were tracked) |
| 2025-05-06 | Krungsri NOW | `LINEPAY*LP_AIS SERVICE BANGKOK THA` | 500 | `CB …` −25: the **LINE Pay route also counted as online** for NOW |

Three channels, three descriptors:
- `AMP*AIS SERVICESPaymen` (bill), `…Packag` (add-on package), `…Topup` (prepaid top-up): a card used **in the myAIS app**. `AMP` is **Advanced mPAY**, AIS's payment company (a 2005 joint venture, AIS 70% / NTT DoCoMo 30%) acting as payment facilitator. **T** (https://www.docomo.ne.jp/english/info/media_center/pr/2005/000682.html).
- `LP_AIS SERVICE` / `LINEPAY*LP_AIS SERVICE`: the bill paid **through LINE Pay** with a linked card (in the LINE app, or LINE Pay picked inside myAIS).
- **MCC 4814** (telecom) is the vault's reading: Lotus's paid no coins on the 1 Oct bill (its terms exclude phone operators), and SMP1, which assigns categories by the network MCC, counted it as a phone bill ([[../../cards/lotuss-beyond]], [[../../promotions/lotuss-smp1]]). **R**.

Krungsri NOW's ฿300 a calendar month is per account, and Baiboon's online spending competes for it: Aug ฿300 (Baiboon alone, on ฿13,235), Sep ฿200 Baiboon + ฿100 Takumi's AIS, Oct ฿25 (Takumi's ฿500 AIS only; no Baiboon NOW spend). Ledger, read-only.

Whether Takumi also has **AIS Fibre** isn't visible in the ledger (bills can be combined). Ask; it doubles the KBank Smart Bill Pay credit.

## 3. AIS's own channels, fees and points

### 3.1 Channels (AIS Knowledge Center, read today)

| Channel | Mobile | Fibre | Card possible | Fee |
|---|---|---|---|---|
| **myAIS app**: credit/debit card, LINE Pay, bank account, PromptPay QR | ✓ | ✓ | ✓ | **none** ("ไม่มีค่าธรรมเนียม จ่ายปุ๊บตัดยอดปั๊บ") |
| LINE Pay (LINE app → Wallet → AIS Service → AIS Postpaid/Fibre) | ✓ | ✓ | wallet balance or linked card | not stated |
| mPAY, mAgent, mPAY Station | ✓ | ✓ | | not stated |
| ShopeePay, Airpay | ✓ | ✓ | | not stated |
| Mobile banking, ATM, bank counter; bank transfer (mobile only) | ✓ | ✓ / ✗ | | not stated |
| Auto-debit: bank account (**KBank only** through myAIS) or credit card | ✓ | ✓ | ✓ | none |
| AIS Shop, Telewiz | ✓ | ✓ | ✓ | none stated |
| Counters: Lotus's, Big C, MWA, Post Office; Cen Pay machines (Central, FamilyMart, Robinson); Boonterm kiosks; cheque; AIS Call Center | ✓ | ✓ | | not stated |
| QR on the paper bill | ✓ | ✗ | | |

- Sources: https://aiscallcenter.ais.co.th/ikm/acc/index.php?kmid=KM1022269 (mobile), `kmid=KM1020235` (Fibre, the ✓/✗ table), `kmid=KM1020325` (myAIS, no fee), `kmid=KM1042326` and `kmid=KM1020324` (LINE Pay), `kmid=KM1026122` (card in myAIS). **V**.
- **7-Eleven / Counter Service and TrueMoney aren't on AIS's list.** **V** (absence).
- **Partial payments are possible** (the AIS Points rules speak of "การชำระยอดบางส่วน"); the Fibre web channel alone says "ไม่สามารถแยกยอดชำระได้". **R**.
- **myAIS's auto-debit menu was switched off on 14 Jul 2026** ("ปิดปรับปรุง เมนู จ่ายบิลอัตโนมัติ ชั่วคราว … จะกลับมาใช้งานได้อีกครั้งภายในเดือนสิงหาคม 2569"): apply through the bank instead, cancel at an AIS Shop; existing debits continue. The notice is still up today, so whether the menu is back is **U**. KBank Smart Bill Pay (§4.1) works either way.
- **SPayLater can't pay the monthly bill**: AIS's ShopeePay page lets SPayLater pay for devices at AIS Shop "ยกเว้น SIM เบอร์สวย และ ค่าบริการรายเดือน". https://www.ais.th/consumers/promotions/smart-pay/finance/shopee-pay · **V**.

### 3.2 AIS Points for paying the bill

- **1 AIS Point per ฿25 of service charges**, once registered (`*550#`, free). Excluded: "Goods & Service" (donations, Google Pay charges, AIS Top Up, Netflix).
- The **whole bill** must be paid by the due date or within 7 days after. Partial or advance payments get their points once the bill is issued. Points arrive within 30 minutes by SMS; the billed number earns them, whoever pays.
- The text sits on the myAIS page but names no channel, so every channel earns them (**R**): no reason to choose one card over another.
- https://aiscallcenter.ais.co.th/ikm/acc/index.php?kmid=KM1020325 · **V**.
- **No way to pay the bill with AIS Points was found** (searched; AIS Points buy packages, movie tickets, fuel discounts for Serenade members, discounts in the CLICX and Paotang apps). **U**.

### 3.3 AIS's own bill offers this month

- AIS's bank-promotion hub lists **one** bill-payment deal today: **AIS Bill × KTC** (§4.2). https://www.ais.th/consumers/promotions/bank-financial → https://www.ais.th/consumers/promotions/special-promotions/ais-bill-ktc · **V**.
- **CLICX × AIS Points ×10** (pay or top up through the CLICX virtual bank, KTB–AIS–OR): 18 Jun – 31 Aug 2026, ≤ 100 extra points per number. **Ended**; no successor found. **T** (https://droidsans.com/clicx-ais-points-and-clicx-save-max-promotion/).
- **AIS partner-points transfer bonus**, 1 Sep – 31 Dec 2026: transfer partner points into AIS Points and get **+15 / +50 / +150 / +600 / +2,500** at 300 / 500 / 1,000 / 3,000 / 5,000 AIS Points transferred in a month (≤ 2,500 per number a month, 20,000 rights across all partners). Partners include **Krungsri Card** (1,000 กรุงศรี พอยต์ = 100 AIS Points, UCHOOSE; https://www.krungsricard.com/th/promotion/ais-points), **Bangkok Bank** (Thank You Rewards 1,000 = 100, call 02-638-4000; 1 Jun – 31 Dec), **UOB** (`APW642`, 1 Jun – 31 Dec; rates not read) and **GSB** (600 = 50 AIS Points, My Card by GSB app). Sources: https://www.gsb.or.th/promotions/gsb-reward-point-ais/ (bonus table), Bangkok Bank `ais-point-260601-261231` (KTC/AEON researcher's listing dump). **V**. AIS Points have no published baht value, so this isn't a way to pay the bill.
- An earlier **AIS Bill × SCB CardX** round (POINTX → 10%, or 15% on bills ≥ ฿1,000, `PTE1` / `PTE5`) ran 15 Jul – 30 Sep **2025**; the page is still up, but no 2026 round exists. https://www.ais.th/consumers/promotions/special-promotions/ais-bill-scb-cardx · **V** (dates).

## 4. Card campaigns that pay on an AIS bill in November

### 4.1 KBank Smart Bill Pay — ฿100 per new auto-debit, AIS and AIS Fibre included

- **What**: bind a KBank credit card as the monthly auto-debit through **KBank Smart Bill Pay**. After **3 consecutive successful debits**, **฿100 cashback per provider**, **≤ ฿900 per cardholder** for the campaign. Providers: MEA, PEA, MWA, **AIS**, **AIS Fibre**, NT, True 5G, True Online, True Visions (legal names: "บริษัท แอดวานซ์ ไวร์เลส เน็ทเวอร์ค จำกัด", NT, True Move H, True Internet, True Visions).
- **ต่อ 2**: a ฿200 LINE MAN food e-voucher (orders ≥ ฿200, paid by KBank card) for a **new** MEA, PEA or MWA binding; one per cardholder.
- **New bindings only**: never bound with that provider before, or cancelled ≥ 6 months ago; moving an existing binding to another card doesn't count.
- **Apply** 1 Oct – **31 Dec 2026** in **K PLUS** or at **K-Contact Center 02-888-8888**. Campaign code `ACCS260499` (no SMS code on the page).
- **Cards**: every KBank credit card **except KBank JCB, KBank UnionPay**, corporate, Fleet, ThaiBev, K SME and business cards. So **KBank PLUSTINUM, KBank LINE Points and KBank Shopee qualify; KBank JCB doesn't.**
- **Credit** within 60 days after the month-end of the 3rd debit (page example: debits Feb–Apr, credit in June). Personal-name accounts only.
- "MEA, PEA, MWA and NT bills ตามปกติจะไม่ได้รับคะแนน K Point": AIS isn't in that sentence, so an AIS debit earns ordinary K Point on PLUSTINUM/Shopee (**R**).
- **The trade-off**: an auto-debit isn't a myAIS card payment, so that bill leaves Krungsri NOW's 5% (and SMP1, which excludes auto-debits). Three months of NOW on ฿2,000 is up to ฿300; the one-off is ฿100. It wins only if NOW's cap is full anyway, or for a bill NOW doesn't carry (e.g. AIS Fibre).
- https://www.kasikornbank.com/th/personal/promotion/creditcard/pages/smartbillpay.aspx (headless) · **V**.

### 4.2 KTC `BIL` — 399 KTC FOREVER points → ฿50 per AIS bill

- "โปรโมชั่น AIS จ่ายบิลมือถือ/เน็ตบ้าน กับบัตรเครดิต KTC", **1 Jul 2026 – 31 Mar 2027**.
- Pay a **mobile or AIS Fibre bill** in full by card (not installments), **≥ ฿399 a slip**, **at an AIS branch or in myAIS**; KTC takes **399 points** and credits **฿50** (≈ ฿0.125 a point against KTC's standard 1,000 = ฿100).
- **Register once**, on or before the first payment: SMS **`BIL <16-digit card number>` → 061-384-5000**, or ktc.promo/ais-pointredemption. It then applies to every qualifying slip while the points last. Not enough points → no credit.
- No monthly cap is written. Splitting one bill into several slips to get more credits isn't allowed ("ไม่สามารถแยกยอดใช้จ่ายเป็นหลายเซลส์สลิปเพื่อรับสิทธิ์").
- **Cards**: every KTC credit card except ROYAL ORCHID PLUS, **KTC CASH BACK**, the Red Cross card, corporate/government cards and KTC PROUD. Takumi's KTC Digital VISA, JCB, Mastercard and UnionPay all qualify; more than one registered card is counted per card.
- Credit within 60 days after the month-end.
- https://www.ktc.co.th/promotion/electronics-mobile/mobile-computer-tech-gadgets/ais-pointredemption · AIS's copy https://www.ais.th/consumers/promotions/special-promotions/ais-bill-ktc · **V**. The previous round (`-1`) ran 1 Jan – 30 Jun 2026; KTC's hub `/telco-pointredemption` holds the AIS, NT and True/dtac versions.
- **Value**: on a ฿2,000 bill, ฿50 credit + 80 ordinary points (฿8), for 399 points that would otherwise cash out at ฿39.90 → **≈ ฿18 better** than not using it (0.9%); on ฿500, ≈ ฿12 (2.4%). It's a good use of KTC points, not new money.
- **`TEL` / `TO` is for goods, not bills**: "โปรโมชั่นร้านค้า AIS, TRUE และ DTAC" (1 Jul 69 – 31 Jan 70): 0% up to 10 months at AIS shops and AIS Online Store (no KTC points on those rows), points → 13% (slip ฿1,000–9,999) / 15% (≥ ฿10,000) at AIS shops and Telewiz (EDC at the counter; SMS `TEL <16 digits>#<points>` → 061-384-5000 for AIS Online Store and Telewiz). https://www.ktc.co.th/promotion/electronics-mobile/mobile-computer-tech-gadgets/telco-operators · **V**.

### 4.3 Krungsri NOW 5% online (card benefit) — myAIS bills count

- **฿25 per whole ฿500 on each online slip (web/app), ≤ ฿300 a calendar month** per account; 1 Jan – 31 Dec 2026. Credit within 5 days of posting.
- Excluded: insurance, funds, travel; online ads; **QR-code payments**; utilities = **electricity, water and "ค่าบริการใดๆ ขององค์การโทรศัพท์แห่งประเทศไทย"** (TOT, now NT) in any channel; public transport, petrol, government MCCs; charities; fees; easyBills; Krungsri Smart Plan online installments; MCC 5199.
- **AIS isn't TOT/NT**, so a card payment in myAIS counts; the Sep (−฿100) and Oct (−฿25) credits prove it. The 5% box doesn't exclude wallets (the dining 2× box does), and the 2025 LINE Pay payment also earned it (**R** for 2026).
- **No Krungsri points** on 5% rows. "ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้".
- The ฿300 is shared with Baiboon's online spending (§2), first come first served by posting.
- https://www.krungsricard.com/th/product/creditcard/now · **V**.

### 4.4 Lotus's SMP1 "ช้อปคุ้มตัวแม่" — phone bills are a named category

- 1 Sep – 31 Dec 2026; Takumi's Lotus's Beyond is registered. The category reads: "จ่ายบิลค่าโทร ค่าเน็ต เมื่อชำระผ่านเคาน์เตอร์ เว็บไซต์ และ/หรือแอปพลิเคชั่น ของผู้ให้บริการเครือข่าย … โดยตรง อาทิ AIS Shop, My AIS, TRUE & dtac Shop, True iservice, True Money Wallet (เฉพาะการชำระค่าบริการโทรศัพท์มือถือ/อินเทอร์เน็ตรายเดือน)".
- Monthly, highest tier only: **฿70 per whole ฿3,500 (≤ ฿350)** · or ฿450 per whole ฿25,000 (≤ ฿1,800) · or ฿2,600 from ฿150,000. ≤ ฿2,600 a month; campaign ฿10,400 in the conditions (the banner says ฿14,000). Credit within 30 days after each month-end.
- **A ฿2,000 bill alone earns nothing**: it needs ฿3,500 of category spend in the month (department stores, fashion incl. UNIQLO, cosmetics, IT shops, books/stationery, Daiso, MR.DIY, MINISO…). With it, the bill is worth 2% of its block.
- Excluded: "รายการหักค่าสาธารณูปโภคผ่านบัญชีอัตโนมัติรายเดือนรายปี" (pay by hand, not auto-debit), installments, and spend counted in another Lotus's promotion.
- **No Lotus's coins** on phone bills ([[../../cards/lotuss-beyond]]).
- **SMT2** (฿200 at ฿2,000 in October) ended 31 Oct; **no SMT3** ([[krungsri-group]]). Register: UCHOOSE `SMP1` or SMS `SMP1 <16 digits>` → **081-250-7777**.
- https://www.lotussmoney.com/promotion/credit-card/shopping/cashback-nationwide ([[krungsri-group|Krungsri researcher's]] dump today) · **V**.
- Lotus's online/food-delivery offer excludes "การชำระค่าบริการโทรศัพท์มือถือ/อินเทอร์เน็ตรายเดือนทุกเครือข่ายผ่าน LINEPay ทุกช่องทาง" (same dump). **V**.

### 4.5 AEON Rabbit 5% on LINE Pay — reaches an AIS bill paid through LINE Pay

- AEON Rabbit Platinum benefit: **5% on spend through LINE Pay**, **≤ ฿50 a transaction**, **≤ ฿1,000 per primary card a cycle** (11th – 10th); credited within 2 cycles.
- Excluded: funds, insurance, "การตัดชำระค่าสาธารณูปโภคและ/หรือการตัดชำระรายเดือนรายปี (MCC Code 4900)", installments, FX, cash, fees, wallet top-ups (easyBills, TrueMoney, ShopeePay…), gift cards, digital assets. **MCC 4814 isn't excluded**, so an AIS bill paid in LINE Pay with AEON Rabbit as the linked card earns 5%. **R**.
- At ≤ ฿50 a transaction: ฿500 → ฿25, ฿1,000 → ฿50, ฿2,000 in one payment → ฿50 (2.5%). Two ฿1,000 payments → ฿100 if LINE Pay lets the bill be paid in parts (**U**: LINE Pay's AIS screen fills in the outstanding amount).
- No points on AEON Rabbit since 11 Nov 2025 ([[../../cards/aeon-rabbit]]).
- https://www.aeon.co.th/aeon/cards/aeon-rabbit-platinum-card ([[ktc-aeon-other-banks-networks|KTC/AEON researcher's]] dump today) · **V** (terms) / **R** (AIS counts).

### 4.6 AEON Next Gen 5% online — myAIS card payments, if the card is woken up

- 5% on online slips **≥ ฿500**, **≤ ฿50 a transaction**, ≤ ฿1,000 per primary account a cycle; **only in a cycle with ≥ ฿500 of Scan To Pay** on the card.
- Excluded: Scan To Pay, QR, **e-wallets**, P2P, airline tickets, funds, insurance, utilities = electricity, water, any TOT service "และค่าโทรศัพท์พื้นฐานทุกช่องทาง (… TOT/True/TT&T/CAT)" (landline), **"การตัดชำระรายเดือนรายปี"** (recurring), easyBills, installments, FX, cash, fees. A one-off myAIS card payment of an AIS **mobile** bill isn't in the list (**R**); through LINE Pay it is (e-wallet).
- ฿500 → ฿25; ฿2,000 → ฿50 (or ฿100 as two ฿1,000 myAIS payments, if partial payments are accepted, §3.1). No points on those rows.
- Takumi's AEON Next Gen is unused since Nov 2025 (household memory; [[../2026-10/education-krungsri-ktc-aeon]] has the same terms); the ฿500 Scan-To-Pay condition is the obstacle.
- https://www.aeon.co.th/aeon/cards/aeon-nextgen-digital-card/ · **V** (terms) / **R** (AIS counts).

### 4.7 CardX — first principal card: Starbucks ฿1,000 for an AIS auto-debit

- CardX BEYOND / UP2ME / JCB PLATINUM as a **first principal card**, applied for in the CardX app without a sales code, **approved by 31 Dec 2026**, with e-Statement.
- ต่อ 1: Starbucks e-Coupon ฿500 at ≥ ฿5,000 within 30 days. **ต่อ 2: Starbucks e-Coupon ฿1,000** for a monthly auto-debit with a listed provider (**AIS, AIS Fibre**, MEA, MWA, True, 3BB, dtac, CAT, TOT, NT; also online shops and streaming), first debit within 30 days of approval, then 3 consecutive cycles. ≤ ฿1,500 per person.
- Only for someone who has never held a CardX card or cancelled ≥ 180 days ago. Nuta holds a CardX JCB supplement, so probably not her; Takumi only if he holds no CardX card. Coupons by 28 Feb / 31 Mar / 30 Apr 2027 (Oct / Nov / Dec approvals), in POINTX.
- `dacq-q42026-1stcard1500stb` ([[kbank-cardx-uob-ttb|KBank/CardX researcher's]] dump) · **V**.

### 4.8 Wallet-routed campaigns (paying AIS through LINE Pay, ShopeePay, TrueMoney)

| Campaign | Counts an AIS bill paid through a wallet? | Detail · label |
|---|---|---|
| **Krungsri `ONQ3`** (to **30 Nov**, last month; VISA/JCB/Lady registered, NOW excluded) | **Yes** (**R**): card payments through TrueMoney, LINE Pay, ShopeePay count; the only utility exclusion is MCC 4900 | ฿3,000–14,999 a month → ฿40 · ฿15,000–29,999 → ฿170 · ≥ ฿30,000 → ฿350; "not combinable". https://www.krungsricard.com/th/promotion/online-shopping-cashback ([[krungsri-group]] dump) · V terms |
| **CardX `OEC`** (1 Oct 2026 – 31 Jan 2027) | **Yes** (**R**): Google Pay, LINE Pay, ShopeePay, TrueMoney payments count; exclusions are wallet top-ups, Lotus's, Makro, delivery apps | ฿70 / 300 / 1,000 / 1,800 at ฿5k / 20k / 60k / 100k a month; register monthly `OEC <last 12 digits>` → **4545777**, 1,000 rights a month. Only Nuta has a CardX card. https://www.cardx.co.th/th-TH/credit-card/promotion/e-commerce-cb-oct26-onc05 · V terms |
| **UOB `SPW796`** | **No**: "การชำระบิล ค่าประกัน ค่าภาษี ค่าบริการสาธารณูปโภคทุกประเภท … ไม่ร่วมในรายการ" | https://www.uob.co.th/personal/credit-cards/promotions/shopping-lifestyle/shopping-online-spw796-1226.page · V |
| **KBank LINE Points 3% on LINE Pay** | **Very likely no**: the card's earning terms list "รายการชำระค่าสาธารณูปโภค (MCC 4900, 4814)" and MCC 7399 "mPay Shopping, PAYSBUY…" among spend that earns no LINE POINTS | booklet §9, https://www.kasikornbank.com/SiteCollectionDocuments/kcc/linepoints/pdf/booklet.pdf (25 Jun 2026) · R |
| LINE Pay / ShopeePay / TrueMoney own offers | **none found** for AIS bills (LINE Pay's promotion page has no posts; TrueMoney isn't an AIS channel) | [[merchants-wallets]] §4 · V |

## 5. Base earning on an AIS bill (MCC 4814), card by card

| Card | On a myAIS card payment | Through LINE Pay | Source · label |
|---|---|---|---|
| **Krungsri NOW** | **5%** in whole ฿500 blocks, no points; ≤ ฿300 a month per account | 5% (2025 evidence) | §4.3 · V / R |
| Krungsri VISA / JCB / Lady | 1 กรุงศรี พอยต์ per ฿25 a slip (≈ 0.32%); "utilities" = electricity, water, TOT only | same + `ONQ3` (to 30 Nov) | https://www.krungsricard.com/th/krungsri-point · V |
| First Choice | 1 point per ฿25 (≈ 0.36%); MCC exclusions are transit, EEA, China. **Counts for NW4** (utilities there = electricity, water, TOT landline, MCC 4900/9402; auto-debits excluded) → **2% at the margin** (฿200 per whole ฿10,000 pooled a month) | same | firstchoice.co.th rewards + NW4 pages (all-spend researcher's dumps) · R |
| Central The 1 REDZ | 1 The 1 point per ฿25 (≈ 0.5%); its "utilities" exclusion isn't defined, Krungsri-family pages mean electricity, water, TOT | ✗ via TrueMoney; LINE Pay same | [[../2026-10/the1]] §A · R |
| Lotus's Beyond | **no coins**; SMP1 2% inside ฿3,500 blocks | not in SMP1's channel list | §4.4 · V |
| UOB One | **1%** (only MCC 4900 and MEA/PEA/MWA are out), ≤ ฿2,000 a cycle shared | 1% (e-wallet) | https://www.uob.co.th/personal/credit-cards/uob-one (all-spend dump today) · V |
| **UOB World** | **×5** if Mastercard flags it as e-commerce ("เฉพาะรายการที่ถูกกำหนดให้เป็นรายการ e-Commerce โดยมาสเตอร์การ์ดและวีซ่า"); the household's AIS rows are ×5 and the Aug cycle reconciles → **≈ 2.1%** within the ฿20,000 a cycle quota (Takumi + Baiboon), ×2 (≈ 0.83%) beyond | ×5 (e-wallet) | UOB World page (KBank/UOB researcher's dump) + ledger · R |
| UOB Premier / UOB Makro | not read | | U |
| KTC Digital VISA / JCB / Mastercard | 1 point per ฿25 (cycle-floored, ≈ 0.4%); 4814 isn't excluded on Visa/MC/JCB; **+ `BIL`** | same (BIL needs myAIS or a branch) | [[../../promotions/ktc-forever]] · R |
| KTC UnionPay | **no points** (rule 16: MCC 4814); `BIL` still works | | [[../../promotions/ktc-forever]] · V |
| KBank PLUSTINUM / KBank Shopee | K Point 1 per ฿25 (≈ 0.4%); **+ Smart Bill Pay** if set up as an auto-debit | | §4.1 · R |
| **KBank LINE Points** | **no LINE POINTS** (MCC 4814 and 7399 excluded) | very likely none | §4.8 · R |
| AEON World / Primo / UnionPay | **no points** on MCC 4814 on every AEON card except Big C (from 11 Nov 2025) | no points | AEON notice (all-spend dump) · V |
| AEON Rabbit | no points at all | **5%, ≤ ฿50 a transaction** | §4.5 · R |
| AEON Next Gen | **5%, ≤ ฿50 a transaction**, needs ฿500 Scan To Pay in the cycle | ✗ (e-wallet) | §4.6 · R |
| ttb so smart | **1%** (its exclusions are MCC 4900, TrueMoney, 7-Eleven, petrol, installments…; telecom isn't named), ≤ ฿2,000 a cycle | ✗ TrueMoney | [[../../cards/ttb-so-smart]] · R |
| CardX JCB (Nuta) | POINTX; no telecom exclusion known | counts for `OEC` | U |
| UOB Cash Plus, SPayLater, Grab PayLater | not usable / no rewards (SPayLater can't pay the monthly bill, §3.1) | | V |

## 6. Ranked answer

### 6.1 Takumi's ฿2,000 bill in November

| # | How | Back | % | Conditions · label |
|---|---|---:|---:|---|
| 1 | **Krungsri NOW**, card in myAIS | **฿100** | 5.0% | only while ≥ ฿100 of the account's ฿300 is left this month; pay early, before Baiboon's online spend on the card · V |
| 2 | AEON Rabbit through LINE Pay, **2 × ฿1,000** | ฿100 | 5.0% | only if LINE Pay accepts a part payment (U); one ฿2,000 payment = ฿50 · R |
| 3 | AEON Next Gen, card in myAIS, 2 × ฿1,000 | ฿100 | 5.0% | ฿500 Scan To Pay in the cycle; part payments (R) · R |
| 4 | First Choice, card in myAIS | ≈ ฿47 | ≈ 2.4% | NW4's 2% at the margin of the pooled month + points ≈ ฿7 · R |
| 5 | UOB World, card in myAIS | ≈ ฿42 | ≈ 2.1% | ×5 inside the ฿20,000 cycle quota · R |
| 6 | AEON Rabbit through LINE Pay, one payment | ฿50 | 2.5% | ≤ ฿50 a transaction · R |
| 7 | KTC (Visa/MC/JCB) + `BIL` | ฿50 credit + ฿8 points, for 399 points | net ≈ 0.9% | register `BIL` first; good use of KTC points · V |
| 8 | UOB One · ttb so smart | ฿20 | 1% | inside each card's ฿2,000 a cycle cap · V / R |
| 9 | REDZ · KBank PLUSTINUM · Krungsri VISA/JCB/Lady | ฿10 · ฿8 · ฿6 | 0.3–0.5% | points · R / V |
| 10 | Lotus's Beyond | ฿0 (฿70 only with ฿1,500+ more SMP1 spend that month) | 0–2% | SMP1 · V |
| — | KBank LINE Points (direct or LINE Pay), KTC UnionPay (without BIL), AEON World/Primo/UnionPay | ฿0 | 0% | §5 |

One-offs on top: **KBank Smart Bill Pay ฿100** (an AIS and/or AIS Fibre auto-debit on a KBank card, 3 debits; costs the NOW 5% on those months), **CardX new card Starbucks ฿1,000** (new CardX customers only).

### 6.2 A ฿500 bill (or a part payment)

| # | How | Back | % |
|---|---|---:|---:|
| 1= | Krungsri NOW in myAIS | ฿25 | 5% |
| 1= | AEON Rabbit through LINE Pay | ฿25 | 5% |
| 1= | AEON Next Gen in myAIS (with ฿500 Scan To Pay that cycle) | ฿25 | 5% |
| 4 | First Choice | ≈ ฿12 | ≈ 2.4% |
| 5 | KTC + `BIL` | ฿50 credit for 399 points (+ 20 points) | net ≈ 2.4% |
| 6 | UOB World ×5 | ≈ ฿10 | ≈ 2.1% |
| 7 | UOB One · ttb so smart | ฿5 | 1% |

Prepaid top-ups of ฿20 and packages of ฿80: NOW pays nothing below ฿500, and AIS Points exclude top-ups; UOB World ×5 (≈ 2.1%) or AEON Rabbit through LINE Pay (5%, AIS has a LINE Pay top-up, `kmid=KM1042325`) are the only returns worth naming.

### 6.3 Best in the market (any card)

For a regular monthly bill paid by hand, **5%** is the ceiling found: **Krungsri NOW** (≤ ฿300 a month, whole ฿500 blocks), **AEON Rabbit through LINE Pay** and **AEON Next Gen online** (≤ ฿50 a payment). The one-offs are **KBank Smart Bill Pay** (฿100 per provider, ≤ ฿900) and **CardX's new-card Starbucks ฿1,000**; **KTC `BIL`** is the only standing AIS-bill points offer. No other issuer's November AIS-bill campaign was found (searched: Krungsri, First Choice, Lotus's, KBank, CardX, UOB, ttb, KTC, AEON, Bangkok Bank, GSB listings; AIS's bank hub).

## 7. What ends this month / what's announced for December

- **Ends 30 Nov**: Krungsri `ONQ3` (no ONQ4 announced, [[krungsri-group]]).
- **Ends 31 Dec**: KBank Smart Bill Pay sign-ups; CardX first-card offer (approval by 31 Dec); Lotus's SMP1; Krungsri NOW 5% (2026 benefit — check its 2027 terms); AIS partner-points transfer bonus; Krungsri/Bangkok Bank/UOB points → AIS Points pages.
- **Runs on**: KTC `BIL` to 31 Mar 2027; KTC `TEL`/`TO` (goods) to 31 Jan 2027; CardX `OEC` to 31 Jan 2027.
- **Nothing December-specific announced** by AIS or the banks for bills on 1 Nov.

## 8. Not found / couldn't read

- **AIS's fees per channel** other than myAIS (no fee): LINE Pay, counters, mPAY Station, ShopeePay — not stated on AIS's pages. **U**.
- Whether **myAIS's auto-debit menu** is back (the July notice is still up). **U**.
- Whether **LINE Pay** lets the AIS bill be paid in parts (decides AEON Rabbit's ฿50 cap). **U**.
- **CLICX** November offers (clicxbank.com not read; news to Aug only). mitihoon.com (the CLICX press release) is Cloudflare-captcha'd to curl, r.jina.ai and headless Chrome.
- **UOB `APW642`** transfer rates; **UOB Premier / UOB Makro** earning on telecom; **CardX JCB** POINTX on telecom; **REDZ**'s definition of utilities. **U**.
- **KBank `k_linepointscctac`** (the LINE POINTS card T&C short link) returned nothing to an in-page fetch; the booklet PDF was used instead.
- **ShopeePay / TrueMoney / K PLUS** app-only bill offers can't be read without the apps.
- Other banks with no AIS-bill page found: SCB (now CardX), Krungthai (KTC), Citi (now UOB), KKP, TISCO, LH Bank, ICBC (its ANY 6% excludes telecom/recurring, [[../2026-10/all-spend-ticketing]] X2).

## 9. Logo

- **Wikimedia Commons `File:Advanced Info Service logo.svg`** (uploaded 16 Jan 2026, 524 × 191): green double swoosh + dark "AIS" wordmark, transparent. The 960 px PNG render renders cleanly: https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Advanced_Info_Service_logo.svg/960px-Advanced_Info_Service_logo.svg.png (curl 200, 960 × 350; viewed). Original SVG: https://upload.wikimedia.org/wikipedia/commons/3/3b/Advanced_Info_Service_logo.svg. **Use this one** on the white plate.
- AIS's own header logo https://www.ais.th/content/dam/ais/consumer/symbols/logo/ais-white-text.svg is the white-text version for dark backgrounds (wrong on white). `File:Advanced Info Services (logo).jpg` on Commons is a 2011 200 × 104 JPEG (old).
- Icon suggestion: 📱.

## 10. Lineage rows

Page letter for this page: **B** (AIS Bill Payment; **A** is Apple Products).

| Campaign | Pays | Oct 2026 | Nov 2026 | Pages | predecessor → successor |
|---|---|---|---|---|---|
| KTC `BIL` (`ais-pointredemption`) | 399 KTC points → ฿50 per AIS bill ≥ ฿399 (myAIS / branch) | running | 1 Jul 69 – 31 Mar 70 | B | `ais-pointredemption-1` (1 Jan – 30 Jun 69) → this |
| KBank Smart Bill Pay `ACCS260499` | ฿100 per new auto-debit provider (AIS, AIS Fibre, MEA, PEA, MWA, NT, True ×3), ≤ ฿900; LINE MAN ฿200 for MEA/PEA/MWA | running (not in the vault) | 1 Oct – 31 Dec 69 | B | — |
| Krungsri NOW 5% online | ฿25 per ฿500 online slip, ≤ ฿300/month; myAIS bills count | running | 1 Jan – 31 Dec 69 | B M S | card benefit |
| Lotus's SMP1 | ฿70 per ฿3,500 … in categories incl. phone bills | running | 1 Sep – 31 Dec 69 | B (+ existing) | — |
| Lotus's SMT2 | ฿200 at ฿2,000 in Oct | Oct only | ended, no SMT3 | B | → none |
| AEON Rabbit LINE Pay 5% | 5%, ≤ ฿50/txn, ≤ ฿1,000/cycle | running | standing | B | card benefit |
| AEON Next Gen 5% online | 5% on online slips ≥ ฿500, ≤ ฿50/txn, needs ฿500 Scan To Pay | running | standing | B | card benefit |
| CardX first card `dacq-q42026-1stcard1500stb` | Starbucks ฿500 + ฿1,000 for a utility (incl. AIS) auto-debit | running | 1 Oct – 31 Dec 69 | B | — |
| CardX `OEC` | online + wallet ladder ฿70–1,800 | running | to 31 Jan 70 | B S | — |
| Krungsri `ONQ3` | online + wallet ladder ฿40/170/350 | running | to 30 Nov 69 (last month) | B S | → none announced |
| KTC `TEL` / `TO` (`telco-operators`) | AIS/True/dtac goods: 0% ≤ 10 mo, points → 13/15% | running | 1 Jul 69 – 31 Jan 70 | (Apple) | `telco-operators-3` → this |
| CLICX × AIS Points ×10 | ×10 AIS Points on bills/top-ups via CLICX, ≤ 100/number | ended 31 Aug | — | B | → none found |
| AIS partner-points transfer bonus | +15 … +2,500 AIS Points on transfers of 300 … 5,000 | running | 1 Sep – 31 Dec 69 (BBL/UOB copies 1 Jun – 31 Dec) | B | — |
| AIS Bill × SCB CardX `PTE1`/`PTE5` | POINTX → 10% / 15% on AIS bills | — | — (15 Jul – 30 Sep 2025) | B | → none in 2026 |

## 11. New site tricks

- **AIS Knowledge Center** (`aiscallcenter.ais.co.th/ikm/acc/index.php?kmid=KM…`) reads with plain curl; each article's "บทความที่เกี่ยวข้อง" links are in the HTML (grep `kmid=`). The payment-channel tables and the AIS Points earning rules are there, not on ais.th.
- **ais.th** (Adobe Experience Manager): curl gets the full page, but the body is buried in a huge navigation; anchor the text extraction on a figure from the offer (e.g. "399"). `.model.json` returns 404. `/sitemap.xml` is a 404, `sitemap-loyalty.xml` and `pr-sitemap.xml` work. `/consumers/promotions/bank-financial` is AIS's bank-deal hub.
- **KBank PDFs** (`/SiteCollectionDocuments/…pdf`) are 403 to curl (Akamai): open any KBank page in headless Chrome and `fetch()` the PDF from inside it over CDP (base64 back). The LINE POINTS booklet's Thai text layer is garbled: render pages with `pdftoppm -r 80` and read the images.
- **Wikimedia Commons API** answered today without a 429 (`list=search&srnamespace=6`, then `prop=imageinfo&iiurlwidth=800`).
- **mitihoon.com** is behind a Cloudflare challenge for curl, r.jina.ai and headless Chrome; **droidsans.com** reads with curl and often carries the same press release.
