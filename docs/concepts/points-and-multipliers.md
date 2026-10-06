---
tags: [concept, rewards]
---

# Point multipliers (`×0` `×2` `×3` `×4` `×5` `×6` `÷4`)

Reward points are modelled as **independent boolean multiplier columns**, not as a single number. Each transaction carries several checkbox flags that indicate which promotional rate applies, and the [[../formulas/points-realized|`คะแนนที่ได้จริง`]] formula combines them with the card's `บาทต่อ 1 คะแนน` rate to produce actual points earned.

## The set of multipliers, by person

| Multiplier | [[../people/takumi\|Takumi]] | [[../people/baiboon\|Baiboon]] | [[../people/nuta\|Nuta]] |
|------------|---------|---------|------|
| `×0`       | ✓        | ✓        | ✓     |
| `×2`       | ✓        | ✓        | ✓     |
| `×3`       | ✓        |          |       |
| `×4`       | ✓        | ✓        | ✓     |
| `×5`       | ✓        | ✓        | ✓     |
| `×6`       | ✓        | ✓        | ✓     |
| `÷4`       |          | ✓        | ✓     |

So Takumi's transactions support `×3` but not `÷4`; supplement holders' transactions support `÷4` but not `×3`. `×6` was added to all three on 2026-10-05 for [[../cards/lotuss-beyond|Lotus's coins]] at Lotus's (1.5 coins a ฿50 block = 6 × the 0.25 general rate).

## Why boolean columns instead of one multiplier number

Two reasons inferred from the structure:

1. **Promo identity is preserved**. A `×5` is conceptually different from "five times the base rate" — it's a specific promo campaign. If you stored the resolved multiplier as `5.0`, you'd lose the trace.
2. **Multiple multipliers can co-apply** (or be considered independently for reconciliation). The schema permits more than one checkbox to be true on the same row; the formula must encode priority/combination rules. Decode in [[../formulas/points-realized]] when needed.

## Related fields on the transaction

- `ใช้คะแนน` — points *redeemed* against this transaction (separate axis from points earned).
- `คะแนนที่ได้จริง` (formula) — actual points earned this row.
- `คะแนน unrealized` (formula) — potential/expected points before some condition resolves (likely tied to `Processed` or `Credit Return`).

## On the Cards side

- `บาทต่อ 1 คะแนน` (baht per point) is the per-card base rate, rolled up into each transaction.
- `คะแนนต่อ 1 หน่วย` (points per unit; since 2026-10-05) is what one `บาทต่อ 1 คะแนน` block earns at ×1. Empty means 1; only Lotus's Beyond sets it (0.25). It is applied after the formula's floors, so a card can earn fractions. See [[../formulas/points-realized]].
- `คะแนนสะสม` rolls up `คะแนนที่ได้จริง` across transactions.
- `ให้คะแนนตามรอบบิล` is a per-card checkbox: true if the bank awards points per billing cycle rather than per transaction (changes when "realized" happens).

## Approximation caveat

The `×0/×2/×3/×4/×5/÷4` set is **not** the issuer's real earning rule — it's a **convenience approximation** chosen to be fast to click in Notion's fixed-checkbox UI and to cover the common Thai-credit-card promotional shapes. Real earning rules can be richer:

- **Fractional points** (a transaction earns `0.25 pts` per 50 ฿, not an integer multiple of a base rate). The checkbox enum can't express this alone; since 2026-10-05 the card's `คะแนนต่อ 1 หน่วย` carries the fraction. See [[../cards/lotuss-beyond]].
- **Per-merchant bonus tiers within a card** — the issuer awards different rates depending on the merchant string, not just on whether a promo checkbox is set. See [[../cards/lotuss-beyond]] (general vs at-Lotus) and [[../cards/uob-makro]] (general vs in-store Makro, with the `÷4` checkbox standing in for "this was an in-store-Makro swipe").
- **Conditional fall-back via the merchant string** — UOB Makro's `÷4` only applies when the transaction was physically read by Makro's in-store reader. TrueMoney intermediation (`TMN*…`) breaks that condition and reverts to the base rate. The checkbox alone doesn't encode the "TrueMoney breaks it" rule; the human entering the row has to know.

So the multiplier set is a **lossy projection** of the underlying rules. Where the gap matters, the per-card narrative note is the source of truth (`docs/cards/<card>.md`), not the Notion checkbox. The phase-2 app models the underlying rules directly as `RewardRule` JSON entries on `Transaction` — see [[../future-app/data-model-target]] and [[promotions]].

## Programme quirks the ledger lives with (2026-09-28)

- **Rounding.** UOB and the Krungsri family (Krungsri, Lotus's) round per statement line, like the ledger formula; Krungsri leaves credit lines out of the point base (user, 2026-10-07; the 5 Oct 2026 Visa printed 485, where one rounding on the cycle gives 486, and Lady's 177 ignores its −฿152 of credits). KBank and KTC round once on the cycle's spend, so the ledger runs short each cycle. The difference goes on a `[ปรับคะแนน] ปัดเศษคะแนนรอบบิล YYYY-MM` row in the principal holder's ledger; `/record-statement` adds it (user). A charge split into `[บัตรหลัก]` shares loses points the same way: `[ปรับคะแนน] <line>` rows, also on the principal holder's ledger.
- **Bonus points and redemptions outside a card.** KBank prints `BONUS POINTS` per product (Shopee +800 in Aug 2026, PLUSTINUM +1,000 in Sep 2026); these are recorded as `[คะแนนพิเศษ] KBank BONUS POINTS` rows. A `CASH REBATE` redemption can draw on bonus points that belong to no card; only the part a card pays shows on it (PLUSTINUM −69, `แลกคะแนน CASH REBATE 69 คะแนน`).
- **Lotus's coins are fractional**: 0.25 coin per ฿50, or 1.5 coins per ฿50 at Lotus's, counted per statement line (decoded 2026-10-05). Until 2026-10-05 the household kept whole points everywhere and Lotus's coins weren't audited (user, 2026-09-28); now the ledger holds them (`คะแนนต่อ 1 หน่วย` = 0.25, `×6` at Lotus's) and `/audit-rewards` and `/sync-points-balance` cover them. See [[../cards/lotuss-beyond]].
- **No points at Bangchak on Krungsri** (user, 2026-10-07: "whether you receive cashback or not"). The Bangchak promotion's terms ([krungsricard.com/th/promotion/bangchak](https://www.krungsricard.com/th/promotion/bangchak), 1 Oct 2026 – 31 May 2027) say `สงวนสิทธิ์ยกเลิกการให้คะแนนสะสมปกติ` (the card's normal reward points are withheld). The cards it lists include Krungsri Visa Platinum, Mastercard Platinum, JCB Platinum and Lady Titanium; the household's Visa is the Platinum. `BSRC-…` stations are Bangchak's. `KrungsriPetrolCampaign` is narrower in its cards and broader in its stations than the bank: it covers JCB and Lady only, but zeroes points at every petrol brand (PTT, Shell, Caltex, Esso too). The 5 Sep 2026 JCB statement printed +0 on `BSRC-PHAAPOOM ENERGY` ฿800, its only line. **Krungsri JCB, 5 Oct 2026 (/audit-rewards, 2026-10-07):** printed +305 against the ledger's 253. With per-line rounding and credits left out, exactly one of the 256 ways to include or exclude its 8 charge lines gives 305: `HTTPS://WWW.MAKRO.PRO/` 161 + `SUSHIRO` 53 + `AGODA.COM INTERNET INT` ฿2,289.43 91. So, unconfirmed:
  1. **That Agoda line earned**, though the ledger has it `×0` under the foreign-in-THB default. Whether it is a foreign merchant at all is unclear: the statement prints `INTERNET INT`, not a country (user, 2026-10-07) ([[promotions#Foreign merchant billed in THB]]).
  2. ~~Posting-date deferral~~ *Unlikely* (user, 2026-10-07): UCHOOSE showed 3,857 on 6 Oct, the statement's figure, with no spending since 5 Oct. So the two lines dated 05/10 most likely just didn't earn. **The two lines posted on the statement date earned nothing yet**: `MJT-CPN` ฿980 (39) and `AGODA.COM CHAROEN TH` ฿964.21 (38), both posting 05/10/26. That looks like UOB's posting window (points for lines posted up to the day before the statement date). If so, the 5 Nov 2026 statement prints +39, or +77 if the second Agoda earns too, beyond its own lines. Lotus's lines posted 04/10 did earn on 5 Oct; no earning line on these statements posted on 05/10 except these two.
  3. **Petrol earned nothing**, as on Lady (BSRC ฿800) and the 5 Sep JCB (BSRC ฿800).
  The ledger's account balance agrees: Takumi 3,390 + Baiboon 415 = 3,805 against 3,857 on the statement and in UCHOOSE. That is the same 52, since the Sep balance was set to the statement's 3,552. Without the deferral, the only line mix that fits is: `MJT-CPN CHIANGMAI` ฿980 (Takumi's) earned nothing, Agoda ฿2,289.43 earned 91, and Agoda ฿964.21 earned nothing (253 − 39 + 91 = 305).
  **Backtest (2026-10-07).** The rule was checked on all 16 Krungsri-family statements with a points box on the Bills rows: JCB Feb/Apr 2025 and Sep/Oct 2026, Lady Sep/Oct 2026, NOW Jun–Oct 2026, Visa Sep/Oct 2026, and Lotus's May/Sep/Oct 2026. The check uses per-line points, credits left out, installment terms at 0 (Krungsri pays their points upfront), and NOW at 0. First Choice and Central The 1 print no points; Visa Feb 2025 has no points box; Visa Apr 2025 is a photo.
  - Only the 5 Oct 2026 JCB has an earning line posted on its statement date. It fits with the deferral and is +77 without it. On every other statement both models give the same figure, so they neither support nor contradict the rule. No statement credits a line posted on its own statement date. The carry-in side has never been testable: no earlier statement had such a line. The 5 Nov 2026 JCB is the first test.
  - Eleven statements match exactly, all those from Sep 2026 on plus NOW Jun–Aug.
  - Three mismatches have nothing to do with timing. JCB Feb 2025 printed 1,842: 1,789 is the upfront points on `2C2P (THAILAND) - SAMSUN` ฿44,736 (`001/010`), and the rest only fits if the `TMN 7-11` lines earned, so the [[krungsri-truemoney-711-exclusion|7-11 exclusion]] postdates it. JCB Apr 2025 printed 129, and only one mix fits: `SPOTIFY STOCKHOLM SWE` ฿219 + `AGODA.COM` ฿2,103.87 + ฿948.29. So foreign merchants in THB earned on JCB then too, except a third Agoda line (฿1,035.23) that got nothing. Lotus's 28 May 2026 (the old cycle) only fits if …6524's Lotus's lines earned double special coins.
  - Krungsri NOW printed 0 points on all five statements, Jun–Oct 2026, with nothing outstanding, though the classifier gives its non-online lines points (`HTTPS://WWW.MAKRO.PRO/`, `AMP*AIS`). The ledger already has them at `×0`.
- **KTC** has the longest exclusion list; see [[../promotions/ktc-forever]].

## Statement balance rows

A card's `คะแนนสะสม` is the sum of its ledger rows, and each ledger only goes back so far. Takumi's reset rows (2026-09-22, [[ledger-reset]]) zeroed his cards, and the friends' ledgers never held the whole account. So on **2026-09-29** each card's running points were set to what the bank prints, with one row per card and statement. [[../../.claude/skills/sync-points-balance/SKILL|`/sync-points-balance`]] writes and maintains these rows:

| Property | Value |
|---|---|
| `Name` | `[ปรับคะแนน] ยอดคะแนนคงเหลือตามใบแจ้งยอด <statement BC>` ("points outstanding per the statement") |
| `ยอดชำระ` | `0`, `×0` |
| `ใช้คะแนน` | −(printed outstanding − the ledgers' points as of the statement). Negative adds points. |
| `Transaction Datetime` / `Bill Cycle Date` / `Due Date` | the statement's cycle |
| ledger | the account holder's: **Takumi's** for a pooled account (UOB, KBank, Krungsri); the card's own holder where the bank prints one statement per card number (KTC, CardX) |

**The rule** (user, 2026-09-29): *the points total on a statement = Takumi's points + his friends' points.* The row is sized so that the sum over all three ledgers, as of the statement, equals the printed outstanding points. On a KTC or CardX statement, which covers one card number, that sum is the card number's own rows, plus friends' `[บัตรหลัก]` shares on Takumi's principal card.

**As of the statement** uses `/audit-rewards`' period rule. For UOB, charges count if they *posted* before the statement's cycle date. For other issuers, rows count if they're billed on or before the statement's cycle. `Reset …` rows always count. Rows after the statement, such as open-cycle charges and a redemption made since, stay on top. So the card reads the bank's figure plus what has happened since.

`/audit-rewards` and `/record-statement`'s rounding step leave these rows out (`BALANCE_ADJUSTMENT` in `lib/points_account.py`). They set an opening balance; they aren't points earned in the cycle. `/record-statement` already ignores `[ปรับคะแนน…` rows when matching statement lines.

Rows written 2026-09-29 (the printed figures):

| Card | Statement | Printed | Ledgers before | Row |
|---|---|---:|---:|---:|
| UOB World …9310 | 2026-09-25 | 17,618 | 1,020 | +16,598 |
| UOB Premier …4721 | 2026-09-25 | 162 | 0 | +162 |
| UOB Makro …1649 | 2026-09-25 | 1,545 | 1,540 | +5 |
| KBank Shopee …0052 | 2026-09-25 | 5,792 | 1,003 | +4,789 |
| KBank PLUSTINUM …3831 | 2026-09-25 | 4,004 | 3,811 | +193 |
| Krungsri JCB …8391 | 2026-09-05 | 3,552 | 201 | +3,351 |
| Krungsri Visa …7679 | 2026-09-05 | 2,678 | 230 | +2,448 |
| KTC Digital VISA …0581 | 2026-08-27 | 4,932 | 71 | +4,861 |
| KTC JCB …0059 | 2026-08-27 | 23 | 10 | +13 |
| KTC UnionPay …1346 | 2026-08-27 | 1,964 | 53 | +1,911 |
| KTC UnionPay …2310 (Baiboon) | 2026-08-27 | 235 | 238 | −3 |
| CardX JCB …1265 (Nuta) | 2026-09-05 | 70 | 66 | +4 |
| Lotus's Beyond …3471 (written 2026-10-05) | 2026-09-05 | 287.5 coins | 15.25 | +272.25 |

KBank JCB, Krungsri Lady and Krungsri NOW already matched at 0. No row was written for:
- **Lotus's Beyond** on 2026-09-29: the statement prints fractional coins (287.5), which the ledger couldn't hold then. Its row followed on 2026-10-05 (above).
- **AEON, First Choice, Central The 1, ttb, UOB One**: their statements print no points, or the card earns none.
- **KBank LINE Points, KTC Mastercard**: no points summary or statement is on file.

Re-running `/sync-points-balance` recomputes each row and updates it in place. That matters if older rows are backfilled into a ledger later. After each new statement, a matching audit makes the new row `ok`, so no row is written.
