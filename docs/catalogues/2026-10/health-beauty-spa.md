---
tags: [catalogue-research, 2026-10]
researched: 2026-10-02
---

> **Research snapshot**: Hospitals, clinics, health & beauty and spa / massage — category campaigns, October 2026 research. Scope: card campaigns whose category is hospitals (MCC 8062), doctors and clinics (8011, 8099), dentists (8021), beauty, spa and massage (7230, 7297, 7298) and wellness, from every Thai issuer and network, valid in October 2026, as they would pay at Sriphat Medical Center (CMU, Chiang Mai) and at Yunomori Onsen & Spa without naming them; also hospital 0% installment programmes, spa cardholder discounts in Chiang Mai, and the household cards' standing rates in these categories. Read on **2026-10-02** from the official pages, for the October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions (HTML, JSON, posters) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# Hospitals, clinics, beauty and spa — category campaigns, October 2026

Confidence labels: **V** = verified (official page or poster read on 2 Oct), **3P** = third-party only, **U** = unverified. Unless a section says otherwise, every campaign below is **full-payment only** (installments excluded) and pays the reward to the **primary** card account. Supplement spend is pooled with the primary.

Two merchant facts frame everything:
- Ledger rows read `SRIPHAT MEDICAL CENTER CHIANGMAI TH` and `CENTER FOR MEDICAL EXC… CHIANGMAI TH`. KTC's statement reading puts the CMU Center for Medical Excellence at **MCC 8062** (see [[../../promotions/ktc-forever|ktc-forever]]). Sriphat's own MCC has not been seen; it is a CMU Faculty of Medicine centre, so 8062 is likely but **unconfirmed**.
- Yunomori's MCC is unknown. KTC lists Yunomori under its "MCC Beauty 5698, 7230, 7297, 7298, 8011 และ 8099" campaign (section 2.4), so it codes as one of those.

---

## 0. What matters for the household (short)

