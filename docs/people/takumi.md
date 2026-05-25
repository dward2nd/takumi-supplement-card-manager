---
tags: [person]
aliases: [เว็บ, web, primary-cardholder]
---

# Takumi (เว็บ)

The primary cardholder. Every credit card in this system is issued to Takumi by the bank; [[baiboon]] and [[nuta]] hold *supplement* cards on Takumi's accounts and share his credit limit. See [[../concepts/supplement-card-model]] for the motivation.

## Notion presence

Two databases under parent page **Personal Monetary Policy**:

- [[../databases/takumi-cards]] — `สรุปบัตรและสินเชื่อของเว็บ`
- [[../databases/takumi-transactions]] — `รายการใช้จ่ายผ่านบัตรของเว็บ`

There is **no Bills database** for Takumi — unlike Baiboon and Nuta. See [[../concepts/known-divergences]]. (**Phase 2**: this asymmetry disappears — Takumi gains a symmetric Bills view in the new app per [[../future-app/product-shape#Bills & reconciliation]].)

## Distinguishing features vs supplement holders

- Transactions have a `หมวดหมู่` (category) relation that supplement holders don't. Categories themselves live in a separate Notion database (not yet fetched into this vault).
- Transactions have a `×3` multiplier checkbox in addition to the shared `×0` `×2` `×4` `×5`. See [[../concepts/points-and-multipliers]].
- Cards summary omits the `ธนาคาร/บริษัท` (bank/issuer) select that Baiboon and Nuta have. Issuer is implicit in the card name.
- No cashback model (no `% cb`, no `cashback` formula) — unlike Baiboon and Nuta.
- Activity has reportedly been **discontinued for some time**, so live data may be stale relative to the schema documented here.

## Why the structure differs

Takumi's own setup predates the supplement-card model. Baiboon's and Nuta's databases were built later, refined the schema (added Bills, added `ธนาคาร/บริษัท`), and layered cashback tracking on top (Nuta first; Baiboon followed on 2026-05-25). The migration target in [[../future-app/data-model-target]] should reconcile these.

## Phase 2 role

Per [[../future-app/product-shape]], Takumi takes on an **admin role** in the new app. On launch, Takumi sees a cross-holder aggregated overview (own + Baiboon + Nuta), can issue password resets for the supplement holders, and receives notifications for everyone's bill / cycle / quota events.
