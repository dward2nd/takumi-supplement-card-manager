---
tags: [moc]
---

# Personal Monetary Policy — knowledge vault

This is the map of content (MOC) for the `takumi-supplement-card-manager` documentation vault. Open the `docs/` folder as an Obsidian vault for the graph view; click any link below to enter the network.

> **What lives here**: the structure of Takumi's Notion workspace for managing his own credit cards and the supplement cards he issues to [[people/baiboon|Baiboon]] and [[people/nuta|Nuta]]. Notion holds the data; this vault explains the *shape* of the data and the *why* behind the modelling choices.

## People

- [[people/takumi]] — primary cardholder (Notion name: **เว็บ**)
- [[people/baiboon]] — supplement holder (**ใบบุญ**)
- [[people/nuta]] — supplement holder (**นุตา**)

## Databases (8)

Each note opens with a live Notion URL, collection ID, and the full property schema.

### Takumi's

- [[databases/takumi-cards]] — สรุปบัตรและสินเชื่อของเว็บ
- [[databases/takumi-transactions]] — รายการใช้จ่ายผ่านบัตรของเว็บ

### Baiboon's

- [[databases/baiboon-cards]] — สรุปบัตรและสินเชื่อที่ใบบุญถือ
- [[databases/baiboon-transactions]] — รายการใช้จ่ายผ่านบัตรของใบบุญ
- [[databases/baiboon-bills]] — บิลเรียกเก็บค่าบัตรเครดิต

### Nuta's

- [[databases/nuta-cards]] — สรุปบัตรและสินเชื่อที่นุตาถือ
- [[databases/nuta-transactions]] — รายการใช้จ่ายผ่านบัตรของนุตา
- [[databases/nuta-bills]] — บิลเรียกเก็บค่าบัตรเครดิตของนุตา

## Concepts (cross-cutting)

- [[concepts/supplement-card-model]] — why this whole system exists
- [[concepts/three-database-trinity]] — `Cards` ⟷ `Transactions` + `Bills` per holder
- [[concepts/payment-lifecycle]] — `Processed` → `ชำระแล้ว` → `Credit Return`
- [[concepts/billing-cycle]] — four date axes on every transaction
- [[concepts/points-and-multipliers]] — `×0` `×2` `×3` `×4` `×5` `÷4`
- [[concepts/cashback]] — `% cb` on Baiboon and Nuta (not Takumi)
- [[concepts/premium-tier]] — Signature / Platinum / none
- [[concepts/card-network]] — JCB / Mastercard / VISA / UnionPay
- [[concepts/known-divergences]] — schema inconsistencies worth knowing

## Formulas

Notion stores formula bodies behind `formulaCode://` URLs. These notes decode them on demand.

- [[formulas/points-realized]] — `คะแนนที่ได้จริง`
- [[formulas/points-unrealized]] — `คะแนน unrealized`
- [[formulas/outstanding-balance]] — `ยอดค้างชำระ`
- [[formulas/cashback]] — `cashback` (Baiboon + Nuta, not Takumi)

## Cards

- [[cards/_stubs]] — list of all card products observed in SELECT options; individual notes are promoted lazily as we discuss each card's rules.

## Future application

Stack-agnostic target model for phase 2 (Notion-replacement app).

- [[future-app/data-model-target]]
- [[future-app/migration-considerations]]

## Conventions

- Filenames are kebab-case English; narrative is English; Thai field names are preserved verbatim in backticks, glossed in English on first use per note.
- Every note carries at least one tag: `#person`, `#database`, `#concept`, `#formula`, `#future`, `#moc`, `#card`.
- Wikilinks use the `[[folder/note]]` form so they survive folder moves.
- Notion URLs at the top of each DB note are the canonical reference. The schema in this vault can drift; always verify against Notion before quoting specifics.
