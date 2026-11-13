---
tags: [promotion, lotuss]
---

# Lotus's SMP1 "ช้อปคุ้มตัวแม่" (Sep–Dec 2026), SMT2 "รูดก่อน ได้ก่อน" (Oct 2026) and SMT3 (11–30 Nov 2026)

Lotus's credit card cashback on everyday shopping categories, pooled per calendar month on Takumi's Lotus's Beyond account, supplements included. Takumi registered both before his 1 Oct 2026 AIS bill payment, and the UCHOOSE app shows that payment counting for both (user, 2026-10-05). Tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] from October 2026. The user calls the pair "SMT1 / SMT2", but the bank's code for the first is **SMP1**.

> **Structured source of truth**: `scripts/python/lib/bureau/lotus_shopping.py` (`SMP1Promotion`, `SMT2Promotion`, `SMT3Promotion`).

## Categories (both)

The page names examples; the bank decides by the card network's MCC, so an unnamed store in a category counts too.

- **Department stores**: Central, Paragon, Robinson, The Mall, ICONSIAM, King Power.
- **Fashion**: H&M, AIIZ, ZARA, Chanel, Louis Vuitton, UNIQLO, Decathlon, Anello.
- **Cosmetics**: BEAUTRIUM, Bath & Body, Cute Press, EVEANDBOY, Oriental Princess, Sephora.
- **Mobile and IT**: Jaymart, Banana, Big Camera, Com7, I-Studio, IT City, JIB, Advice, Telewiz.
- **Phone and internet bills** paid at the operator's own counter, website or app: AIS Shop, My AIS, TRUE & dtac Shop, True iservice; True Money Wallet only for the monthly bill. `AMP*AIS SERVICESPaymen BANGKOK TH` counts (confirmed in the app, 2026-10-05).
- **Books, stationery, office and household lifestyle**: SE-ED, Naiin, Asia Books, Nanmeebooks, Kinokuniya, B2S, OfficeMate, Daiso, MR.DIY, MINISO, Moshi Moshi.

**Excluded**: anything sold by Lotus's and every supermarket, hypermarket and convenience store; Power Buy and Power Mall; Lazada, Shopee, ShopeePay, Konvy, TikTok, True Select, Top Value, easyBills, AirPay, Alibaba, AliExpress, All Online; Boots, Watsons and direct sales; gold, jewellery and watches; spend abroad and foreign-registered online stores; utility auto-debits; installments; fees and interest.

## SMP1 — the monthly ladder

- **Only the single highest tier pays** ("สงวนสิทธิ์การให้เครดิตเงินคืนระดับสูงสุดเพียงระดับเดียวเท่านั้น"):
  - ฿70 per whole ฿3,500, at most ฿350;
  - or ฿450 per whole ฿25,000, at most ฿1,800;
  - or ฿2,600 from ฿150,000.

  So ฿24,999 earns ฿350 and ฿25,000 earns ฿450.
- **Caps**: ฿2,600 a month. For the campaign the conditions say ฿10,400 per primary account; one banner line says ฿14,000.
- **Registration** once, counting from the registration day: UCHOOSE → `SMP1`, or SMS `SMP1 <16-digit card no.>` to 081-250-7777.

## SMT2 — ฿200 at ฿2,000 in October

- ฿2,000 or more in the categories during **1–31 Oct 2026** → **฿200 once** per primary account.
- **First 500 accounts** to register *and* reach ฿2,000; register **before** spending. Check the rights left in UCHOOSE before spending.

## SMT3 — ฿200 at ฿2,000, 11–30 Nov ("รูดก่อน ได้ก่อน รับเครดิตเงินคืน คุ้มแบบ Double")

SMT2 again for 11.11, posted on the same page on 11 Nov 2026. Read 2026-11-13. The ฿2,000 threshold and the ฿200 appear only in the banner image (`…-Smallshopping-Detailpro-3-11-11.webp`); the text gives the ฿200 cap and the rights.

- ฿2,000 or more in SMP1's categories during **11–30 Nov 2026** → **฿200 once** per primary account. Supplements of every type count.
- **First 500 accounts** to register and reach ฿2,000. Register **before** spending, in **UCHOOSE only** (search `SMT3`).
- Takumi's `AMP*AIS SERVICESPaymen BANGKOK TH` ฿2,000 on 13 Nov reaches it on its own (user: eligible, 2026-11-13).

### Changes from SMT2 (and SMP1)

- **Period**: 11–30 Nov, 20 days from 11.11 (SMT2: the whole of October). The 1 Nov AIS bill falls before it and counts for SMP1 only.
- **Registration**: UCHOOSE only (SMT2: UCHOOSE or SMS to 081-250-7777).
- **Where the terms are**: the threshold and payout are only in the banner (SMT2's page stated them in text).
- **Unchanged**: ฿200 once at ฿2,000, the first 500, register before spending, SMP1's categories and exclusions, credited within 30 days after the month ends (by 30 Dec 2026), stacks with SMP1 under the same joint terms.

## All three

- **Stacking**: the joint terms bar spend counted in another Lotus's promotion (e.g. [[lotuss-lbs3|LBS3]]), but SMP1 and SMT2/SMT3 share those terms and stack. The app showed the October AIS payment in both SMP1 and SMT2.
- **Crediting**: within 30 days after each month-end, on the primary account's statement.
- **`% cb` is left unset**, as on every Lotus's row. The money goes in the Bureau and Takumi's tracker.
- **Coins vs cashback**: phone bills earn no Lotus's coins (MCC 4814, [[../cards/lotuss-beyond#Coin exclusions|card terms]]) but count here.

## Bureau rows

| Row | Created | State |
|---|---|---|
| `2026M10 — SMP1 cb 2%` | 2026-10-05 | ฿2,000 linked; ฿0 until October reaches ฿3,500 |
| `2026M10 — SMT2 cb ฿200` | 2026-10-05 | ฿200 to Takumi; credited 7 Nov as `CB - SMT2_(OCT'26)` −฿200, tracker `SMT2 ฿200 1—31 Oct` settled |
| `2026M11 — SMP1 cb 2%` | 2026-10-25 | ฿4,000 linked (AIS 1 Nov + 13 Nov) → ฿70 to Takumi so far |
| `2026M11 — SMT3 cb ฿200` | 2026-11-13 | 11–30 Nov; AIS ฿2,000 of 13 Nov linked → ฿200 to Takumi (tracker `SMT3 ฿200 11—30 Nov`) |

Source, read 2026-10-05 (SMP1, SMT2) and 2026-11-13 (SMT3): <https://www.lotussmoney.com/cashback-nationwide>.
