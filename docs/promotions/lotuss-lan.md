---
tags: [promotion, lotuss]
---

# Lotus's LAN "ช้อปโลตัส รับคืนซูเปอร์คุ้ม" (Oct–Dec 2026)

Lotus's credit-card cashback on spend **at Lotus's itself**: every branch and Lotus's Shop Online, pooled per calendar month on Takumi's [[../cards/lotuss-beyond|Lotus's Beyond]] account, supplements included. Takumi registered on or before 2 Oct 2026 (user, 2026-10-05). Tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] from October 2026.

> **Structured source of truth**: `scripts/python/lib/bureau/lotus_store.py` (`LANPromotion`).

## The monthly ladder

**Only the single highest tier pays** ("สงวนสิทธิ์การให้เครดิตเงินคืนเพียงระดับสูงสุดเพียงระดับเดียวเท่านั้น"):

| Pooled Lotus's spend in the month | Cashback |
|---|---|
| under ฿2,000 | nothing |
| every whole ฿2,000, while under ฿20,000 | ฿40, at most ฿200 |
| or every whole ฿20,000, from ฿20,000 | ฿300, at most ฿600 |

So ฿19,999 earns ฿200 and ฿20,000 earns ฿300. Caps: ฿600 a month and ฿1,800 for the campaign per primary account, which three full months reach exactly.

## What counts

- Every Lotus's branch (`LOTUS'S <branch> …`) and Lotus's Shop Online, in Thailand.
- Paid by **EDC, tap or UCHOOSE QR only — no e-wallet of any kind**, so `TMN*LOTUS HYPER` / `TMN LOTUS` don't count. That's unlike the card's coins, which do pay 1.5 on `TMN*LOTUS HYPER` ([[../cards/lotuss-beyond|card note]]).
- Settled spend, as billed on the statement; cancelled or returned spend comes back out.
- Supplements count, and their credit goes to the primary account. The untracked supplement …6524 counts toward the same pool but sits in Takumi's ledger as one `โอนยอดจากบัตรเสริม` lump, so **the bank can pay a higher tier than the Bureau's linked rows reach**.
- Register once: UCHOOSE → `LAN`, or SMS `LAN <16-digit card no.>` to 081-250-7777. Only spend from the registration day on counts.
- Cards approved from 1 Aug 2026 on can't join.

**Excluded**: shops renting space and food courts inside Lotus's malls (they post under their own names, e.g. `884 WATSONS LOTUS'S JO CITY TH`); Lotus's abroad; Lotus's goods bought through another platform; gift baskets, alcohol, cigarettes and stage 1–2 infant formula (taken out of a slip, so the ledger can't see them); utility bills, mutual funds, insurance, installments, cash advances, balance transfers, fees and interest.

## Stacking

The page has no clause against other promotions. [[lotuss-smp1|SMP1]] and [[lotuss-lbs3|LBS3]] both exclude Lotus's own spend, so nothing is counted twice anyway.

## Crediting

Within 60 days after each month-end, on the primary account's statement: October's by December, November's by January 2027, December's by February 2027. `% cb` stays unset on Lotus's rows; the money goes in the Bureau and Takumi's tracker.

## Predecessor?

Takumi's ledger has `CB MLO_Promotion 1 - 31 JUL'26`, `… AUG'26` and `CB MLO_Promotion 1 - 30 Sep'26` (6 Oct), ฿40 each, a month after the month they name. That is the size of one ฿2,000 step. His own Lotus's spend in August was well under ฿2,000, so if MLO was LAN's Q3 predecessor, the …6524 supplement's spend made up the rest. Unconfirmed.

## Bureau rows

| Row | Created | State |
|---|---|---|
| `2026M10 — LAN cb 2%` | 2026-10-05 | ฿119 linked (2 Oct); ฿0 until October reaches ฿2,000 |

Source, read 2026-10-05: <https://www.lotussmoney.com/promotion/credit-card/shopping/lotuss-shopping-online>.
