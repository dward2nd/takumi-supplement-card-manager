---
tags: [concept, rewards]
---

# Point multipliers (`×0` `×2` `×3` `×4` `×5` `÷4`)

Reward points are modelled as **independent boolean multiplier columns**, not as a single number. Each transaction carries several checkbox flags that indicate which promotional rate applies, and the [[../formulas/points-realized|`คะแนนที่ได้จริง`]] formula combines them with the card's `บาทต่อ 1 คะแนน` rate to produce actual points earned.

## The set of multipliers, by person

| Multiplier | [[../people/takumi\|Takumi]] | [[../people/baiboon\|Baiboon]] | [[../people/nuta\|Nuta]] |
|------------|---------|---------|------|
| `×0`       | ✓        | ✓        | ✓     |
| `×2`       | ✓        | ✓        | ✓     |
| `×3`       | ✓        |          |       |
| `×4`       | ✓        | ✓        | ✓     |
| `×5`       | ✓        | ✓        | ✓     |
| `÷4`       |          | ✓        | ✓     |

So Takumi's transactions support `×3` but not `÷4`; supplement holders' transactions support `÷4` but not `×3`.

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
- `คะแนนสะสม` rolls up `คะแนนที่ได้จริง` across transactions.
- `ให้คะแนนตามรอบบิล` is a per-card checkbox: true if the bank awards points per billing cycle rather than per transaction (changes when "realized" happens).

## Approximation caveat

The `×0/×2/×3/×4/×5/÷4` set is **not** the issuer's real earning rule — it's a **convenience approximation** chosen to be fast to click in Notion's fixed-checkbox UI and to cover the common Thai-credit-card promotional shapes. Real earning rules can be richer:

- **Fractional points** (a transaction earns `0.25 pts` per 50 ฿, not an integer multiple of a base rate). The Notion checkbox enum literally cannot express this. See [[../cards/lotuss-beyond]].
- **Per-merchant bonus tiers within a card** — the issuer awards different rates depending on the merchant string, not just on whether a promo checkbox is set. See [[../cards/lotuss-beyond]] (general vs at-Lotus) and [[../cards/uob-makro]] (general vs in-store Makro, with the `÷4` checkbox standing in for "this was an in-store-Makro swipe").
- **Conditional fall-back via the merchant string** — UOB Makro's `÷4` only applies when the transaction was physically read by Makro's in-store reader. TrueMoney intermediation (`TMN*…`) breaks that condition and reverts to the base rate. The checkbox alone doesn't encode the "TrueMoney breaks it" rule; the human entering the row has to know.

So the multiplier set is a **lossy projection** of the underlying rules. Where the gap matters, the per-card narrative note is the source of truth (`docs/cards/<card>.md`), not the Notion checkbox. The phase-2 app models the underlying rules directly as `RewardRule` JSON entries on `Transaction` — see [[../future-app/data-model-target]] and [[promotions]].

## Programme quirks the ledger lives with (2026-09-28)

- **Rounding.** UOB rounds per statement line, like the ledger formula. KBank, KTC and Krungsri round once on the cycle's spend, so the ledger runs short each cycle. The difference goes on a `[ปรับคะแนน] ปัดเศษคะแนนรอบบิล YYYY-MM` row in the principal holder's ledger; `/record-statement` adds it (user). A charge split into `[บัตรหลัก]` shares loses points the same way: `[ปรับคะแนน] <line>` rows, also on the principal holder's ledger.
- **Bonus points and redemptions outside a card.** KBank prints `BONUS POINTS` per product (Shopee +800 in Aug 2026, PLUSTINUM +1,000 in Sep 2026); these are recorded as `[คะแนนพิเศษ] KBank BONUS POINTS` rows. A `CASH REBATE` redemption can draw on bonus points that belong to no card; only the part a card pays shows on it (PLUSTINUM −69, `แลกคะแนน CASH REBATE 69 คะแนน`).
- **Lotus's coins are fractional**: 0.25 coin per ฿50, or 1.5 coins per ฿50 at Lotus's (user). The household's points are whole numbers everywhere and stay that way, so Lotus's coins aren't audited.
- **Krungsri Lady and Krungsri JCB** earn no points at petrol stations (the Thai-petrol campaign; `KrungsriPetrolCampaign`).
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

KBank JCB, Krungsri Lady and Krungsri NOW already matched at 0. No row was written for:
- **Lotus's Beyond**: the statement prints fractional coins (287.5), which the ledger's whole points can't hold.
- **AEON, First Choice, Central The 1, ttb, UOB One**: their statements print no points, or the card earns none.
- **KBank LINE Points, KTC Mastercard**: no points summary or statement is on file.

Re-running `/sync-points-balance` recomputes each row and updates it in place. That matters if older rows are backfilled into a ledger later. After each new statement, a matching audit makes the new row `ok`, so no row is written.
