---
tags: [formula]
---

# `ยอดค้างชำระ` — outstanding balance (per card)

A formula property on every Cards DB. The card's running balance: everything ever charged, minus everything ever paid.

> **Phase 2**: this Notion formula is replaced by application code in the new app — see [[../future-app/product-shape#Rewards & computation]]. The body below is retained for reference and as a one-time decode target during phase-2 setup of the outstanding-balance engine.

## Where to find the body

- Takumi: `formulaCode://1aacb755-f0f1-818a-a284-000b17d155de/OjtEcQ`
- Baiboon: `formulaCode://99bb5ba6-79b1-47e2-9b8f-fa3102d5b294/OjtEcQ`
- Nuta: `formulaCode://2a1cb755-f0f1-8188-9b00-000b5fa448b8/OjtEcQ`

Read them through the Notion HTTP API instead — `GET /v1/data_sources/{id}` returns every formula's `expression` inline.

## Decoded body

**Verified 2026-09-22** on Baiboon's and Nuta's Cards data sources; both are byte-identical:

```
sum(prop("ยอดค้างชำระ rollup"))
```

…where `ยอดค้างชำระ rollup` is a `sum` rollup of `ยอดชำระ` over the card's entire transaction relation:

| | |
|---|---|
| `function` | `sum` |
| `rollup_property_name` | `ยอดชำระ` |
| `relation_property_name` | `รายการใช้จ่ายผ่านบัตรของใบบุญ` (see [[../concepts/known-divergences#6. Cards-DB property labels lag]]) |

Takumi's copy could not be verified — his Cards data source is not shared with the scripts' Notion integration, so the API cannot see it. Assume it matches until proven otherwise.

## The formula is a no-op wrapper

`sum()` over a single number returns that number. `ยอดค้างชำระ` is therefore *exactly* `ยอดค้างชำระ rollup`, and the two columns always agree. The `sum()` is presumably there to coerce the rollup into a number for sorting.

The earlier hypothesis in this note — that the formula refines the rollup by filtering on `ชำระแล้ว` or excluding `Credit Return` — **is wrong**. There is no filter of any kind.

## Consequences worth internalising

- **`ชำระแล้ว` does not affect the balance.** The paid checkbox is lifecycle metadata for [[../concepts/payment-lifecycle]] and for bill reconciliation. It is invisible to this formula. A card whose rows are all ticked `ชำระแล้ว` still shows the full balance if no payment rows were entered.
- **The balance nets to zero only because payments are entered as negative rows.** This is why [[../databases/baiboon-transactions|the ledger]] carries `ชำระบิลเต็มจำนวน`-style negative transactions — see `/record-payment`. Without them the number only ever grows.
- **`Credit Return` rows still count.** A refunded charge keeps contributing its `ยอดชำระ` to the balance; the offsetting refund must be its own negative row.
- **A negative balance is meaningful**, not an error: it means the card is overpaid (a credit sitting with the bank). `/summarize-overview` deliberately keeps negative rows while hiding zero rows.
- **Any row on the card moves the balance**, regardless of date, cycle, or paid state. That is what makes [[../concepts/ledger-reset]] possible — and what makes it dangerous to run on a card with live debt.

## Used by views

The Cards DB tables sort by `ยอดค้างชำระ` descending — "what's the biggest open balance right now?" is the primary at-a-glance question.
