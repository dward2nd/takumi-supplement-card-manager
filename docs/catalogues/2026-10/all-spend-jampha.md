---
tags: [catalogue-research, 2026-10]
researched: 2026-10-06
---

> **Research snapshot**: offers that name no merchant, wallets, and each of Baiboon's cards' own earning, checked against a slip at **Jampha Savemart** (แจ่มฟ้า เซฟมาร์ท, statement name `JAMPHA SAVEMART CO.,LTD. CHIANGMAI TH`, a local independent supermarket in Chiang Mai, MCC presumably 5411), October 2026 and what is announced for November. Scope: every one of Baiboon's cards at MCC 5411 in store; all-spend and spend-threshold offers from every issuer (held or not); network offers; credit-card QR campaigns; wallet routes, above all **paying Jampha's PromptPay QR from TrueMoney with a linked Visa card**; welcome offers a month of ≈ ฿30,000 would complete. Read on **2026-10-06** from the official pages, UnionPay's offer API and the repo, for the October 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] page. Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]] · sibling: [[supermarket-jampha-banks|Jampha — bank and network campaigns]].
> The raw dumps it mentions (HTML, JSON) stayed in that session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# Offers that name no merchant, wallets and card earning, at Jampha Savemart — October 2026 (ต.ค. 69)

This continues [[all-spend]] (Makro), [[all-spend-hospital-spa]], [[all-spend-ticketing]], [[all-spend-apple]] and [[all-spend-uniqlo]]. Campaigns by category or by name (KTC `JFM`, AEON's Lamphun gift, KBank `HYP` / `BCB`, Krungsri HALO, the named-chain supermarket lists) are in the sibling [[supermarket-jampha-banks]]; they appear here only where they meet a card's own rate or a wallet route.

**Confidence labels**:
- **verified**: the official page (or UnionPay's offer API) was read on 2026-10-06.
- **verified (date)**: read on the official page by an earlier October report on that date, not re-read today.
- **repo-verified**: the repo's card YAML, promotion note or Bureau class, built from the bank's page.
- **household**: the household's own ledger or a reconciled statement shows it.
- **third-party only**: the only source is not the issuer or the merchant.
- **unverified**: an inference. A **reading** is an inference from the terms, labelled as such.

**Point values used** (as in [[all-spend-uniqlo]]): UOB Rewards ≈ ฿0.104 (UOB → The 1 transfer; no cash rate published) · Krungsri **฿0.08** (`ทุก 1,000 คะแนน แทนเงินฝาก 80 บาท` — points to bill credit, [krungsri-point](https://www.krungsricard.com/th/krungsri-point), verified) or ฿0.10 through the PT26 10% cash-out · First Choice ≈ ฿0.08–0.10 · K Point ฿0.10 (a points-equal-to-slip cash-out at a card terminal) · KTC ฿0.10 (1,000 = ฿100) · The 1 ฿0.125 · Lotus's coin ฿1 (a Lotus's coupon). AEON Happy Point has no published value.

---

## 0. How Jampha takes money — read this first

**The user, 2026-10-06, first-hand:**
- The only credit-card QR Jampha accepts is **UnionPay QR**. No issuer's in-app credit-card QR works there (Krungsri UCHOOSE, KTC Mobile Visa QR, UOB TMRW, K PLUS Scan to Pay, AEON Scan To Pay).
- It also takes **PromptPay** from bank accounts.
- A **physical credit card** (tap or insert) carries a **2% processing fee**.

**What that does to every number below:**
- **Physical card**: a ฿10,000 basket is charged ฿10,200, and ฿200 is lost before any reward. **Does the fee line earn?** The card sees one amount from `JAMPHA SAVEMART`, so points, cashback and spend campaigns count the ฿10,200 as an ordinary MCC 5411 charge (reading; the household hasn't had a surcharged Jampha slip it can check line by line). So a card's net is `rate × 1.02 − 2%`. A 1% card nets **−0.98%**; even a 2% card only breaks even (+0.04%).
- **UnionPay QR**: no fee. Only UnionPay cards can use it, and UnionPay's 6% offer runs only through KTC Mobile, ICBC Mobile Banking and BOC TH Mobile Banking ([terms](../../sources/unionpay-qr-terms-2026-09-30.txt), repo-verified).
- **PromptPay through a wallet**: no fee either, because Jampha sees a PromptPay payment. **TrueMoney lets a linked Visa credit card pay any merchant PromptPay QR** (§3), and that is the one way to use non-UnionPay cards at Jampha without the fee. Bank-account PromptPay earns no card rewards.

**Household history at Jampha** (read today from Baiboon's ledger, read-only) · household:
- 19 rows since Jun 2026. Almost all are on **KTC UnionPay** (…2310, and one `[บัตรหลัก]` row on Takumi's …1346), marked ×0 with the supermarket Note. Three slips on 5 Jul 2026 (฿5,637, ฿6,120, ฿6,120) went on **First Choice**.
- A ฿20.68 row (5 Jul) is ฿22 less 6%, so Jampha took UnionPay QR under the earlier UnionPay offer too.
- **1 Oct 2026**: ฿14,875 and ฿14,815, two slips on the same card (…2310) the same day. Only one slip a card a day gets the 6%, capped at ฿60, so ≈ ฿29,700 earned at most ฿60, and no points (KTC rule 16).

**October position** (`write-catalogue status`, read 6 Oct ≈ 18:40):
- UnionPay QR 6%: …2310 (Baiboon) **฿139.80 left** of ฿300 · …1346 (Takumi, also Baiboon's `[บัตรหลัก]`) **฿180 left**. UnionPay's October pool: **34.16% left at ≈ 19:40, 6 Oct** (`260723112620`, API). It read 80% on 2 Oct, so at this pace it runs out around **8–9 Oct** (reading; September's ran out on 12 Sep).
- First Choice NW4: pool ฿9,266.88 → ฿50 so far.
- UOB World ×5: ฿650 used of the ≈ ฿20,000 quota for the cycle 25 Sep – 21 Oct (Takumi and Baiboon share it).
- UOB One 1%: **฿1,728.94 left** of ฿2,000 for the cycle 25 Sep – 21 Oct.
- ttb so smart 1%: ฿1,966.38 left of ฿2,000 (cycle 27 Sep – 26 Oct).
- ONQ3: Krungsri VISA ฿183 pooled (under the ฿3,000 first band).
- NTW1 and AEON World 5%: ฿0, but Jampha doesn't count for either (§5).

---

## 1. The answer — routes for ≈ ฿30,000 a month, ranked by what's left after any fee

| # | Route | Card · channel | ฿10,000 slip, net | ≈ ฿30,000 / month, net | Caps · conditions | Confidence |
|---|---|---|---|---|---|---|
| 1 | **UnionPay QR "Get 6% off"** | **KTC UnionPay** · UnionPay QR in KTC Mobile | **+฿60** (0.6%); a ฿1,000 slip gets the full **6%** | ฿60 per card per visit day; this month **฿139.80 (…2310) + ฿180 (…1346)** left | 1 discounted slip per card per day, ≤ ฿60 a slip, ≤ ฿300 a card a month; card registered for the month; UnionPay's pool (34% left, likely gone in days). No points at 5411 | verified (API) · household |
| 2 | **TrueMoney → PromptPay, UOB World** (×5 e-wallet bonus) | UOB World **if it is the Visa version** (UOB issues World as both Mastercard and Visa) | **+฿208** (≈ 2.08%) | ≈ **+฿400** on the ≈ ฿19,350 of ×5 quota left this cycle; ×2 (≈ 0.83%) after | ×5 on the first ≈ ฿20,000 a cycle, shared with Takumi, every UOB World transaction using it; e-wallet top-ups excluded, payments are a ×5 category | verified (terms) · household (TMN rows reconcile at ×5) · reading (PromptPay = e-wallet payment) · **unverified (card network)** |
| 3 | **TrueMoney → PromptPay, First Choice** (NW4) | First Choice (Visa Platinum) · TrueMoney | **+฿150–200** (each whole ฿10,000 of the pooled month pays ฿200; from today's ฿9,266.88 pool a ฿10,000 slip lifts ฿50 to ฿200) | **+฿550**: today's ฿9,266.88 pool + ฿30,000 = ฿39,266 → ฿600 (from ฿50) | ฿200 per whole ฿10,000 of the account's pooled month, ≤ ฿2,000 a month, ≤ ฿6,000 for Oct–Dec; **outside the ฿30,000 supermarket cap** (it posts as TrueMoney, not 5411 — reading); no First Choice points on TrueMoney | verified (terms) · **household: the bank counted `TMN*PROMPTPAY30` rows for NW3** (UCHOOSE eligible list, Sep 2026) |
| 4 | **TrueMoney → PromptPay, KBank PLUSTINUM** | Takumi's PLUSTINUM (BIN 4417 70 = Visa) · TrueMoney | +฿40 in K Point; +฿100–260 e-coupon if the month crosses ฿10,000 | ≈ +฿120 K Point + ฿200 e-coupon + **Starbucks ฿400** (≥ ฿30,000 in Oct, Season 3, **register in K PLUS for October first**) ≈ **2.4%, mostly vouchers** | 1 e-coupon per person per month, **all of Takumi's KBank cards pooled**, so Jampha adds nothing if his own spend already crosses ฿10,000; Season 3 ends 31 Oct | verified (terms) · reading (no e-wallet exclusion in either) |
| 5 | **TrueMoney → PromptPay, Krungsri VISA** (ONQ3) | Krungsri VISA · TrueMoney | +฿40 (only if the month has nothing else) | **+฿350** at ฿30,000 (1.17%); ฿170 at ฿15,000 | per primary account per month: ฿40 / ฿170 / ฿350 at ฿3k / 15k / 30k; to 30 Nov; registered; no Krungsri points on TrueMoney; the page says "not combinable" | verified (terms) · reading (a PromptPay payment is "card payment through TrueMoney") |
| 6 | **TrueMoney → PromptPay, UOB One** | UOB One **if Visa** · TrueMoney | **+฿100** (1%) | +฿300 | ฿2,000 a cycle, shared by the account; ฿1,728.94 left | verified (`การใช้จ่ายผ่าน e-Wallet จะได้รับเครดิตเงินคืน 1%`) · **unverified (network)** |
| 7 | First Choice, **physical card** | First Choice · tap/insert | ≈ **0** (−฿15 to +฿40: NW4 ฿150–200 + 408 points − ฿200 fee) | ≈ +฿50–70, **only while the account's ฿30,000 supermarket allowance is unused** (Makro PRO 5411, Tops … share it) | as #3 | verified |
| 8 | Bangkok Bank UnionPay 2% (not held) | physical card (BBL's app QR-credit is Visa/Mastercard only) | **+฿4** | +฿12 | ≥ ฿2,000 a month, ≤ ฿1,000 a month | verified (1 Oct) · verified (BBL QR page) |
| — | **Every other physical card** | tap/insert | **−฿98 to −฿200** | −1% to −2% | see §2 | verified |

**What this means for Baiboon:**
- **Keep KTC UnionPay by QR for the first slip of the day on each registered card, and size that slip near ฿1,000** (6%, ฿60) while UnionPay's pool lasts. Splitting into 2–4 slips only helps if each extra slip goes on a *different* registered card. Nuta's KTC UnionPay isn't registered for the offer; registering it would add ฿300 a month of room.
- **Pay the rest of the basket by scanning Jampha's PromptPay QR in TrueMoney with a linked Visa** (§3). Fill UOB World's ×5 quota first (if her UOB World is a Visa), then First Choice for NW4, then Krungsri VISA's ONQ3 band or PLUSTINUM's coupons. **Untested at ฿10,000+ slips**: try a small payment first and check TrueMoney's limit.
- **Don't tap a card.** Only First Choice (NW4, inside the supermarket cap) and a 2% card break even after the fee; every other card loses 1–2%.

---

## 2. Each of Baiboon's cards at a ฿10,000 Jampha slip, by channel

"Physical" = the ฿10,000 basket charged as ฿10,200 (2% fee); the net is what the rewards are worth minus the ฿200 fee. "Credit-card QR in app": ✗ for every card (the user: Jampha takes no issuer QR). "Via wallet" = TrueMoney scanning Jampha's PromptPay QR with the card linked, **Visa cards only** (§3); ShopeePay and LINE Pay can't take a credit card for this (§4).

| Card · 🏠 who | Network | Physical (tap/insert), net | UnionPay QR | Via TrueMoney (PromptPay) | Own rate at 5411 · caps | Exclusions that bite | Source | Confidence |
|---|---|---|---|---|---|---|---|---|
| **KTC UnionPay** · Baiboon …2310, Takumi …1346 | UnionPay | **−฿200** (no points) | **+฿60** (6%, ≤ ฿60 a slip, 1 a card a day, ≤ ฿300 a month) | ✗ (not Visa) | **0 points**: rule (16) lists `5411 supermarkets and grocers` | KTC FOREVER rule (16) | [[../../promotions/ktc-forever]] · [[../../sources/ktc-forever-terms-2026-09-28.txt|terms]] · [UnionPay offer](https://marketing.unionpayintl.com/offer-promote/?language=en&insCode=299990156#/offer?offerNo=260723112620) | repo-verified · verified (API) · household (×0 rows) |
| **First Choice** · Baiboon …1064 (Takumi's account) | Visa | ≈ **0** (NW4 ฿150–200 inside the ฿30k supermarket cap + 408 pts − ฿200) | ✗ | **+฿150–200** (NW4 at the margin; 0 points) | 1 pt / ฿25 (≈ ฿0.08–0.10); NW4 ฿200 per whole ฿10,000 pooled, ≤ ฿2,000 a month | NW4: supermarket spend over ฿30,000 a month per primary account doesn't count; e-wallet **top-ups** excluded (payments counted under NW3); Krungsri-family points: TrueMoney earns none | [NW4](https://www.firstchoice.co.th/promotion/firstchoice-cashback) · [[../../promotions/first-choice-nw3]] | verified · household |
| **UOB World** · Baiboon …1009 (Takumi …9310) | **Mastercard or Visa** — UOB issues both ([card art](https://www.uob.co.th/personal/credit-cards/rewards/uob-world-credit-card.page)) | **−฿115** (×2: 816 pts ≈ ฿85) | ✗ | **+฿208** (×5: 2,000 pts) if Visa, within the ×5 quota; else ✗ | 5411: ×2 up to ฿100,000 a cycle (`ยอดการใช้จ่ายที่ไฮเปอร์มาร์เก็ต และซุปเปอร์มาร์เก็ต … 0-100,000 บาท จะได้รับ 2 คะแนน`); ×5 on online / **e-wallet** / dining / travel / FX up to ฿20,000 a cycle | Makro, fuel, e-wallet top-ups, MCC 4900; quota shared with Takumi | [UOB World](https://www.uob.co.th/personal/credit-cards/rewards/uob-world-credit-card.page) · [[../../promotions/uob-world-points]] | verified · household · unverified (network) |
| **UOB One** · Baiboon …2497 | **Mastercard or Visa** (both issued) | **−฿98** (1% = ฿102) | ✗ | **+฿100** (1% e-wallet) if Visa | 1%, ฿2,000 a cycle per account (฿1,728.94 left) | Makro, fuel, MCC 4900, **e-wallet top-ups** (payments earn 1%) | [UOB One](https://www.uob.co.th/personal/credit-cards/cash-back/one-cash-back-credit-card.page) · [[../../promotions/uob-one-2026]] | verified · unverified (network) |
| UOB Premier · Baiboon …6040 (active to Jan 2026 per the card YAML) | Mastercard ([banner](https://www.uob.co.th/personal/credit-cards/shopping/uob-premier-credit-card.page)) | **−฿115** (×2) | ✗ | ✗ (Mastercard) | ×2 domestic; ×4 only at MCC 5311/5309; `PRS` 5% only at named supermarkets (not registered) | Makro, fuel, top-ups | [UOB Premier](https://www.uob.co.th/personal/credit-cards/shopping/uob-premier-credit-card.page) | verified |
| UOB Makro · Baiboon (`[บัตรหลัก]`, Takumi …1649) | not stated on the page | **−฿158** (408 pts ≈ ฿42) | ✗ | +฿42 if Visa (TMN rows earn the 1 / ฿25 base) | supermarkets 1 pt / ฿25 up to ฿100,000 a cycle; the 16th-of-month ×2 (`MMID`) doesn't cover non-Makro 5411 | UMK26 mission 3 excludes MCC 5411 | [UOB Makro](https://www.uob.co.th/personal/credit-cards/rewards/uob-makro-rewards-credit-card.page) · [[../../cards/uob-makro]] · [[../../promotions/uob-makro-gold-mission]] | verified |
| ttb so smart · Baiboon …0864 | — | **−฿98** (1% = ฿102, paid to a ttb account) | ✗ | **0** (TrueMoney excluded) | 1%, ฿2,000 a cycle per card account | TrueMoney, 7-Eleven, fuel, transport, installments | [[../../promotions/ttb-2026]] (bank's list) | repo-verified |
| KBank PLUSTINUM · Takumi's card (Baiboon uses it) | Visa (BIN `4417 70`) | **−฿159** (408 K Point ≈ ฿41) + an e-coupon if the month crosses ฿10,000 → ≈ +฿41 | ✗ | **+฿41** + same coupons, no fee | 1 K Point / ฿25; **at 5411 at most 800 K Point a cycle** (= ฿20,000); ×3 bonus is restaurants / dept stores / fashion only | K Point: cash, utilities, tax, fees, funds, foreign-registered baht; no e-wallet item | [K Point terms](https://www.kasikornbank.com/th/promotion/credit-card/reward-points/pages/condition.aspx) · [e-coupon](https://www.kasikornbank.com/th/promotion/creditcard/pages/plustinum-event.aspx) · [Season 3](https://www.kasikornbank.com/th/promotion/creditcard/pages/plustinum-promotion.aspx) | verified · reading (TrueMoney earns) |
| KBank JCB · Baiboon (Takumi's …2511) | JCB | **−฿159** (408 K Point, 800 a cycle cap at 5411) | ✗ | ✗ (JCB) | 1 K Point / ฿25 | as above | [K Point terms](https://www.kasikornbank.com/th/promotion/credit-card/reward-points/pages/condition.aspx) | verified |
| Krungsri VISA · Baiboon …4493 | Visa | **−฿167** (408 pts × ฿0.08; −฿159 at ฿0.10) | ✗ | **0 points**; counts toward **ONQ3** (+฿40 / 170 / 350 a month) | 1 pt per whole ฿25 a slip; `2x-platinum` ×2 only at Big C / Lotus's / Tops / Gourmet | `ทุกการใช้จ่ายที่เกิดจากการผูกบัตรกับบัญชีทรูมันนี่ วอลเล็ท` earns no points from 1 Aug 2026 | [krungsri-point](https://www.krungsricard.com/th/krungsri-point) · [2x-platinum](https://www.krungsricard.com/th/promotion/2x-platinum) · [ONQ3](https://www.krungsricard.com/th/promotion/online-shopping-cashback) | verified |
| Krungsri JCB · Baiboon …0109 | JCB | **−฿167** | ✗ | ✗ | as Krungsri VISA | as above | same | verified |
| Krungsri Lady · Baiboon | Mastercard | **−฿167** | ✗ | ✗ | as above | as above | same | verified |
| Krungsri NOW · Baiboon (Takumi's …5655) | Mastercard | **−฿167** in store (5% is online only, QR excluded) | ✗ | ✗ | 1 pt / ฿25 a slip in store | NOW's 5%: `เฉพาะการซื้อสินค้า/บริการผ่านเว็บไซต์หรือแอปพลิเคชัน ไม่รวม … QR Code` | [NOW](https://www.krungsricard.com/th/product/creditcard/now) | verified |
| Central The 1 REDZ · Baiboon | Mastercard | **−฿149** (408 The 1 pts ≈ ฿51) | ✗ | ✗ (Mastercard; REDZ also excludes TrueMoney-linked spend from 1 Aug 2026) | 1 The 1 pt / ฿25 a slip (≈ 0.5%) | — | [[all-spend-uniqlo]] §2.8 · [[all-spend]] B12 | verified (1–5 Oct) |
| Lotus's Beyond · Baiboon (Takumi's account) | Mastercard | **−฿149** (51 coins) | ✗ | ✗ | 0.25 coin per whole ฿50 a line; no supermarket exclusion | SMP1 / SMT2 / LBS3 / invited segments exclude supermarkets; LAN is Lotus's only; QRT4 categories don't include supermarkets | [[../../cards/lotuss-beyond]] · [[../../promotions/lotuss-smp1]] | repo-verified |
| AEON World Mastercard · Baiboon (`[บัตรหลัก]`) | Mastercard | **−฿200** + 340 Happy Points (no published value) | ✗ | ✗ | 1 pt / ฿30; its 5% and NTW1 are named supermarket lists without Jampha | AEON's no-points MCC list doesn't include 5411 | [AEON World](https://www.aeon.co.th/aeon/cards/aeon-world-mastercard) · [[../../promotions/aeon-2026]] | verified |
| AEON Primo (digital) · Baiboon | not stated | −฿200 + 510 Happy Points, **if** it can be tapped at all (a digital card; AEON's Scan To Pay isn't accepted) | ✗ | not stated (AEON's app pays Visa/Mastercard Thai QR only — third-party) | 1 pt / ฿20 | — | [Primo digital](https://www.aeon.co.th/aeon/cards/aeon-primo-digital-card) | verified (rate) · unverified (channel) |
| AEON Next Gen (digital) · Baiboon | not stated | as Primo, **0 points** (`สงวนสิทธิ์ยกเว้นการให้คะแนนสะสม AEON Happy Reward`) | ✗ | not stated | 5% only online (≤ ฿50 a transaction; needs ≥ ฿500 of Scan To Pay in the cycle; QR / e-wallet / Scan To Pay spend itself excluded) | — | [Next Gen digital](https://www.aeon.co.th/aeon/cards/aeon-nextgen-digital-card) | verified |
| SPayLater · Baiboon | (Shopee BNPL) | — | ✗ | **0** through ShopeePay scanning a merchant PromptPay QR (0% for 1 month, up to 12 months); no rewards | — | personal PromptPay QRs refused | [Help Center 183049](https://help.shopee.co.th/portal/4/article/183049) | verified |
| *Not Baiboon's:* AEON UnionPay (Takumi, Nuta) | UnionPay | −฿200 (0 points; 3% only in CNY/HKD/MOP/TWD) | **no app route**: the 6% offer runs only in KTC / ICBC / BOC apps, and AEON's Scan To Pay is Visa/Mastercard (third-party) | ✗ | — | — | [[../../cards/_stubs]] · [[../../promotions/aeon-2026]] | repo-verified · third-party only |

Per-slip arithmetic used: `floor(10,200 / 25) = 408` blocks on a physical slip; `floor(10,000 / 25) = 400` through TrueMoney (no fee). UOB ×2 = 816 points, ×5 = 2,000.

---

## 3. The TrueMoney route — paying Jampha's PromptPay QR with a linked Visa

### 3.1 What TrueMoney says · verified

- **Card-funded PromptPay** ([page](https://www.truemoney.com/debit-credit-card/promptpay/), published 9 Sep 2026): `ผูกบัตรเครดิต / เดบิต VISA กับทรูมันนี่ ใช้จ่ายร้านค้าพร้อมเพย์ได้แล้ว!!!`; `ไม่มีขั้นต่ำ ไม่มีค่าธรรมเนียม` (no minimum, no fee); `ที่ร้านค้าพร้อมเพย์ (ร้านไม่รับบัตรก็จ่ายได้)` (at PromptPay shops, even ones that don't take cards); `คุ้มกว่าทั้งได้สะสมคะแนนบัตรเครดิต และได้ทรูมันนี่คอยน์` (you keep the card's points and get TrueMoney Coins). Steps: scan → choose `VISA บัตรเครดิต/เดบิต`. **Visa only**; no Mastercard, JCB or UnionPay.
- **Which QRs** ([PromptPay page](https://www.truemoney.com/promptpay/)): `สแกนจ่ายได้ทุก QR พร้อมเพย์`. Juristic-person shops (`ร้านค้านิติบุคคล … ชื่อบัญชีเป็น บริษัท บจ. บมจ.`) can be paid straight away; a shop whose account is a person's needs TrueMoney's advanced KYC (`บัญชีขั้นสูง`, at 7-Eleven or a TrueMoney kiosk). **Jampha is `JAMPHA SAVEMART CO.,LTD.`, a company**, so its QR should be the immediate kind (reading: what account its QR pays into is the store researchers' question).
- **TrueMoney Coins**: 1 coin per ฿20, only at Tag 30 / juristic shops, **at most 25 coins a month**: negligible.
- **Launch offer** (TrueMoney × Visa press release, 2 Sep 2026, [share2trade](https://www.share2trade.com/news/58882/)): ฿30 back on the first PromptPay scan paid with a Visa card (≥ ฿100), once per user, to **31 Dec 2569**; lucky draws to 30 Sep (ended). · third-party only (the campaign link `tmn.app.link/PP30VISAPR` opens only the app).
- **Limits** for a card-funded PromptPay payment aren't published (the [fee page](https://www.truemoney.com/rates/) has no line for it). The household's rows so far are ≤ ฿1,000 · **unverified for ฿10,000+ slips**.

### 3.2 How the slip looks to the bank · household

The household already pays this way: `TMN*PROMPTPAY30 BANGKOK TH` rows on **First Choice**, Baiboon's and Takumi's, from May 2026 (dozens of rows, ฿30–1,000 each). "30" is most likely the Thai QR **Tag 30** (merchant bill-payment QR), not a fee (reading). The amounts are whole baht, so no fee was added.
- **First Choice counted them**: the UCHOOSE app's NW3 eligible list for September included the household's `TMN*PROMPTPAY30` rows, and the Bureau matched that list to the satang ([[../../promotions/first-choice-nw3]]: "TrueMoney-routed card payments aren't top-ups to the bank"). NW4's exclusions read the same (`การเติมเงินเข้า E-Wallet`), so the route counts for NW4 (reading).
- **The charge loses MCC 5411**: it posts as TrueMoney. That is why it escapes NW4's ฿30,000 supermarket cap and KBank's 800-point supermarket cap, and also why it can't count for any supermarket-category campaign (KBank `HYP`, Krungsri HALO's supermarket leg, AEON's Lamphun gift, KTC `JFM`).

### 3.3 What each Visa card earns on it

| Card | Earns on `TMN*PROMPTPAY…` | Confidence |
|---|---|---|
| **UOB World (Visa version)** | ×5 (e-wallet is a bonus category) inside the ฿20,000 cycle quota, then ×2 | verified (terms) · household (`TMN …` rows on UOB World reconcile at ×5 against the statements) · reading (PromptPay rows are e-wallet payments) |
| **First Choice** | NW4 at the margin; **no points** (Krungsri family, TrueMoney) | verified · household |
| **KBank PLUSTINUM** | 1 K Point / ฿25 (no e-wallet exclusion in the K Point terms); counts for the monthly e-coupon and Season 3 (neither excludes e-wallets) | verified (terms) · reading |
| **Krungsri VISA** | **no points**; ONQ3 counts `แอปอีวอลเล็ต ได้แก่ TrueMoney, LINE Pay, ShopeePay` (food delivery excepted) | verified (terms) · reading (a PromptPay payment is a card payment through the TrueMoney app; the Bureau's `ONQ3Promotion` counts any `TMN*` row) |
| **UOB One (Visa version)** | 1% (`การใช้จ่ายผ่าน e-Wallet จะได้รับเครดิตเงินคืน 1%`; top-ups excluded) | verified (terms) · household (`TMN MAKRO` 1% reconciled) · reading (PromptPay) |
| UOB Makro (if Visa) | 1 pt / ฿25 | repo-verified · reading |
| ttb so smart | nothing (TrueMoney excluded from the 1%) | repo-verified |
| KTC Digital VISA (Takumi's, not Baiboon's) | unclear: the repo's `KTCCard` class zeroes every `TMN …` row, while KTC FOREVER's TrueMoney-linked rule names other KTC products (rule 3 covers only 7-Eleven through TrueMoney) | repo-verified · unverified |
| UOB SPW796 overlay (any UOB card) | **probably not**: TrueMoney counts only `ร้านค้าที่ร่วมรายการ` on truemoney.com/retail-store (7-Eleven, McDonald's …), and bill payments are excluded | verified ([terms JSON](https://www.uob.co.th/assets/web-resources/personal/credit-cards/promotions/shopping-lifestyle/shopping-online-spw796-1226.json)) · reading |

**Not combinable**: one payment carries one card, so the routes split the basket rather than stack. ONQ3's own page says `ไม่สามารถใช้ร่วมกับรายการส่งเสริมการขายอื่นๆ ได้`; the household has seen Krungsri pay overlapping campaigns anyway ([[../../promotions/krungsri-card-2026]], "Stacking").

---

## 4. Other wallet and QR routes

- **UnionPay QR** (KTC Mobile, ICBC Mobile Banking, BOC TH Mobile Banking): the only fee-free card route for UnionPay cards. Other UnionPay cards a household member could add: **ICBC (Thai) or BOC UnionPay** credit cards get the same 6% (one per card) · verified (terms); their own earning wasn't researched.
- **UnionPay's other Thai offers in October** (API, `merchant/getMerchantList`, 12 merchants): the only one that names no merchant besides the 6% QR is **"Mobile Payment Instant Discount 3% OFF"** (`260226111820`, NFC), whose pool reads **0%**, and a tap would carry Jampha's fee anyway. The rest are named merchants (The Mall, Lazada, hospitals, Grab, EV charging, ONESIAM Huawei Pay) or abroad · verified.
- **ShopeePay / SPayLater**: SPayLater can scan a **merchant** PromptPay QR (`ร้านค้าที่เป็นพร้อมเพย์ และเป็นชื่อร้านค้าชัดเจน`, not a personal one), 0% for 1 month, up to 12 months ([183049](https://help.shopee.co.th/portal/4/article/183049)). No reward; its fee schedule (linked from the article) wasn't read. ShopeePay balance topped up by card earns nothing on any card (top-ups excluded) · verified.
- **LINE Pay / Rabbit LINE Pay**: no way found to pay a PromptPay QR with a linked credit card. AEON Rabbit's 5% LINE Pay benefit (≤ ฿50 a transaction) would work only if Jampha takes LINE Pay itself · not found.
- **TrueMoney Pay Next** (BNPL): 3% back on payments ≥ ฿100 at participating shops, ฿100 a round ([[merchants-wallets]] §1.2), but Pay Next charges a fee per transaction on its credit line (฿90 for ฿6,100–10,000, [rates](https://www.truemoney.com/rates/)) · verified (fees).
- **Bank-account PromptPay**: no card rewards. No PromptPay-from-account cashback offer was found for October.
- **Issuer credit-card QR campaigns** (KTC VISA Scan to Pay ฿150 for 3 slips ≥ ฿1,000, Lotus's QRT4 UCHOOSE QR, Krungsri NOW's QR exclusion, AEON Next Gen's Scan To Pay qualifier, POINTX QR): **none works at Jampha**, which takes no issuer QR (user, 2026-10-06).

---

## 5. Offers that name no merchant — checked against Jampha

| Offer · issuer | 🏠 | Jampha by physical card (net of 2%) | Jampha by UnionPay QR | Jampha via TrueMoney (Visa) | Caps · period | Confidence |
|---|---|---|---|---|---|---|
| **First Choice NW4** (`คืนคุ้มทุกการใช้จ่าย`) | 🏠 all three, pooled, auto-enrolled | ✓ ≈ 0, supermarket spend counted to ฿30,000 a month per primary account (`ยอดการใช้จ่ายสะสมในหมวดซูเปอร์มาร์เก็ต เช่น บิ๊กซี, โลตัส … ที่เกิน 30,000 บาท`) | ✗ (Visa) | ✓ **+2%** at the margin, outside the supermarket cap (reading) | ฿50 at ฿5,000–9,999; ฿200 per whole ฿10,000; ≤ ฿2,000 a month, ≤ ฿6,000 1 Oct – 31 Dec | verified ([page](https://www.firstchoice.co.th/promotion/firstchoice-cashback)) · household (NW3) |
| **Krungsri ONQ3** (online + wallets) | 🏠 VISA, JCB, Lady (registered) | ✗ (in-store card spend isn't online) | ✗ | ✓ Krungsri VISA only (Visa): ฿350 at ฿30,000 (1.17%) | ฿40 / ฿170 / ฿350 per primary account a month; ≤ ฿1,400 for the campaign; 7 Aug – 30 Nov | verified ([page](https://www.krungsricard.com/th/promotion/online-shopping-cashback)) · reading |
| **UOB SPW796** (e-commerce / e-wallet, ฿100 per ฿5,000, ≤ ฿200 a month) | 🏠 registered | ✗ | ✗ | probably ✗ (TrueMoney only at its partner stores) | 1 Oct – 31 Dec | verified (terms) · reading |
| **UOB One 1%** · **UOB World ×5** (card benefits) | 🏠 | 1% / ×2 → −1% / −1.15% | ✗ | 1% / ×5 if the card is Visa | §2 | verified |
| **ttb so smart 1%** | 🏠 | −0.98% | ✗ | ✗ (TrueMoney excluded) | ฿2,000 a cycle | repo-verified |
| **KBank PLUSTINUM e-coupon** (≥ ฿10,000 a month → BBQ Plaza ฿100/200, Starbucks ฿200, SF ฿260) and **Season 3** (≥ ฿30,000 in Oct → Starbucks ฿400) | 🏠 Takumi's card | ≈ 0 at ฿10,000 / ฿30,000 (coupon value ≈ the fee) | ✗ | ✓ coupons free of fee (+2% at ฿10,000 / ฿30,000 in vouchers) | 1 coupon a person a month, all KBank cards pooled, principal and supplement separate; claim in K PLUS on the 15th; Season 3 needs **registration for October before spending**, ends 31 Oct | verified ([e-coupon](https://www.kasikornbank.com/th/promotion/creditcard/pages/plustinum-event.aspx), [Season 3](https://www.kasikornbank.com/th/promotion/creditcard/pages/plustinum-promotion.aspx)) |
| **Lotus's SMP1 / SMT2 / LBS3 / LAN / invited segments** | 🏠 Takumi's account (SMP1, SMT2, LAN registered) | ✗: SMP1 / SMT2 exclude `ทุกซูเปอร์มาร์เก็ต`; LBS3 excludes supermarkets (Makro excepted); LAN is Lotus's only; invited segments exclude supermarkets | ✗ | ✗ (Mastercard) | — | repo-verified ([[../../promotions/lotuss-smp1]], [[../../promotions/lotuss-lbs3]], [[../../promotions/lotuss-lan]]) |
| **AEON NTW1** (Everyday with AEON) · **AEON World 5%** | 🏠 AEON World | ✗: both are named lists (NTW1: `BigC, Tops, Tops Food Hall, Tops daily, Gourmet Market, Foodland, Go Wholesale และ Makro PRO`) | ✗ | ✗ | — | verified ([NTW1](https://www.aeon.co.th/aeon/promotions/happy-monthly-with-aeon-2026/), 5 Oct dump; [AEON World](https://www.aeon.co.th/aeon/cards/aeon-world-mastercard)) |
| **AEON 365 วัน** (≥ ฿3,000 full-pay in a month → ≈ ฿190 of food vouchers) | 🏠 AEON Next Gen, AEON UnionPay (principals only) | Next Gen is digital (no tap found); AEON UnionPay: ≈ +฿130 on a ฿3,000 month (vouchers − ฿60 fee) — Takumi's card | ✗ (no app for AEON UnionPay QR) | not stated | 1 Sep 69 – 28 Feb 70 | verified (2 Oct, [page](https://www.aeon.co.th/aeon/promotions/aeon-365-days-september-2026)) |
| **UOB Makro UMK26 mission 3** (฿300 at ≥ ฿10,000 outside Makro) | 🏠 registered | ✗ (excludes MCC 5411) | ✗ | ✗ (e-wallets excluded) | — | repo-verified ([[../../promotions/uob-makro-gold-mission]]) |
| **Krungsri `2x-platinum`** (×2 at supermarkets) | 🏠 VISA, JCB (Platinum) | ✗ (Big C, Lotus's, Tops, Gourmet only; ≤ 120 bonus pts a month) | ✗ | ✗ | 1 Jul – 31 Dec | verified ([page](https://www.krungsricard.com/th/promotion/2x-platinum)) |
| **UnionPay QR 6%** | 🏠 KTC UnionPay (Takumi, Baiboon; Nuta not registered) | — | ✓ ≤ ฿60 a slip, 1 a card a day, ≤ ฿300 a card a month; pool 34% left | — | Oct `260723112620`; **Nov `260723112621` opens 1 Nov** (API: "not started"); Dec, Jan listed | verified (API) |
| **Bangkok Bank UnionPay 2%** (≥ ฿2,000 a month, anywhere except China) | — | ✓ but ≈ 0 net (+0.04%) | ✗ for this card: BBL's QR payment with a credit card is Visa/Mastercard only ([BBL](https://www.bangkokbank.com/en/Personal/Digital-Banking/Bualuang-mBanking/How-to-Use/QR-Code-Payment-with-Credit-Card)); BBL's UnionPay QR-to-pay is from a savings account | ✗ | ≤ ฿1,000 a month; 1 Jul 69 – 30 Jun 70 | verified (1 Oct; BBL QR page today) |
| Bangkok Bank Titanium (0.5% to ฿25,000 a cycle; 5411 counts to ฿20,000) | — | −1.5% | ✗ | ✗ (Mastercard) | — | verified (1 Oct) |
| ttb Disney 5× at 5310 / 5411 (≈ 2% if a point is ฿0.10) | — | ≈ 0 | ✗ | — | ≤ 3,000 bonus pts a cycle; 3 slips ≥ ฿1,000 | verified (1 Oct) · value unpublished |
| KTC Cash Back cards (≤ 0.8%) · ICBC ANY 6% online | — | negative / ✗ (online) | ✗ | — | — | verified (1–3 Oct) |
| Visa / Mastercard / JCB network offers | 🏠 | nothing all-spend for October (Visa 57 perks, Priceless 72 offers: travel, dining, abroad; JCB's Japan draw gives rights only — [[supermarket-jampha-banks]] §3.3) | — | Visa × TrueMoney ฿30 first scan (above) | — | verified (3 Oct) · third-party (TrueMoney × Visa) |
| CardX invite-only thresholds (`CDM3`, `cc-jump-retail-high-cb-oct-2026`) | Nuta's CardX JCB, if invited | physical only (JCB) | ✗ | ✗ | Starbucks ฿200–600 at ฿10k / 30k; ฿500 at ฿50k | verified (5 Oct, index) · unverified (invitation) |
| GSB, Krungthai, CIMB, KKP, TISCO, LH Bank | — | no all-spend offer found | — | — | — | verified (2 Oct) |

---

## 6. Welcome offers a month of ≈ ฿30,000 at Jampha would complete

Eligibility as in [[apple-wallets-networks-welcome]] §4 (verified 3 Oct): Takumi and Baiboon already hold UOB, KBank, KTC, ttb, Krungsri Card, First Choice, Central The 1, Lotus's and AEON; Nuta holds supplements only. **At Jampha a new card pays 2% to complete its spend target unless it's UnionPay (QR) or a Visa (TrueMoney)**, and the welcome terms' e-wallet treatment wasn't read for any of them.

| Offer | Window | Spend needed | Reward | Fee to complete at Jampha by card | Who | Conf. |
|---|---|---|---|---|---|---|
| **KBank `NCCS260871`** | approved 1 Aug 69 – 31 Jan 70 | ≥ ฿15,000 / ≥ ฿30,000 within 30 days | 5,000 / 12,000 K Point (≈ ฿500 / ฿1,200 at ฿0.10) | ฿300 / ฿600 → **net ≈ +฿200 / +฿600** | Nuta | verified (3 Oct) |
| **ttb so smart** new card | approved by **31 Oct 69** | ≥ ฿15,000 within 30 days | ฿500 + the 1% | ฿300 → ≈ +฿350 | Nuta | verified (3 Oct) |
| **Central The 1 REDZ** | applications to **31 Oct 69** | ฿8,000–29,999 / ≥ ฿30,000 within 45 days | bag ฿2,590 / 24" case ฿6,990 | ฿160 / ฿600 | Nuta | verified (1 Oct, GO's copy) |
| **Krungsri Card** (website application) | approved 1 Oct 69 – 31 Jan 70 | ≥ ฿5,000 + e-Statement, or ≥ ฿7,000, within 30 days | VR ROAM bag ฿2,590 | ฿100–140 | Nuta | verified (3 Oct) |
| **Lotus's** new card | applied 1 Sep – 30 Nov 69 | ≥ ฿8,000 within 60 days + e-Statement | Pochacco 20" case ฿5,590 | ฿160 | Nuta | verified (3 Oct) |
| **GSB Welcome No.5** | applied with e-Statement 1 Mar – 31 Dec 69 | ≥ ฿5,555 within 55 days | case ฿5,290 (5,555 GSB points) | ≈ ฿111 | all three | verified (3 Oct) |
| **CardX** first principal (`C6902030`) | approved by 31 Dec 69 | ≥ ฿5,000 within 30 days | Starbucks ฿500 | ฿100 | Baiboon | verified (3 Oct) |
| Bangkok Bank M Visa / AirAsia | 1 Jul – 31 Dec 69 / 1 Aug 69 – 31 Jul 70 | ≥ ฿10,000 in 60 days / ฿100 per ฿5,000 | suitcase ฿4,590 / ≤ ฿200 | ฿200 / ≤ ฿200 (M Visa is a Visa → TrueMoney route possible) | all three | verified (1 Oct) |
| KTC JCB new principal | applied 1 Sep – 31 Dec 69 | 3 transactions within 30 days | GrabFood ฿500 | 2% of three small slips | Baiboon, Nuta | verified (3 Oct) |
| UOB One / World Q4 | applied 1 Oct – 31 Dec 69 | ≥ ฿5,000 within 60 days | ฿2,000 / ฿1,500 | — | nobody (all hold UOB) | verified (3 Oct) |

---

## 7. November

- **UnionPay QR 6%**: November's offer `260723112621` is listed (1–30 Nov, "not started" on the API); register each card again. December `…622` and January `…623` are listed too · verified.
- **NW4** runs to 31 Dec; **ONQ3** ends 30 Nov; **PLUSTINUM e-coupon** runs to 31 Dec, **Season 3 ends 31 Oct** (no Season 4 found); TrueMoney × Visa ฿30 first-scan offer to 31 Dec · verified.
- UOB World's next ×5 quota starts with the cycle from 22 Oct; UOB One's ฿2,000 resets the same day; ttb so smart's from 27 Oct · repo-verified (Bureau periods).

## 8. Not found / open

- **The household's UOB World and UOB One networks.** UOB issues both cards as World Mastercard and Visa Platinum (card art on both pages). The TrueMoney route needs the Visa one: **check the card faces**.
- **TrueMoney's limit for a card-funded PromptPay payment** (per payment, per day, per month) isn't published; the household's largest is ฿1,000. Try one ฿10,000+ payment before relying on it.
- **Whether UOB classes `TMN*PROMPTPAY…` as an e-wallet payment** (×5 / 1%) rather than a transfer: no UOB row of this kind yet. The first statement line will show it.
- **Whether Krungsri's ONQ3 counts a PromptPay payment through TrueMoney**: the terms name TrueMoney card payments without limiting them to TrueMoney's partner shops; no bank credit has confirmed it.
- **Whether Jampha's PromptPay QR is a company (Tag 30) QR**: TrueMoney pays company QRs at once; a personal one needs advanced KYC, and SPayLater refuses it.
- **Whether a card can pay Jampha's UnionPay QR outside KTC / ICBC / BOC apps** (BBL UnionPay, AEON UnionPay): no app route found.
- **AEON Primo and Next Gen** are digital cards; whether either can be tapped at Jampha (in a phone wallet) wasn't checked, and their networks aren't on the pages.
- **Whether the 2% surcharge itself is allowed** under Jampha's acquirer agreement wasn't researched; neither was whether the store applies it to UnionPay cards tapped physically (the household pays UnionPay by QR).
- **SPayLater's fee for in-store PromptPay payments**: linked from Help Center 183049, not read.

## 9. Site methods

- **truemoney.com reads through `r.jina.ai`**: `/promptpay/` (which QRs, juristic vs personal shops, coins) and `/debit-credit-card/promptpay/` (the Visa card route, "no minimum, no fee"); the fee table is `/rates/`. `/sitemap.xml` returns a 404 page that still lists the menu. TrueMoney's campaign deep links (`tmn.app.link/…`) open only the app; the press release (share2trade) carries the terms summary.
- **UnionPay's Thai offer list**: `merchant/getMerchantList?countryCode=764&pageIndex=1&pageSize=50&insCode=299990156&language=en` returns 12 merchants with each offer's `couponName` in `section[]`; `coupon/flushProcess?couponno=<n>&couponType=07&insCode=299990156&language=en` gives `percent` left for any offer number, not only the 6% QR one (`lib.bureau.unionpay_offer._get`).
- **UOB card networks** aren't in the page text; the card art (`/assets/web-resources/images/personal/cards/credit/<card>/uob-<card>-nov24-th-d.jpg`, curl works) shows which networks a card comes in.
- **KBank K Point conditions** (`/th/promotion/credit-card/reward-points/pages/condition.aspx`) render headless with the desktop agent; they carry the 800-point supermarket/fuel cap per cycle.
- **AEON digital cards** live at `/aeon/cards/aeon-nextgen-digital-card` and `/aeon/cards/aeon-primo-digital-card` (no trailing slash; the slash-less older slugs return the listing).
- **Krungsri points terms** (`/th/krungsri-point`, plain curl): the full no-points list, including `ทุกการใช้จ่ายที่เกิดจากการผูกบัตรกับบัญชีทรูมันนี่ วอลเล็ท` from 1 Aug 2026, and the standing 1,000 points = ฿80 bill credit.
- **The household ledger answers "does this channel work here?"** faster than any page: `fetch-transactions` with `name_contains` (`SAVEMART`, `PROMPTPAY`) showed Jampha's UnionPay QR and First Choice history and the TrueMoney PromptPay habit.
