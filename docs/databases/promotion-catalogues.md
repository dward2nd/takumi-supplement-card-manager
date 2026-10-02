---
tags: [database, household, promotion]
owner: household
role: promotion-catalogues
---

# Promotion Catalogues

A page per **merchant (or programme) per month** summarising every payment promotion worth knowing there, plus a spending plan for the household's cards. Written for Baiboon and the household to read, in Thai. Created by Takumi 2026-09-30. Unlike the [[promotion-bureau|Promotion Bureau]], nothing here is linked to transactions: it's reading material, not accounting.

- **Data source**: `3ebcb755-f0f1-80d5-a580-000bf9448d23` (database `3ebcb755-f0f1-80c4-80aa-f0b87391e7e0`), under Personal Monetary Policy. Shared with the scripts' integration.
- **View**: Gallery with page-cover preview, so every page has a **cover** (the merchant's logo on a white plate, the Thai month, a fan of issuer-coloured cards) and an **emoji icon** (user, 2026-09-30).

The research behind each page is archived in [[../catalogues/index|catalogue research]]. It holds the monthly reports, the campaign lineage ([[../catalogues/campaigns|campaigns]]) and how each site can be read ([[../catalogues/research-methods|research methods]]).

Written with [[../../.claude/skills/write-catalogue/SKILL|/write-catalogue]] (`scripts/python/write-catalogue/cli.py`, `lib/catalogue/`): it creates the page, sets the dates, icon and logo cover, and writes the body from Markdown; `{"status": "YYYY-MM"}` reports the month's Bureau usage for the plan.

## Schema

| Property | Type | Meaning |
|---|---|---|
| `Name` | title | `<Merchant> — <Mon YYYY>`, e.g. `Makro — Sep 2026` |
| `Start Date` / `End Date` | date | the month the page covers |

## Page body

The shape the user set with the Makro example (2026-09-30):

1. A callout: who it's for, the period, the "updated" date, what ends today.
2. **แผนการทำยอด** (spending plan): the household's cards ranked **strictly by value, most first**, with each line's rate shown. It notes the quotas already used this month (from the Promotion Bureau) and gives a worked example. Points redemptions follow in their own list, ordered by baht per point. **No one's points balance appears on a page** (private; user, 2026-10-01).
3. **รวมโปร** (catalogue): one section per issuer. Tier tables with the effective rate (`<= 1.5%`), caps, period, registration code, and `ref:` link to the bank's page. `*====== ซ้อนโปร ======*` marks a promotion that stacks on the one above.
4. Other cards the household doesn't hold, the merchant's own deals, and what wasn't found.

Thai narrative, card and code names verbatim. Say where a figure is third-party only.

## Pages

| Page | Icon | Written |
|---|---|---|
| `Makro — Sep 2026` | 🛒 | 2026-09-30 |
| `GO Wholesale — Sep 2026` | 🧺 | 2026-09-30 |
| `Shopee — Sep 2026` | 🛍️ | 2026-09-30 |
| `Lazada — Sep 2026` | 💗 | 2026-09-30 |
| `TikTok Shop — Sep 2026` | 🎵 | 2026-09-30 |
| `Central The 1 — Sep 2026` | 💳 | 2026-09-30 |
| `Makro — Oct 2026` | 🛒 | 2026-10-01 |
| `GO Wholesale — Oct 2026` | 🧺 | 2026-10-01 |
| `Shopee — Oct 2026` | 🛍️ | 2026-10-01 |
| `The 1 — Oct 2026` | 💳 | 2026-10-01 |
| `Sriphat Medical Center — Oct 2026` | 🏥 | 2026-10-02 |
| `Yunomori Onsen & Spa — Oct 2026` | ♨️ | 2026-10-02 |
| `Thaiticketmajor — Oct 2026` | 🎫 | 2026-10-03 |

From October the Central The 1 page is **`The 1 — <Mon YYYY>`**. It covers the The 1 membership (points, member-only deals, network coupons in the The 1 app) as well as the Central The 1 credit card, and says where the two differ (user, 2026-10-01: "they overlap mostly but can be different in some aspects").

## Readings worth keeping

- **Paying at a Makro store depends on the bank** (Oct 2026):
  - Krungsri Card and First Choice promotions count only when you scan to pay in UCHOOSE.
  - KBank's October round (MKR) counts a normal card swipe; September's needed K Scan to Pay.
  - CardX's HY1 has no scan rule.
  - KTC cards can't be used at Makro stores at all. KTC's own article says so; its points offer counts only through a KTC Mobile scan or TrueMoney.
  - AEON, GSB and Krungsri NOW's 5% count Makro PRO only.
- **Makro PRO posts under two strings, and the card doesn't choose.** `HTTPS://WWW.MAKRO.PRO/` is MCC 5411 and `WWW.MAKRO.PRO` is MCC 5199; the same First Choice card got both in Aug 2026.
  - First Choice NW4 excludes 5199.
  - AEON gives no points on 5199.
  - Krungsri NOW's 5% paid on both.
- **Some quotas are shared across pages.** Krungsri SUP1 (per card per month), CardX HY1, NW4's ฿30,000 supermarket allowance, AEON NTW1 and AEON World's 5% (Makro PRO and Tops) all count Makro and GO Wholesale (and Tops) together, so each page that uses them says so.
- **GO Wholesale posts as `CFW-<BRANCH> …`** (Central Food Wholesale), e.g. `CFW-CHIANGMAI 1 CHIANGMAI TH`.
- **Hospitals and spas are paid by category campaigns, not named deals** (Oct 2026). No bank names Sriphat for cashback (only KTC's 0.69% public-hospital installment), and only KTC and JCB name Yunomori. The money is in:
  - Lotus's LHB2 / LFS4 (public and private hospitals, spas);
  - Central The 1 HBF (hospital, beauty and spa, ≥ ฿15,000 a month);
  - First Choice NW4 (hospitals count unless they post as government MCC 9399/9405/7800);
  - the 1% cards and the UnionPay QR 6%.
- **Sriphat posts as a hospital, not as government**, although KTC lists it as a government hospital: its ฿800 (Sep 2026) and CMEx's ฿450 counted in NW3, which was reconciled to UCHOOSE's eligible list. Its MCC isn't published; 8062 is the household's reading.
- **Hospital earning traps**: every AEON card withholds points at MCC 8062 (from 11 Nov 2025); KTC UnionPay gets no points there either; Central The 1 REDZ and Lotus's earn nothing if a hospital posts as 9399, while Krungsri Card keeps hospitals even under government codes.
- **Hospital and spa quotas are shared between pages**: HBF and LHB2 / LFS4 pool hospital and spa spend on one account, and the UnionPay QR 6% (฿300 per card a month) is shared with every QR merchant.
- **Yunomori has no Chiang Mai branch** (Sukhumvit 26, Sathorn 10, Pattaya), so its page is for trips; it ends with a short list of Chiang Mai spa offers.
- **Thaiticketmajor charges 3% on every online method** (card, QR, TrueMoney, ShopeePay) plus ฿30 a ticket, none refundable (Oct 2026). A card only beats paying with no fee when its reward tops 3%; the merchant's own per-slip deals (CardX ฿200, KBank ฿120, Central The 1 ฿100, once a month each) do, so the plan splits a multi-ticket purchase into one order per card. Visa and Mastercard are certain there; JCB and UnionPay acceptance is unconfirmed. No TTM event is in Chiang Mai, so its page is for trips and TTM LIVE streams.
- Bank discount codes are one per order and "not combinable"; the net charge still counts toward the card's own accumulating campaigns.
