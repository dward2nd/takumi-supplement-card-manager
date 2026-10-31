---
tags: [catalogue-research, 2026-11]
researched: 2026-11-01
---

> **Research snapshot**: offers that name no merchant (all-spend cashback cards, monthly spend thresholds, network-wide and welcome offers, every issuer), each household card's own earning at the six merchants, and the fuel question (a ฿500 fill at Shell and PTT) — November 2026 research. Read on **2026-11-01** from the official pages, for the November 2026 [[../../databases/promotion-catalogues|Promotion Catalogues]] pages (Makro, GO Wholesale, Shopee, The 1, Shell, PTT). Hub: [[../index|catalogue research]] · lineage: [[../campaigns|campaigns]] · methods: [[../research-methods|research methods]].
> The raw dumps it mentions stayed in the session's scratchpad and weren't kept; every figure keeps its source URL. Nobody's points balance is recorded here (private).

# Offers that name no merchant, card earning and fuel — November 2026 (พ.ย. 69)

Continues [[../2026-10/all-spend|October's all-spend report]] (partial) and [[../2026-10/all-spend-jampha|the Jampha card-by-MCC table]].

**Confidence labels**: **V** verified on the official page today · **R** my reading of official terms · **T** third-party only · **U** unverified. **repo** = the repo's card YAML, promotion note or Bureau class (built from the bank's page earlier); **household** = the ledger or a reconciled statement shows it.

## 1. Headline changes vs October

- **Makro stops earning points on most of the household's cards this month.** Three issuer notices, all read today:
  - **Krungsri Card** (VISA, JCB, Lady, NOW): no Krungsri Point "ทุกการใช้จ่ายที่แม็คโคร ทุกช่องทางการจำหน่ายและการใช้จ่ายภายใต้ MCC 5199 … โดยมีผลตั้งแต่วันที่ 1 พฤศจิกายน 2569" (item 2.3 (7) of the points terms, [krungsri-point](https://www.krungsricard.com/th/krungsri-point)) · **V**
  - **First Choice** (Visa Platinum, XU): the same from **1 Nov 2026**, "การใช้จ่ายทุกช่องทางที่ร้านค้าแม็คโคร ทุกสาขาและออนไลน์ และการใช้จ่ายภายใต้ … MCC 5199" ([notice PDF](https://www.firstchoice.co.th/getattachment/80828729-0528-4628-aed9-e196573ec562/exemption-of-accumulated-points-mcc-5199.pdf), linked from [First Choice Rewards](https://www.firstchoice.co.th/firstchoice-rewards)) · **V**
  - **Central The 1** (every Central The 1 card, REDZ included): no The 1 points "ที่ร้านค้าแม็คโครทุกสาขาและทุกช่องทาง รวมถึงช่องทางออนไลน์ และการใช้จ่ายภายใต้ … MCC 5199" from **1 Nov 2026** (notice dated 1 Oct 2026, image `T1-Remove-point-Makro-A4-1024px-1.webp` in the [news page](https://www.centralthe1card.com/th/news-updates)'s `point-makro` modal) · **V**
  - **ttb** (every ttb card): from **3 Nov 2026** Makro spend earns no points and no ttb so smart 1% (27 Oct statement notice, already in [[../../promotions/ttb-2026]]) · repo
  - Already in force: **KTC VISA** no points or cashback at Makro and Makro PRO since 1 Sep 2026 ([notice](https://www.ktc.co.th/upload/announcement-document/Makro-CPAXT-KTCVisa-Notice-changes-Points-and-Cashback-Earning-t.pdf)); KTC VISA also earns nothing at the B2B MCCs incl. **5199** and **5172** since 1 May 2026 ([notice](https://www.ktc.co.th/upload/announcement-document/KTC2569-Notice-Changes-KTC-Point-Cashback-Earning-th.pdf)); UOB cards ×0 at Makro stores (UOB Makro ÷4); AEON and Lotus's withhold only on MCC 5199 (`WWW.MAKRO.PRO`) · **V** / repo
  - **Coming 1 Dec 2026, KTC**: on every KTC card, points (and KTC Cash Back cards' cashback) count only the first **฿20,000 per MCC per card per month** at MCC 5310, 5333, 5411 and 5499 ([notice dated 1 Oct 2026](https://www.ktc.co.th/upload/announcement-document/TH_%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%9A%E0%B8%A3%E0%B8%B4%E0%B8%A9%E0%B8%B1%E0%B8%97_KTC_%E0%B8%A2%E0%B8%81%E0%B9%80%E0%B8%A7%E0%B9%89%E0%B8%99%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%83%E0%B8%AB%E0%B9%89%E0%B8%84%E0%B8%B0%E0%B9%81%E0%B8%99%E0%B8%99_Final.pdf)); KTC UnionPay also loses points at merchants registered in New Zealand · **V**
- **What this does to the Makro plan**: points are now a rounding error at Makro on the Krungsri-group cards. Cash campaigns are separate from points and aren't touched by these notices: NW4 still counts `HTTPS://WWW.MAKRO.PRO/` (5411) inside its ฿30,000 supermarket allowance, but NW4's own exclusion line now reads "หมวดการใช้จ่ายใน MCC code 5199 **อาทิ Makro และ Makro PRO**" (Makro and Makro PRO named as examples of 5199) · **V** (text) · **R** (whether Krungsri now treats every Makro slip as 5199 is unclear; the vault reads `HTTPS://WWW.MAKRO.PRO/` as a 5411 supermarket slip that counts, [[../../promotions/first-choice-2026h2]])
- **Krungsri's points terms count fuel, not exclude it.** Item 2.3 (6) limits points on Thai fuel (MCC 5541/5542/5983 and 5172) to the first **฿50,000 per primary account per month** (from 1 Aug 2026), and item 2.1 excludes only **Bangchak**. So Krungsri VISA, JCB and Lady earn 1 point per ฿25 at **Shell and PTT**; only Bangchak (and BSRC, Bangchak's ex-Esso stations) earns nothing (NOW earns at Bangchak too). First Choice has the same ฿50,000 fuel cap and no Bangchak exclusion ([notice](https://www.firstchoice.co.th/getattachment/0dede3d7-9b4d-4e74-b24e-bc9dfc56d290/exemption-of-accumulated-points-7-11-tmn-gas.pdf)) · **V**. **This contradicts the vault's Krungsri JCB rule** ("petrol earns no points", `KrungsriJCB` in `lib/earning`), which was inferred from Bangchak/BSRC rows: Baiboon's `SHELL 0732F CO RUNGROJ NONGKHAI TH` ฿1,600 (18 Oct) on Krungsri JCB was set ×0 by that rule. Check it against the statement billed 5 Nov before changing the rule.
- **First Choice NW4** re-read: unchanged (1 Oct – 31 Dec; ฿50 at ฿5,000–9,999, 2% per whole ฿10,000, ≤ ฿2,000 a month, ≤ ฿6,000 campaign; fuel and supermarkets each count to ฿30,000 a month per primary account). New on the page: **+฿1,800** for taking a cash advance in the same month (interest-bearing; not a plan), and **BLUE PLUS `BPCB`** +฿3,000 a month for BLUE PLUS members only · **V**
- **Fuel successors**: Krungsri's PTT2 (ended 31 Oct) → **Krungsri Pay Save 2** `SAVE` (PTT 5% only on slips ≥ ฿1,000); KTC's PTT rounds renewed 1 Nov – 28 Feb (3% and the JCB ฿45 e-coupon need ≥ ฿1,000 / ≥ ฿900 a slip; the `PTP` points burn has no minimum); **Central The 1 Shell `SE11`** is this month's code (≥ ฿100 → ฿100). See §4.

### 1.1 By page (what this report adds to each)

- **Makro / Makro PRO**: base points are gone at Makro on First Choice, Krungsri Card, Central The 1 (1 Nov), ttb (3 Nov), KBank (current terms) and KTC VISA (1 Sep); only cash campaigns and the UOB Makro / UOB World / AEON World / Lotus's 5411 earning remain (§3). Krungsri NOW's 5% online is cashback, so it still pays on Makro PRO (reading). NW4 at Makro stores now hinges on the store's MCC (§7). UOB One's 1% excludes Makro stores; `TMN MAKRO` still earns it.
- **GO Wholesale**: every all-spend card counts it (NW4 inside the ฿30k supermarket cap, UOB One 1%, ttb so smart 1%); KBank caps supermarket points at 800 a cycle; KTC UnionPay earns 0 (5411); KTC caps 5411 at ฿20k a month per card from 1 Dec.
- **Shopee**: NW4 ✗ (marketplaces → ON4); UOB World ×5, UOB One 1%, ttb 1%, Krungsri NOW 5%, ONQ3 (to 30 Nov), Bangkok Bank UnionPay 2% all count.
- **The 1 / Central**: Central The 1 REDZ earns no points at Makro from 1 Nov; NW4 counts department stores and Tops (Tops inside the ฿30k cap); UOB Premier ×4 at department stores.
- **Shell** (new): Central The 1 `SE11` ฿100 on the first ≥ ฿100 fill of the month (register today, first 1,500); UnionPay QR 6% works at Shell pumps (household); First Choice ≈ 2.4% via NW4. UOB and ttb pay nothing (UOB `SPW109` needs a whole ฿800).
- **PTT** (new): nothing pays a ฿500 slip in cash except NW4 (≈ 2.4% with points); KTC `PTP` burns points at 15%; Krungsri Pay Save 5% and KTC 3% / JCB ฿45 need ฿900–1,000 a slip; the market's best is the KBank BLUE (PTT co-brand) card's points-to-20%.

## 2. Offers that name no merchant, live in November

Rates are at the margin of a month already past the first step. ✓ counts · ✗ doesn't · ? unclear · 🏠 a household card. Point values as in [[../2026-10/all-spend-jampha|October]]: Krungsri ฿0.08 (1,000 points → ฿80 bill credit, [krungsri-point](https://www.krungsricard.com/th/krungsri-point) §8.3) · First Choice ≈ ฿0.09 (330 → ฿30 at Café Amazon; 1,000 → ฿100 donation) · K Point ฿0.10 · KTC ฿0.10 · UOB ≈ ฿0.104 · The 1 ฿0.125 · Lotus's coin ฿1 (Lotus's coupon) · AEON Happy Point unpublished · GSB 1,200 → ฿100.

| # | Offer · issuer | 🏠 | Makro store | Makro PRO | GO Wholesale | Shopee | Central / Tops | **Fuel (Shell, PTT)** | Caps · minimum · registration | Period | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | **First Choice NW4** ("คืนคุ้มทุกการใช้จ่าย") | 🏠 all three, pooled; auto-enrolled | ? — the exclusion line names "MCC 5199 **อาทิ Makro และ Makro PRO**" | 5411 `HTTPS://WWW.MAKRO.PRO/` ✓ (vault reading) · 5199 ✗ | ✓ (supermarket ฿30k cap) | ✗ (→ ON4) | ✓ dept stores; Tops in the ฿30k cap | **✓ to ฿30,000 a month** per primary account | ฿50 at ฿5,000–9,999; ฿200 per whole ฿10,000; ≤ ฿2,000 a month, ≤ ฿6,000 campaign; e-wallet top-ups, FX, insurance, utilities, funds out; SMS `NW4` → 081-256-3333 | 1 Oct – 31 Dec | **V** ([page](https://www.firstchoice.co.th/promotion/firstchoice-cashback)) |
| A2 | **First Choice RSF2** ("จ่ายได้ทุกที่ VISA") — **cash-card loan line only** (First Choice cash card, Central The 1 First Choice, HomePro First Choice) | — (the household's First Choice is the Visa Platinum credit card) | ✓ by Visa QR | ✓ | ✓ | ✓ (named) | ✓ | **✓** (only utilities 4900 / 9402 excluded) | **3%** on ≥ ฿2,000 a month; ≤ ฿300 a month, ≤ ฿900 campaign per account; full-amount only; **loan line: interest runs** (the page's own warning); SMS `RSF2` → 081-256-3333 | 1 Oct – 31 Dec | **V** ([page](https://www.firstchoice.co.th/promotion/pay-with-visa-cashback)) |
| A3 | **Bangkok Bank UnionPay Platinum 2%** | — | ✗ (Makro's store QR is Visa/MC; physical UnionPay acceptance unconfirmed) | ✓ (Makro PRO takes UnionPay online) | ? | ✓ | ? | **✓** — no fuel, supermarket or e-wallet exclusion except Alipay / WeChat Pay | **2%** once the month (principal + supplements) reaches ฿2,000, anywhere except China; ≤ ฿1,000 a month (at ฿50,000), ≤ ฿12,000 per programme; no registration; credited within 60 days of the statement; Be Smart installments, funds 6211, insurance, cash, fees, tax 7276/9311, fines out | 1 Jul 2026 – 30 Jun 2027 | **V** ([page](https://www.bangkokbank.com/th-TH/Personal/Cards/Credit-Cards/Bangkok-Bank-UnionPay-Credit-Card), headless) |
| A4 | **UOB One 1%** (card benefit) | 🏠 all three | ✗ "ยอดใช้จ่ายในห้างแม็คโคร" · via TrueMoney ✓ 1% | ✓ 1% | ✓ | ✓ (e-wallet top-ups out) | ✓ | **✗** "ยอดใช้จ่ายจากสถานีบริการน้ำมัน" | ฿2,000 a cycle per account | 2026 | **V** ([page](https://www.uob.co.th/personal/credit-cards/cash-back/one-cash-back-credit-card.page), headless) |
| A5 | **UOB World ×5** (card benefit) | 🏠 Takumi + Baiboon | ✗ ×0 | ×2 ≈ 0.8% (×5 only if flagged e-commerce) | ×2 | ×5 ≈ 2.1% | ×2 | **✗** ×0 | ×5 on online / e-wallet / dining / travel / FX to ≈ ฿20,000 a cycle (account) | standing | repo ([[../../promotions/uob-world-points]]) |
| A6 | **ttb so smart 1%** | 🏠 Takumi + Baiboon | **✗ from 3 Nov** (statement notice; Makro PRO unstated) | ? from 3 Nov | ✓ | ✓ | ✓ | **✗** | ฿2,000 a cycle per card account; paid into ttb no fixed | standing | repo ([[../../promotions/ttb-2026]]); the [card page](https://www.ttbbank.com/th/personal/credit-cards/card-type/ttb-so-smart) (read by the KBank/ttb researcher today) doesn't mention the Makro change |
| A7 | **Krungsri ONQ3** (online + wallets ladder) | 🏠 VISA, JCB, Lady (registered) | ✗ | ✓ online | online only | ✓ | online only | ✗ (in store); a pump paid by scanning PromptPay in TrueMoney with Krungsri VISA would count as a TrueMoney card payment (reading) | ฿40 / ฿170 / ฿350 at ฿3k / 15k / 30k a month per primary account | 7 Aug – **30 Nov** | repo ([[../../promotions/krungsri-card-2026]]) |
| A8 | **Krungsri NOW 5% online** | 🏠 Takumi (Baiboon uses it) | ✗ (QR excluded) | ✓ 5% (cashback, not points — the Makro **points** exclusion doesn't touch it, reading) | online only | ✓ | online only | ✗ | ฿25 per whole ฿500 a slip; ≤ ฿300 a month; no points on those rows | 2026 | repo |
| A9 | **KBank LINE Points on-top** | 🏠 Takumi's KBank LINE Points | ? (K Point list excludes Makro; the LINE Points card's own Makro rule not found) | ? | spend counts for the on-top, but **supermarket, fuel and insurance earn no normal 1%** | ✓ 1% | ✓ 1% (Tops: on-top only) | **0 normal points**; counts toward the on-top steps | +50 LINE Points at ฿5,000–14,999 a month, +200 at ≥ ฿15,000 (≤ 800 a person); +800 at ฿80,000 cumulative; register once in K PLUS | 1 Sep – 31 Dec | **V** ([page](https://www.kasikornbank.com/th/promotion/creditcard/pages/linepoints-promotion.aspx), KBank researcher's dump today) |
| A10 | **KBank PLUSTINUM monthly e-coupon** | 🏠 Takumi's PLUSTINUM | ✓ spend counts (no K Point there) | ✓ | ✓ | ✓ | ✓ | ✓ | ≥ ฿10,000 a month → one e-coupon (BBQ Plaza / Starbucks / SF), all of a person's KBank cards pooled; Season 3 (≥ ฿30,000 → Starbucks ฿400) **ended 31 Oct, no Season 4 found** | 1 Jul – 31 Dec | **V** (page dated 1 Jul – 31 Dec in today's dump) · Oct terms not re-read |
| A11 | **UnionPay QR "Get 6% off"** (network) | 🏠 KTC UnionPay (…1346, …2310; Nuta's supplement unregistered) | ✗ (store QR is Visa/MC) | ✗ | ? | ✗ | ? | **Shell ✓** (household rows) · PTT ? | ≤ ฿60 a slip, 1 slip a card a day, ≤ ฿300 a card a month; only through KTC Mobile / ICBC / BOC apps; **November offer `260723112621` live: pool 99.87% left of 10,000 at ≈ 02:00 today** (API `flushProcess`) | 1–30 Nov | **V** (API) · household |
| A12 | Bangkok Bank Titanium (0.5% → 2% by cycle spend) | — | — | — | supermarkets count to ฿20,000 a cycle | ✓ | ✓ | fuel counts only to **฿15,000 a cycle** | ≤ ฿2,000 a card a cycle; cashback instead of points | standing | **V** (1 Oct, not re-read) |
| A13 | ttb Disney 5× · ttb reserve / so fast 1 pt/฿10 | — | — | — | — | — | — | not in the 5× categories | as October | standing | **V** (1 Oct, not re-read) |
| A14 | KTC Cash Back cards (≤ 0.8%) | — | ✗ (KTC VISA: no cashback at Makro since 1 Sep) | ✗ | ✓ (from 1 Dec ≤ ฿20,000 per MCC a cycle) | ✓ | ✓ | ✓ (fuel to ฿30,000 a month) | — | standing | **V** (notices) |
| A15 | Lotus's "ช้อปครบรับคุ้ม" (invited) | 🏠 if invited | — | — | — | — | — | — | ฿10 per slip ≥ ฿100 at any shop, +฿100 at 10 slips, ≤ ฿200 within 30 days of registering; invitation only | 1 Jul 2026 – 30 Jun 2027 | **V** (`earning-shopping-retention-y26`, Krungsri researcher's dump) |

**Not all-spend, but checked because the name suggests it**: Lotus's `SMP1` (ช้อปคุ้มตัวแม่) is department stores, fashion, cosmetics, IT and phone bills, not all spend; Lotus's `CCB7` and NW4's +฿1,800 pay for **cash advances** (fees and interest, not a plan); GSB has no all-spend credit-card offer (its Online Festival is a named-partner ladder, 1 Oct – 31 Dec, ≤ ฿1,500 a month); KBank's campaign list (231 items, today) has no all-spend campaign for ordinary cards.

## 3. Each household card × each merchant / channel

November 2026. "Pts" = the card's base points (value in brackets). ✗ = earns nothing there. Campaigns the household is registered for are added in *italics* where they pay at that channel (detail in the merchant reports and [[../campaigns]]). Shell and PTT share one column: no card in the household treats them differently except through per-slip campaigns (§4).

| Card · who | Makro store | Makro PRO `HTTPS://WWW.MAKRO.PRO/` (5411) | Makro PRO `WWW.MAKRO.PRO` (5199) | GO Wholesale (`CFW-…`) | Shopee | Central dept store / Tops | Shell / PTT | Source · conf. |
|---|---|---|---|---|---|---|---|---|
| **First Choice** (Visa) · all three, pooled | ✗ pts from 1 Nov · *NW4 ?* | ✗ pts · *NW4 ✓ in the ฿30k supermarket cap* | ✗ pts · NW4 ✗ | 1 pt/฿25 (≈ 0.36%) · *NW4 ✓* | 1/฿25 · *ON4* | 1/฿25 · *NW4 ✓* | 1/฿25 (fuel ≤ ฿50k a month) · *NW4 ✓ to ฿30k* | **V** (notices, NW4) |
| **Krungsri VISA** · Takumi, Baiboon | ✗ pts from 1 Nov | ✗ | ✗ | 1/฿25 (0.32%); *2x-platinum ×2 is Big C / Lotus's / Tops / Gourmet only* | 1/฿25 · *ONQ3* | 1/฿25 | **1/฿25 at Shell / PTT** (≤ ฿50k a month); Bangchak ✗ pts (*Bangchak700 + BXP cash*) | **V** ([krungsri-point](https://www.krungsricard.com/th/krungsri-point)) |
| **Krungsri JCB** · Takumi, Baiboon | ✗ from 1 Nov (and JCB isn't taken by Makro's store QR) | ✗ | ✗ | 1/฿25 | 1/฿25 · *ONQ3* | 1/฿25 | **1/฿25 at Shell / PTT per the terms** — the vault's `KrungsriJCB` rule zeroes all petrol; only Bangchak is excluded on the page (§1) | **V** (terms) · conflicts with repo |
| **Krungsri Lady** · Takumi | ✗ from 1 Nov | ✗ | ✗ | 1/฿25 | 1/฿25 · *ONQ3* | 1/฿25 (✗ on slips that earn Fashionista) | 1/฿25 (Shell / PTT); Bangchak ✗ | **V** |
| **Krungsri NOW** · Takumi (Baiboon uses it) | ✗ | *5% (฿25/฿500, ฿300 a month), no pts* | *5%* (online) | in store 1/฿25 | *5%* | Central App / central.co.th *5%*; stores 1/฿25 | 1/฿25 incl. Bangchak | **V** · repo |
| **Central The 1 REDZ** · Takumi, Baiboon | ✗ The 1 pts from 1 Nov | ✗ | ✗ | The 1 pts (≈ 0.5%, Oct reading) | The 1 pts | The 1 pts (×3 at Central, Oct reading) | *Shell `SE11` ฿100 once a month*; base pts at fuel not re-checked | **V** (Makro notice, `shell-2026`) · Oct reports |
| **Lotus's Beyond** · Takumi (Baiboon `[บัตรหลัก]`) | 0.25 coin/฿50 (0.5%) if the store posts 5411; ✗ if 5199 | 0.5% | ✗ (5199 since 20 Feb 2026) | 0.5% | 0.5% (top-ups ✗) | 0.5% | **0.5% in November; ✗ from 1 Dec** (MCC 5541/5542 notice, 25 Oct); Bangchak ✗ coins but the card's Bangchak 3% (≤ ฿700 a slip, 3 a cycle, ฿63) | **V** ([fuel notice](https://www.lotussmoney.com/announcement-corporate/lotus-money-coin-fuel-station-exclusion), [5199 notice](https://www.lotussmoney.com/announcement-corporate/coin-exclusion-2026), [Bangchak](https://www.lotussmoney.com/announcement-corporate/bangchak-2026)) |
| **KBank PLUSTINUM / JCB / Shopee** · Takumi (Baiboon on PLUSTINUM, JCB) | **✗ K Point** ("ร้าน Makro และ Makro PRO ทุกช่องทาง") · *MKR* | ✗ · *MKR* | ✗ | 1/฿25 (0.4%), **≤ 800 pts a cycle** at supermarkets | 1/฿25; KBank Shopee ×5 / ×10 | 1/฿25 (Tops in the 800 cap) | 1/฿25, **≤ 800 pts a cycle** at fuel | **V** ([K Point terms](https://www.kasikornbank.com/th/promotion/credit-card/reward-points/pages/condition.aspx), KBank researcher's dump) |
| **KBank LINE Points** · Takumi | ? | ? | ? | **0** normal points (supermarket) | 1% | 1% (Tops 0) | **0** normal points (fuel) | **V** (A9) |
| **KTC Digital VISA** · Takumi | ✗ (since 1 Sep; KTC cards can't be swiped at Makro stores anyway) | ✗ | ✗ | 1/฿25 (0.4%); from 1 Dec ≤ ฿20k per MCC a month | 0.4% | 0.4% | 0.4% (≤ ฿30k a month) · *PTT `PTP` burn 15%* | **V** (notices) · repo |
| **KTC Mastercard** · Takumi | ✗ (KTC FOREVER: Makro, Mastercard/Visa) | ✗ (reading) | ✗ | 0.4% | 0.4% | 0.4% | 0.4% · PTT 3% only ≥ ฿1,000 | repo ([[../../promotions/ktc-forever]]) |
| **KTC JCB** · Takumi | ✗ (no JCB at the store QR) | 0.4% (reading: the Makro rule names Visa / Mastercard) | ? | 0.4% | 0.4% | 0.4% | 0.4% · PTT ฿45 e-coupon only ≥ ฿900 | repo · **R** |
| **KTC UnionPay** · Takumi, Baiboon (Nuta supplement) | ✗ | **0** (5411) | ? | **0** (5411) | 0.4% | Tops 0 (5411); dept store 0.4% | **0.4%** (petrol earns) + ***UnionPay QR 6% at Shell*** | repo · household |
| **UOB One** · all three | ✗ | 1% | 1% (household) | 1% | 1% | 1% | **✗** | **V** |
| **UOB World** · Takumi, Baiboon | ✗ | ×2 ≈ 0.8% (×5 if e-commerce) | ×2 | ×2 | ×5 ≈ 2.1% | ×2 | **✗** (but `SPW109` 2% per whole ฿800 at Shell / Caltex) | repo · **V** (SPW109) |
| **UOB Premier** · Takumi (Baiboon's to Jan 2026) | ✗ | ×2 | ×2 | ×2 | ×2 | ×4 at dept stores (5311) | **✗** (`SPW109` 3% per ฿800 at Shell) | repo |
| **UOB Makro** · Takumi (Baiboon uses it) | ÷4 (≈ 0.1%) · *UMK26-1* | 1/฿25 · *UMK26-2 (app)* | 1/฿25 | 1/฿25 | 1/฿25 | 1/฿25 | **✗** | repo |
| **AEON World Mastercard** · Takumi (Baiboon `[บัตรหลัก]`) | 1 pt/฿30 (value unpublished) | 1/฿30 · *AEON World 5%, NTW1* | **✗** (5199) | 1/฿30 · *NTW1* | 1/฿30 | 1/฿30 · *5% at Tops* | 1/฿30 (fuel isn't on AEON's no-points list) | **V** ([AEON MCC list](https://www.aeon.co.th/aeon/news-events/notification-aeon-credit-cards-2025/)) · repo |
| AEON Rabbit · Takumi | no points | — | — | — | — | — | no points | repo |
| AEON Next Gen · Takumi (unused) | ✗ | 5% online (≤ ฿50 a txn; needs ≥ ฿500 Scan To Pay a cycle) | 5% | — | 5% | — | — | repo |
| AEON UnionPay · Nuta (Takumi's) | no points; 3% only in CNY/HKD/MOP/TWD | — | — | — | — | — | no points | repo |
| **CardX JCB** · Nuta | 0% cashback in Thailand; POINTX rate not re-checked · *HY1* | *HY1* | ? | *HY1* | — | — | not checked | repo |
| **ttb so smart** · Takumi, Baiboon | **✗ from 3 Nov** | ? from 3 Nov | ? | 1% · *BGO* | 1% | 1% | **✗** (`CTG`/`BCG` Caltex / Bangchak only) | repo |
| SPayLater · Grab PayLater · UOB Cash Plus | — | — | — | — | SPayLater: Shopee's own | — | none | repo |

**Reading the table for Makro**: from November, at Makro the only cards still earning *points* are UOB Makro (÷4 in store, ×1 online), UOB World / Premier (Makro PRO only), AEON World (5411 only), Lotus's Beyond (5411 only) and KTC JCB / UnionPay at Makro PRO (reading). Cash campaigns (NW4, MKR, UMK26, HY1, BGO's GO leg, AEON World 5%) are unaffected by the points notices.

## 4. Fuel: a ฿500 fill at Shell and at PTT

### 4.1 What the household pays with today (ledgers, read 2026-11-01)

- Baiboon: `SHELL …` slips on First Choice, UOB World / Premier (×0), Krungsri JCB and **KTC UnionPay**; `PTTST.…` on First Choice and UOB Premier / One (×0).
- **Shell takes UnionPay QR**: Baiboon's KTC UnionPay rows `SHELL 1270F CO THONGPA LAMPHUN TH` ฿470 (8 May 2026) and `SHELL 0732F CO RUNGROJ SENONGKHAI TH` ฿629.80 (3 Oct 2026) are ฿500 and ฿670 less 6% — UnionPay's QR offer, paid at the pump · household. No KTC UnionPay row at a PTT station exists, so PTT's UnionPay QR acceptance is **unknown**.
- Nuta: `PTTST.C BANGSAEN` / `PTTST.D DEEJAI SERVICE` / `PTTST.D TIDA MAHANAKOR` ฿500 almost weekly on **First Choice** (NW rows marked 1.5–2%), once on UOB One (×0, nothing) · household.

### 4.2 Per-slip and fuel campaigns a ฿500 slip can reach

| Campaign · issuer | 🏠 | Shell ฿500 | PTT ฿500 | Minimum · caps · registration | Period | Conf. |
|---|---|---|---|---|---|---|
| **Central The 1 Shell** `SE11` | 🏠 REDZ (Takumi + Baiboon; one primary account) | **฿100 (20%)** once a month | ✗ | slip ≥ ฿100; ฿100 per slip, **once per primary account per month**; **first 1,500 registrants each month**; register on or before the day: UCHOOSE (search `SHL`) or SMS `SE11 <16 digits>` → **081-278-2222**; registration opens the 1st of each month; code per month SE1…SE12 (Dec `SE12`); supplements' credit goes to the primary account | 1 Jan – 31 Dec 2026 | **V** ([`shell-2026`](https://www.centralthe1card.com/promotion?modalId=shell-2026), poster `T1-Shell-Y2026-A4-1024px.webp`) |
| **UnionPay QR "Get 6% off"** | 🏠 KTC UnionPay (…1346 Takumi, …2310 Baiboon; Nuta's not registered) | **฿30 (6%)** off the charge, if the station shows a UnionPay-capable QR | ? (no evidence) | ≤ ฿60 a slip, 1 slip a card a day, ≤ ฿300 a card a month; UnionPay's monthly pool; re-register each card for November's offer `260723112621` | Nov 2026 | household (Shell) · repo ([[../../promotions/unionpay-qr]]) |
| **KTC `PTP`** points → cashback at PTT | 🏠 KTC cards | ✗ | **100 KTC points → ฿15**, up to points = the slip (500 points → ฿75); par is ฿10 per 100, so the gain over cashing points at par is ≈ 5% of the slip | MCC 5541/5542; register once `PTP <16 digits>` → **061-384-5000**; no slip minimum found | 1 Nov 2026 – 28 Feb 2027 | **V** ([page](https://www.ktc.co.th/promotion/auto-gas-ev/gas-station-ev-charger/ptt-point-cashback)) |
| KTC PTT 3% (`PTT`) · KTC JCB ฿45 e-coupon | 🏠 KTC VISA / MC / UnionPay · KTC JCB | ✗ | ✗ for ฿500: **≥ ฿1,000** (3%, ≤ ฿30 a slip, ≤ ฿240 per card, first 35,000 cards) · **≥ ฿900** (฿45 e-coupon, 10,000 a month) | `PTT <16 digits>` → 061-384-5000 for both; no points on what earns the 3% | 1 Nov 2026 – 28 Feb 2027 | **V** ([3%](https://www.ktc.co.th/promotion/auto-gas-ev/gas-station-ev-charger/ptt-cashback), [JCB](https://www.ktc.co.th/promotion/auto-gas-ev/gas-station-ev-charger/ptt-jcb-cashback)) |
| Krungsri Pay Save 2 — เติมเซฟ PTT 5% (`SAVE`) | 🏠 Krungsri VISA / JCB / Lady / NOW | ✗ | ✗ for ฿500: **≥ ฿1,000** a slip; ≤ ฿50 a slip a day, ≤ ฿100 a month per primary account | SMS `SAVE <16 digits>` → 081-927-9999 or UCHOOSE, once | 1 Nov 2026 – 28 Feb 2027 | **V** ([page](https://www.krungsricard.com/th/promotion/krungsri-pay-save), read from the Krungsri researcher's dump today) |
| UOB `SPW109` Shell / Caltex | 🏠 UOB cards | ✗ for ฿500: per **whole ฿800** a slip (World 2%, Premier 3%, others 1%); + 800 points → ฿64 (8%) per ฿800 | ✗ | ≤ ฿3,200 a month per cardholder, ≤ ฿1,600 a slip; UOB One and UOB Makro excluded from the points part | 1 Feb 2026 – 31 Jan 2027 | **V** ([page](https://www.uob.co.th/personal/promotions/credit-cards/shell-caltex-cash-back-spw109-0326/shell-caltex-cash-back-spw109-0326.page)) |
| ttb `CTG` / `BCG` | 🏠 ttb so smart | ✗ (Caltex and Bangchak only) | ✗ | ฿18 per ฿600+ slip | to 31 Dec | repo |
| KTC Shell (2025's `SHP` / `SHC`) | — | ✗ (ended 31 Aug 2025; `ktc.co.th/shell` still points at it) | — | — | — | **V** |
| **KBank BLUE Credit Card** (the PTT Blue co-brand) | — (not held) | ✗ | **K Point = the slip → 20%**, no minimum; SMS `BCC <last 12 digits> <amount>` → **4545888** every time, on the day; also a standing 500 K Point → ฿100 fuel discount (฿0.20 a point) | full-amount slips at PTT Station, EV Station PluZ, Café Amazon, FIT Auto, Jiffy | 16 Apr – 31 Dec 2026 | **V** ([page](https://www.kasikornbank.com/th/promotion/creditcard/pages/blue-promotion.aspx), [new-card page](https://www.kasikornbank.com/th/personal/creditcard/pages/ccpromoacq.aspx), KBank researcher's dumps today) |
| Lotus's Beyond Bangchak 3% | 🏠 | ✗ (Bangchak only) | ✗ | ≤ ฿700 a slip, 3 slips a cycle, ≤ ฿63 a cycle | 1 Jan – 31 Dec 2026 | **V** |
| Bangkok Bank gas rebate (Bangchak, Caltex) | — | ✗ | ✗ | per whole ฿800 a slip, 2–10% by card | 1 Dec 2025 – 30 Nov 2026 | **T** (search summary of the [page](https://www.bangkokbank.com/th-TH/Personal/Cards/Credit-Cards/Promotions/Gas_Cash_Rebate_251201-261130)) |

### 4.3 The answer for a ฿500 fill

Values: the slip's cashback plus the card's points at the values in §2; "at the margin" = the slip's share of a ladder the month is already climbing.

| Rank | Shell, ฿500 (Baiboon, Chiang Mai / Lamphun) | All-in | Conditions |
|---|---|---|---|
| 1 | **Central The 1 REDZ, after registering `SE11`** | **฿100 (20%)** + base The 1 points | first qualifying slip of the month only, **one ฿100 per primary account** (Takumi's and Baiboon's REDZ share it); **first 1,500 registrants of the month** — register today (SMS `SE11 <16 digits>` → 081-278-2222, or UCHOOSE `SHL`), before the fill |
| 2 | **KTC UnionPay by UnionPay QR** (KTC Mobile scan) | **≈ ฿32 (≈ 6.4%)**: ฿30 off + ≈ 0.4% KTC points on ฿470 | the pump's QR must take UnionPay (two Shell stations did); 1 discounted slip a card a day, ≤ ฿300 a card a month = 10 such fills; re-register each card for November; pool 10,000 slips nationwide (99.87% left this morning) |
| 3 | **First Choice** | **≈ ฿12 (≈ 2.4%)**: NW4 2% at the margin (฿10) + 20 points (≈ ฿1.8) | NW4 counts fuel to ฿30,000 a month per primary account; the 2% is only "at the margin" — it pays ฿200 per whole ฿10,000 of the pooled month |
| 4 | Lotus's Beyond | ฿2.50 (0.5%) | **November only** (no coins at fuel from 1 Dec) |
| 5 | KTC Digital VISA / Mastercard / JCB · KBank PLUSTINUM / JCB | ฿2 (0.4%) | KBank: ≤ 800 fuel points a cycle |
| 6 | Krungsri VISA / JCB / Lady / NOW | ฿1.60 (0.32%) | points at Shell per the terms (fuel ≤ ฿50,000 a month); Krungsri JCB per the vault: nothing — see §1 |
| — | UOB One / World / Premier / Makro · ttb so smart · KBank LINE Points | **0** | UOB's `SPW109` needs a whole ฿800; ttb pays only Caltex / Bangchak |

| Rank | PTT, ฿500 (Nuta in Bang Saen; Baiboon in Chiang Mai) | All-in | Conditions |
|---|---|---|---|
| 1 | **KTC card with `PTP`** (any KTC card; Takumi's KTC cards, Baiboon's KTC UnionPay supplement) | up to **฿75** credit for 500 points; **≈ ฿25 (5%) more than the same points cashed at par** | register once `PTP <16 digits>` → 061-384-5000; needs the points; points at most = the slip |
| 2 | **First Choice** (Nuta's usual card) | **≈ ฿12 (≈ 2.4%)** | as above |
| 3 | KTC UnionPay by UnionPay QR | ≈ 6.4% **if** PTT's QR takes UnionPay | **unknown**: no household KTC UnionPay row at a PTT station; worth one try (Nuta's KTC UnionPay supplement would need registering for the offer) |
| 4 | Lotus's 0.5% (Nov) · KTC / KBank 0.4% · Krungsri 0.32% | ฿1.60–2.50 | — |
| — | UOB cards · ttb so smart · KBank LINE Points | 0 | — |
| — | Krungsri Pay Save `SAVE` 5% · KTC `PTT` 3% · KTC JCB ฿45 | **0 at ฿500** | they start at **฿1,000 / ฿1,000 / ฿900 a slip**: one ฿1,000 fill instead of two ฿500 fills would earn ฿50 (Krungsri, ≤ ฿100 a month) or ฿30 (KTC 3%, no points on it) or ฿45 (KTC JCB e-coupon, 10,000 a month) |

**Best in the market** (cards the household doesn't hold):
- **Shell**: nothing beats Central The 1's ฿100 on the first fill (the household has it). After that, UnionPay QR 6% (any KTC, ICBC or BOC UnionPay card in their apps), then the all-spend cards: First Choice **RSF2** 3% (cash-card loan line, interest runs), **Bangkok Bank UnionPay 2%** (fuel isn't excluded; the month needs ฿2,000), NW4 2%.
- **PTT**: the **KBank BLUE Credit Card** (PTT Blue co-brand) — K Point equal to the slip → 20% at PTT Station with no minimum (`BCC` SMS each time), i.e. points spent at ฿0.20 instead of ฿0.10, plus 500 K Point → ฿100 fuel. For cash rather than points: RSF2 3%, Bangkok Bank UnionPay 2%. Bangkok Bank Titanium counts fuel only to ฿15,000 a cycle at 0.5%.
- **Fuel caps inside all-spend offers**: NW4 ฿30,000 a month; Krungsri and First Choice points ฿50,000 a month; KTC points ฿30,000 a card a month; KBank 800 K Point a cycle (= ฿20,000); Bangkok Bank Titanium ฿15,000 a cycle; UOB One / World / Premier and ttb so smart exclude fuel entirely; Bangkok Bank UnionPay 2% and RSF2 3% don't cap it.

## 5. Welcome / new-card offers live in November

Who could still qualify: Takumi holds every issuer below except CardX, GSB, Bangkok Bank; Baiboon and Nuta mostly hold **supplements on Takumi's accounts** (First Choice, Krungsri, KTC UnionPay, UOB, ttb) and use some of his cards as `[บัตรหลัก]` rows (KBank, Lotus's, AEON World, UOB Makro). Whether a supplement counts as "already holding the issuer's card" is per issuer, noted where the terms say.

| Offer | Window | Spend needed | Reward | Who could qualify | Conf. |
|---|---|---|---|---|---|
| **KBank `NCCS260871`** | approved 1 Aug 2026 – 31 Jan 2027 | within 30 days of approval, with K-eMail Statement; ฿15k / 30k / 80k → 5,000 / 12,000 / 45,000 K Point (Oct tiers) | ≤ 50,000 K Point; points then buy gifts (AirPods 4, luggage, fuel cards) | "ลูกค้าใหม่ที่ไม่มีบัตรเครดิตกสิกรไทยมาก่อน หรือยกเลิกแล้วไม่น้อยกว่า 6 เดือน", principal **or first supplement**: **Nuta**; Baiboon only if she holds no KBank card in her own name (her KBank rows sit on Takumi's cards) | **V** (window, eligibility) · Oct (tiers) |
| **CardX first principal card** (CardX BEYOND / UP2ME / JCB PLATINUM), digital application, no sales code | approved by **31 Dec 2026** | ≥ ฿5,000 within 30 days (+ e-Statement, POINTX linked within 30 days) | Starbucks ฿500; +฿1,000 for setting up a recurring utility / streaming payment (≤ ฿1,500) | never held any CardX card, or cancelled ≥ 180 days: Takumi or Baiboon if they hold none; **Nuta probably not** (she holds a CardX JCB supplement — reading) | **V** (`dacq-q42026-1stcard1500stb`, KBank/CardX researcher's dump) |
| **Lotus's** new card (website / UCHOOSE) | applied **1 Sep – 30 Nov 2026**, approved by 15 Dec | ≥ ฿8,000 within 60 days + e-statement | Pochacco 20" case (฿5,590); first-year fee waived | new members (not cancelled within 6 months): **Nuta, Baiboon** (Baiboon's Lotus's rows are on Takumi's card) | **V** ([page](https://www.lotussmoney.com/credit-card/apply-online)) |
| **GSB Welcome No.5** | applied 1 Mar – **31 Dec 2026** with e-Statement | ≥ ฿5,555 within 55 days, principal card only | 5,555 GSB points (≈ ฿463 at 1,200 → ฿100; or the suitcase, Oct) | all three | **V** ([page](https://www.gsb.or.th/promotions/welcome-no5/)) |
| **Krungsri Card** website application | approved 1 Oct 2026 – 31 Jan 2027 | ≥ ฿5,000 + e-Statement or ≥ ฿7,000 within 30 days | VR ROAM bag ฿2,590 | Nuta on paper (Takumi, Baiboon hold Krungsri cards) | Oct (verified 3 Oct; not re-read) |
| **First Choice / XU / cash card** new round | **1 Nov 2026 – 28 Feb 2027** | not read | gifts "up to ฿4,590" | nobody: all three hold First Choice | **V** (tile on [apply-card](https://www.firstchoice.co.th/promotion/apply-card)) |
| UOB One + Cash Plus ฿2,000 · UOB new-to-card Rewards+ Starbucks ฿150 | 1 Oct – 31 Dec 2026 | ≥ ฿5,000 within 60 days | ฿2,000 / ฿150 | nobody (all hold UOB) | **V** (UOB One page; index) |
| Bangkok Bank AirAsia · M Visa | 1 Aug 2026 – 31 Jul 2027 · to 31 Dec 2026 | ฿100 per ฿5,000 in 60 days (≤ ฿200) · ≥ ฿10,000 in 60 days | cashback · suitcase ฿4,590 | all three (new to BBL) | Oct (1 Oct) |
| KTC JCB new principal | applied 1 Sep – 31 Dec 2026 | 3 transactions within 30 days | GrabFood ฿500 | Baiboon, Nuta (no principal KTC card) | Oct (3 Oct) |
| Central The 1 · ttb · AEON | — | — | **none found**: no new-card item in Central The 1's 184-item list today; ttb's Oct round ended 31 Oct and the new-card listing didn't load; AEON `NEW4` ended 30 Sep with no `NEW5` (not re-checked) | — | **V** (Central The 1) · **U** (ttb, AEON) |

## 6. What ends this month / what's announced for December

- **Ends 30 Nov**: Krungsri ONQ3; UnionPay's November QR offer (and its pool, likely sooner); Lotus's new-card applications; Bangkok Bank's Bangchak / Caltex rebate (**T**). **15 Nov**: BTS draw round 3 (First Choice, Krungsri VISA). Central The 1 `SE11` is November's code; register again on 1 Dec with `SE12`.
- **From 1 Dec 2026**: **Lotus's coins stop at fuel** (MCC 5541/5542, notice 25 Oct); **KTC caps supermarket/hypermarket points at ฿20,000 per MCC per card a month** (5310, 5333, 5411, 5499); KTC UnionPay earns nothing at New Zealand merchants · **V**.
- **Continuing into December**: NW4 (its last month), RSF2, UOB One / World, Bangkok Bank UnionPay 2% (to Jun 2027), KTC `PTP` / `PTT` / JCB PTT (to 28 Feb 2027), Krungsri Pay Save 2 (to 28 Feb 2027), KBank BLUE 20% (to 31 Dec), KBank LINE Points on-top and PLUSTINUM e-coupon (to 31 Dec), UOB `SPW109` (to 31 Jan 2027), UnionPay QR (December offer `260723112622` listed in October).

## 7. Not found / couldn't read

- **Whether a PTT station's QR takes UnionPay** (and so the 6%): no household row, no source. One try with KTC Mobile at `PTTST.C …` settles it.
- **Makro's in-store MCC** (5411 or 5199): it now decides NW4 at Makro stores — NW4's page names "Makro and Makro PRO" as examples of 5199 while the vault reads `HTTPS://WWW.MAKRO.PRO/` (5411) as a supermarket slip that counts. Also decides Lotus's coins and KTC UnionPay at the store.
- **Krungsri JCB at Shell / PTT**: the terms say points (only Bangchak excluded); the vault zeroes all petrol on this card. The 5 Nov statement (Baiboon's ฿1,600 Shell slip, 18 Oct) will show which.
- **Central The 1 card's own earning at fuel** (base The 1 points at Shell): the REDZ product page didn't render its earn table to curl; not re-checked.
- **KBank LINE Points card at Makro**: the K Point list excludes Makro "for every KBank card", but the LINE Points card earns LINE Points, not K Point; its own Makro rule wasn't found.
- **ttb new-card offers for November** and **ttb's own wording of the Makro change** (the card page doesn't mention it; the notice is only on the statement).
- **AEON `NEW5`**, **CardX JCB's POINTX rate**, **KBank BLUE card's base earn**: not checked.
- **Network offers (Visa, Mastercard, JCB)** weren't re-read: Visa's perks API answered 405 to GET and 400 ("Validation failure") to a POST without the page's body. UnionPay's list was read (§2 A11; its other Thai offers name merchants: EM District, The Mall, Lazada, hospitals, EV charging, Huawei Pay, Banzaan, "Top Global Online Merchants").
- **Bangkok Bank's fuel page** was read only through a search summary (**T**); its other Nov campaigns weren't listed (the listing API needs the in-page fetch).

## 8. Lineage rows

| Campaign | Pays | Oct 2026 | Nov 2026 | Pages | predecessor → successor |
|---|---|---|---|---|---|
| Krungsri / First Choice / Central The 1 points at Makro | base points | earned (5411) | **none at Makro (all channels) or MCC 5199, from 1 Nov** | M | — |
| ttb points / so smart 1% at Makro | 1% | earned | **none from 3 Nov** | M | — |
| KBank K Point at Makro / TrueMoney / 7-Eleven / 5199 | base points | (Oct reading: TrueMoney earned) | **none** (current terms) | M J | — |
| KTC points at supermarkets | base points | uncapped | uncapped; **≤ ฿20,000 per MCC per card a month from 1 Dec** | M G T | — |
| Lotus's coins at fuel | 0.25 per ฿50 | earned (Bangchak ✗) | earned; **none from 1 Dec** | F P | — |
| First Choice NW4 | pooled ladder; fuel to ฿30k | 1 Oct – 31 Dec | continues; +฿1,800 cash-advance bonus, BLUE PLUS `BPCB` | M G T F P | NW3 → NW4 |
| First Choice RSF2 | 3% any Visa, loan line | 1 Oct – 31 Dec | continues | M G S T F P | RSF1 → RSF2 |
| Bangkok Bank UnionPay 2% | all spend except China | to 30 Jun 2027 | continues; fuel not excluded | M S F P | — |
| UnionPay QR 6% | ≤ ฿60 a slip | `…620` (gone early Oct) | `260723112621`, 10,000 slips, 99.87% left on 1 Nov | M G J **F** (P?) | `…620` → `…621` → `…622` |
| Central The 1 Shell | ฿100 on ≥ ฿100, monthly code | `SE10` | **`SE11`** (`SE12` in Dec) | T **F** | SE10 → SE11 |
| Krungsri PTT2 → **Pay Save 2** (`SAVE`) | PTT 5% on ≥ ฿1,000 | PTT2 to 31 Oct | 1 Nov 2026 – 28 Feb 2027 | **P** | PTT2 → Pay Save 2 |
| KTC PTT `PTT` 3% · JCB ฿45 · `PTP` 15% | PTT | Jul – Oct round | 1 Nov 2026 – 28 Feb 2027 | **P** | previous KTC PTT round → this |
| KBank BLUE Credit Card 20% | K Point = slip at PTT | 16 Apr – 31 Dec | continues | **P** | — |
| UOB `SPW109` | Shell / Caltex per ฿800 | 1 Feb 2026 – 31 Jan 2027 | continues | **F** | — |
| KBank LINE Points on-top | +50 / +200 a month, +800 at ฿80k | 1 Sep – 31 Dec | continues; fuel and supermarket earn no normal 1% | — | — |
| PLUSTINUM Season 3 | ≥ ฿30k → Starbucks ฿400 | ended 31 Oct | **no Season 4 found** | — | Season 3 → (none) |
| CardX first-card Q4 | Starbucks ฿500 + ฿1,000 | to 31 Dec | continues | — | — |
| First Choice new-card | gifts ≤ ฿6,590 → ≤ ฿4,590 | 1 Jul – 31 Oct | new round 1 Nov 2026 – 28 Feb 2027 | — | — |

## 9. New site tricks

- **Points-programme exclusions are dated items in the terms**, not campaigns: Krungsri's `/th/krungsri-point` §2.3 lists each exclusion with its start date (Makro item (7) from 1 Nov 2026); First Choice's are PDFs linked from `/firstchoice-rewards` (`exemption-of-accumulated-points-mcc-5199.pdf`, `…-7-11-tmn-gas.pdf`). Re-read both at the start of every month.
- **Central The 1 notices** are modals on `/th/news-updates`: find `_openCustomModal('<id>')` near the tile, then the image inside `id="<id>"` (`T1-Remove-point-Makro-A4-1024px-1.webp`). The text is only in the image.
- **Lotus's notices** live under `/announcement-corporate/<slug>` (the sitemap lists them) and are images (`…annoucement…webp`, sic). `lotus-money-coin-fuel-station-exclusion` and `coin-exclusion-2026` were found this way.
- **KTC notices** are PDFs under `/upload/announcement-document/`; a web search for the Thai topic finds them faster than the site. KTC's fuel offers: `/promotion/auto-gas-ev/gas-station-ev-charger` lists every one with dates; terms are in the RSC chunks (`self.__next_f.push`).
- **UnionPay `flushProcess`** also returns `totalCount` (10,000 slips for November's QR offer), so the pool size is readable, not only the share left.
- **Visa Thailand's perks API** now refuses GET (405) and a bare POST (400 "Validation failure"); it needs the page's own request body (capture it over CDP).
- **Reuse the other researchers' dumps**: KBank's `kpoint-condition`, `blue-promotion`, `ccpromoacq` and campaign list `all.json`, the UOB `data-promotion.json`, Central The 1's `gcspromotion` list and Krungsri's listing JSON were all in the session scratchpad within minutes of starting.
