---
tags: [catalogue-research, 2026-10]
researched: 2026-10-01
---

> **Research snapshot**: The merchants' own deals and wallets — October 2026 research. Scope: Makro, GO Wholesale and Shopee's own campaigns, TrueMoney / ShopeePay / SPayLater, the government 60/40, cashback portals. Read on **2026-10-01** from the official pages, for the October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions (HTML, JSON, posters) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# Merchants & wallets — October 2026 (Makro · GO Wholesale · Shopee)

Researcher: `merchants-wallets`. Read 1 Oct 2026 (1 ต.ค. 69), 03:00–03:50 local time. Read-only; no Notion.
Scope: everything that is **not** a bank-card promotion at the three merchants (the merchant's own campaigns, loyalty points,
wallets and QR, BNPL, the government co-payment scheme, cashback portals), plus the card promotions **GO Wholesale itself
re-posts** and what could be found of **Shopee's bank-code hub**.

Raw files (HTML/DOM dumps, JSON, posters): `…/scratchpad/research/merchants-wallets/` (`gw_*`, `mk_*`, `mk37_*`, `mkc_*`,
`tmn_*`, `gov_*`, `sp_*`, `as_*`, `gp_*`, `hc_*`, `sb_*`, `banks/`).

How pages were read:
- **GO Wholesale** (Cloudflare blocks curl, including `wp-json`): headless Chrome `--dump-dom` works for every page. Posters
  were pulled with a same-origin `fetch()` from inside Chrome.
