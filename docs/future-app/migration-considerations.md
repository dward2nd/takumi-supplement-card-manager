---
tags: [future, migration]
---

# Migration considerations: Notion → custom app

When phase 2 begins, the new app **does not import** the Notion vault. Decision pinned in [[product-shape]] (interview 2026-05-21): **fresh start**. This note captures what that means in practice and what remaining work the cut-over needs.

## Strategy: fresh start

The new app launches with an empty database.

- **No bulk import** of historical Notion data.
- **Historical depth at launch**: only the in-progress (current) bill cycle is recreated by hand if needed. Anything older stays in Notion.
- **Attachments** (statement PDFs in Bills, payment-evidence photos) are **not** migrated. They remain accessible in the Notion archive.
- **Notion lifecycle**: Notion becomes a **read-only archive** after launch. No new writes; lookups still work for historical questions. No dual-write window, no live mirror.

This skips most of the integration risk a full migration would carry (rate-limited Notion exports, expiring file URLs, schema-difference reconciliation, dual-write conflict resolution). The trade-off is intentional: rebuild config at launch, accept that years of recorded rewards don't carry over.

## What gets re-entered by hand at setup

Structural data only — not transactions. Estimated ~1 evening of typing for the three-user household:

1. **People**: Takumi (เว็บ), Baiboon (ใบบุญ), Nuta (นุตา). Roles assigned per [[product-shape#Users & access model]].
2. **Issuers & networks**: UOB, KTC, Krungsri, etc. The current `ธนาคาร/บริษัท` SELECT values are the seed list.
3. **CardProducts**: each card product the household uses (e.g. UOB Premier, UOB One, KTC Forest, Krungsri Visa Platinum).
4. **PrimaryAccounts**: one per credit line, with `accountNumberHash` (a private mocked value at first — the real hash is filled in only when needed for reconciliation).
5. **Cards**: each plastic card the three holders carry, with `holderPersonId`, `productId`, `premiumTier`, `bahtPerPoint`, `pointsPerCycle`, `allocatedLimit`, last-4-digits, nickname.
6. **Per-cycle quotas**: the promotional caps that exist today (e.g. UOB One's tiers, any card-level ×5 cap). Authored once, then per-cycle progress accumulates from transactions.
7. **Categories**: seed from current Notion list (`อาหาร`, `เดินทาง`, `ออนไลน์`, `ค่าใช้จ่ายประจำ`, …). Universal across holders.
8. **Alias rules**: pattern → canonical merchant + auto-category. Authored as the user notices repeats (e.g. `contains "Agoda"` → "Agoda" + Travel). Lazy — doesn't all need to happen at launch.
9. **Bill cycle / due date patterns** per card. Used for default-filling new transactions and for cycle-close reminders.

## What gets dropped

By choosing fresh start, the household accepts losing:

- Historical transaction-level reward earnings (the `คะแนนสะสม` rollups don't carry over). Going forward, the new app's computed-rewards engine builds new totals from launch day.
- Historical bills and the paid/unpaid history of past cycles.
- Statement PDFs and payment-evidence photos (these remain in Notion archive, just not accessible from the new app).
- Notion-specific metadata: page IDs, last-edited timestamps, etc.

## What stays the same as Notion

- The **verbatim merchant-string rule** survives unchanged — every `Transaction.merchant` is stored character-for-character.
- The **four-date model** (`swipedAt` / `processedDate` / `billCycleDate` / `dueDate`) is preserved and now surfaced as first-class columns in the UI (see [[../concepts/billing-cycle]]).
- The reward-rule **semantics** carry over (×0..×5, ÷4, cashback %), but the **storage shape** changes — JSON array on Transaction instead of parallel checkbox columns (resolves [[../concepts/known-divergences|divergences #4 and #5]]).

## When does Notion go away?

It doesn't, formally. Notion stays **forever as a read-only archive**. No subscription cancellation pressure on day one — historical lookups still need it. If access becomes a problem later, the data can be exported to JSON and stored alongside the new app's backups.

## See also

- [[product-shape]] — full product spec.
- [[data-model-target]] — entity shape the structural data lands in.
- [[../concepts/known-divergences]] — which divergences are resolved by phase 2 (most of them) and which remain (none).
