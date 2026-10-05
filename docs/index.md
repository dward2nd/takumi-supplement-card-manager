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
- [[databases/takumi-bills]] — บิลเรียกเก็บค่าบัตรเครดิตของเว็บ (statement-driven)

### Baiboon's

- [[databases/baiboon-cards]] — สรุปบัตรและสินเชื่อที่ใบบุญถือ
- [[databases/baiboon-transactions]] — รายการใช้จ่ายผ่านบัตรของใบบุญ
- [[databases/baiboon-bills]] — บิลเรียกเก็บค่าบัตรเครดิต

### Nuta's

- [[databases/nuta-cards]] — สรุปบัตรและสินเชื่อที่นุตาถือ
- [[databases/nuta-transactions]] — รายการใช้จ่ายผ่านบัตรของนุตา
- [[databases/nuta-bills]] — บิลเรียกเก็บค่าบัตรเครดิตของนุตา

### Household-wide

- [[databases/promotion-bureau]] — Promotion Bureau: one row per pooled-campaign period, linked to everyone's transactions
- [[databases/promotion-catalogues]] — Promotion Catalogues: a Thai reading page per merchant per month (every promotion + a spending plan), gallery with logo covers
  - [[catalogues/index]] — the research behind it: monthly reports, campaign lineage (predecessor → successor), how each site can be read
- [[databases/cashback-trackers]] — รายการติดตามเครดิตเงินคืนของ<name>: one per holder, a row per expected credit

## Concepts (cross-cutting)

- [[concepts/supplement-card-model]] — why this whole system exists
- [[concepts/three-database-trinity]] — `Cards` ⟷ `Transactions` + `Bills` per holder
- [[concepts/payment-lifecycle]] — `Processed` → `ชำระแล้ว` → `Credit Return`
- [[concepts/billing-cycle]] — four date axes on every transaction
- [[concepts/points-and-multipliers]] — `×0` `×2` `×3` `×4` `×5` `÷4`
- [[concepts/cashback]] — `% cb` on Baiboon and Nuta (not Takumi)
- [[concepts/promotions]] — cashback is promotion-driven; effective dates, tier rules, and how general rules (foreign-in-THB, etc.) interact with promos
- [[concepts/promotion-bureau]] — campaigns paid on pooled spend: one Bureau row per quota period, one class per payout shape and per campaign, first-come-first-served split
- [[concepts/installment-reward-campaigns]] — ดีจังผ่อน / U Plan and why an installment plan's rewards can't be read off the merchant string
- [[concepts/premium-tier]] — Signature / Platinum / none
- [[concepts/card-network]] — JCB / Mastercard / VISA / UnionPay
- [[concepts/ledger-reset]] — `Reset ยอดใช้จ่ายและคะแนน`: zeroing a card's balance and points without deleting history
- [[concepts/known-divergences]] — schema inconsistencies worth knowing
- [[concepts/page-icons]] — every script-created row gets an emoji page icon: row kind, then merchant category; bills show 📝 draft / 🧾 final; Cards DBs untouched

## Formulas

Notion stores formula bodies behind `formulaCode://` URLs. These notes decode them on demand.

- [[formulas/points-realized]] — `คะแนนที่ได้จริง`
- [[formulas/points-unrealized]] — `คะแนน unrealized`
- [[formulas/outstanding-balance]] — `ยอดค้างชำระ`
- [[formulas/cashback]] — `cashback` (Baiboon + Nuta, not Takumi)

## Cards

- [[cards/_stubs]] — list of all card products observed in the Cards DBs and the Bills' legacy `Card (old select)` options; individual notes are promoted lazily as we discuss each card's rules.

## Promotions

- [[promotions/uob-one-2026]] — UOB One 2026 cashback promotion (effective `2026-01-01` → `2026-12-31`).
- [[promotions/first-choice-nw3]] — First Choice NW3 pooled cashback ladder (`2026-07-01` → `2026-09-30`), tracked in the Promotion Bureau.
- [[promotions/uob-epw538]] — UOB e-Commerce & e-Wallet EPW538 (`2026-07-01` → `2026-09-30`) and its Q4 successor SPW796, pooled across every UOB card, tracked in the Promotion Bureau.
- [[promotions/uob-spw592]] — UOB supermarkets SPW592 (฿50 / ฿150 a month, Jul–Dec 2026; UOB Makro excluded); modelled, not registered.
- [[promotions/first-choice-2026h2]] — First Choice ON3, DLV3, IS3 and the BTS lucky-draw rights (Krungsri VISA + First Choice); Q4 2026's NW4, ON4 and IS4; in the Promotion Bureau.
- [[promotions/first-choice-privilege-2026]] — First Choice BLUE PLUS status: ฿400,000 accumulated over calendar 2026, primary + supplements; how to count it from the statements, and the 2026-10-01 reckoning.
- [[promotions/krungsri-card-2026]] — Krungsri Card ONQ3, SUP1, PTT2, EAT, Bangchak/BC3P (BXP and Bangchak700 from Oct 2026), LOTA/LOTB, J Dining and NOW online, one Bureau row per card account.
- [[promotions/lotuss-lbs3]] — Lotus's LBS3 big-ticket cashback (Sep–Dec 2026).
- [[promotions/aeon-2026]] — AEON Rabbit 5%, AEON World 5% supermarkets, Everyday with AEON (NTW1), AEON UnionPay 3%, per AEON cycle.
- [[promotions/ttb-2026]] — ttb so smart 1% (฿2,000 a cycle), and ttb's Caltex, Bangchak, hypermarket (BMG → BGO) and MUJI campaigns.
- [[promotions/uniqlo-2026]] — UNIQLO per slip, Oct 2026 – Feb 2027: UOB UNO, Krungsri UNQ, KBank UQN (per card), ttb UQCB, CardX UQC; KTC's and Krungsri JCB's bonus points.
- [[promotions/kbank-makro]] — KBank MKR at Makro (฿100/240 a month, +฿1,500 per ฿300,000), Oct–Dec 2026, one Bureau row per KBank card.
- [[promotions/uob-makro-gold-mission]] — UOB Makro 26th "Gold Mission" `UMK26` (Makro stores monthly, Makro PRO app per slip, other spend ฿300 a month), Oct–Dec 2026.
- [[promotions/cardx-hypermarket]] — CardX HY1 per hypermarket slip (฿40/200/720, ฿1,440 a month) and HYP ฿3,000 at ฿300,000, Oct–Dec 2026.
- [[promotions/unionpay-qr]] — UnionPay QR 6% off on KTC UnionPay (monthly from Sep 2026), taken off the charge itself; one Bureau row per card number, `Quotas Exceeded Date` when UnionPay's pool runs out.

## Future application

Stack-agnostic target model for phase 2 (Notion-replacement app).

- [[future-app/data-model-target]]
- [[future-app/migration-considerations]]

## Conventions

- Filenames are kebab-case English; narrative is English; Thai field names are preserved verbatim in backticks, glossed in English on first use per note.
- Every note carries at least one tag: `#person`, `#database`, `#concept`, `#formula`, `#future`, `#moc`, `#card`.
- Wikilinks use the `[[folder/note]]` form so they survive folder moves.
- Notion URLs at the top of each DB note are the canonical reference. The schema in this vault can drift; always verify against Notion before quoting specifics.
