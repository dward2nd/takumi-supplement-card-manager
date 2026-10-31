---
tags: [promotion, uob, pay-with-points, dining]
---

# UOB Dining PWP 2026 — PWP20 / DPWP (DPW128)

A UOB **pay-with-points** dining campaign: register a restaurant slip, and UOB takes UOB Rewards points equal to the slip's net amount and credits back a share of the slip in baht. It is a points redemption, not a cashback earned on spend, so it costs points, and it isn't in the [[../concepts/promotion-bureau|Promotion Bureau]].

- **Campaign**: `2026-01-01` → `2026-12-31`, campaign code DPW128.
- **Source**: <https://www.uob.co.th/personal/promotions/credit-cards/dining-pwp-2026-dpw128-0226/dining-pwp-2026-dpw128-0226.page>, read 2026-10-30. An old-style URL with no `.json` twin: the terms render through r.jina.ai, and the rate table is only in the banner image (`…/dining-pwp-2026-dpw128-0226-d.jpg`). See [[../catalogues/research-methods|research methods]].

## Rates

| Code | Days | Slip | Credit |
|---|---|---|---|
| `PWP20` | Friday – Sunday | ≥ ฿1,500 | 20% |
| `DPWP` | every day | ≥ ฿500 | 10% |

Points are taken 1 for each baht of the slip ("ใช้คะแนนสะสม … เท่ายอดใช้จ่ายสุทธิ"), so a ฿1,760 slip costs 1,760 points and returns ฿352 under PWP20. `PWP20` is limited to 2 redemptions a month. The page names no other cap.

## Terms that matter here

- **Primary cards only.** Every supplement card is excluded, as are business cards, every KrisFlyer World and Royal Orchid Plus card, YOLO Platinum, UOB One, UOB Simple, UOB Lazada, **UOB Makro** and the TMRW card. Of the household's UOB credit cards, only Takumi's own UOB World and UOB Premier can join. A friend's dining on her own supplement can't join; her `[บัตรหลัก]` share of a slip on Takumi's card can.
- **Register each slip, on the day of the meal**: SMS `<code> <last 12 card digits> <slip amount without commas or decimals>` to 4545111, or Rewards+ in UOB TMRW.
- **Restaurants by MCC**: 5462, 5811, 5812, 5813, 5814, 5921. Not hotel restaurants, not paid through an e-wallet (TrueMoney, Rabbit LINE Pay, ShopeePay).
- **Timing**: the points come off and the credit lands on the primary card account within 60 days of the end of the month of the meal. A meal in October is credited by 30 December.
- If the account has fewer points than the slip's amount, UOB may cancel the redemption. Points taken aren't returned, and a cancelled or refunded meal loses its credit.
- "Not combinable with other promotions" (term 13). The card's standing `×5` points are still left on the row: whether UOB withholds them on a PWP slip is unknown until a statement shows it.

## Booking

The credit prints on Takumi's UOB statement as a `PWP: <merchant>` line. Book it with the pay-with-points pattern (and, when it lands after a statement, the "Bank credits that post after the cut-off" rule under [[../databases/takumi-bills#Payments|Takumi's Bills → Payments]]):

- **Takumi's share** of the slip: the bank's `PWP: …` line in his ledger, `×0`, `% cb` unset. His points come off through a ฿0 `แลกคะแนนแทนค่าใช้จ่าย <n> คะแนน` row with `ใช้คะแนน` n.
- **Trackers at registration** (user, 2026-11-01: "I didn't find the expected 20% cashback … in the cashback tracker DB"). PWP isn't a Bureau campaign, so no sync makes trackers for it. When a slip is registered, add a tracker row by hand for each holder with a share of the slip: `PWP20 UOB World 20% <merchant> <d Mon>`, `Transaction Date` the meal date, `Card` that holder's UOB World, `Promotion` empty, `Expected Cashback` = rate × that holder's share of the slip. Link the credit row in `Slip Transaction` and tick when it posts ([[../databases/cashback-trackers|cashback trackers]]).
- **A friend's `[บัตรหลัก]` share**: her credit goes in her ledger (`[หักลบหนี้เก่า] PWP: …` in the meal's cycle, then `PWP: …` and a cancelling `[ยกยอดมาจาก <YYYY-MM>]` in the cycle that prints it). Whoever's points pay for her share get a ฿0 `แลกคะแนนแทนค่าใช้จ่าย` row in their own ledger. Ask how the points and the credit are split when the user hasn't said.

## Uses

| Meal | Slip | Code | Rows | Points | Credit | Status |
|---|---|---|---|---|---|---|
| Fri 30 Oct 2026, `SUSHIRO GH(TH)C.CHIANG BANGKOK TH` (UOB World) | ฿1,760 | `PWP20` | Takumi ฿1,155 + Baiboon `[บัตรหลัก]` ฿605 | 1,760 | ฿352 | Registered (user, 2026-10-30). Credit due by 30 Dec 2026. Credit split by share: trackers Takumi ฿231 + Baiboon ฿121 (2026-11-01). Points assumed the same way (1,155 + 605), to confirm when UOB takes them. |

The two rows add up to the one slip: Takumi's ฿1,155 alone is under PWP20's ฿1,500 floor.
