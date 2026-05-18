---
tags: [database, baiboon, bills]
owner: baiboon
role: bills
---

# Baiboon — Bills (`บิลเรียกเก็บค่าบัตรเครดิต`)

One row per monthly **statement** issued by a card for Baiboon's spending. This is where PDFs of statements and payment evidence are stored, and where `จ่ายแล้ว` flips per billing cycle.

- **Notion URL**: https://www.notion.so/dward2nd/192cb755f0f1804e9648e12cf2b97bbd
- **Collection ID**: `192cb755-f0f1-8064-9075-000be05ba72d`
- **Parent page**: `💳 รายการใช้จ่ายผ่านบัตรของใบบุญ` → `Personal Monetary Policy`
- **Last schema-verified**: 2026-05-19

## Properties

| Name (Notion)       | Type     | Notes |
|---------------------|----------|-------|
| (title, blank name) | title    | Free-form, e.g. `UOB Premier — Apr 2025` |
| `Card`              | **select** | **NOT a relation.** Hardcoded list of card names matching the Cards DB. See [[../concepts/known-divergences]]. |
| `วันตัดรอบบิล`        | date     | Statement cut-off date |
| `ยอดชำระ`            | number (baht) | Total amount due on the statement |
| `จ่ายแล้ว`            | checkbox | Whether the bill has been paid |
| `ใบแจ้งยอด (PDF)`     | files    | Attached PDF statement(s) |
| `หลักฐานการชำระ`      | files    | Payment evidence (transfer slips, screenshots) |
| `Note`              | text     |  |

### `Card` select options (verbatim)

`AEON Next Gen`, `AEON Primo`, `First Choice`, `Krungsri JCB`, `Krungsri NOW`, `Krungsri Visa`, `KTC UnionPay`, `Lotus's Beyond`, `SPayLater`, `ttb so smart`, `UOB Makro`, `UOB One`, `UOB Premier`, `UOB World`.

## The big divergence

The `Card` field here is a **SELECT** with a hardcoded list, not a relation to [[baiboon-cards]]. This means:

- Adding a new card requires editing the SELECT options as well as inserting a Cards row.
- A typo silently disconnects bills from cards.
- Rollups from bills back to cards do not exist (impossible without a relation).

See [[../concepts/known-divergences]]. The [[../future-app/data-model-target]] should make this a proper foreign key.

## Views

A single table view filtered to `จ่ายแล้ว = false`, sorted by `วันตัดรอบบิล` (desc) then `ยอดชำระ` (desc) — i.e. "what do I still owe, biggest first?"