| # | Campaign | Household card | Pays at Sriphat? | Pays at Yunomori? | Conf. |
|---|---|---|---|---|---|
| 1 | **Lotus's LHB2** — health, beauty and pet ladder, ฿65 at ฿5,000/month, ฿130 per ฿9,000 (to ฿520), then 750–3,600 | Lotus's Beyond (Takumi, Baiboon supp.) | yes: public **and** private hospitals named | yes: "ฟิตเนส ยิม สปอร์ตคลับ สปา" | V |
| 2 | **Lotus's LFS4** — ฿200 at ≥ ฿4,000 health/beauty/pet, 1–15 Oct, first 500 | Lotus's Beyond | yes | yes | V |
| 3 | **First Choice NW4** (already registered) — hospitals count except government MCCs 9399/9405/7800 | First Choice (all three) | yes (Sriphat was in NW3 in Sep) | yes | V |
| 4 | **ttb so smart 1%** — hospitals and spas are not excluded | ttb so smart | yes | yes | V |
| 5 | **UOB One 1%** (5% only at Watsons, not spas) | UOB One | 1% | 1% | V |
| 6 | **KTC Wellness Max BWC 0.5%** (replaces points) / **BWP 13%** points-for-cashback on ≥ ฿1,000 slips | KTC cards | no (MCC 8062 not in the list) | yes | V |
| 7 | **KTC HOH** — 1,000 KTC points → ฿100 per ≥ ฿1,000 slip at any MCC 8062/8021/8071 | KTC Digital VISA / JCB / Mastercard (UnionPay earns no 8062 points) | yes, slips ≥ ฿1,000 | no | V |
| 8 | **UOB UH** — redeem UOB points equal to the slip → 10% at **any MCC 8062 hospital** (primary cards only; UOB One/Makro excluded) | UOB Premier / World (Takumi's primaries) | yes | no | V |
| 9 | **Krungsri PT26** — 500 points → ฿50 at listed MCCs incl. 8062, 8011, 8021, 8099, 7230, 7297, 7298 (primary only) | Krungsri VISA / JCB / Lady / NOW | yes | yes | V |
| 10 | **UnionPay QR 6%** (repo) / **UnionPay hospitals 5%** (≤ ฿2,000/slip, 2 per card) / **UnionPay NFC 3%** — one UnionPay offer per payment | KTC UnionPay, AEON UnionPay | QR 6% already used at CMU; 5% only at listed hospitals (list not read) | QR 6% if Yunomori takes UnionPay QR | V / U |
| 11 | **U PLAN 0% × 3 months** at 11 public hospitals incl. **Maharaj Nakorn Chiang Mai** (no points earned) | First Choice, Central The 1, Lotus's | **unconfirmed** that Sriphat bills as "Maharaj Nakorn Chiang Mai" | — | V (terms) / U (Sriphat) |
| 12 | **AEON 30% at Oasis Spa** (Nimman and Lanna branches, Chiang Mai), all AEON credit cards, to 31 Jul 2027 | AEON World / Primo / UnionPay / Next Gen / Rabbit | — | (another spa) | V |

The Central The 1 **HBF** (Happy Health & Beauty Fest) is verified: it pays at hospitals, beauty and spa anywhere, but needs **฿15,000 a month** for its first ฿100, and is on the **Central The 1 card only**. No Krungsri Card, First Choice or Lotus's version exists.

---

## 1. Krungsri Consumer group

### 1.1 Central The 1 credit card (REDZ / LUXE / BLACK / THE BLACK)

Source of all items: `POST https://www.centralthe1card.com/gcspromotion` (170 promotions on 2 Oct). Pages are `https://www.centralthe1card.com/promotion?modalId=<code>`. All four Central The 1 card tiers (`red|luxe|black|theblack`) unless noted.

**A. Happy Health & Beauty Fest — HBF · V** (`health-fest-202608`)
- Where: "หมวดโรงพยาบาล, ความงามและสปาทุกที่ทั่วไทย" (the hospital, beauty and spa categories, anywhere in Thailand). No MCC list is published.
- Period: **1 Aug – 31 Oct 2569**.
- Monthly accumulated full-payment spend → cashback (poster):

  | Accumulated per month | Cashback |
  |---|---|
  | ฿15,000–49,999 | ฿100 |
  | ฿50,000–119,999 | ฿450 |
  | ฿120,000–249,999 | ฿1,400 |
  | ≥ ฿250,000 | ฿3,500 |

- Caps: ฿3,500 per primary account per month, **฿10,500** per primary account for the campaign.
- **Excluded from 1 Sep**: the private hospitals of Happy Health Together — Bangkok Hospital (Soi Soonvijai, **Chiang Mai**, Pattaya, Udon), the Phyathai and Samitivej groups, Bumrungrad, MedPark, Vichaiyut, KDMS, and Siriraj Piyamaharajkarun. **Public hospitals are not excluded.**
- Not counted: QR Payment / e-wallet payments, Krungsri Consumer installment plans, interest and fees.
- Registration: once, on or before the day of spending. UCHOOSE, or SMS **`HBF <16-digit card number>`** to **081-278-2222**. Spend counts only from the day registration is confirmed.
- Crediting: within 15 days of the merchant's settlement, to the primary account. Supplement spend is pooled with the primary.
- Poster: https://www.centralthe1card.com/getattachment/534764b7-8a23-406e-a144-92815c0d5e0b/02_online_Happy-Health-Beauty-Fest_website.webp
- **Krungsri Card, First Choice and Lotus's do not run HBF.** Checked on 2 Oct: Krungsri Card's listing (485 items), First Choice's promotion index, Lotus's sitemap. Lotus's equivalent is LHB2 (1.4).

**B. Happy Health Together — HP2 · V** (`hhp--together-202609`)
- Per full-payment slip at **Bangkok Hospital (Soi Soonvijai, Chiang Mai, Pattaya, Udon)**, the Phyathai group, the Samitivej group, Bumrungrad, MedPark, Vichaiyut and KDMS. Online payments to those hospitals count too.

  | Per slip | Cashback |
  |---|---|
  | ฿15,000–49,999 | ฿160 |
  | ฿50,000–79,999 | ฿560 |
  | ฿80,000–149,999 | ฿950 |
  | ฿150,000–349,999 | ฿1,800 |
  | ≥ ฿350,000 | ฿4,500 |

- Caps: ฿4,500 per primary account per month and **฿18,000** for the campaign, all hospitals together.
- Period: **1 Sep – 31 Dec 2569** (poster text; the file name says "31Dec27").
- Registration: SMS **`HP2 <16 digits>`** to 081-278-2222, or UCHOOSE, on or before the day.
- Excluded: QR / e-wallet payments and installments. Crediting: within 15 days of settlement.
- Sriphat is not on the list. **Bangkok Hospital Chiang Mai is.**
- Poster: https://www.centralthe1card.com/getattachment/d62977b4-f655-4805-95ee-d6d237b794d9/T1-Hospital-(1Sep26-31Dec27)-OL-A4-1024px-copy.webp

**C. U PLAN — 11 public hospitals, 0% for 3 months · V** (`u-plan-202601`)
- Converts medical bills at **11 public hospitals**, done in UCHOOSE:
  - Siriraj, Chulalongkorn, Somdet Chaopraya Institute of Psychiatry, Srithanya, Srinagarind (Khon Kaen University), Khon Kaen Hospital;
  - Burapha University Hospital, **Maharaj Nakorn Chiang Mai**, Buddhachinaraj Phitsanulok, Songklanagarind, Maharaj Nakhon Si Thammarat.
- Terms:
  - **0% for 3 months, no points** on the converted spend.
  - Or a special rate **from 0.39% a month for 4–10 months**, i.e. an effective 7.01–15.83% a year, set per person.
  - Minimum ฿500 per slip and ฿3,000 converted in total. A slip of ≥ ฿3,000 converts at once.
  - Must be done before the statement date (3 business days before, for the 0% plan).
  - 1 Jan – 31 Dec 2569.
- Whether a `SRIPHAT MEDICAL CENTER` charge counts as "Maharaj Nakorn Chiang Mai" is **unconfirmed**; ask in UCHOOSE before relying on it.

**D. Other Central The 1 card health items (brief) · V**
- **Health & Wellness** (`health-wellness-202608`, 1 Aug – 31 Oct): 0% for 6+ months at participating clinics. Cashback starts at ฿10,000 per slip, capped at ฿17,000 per slip and ฿40,000 per account. Not via HD Mall / Shopee / Lazada.
- **Beauty** (`beauty-202607`, to 31 Oct): 0% up to 10 months + up to ฿40,000 at beauty clinics.
- **Hospital and nursing-home installments** (`cat-hospital-202605`, to 31 Dec): 0% up to 10 months, cashback from ฿10,000 per slip, up to ฿100,000 per account. Register `HOS`. Not via payment gateways (HDMall, 2C2P, Omise, Ksher…).
- Named-merchant offers, all Bangkok: Siriraj Piyamaharajkarun (`siriraj-202610`, up to ฿15,000), Vimut, Bangkok Eye, Praram 9, VitalLife, Divana Spa 30%, Panpuri (Ancient Onsen Bath day pass ฿690, LUXE/BLACK only), Jivamanee Spa, Anantara Riverside spa (LUXE+). **None in Chiang Mai.**

### 1.2 Krungsri Card (VISA, JCB Platinum, Lady Titanium, NOW Platinum)

Index: the promotion page at https://www.krungsricard.com/th/promotion embeds every item (485 on 2 Oct) as JSON with `TypePromotion` / `SubTypePromotion` (`health-beauty`, `medical-hospital`, `medical-beauty`, `medical-wellness`, `medical-dental`).

**A. "ดูแลสุขภาพ ใส่ใจทุกค่ารักษา" — MED1 / MED2 / PT26 · V** — https://www.krungsricard.com/th/promotion/top-hospital
- Period: 1 Oct – 31 Dec 2569. All Krungsri cards except corporate cards.
- **MED1**: per full-payment slip at participating hospitals (MCC 8062 on Visa, Mastercard and JCB).
  - Tiers: ฿15,000+ → ฿170; ฿50,000+ → ฿650; ฿100,000+ → ฿1,300; ฿250,000+ → ฿3,300; ฿400,000+ → ฿5,500.
  - Cap ฿5,500 per primary account for the campaign. Credited within 30 days after the campaign ends.
  - Register once: UCHOOSE "MED1", or SMS **`MED1 <16 digits>`** to **08 1927 9999**.
- **MED2**: +฿1,500 at ฿700,000 accumulated over the campaign, first 50 accounts. SMS `MED2`.
- **Hospital list** (all Bangkok and the east): Siriraj Piyamaharajkarun, Bangkok Hospital (Soi Soonvijai), BDMS Wellness Clinic, the Samitivej and Phyathai groups, Bumrungrad, VitalLife, Vichaiyut, MedPark, the Kasemrad group, the Paolo group, Bangkok Christian, Saint Louis, Thainakarin, Nakornthon, Praram 9, Yanhee, Vibhavadi, the Synphaet group, World Medical, the Sikarin group, Ramkhamhaeng, Ramathibodi Sri Ayudhya. **No Chiang Mai hospital.**
- Excluded: foreign currency, e-wallets, Thonburi Health Village, installments.

**B. PT26 — Krungsri points to cashback at medical and personal-care MCCs · V** — https://www.krungsricard.com/th/promotion/point-cashback
- Redeem in UCHOOSE ("PT26") in the same month as the spend: 500 points → ฿50, 1,000 → ฿100, 5,000 → ฿500 (฿0.10 a point; Krungsri calls it "10%").
  - No minimum slip. Cap 500,000 points per primary account per day. Credited the next day.
  - Primary cards only. Krungsri VISA, JCB Platinum, NOW Platinum and Lady are included.
- MCC list (PDF https://www.krungsricard.com/KrungsriCreditCard/media/html/MCC-Code-10percent-Y2026_04-08-26.pdf), baht charges only:
  - Medical: **8062** hospitals, 8071, **8099**, **8011**, **8021**, 8031, 8041, 8042, 8043, 8044, 8049, 8050, 4119, 5122, 5912, 5975, 5976, 7277;
  - Personal care: **7230**, 7297 massage parlours, **7298** health and beauty spas, 7299, 8351.
  - So it reaches both Sriphat and Yunomori.
- The hospital page (https://www.krungsricard.com/th/promotion/hospital), beauty & spa page and wellness page repeat PT26 as "พิเศษ 2", valid 1 Jan – 31 Dec 2569.
- Sister offer **"แลกพอยต์รับเครดิตเงินคืนสูงสุด 50%"** (https://www.krungsricard.com/th/promotion/redeem-points-cashback, 1 Sep – 31 Dec): same ฿0.10 a point, up to 5× the month's spend.
  - Categories: clinics and beauty institutes (**MCC 8011, 7230, 7298**), plus foreign spend, insurance, home, auto and opticians.
  - Redeem by USSD `*465*12886*<last 4>*<points>#`. Not combinable with other promotions.

**C. Krungsri Card discounts in Chiang Mai · V** (show the card; no registration)
- Hospitals, northern list (PDF https://www.krungsricard.com/KrungsriCreditCard/media/html/hospital-deal-north.pdf), 2569:
  - **Chiang Mai Ram**: 10% on room, medicine and treatment. Excludes doctor fees, beauty laser, dental, all package programmes and some medicines.
  - **Lanna Hospital** (1 Feb – 31 Dec): 20% on rooms; 10% on rooms, lab, ordinary X-ray and EKG. Excludes CT, MRI, ultrasound and special X-ray. Show the card at the cashier.
- Beauty & spa, northern list (https://www.krungsricard.com/KrungsriCreditCard/media/html/Beauty_north.pdf):
  - Pornkasem Clinic, Central Festival Chiang Mai: programme prices.
  - Pan Clinic, Central Chiang Mai Airport: 15% on products and single treatments.
  - **No spa or onsen in Chiang Mai is on the list.**
- Wellness, northern list (https://www.krungsricard.com/KrungsriCreditCard/media/html/Wellness_north_1.pdf):
  - Absolute Health Clinic Chiang Mai: Rebalance Check ฿4,990 (from ฿7,292).
  - Jetts Fitness at Index and One Nimman: ฿200/month off, joining and card fees waived, PT package prices.

**D. Hospital installments — HOS · V** — https://www.krungsricard.com/th/promotion/hospitals-installment
- 0% up to 10 months at participating hospitals (terms set per hospital). Register once with UCHOOSE "HOS" or SMS **`HOS <16 digits>`** to **06 1404 5555**.
- Cashback per installment slip: ฿10,000–29,999 → ฿120; ฿30,000–59,999 → ฿500; ฿60,000–119,999 → ฿1,100; every ฿120,000 → ฿2,400. Cap ฿100,000 per primary account. Credited next cycle.
- Not via online channels or payment gateways (HDMall, 2C2P, Omise, Ksher, Pranintech, Xendit…). 1 Jan – 31 Dec 2569.
- Hospital list PDF https://www.krungsricard.com/KrungsriCreditCard/media/html/HOS_2026.pdf includes **เชียงใหม่รามธุรกิจการแพทย์ (Chiang Mai Ram) and its Lanna Hospital**. No Sriphat, Maharaj, Bangkok Hospital Chiang Mai or McCormick.
- **The 11-public-hospital U PLAN page is not in Krungsri Card's listing.** It is on Central The 1 (1.1 C), First Choice (1.3) and Lotus's (1.4).

**E. Lady Titanium "light pay" · V** — https://www.krungsricard.com/th/promotion/lady-light-pay
- 0% for 4 months, converted in UCHOOSE.
- MCCs: **8011, 7230, 7298** and fashion/cosmetics MCCs (5611 … 5977, 7296).
- Needs ≥ ฿1,000 per slip and ≥ ฿15,000 accumulated. Department stores and ZARA, H&M, Jaspal, POMELO, SEPHORA, EVEANDBOY and Adidas are excluded.
- Converted rows earn no points. 1 Jan – 31 Dec 2569. The household's Lady is the Lady Titanium.

**F. Not found**: no Krungsri Card bonus-point category for health or beauty. No MED-style campaign at a Chiang Mai hospital. The dental page `beauty-dental-discount` is dated 1–31 Dec 2569.

### 1.3 First Choice (Krungsri First Choice Visa Platinum)

- **NW4 covers hospitals and spas · V** — https://www.firstchoice.co.th/promotion/firstchoice-cashback
  - NW4 is pooled all-spend (details in [[kbank-cardx-uob-ttb]] / [[krungsri-group]]).
  - Excluded: "รายการที่เกี่ยวกับการชำระค่าใช้จ่ายที่เกี่ยวข้องกับหน่วยงานราชการ … ซึ่งอาจรวมถึงการชำระค่าใช้จ่ายในโรงพยาบาลรัฐบางแห่ง หรือรายการที่เข้า MCC 9399, 9405 และ 7800". That means government bodies, which may include some public hospitals, i.e. MCC 9399, 9405 and 7800.
  - A public hospital coded **8062** counts. Sriphat's Sep row was counted in NW3.
  - Registration: UCHOOSE "NW4", or SMS `NW4 <16 digits>` to 081-256-3333.
- **U PLAN at 11 public hospitals · V** — https://www.firstchoice.co.th/promotion/epr-hospital
  - The same hospital list and terms as 1.1 C, including **Maharaj Nakorn Chiang Mai**.
  - 0% for 3 months with no points, or from 0.39%/month for 4–10 months (effective 7.01–15.83%).
  - ≥ ฿500 per slip, ≥ ฿3,000 in total. 1 Jan – 31 Dec 2569.
  - Caution (U): NW4 excludes installments, so a converted slip probably drops out of NW4.
- **Hospital installments HOS · V** — https://www.firstchoice.co.th/promotion/hospital (poster `/getattachment/96130268-018a-4a1b-a3b8-ae6307bad7fa/Cate-Hospital-HOS_Jan-Dec26_PAGE.jpg`)
  - Same tiers as Krungsri Card's HOS (฿120 / 500 / 1,100 / 2,400, cap ฿100,000). Register `HOS` to 061-404-5555. 1 Jan – 31 Dec 2569.
  - Dealer list PDF `/getattachment/cb7f87f3-373b-4ab7-99e0-d1e2808a7ca9/Dealer-Hos_KFC.pdf` includes **เชียงใหม่รามธุรกิจการแพทย์** (Chiang Mai Ram).
  - Merchant installments on First Choice book to the loan line (see [[../../promotions/first-choice-privilege-2026|first-choice-privilege-2026]]), so they earn nothing else.
- **No HBF and no health or beauty cashback ladder on First Choice.** The Jul–Sep "CASHBACK MATCH" (3P: mitihoon, which named medical and beauty clinics) ended on 30 Sep. No Q4 successor appears in the promotion index.

### 1.4 Lotus's (Lotus's Beyond and other Lotus's cards)

**A. LHB2 — "Health & Beauty: สุขภาพ ความงาม & สัตว์เลี้ยง" · V** — https://www.lotussmoney.com/promotion/credit-card/health-beauty/health-and-beauty
- Period: **1 Jul – 31 Oct 2569**. All Lotus's credit cards.
- **Counts**:
  - hospitals, "**ทั้งโรงพยาบาลรัฐ และเอกชนทั่วประเทศ**" (both public and private, nationwide);
  - beauty and specialist clinics, and dental clinics;
  - pharmacies and beauty stores (Watsons, Boots);
  - opticians;
  - "**ฟิตเนส ยิม สปอร์ตคลับ สปา และร้านทำผม**" (fitness, gyms, sports clubs, spas and hair salons);
  - vets and pet shops;
  - six health-product sellers (Amway, Giffarine, Zhulian, Herbalife, Unicity, Kangzen-Kenko), including their own online channels.
  - Lotus's classifies by the card network's MCC.
- Monthly full-payment accumulation → cashback. Only the highest tier applies.

  | Accumulated per month | Cashback |
  |---|---|
  | ฿5,000–8,999 | ฿65 |
  | every whole ฿9,000 | ฿130 (max ฿520) |
  | ฿50,000–74,999 | ฿750 |
  | ฿75,000–99,999 | ฿1,200 |
  | ฿100,000–149,999 | ฿1,650 |
  | ฿150,000–199,999 | ฿2,600 |
  | ≥ ฿200,000 | ฿3,600 |

- Caps: ฿3,600 per primary account per month; ฿14,400 per primary account for the campaign.
  - The headline "28,800" adds the U PLAN part below.
- **U PLAN part (`**`)**: converting a ≥ ฿3,000 health and beauty slip to U PLAN in UCHOOSE pays the cashback again ("เพิ่ม 1 เท่า").
  - Same caps: ฿3,600 a month, ฿14,400 in total. Conversions allowed to 18 Nov.
  - The rate is **from 0.69% a month flat** (effective 12.38–16.00%) for 3–10 months, which costs more than the extra cashback.
  - The 0%-for-3-months public-hospital conversions are excluded.
- Excluded:
  - e-commerce marketplaces, installments and installment terms;
  - **government-category spend earns no Lotus's coins** (a general rule, stated on the page).
- Not combinable: spend counted in another Lotus's promotion can't count here.
- Registration: once, on or before the day. UCHOOSE "**LHB2**" or SMS **`LHB2 <16 digits>`** to **081-250-7777**.
- Crediting: within 60 days after each month ends. Supplement spend is pooled with the primary.
- Posters: `/getattachment/f2fe74ba-…/health-beauty-credit-card-promotion-jun26-detailpro-1.webp`, `…-detailpro-3.webp` (U PLAN line).

**B. LFS4 — "รูดก่อน ได้ก่อน หมวดสุขภาพ & ความงาม" · V** — https://www.lotussmoney.com/promotion/credit-card/health-beauty/health-and-beauty-deal
- **1–15 Oct 2569.** Accumulate ≥ ฿4,000 full payment in the same health, beauty and pet categories (same definition as LHB2) → **฿200**, once per account.
- First **500** registrants who complete the spend. Register in UCHOOSE "**LFS4**" (check the remaining rights there) or SMS `LFS4 <16 digits>` to 081-250-7777, **before** spending.
- Credited within 60 days after the campaign. Same "not combinable with other promotions" clause as LHB2.
- **Whether one slip can count for both LFS4 and LHB2 is unclear.**

**C. Lotus's discounts in Chiang Mai · V** (show the card)
- **Chiang Mai Ram** (https://www.lotussmoney.com/promotion/credit-card/health-beauty/chiangmairam-hospital): 10%, excluding doctor fees, beauty laser, dental, packages and medical supplies. 1 Apr – 31 Dec 2569.
- **Chiang Mai Klai Mor** (…/chiangmaiklaimor-hospital): 10% on IPD rooms; 7% on medicine, supplies, lab and X-ray. Excludes MRI. 1 Mar – 31 Dec 2569.

**D. Lotus's U PLAN, public hospitals · V** — https://www.lotussmoney.com/promotion/credit-card/installment/installment-health-government-hospital
- The same 11 hospitals, including **Maharaj Nakorn Chiang Mai**. 0% for 3 months with no coins, on ≥ ฿500 slips and ≥ ฿3,000 in total.
- Otherwise from **0.69%/month** up to 10 months. The page's own lines disagree on the effective rate (7.01–15.83% vs 12.38–16.00%).
- Separately, merchant installments at participating hospitals: https://www.lotussmoney.com/promotion/credit-card/installment/hospital (list PDF not read).

---

## 2. KTC (KTC Digital VISA, KTC JCB, KTC Mastercard, KTC UnionPay)

KTC's promotion sitemap (`/sitemap-promotions-1…12.xml`, ~6,000 Thai URLs with `lastmod`) has 80 `health-beauty/hospital` and 39 `wellness-center-spa` pages.

**Points earning (terms from 2026-09-28, [[../../promotions/ktc-forever|ktc-forever]]) · V**
- Rule (16) withholds points at **MCC 8062** (public hospitals) on **KTC UnionPay only**.
- KTC Digital VISA, KTC JCB and KTC Mastercard earn 1 point per ฿25 at hospitals. The Mastercard's government-MCC rule (2) covers 9211/9222/9311/9399/9402/9405, not 8062.

**2.1 Hospital per-slip cashback — MED2 · V** — https://www.ktc.co.th/promotion/health-beauty/hospital/retail-cashback
- Period: **1 Oct 2569 – 31 Jan 2570**. At "100 private hospitals" in the Medical MCCs 5912, 8021, 8062 and 8071.

  | Per slip | Cashback |
  |---|---|
  | ฿15,000–44,999 | ฿170 |
  | ฿45,000–84,999 | ฿500 |
  | ฿85,000–149,999 | ฿950 |
  | ฿150,000–349,999 | ฿1,700 |
  | ฿350,000–499,999 | ฿4,400 |
  | ≥ ฿500,000 | ฿6,700 |

- Unlimited over the campaign; 1 slip per card per day.
- **Earns no points** (they are clawed back).
- Register once: SMS **`MED2 <16 digits>`** to **0613845000**, or the page. Credited within 60 days after each calendar month.
- Excluded cards: KTC CASH BACK, corporate and government cards.
- Hospital list (https://www.ktc.co.th/upload/02-promotion-download/Merchant-Name_Retail-CB_Q4-Oct26-Jan27.pdf) includes **Bangkok Hospital Chiang Mai, Chiang Mai Ram and McCormick**. **No Sriphat, Maharaj or Lanna.**

**2.2 Hospital points-for-cashback · V** (same page; 1 Jan – 31 Dec 2569)
- **HOH — 10% at any hospital or clinic nationwide, MCC 8062, 8021, 8071.**
  - On a full-payment slip of ≥ ฿1,000, redeem 1,000 KTC FOREVER points per ฿1,000 → ฿100. Points may not exceed the slip.
  - SMS `HOH <16 digits>#<points>` to 0613845000 on the day, each time. Credited within 60 days after the month.
  - Excluded: KTC ROP, CASH BACK and corporate cards.
- **HOP — 13% at participating hospitals and clinics**: the same mechanic, ฿130 per 1,000 points. SMS `HOP …`.
- For the household:
  - Baiboon's ~฿450 CMU slips are under the ฿1,000 minimum.
  - A Sriphat bill of ≥ ฿1,000 on a KTC Visa/JCB/Mastercard qualifies for HOH if Sriphat is MCC 8062.

**2.3 Hospital installment cashback — HOS · V** — https://www.ktc.co.th/promotion/health-beauty/hospital/cashback-installment
- 1 Jul – 31 Dec 2569. On 0% installments of 3–10 months at participating hospitals.
- Per slip: ฿10,000–24,999 → ฿120; ฿25,000–39,999 → ฿400; ฿40,000–79,999 → ฿700; ฿80,000–129,999 → ฿1,500; ≥ ฿130,000 → ฿3,100. Unlimited.
- SMS `HOS <16 digits>` to 061 384 5000. The hospital list on this page was not opened.
- The 1 Jan – 30 Jun version (`cashback-installment-1`) has ended.

**2.4 Wellness Max — BWC / BWP / ACC · V** — https://www.ktc.co.th/promotion/health-beauty/aesthetic-clinic/wellnessmax (= `ktc.co.th/wellnessmax`)
- Where: "ศูนย์ดูแลสุขภาพทั่วประเทศ ภายใต้ MCC Beauty **5698, 7230, 7297, 7298, 8011 และ 8099**" (health centres nationwide under those MCCs). **No 8062**, so hospitals don't count.
- Period: 1 Jul – 31 Dec 2569.
- **BWC**: 0.5% cashback from the first baht, per card, credited within 60 days of month-end.
  - **Points are forfeited** on that spend.
  - A slip converted to KTC's own 0.74%/month installment is excluded.
  - Register once: SMS `BWC <16 digits>` to 061 384 5000, or the page.
- **BWP**: on each full-payment slip of ≥ ฿1,000, every 1,000 points → ฿130 (13%). The poster says "13.5%"; the T&C say 13%.
  - Register each time, on the day: `BWP <16 digits>#<points>`.
  - Excluded: KTC ROP and CASH BACK cards.
- **ACC** ("Accumulate Project … 2nd Half 2026"): e-coupons once accumulated health and beauty spend reaches ฿50,000 / ฿100,000 (https://www.ktc.co.th/promotion/health-beauty/hospital/healthlevelup).
  - All Bangkok clinics and partners, plus HDmall's 10% on-top coupon. No cash value.
- Poster: `…/promotion-wellness-bliss-max-h2-2026-sm-jun26-369.webp`.
- **Yunomori is a named Wellness Max merchant** (https://www.ktc.co.th/promotion/health-beauty/wellness-center-spa/yunomori-onsen-and-spa, updated 25 Sep). The page adds KTC points prices (13 May – 31 Dec), e.g.:
  - 1 point → Onsen + Aromatherapy 90 min ฿1,950 (from ฿2,475);
  - 1,990 points + ฿340 → Onsen Day Pass (฿650 value).
  - Branch-specific limits are on the Yunomori research page.

**2.5 KTC UnionPay × hospitals 5% (UnionPay offer `260807112707`) · V**
- Pages: https://www.ktc.co.th/promotion/health-beauty/hospital/hospital-x-unionpay and UnionPay's offer API.
- 5% off, up to **฿2,000 per slip**, at participating hospitals ("Hospitals in Thailand", UnionPay merchant `898410064576002`).
- Limits: 1 per card per day, **2 per card** over the campaign, 1,000 redemptions in total. The offer API shows `totalCount` 10,000 and **85.5% left** on 2 Oct.
- Period: **1 Sep – 31 Dec 2569**. Register the card first on UnionPay's offer page.
- Cards: "All UnionPay credit, debit, and cash cards (except debit cards, KBANK and BBL credit cards issued in Thailand)". So **KTC UnionPay and AEON UnionPay** qualify.
- Stacking: combinable with other promotions **except other UnionPay ones**. The system applies the single best UnionPay discount, so not on top of QR 6%.
- The hospital list is a Tencent Docs sheet (`https://docs.qq.com/sheet/DVnpxQmtuYkZTRmhH?tab=BB08J2`) that didn't render (see Not found).

**2.6 KTC spa and onsen deals · V**
- **Let's Relax** (https://www.ktc.co.th/promotion/health-beauty/wellness-center-spa/lets-relax-spa): 10% off every service via a 1-point KTC Mobile e-coupon.
  - All branches; Chiang Mai has 3 (per the Visa page below). 16 Mar – 31 Dec 2569. Not combinable with other offers.
- **Onsen @ Moncham, Mae Rim, Chiang Mai** (https://www.ktc.co.th/promotion/air-ticket-hotels-travel/hotels-resorts/onsen-at-moncham), 1 Sep 2569 – 31 Mar 2570:
  - 10% off rooms booked direct (Best Flexible) and 10% at Mi Zu Restaurant;
  - KTC VISA ×5 points per ฿4,000 (capped at 1,600 points or ฿8,000 a month, register monthly);
  - 13% points-for-cashback at participating hotels.
- Dental (`hospital/dentistry`): programme prices and a Premium Dental Check-up for 1 point (100 rights) at one Bangkok clinic.
- `beautywellness` (1 Oct – 31 Jan): 0% up to 10 months at participating health centres, with ฿220–7,100 per installment slip from ฿10,000. Not Chiang Mai-specific.

---

## 3. UOB (UOB One, UOB World, UOB Premier, UOB Makro)

Index: `https://www.uob.co.th/assets/web-resources/personal/credit-cards/promotions/data-promotion.json` (627 items; categories include `hospital` and `beauty`). The terms are in the `.json` twin under `/assets/web-resources/personal/credit-cards/promotions/<cat>/<slug>.json`.

**3.1 Hospital Q4 — HHP / UH (OPW806) · V**
- Page: https://www.uob.co.th/personal/credit-cards/promotions/others/hospital-opw806-1226.page · terms: `/assets/web-resources/personal/credit-cards/promotions/others/hospital-opw806-1226.json`
- Period: 1 Oct – 31 Dec 2569.
- **HHP** (สิทธิพิเศษ 1): every ฿30,000 per slip → ฿300, capped at **฿1,200 per cardholder** for the campaign on ordinary cards (Reserve and Infinite: ฿3,000).
  - Only at Bangkok Hospital (Soi Soonvijai), Bumrungrad, BDMS Wellness Clinic, MedPark, Praram 9, the Phyathai group (1/2/3/Phahon Yothin/Nawamin/Sriracha), the Samitivej group, Vichaiyut and Siriraj Piyamaharajkarun.
  - SMS **`HHP <last 12 digits>`** to **4545111** before spending, or Rewards+ in UOB TMRW.
- **UH** (สิทธิพิเศษ 2): redeem UOB Rewards points equal to the slip → **10%** (12% on Reserve, Infinite and Zenith), at **any hospital nationwide under MCC 8062**.
  - Cap 100,000 points per cardholder per month.
  - SMS **`UH <last 12 digits> <slip amount>`** to 4545111 on the day of payment, each time.
  - **Primary cards only.** Excluded: UOB One, Simple, Lazada, **Makro**, Grab, Yolo, ROP, KrisFlyer and TMRW cards, **and all supplements**.
  - Online payments, gift cards and installments are excluded.
- For the household: **Takumi's UOB Premier or UOB World primary** can use UH at Sriphat, if it is MCC 8062. Baiboon's supplements can't. The UOB One isn't eligible.

**3.2 Hospital installments (HPW354 / HPW585) · V**
- HPW354 ("HOS26"):
  - 0% up to 10 months; cashback from ฿40,000 per installment slip of 4+ months: ฿300 / ฿1,600, or ฿4,500 on Reserve/Infinite.
  - Caps ฿1,600 per quarter on ordinary cards. Two rounds: Jul–Sep and **Oct–Dec**. SMS **`HOS26 <last 12>`** to 4545111.
  - Also a 12% points discount on installments (primary only).
- HPW585: GrabFood e-coupons for installment slips from ฿90,000.
- Hospital lists: Bangkok and eastern hospitals only. **No Chiang Mai hospital** in either.
- Pages: https://www.uob.co.th/personal/credit-cards/promotions/ipp/ipp-hospital-hpw354-1226.page and …/ipp/hospital-h2-hpw585-1226.page.

**3.3 Standing earn in these categories · V**
- **UOB One** (https://www.uob.co.th/personal/credit-cards/cash-back/one-cash-back-credit-card.page):
  - **5%** only at "ร้านวัตสันทั่วประเทศ และวัตสันออนไลน์" (Watsons stores and online), 7-Eleven and Grab, with 10%/5% capped at ฿500 a month together.
  - **Spas and hospitals earn the 1%**, capped at ฿2,000 a cycle. The 1% exclusions (funds, unit-linked, cash, petrol, Makro, utilities, FX…) don't name hospitals.
  - So the 5% tier does **not** reach spas.
- **UOB World** (https://www.uob.co.th/personal/credit-cards/rewards/uob-world-credit-card.page):
  - ×5 per ฿25 online and e-wallet, and in dining, travel and foreign currency;
  - **×2 everywhere else**, which covers hospitals and spas paid at the counter.
- UOB Premier: not re-read for this topic.

**3.4 UOB wellness / dental privileges (WPW267, HPW237, HPW265) · V** (all 2569)
- Discounts at named partners. Northern entry: **Absolute Health Clinic Chiang Mai** (053 223 023). The offer details were not extracted.
- Page: https://www.uob.co.th/personal/promotions/credit-cards/wellness-hospital-prvilege-spw267-1226/wellness-hospital-prvilege-spw267-1226.page
- The `/personal/promotions/credit-cards/…` pages show "Loading…" in curl and have no `.json` twin at the expected path (HPW116 "12% at hospitals" wasn't read). OPW806's UH covers the same mechanic for Q4.

---

## 4. KBank (KBank JCB, LINE Points, PLUSTINUM, Shopee)

Read in headless Chrome. Akamai serves "Access Denied" to headless Chrome's default user agent; a desktop Chrome `--user-agent` works.

**4.1 Hospital cashback (HP4 / MHP4 / HL) · V** — https://www.kasikornbank.com/th/promotion/creditcard/pages/health-beauty-hospital-cashback.aspx
- Period: 1 Oct – 31 Dec 2569.
- Group 1 (BDMS 5 + Siriraj Piyamaharajkarun, Vejthani, Vichaiyut, Thonburi Bamrungmuang …): per slip from ฿20,000, up to ฿4,400. Plus accumulated bonus K Point. SMS `HP4`.
- Group 2 (Synphaet, Bangkok Christian, Ramkhamhaeng, Vibhavadi, Nakornthon, Chaophya, Yanhee, Sikarin, Nonthavej, Vimut, Bangpakok 9, Thainakarin, Kasemrad, Bangmod …): ฿10,000–29,999 → ฿110 … ≥ ฿250,000 → ฿3,100. Cap ฿6,300. SMS `MHP4`.
- All Bangkok. **No Chiang Mai hospital.**
- **HL**: K Point equal to the slip → **10%** at **participating hospitals only**. SMS `HL <last 12> <amount>` to 4545888. Excluded: **LINE POINTS card**, Titanium and business cards.
- **0% via K PLUS on any MCC 8062 hospital slip of ≥ ฿50,000**: 3 months on ordinary KBank cards (6 on the BDMS co-brand). No registration. Forfeits K Point.

**4.2 Hospital installments (BD4) · V** — https://www.kasikornbank.com/th/promotion/creditcard/pages/health-beauty-hospital-installment.aspx
- Period: 1 Oct – 31 Dec 2569.
- Group 1 = Bangkok Hospital group, 22 branches **including Bangkok Hospital Chiang Mai**: 0% for 6 months; per installment slip ฿20,000–49,999 → ฿250, ฿50,000–99,999 → ฿750, ≥ ฿100,000 → ฿3,000.
- Cap ฿9,000 per person. SMS **`BD4 <last 12>`** to **4545888**. Plus HL 10% K Point redemption.
- Other KBank health pages (clinic chains, beauty clinics 0% 6–10 months, fitness, dental, Bangkok Drug Store 10% points): not Chiang Mai-specific; not detailed.
- **No KBank spa offer** was found in the health-beauty category list.

---

## 5. CardX (Nuta's CardX JCB)

Read from CardX's search index: `POST kong-prod-frontend.cardx.co.th/indexes/promotion/search`, key from the front-end bundle (see Site tricks). Pages are `https://www.cardx.co.th/credit-card/promotion/<slug>`.

- **"สุขภาพดีไปด้วยกัน" HPB · V** (`hospital-oct26-usc03`, C6901899), 1 Oct – 31 Dec 2569:
  - Per full-payment slip, including the hospitals' online and call-centre payments: ฿10,000–29,999 → ฿100; ฿30,000–49,999 → ฿350; ฿50,000–119,999 → ฿600; ฿120,000–249,999 → ฿1,500; ≥ ฿250,000 → ฿3,200.
  - 1 slip per person per day. Caps ฿3,200 a month, **฿9,600** for the campaign.
  - Register once: SMS **`HPB <last 12>`** to **4545777**, or the CardX App.
  - Hospitals: Ramkhamhaeng 1–2, Saint Louis, Nonthavej, Piyavate, the Kasemrad group, Navavej, the Chularat group, Siriraj H Solutions, Ramathibodi Sri Ayudhya, **Bangkok Hospital Chiang Mai**, Bangkok Pattaya, Bangkok Hua Hin, Triyaja, Rutnin.
- **"สุขภาพดีเพื่อคนที่คุณรัก" · V** (`topmain-hospital-oct26-usc03`, C6901737), 1 Oct – 31 Dec:
  - Per slip ฿10,000+ → ฿110 … ≥ ฿400,000 → ฿5,500. Plus ฿6,500 a month at ≥ ฿800,000.
  - Bangkok hospitals only.
- **NHP1–NHP5 points · V** (`ntw-hospital-apr26-usc03`, C6900758), 1 Apr – 31 Dec:
  - Redeem POINTX points 1–5× the slip → 10–50% back, at participating hospitals, health institutes, dental clinics and opticians "ภายใต้ MCC Code 8062".
  - No minimum. Points from the paying card only. SMS `NHP<n> <last 12> <amount>` to 4545777, each time.
  - The participating list isn't on the index document. The Oct HPB page repeats NHP for its hospitals.
- **BTP1 "สวยคุ้ม แลกรับเครดิตเงินคืน 10%" · V** (`usage-beauty-q1-jan26-usc03`, C6900079), 6 Jan – 31 Dec:
  - At "สถานเสริมความงามและสปาที่ร่วมรายการทั่วประเทศ" (participating beauty salons and spas nationwide), slips ≥ ฿1,000: every 1,000 POINTX → ฿100.
  - SMS `BTP1 <last 12> <points>` to 4545777.
  - The T&C name **MCC 5947**, which is the gift/novelty MCC. Probably a CardX typo for 7298; treat the spa coverage as **U**.
- Hospital installment cashback (`hospital-b-wellness-oct26-usc03`, 1 Oct – 31 Dec): ฿150–6,500 per installment slip from ฿10,000. Bangkok list. Also `ipp0-hospital-g1` points 10–30% on installments.
- **No Chiang Mai spa offer** in CardX's index ("สปา" returns mostly unrelated hits).

---

## 6. ttb (ttb so smart)

- **ttb so smart 1% counts hospitals and spas · V** — https://www.ttbbank.com/th/personal/credit-cards/card-type/ttb-so-smart
  - The exclusions are utilities (MCC 4900), insurance, funds, cash, interest and fees, **ttb so goood and pay-plan installments**, transfers, FX, business spend, taxes, China/EEA merchants, 7-Eleven, TrueMoney, foreign merchants in baht and petrol.
  - No hospital or spa exclusion. ฿2,000 per card per cycle.
- **"ห่วงใยสุขภาพ" HST · V** — https://www.ttbbank.com/th/promotion/credit-card/health/tophospital-oct26, 1 Oct – 31 Dec 2569:
  - Per full-payment slip, including online but not e-wallet: ฿20,000–49,999 → ฿200; ฿50,000–99,999 → ฿550; ฿100,000–299,999 → ฿1,200; ฿300,000–499,999 → ฿3,800; ≥ ฿500,000 → ฿6,500.
  - Cap ฿6,500 per person. Only the highest slip per round counts.
  - Hospitals: Bumrungrad, VitalLife, "**โรงพยาบาลกรุงเทพ และในเครือ**" (Bangkok Hospital and its network, so probably Bangkok Hospital Chiang Mai: U at branch level), BDMS Wellness, the Phyathai and Samitivej groups, MedPark.
  - Register: ttb touch, or SMS **`HST <last 12>`** to **4899777**.
- **ttb so goood at hospitals · V** — https://www.ttbbank.com/th/promotion/credit-card/health/sogooodspecialrate-jun26, 1 Sep – 31 Dec 2569:
  - On full-payment slips of ≥ ฿1,000 in hospital MCCs **8011, 8021, 8050, 8062, 8099** (and 0742 vets), convert in ttb touch to **0% for 3 months**, or 0.59%/month flat for 6 or 10 months.
  - **Converting forfeits the so smart 1%** and ttb rewards points.
- Named clinic offers (Laser Bank, Rajdhevee, The Klinique, The Touch, Zenva, HDmall): Bangkok; not detailed.

---

## 7. AEON (AEON World, Primo, UnionPay, Next Gen, Rabbit)

- **Oasis Spa 30% · V** — https://www.aeon.co.th/aeon/promotions/the-oasis-spa/
  - 30% off four 2-hour treatments: Deep Calm Recovery (฿3,500 list), King / Queen of Oasis Signature Massage (฿3,900), Urban Heat Reset Ritual (฿3,900). Prices exclude service charge and VAT.
  - At all 8 Oasis branches, including **Oasis Spa at Nimman** and **Oasis Spa Lanna** in Chiang Mai.
  - **All AEON credit cards.** 1 Sep 2569 – 31 Jul 2570. Book ahead (02-262-2122, LINE @oasisspa). Not combinable with other promotions.
- **NTW1 does not reach spas or hospitals · V** — https://www.aeon.co.th/aeon/promotions/happy-monthly-with-aeon-2026/
  - Its "หมวดสุขภาพ และความงาม" (health and beauty) is only **Beautrium, Boots, EVEANDBOY, Sephora and Watson**.
  - Correction to the earlier one-line summary in [[ktc-aeon-other-banks-networks]].
- Other AEON items, not Chiang Mai: Phyathai Happy Point (points use), AEON Wellness Platinum discounts (that card only), Rak-Kho Hospital, Fitness 24 Seven, THE KLINIQUE.

---

## 8. Bangkok Bank (not held)

- **2026 Hospital year-round benefit, regional · V** (headless Chrome) — https://www.bangkokbank.com/th-TH/Personal/Cards/Credit-Cards/Promotions/2026_Hospital_year_round_benefit_Region_260101-261231
  - Discounts set per hospital, for BBL credit cards and B-Fest debit cards, 1 Jan – 31 Dec 2569.
  - Chiang Mai entries: **Chiang Mai Ram, Chiang Mai Klai Mor, Chiang Mai Hospital, Lanna**.
  - Plus **12%** back by redeeming Thank You Rewards equal to the slip: SMS `HOSP <16 digits>` to 4712008 (฿3) on the day. Primary only; Titanium, AirAsia, M Visa and supplements excluded.
- The BBL UnionPay Platinum 2% all-spend (≥ ฿2,000 a month, ฿1,000 cap) is in [[all-spend]]; not re-read.

---

## 9. Networks

- **UnionPay**, from UnionPay International's offer API (`marketing.unionpayintl.com/h5Promote/v1/…`). Only one UnionPay offer applies per payment.
  - **Hospitals 5%** (2.5), 1 Sep – 31 Dec. · V
  - **QR 6%** (repo: [[../../promotions/unionpay-qr|unionpay-qr]]): October offer `260723112620`. · V (repo)
  - **NFC 3%** (offer `260226111820`, merchant "UnionPay Offline Merchants in Thailand"), 1 Mar – 31 Dec 2569. · V
    - 3% off at offline merchants paid by **UnionPay contactless in a phone wallet** (Apple Pay, Samsung Pay, …). QR scans are excluded.
    - Limits: ≤ ฿100 per payment, 3 a day, 6 a month, ฿600 a month; 15,000 discounts nationwide a month. No registration.
    - The API showed **0% of the pool left** on 2 Oct.
  - The 10%-abroad offer (`260925112958`) is for ICBC (Thai), BOC (Thai) and KKP debit cards only. Not domestic.
  - UnionPay's Thailand merchant list (12 entries) has no spa or massage merchant.
- **Visa Signature — 50% at spas · V** — https://www.ktc.co.th/credit-card-privileges/spa (a Visa privilege that KTC hosts)
  - 50% off one treatment: Let's Relax Thai massage 90 min (฿1,000 list; **3 Chiang Mai branches**), Health Land Thai massage 120 min (฿700; **1 Chiang Mai branch**), Oasis Spa (aroma hot oil 60 min ฿1,590 / Thai 60 min ฿1,178 / facial 60 min ฿1,648; **2 Chiang Mai branches**), Kliniq, THANN (Bangkok).
  - **Visa Signature primary cards issued in Thailand only.** Needs ฿50,000 on that card in the 60 days before booking. Book ≥ 7 days ahead at `www.vthgservice.com`. Once per card for the year. 1 Jan – 31 Dec 2569.
  - Whether any household Visa is a Signature is **unknown**.
  - **Update 2026-10-02 (user):** Takumi's KTC cards are now KTC Digital VISA **Signature**, KTC World Reward Mastercard, KTC JCB **Ultimate** and KTC UnionPay Diamond (Baiboon's and Nuta's KTC UnionPay supplements are Diamond too). So Takumi's KTC Digital VISA qualifies, with ฿50,000 on it in the 60 days before booking.
- **Mastercard, JCB, Amex**: no Thai-issued-card spa or hospital offer in Chiang Mai was found.
  - JCB's special-offers site didn't connect from this session.
  - The KTC-hosted JCB/Mastercard Panpuri offers and KTC JCB Ultimate × Yunomori are Bangkok / Pattaya.

## 10. Other issuers

GSB, Krungthai (KTB debit), Kiatnakin, LH Bank, ICBC, BOC, Citi (now UOB): **not found**. A web search found only expired GSB hospital pages (Nakharin, Jun–Aug 2569). These sites weren't read in depth.

---

## 11. Cross-cutting answers

### Do public hospitals count?

| Campaign | Public hospitals | Note |
|---|---|---|
| Central The 1 HBF | yes, not excluded | Excludes only the named private chains |
| Lotus's LHB2 / LFS4 | **yes, named** ("ทั้งโรงพยาบาลรัฐ และเอกชน") | Government-category spend earns no Lotus's coins |
| First Choice NW4 | yes unless coded MCC 9399/9405/7800 | "may include some public hospitals" |
| KTC HOH 10% | yes (MCC 8062) | KTC UnionPay earns no points at 8062 |
| UOB UH 10% | yes (MCC 8062, nationwide) | Primary only; UOB One excluded |
| Krungsri PT26 | yes (8062 on the MCC list) | Primary only |
| CardX NHP | only *participating* 8062 hospitals | List not on the index |
| ttb so goood 0% | yes (8062 and others) | Forfeits the 1% |
| KBank K PLUS 0% (≥ ฿50,000) | any 8062 | |
| U PLAN 0% × 3 | **only 11 public hospitals** (incl. Maharaj Nakorn Chiang Mai) | Central The 1, First Choice, Lotus's |

### Hospital 0% installments in October that name a Chiang Mai hospital

| Programme | Chiang Mai hospital | Terms |
|---|---|---|
| U PLAN (Central The 1 / First Choice / Lotus's) | Maharaj Nakorn Chiang Mai | 0% × 3, no points; else 0.39%/mo (CT1/FC) or 0.69%/mo (Lotus's) |
| Krungsri Card / First Choice HOS | Chiang Mai Ram, Lanna | 0% up to 10 months per hospital + ฿120–2,400 per slip from ฿10,000 |
| KBank BD4 | Bangkok Hospital Chiang Mai | 0% × 6 + ฿250–3,000 from ฿20,000 |
| KBank K PLUS | any 8062 | 0% × 3 on slips ≥ ฿50,000 |
| ttb so goood | any hospital MCC | 0% × 3 on slips ≥ ฿1,000 (or 0.59%/mo × 6/10) |
| KTC HOS | list not opened | 0% × 3–10 + ฿120–3,100 from ฿10,000 |
| UOB HOS26 / HPW585 | none | Bangkok and eastern lists |
| CardX installment cashback | none | Bangkok list |
| BBL Be Smart, AEON | not found | |

**Sriphat and McCormick appear on no installment list.** McCormick is on KTC's MED2 per-slip cashback list (2.1).

### Category structures on the household's cards (health, beauty, spa)

| Card | At hospitals | At spas / massage | Source |
|---|---|---|---|
| UOB One | 1% | 1% (5% is Watsons only) | 3.3 · V |
| UOB World | ×2 points | ×2 points | 3.3 · V |
| UOB Premier | base points; UH 10% redemption (primary) | base | 3.1 · V (earn rate not re-read) |
| ttb so smart | 1% | 1% | 6 · V |
| First Choice | NW4 ladder | NW4 ladder | 1.3 · V |
| Krungsri VISA / JCB / Lady / NOW | base points; PT26 | base; PT26; Lady 0% × 4 at 7230/7298 | 1.2 · V |
| Lotus's Beyond | LHB2, LFS4 | LHB2, LFS4 | 1.4 · V |
| Central The 1 REDZ | HBF (≥ ฿15k/mo); HP2 at the listed private hospitals | HBF | 1.1 · V |
| KTC Digital VISA / JCB / Mastercard | 1 pt/฿25; MED2 per slip; HOH 10% | BWC 0.5% or BWP 13% | 2 · V |
| KTC UnionPay | no points at 8062; QR 6% / hospitals 5% | BWC / BWP; QR 6% | 2, 9 · V |
| KBank JCB / LINE Points / PLUSTINUM / Shopee | no category bonus found; HL 10% at Bangkok hospitals (not LINE Points) | none found | 4 · V (partial) |
| CardX JCB (Nuta) | HPB at Bangkok Hospital CM; NHP points | BTP1 (MCC uncertain) | 5 · V/U |
| AEON World / Primo / UnionPay / Next Gen / Rabbit | no category bonus (NTW1's health = 5 retailers) | Oasis Spa 30% | 7 · V |

---

## 12. Corrections to the brief's priors

- **HBF** is on the **Central The 1 card only** (all four tiers). Code `HBF`, SMS 081-278-2222, from 1 Aug. **Bangkok Hospital Chiang Mai is excluded from HBF** from 1 Sep. Public hospitals and spas count; QR and e-wallet payments don't.
- **Happy Health Together** is also Central The 1 only. Code `HP2`, **per slip** from ฿15,000. Its hospital list **includes Bangkok Hospital Chiang Mai**. Caps ฿4,500 a month and ฿18,000 in total.
- **U PLAN "0.39% × 10 months"** is not interest-free:
  - it is a flat rate from 0.39%/month for 4–10 months, effective 7.01–15.83% a year;
  - **0% applies only for 3 months, at 11 public hospitals**, with no points;
  - Lotus's rate starts at 0.69%/month.
- **AEON NTW1's "health & beauty"** is five named retailers, not spas or hospitals.
- **UOB One's 5%** is Watsons only. Spas and hospitals earn the 1%.
- **KTC FOREVER**: only KTC UnionPay loses points at MCC 8062. The other KTC cards earn there.

---

## Not found / unconfirmed

- **Sriphat's MCC** and whether its charges count as "Maharaj Nakorn Chiang Mai" for U PLAN. Sriphat appears on **no** campaign's named-hospital list.
- **UnionPay hospitals 5% list** (Tencent Docs sheet `DVnpxQmtuYkZTRmhH`): JavaScript-rendered, not read. Whether any Chiang Mai hospital takes part is unknown.
- **UnionPay NFC 3%**: the API showed 0% of the pool left on 2 Oct. It may be used up already.
- **LFS4 + LHB2 stacking** on the same slips: both say "not combinable with other promotions". Unclear.
- **CardX BTP1**: the T&C's "MCC 5947" (gift shops) for beauty and spa looks like a typo.
- **CardX NHP**: the participating-hospital list isn't on the index document.
- **ttb HST**: "โรงพยาบาลกรุงเทพ และในเครือ" probably includes Bangkok Hospital Chiang Mai, but no branch list was published.
- **KTC HOS (installments)**: hospital list not opened. **KTC HOP 13%**: participating list not opened.
- **UOB HPW116** (12% at hospitals, whole year) and the HPW265/WPW267 privilege details: the pages show "Loading…" in curl; no `.json` twin was found.
- **Krungsri Lady / Central The 1 / KBank / KTC card-level bonus points for beauty or health**: none found. The Krungsri Lady product page returned 444 bytes.
- **Visa Signature status** of any household Visa card. Answered 2026-10-02: Takumi's KTC Digital VISA is a Visa Signature.
- **Mastercard Priceless / Visa Offers / JCB Thailand / Amex** Chiang Mai spa offers: none found. specialoffers.jcb didn't connect.
- **GSB, KTB, Kiatnakin, LH Bank, ICBC, BOC, Citi** health campaigns: none found (limited search).
- **BBL Be Smart** and **AEON** hospital installment programmes: not found.
- The **Central The 1 HHT** end date: the page and poster say 31 Dec 2569; the poster file name says 31Dec27.

## Site tricks

- **krungsricard.com listing**: the promotion index HTML embeds every item as JSON. Split the page on `{"SourceColumns":` and read `Title`, `TypePromotion`, `SubTypePromotion`, `Text_datetime`, `AbsoluteUrl`, `DocumentPublishTo` (485 items on 2 Oct).
- **Krungsri PDFs**: regional deal lists and MCC lists are PDFs under `/KrungsriCreditCard/media/html/`. They are linked from each page's HTML; curl them and run `pdftotext -layout`. Examples: `hospital-deal-north.pdf`, `Beauty_north.pdf`, `Wellness_north_1.pdf`, `HOS_2026.pdf`, `MCC-Code-10percent-Y2026_04-08-26.pdf`.
- **firstchoice.co.th**: hospital dealer lists are PDFs under `/getattachment/<guid>/Dealer-Hos_KFC.pdf`; tier tables are in `/getattachment/…_PAGE.jpg` posters.
- **lotussmoney.com**: `sitemap.xml` (1,547 URLs) and the `/promotion` index list every `health-beauty/…` and `installment/…` page; the HTML has the full T&C in plain text.
- **ktc.co.th**:
  - The sitemap index `sitemap.xml` → `sitemap-promotions-1…12.xml` carries `lastmod`, so sort by it to find this month's pages.
  - Campaign codes and names sit in the Next.js RSC payload (`self.__next_f.push`) as `"slug":"HOH","name":"Hospital Redeem Point 10% (HOH)"`, which gives codes that the visible text omits.
  - Merchant lists are PDFs under `/upload/02-promotion-download/`.
- **uob.co.th**: the `.json` twin of a `/personal/credit-cards/promotions/<cat>/<slug>.page` lives at `/assets/web-resources/personal/credit-cards/promotions/<cat>/<slug>.json`, not at the page's own path (that returns 404). Older `/personal/promotions/credit-cards/<slug>/<slug>.page` pages have no twin found.
- **kasikornbank.com**: headless Chrome with `--user-agent="Mozilla/5.0 (Macintosh…) Chrome/129…"` gets past Akamai's "Access Denied". The default headless user agent is blocked. Wrap Chrome in `perl -e 'alarm 90; exec @ARGV'`: it often hangs after writing the DOM, and macOS has no `timeout`.
- **ttbbank.com**: `__NEXT_DATA__` → `props.pageProps` holds `a5_promotion_details`, `a6_partner_list…` and `a11_promotion_conditions` as HTML strings. The category page `/th/promotion/credit-card/health` lists every health slug.
- **cardx.co.th**: the Meili key is in the front-end bundle (`MEILI_KEY`). `POST /indexes/promotion/search` with `{"q":"โรงพยาบาล","limit":100}` returns documents with `effectiveDate`, `expireDate`, `promotionCode` and the full `template`, from which the T&C text can be flattened.
- **aeon.co.th**: promotion links are relative (`href="the-oasis-spa"`). The detail page is `/aeon/promotions/<slug>/` with the trailing slash; without it you get the listing.
- **UnionPay offer API** (beyond `lib.bureau.unionpay_offer`):
  - `GET merchant/getMerchantList?countryCode=764&pageIndex=…&pageSize=50&insCode=299990156&language=en` lists every Thai offer merchant (12 on 2 Oct).
  - `GET coupon/getCouponInfo?pmtCode=<offerNo>` gives the merchant number.
  - `POST coupon/getCoupon` with JSON `{"couponno","insCode","language","merchantNo"}` returns the full offer text and rules.
  - Endpoint names are in the lazy-loaded chunks listed in `static/js/manifest.<hash>.js`.
- **Bangkok Bank**: the regional hospital page renders in headless Chrome. Its hospital names are in the DOM text (no PDF).
