---
tags: [promotion, central-the-1, krungsri]
---

# Central The 1 "T1 Invite": ฿200 per ฿10,000, up to ฿400 (16 Nov 2026 – 15 Jan 2027)

**พิเศษเฉพาะคุณ รับเครดิตเงินคืนสูงสุด 400 บาท\*** ("just for you: up to ฿400 cashback credit"). A Central The 1 card offer **by invitation only**, sent to Takumi's account. It is tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] as `2026M11 — T1 Invite cb ฿400`, one row for the whole campaign.

> **Structured source of truth**: `scripts/python/lib/bureau/central_invite.py` (`CentralInvitePromotion`).

## Terms

The user typed these in from the invitation on 2026-11-26. Invitation-only offers have no public page, and a web search that day found nothing.

| Spend over the whole campaign | Cashback credit |
|---|---|
| every whole ฿10,000 | ฿200 |
| cap | **฿400 per primary card account** (`หมายเลขบัญชีบัตรหลัก`) for the campaign, reached at ฿20,000 |

- **Who:** only cardholders who received the invitation.
- **Registration:** by SMS, or free in UCHOOSE, on or before the spend day (`ลงทะเบียนก่อนหรือภายในวันที่ทำรายการ`). Only spend after the confirmation SMS counts.
- **Pooling:** supplement spend counts with the primary account (`ยอดใช้จ่ายจากบัญชีบัตรเสริมจะถูกคำนวณรวมกับบัญชีบัตรหลัก`). On the Central The 1 Redz that means Takumi's rows and Baiboon's: both her supplement rows and her `[บัตรหลัก]` rows on his card.
- **Not counted:**
  - utilities;
  - funds of every kind;
  - insurance of every kind, unit-linked policies included;
  - cash withdrawals and Central The 1 Call for Cash;
  - cancelled or disputed charges;
  - interest and fees.

  Nothing else is excluded. Spend thresholds are read verbatim ([[../concepts/promotion-bureau|Bureau]]), so Makro, marketplaces, delivery apps, TrueMoney payments, foreign spend and subscriptions all count.
- **Installment terms (`NN/NN`) are flagged `uncertain`.** The page doesn't exclude installments, but it's unknown whether the bank counts the purchase once or each term.
- **Crediting:** within 60 days of the date the merchant bills each charge to the bank (`นับจากวันที่ร้านค้าทำการเรียกเก็บ`), into the primary account. The amount counted is what the merchant bills, which can differ from the price at the till. A ฿200 step can therefore arrive before 15 Jan.
- **General conditions:**
  - The account must be open and in good standing when the credit is given.
  - A missing or wrong credit must be raised with the card centre within 90 days of the end, i.e. by 15 Apr 2027.
  - Issued by General Card Services (บริษัท เจเนอรัล คาร์ด เซอร์วิสเซส จำกัด).

## Code

The user didn't give the bank's SMS / UCHOOSE keyword, so the household calls it **`T1 Invite`**. If the statement's credit line shows a code, rename the Bureau row and the trackers to match. The class matches on `\bT1 Invite\b`, so its `code` changes too.

## Registration and the eligible list

UCHOOSE's eligible list on 2026-11-26 (user) showed exactly the three rows the Bureau linked:

| Date | Holder | Row | ฿ |
|---|---|---|---:|
| 22 Nov | Takumi | `THE BARISTRO CHIANGMAI TH` | 85.00 |
| 22 Nov | Baiboon | `[บัตรหลัก] THE BARISTRO CHIANGMAI TH` | 145.00 |
| 26 Nov | Takumi | `WWW.THAITICKETMAJOR.CO BANGKOK TH` | 6,519.00 |

That makes ฿6,749 pooled, so ฿3,251 more reaches the first ฿200. Takumi registered by 22 Nov. The card has no spend from 16 to 21 Nov, so the exact date costs nothing. The `[คะแนนพิเศษ]` ฿0 rows are not purchases and aren't linked.

## Changes from NW4 and GWSE

Compared on 2026-11-26 with First Choice [[first-choice-2026h2|NW4]] (the Krungsri group's own ฿200-per-฿10,000 ladder) and with **GWSE**, the Central The 1 card's own one-off threshold (+฿300 at ฿50,000 at GO Wholesale, 14 Oct – 24 Nov; [[../catalogues/2026-11/the1|The 1 research]] §3.1):

- **Period:** one quota for the whole campaign. NW4's ladder resets each calendar month; GWSE also has one quota for its campaign.
- **Ladder:** ฿200 per whole ฿10,000, at most ฿400.
  - NW4: ฿50 at ฿5,000–9,999, then ฿200 per ฿10,000 up to ฿2,000 a month.
  - GWSE: ฿300 once, at ฿50,000.
- **What counts:** nearly everything.
  - NW4 also leaves out marketplaces, delivery apps, travel, Makro (MCC 5199), government, gold, financial services, foreign spend, subscriptions and e-wallet top-ups, and caps supermarkets and fuel at ฿30,000 a month.
  - GWSE counts GO Wholesale only and leaves out every e-wallet.
- **Crediting:** within 60 days of each charge's billing date.
  - NW4: within 60 days after each month-end.
  - GWSE: within 7 days after its end.
- **Who:** invited cardholders only. NW4 and GWSE are open to anyone who registers. Registration works the same way in all three: UCHOOSE or SMS by the spend day, counting from the confirmation.
- **Pooling:** supplement spend pools with the primary account and the credit lands on the primary, as for NW4 and GWSE.

## Household split

First come, first served by `Transaction Datetime`, as for every ladder ([[../concepts/promotion-bureau|Bureau]]). Only spend inside a paid step earns. Rows on the same day share a step boundary pro rata. Takumi receives the credit on his card and pays Baiboon her share ([[../concepts/promotion-bureau|trackers]]).
