---
tags: [concept, rewards]
---

# Cashback model

[[../people/baiboon|Baiboon]]'s and [[../people/nuta|Nuta]]'s transactions track cashback. Two fields are involved:

| Field      | Type                       | Where |
|------------|----------------------------|-------|
| `% cb`     | number (percent) | [[../databases/baiboon-transactions]], [[../databases/nuta-transactions]] |
| `cashback` | formula = `% cb` × `ยอดชำระ` | [[../databases/baiboon-transactions]], [[../databases/nuta-transactions]] |

[[../people/takumi|Takumi]]'s Transactions DS does not have these fields. The decoded formula body lives in [[../formulas/cashback]].

## Cashback values come from promotions

The `% cb` value on a transaction is the *output* of applying an active **promotion** to that transaction — not a permanent property of the card. The card's note links to the currently-active promo, which defines tier rules, merchant exclusions, installment treatment, and the cashback-crediting workflow. See [[promotions]] for the cross-cutting model and per-card promotion notes under [[../promotions/]].

When a row earns no cashback (no active promo, or the active promo excludes the row), **leave `% cb` unset** — never write an explicit `0`. Use `Note` to record the reason when it's beyond the card/promo's headline rule (foreign-in-THB, petrol-on-UOB, primary-card-swipe, etc.).

## Two ways cashback is recorded

`% cb` on the spend row is only one of the two recording conventions in the data:

1. **`% cb` on the spend row** — the `cashback` formula derives the baht. Works when the rate is a flat percentage of that single transaction. This is the default, and it's what `auto_classify` writes.
2. **A separate negative-amount credit row** — a distinct transaction whose `ยอดชำระ` is the credited baht. Needed whenever the credit can't be expressed as a percentage of one row: Krungsri NOW's block math (25 THB per complete 500 THB of online spend) under a ฿300/calendar-month cap, recorded per `scripts/repositories/cards/krungsri-now.yaml`; and the [[../promotions/uob-one-2026|UOB One]] per-tier credits that the bank posts on a later statement. Rows recorded this way leave `% cb` unset.

Credit rows in convention 2 follow one of two naming shapes, both of which downstream tooling has to recognize:

| Shape | Examples | Seen on |
|-------|----------|---------|
| `CASHBACK` in the name | `Cashback 5%`, `UOB ONE CASHBACK 10%`, `NW2 Cashback 2% (1 พ.ค. - 31 พ.ค.)`, `[บัตรหลัก][Cashback] …` | UOB, AEON, First Choice |
| `CB` prefix + credited merchant / campaign code | `CB TMN FAST FOOD BANGKOK THA`, `CB HTTPS://WWW.MAKRO.PRO/ BANGKOK TH`, `CB-025 SHELL-CALTEX NOV 2025`, `CB15_ SUP1 CAMPAIGN 1AUG26-31AUG26` | Krungsri NOW, several of Takumi's cards |

Both shapes are always **negative**. The separator after `CB` varies — space, hyphen before a batch number, or a digit opening a campaign code — so a `CB `-with-space test under-matches. `lib/bills.py:_is_cashback_row` is the shared predicate; `lib/payments.py:is_bill_payment_row` relies on the same fact to keep credits counted in a bill's `ยอดชำระ` while excluding `ชำระ…`/`จ่าย…` payment rows (see [[payment-lifecycle]]).

Both conventions leave the credit **inside** the bill total — cashback reduces what's owed. Only bill *payments* are excluded from `ยอดชำระ`.

## Why Takumi doesn't have this (yet)

Takumi's setup predates the supplement-card model. Nuta's DS introduced cashback tracking; Baiboon's DS was extended to match on 2026-05-25. Takumi's can be cloned the same way if it ever needs it — both columns are additive (don't affect existing rows when added).

## Migration consideration

In the [[../future-app/data-model-target|future app]], cashback and points should likely be modelled as polymorphic "rewards" per transaction rather than as parallel column families.

## Phase 2 model (resolved 2026-05-21)

Confirmed in [[../future-app/product-shape]]:

- Cashback becomes universal — it joins multipliers inside `Transaction.rewardRules` (a JSON array on `Transaction`). Any holder's transaction (including Takumi's) can carry `{type: "cashback", percent: 5}` alongside or instead of a multiplier. (Baiboon and Nuta already track cashback in Notion as of 2026-05-25; phase 2 closes the gap for Takumi.)
- The cashback `formula` field disappears — the new app **computes** the cashback baht in code on read, replacing the Notion formula (see [[../formulas/cashback]] for the historical formula body).
- **Auto-classify with override** — per-card cashback-tier rules (e.g. UOB One's 10% / 5% / 1%) get applied automatically when a transaction is added, based on the merchant string. The user can override per row when the auto-tier is wrong.
