---
tags: [promotion, first-choice, krungsri]
---

# First Choice campaigns, H2 2026 — ON3/ON4, DLV3, IS3/IS4, NW4 and the BTS draw

Four Krungsri First Choice campaigns running beside [[first-choice-nw3|NW3]]. Each is tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] with one row per calendar month. First Choice is one account (Takumi's primary, plus Baiboon's and Nuta's supplements), so every campaign pools the three holders' spend. Wired in 2026-09-29 (user): ON3, DLV3 and IS3 are tracked from September 2026; BTS from August 2026.

> **Structured source of truth**: the classes in `scripts/python/lib/bureau/` — `on3.py`, `dlv3.py`, `is3.py`, `bts.py`. Each holds the terms, the bank's worked examples (asserted on every render) and the page text.

| Campaign | Class | Period | Pays | Cap |
|---|---|---|---|---|
| **ON3**, ช้อปออนไลน์ได้คืนคุ้ม | `ON3Promotion` (ladder) | 1 Jul – 30 Sep 2026 | Shopee, Lazada and TikTok spend: ฿60 per whole ฿4,000 under ฿15,000 (at most 3); from ฿15,000, ฿270 per whole ฿15,000 instead (at most 8); +฿340 at ฿150,000 | ฿2,500/month |
| **DLV3**, สั่งเดลิเวอรี่คุ้ม | `DLV3Promotion` (ladder) | 1 Sep – 31 Dec 2026 | Grab, LINE MAN, Bolt, ShopeeFood and Robinhood: ฿30 per whole ฿2,000 under ฿10,000 (at most 4); from ฿10,000, ฿200 per whole ฿10,000 (at most 2) | ฿400/month |
| **IS3**, insurance | `IS3Promotion` (per slip) | 1 Jul – 30 Sep 2026 | Per insurance slip: ฿80 per ฿10,000 (฿10k–99,999), ฿100 per ฿10,000 (฿100k–199,999), ฿1,000 per ฿100,000 (฿200k+) | ฿5,000/month |
| **BTS**, BTS WORLD TOUR 'ARIRANG' draw | `BTSFirstChoice`, `BTSKrungsriCard` (rights) | 1 Aug – 15 Nov 2026 | One lucky-draw right per slip of ฿1,500+ (full amount or installment) on a Visa card | 10 rights/month per company: First Choice and Krungsri Card each |

## Readings

- **The two ladders replace each other.** ON3's examples put ฿17,500 at ฿270, not ฿270 + ฿60, and DLV3's put ฿8,800 at ฿120 and ฿11,000 at ฿200. Both are `LadderPromotion`s like NW3: spend past the last whole step earns nothing, first come, first served.
- **ON3, DLV3, IS3 and NW3 never share a row.** NW3 excludes marketplaces, delivery and insurance because these campaigns cover them. ON3 and DLV3 mark `% cb` on the rows they pay, as NW3 does: ON3 at 1.5% or 1.8%, DLV3 at 1.5% or 2%. IS3 pays a fixed amount per slip, so it leaves `% cb` alone and keeps the money in the trackers.
- **BTS pays rights, not money.** It's the Bureau's first `RIGHTS` campaign: the month's count goes in the Bureau's `สิทธิ์ลุ้นรางวัล`. There are no trackers and no row fields. Supplements' slips earn Takumi's rights, since they count toward the primary card number. **Each company is its own pool** (user, 2026-09-29): First Choice (one Visa card per principal) and Krungsri Card (possibly several Visa cards) each give up to 10 rights a month, 20 in all. So the Bureau keeps two rows a month. The household's only Krungsri Visa card is Krungsri VISA; Lady and NOW are Mastercard. Rights are given first come, first served, in `Transaction Datetime` order.
- **BTS installment terms are only a maybe.** The bank counts the purchase slip, and the ledger holds monthly terms, so a `NN/NN` row is flagged, not linked.

## Q4 2026 — NW4, ON4, IS4 (read 2026-10-01)

NW3, ON3 and IS3 ended 30 Sep, and their successors run 1 Oct – 31 Dec 2026. DLV3 runs to 31 Dec unchanged. Each is still one row per calendar month, pooled over the three holders.

> **Structured source of truth**: `nw4.py`, `on4.py`, `is4.py`.

| Campaign | Class | Pays | Cap |
|---|---|---|---|
| **NW4**, รูดก็ได้เงินคืน | `NW4Promotion` (ladder) | ฿50 at ฿5,000–9,999; ฿200 per whole ฿10,000, up to ฿2,000. No ฿200,000 bonus any more | ฿2,000/month, ฿6,000 campaign |
| **ON4**, Shopee / Lazada / TikTok | `ON4Promotion` (ladder) | ฿25 at ฿2,000–3,999; ฿60 per whole ฿4,000 under ฿15,000 (at most 3); from ฿15,000 ฿270 per whole ฿15,000 (at most 7, ฿1,890); +฿610 at ฿150,000 | ฿2,500/month |
| **IS4**, insurance | `IS4Promotion` (per slip) | as IS3: ฿80 / ฿100 per ฿10,000, ฿1,000 per ฿100,000 by slip size | ฿5,000/month |

- **NW4 caps two categories inside the ladder.** Supermarket spend and fuel each count only up to ฿30,000 a month per primary account. The part past that is left out, and the part up to it counts as usual. NW3 instead dropped single charges over ฿10,000 (supermarket) or ฿3,000 (fuel). `NW4Promotion.countable` gives each category its ฿30,000 first come, first served, and a same-time group crossing it shares pro rata. A row cut short keeps `% cb` unset, like the boundary row.
- **NW4 leaves out MCC 5199, so `WWW.MAKRO.PRO` no longer counts.** `HTTPS://WWW.MAKRO.PRO/` (MCC 5411) is a supermarket and counts within the ฿30,000. Travel now belongs to TR3 (1 Sep – 31 Oct, not tracked) and insurance to IS4.
- **NW4 enrolment**: NW4 registrants with more than ฿10,000 of NW3 spend in both Jul and Aug 2026 were enrolled for all of Oct–Dec. The household's July and August NW3 credits (฿1,000 and more) put it well past that.
- **ON4's bank examples fix the joins**: ฿2,800 → ฿25, ฿17,500 → ฿270, ฿105,000 and ฿120,000 → ฿1,890, ฿150,000 → ฿2,500. It marks `% cb` like ON3; travel agents and airlines bought through the apps belong to TR3.
- **IS4** is credited within 5 business days and can't also count toward NW4.
- **A U PLAN conversion keeps the original charge counting** toward NW4 and IS4, once, as the full-amount slip; merchant installments (personal-loan line) never count, and no billed term is new spend (user, 2026-10-03). See [[../concepts/installment-reward-campaigns#U Plan — Krungsri / First Choice]].

## Months

| Month | Row | Result |
|---|---|---|
| Aug 2026 | `2026M8 — BTS First Choice 10 rights` / `— BTS Krungsri Card 10 rights` | 10 (the cap; Baiboon's slips 9, Takumi's 1) / 1 (Baiboon) |
| Sep 2026 | `2026M9 — BTS First Choice …` / `— BTS Krungsri Card …` | 5 (Takumi's 3, Baiboon's 2) / 2 (Baiboon) |
| Sep 2026 | `2026M9 — ON3 …`, `— DLV3 …`, `— IS3 …` | no qualifying First Choice spend yet |

Q4 sources, read 2026-10-01: <https://www.firstchoice.co.th/promotion/firstchoice-cashback> (NW4), <https://www.firstchoice.co.th/promotion/online-shopping> (ON4), <https://www.firstchoice.co.th/promotion/delivery-cashback> (DLV3, unchanged), <https://www.firstchoice.co.th/promotion/insurance-creditcard> (IS4).

Sources, read 2026-09-29: <https://www.firstchoice.co.th/promotion/shopping-online>, <https://www.firstchoice.co.th/promotion/delivery-cashback>, <https://www.firstchoice.co.th/promotion/insurance-credit-card>, <https://www.firstchoice.co.th/promotion/bts-world-tour-arirang-in-bangkok>.
