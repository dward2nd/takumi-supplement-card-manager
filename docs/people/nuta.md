---
tags: [person]
aliases: [นุตา, supplement-holder-2]
---

# Nuta (นุตา)

A friend who holds **supplement cards** on [[takumi|Takumi]]'s credit accounts. Like [[baiboon|Baiboon]], Nuta gets a per-person Notion universe; unlike Baiboon, Nuta's setup also tracks **cashback**.

See [[../concepts/supplement-card-model]] for why this exists.

## Notion presence

Three databases — the full [[../concepts/three-database-trinity]]:

- [[../databases/nuta-cards]] — `สรุปบัตรและสินเชื่อที่นุตาถือ`
- [[../databases/nuta-transactions]] — `รายการใช้จ่ายผ่านบัตรของนุตา`
- [[../databases/nuta-bills]] — `บิลเรียกเก็บค่าบัตรเครดิตของนุตา`

## Distinguishing features

- Uniquely tracks **cashback**: transactions have a `% cb` (percent cashback) number column and a `cashback` formula column. See [[../concepts/cashback]].
- No `×3` multiplier (Takumi-only); multipliers are `×0` `×2` `×4` `×5` `÷4`.
- Cards include the `ธนาคาร/บริษัท` issuer select.

## Issuers seen on Nuta's cards

Decoded from `ธนาคาร/บริษัท`: **UOB**, **Shopee**, **บัตรกรุงศรี** (Krungsri), **KTC** — same set as Baiboon.

Card products observed: see [[../cards/_stubs]]. Notably, Nuta has some cards Baiboon doesn't (e.g. `AEON UnionPay`, `CardX JCB`) and vice versa.

## Phase 2 role

Per [[../future-app/product-shape]], Nuta signs in with email + password and sees only their own data, **plus** aggregate balances and shared cycle/promo quotas on the underlying `PrimaryAccount`s. No visibility into Baiboon's transactions. Takumi (admin) can issue Nuta a password reset if needed. Nuta's cashback tracking (Nuta-only in Notion) becomes universal in the new app — cashback joins multipliers inside `Transaction.rewardRules` and any holder can carry cashback rules.
