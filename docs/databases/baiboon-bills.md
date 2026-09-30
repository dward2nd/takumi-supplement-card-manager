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
- **Last schema-verified**: 2026-09-30

## Properties

| Name (Notion)       | Type     | Notes |
|---------------------|----------|-------|
| (title, blank name) | title    | Free-form, e.g. `UOB Premier — Apr 2025` |
| `Card`              | relation → [[baiboon-cards]] | One-way (no back-link column on Cards). The card this bill is for. A relation since 2026-09-30; before that a SELECT. See [[../concepts/known-divergences]] #1. |
| `Card (old select)` | select   | **Legacy.** The SELECT that `Card` used to be, renamed and kept so existing views grouped/filtered by it still work. To be deleted once the views move to the relation. Scripts ignore it. |
| `วันตัดรอบบิล`        | date     | Statement cut-off date |
| `ยอดชำระ`            | number (baht) | Total amount due on the statement |
| `จ่ายแล้ว`            | checkbox | Whether the bill has been paid |
| `ใบแจ้งยอด (PDF)`     | files    | Attached PDF statement(s) |
| `หลักฐานการชำระ`      | files    | Payment evidence (transfer slips, screenshots) |
| `Note`              | text     |  |

### Legacy: `Card (old select)` options (verbatim)

`AEON Next Gen`, `AEON Primo`, `AEON World Mastercard`, `First Choice`, `KBank JCB`, `KBank PLUSTINUM`, `Krungsri JCB`, `Krungsri NOW`, `Krungsri Visa`, `KTC UnionPay`, `Lotus's Beyond`, `SPayLater`, `ttb so smart`, `UOB Makro`, `UOB One`, `UOB Premier`, `UOB World`.

17 options as of 2026-09-27, read live from the DS when the property was still `Card`. `KBank JCB` was added that day by the card's first bill. Nothing adds options any more: new bills set the relation only.

## The former divergence (resolved 2026-09-30)

Until 2026-09-30 `Card` was a **SELECT** with a hardcoded list, not a relation to [[baiboon-cards]]. A new card needed a SELECT option as well as a Cards row, a typo silently disconnected a bill from its card, and no rollup from bills back to cards was possible. `/prepare-bill` had learned to mint the option on a card's first bill.

On 2026-09-30 the user had the SELECT replaced with a one-way relation to [[baiboon-cards]]. All 109 of Baiboon's existing bills were linked, each to the Cards page its old select named (`Krungsri Visa` matched `Krungsri VISA` case-insensitively). Bill titles keep their `<Card> <YYYY-MM>` naming. See [[../concepts/known-divergences]] #1, #8 and #11.

## Views

A single table view filtered to `จ่ายแล้ว = false`, sorted by `วันตัดรอบบิล` (desc) then `ยอดชำระ` (desc) — i.e. "what do I still owe, biggest first?"
