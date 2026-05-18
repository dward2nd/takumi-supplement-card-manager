---
tags: [concept, foundational]
---

# The supplement-card model — why this whole system exists

[[../people/takumi|Takumi]] holds primary credit-card accounts. From those accounts he issues **supplement cards** — additional physical cards on the same underlying account — to two friends: [[../people/baiboon|Baiboon]] and [[../people/nuta|Nuta]].

Supplement-card spending is invisible to the friend's own credit history but fully visible to Takumi's: the bank bills Takumi for all of it. The credit limit is shared. There's no per-supplement-cardholder statement from the bank.

## The problem

Without active record-keeping:

- Baiboon doesn't know how much they've spent until Takumi tells them — opaque.
- Takumi has to manually reconcile bank statements per cardholder before invoicing — error-prone.
- A typo or memory lapse damages trust.

## The solution Takumi built

A per-cardholder Notion universe. Each of [[../people/baiboon|Baiboon]] and [[../people/nuta|Nuta]] gets the [[three-database-trinity]]:

1. `Cards` — what supplement cards exist, with bank, network, points rate, credit limit.
2. `Transactions` — every individual swipe.
3. `Bills` — the monthly statement amount per card.

Each cardholder can be invited to *their* Notion page and see *only* their own data.

## Invariants

- One person, one Cards DB, one Transactions DB, optionally one Bills DB.
- A Card row lives in exactly one person's Cards DB.
- A Transaction row references its Card by relation. (Bills break this — they use a `Card` select. See [[known-divergences]].)
- Credit limit (`วงเงินที่ได้`) on a supplement Card row is the *holder's* allocated share of Takumi's underlying limit, not the full account limit.

## What this means for [[../future-app/data-model-target|the future app]]

The app needs first-class **person** entities, per-person scoping/authorization, and a clear mapping from supplement-card → underlying primary-card-account. The current Notion structure lacks an explicit "primary account" entity — that's a gap to close in phase 2.