- **Makro PRO**: curl works, and the data is in `__NEXT_DATA__` (Strapi "flexi pages"). Banners are on `strapi-cdn.mango-prod.siammakro.cloud`.
- **TrueMoney**: Cloudflare blocks curl, but the `r.jina.ai` reader works.
- **Shopee** `shopee.co.th/m/*` pages give a slider captcha (`scene=crawler_item`) to curl, to headless Chrome and to headed
  Chrome over CDP. The chrome-devtools MCP profile was locked by another session, so I didn't use it. What did work:
  the **App Store / Google Play listings** (Shopee Thailand's own promotional text and screenshots), the **Help Center API**
  (`help.shopee.co.th/api/inhouse/hc/mobile/v1/...`, open to curl), and the banks' own Shopee pages.

Legend: **Confidence**: `verified (official page)` / `third-party only (<source>)` / `unverified`.
**Status vs Sep**: new / continuing / changed / ended 30 Sep (successor?). Household cards are marked 🏠.

---

## Most important changes vs September

1. **Government co-payment**: the successor is **“ไทยช่วยไทย พลัส (60/40) (เพิ่มเติม)”**. It runs 1 Oct – 30 Nov 69:
   the state pays 60%, up to ฿200/day and **฿1,000 per person for the whole scheme**. Confirm your right in เป๋าตัง between
   1 and 15 Oct. **Makro and GO Wholesale still can't take it.** The shops that can are non-juristic operators, ธงฟ้า
   shops, village-fund and community-enterprise shops, juristic persons with revenue ≤ ฿1.8M, public transport and food
   delivery. Makro PRO's “ไทยช่วยไทย พลัส (30 ก.ย.–13 ต.ค. 69)” is only a **price-cut product collection**, not the 60/40.
2. **Makro 37th anniversary is over.** Stamp Hunt and missions ended 29 Sep and lucky-draw entries closed 29 Sep. The
   draw is **15 Oct 69 at 11:00** and **results come out 20 Oct 69 at 11:00** at every branch and on makro.co.th.
3. **Makro PRO October** has no 10.10 or bank-partner page. What it has:
   - **Referral** “ชวนปั๊บ รับพอยท์”, 1–31 Oct: up to 30 PRO Points for each friend you bring in.
   - **New-customer pack**, 1 Oct – 31 Dec: ฿100 off ฿1,000, free delivery on a first order of ฿500+ sent as “ส่งด่วน”,
     and one ฿1 item for 1 point.
   - **Point-expiry reminder**: points must be used by 31 Dec 69.
   - **Makro Club** (paid, ฿1,299/yr, running since Dec 2025): **1 PRO Point per ฿100 (1%)** on participating items, up to
     1,500 points a month. A TrueMoney partner perk adds 1% more.
4. **TrueMoney at Makro**: “Makro_THT” (double PRO Points on TrueMoney slips of ฿1,000+) **ended 30 Sep**, and there's no
   successor. **Pay Next / Pay Next Extra 3% cashback round 4 runs 1 Oct – 31 Dec** (20,000 rights, ฿100 cap per round).
   The page still showed the round-3 “สิทธิ์เต็มแล้ว” (quota full) banner when I read it.
5. **GO Wholesale**:
   - New card promos GO re-posts: **SCB CardX `HY1`** (1 Oct – 31 Dec, per slip ฿40 / ฿200 / ฿720, cap ฿1,440 a month and
     ฿4,320 in all), **ttb `BGO`** (1 Oct – 31 Dec, the same ฿50 / 100 / 450 / 1,500 tiers, a fresh ฿1,500 cap), and
     **Central The 1 T1 MAGICAL DAY** (1–13 Oct: a ฿4,000 slip earns a ฿1,000 Magic e-Voucher plus a ฿2,000 CRC pack;
     register `CRCT1` in UCHOOSE; first 2,500 people).
   - **The 1 PAYDAY** (1,500 pts → ฿400) **ends today, 1 Oct**. No October round is posted yet.
   - The fresh-vegetable ฿90 coupon runs **30 Sep – 13 Oct**, and a new Namthip “Hug the Earth” gives +100 points.
   - Stick & Save and GO Pick The Deal ended 30 Sep with no successor.
6. **Shopee 10.10 “ทั้งลด ทั้งแถม”**, per Shopee's own App Store listing: **collect codes from 7 Oct, use them 9–12 Oct only**.
   It offers ร้านโค้ดคุ้ม shops at 30% off, buy-1-get-1 deals and free shipping from ฿0.
   - The listing screenshots also show SPayLater 0% for up to 12 months, 25% Coins cashback capped at 1,500 Coins, and
     flash slots at 00:00, 12:00, 18:00 and 20:00. These are illustrative marketing images, not terms.
   - October **Payday** isn't announced yet.
   - Shopee's **bank-code hub is captcha-blocked**. Bank pages already carry October codes (KTC, First Choice, AEON; see §3.7).

## What happened to September's items

| Sep item (draft section) | Oct status |
|---|---|
| Makro PRO Points 1/฿1,000 (makro §10) | continuing, unchanged; redeem expiring points by 31 Dec 69 |
| 37th anniversary Shopping Mission / Stamp Hunt (makro §10) | **ended 29 Sep**, no October round |
| 37th anniversary lucky draw (makro §10) | entries closed 29 Sep; **draw 15 Oct, results 20 Oct** |
| TrueMoney first payment at Makro → 50–100 pts (makro §10) | continuing to 31 Dec; the official page says **50** points |
| `TMN MAKRO` (card linked in TrueMoney) (makro §10) | continuing |
| Pay Next / Extra 3%, max ฿100 per round (makro §10) | **new round 4, 1 Oct – 31 Dec** (20,000 rights) |
| Pay Next Extra 0% 48 months + up to ฿4,200 (makro §10) | continuing to 31 Dec |
| TrueMoney “Makro_THT” ×2 points (not in draft) | **ended 30 Sep**, no successor |
| UnionPay QR 6% (makro §10) | bank or network side; Makro acceptance still unconfirmed |
| ไทยช่วยไทยพลัส 60/40 (makro §10) | ended 30 Sep; **successor “(เพิ่มเติม)”, 1 Oct – 30 Nov**; Makro and GO still not eligible |
| GO: The 1 earn 1/฿100, 800 pts = ฿100 (go §11) | continuing |
| GO: The 1 PAYDAY 25 Sep – 1 Oct (go §11) | **ends 1 Oct**; no October round posted |
| GO: Super Wednesday 800 → ฿200 (go §11) | continuing (7, 14, 21, 28 Oct) |
| GO: fresh-veg ฿90 coupon 30 Sep – 13 Oct (go §11) | continuing |
| GO: Stick & Save (go §11) and GO Pick The Deal (go §3) | **ended 30 Sep**, no successor listed |
| GO: ShopBack 1% (go §11) | continuing |
| GO: Visa ฿500 coupon / Mastercard Friday (go §10) | continuing (to 31 Oct / 25 Dec) |
| GO re-posts: CardX SP1, ttb BMG (go §2, §4) | ended 30 Sep; **successors CardX HY1 and ttb BGO, 1 Oct – 31 Dec** |
| GO re-post: T1 MAGICAL DAY (go plan §9) | **new, 1–13 Oct** (`CRCT1`) |
| Shopee Payday 23–30 Sep (shopee §12) | ended; **October Payday not announced** |
| Shopee Tuesday Xtra, daily 12:00 Mall 30%, day-1 deals, Live/Video codes (shopee §12) | continuing per iPrice (third-party) |
| ShopeePay / SPayLater “no promo found” (shopee §12) | still nothing specific; the 10.10 banner shows SPayLater 0% up to 12 months (illustrative) |
| Shopee 9.9 | succeeded by **10.10 (collect 7 Oct, use 9–12 Oct)** |

---

# 1. Makro (แม็คโคร) — in store and Makro PRO

## 1.1 Makro / CP Axtra (the merchant's own)

### Makro PRO Point (แม็คโครโปรพอยท์) — standing earn rate
- **Mechanic**: 1 point per ฿1,000 bought (0.1%) at any branch except Fresh@Makro, or online. 1 point = ฿1 off, redeemed in
  the app or at the cashier. Points last **2 calendar years**. Alcohol, cigarettes and infant formula (stages 1–2) earn nothing.
- **When credited**: app orders are counted on the delivery date and show the next day; in-store points show the next day.
- **Oct note**: the homepage banner “Point Expiry (16 Sep – 31 Dec 26)” reads “อย่าลืม! แลกพอยท์ก่อนหมดอายุ … ถึง 31 ธ.ค. 69
  เท่านั้น” (don't forget to redeem before they expire, by 31 Dec 69). Points about to expire have to be used by 31 Dec 69.
- There are also brand “PRO Point” product collections (e.g. “Get PRO Point | Online Only”, NAMTHIP / FOREMOST / MIDEA … PRO
  Point) that give extra points on listed items. The per-item amounts are inside the app and weren't read.
- URL: https://www.makro.pro/th/static/makro-pro-point · banner: `strapi-cdn…/uploads/Web_homepage_banner_TH_3a01c23a8a.jpg`
- **Confidence**: verified (official page and banner). **Status**: continuing; the earn rate is unchanged and the expiry
  reminder is new.

### Makro Club (แม็คโครคลับ) — paid membership (not in the Sep page)
- **Fee**: ฿1,299 a year (shown as “108/เดือน”). You join and pay in the Makro PRO app. It's for individuals only, not
  juristic persons, Horeca Club or “จัดให้” members. You can cancel within 7 days for a refund.
- **Benefits** (T&C §2.1):
  - **1 PRO Point per ฿100 on participating items (1%)**, in store or in the app, capped at **1,500 points a month and
    10,000 a year**. Past the cap you're back to 1 per ฿1,000. Club-rate points expire 30 days after the membership year ends.
  - 100 points on first sign-up (credited within 8 days; use within 30 days).
  - 50 points in your birthday month (use within that month).
  - Member-only prices and partner perks from SLC & S'RENE, MorDee, Better Vision, Bangchak and TrueMoney.
- The banner says “รับพอยท์และเงินคืนรวม 2%” (points and cashback, 2% in total): 1% in points plus “รับเงินคืนเพิ่มสูงสุด 1%”
  (up to 1% more cashback) when you pay through a participating partner.
- **Makro Club × TrueMoney**: Club members get **1% in PRO Points, up to 50 points per member a month**. It applies when you
  spend **฿5,000+ a month** with Pay Next or Pay Next Extra in a branch, or through TrueMoney on any Makro PRO channel.
  No dates are shown on the banner.
- **Excluded from points**: tobacco, alcohol, formula and baby food, pharmacist-controlled drugs, purchases on
  “ลูกค้าเครดิต ซีพี แอ็กซ์ตร้า” (CP Axtra credit accounts), gift cards, and goods Makro doesn't sell itself.
- URLs: https://www.makro.pro/th/fp/makro-club-join-now · T&C https://www.makro.pro/th/static/t-n-c-for-makro-club
  (published 2025-12-03). Posters: `…/NEW_Club_Benefit_Flexi_Page_TH_top_9fefc2e2dc.png`, `…_bottom_3e2b9d7200.png`,
  `…/True_Money_TH_aa0b800967.jpg`.
- **Confidence**: verified (official T&C and posters). **Status**: continuing; it has run since Dec 2025 but the Sep page didn't list it.

### Referral “ชวนปั๊บ รับพอยท์” — 1–31 Oct 69 (new)
- Get **up to 30 PRO Points for each friend** who signs up and orders. Points arrive within 24 hours of the friend's sign-up
  and order. The Makro PRO banner is labelled “37th Anniversary | Referral Program (Oct 26)”.
- The full T&C sits behind a login (`account.makro.pro/…/referral-program`), so per-person caps and the friend's minimum
  order weren't read.
- Banner: `strapi-cdn…/uploads/WHB_Banner_TH_1_9bd5187539.jpg`. **Confidence**: verified (official banner); details unverified.
  **Status**: new.

### New-customer pack “เริ่มช้อป ก็คุ้มเลย!” (RAK MAK MAKRO x LYKN) — 1 Oct – 31 Dec 69 (new)
- **฿100 off a ฿1,000 basket** (10%). Only for a new customer's **first order in the Makro PRO app**, 1 use per member ID
  (MMID). Makro checks the ID card number, IP address and delivery address for repeat use.
- **Free delivery** (“ส่งฟรีทั่วไทย”) on a first order of **฿500+**, only when you pick **“ส่งด่วน”** (express). 1 use per Makro ID.
- **1 point buys a ฿1 item**: new customers pick 1 of 3 listed items. Stock is limited and varies by branch.
- Household relevance: little, since Takumi and Baiboon are existing Makro members.
- URL: https://www.makro.pro/th/fp/live-like-a-pro-makro · posters `…/Acquitsition_1_Oct_30_Dec_Image_Stacker_TH_1/2/3_*.png`.
- **Confidence**: verified (official page and posters). **Status**: new; the Sep equivalent wasn't in the draft.

### Makro PRO delivery fees (standing)
- Delivery is free on orders of **฿999+ within 40 km**. At 40–49.9 km it costs ฿49, at 50–59.9 km ฿99, and beyond 60 km
  the address is out of the service area. FAQ “updated 30 Apr 2026”.
- URL: https://www.makro.pro/th/static/faq. **Confidence**: verified. **Status**: continuing.

### “รักมาก แม็คโคร 37 ปี” — 37th anniversary (22 Jul – 29 Sep 69)
- **Stamp Hunt Unlock** (1 stamp per ฿1,000 in store or on Makro PRO; 2 stamps = instant discount, 4 = coupon, rewards every
  2 weeks): the poster reads “ระยะเวลากิจกรรม 22 ก.ค. 2569 – 29 ก.ย. 2569” (activity period). **Ended 29 Sep.**
- **Shopping Mission**: the page is now an empty shell. **Ended**, with no October round seen.
- **Lucky draw**: one entry per ฿2,000 per receipt; entries closed 29 Sep. **Drawing: 15 Oct 69 from 11:00** at Makro head
  office. **Results: 20 Oct 69 from 11:00**, posted at every branch entrance and on https://www.makro.co.th. Winners must
  claim within 30 days and pay 5% withholding tax on prizes of ฿1,000+. Prizes include an Isuzu X-Series pickup and
  37,000 Makro PRO Points (value ฿37,000).
- **Bank Partner (22 Jul – 30 Sep 26)** section: **ended**. No October bank-partner flexi page was found; I probed
  `fp/1010`, `fp/10-10`, `fp/bank-partner` and the like, and all returned 404.
- URLs: https://www.makro.pro/th/static/makro-37th-anniversary-lucky-draw (licence 1695/2569) ·
  https://www.makro.pro/th/fp/makro-37th-anniversary-activity-stamp-hunt · poster `mk37_Image_Stacker_TH_1_e01012c336.png`.
- **Confidence**: verified. **Status**: ended 29 Sep; the draw and results are still to come.

### October price campaigns on Makro PRO and in store (product prices, not payment offers)
- **Makro Mail 21**, 30 Sep – 13 Oct (flyer): https://www.makro.pro/th/fp/makro-mail-21-2026 and https://www.makro.co.th/Makromail21
- **“ไทยช่วยไทย พลัส ยกทัพแบรนด์ดัง ช่วยผู้ประกอบการประหยัดต้นทุน”** (Thai Helps Thai Plus: big brands help business owners
  save on costs), 30 Sep – 13 Oct. It's a discounted-product collection (e.g. Crystal water, Khao San Dee rice, Wai Wai
  noodles), **not** the government 60/40. URL: https://www.makro.pro/th/fp/thai-helps-thai
- **“แม็คโครเคียงข้างคุณ”** (Makro stands by you): flood-relief essentials, 28/30 Sep – 13 Oct. URL: https://www.makro.pro/th/fp/flooding-promotion
- **Mega Saving “ซื้อเยอะ ถูกกว่า!”** (buy more, pay less), 30 Sep – 6 Oct. **Home Cleaning Big Saving**, 1–7 Oct.
- **Vegetarian festival “J Your Way”**, 30 Sep – 18 Oct. **HORECA Quality Products**, 2 Sep – 1 Nov. **Gold Container**
  daily deals, dated daily.
- **Confidence**: verified (homepage JSON). **Status**: new cycle; these are not payment offers.

## 1.2 TrueMoney / Ascend (wallet, Pay Next BNPL) at Makro

In store, pay by showing the **TrueMoney barcode for the cashier to scan**. Paying by **scanning Makro's PromptPay QR with
TrueMoney joins no promotion**; the TrueMoney Makro page says so. A credit card linked in TrueMoney posts as **`TMN MAKRO`**.

### Pay Next / Pay Next Extra — 3% cashback on every payment, **round 4: 1 Oct – 31 Dec 69** (successor round)
- **Mechanic**: **3% back** on each Pay Next or Pay Next Extra payment of **฿100+**, at participating shops. The page is
  filed under Makro.
- **Caps**: ฿100 per registration round. If you use both Pay Next and Pay Next Extra, the ฿100 is shared. Each round has
  **20,000 rights** (80,000 across the four rounds of 2569); rounds are 1 Feb–31 Mar, 1 Apr–30 Jun, 1 Jul–30 Sep (marked
  full) and **1 Oct–31 Dec**.
- **Registration**: once per round, from the banners in the TrueMoney app (“กดรับสิทธิ์” → “เริ่มใช้เลย”).
- **Crediting**: instant, into the TrueMoney wallet linked to Pay Next.
- **Exclusions**: energy drinks, alcohol, tobacco, infant and follow-on formula (0–3 yrs), pharmacies, gift cards and mobile
  top-up cards. It **can't be combined with other promotions** (clause 8).
- **Stacking with points**: Pay Next and Pay Next Extra payments earn **TrueMoney Coins ×3** (1 base coin per ฿20 plus
  2× extra). Base store coins are capped at 50 a month, and the ×3 total at 465 a month.
- URL: https://www.truemoney.com/a/paynext-extra-promotion-02/ (banner `…/2025/05/Ascend-Paynext_Ascend-Paynext-Extra-promotion-02-banner-20260331-700x440-1.jpg`)
  · coins https://www.truemoney.com/a/redirect-paynext-extra-makro-coinx3/
- **Confidence**: verified (official page, read through r.jina.ai). When read at 03:08 on 1 Oct the page header still said
  “ขออภัยสิทธิ์เข้าร่วมแคมเปญเต็มแล้ว” (sorry, the campaign is full), which is left over from round 3. Check the app before relying on it.
  **Status**: continuing; the new round started 1 Oct.

### Pay Next Extra — 0% for up to 48 months on appliances, plus cashback up to ฿4,200 — 1 Mar – 31 Dec 69
- **Step 1**: 0% for up to 48 months on participating appliances at Makro, paid with Pay Next Extra.
- **Step 2**: instant cashback into TrueMoney, by installment amount per transaction:

  | Installment amount | Cashback |
  |---|---|
  | ฿3,000–8,000 | ฿100 |
  | ฿8,001–15,000 | ฿200 |
  | ฿15,001–45,000 | ฿300 |
  | ฿45,001–65,000 | ฿600 |
  | ฿65,001–80,000 | ฿1,000 |
  | ฿80,001+ | ฿2,000 |

- **Caps**: 1 use per tier per transaction per ID card per month; **฿4,200 per ID card per month**; **2,750 rights for the
  whole campaign**.
- **Registration**: once, before the first installment. Doesn't combine with other promotions. Interest is 25% p.a. if not
  paid on time.
- URL: https://www.truemoney.com/a/promotion-makro-02/. **Confidence**: verified. **Status**: continuing.

### “จ่ายครั้งแรกที่แม็คโคร รับ 50 แม็คโครโปรพอยท์” (first TrueMoney payment at Makro) — 15 Feb – 31 Dec 69
- **50 PRO Points** on your **first-ever TrueMoney payment at Makro** of **฿1,000+ after discounts**, in store or on Makro
  PRO. New-to-TrueMoney-at-Makro customers only; one per TrueMoney account; you must press “ลงทะเบียนเพื่อรับสิทธิ์”
  (register) first.
- Points reach the Makro account **by the 15th of the next month**.
- Note: the Sep draft said “50–100 คะแนน”; the official page says **50**.
- URL: https://www.truemoney.com/a/promotion-makro-01/. **Confidence**: verified. **Status**: continuing.

### “Makro_THT (Thai Help Thai)” — double PRO Points with TrueMoney — **ended 30 Sep 69**
- It gave one extra multiple of PRO Points (capped at **+5 points per ID per month**) on TrueMoney payments of ฿1,000+ per
  receipt for **designated items**, in Makro branches, 1 Jul – 30 Sep 69.
- **No October successor** was found. The TrueMoney promotion list still shows it, and `makro-promotion-06…20` and
  `promotion-makro-03…06` are 404 or expired.
- URL: https://www.truemoney.com/a/makro-promotion-05/. **Confidence**: verified. **Status**: ended 30 Sep, no successor.

### Paying by credit card through TrueMoney at Makro — since 15 Oct 68
- Link a credit or debit card in TrueMoney and choose it when paying at Makro. There's no minimum and no fee. Slips post as
  `TMN MAKRO`.
- URL: https://www.truemoney.com/a/makro-promotion-04/. **Confidence**: verified. **Status**: continuing (standing).

## 1.3 Other wallets and QR at Makro
- **LINE Pay / Rabbit LINE Pay**: the official promotions page https://pay.line.me/portal/th/about/promotions shows “ไม่พบโพสต์”
  (no posts), as it did on 30 Sep. **Nothing found.**
- **ShopeePay / SPayLater**: no Makro promotion found. SPayLater can now **scan merchant PromptPay QRs**; the Help Center
  article [183049](https://help.shopee.co.th/portal/4/article/183049) offers 0% for 1 month and installments up to 12 months.
  Whether Makro's own PromptPay QR accepts it is **unverified**.
- **Alipay+**: nothing Makro-specific found.
- **PromptPay bank-app QR promos**: only the banks' own card-QR promotions (K PLUS, SCB EASY / CardX, UCHOOSE, KTC Mobile),
  which the bank researchers cover. No wallet-type PromptPay promo was found.
- **UnionPay QR 6% (KTC Mobile)** belongs to the banks' side; see `docs/promotions/unionpay-qr.md`. Whether Makro accepts
  UnionPay QR is **still unconfirmed**.

## 1.4 Government co-payment “ไทยช่วยไทย พลัส (60/40) (เพิ่มเติม)” — 1 Oct – 30 Nov 69 (successor)
- **Mechanic**: the state pays **60%**, **up to ฿200 per person per day** and **฿1,000 per person for the whole scheme**
  (Oct–Nov 69). The person pays 40%. You spend it through **G Wallet in เป๋าตัง**, face to face, by scanning the shop's
  QR, 06:00–23:00. Food-delivery orders run 06:00–21:00 and cover food only, not delivery fees.
- **Eligibility**: Thai nationals aged 18+. You must **confirm your right in เป๋าตัง between 1 and 15 Oct 69**. Two groups
  qualify:
  - holders of the first 60/40 right who didn't pass the 2569 welfare-card screening, and
  - 2565 welfare-card holders who failed the 2569 screening, plus listed marginal groups.
  People suspended from คนละครึ่ง phases 1–5, คนละครึ่ง พลัส or the first 60/40 are excluded.
- **Eligible shops**: non-juristic operators, ธงฟ้า shops, village-fund and community-enterprise shops, small juristic
  persons (revenue ≤ ฿1.8M in the 2567 tax filing), public transport, and food-delivery shops tied to one platform. No
  franchise convenience stores; no massage, spa, nail or hair services.
- **Makro / GO Wholesale: not eligible.** Both are large juristic companies. thailand.go.th's guide to the first phase names
  “Big C, Lotus's, Makro, 7-Eleven, Tops” as modern trade that **can't** take 60/40, and says those chains ran parallel
  “ไทยช่วยไทย” price cuts instead.
- In the first phase, CP Axtra ran “ศูนย์รวมร้านค้าไทยช่วยไทยพลัส” (a hub for 60/40 shops) with 1,500+ free booths and
  10,000+ small shops on Makro and Lotus's sites. Whether those booths run again for the extra phase is **unconfirmed**.
- Welfare-card holders: the limit rises to ฿1,000 a month in Oct 69, from ฿300 (per THE STANDARD).
- URLs: official https://www.ไทยช่วยไทยพลัส.th/home (read through r.jina.ai; banners `gov_Citizens2.png` and `gov_Mer2.png`
  show 1–15 Oct confirmation, use 1 Oct – 30 Nov, and “ใช้สิทธิได้ 1,000 บาท ตลอดโครงการ … วันละไม่เกิน 200 บาท/คน/วัน”, i.e.
  ฿1,000 for the whole scheme, at most ฿200 a person a day) · https://thailand.go.th/public/index.php/guide-book-detail/-6040--2569----
  (first-phase merchant rules) · https://thestandard.co/thai-chuay-thai-plus-60-40-2/ (22 Sep 69).
- **Confidence**: verified (official site). The Makro exclusion is verified for phase 1 (thailand.go.th) and implied for the
  extra phase by the official merchant criteria. **Status**: ended 30 Sep, with the successor running 1 Oct – 30 Nov.

---

# 2. GO Wholesale (โก โฮลเซลล์, Central Food Wholesale; slips `CFW-<BRANCH> …`)

The promotion list was read at 03:00 on 1 Oct: https://centralfoodwholesale.co.th/promotion/ (TH) and /en/promotion/.
The TH and EN lists match, except that the EN list still shows “ซื้อ 2 ชิ้น คุ้มกว่า (2–15 ก.ย.)” (buy 2, pay less; expired)
and gives different dates for the installment item (see §2.3).

## 2.1 GO Wholesale / The 1 (merchant and loyalty)

### The 1 points at GO (standing)
- GO members linked to The 1 earn **1 point per ฿100**, in store and in the GO app. **800 points = a ฿100 cash coupon**,
  so the return is 0.125%.
- With a **Central The 1 credit card** 🏠 (REDZ …2611: Takumi, and Baiboon's supplement) you earn **up to 10 points per
  ฿100 per slip** (9 from the card plus 1 as a GO member), 5 Mar 68 – 31 Dec 69. Installments, QR and e-wallets don't earn.
- URLs: https://centralfoodwholesale.co.th/membership/ · https://centralfoodwholesale.co.th/promotion/the1-creditcard-point/
- **Confidence**: verified. **Status**: continuing.

### 7 วันเท่านั้น! The 1 PAYDAY (seven days only) — 25 Sep – 1 Oct 69 (**ends today**)
- Redeem **1,500 The 1 points for ฿400 off** any purchase of **฿4,500+ per receipt**; normally 800 pts buys ฿100. Redeem and
  use in the The 1 app only. 1,000 rights in total, 1 coupon per member and 1 per receipt.
- Excluded: alcohol, cigarettes, infant formula, medicines, bulk or Credit Sales purchases, and vouchers.
- **October round: not posted yet** (as of 03:00 on 1 Oct).
- URL: https://centralfoodwholesale.co.th/promotion/the1-pay-day/ · poster `…/2025/07/The-1-PAY-DAY-25-Sep-1-Oct-2026-01.jpg`
- **Confidence**: verified. **Status**: ends 1 Oct; successor not yet announced.

### The 1 แลกคุ้ม ทุกพุธ (Super Wednesday) — 7 Jan – 27 Dec 69
- Redeem **800 points for ฿200 off ฿2,500+ per receipt** (฿0.25 a point). Redeem on **Wednesdays** only and use Wednesday to
  Sunday. **300 rights per round**, 1 per member. The same product exclusions as PAYDAY apply.
- October Wednesdays are 7, 14, 21 and 28 Oct.
- URL: https://centralfoodwholesale.co.th/promotion/the1-super-wednesday/ (link `offers.onelink.me/H3Sq/hubcfw55`)
- **Confidence**: verified. **Status**: continuing.

### The 1 Exclusive coupon — 1 Jan – 31 Dec 69
- **The 1 Exclusive tier only**: ฿300 off ฿12,000+ per receipt. 1,000 rights a month, 1 per member.
- URL: https://centralfoodwholesale.co.th/promotion/the1-exclusive/. **Confidence**: verified. **Status**: continuing
  (the Sep page didn't list it).

### The 1 Hug The Earth — 30 Sep – 27 Oct 69 (new)
- **+100 The 1 points** for buying **5+ packs of Namthip water** (550 ml ×12, 1.5 L ×6 or 350 ml ×12), in store or in the GO
  app. You must register first at https://go.the1.co.th/UohD/566spxnq; spending before you register doesn't count.
- Points arrive within 30 working days after the campaign ends.
- URL: https://centralfoodwholesale.co.th/promotion/the1-hug-the-earth/. **Confidence**: verified. **Status**: new.

### ยิ่งซื้อ ยิ่งลด! Fresh-vegetable coupon — 30 Sep – 13 Oct 69
- Buy **฿300+ of listed vegetables, mushrooms and big-bag chillies** in one receipt (80 SKUs listed) and get a **฿90 coupon**
  through the GO WHOLESALE app. That's 30% of the ฿300 threshold.
- **14 uses per member** over the campaign. It works in every branch, through branch sales staff and in the GO app. The
  poster carries the “ไทยช่วยไทย ลดภาระ ลดค่าครองชีพ” price-relief logo.
- URL: https://centralfoodwholesale.co.th/promotion/fresh-vegetable-coupon/ · poster `…/2026/09/BM20-fresh-coupon-30-sep-13-oct-26-03.jpg`
- **Confidence**: verified. **Status**: continuing (new round).

### Price campaigns (not payment offers)
- **FF Weekly “7 วันเท่านั้น! โปรลด สดใหม่”** (seven days only: fresh-produce deals), 30 Sep – 6 Oct: https://centralfoodwholesale.co.th/promotion/ff-weekly/
- **E-Catalog “GREAT OFFERS! โปรลดแรง ขายง่าย กำไรเพิ่ม”** (big discounts, easy to resell, more margin), 30 Sep – 13 Oct.
  **“เทศกาลกินเจ อิ่มบุญ อิ่มใจ”** (vegetarian festival), 30 Sep – 18 Oct.
- **Ended 30 Sep, no successor listed**: **Stick & Save “แปะอะไรก็ลด”** (whatever you stick on is discounted; sticker book,
  19 Aug – 30 Sep) and its card-linked **GO Pick The Deal** ฿65 coupon.
- **Confidence**: verified (list page). **Status**: as noted.

### GO app offers
- No October app-only offer (new-user code, free delivery) is posted on centralfoodwholesale.co.th.
- **ShopBack**: **1% cashback** on GO Wholesale online, tracked through ShopBack. https://www.shopback.co.th/gowholesale.
  **Confidence**: third-party only (ShopBack). **Status**: continuing.

## 2.2 Card promotions GO re-posts — **new for October**

### SCB / CardX — supermarket-hypermarket cashback `HY1` — 1 Oct – 31 Dec 69 (successor to SP1)
- **Cards**: every CardX and SCB WEALTH by CardX card (SCB Private Banking, First, Prime), SCB cards not yet reissued, and
  CardX FLEX (SMS `FHY`). Not SPEEDY CASH. 🏠 **Nuta's CardX JCB** qualifies.
- **Channel**: GO WHOLESALE stores, GO app and web. The GO copy lists only GO under “ร้านค้าที่ร่วมรายการ” (participating
  shops); CardX's own page may list more, so check the bank researcher's report.
- **Per-slip mechanic, full payment only**:

  | Spend per slip | Cashback | Effective rate |
  |---|---|---|
  | ฿3,000–9,999 | ฿40 | ≤ 1.33% |
  | ฿10,000–29,999 | ฿200 | ≤ 2.0% |
  | ฿30,000+ | ฿720 | ≤ 2.4% |

- **Caps**: ฿1,440 per person a month and ฿4,320 per person for the campaign, across all cards.
- **Registration**: once, for each card you want to use: CardX app or web, or SMS `HY1 <last 12 digits>` to 4545777.
  Crediting is within 60 days after the campaign ends.
- **Extra step**: **฿3,000** when accumulated spend reaches **฿300,000** over 1 Oct – 31 Dec. 150 rights, SMS `HYP`.
- **POINTX redemption**: redeem points equal to the slip for **12% cashback (Mon–Thu) or 14% (Fri–Sun)**, with no limit.
  Register each time, the same day, with SMS `HY2 <last 12> <slip amount>`. CardX FAMILY PLUS is excluded.
- **Exclusions**: every kind of installment (including ดีจัง 0%), ShopeePay, Rabbit LINE Pay, commercial use.
- **ดีจัง แบ่งจ่าย 0% 4 เดือน** (0% over 4 months): slips of ฿2,000+, but installment slips lose points and cashback.
- URL: https://centralfoodwholesale.co.th/promotion/scb-cashback-oct26/
- **Confidence**: verified (GO's official page). **Status**: new; it succeeds SP1 (฿700 cap, ended 30 Sep).

### ttb — hypermarket cashback `BGO` — 1 Oct – 31 Dec 69 (successor to BMG)
- **Cards**: every personal ttb card, including TMB, Thanachart, ttb Global House and ttb Disney, primary and supplement.
  🏠 Takumi's and Baiboon's **ttb so smart** qualify.
- **Channel**: hypermarket stores and online (GO in store and online). E-wallets are excluded. Makro PRO is **not** part of
  BGO; see `docs/promotions/ttb-2026.md`.
- **Per-slip mechanic** (tier table from poster `…/2026/09/ttb-table-1.png`):

  | Spend per slip | Cashback | Effective rate |
  |---|---|---|
  | ฿3,000–4,999 | ฿50 | ≤ 1.67% |
  | ฿5,000–19,999 | ฿100 | ≤ 2.0% |
  | ฿20,000–99,999 | ฿450 | ≤ 2.25% |
  | ฿100,000+ | ฿1,500 | 1.5% |

- **Cap**: **฿1,500 per person for the whole campaign**, across all primary and supplement cards and every participating
  hypermarket. It's paid to the one primary card with the highest spend.
- **Registration**: once, on or before the day of the transaction: ttb touch, or SMS `BGO <last 12>` to 4899777.
  ttb reserve infinite is enrolled automatically. Crediting is within 60 days after the end; disputes within 90 days.
- Stacks with the ttb so smart 1% card cashback (card policy). **ttb so goood 0% for 3 months** on slips of ฿1,000+.
- URLs: https://centralfoodwholesale.co.th/promotion/ttb-cashback-oct26/ · tent card `…/2026/09/GO-WHOLESALE-Tent-Card-Insertion-10.5x7.3-cm-1.jpg`
- **Confidence**: verified. **Status**: new; it succeeds BMG (ended 30 Sep). The cap is fresh.

### Central The 1 credit card — **T1 MAGICAL DAY** — 1–13 Oct 69 (new)
- **Cards**: Central The 1 credit cards, including **UCHOOSE QR Payment**. Supplement spend counts toward the primary, and
  rewards go to the **primary holder only**, who needs UCHOOSE. 🏠 Takumi's REDZ …2611 and Baiboon's supplement, with the
  rewards landing with Takumi.
- **XL Pack**: a single slip of **฿4,000+** at one Central Retail store earns a **Magic e-Voucher worth ฿1,000** plus a **CRC
  Exclusive Pack worth ฿2,000**. Eligible stores: Central, Robinson, Supersports, **GO Wholesale**, Thai Watsadu, BnB Home,
  Auto1, Power Buy, OfficeMate, including their online channels.
  - The e-voucher alone is worth 25% of a ฿4,000 slip; the poster headline reads “มูลค่าสูงสุด 25% (รวมสูงสุด 1,200 บาท)”
    (worth up to 25%, ฿1,200 at most).
  - **First 2,500 successful registrants.**
- **S Pack** (not GO): ฿1,000+ at MUJI, Tops, Matsukiyo or B2S earns a ฿200 e-voucher plus a ฿500 pack; first 2,500.
- **Registration**: in UCHOOSE, search **`CRCT1`**, from **1 Oct 69 at 09:00**. Register once for each pack.
- **Exclusions**: 0% 3-month EDC installments, gift cards, other wallets or QR, cancelled spend.
- **Rewards**: land in UCHOOSE within 45 days after the end and must be **used by 15 Nov 69**. Each coupon lasts 60 minutes
  once pressed. Any difference has to be paid with the card.
- URL: https://centralfoodwholesale.co.th/promotion/รับ-magic-e-voucher-1000-บ-เมื่อใช้จ่ายครบ-40/ · poster `…/2026/09/01BUCRC-Magical-DayY26Q2_1000x1000px-2.jpg`
- **Confidence**: verified. **Status**: new; the Sep page had flagged it as upcoming.

## 2.3 Card and network promotions GO lists that **continue** (details are in the bank researchers' reports)

| Item on GO's list | Period | Status |
|---|---|---|
| Central The 1 **GWS3**: per slip ฿35 / 95 / 400 / 1,800; cap ฿9,000 a month, ฿27,000 in all (`t1-cashback-27000-aug26`) | 1 Aug – 31 Oct 69 | continuing |
| Krungsri **SUP1 / SUP2** (up to ฿2,100) (`kcc-cashback2100-aug26`) | 1 Aug – 31 Oct 69 | continuing |
| KBank **HYP** supermarkets (up to ฿5,000) (`kbank-cashback-15jul26`) | 15 Jul – 31 Oct 69 | continuing |
| KTC **Visa scan-to-pay**: 3 slips of ฿1,000+ → ฿150/month, cap ฿750 (`ktc-visa-750-aug26`) | list says to 31 Oct; the Sep T&C said to 31 Dec | continuing |
| KTC **points → 13% cashback** (`ktc-cashredeem13-aug26`) | 1 Aug – 31 Dec 69 | continuing |
| UOB **SPW592** “ไม่ต้องแลกคะแนน” (no points needed), up to ฿900 (`uob-supermarket-900cashback-jul26`) | 1 Jul – 31 Dec 69 | continuing |
| AEON **NTW1** (up to ฿340 per cycle) (`aeon-cashback-jul26`) | 11 Jul 69 – 10 Mar 70 | continuing |
| KBank **0% 3 months** on goods and appliances (`kbank-installment0-jul26`) | 1 Jul – 31 Dec 69 | continuing |
| **0% installments** on Central The 1, KBank or UOB (New Year hampers, Clio, smart home: 3 months on ฿1,500+; Fresher freezers: 6 months on ฿5,000+) (`newyear26-creditcard-installment`) | body says 1 Aug – 31 Dec 69; the TH title says “1 ต.ค. 68 – 30 ก.ย. 69” and the EN title “3 เดือน … – 31 ธ.ค. 69” | continuing (the titles are inconsistent; the body governs) |
| KTC Forever points → 0% for 3 months (`ktc-installment0-feb26`) | 16 Feb 69 – 31 Jan 70 | continuing |
| Central The 1 sign-up gift: a luggage set worth up to ฿6,990 (`the1-acquisition-mar26`) | apply 1 Aug – 31 Oct 69 | continuing |
| **Visa** (any bank): tap-to-pay ฿5,000+ within 3 days across 2+ Central Retail banners → ฿500 The 1 cash coupon; 11,000 people (`crc-visa-aug2026`) | 21 Aug – 31 Oct 69 | continuing |
| **Mastercard Friday** (any Thai Mastercard): ฿100 coupon in the The 1 app on ฿1,000+ (`mastercard-friday-2026`) | 2 Jan – 25 Dec 69; October Fridays 2, 9, 16, 23, 30 | continuing |
| SCB CardX **SP1** ฿700 (`scb-cashback-700thb-jul26`) | 1 Jul – 30 Sep 69 | **ended**, succeeded by HY1 |
| ttb **BMG** ฿1,500 (`ttb-cashback1500-jul26`) | 1 Jul – 30 Sep 69 | **ended**, succeeded by BGO |

Source: https://centralfoodwholesale.co.th/promotion/ (dates as listed). **Confidence**: verified for GO's own list; the bank
terms were read on 30 Sep (see the Sep draft and `gowholesale-notes.md`).

---

# 3. Shopee (Thailand) — platform, ShopeePay, SPayLater, Coins

Caveat: Shopee's own campaign and T&C pages (`shopee.co.th/m/10-10`, `/m/partnership-vouchers-rewards`) **couldn't be read**,
because every method tried hit a captcha. The official sources used below are Shopee Thailand's **App Store and Google Play
listings** (text and screenshots published by SHOPEE THAILAND CO., LTD.) and the **Shopee Help Center**.

## 3.1 Shopee 10.10 “ทั้งลด ทั้งแถม” (10.10: discounts and freebies) — new
- **Official listing text** (App Store id959841453, TH):
  > “Shopee 10.10 ทั้งลด ทั้งแถม | ส่วนลดร้านโค้ดคุ้ม 30% | ซื้อ 1 แถม 1* | ส่งฟรี* ขั้นต่ำ 0.- | อย่าพลาด เก็บโค้ดเลย 7 ต.ค. เริ่มใช้วันที่ 9-12 ต.ค. นี้เท่านั้น”

  In English: 30% off at ร้านโค้ดคุ้ม shops, buy 1 get 1, free shipping from ฿0; collect codes from 7 Oct and use them only
  on 9–12 Oct. Google Play (updated 25 Sep 2569) reads “Shopee 10.10 ทั้งลด ทั้งแถม ส่วนลดร้านโค้ดคุ้ม 30% พร้อมดีลซื้อ 1 แถม 1*”;
  its EN listing reads “Shopee 10.10 Double Sale 30% Xtra voucher with BOGO* deals”.
  - **Collect codes: from 7 Oct 69. Use: 9–12 Oct 69 only.**
  - **ร้านโค้ดคุ้ม (Xtra) 30% shop voucher.** The cap and minimum weren't published in the listing text.
  - **Buy 1 get 1** deals and **free shipping from ฿0** at designated shops.
- **Screenshots** (official but illustrative mock-ups, so don't quote them as terms):
  - The home banner “10.10 ทั้งลด ทั้งแถม” shows “ส่วนลดร้านโค้ดคุ้ม 30%”, “ส่งฟรี ขั้นต่ำ 0” and **“SPayLater ผ่อน 0% สูงสุด 12 เดือน”** (0% for up to 12 months).
  - A voucher card reads “ส่วนลดร้านโค้ดคุ้ม 30% · ร้านโค้ดคุ้ม Xtra · ใช้ได้ 10 ต.ค. 69” (usable 10 Oct 69).
  - A Coins-cashback card reads “เงินคืน 25% Coins สูงสุด 1,500 Coins ขั้นต่ำ ฿100 (Platinum | ร้านโค้ดคุ้ม Xtra)” (25% back in
    Coins, max 1,500, ฿100 minimum).
  - The free-shipping page reads “ส่งฟรีไม่อั้น + โค้ดลดทั้งแอป”, “ส่งฟรี ร้านโค้ดคุ้ม ขั้นต่ำ ฿0 · ร้านค้าที่กำหนด · ใช้ได้ 10 ต.ค. 69”,
    with a tab for “โค้ดลดจากพาร์ทเนอร์” (the partner/bank-code hub).
  - The BOGO page shows flash slots at **00:00 / 12:00 / 18:00 / 20:00**.
- URLs: https://apps.apple.com/th/app/id959841453?l=th · https://play.google.com/store/apps/details?id=com.shopee.th&hl=th&gl=TH
  · screenshots `as_ss1–4.jpg` in the raw folder.
- **Confidence**: verified (official store listings) for the dates and headline mechanics. Screenshot figures are
  unverified (illustrative). **Status**: new (the Sep equivalent was 9.9).

## 3.2 Shopee Payday (October)
- **Not announced yet** as of 1 Oct.
- The Sep pattern (third-party only, iPrice) was 23–30 Sep:
  - Mall 30%, capped at ฿300, on ฿300+.
  - ร้านโค้ดคุ้ม 30%, capped at ฿2,000, on ฿1,000+.
  - Codes refilled at 00:00, 12:00, 18:00 and 20:00.
- A blog calendar (roonnhaidee) *forecasts* 26–31 Oct. That's speculation, not a source.
- Banks already publish Payday codes, e.g. KTC `KTCPAYDAY` (฿300 off ฿2,000, from the 25th to month-end every month,
  25 Jan – 31 Dec 69).
- **Confidence**: unverified. **Status**: the Sep Payday ended 30 Sep; October's is unknown.

## 3.3 Recurring platform codes and events (third-party only)
iPrice (`ipricethailand.com/coupons/shopee/`, still titled “กันยายน 2569”) lists these as running for another 64–94 days, i.e.
into Dec 2026. None are confirmed on a Shopee page.
- **Every 1st of the month**: ฿111 deals, a “surprise” code up to ฿1,111, and ShopeeTH live at 19:30 with codes up to 50%
  (30% all day). Today, 1 Oct, is one of those days.
- **Tuesdays** (6, 13, 20, 27 Oct): ร้านโค้ดคุ้ม Xtra up to 25% plus a free-shipping coupon up to ฿300 (99 rights).
- **Wednesdays**: “Wednesday Special” shipping from ฿9, with free shipping on participating items.
- **Daily at 12:00**: Shopee Mall 30% codes.
- **Shopee Live / Video**: codes of 25% (max ฿300) and 40% (max ฿100), plus up to 10 Coins a day for watching.
- **Shopee InstantMart**: free delivery for the first 5 km and codes up to 50% (1-hour delivery).
- **Confidence**: third-party only (iPrice). **Status**: continuing, per iPrice.

## 3.4 Shopee Coins, Shopee Rewards (standing, from the Help Center)
- **Coins**: **1 Coin = ฿1** off, in the app, at partner shops and on ShopeeFood. They **expire at the end of the 3rd month**
  after the month you got them; oldest are used first. You earn them from daily check-in, Prizes games, reviews, referrals,
  ShopeePay in-store scans, **Coins Cashback vouchers** (on items tagged “ส่วนลด ร้านโค้ดคุ้ม”, credited within 24 h of
  pressing “ฉันได้ตรวจสอบและยอมรับสินค้า”, i.e. confirming you received the goods), and watching Live and Video.
  Articles [80515](https://help.shopee.co.th/portal/4/article/80515), [80760](https://help.shopee.co.th/portal/4/article/80760)
  and [80755](https://help.shopee.co.th/portal/4/article/80755).
- **Shopee Rewards tiers**, per half-year (1 Jan–30 Jun and 1 Jul–31 Dec):

  | Tier | Orders | Spend |
  |---|---|---|
  | Silver | 6 | ฿1,500 |
  | Gold | 24 | ฿7,500 |
  | Platinum | 50 | ฿30,000 |

  Perks: monthly free-shipping codes, cashback codes worth 50–200 Coins, shop codes up to 30%, premium customer service.
  Article [80413](https://help.shopee.co.th/portal/4/article/80413).
- **Confidence**: verified (official Help Center). **Status**: continuing.

## 3.5 ShopeePay (wallet) and SPayLater (BNPL, Monee Capital)
- **ShopeePay Payment Channel Promotion**: an extra discount is applied automatically to eligible users who pay with the
  ShopeePay Wallet or ShopeePay bank debit. It stacks with other codes, is first come first served, and isn't refunded on
  returns. No amounts are published. Article [183609](https://help.shopee.co.th/portal/4/article/183609).
- **ShopeePay offline deals**: ShopeeFood → “ดีลใช้หน้าร้าน” (in-store deals), with vouchers and flash sales. Article [122842](https://help.shopee.co.th/portal/4/article/122842).
- **ShopeePay's own site** https://shopeepay.co.th/marketing (“กิจกรรมส่งเสริมการตลาด”, marketing activities) was **empty** when read.
- **SPayLater**:
  - Interest is **15%–25% a year**, reducing balance ([104115](https://help.shopee.co.th/portal/4/article/104115)).
  - The minimum item price is ฿1.
  - One-month BNPL purchases of more than ฿10 can be converted to installments before the first due date ([140257](https://help.shopee.co.th/portal/4/article/140257)).
  - It can **scan merchant PromptPay QRs** in shops, at 0% for 1 month and up to 12-month installments ([183049](https://help.shopee.co.th/portal/4/article/183049)).
  - The 10.10 banner advertises **0% for up to 12 months**. The terms and the minimum weren't read.
  - The lender is **Monee Capital** ([183503](https://help.shopee.co.th/portal/4/article/183503)).
- **Confidence**: verified for the mechanics; no October ShopeePay or SPayLater promotion text was found. **Status**: the Sep
  page had “ยังไม่พบโปร” (no promo found yet). October has only the 10.10 SPayLater-0% banner (illustrative).

## 3.6 Government 60/40 and ShopeeFood
- The first phase's approved food-delivery platforms were **Grab, LINE MAN, ShopeeFood, Robinhood** (thailand.go.th).
- For the **extra phase (1 Oct – 30 Nov)**, the official site says shops keep the delivery platform they were already
  linked to (one platform each). Delivery runs 06:00–21:00 and covers food only.
- The extra phase's platform list is only shown as an image or video, so ShopeeFood's participation is **unverified**. The
  Shopee marketplace itself isn't eligible, since use has to be face to face.
- **Confidence**: verified for the rules; ShopeeFood in the extra phase is unverified. **Status**: successor phase.

## 3.7 Shopee's bank-code hub (“โค้ดลดจากพาร์ทเนอร์”, `shopee.co.th/m/partnership-vouchers-rewards`) — **blocked**
The hub itself couldn't be read (captcha). Instead, here's what the **banks' own pages** already show for October. This is
not the hub's full list; the bank researchers should confirm. 🏠 marks household cards.

- **KTC** 🏠 (Takumi: KTC Digital VISA, JCB, Mastercard, UnionPay; Baiboon: KTC UnionPay). Source:
  https://www.ktc.co.th/promotion/online-shopping-services/online-shopping/shopee-codes. Codes are collected in the Shopee app.

  | Code | Discount | Minimum | Scope / limits |
  |---|---|---|---|
  | `KTC10` | ฿150 | ฿1,400 | monthly |
  | `KTC10H` | ฿2,500 | ฿25,000 | monthly |
  | `KTC10HH` (new tier) | ฿4,000 | ฿40,000 | monthly |
  | `KTCUPI10` | ฿200 | ฿1,200 | **KTC UnionPay only, 5 uses per Shopee account per month**, 1 Oct 69 – 31 Jan 70 |
  | `KTCUPI10H` | ฿1,000 | ฿8,000 | KTC UnionPay only, 1 use a month |
  | `KTCAP10` | ฿4,000 | ฿40,000 | Apple items from listed stores, 300 codes |
  | `KTCPREM10` | ฿650 | ฿2,500 | Shopee Premium-tagged items |
  | `KTCWED` | ฿180 | ฿1,600 | Wednesdays |
  | `KTCPAYDAY` | ฿300 | ฿2,000 | from the 25th to month-end |
  | Shopee Mall | ฿300 | ฿2,000 | all KTC cards |
  | Shopee Mall | ฿500 | ฿3,300 | KTC VISA only |
  | 0% installments up to 10 months | ฿1,400 | ฿11,500 | installment purchase |

  KTC's separate **shopee-1010** page still shows **last year's** 10 Oct 68 codes (`10SPKTC…`); no 2569 version yet.
- **Krungsri First Choice** 🏠 (Visa Platinum): `KFVOCT150` ฿150 off ฿1,200 (455 codes) and `KFVOCT350` ฿350 off ฿3,000
  (325 codes), 1–31 Oct 69. November and December codes are listed too. Page:
  https://www.firstchoice.co.th/promotion/shoponline-shopee (“สูงสุด 1,500 บาท”, up to ฿1,500, 1 Oct – 31 Dec 69).
- **AEON** 🏠 (World / Rabbit / UnionPay): `AEONOCT` ฿180 off ฿1,099; 2 uses per Shopee account a month; 1,200 rights a
  month. Thursday codes run 2 Jul – 29 Oct. Page: https://www.aeon.co.th/aeon/promotions/shopee-everyday-wow-july-2026
- **Mastercard network**:
  - Shopee Mall ฿225 off ฿1,500, for Platinum, Titanium, World, World Select and World Elite credit or debit cards, once a
    month, 15 Jul – 31 Dec 69. KTC page `shopee-mastercard`.
  - ฿80 off ฿800, once per card a month, 1 Nov 68 – 31 Dec 69. KTC page `shopee-x-mastercard`. The page title says “KTC
    MASTERCARD”, but its T&C describes a Mastercard-run offer for consumer Platinum, Titanium, World and World Elite cards
    issued in Thailand.
  - 🏠 AEON World Mastercard, KTC Mastercard and Krungsri Lady / NOW qualify if their tier fits.
- **ttb** (so smart 🏠): the `shopee-alwayson-jul26` page body loads by script and wasn't read. `shopee-alwayson-oct26`
  doesn't exist. Code for the October successor to TTBSEP: **unverified**.
- **Krungsri Card** (`krungsricard.com/th/promotion/shopee-payday`): the page now returns “ไม่พบหน้า” (not found). October
  codes are **unverified** here.
- **Not checked by me**: UOB, KBank, SCB/CardX, GSB, BBL, Lotus's, Central The 1. Left to the bank researchers.
- **Confidence**: verified (the banks' official pages) for the rows shown. The hub listing itself is unverified.

## 3.8 Cashback portals
- **ShopBack → Shopee: 0.1%**, capped at ฿5 per item for “other items”; some shops pay more. Tracked in 2 days, confirmed in
  20. It doesn't track purchases through Live or Video, ShopeeFood, vouchers, bills or top-ups. https://www.shopback.co.th/shopee.
  **Confidence**: third-party only (ShopBack). **Status**: continuing.
- **ShopBack → GO Wholesale: 1%** (see §2.1). **ShopBack → Makro PRO: not listed**; `/makropro` redirects to the all-stores page.

---

# 4. Not found / unconfirmed

- **Makro**:
  - No **10.10**, **Payday** or **member-day** campaign and no October **bank-partner page** on Makro PRO or makro.co.th.
    I probed the obvious flexi handles and checked news-detail IDs up to 1034; the last news item is #1007 (flood relief).
  - No Makro PRO **app coupon codes** for October are visible without logging in; the Loyalty Reward Centre is app-only.
  - **Referral** T&C (caps, the friend's minimum order) sit behind a login.
  - No successor to TrueMoney's **Makro_THT** double points.
  - Makro acceptance of **UnionPay QR** and **SPayLater PromptPay-QR scans** is unconfirmed.
  - No **LINE Pay / Rabbit LINE Pay**, **ShopeePay** or **Alipay+** promotion at Makro.
  - Whether CP Axtra's **60/40 booths** return for the extra phase is unconfirmed.
- **GO Wholesale**:
  - The **October The 1 PAYDAY** round isn't posted.
  - No GO-app-only offer is found.
  - T1 MAGICAL DAY's CRC Exclusive Pack contents (which shops' coupons) aren't listed on GO's page.
  - The KTC Visa 750 end date is inconsistent: 31 Oct in the list title, 31 Dec in the Sep T&C.
- **Shopee**:
  - The **full 10.10 T&C** is unread: voucher caps and minimums, whether BOGO and free shipping are limited to Mall or
    ร้านโค้ดคุ้ม Xtra shops, and the 10.10 SPayLater 0% terms.
  - The **bank-code hub** is unread; so are **October Payday** dates and codes, any **ShopeePay** top-up or cashback
    promotion, and **Shopee's own Facebook/LINE posts**.
  - **ShopeeFood** participation in the extra 60/40 phase is unverified.
  - Third-party deal sites (iPrice, Picodi) still showed September content at 03:30 on 1 Oct. Re-check them later on 1–7 Oct
    for 10.10 codes.
