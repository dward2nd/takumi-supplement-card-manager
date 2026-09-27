---
tags: [promotion, first-choice]
---

# First Choice NW3 — "แมตช์ทุกยอด คุ้มทุกการใช้" (Jul–Sep 2026)

Krungsri First Choice's monthly cashback ladder on pooled full-amount spend. Takumi holds the primary card, and Baiboon and Nuta have supplements on it. The bank credits Takumi's account, and the household shares the credit out through the [[../concepts/promotion-bureau|Promotion Bureau]].

> **Structured source of truth**: `scripts/python/lib/bureau/nw3.py` (`NW3Promotion`). The ladder, the exclusion list, the page text and the bank's worked examples all live there. The Bureau page body is rendered from them, so edit the class and re-render (`/sync-promotion` with `replace_summary`) rather than hand-editing the page.

- **Campaign**: `2026-07-01` → `2026-09-30`; register once before spending (UCHOOSE app `NW3`, or SMS). Follows NW2 (Apr–Jun).
- **Card**: First Choice (Krungsri First Choice Visa Platinum; see `scripts/repositories/cards/first-choice.yaml`).
- **Source**: <https://www.firstchoice.co.th/promotion/cashback-firstchoice>, read 2026-09-28.

## Ladder (per calendar month, pooled)

฿5,000–9,999 → ฿50 flat · every whole ฿10,000 → ฿200 (2%), up to ฿2,000 at ฿100,000 · ฿200,000+ → +฿500. The monthly cap is ฿2,500 and the campaign cap ฿7,500; the campaign cap is just 3 × the monthly one, so it never binds alone. **Steps, not a smooth 2%**: the bank's own examples put ฿30,000 at ฿600, and the household's ฿36,908.92 in September also earns ฿600.

## Household readings of the terms

- **Public organizations are excluded.** The bank excludes government-agency payments (หน่วยงานราชการ). The household reads that to include public organizations (องค์การมหาชน), so `MUSEUM SIAM` rows are left unlinked (user, 2026-09-28).
- **ShopeeFood is excluded.** It falls under food delivery, even though the marketplace clause names it as an exception to *that* clause.
- **TrueMoney rows are unresolved.** NW3 excludes e-wallet top-ups. `TMN*TMN 7-11` is read as a top-up at 7-Eleven, and `TMN*PROMPTPAY30` / `TMN*<merchant>` are payments routed through TrueMoney. The household links them anyway; `/sync-promotion` flags them `uncertain`. In September, dropping all 52 (฿6,465.33) still leaves ฿30,443.59, so still ฿600.
- **Installments never count.** A merchant installment books to First Choice's personal-loan line (see the card YAML's notes).

## Months

| Month | Bureau row | Pooled | Credit | Split |
|---|---|---|---|---|
| Jul 2026 | — (pre-Bureau) | — | ฿1,000 (statement) | friends flat 2%, Takumi remainder: Baiboon 941.52 · Nuta 37.16 · Takumi 21.32 |
| Aug 2026 | — (pre-Bureau) | — | pending statement | friends flat 2%: Baiboon 674.54 · Nuta 17.84 |
| Sep 2026 | `2026M9 — NW3 cb 2%` | ฿36,908.92 | ฿600 (ladder) | FCFS: Takumi 299.35 · Baiboon 250.32 · Nuta 50.33 |

**Open drift (Sep).** On 2026-09-28 the bank app showed ฿36,803.92 against the Bureau's ฿36,908.92, a gap of +฿105. The likeliest cause is `KALM VILLAGE CHIANGMAI TH` (2026-09-15). It sits at ฿105 on both Takumi's row and Baiboon's `[บัตรหลัก]` row, both noted `ทำข้อตกลงหารครึ่ง` ("agreed to split in half"), which would fit a ฿105 charge recorded twice instead of ฿52.50 each. It doesn't change the step (still ฿600), but it moves the FCFS shares by about ฿2. Fix from the October statement, then re-run `/sync-promotion`.
