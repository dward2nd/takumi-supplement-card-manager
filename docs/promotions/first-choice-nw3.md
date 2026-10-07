---
tags: [promotion, first-choice]
---

# First Choice NW3 — "แมตช์ทุกยอด คุ้มทุกการใช้" (Jul–Sep 2026)

Krungsri First Choice's monthly cashback ladder on pooled full-amount spend. Takumi holds the primary card, and Baiboon and Nuta have supplements on it. The bank credits Takumi's account, and the household shares the credit out through the [[../concepts/promotion-bureau|Promotion Bureau]].

> **Structured source of truth**: `scripts/python/lib/bureau/nw3.py` (`NW3Promotion`). The ladder, the exclusion list, the page text and the bank's worked examples all live there. The Bureau page body is rendered from them, so edit the class and re-render (`/sync-promotion` with `replace_summary`) rather than hand-editing the page.

- **Campaign**: `2026-07-01` → `2026-09-30`; register once before spending (UCHOOSE app `NW3`, or SMS). Follows NW2 (Apr–Jun). Followed by **NW4** (1 Oct – 31 Dec 2026): same ladder without the ฿200,000 bonus, ฿30,000-a-month caps on supermarket and fuel spend, MCC 5199 out; see [[first-choice-2026h2#Q4 2026 — NW4, ON4, IS4 (read 2026-10-01)]].
- **Eligible list**: the First Choice app (UCHOOSE, as for every Krungsri-family card) shows which transactions count toward NW3, with their total. That list is the reference for linking rows to the Bureau, and its total is `/sync-promotion`'s `bank_spend`.
- **Card**: First Choice (Krungsri First Choice Visa Platinum; see `scripts/repositories/cards/first-choice.yaml`).
- **Source**: <https://www.firstchoice.co.th/promotion/cashback-firstchoice>, read 2026-09-28.

## Ladder (per calendar month, pooled)

฿5,000–9,999 → ฿50 flat · every whole ฿10,000 → ฿200 (2%), up to ฿2,000 at ฿100,000 · ฿200,000+ → +฿500. The monthly cap is ฿2,500 and the campaign cap ฿7,500; the campaign cap is just 3 × the monthly one, so it never binds alone. **Steps, not a smooth 2%**: the bank's own examples put ฿30,000 at ฿600, and the household's ฿36,908.92 in September also earns ฿600.

## Household readings of the terms

- **Public organizations are excluded.** The bank excludes government-agency payments (หน่วยงานราชการ). The household reads that to include public organizations (องค์การมหาชน), so `MUSEUM SIAM` rows are left unlinked (user, 2026-09-28).
- **ShopeeFood is excluded.** It falls under food delivery, even though the marketplace clause names it as an exception to *that* clause.
- **TrueMoney rows count.** NW3 excludes e-wallet top-ups, but the app's NW3 eligible list for September included the household's `TMN*…` rows (`TMN*PROMPTPAY30`, `TMN*TMN 7-11`, `TMN*<merchant>`): 52 rows, ฿6,465.33, against a gap of only ฿105. So TrueMoney-routed card payments aren't top-ups to the bank, and the exclusion rule has no merchant test.
- **Merchant installments never count; U PLAN conversions do.** A merchant installment books to First Choice's personal-loan line (see the card YAML's notes). A full-amount charge converted later through U PLAN still counts, once, as the original charge: sure for 0% plans, unconfirmed for plans with interest (user, 2026-10-03). Billed terms (`NN/NN`) are never new spend. See [[../concepts/installment-reward-campaigns#U Plan — Krungsri / First Choice]].

## Months

| Month | Bureau row | Pooled | Credit | Split |
|---|---|---|---|---|
| Jul 2026 | — (pre-Bureau) | — | ฿1,000 (statement) | friends flat 2%, Takumi remainder: Baiboon 941.52 · Nuta 37.16 · Takumi 21.32 |
| Aug 2026 | — (pre-Bureau) | — | ฿800, credited 6 Sep | friends flat 2%, Takumi remainder: Baiboon 674.54 · Nuta 17.84 · Takumi 107.62 |
| Sep 2026 | `2026M9 — NW3 cb 2%` | ฿44,036.92 | ฿800 (ladder), credited 6 Oct | FCFS: Takumi 334.25 · Baiboon 415.42 · Nuta 50.33 |

**September reconciled (2026-09-28).** The Bureau matches the app's eligible list to the satang: ฿36,803.92. Getting there took two fixes:

- **+฿200 removed.** Baiboon's `TMN*PROMPTPAY30` ฿90 and ฿110 on 2026-09-16 had been entered twice (again in the 2026-09-18 batch); the later copies were archived.
- **−฿95 added.** A second `FIVE STAR THREE KINGS CHIANGMAI TH` charge on 2026-09-15 (฿95, Takumi's primary card, alongside the ฿60 one) was missing from Notion. It was recorded and linked.

False leads, for next time: KALM VILLAGE (an even split), the two ฿95 `TMN*PROMPTPAY30` rows on 09-13 (both real), and the five split charges (all match the app). A single row equal to the gap is no lead when even splits exist. Checking against the app's list row by row, from the day after the last verified statement, is what found both errors.

The boundary day (09-24) was then ordered by times the user found: PROMPTPAY30 10:56, DUMPLINGS 18:47, Hai Di Lao 21:21. Final split: Takumi ฿302.94 · Baiboon ฿246.73 · Nuta ฿50.33 = ฿600.

**September credited (2026-10-07).** Spend recorded after 28 Sep, to the month's end, took the pool to ฿44,036.92 and the ladder to ฿800. The bank credited ฿800 on 6 Oct, matching the Bureau. Each holder's ledger has a `NW3 Cashback 2% (1–30 Sep 2026)` row for their share on First Choice, billed 5 Nov, as August's were: Takumi −334.25 (`×0`, the Note naming the friends' shares), Baiboon −415.42, Nuta −50.33.
