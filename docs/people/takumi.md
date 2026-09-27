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

Both are shared with the scripts' Notion integration ("Claude Code's Automated Scripts") as of 2026-09-22, when Takumi added the Cards DS. Before that only Transactions was shared, which made every row in it read back with an empty `Card` relation — a silent access artifact, not missing data. Worth remembering as a diagnosis: an unshared target turns relations into `[]` rather than raising.

- [[../databases/takumi-bills]] — `บิลเรียกเก็บค่าบัตรเครดิตของเว็บ`, added 2026-09-27

His Bills DB is **statement-driven**: each row is the bank's total for one card — his own charges plus Baiboon's and Nuta's — because he pays the whole card to the bank. See [[../databases/takumi-bills]] for the ledger model that makes each statement line land in exactly one holder's DB.

## Distinguishing features vs supplement holders

- Transactions have a `หมวดหมู่` (category) relation that supplement holders don't. Categories themselves live in a separate Notion database (not yet fetched into this vault).
- Transactions have a `×3` multiplier checkbox in addition to the shared `×0` `×2` `×4` `×5`. See [[../concepts/points-and-multipliers]].
- Cards summary omits the `ธนาคาร/บริษัท` (bank/issuer) select that Baiboon and Nuta have. Issuer is implicit in the card name.
- Cashback tracked via `% cb` + `cashback` formula since 2026-09-28, as on Baiboon's and Nuta's DSes (older rows are empty).
- Activity was **dormant from 2025-06-11** until 2026-09-27, when Takumi restarted his ledger from his UOB and KBank (cycle 2026-08-25) and AEON (cycle 2026-09-10) statements — see [[../databases/takumi-bills]].

## Ledger reset — 2026-09-22

Takumi began a fresh record on his own cards using the [[../concepts/ledger-reset|`Reset ยอดใช้จ่ายและคะแนน`]] pattern: one transaction row per card that negates the card's running `ยอดค้างชำระ` and cancels its `คะแนนสะสม`, rather than deleting the historical rows.

All sixteen cards now carry one, and every card reads 0 balance / 0 points. Takumi wrote four by hand on 2026-09-22; the remaining ten were written through `/add-transaction` on 2026-09-23, and two of the hand-written four needed correcting (a sign slip and a self-earned-points miss — see the concept note). `SPayLater` and `KTC JCB` were already at zero and got no row. The rows are identifiable by the exact title `Reset ยอดใช้จ่ายและคะแนน`.

This was safe on Takumi's universe specifically — it was dormant, and he had no Bills DB for a reset row to leak into. (His Bills DB, added 2026-09-27, is statement-driven, so reset rows still don't reach a bill total.) The same move on [[baiboon]]'s or [[nuta]]'s live cards would erase genuinely-owed balances and corrupt the next bill draft. See the cautions in [[../concepts/ledger-reset]].

## Why the structure differs

Takumi's own setup predates the supplement-card model. Baiboon's and Nuta's databases were built later, refined the schema (added Bills, added `ธนาคาร/บริษัท`), and layered cashback tracking on top (Nuta first; Baiboon followed on 2026-05-25). The migration target in [[../future-app/data-model-target]] should reconcile these.

## Phase 2 role

Per [[../future-app/product-shape]], Takumi takes on an **admin role** in the new app. On launch, Takumi sees a cross-holder aggregated overview (own + Baiboon + Nuta), can issue password resets for the supplement holders, and receives notifications for everyone's bill / cycle / quota events.
