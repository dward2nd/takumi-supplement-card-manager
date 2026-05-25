---
tags: [person]
aliases: [ใบบุญ, supplement-holder-1]
---

# Baiboon (ใบบุญ)

A friend who holds **supplement cards** on [[takumi|Takumi]]'s credit accounts. Baiboon's spending appears on Takumi's statements but is tracked separately in Notion so Baiboon has a transparent record of *only* their own activity.

See [[../concepts/supplement-card-model]] for why this exists.

## Notion presence

Three databases — the full [[../concepts/three-database-trinity]]:

- [[../databases/baiboon-cards]] — `สรุปบัตรและสินเชื่อที่ใบบุญถือ`
- [[../databases/baiboon-transactions]] — `รายการใช้จ่ายผ่านบัตรของใบบุญ`
- [[../databases/baiboon-bills]] — `บิลเรียกเก็บค่าบัตรเครดิต`

## Distinguishing features

- Has the full trinity (Cards + Transactions + Bills), unlike [[takumi|Takumi]].
- Tracks cashback via `% cb` + `cashback` formula (added 2026-05-25, mirroring [[nuta|Nuta]]).
- No `×3` multiplier (Takumi-only); multipliers are `×0` `×2` `×4` `×5` `÷4`.
- Cards include the `ธนาคาร/บริษัท` issuer select.

## Issuers seen on Baiboon's cards

Decoded from `ธนาคาร/บริษัท` select options on the Cards DB: **UOB**, **Shopee**, **บัตรกรุงศรี** (Krungsri), **KTC**.

Card products observed: see [[../cards/_stubs]].

## Phase 2 role

Per [[../future-app/product-shape]], Baiboon signs in with email + password and sees only their own data, **plus** aggregate balances and shared cycle/promo quotas on the underlying `PrimaryAccount`s. No visibility into Nuta's transactions. Takumi (admin) can issue Baiboon a password reset if needed. Baiboon receives notifications for their own bill due-dates, cycle closings, and quota thresholds.
