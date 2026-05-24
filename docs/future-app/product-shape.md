---
tags: [future, product, spec]
---

# Phase-2 product shape (interview-derived)

The future application that will replace the Notion vault. This note encodes the design decisions reached in a structured interview with Takumi on 2026-05-21. Pairs with [[data-model-target]] (entity shape) and [[migration-considerations]] (cut-over).

**Guiding constraint** (applies to every decision below): minimal setup, ~3 users only. Bias toward simplicity over scale. No feature exists "for completeness" — every line of code has to earn its keep against three users.

## Users & access model

- **Three people, each with their own account**: Takumi (เว็บ), Baiboon (ใบบุญ), Nuta (นุตา).
- **Takumi has an admin role**: when logged in, sees every holder's data (own + Baiboon + Nuta). Defaults to a **cross-holder aggregated overview** on launch — drill into individual holders from there.
- **Supplement holders see only their own data, plus**:
  - **Aggregate balances** on shared `PrimaryAccount`s (e.g. "UOB account: ฿150,000 / ฿300,000 used across all cards").
  - **Shared cycle quotas for promotions** — when a per-account promo has a household-wide quota (e.g. "×5 promo capped at ฿10,000/cycle across the whole UOB account"), supplement holders can see the shared remaining quota. This is why quotas live at `PrimaryAccount` level, not just per-`Card` — see [[data-model-target]].
- No supplement-to-supplement visibility into transaction-level data.

## Platform

- **Mobile-first PWA**. Installable to home screen on iOS / Android. Desktop browser works as a secondary surface.
- **Online with offline cache**: server is the source of truth; client caches recent data so the app stays usable on flaky connections. Conflicts resolved server-side.
- **Fully synced multi-device**: same account on phone + laptop. A transaction added on phone shows on laptop. Implies a real backend.
- **Self-hosted on a VPS**. Single instance. Notion gets archived; one bill to run the new app.

## Daily-use workflow

The app is opened **daily as a spend journal**. The defining workflow is "record a transaction the day it happens", optimized to be as fast as possible.

### Home screen

Action-first. Big **Add transaction** button at the top of the home screen with recent transactions in a feed below. The aggregated overview content (for Takumi) sits under the action button.

### Transaction entry

Three distinct flows feed into one mini-table entry surface:

1. **New merchant** — user types the merchant string **verbatim** (character-for-character, no normalization, no abbreviation expansion). Same hard rule as [[../../.claude/skills/add-transaction/SKILL.md|/add-transaction]] Rule 1.
2. **Alias-matched** — if the typed string matches a saved alias rule (e.g. `contains "Agoda"` → canonical merchant "Agoda" + category "Travel"), the alias auto-fills the canonical name and category. The original verbatim string is still stored.
3. **Tap-to-reuse** — pick an existing merchant from history; the app autofills merchant + card + bill cycle + due date + category. Only the amount needs editing.

**Bulk-primary** entry surface: the entry UI is a mini-table where the user can add multiple rows at once. Single entries use the same UI with one row.

### Merchant string rules

- **Verbatim is the default**: store the exact string the user typed/pasted.
- **Alias rules** are a separate concept: pattern (e.g. `contains "Agoda"` or exact-match) → canonical merchant + auto-category. Multiple aliases can collapse to one canonical merchant.
- **No on-entry normalization**: even if the user has an alias rule, the original verbatim string is preserved alongside the canonical alias.

## Data model decisions (resolves open questions in [[data-model-target]])

### `PrimaryAccount` exposure

- **Visible as its own surface** in the UI. A dedicated view shows each credit line (UOB / KTC / Krungsri), its total credit limit, total outstanding across all cards on it, and the cards attached.
- Supplement holders see only the aggregate-balance and shared-quota slice.
- New field on `PrimaryAccount`: `accountNumberHash` (stored, not displayed).

### `RewardRule` shape

- **JSON column on `Transaction`** — embedded array. Closer to current POC; simpler queries on whole transactions; JSON operators for "which transactions earned cashback".

### Per-cycle quotas

- **First-class on `Card` AND on `PrimaryAccount`**. Some promotions cap at the card level (e.g. "this card's ×5 up to ฿10,000/cycle"), others at the account level (e.g. "UOB account's ×5 quota: ฿10,000/cycle total across all cards on this account"). Model supports both.
- The app applies quota rules when classifying transactions into reward tiers.

### Credit Return / refunds

- **Both: adjustment row + status update**.
  - A refund creates a new negative-amount `Transaction` row (the "adjustment row").
  - The original transaction's status flips to `refunded`.
- **Cross-cycle refunds**: when the refund posts in a bill cycle *after* the original transaction's cycle, the adjustment row is credited to the **next** bill as advance payment — banks commonly handle it this way and the user expects to pre-pay (or net it against) the following cycle's charges. Model needs to express "adjustment applies to bill cycle X".

### `Transaction.status` enum

- `pending` → `processed` → `paid`, or terminal `refunded`. State transitions per [[../concepts/payment-lifecycle]].

### `Transaction` dates

- Four independent dates: `swipedAt` (when the user paid), `processedDate` (when the bank posted; null while pending), `billCycleDate` (which cycle the bank assigned it to), `dueDate` (when the resulting bill is due).
- Cross-cycle nuance above means `billCycleDate` on an adjustment row can be later than the swipe — that's correct.

## Rewards & computation

- **App computes realized points / cashback** per transaction. Replaces every Notion formula in `docs/formulas/` ([[../formulas/points-realized]], [[../formulas/points-unrealized]], [[../formulas/outstanding-balance]], [[../formulas/cashback]]). The new app is the source of truth for earned rewards.
- **Auto-classify merchant tiers with manual override**: per-card tier rules (e.g. UOB One: 10% / 5% / 1% with carve-outs for `TMN 7-11` ≠ `7-11`) get applied automatically on entry. User can override per row when the auto-classification is wrong.
- **Per-card cycle progress** is a first-class UI surface: progress bars showing quota consumption (e.g. "×5 promo: ฿7,200 / ฿10,000 used this cycle"). For shared-account quotas, the progress bar reflects household-wide usage.
- **No "best card for this merchant" / "missed earnings" advice** — explicitly out of scope. The app is a ledger + reward calculator, not an advisor.

## Categories

- **Universal across all three holders** (one shared category list). Initial seed: current Notion categories (`อาหาร`, `เดินทาง`, `ออนไลน์`, `ค่าใช้จ่ายประจำ`, …).
- **User-defined free-form** — no hierarchy. Users add categories as they need them.
- **Required on every transaction**, with an `Other / Uncategorized` fallback when no alias matches and the user doesn't pick one.
- **Single category per transaction** — no multi-tagging.
- **Alias rules can auto-set category** (see *Transaction entry* above).

## Bills & reconciliation

- **Bills are independent rows** (not derived) — same model as current Notion ([[../databases/baiboon-bills|Baiboon Bills]] / [[../databases/nuta-bills|Nuta Bills]]). Resolves [[../concepts/known-divergences|divergence #1]]: `Bill.cardId` is a real FK in the new app, not a SELECT.
- **Reconciliation hint surfaced in UI**: per bill, show `sum(transactions on this cycle) vs. bill.amountBaht` and the delta. When non-zero, prompt the user to **either**:
  - Add an adjustment row (legit bank fee / interest the user didn't record), **or**
  - Review the transactions (most common case is the user missed or duplicated something — based on Takumi's real experience).
- **Statement file** (bank PDF): optional attachment, archival-only. No OCR.
- **Payment evidence** (transfer slip photo): optional. Marking a bill paid doesn't require evidence.
- **Bills exist for all three holders in the new app** — closes [[../concepts/known-divergences|the "Takumi has no Bills DB" divergence]] since the new model treats every cardholder symmetrically.

## Notifications

### Types

- **Bill due-date reminders** — per-holder; Takumi gets reminders for every bill.
- **Bill cycle closing soon** — N days before each card's cycle date, so the user can record any lingering transactions.
- **Quota-threshold alerts** — when a per-card or per-account quota crosses a configurable threshold (default 80%).
- **Reconciliation mismatches** are **in-app only** (chip on the bill), not pushed externally.

### Channels (all supported)

- In-app banner / badge.
- Web Push (PWA) — primary mobile channel.
- Email — for digest-style updates.
- Line / Telegram bot — common in Thailand, more reliable than web push on iOS.

User can disable per channel; types are fixed.

### Default lead times

- **7 days** + **3 days** before each bill due date (two-stage).
- **1 day** before each bill cycle close.

### Cross-holder

Takumi gets notifications for **all three** holders' events. Supplement holders only get their own.

## Migration from Notion

- **Fresh start**: the new app launches with an empty database. No bulk import.
- **Historical depth**: only the current (in-progress) bill cycle is recreated by hand if needed. Older history stays in Notion.
- **Attachments**: not migrated. Existing statement PDFs and slip photos remain in Notion.
- **Notion lifecycle**: Notion becomes a **read-only archive** after launch. No new writes to Notion; lookups still work for historical questions.
- **Selective re-entry**: structural data (the alias rules, category seed, due-date / cycle-date patterns per card) is re-typed into the new app at setup time. Faster than building an importer for ~3 users' worth of data.

## Privacy & data hygiene

### What the app stores about cards

- **Last 4 digits + nickname** per card. Never the full PAN.
- Card product, network, issuer, premium tier — same as today.

### What the app refuses to store

Pattern-rejected on input (the field shakes off the entry with a warning):

- **Full card numbers (PAN)** — 13–19 digit sequences matching credit-card formats.
- **CVV / PIN** — 3- or 4-digit codes when the field context implies card-data entry.
- **Government ID numbers** — Thai national ID (13-digit pattern), passport numbers.

Outside these three patterns: trust the user. No further input filtering.

### Currency / locale

- **THB-only display** for amounts and balances.
- **Foreign currency captured** per transaction: when the underlying charge was in another currency (overseas travel), the app stores the original currency code + amount alongside the THB billed amount. Useful for travel reporting and disputes.

## Authentication & sessions

- **Email + password** as the sign-in method.
- **Account recovery**: both self-serve email reset **and** Takumi can issue a reset for Baiboon / Nuta from his admin view.
- **Multi-device fully synced** — same email/password works on phone + laptop + tablet, all sharing the same data.
- **Data export** — three formats:
  - **CSV** export of transactions / bills (per-holder or all, depending on the logged-in user's role).
  - **Full JSON dump** of everything the user owns.
  - **PDF statement-like** export per bill cycle (transactions + reward calc + bill amount).

## Audit log

- **Mutations only** (writes): every create / update / delete records who, when, what fields changed.
- No read-event logging.
- Surfaced primarily to Takumi (admin) as a trust-building feature — Baiboon / Nuta can see "Takumi edited my transaction t-203 on 2026-05-15".

## Theming

- **Both light and dark**, manually selectable.
- **System preference is the default** when the user hasn't picked one.
- Standard PWA pattern (`prefers-color-scheme` for default, explicit toggle in settings).

## Recurring transactions

- **Rules auto-create draft transactions**.
- User defines a rule (e.g. "Netflix ฿349 on UOB One on the 12th of each month", "ค่าน้ำประปาทุกเดือน").
- On the schedule, the app generates a **draft** transaction.
- User confirms or edits before it posts. Drafts don't enter reward calculations or bill totals until confirmed.

## Technology constraints

- **Backend**: Rust. Single self-hosted binary on a VPS. Optimize for minimal setup and minimal dependencies.
- **Frontend**: TypeScript PWA. No specific framework pinned yet — pick during build, biasing toward "boring + minimal" given ~3 users.
- **Database**: deferred (Postgres is the safe default; SQLite is plausible given the tiny user count and self-host setup).
- **No build-side complexity**: avoid heavy ORMs, microservices, or anything that would cost more in setup than it pays back at this scale.

## Out of scope (explicit non-goals)

These were considered and rejected during the interview:

- **Statement OCR** — optional attachments only; no extraction.
- **Photo-of-slip OCR** — optional attachments only.
- **Bank SMS / share-sheet parsing** — manual entry is the primary path.
- **"Best card for this merchant" / "missed earnings" advice** — explicitly skipped; the app is a ledger, not an advisor.
- **Hierarchical categories** — flat user-defined list is enough.
- **Multi-tag categories** — single category per transaction.
- **Live Notion mirroring** — fresh start, no dual-write window.
- **Statement / attachment migration** — drops with the fresh-start choice.
- **Full historical import** — current cycle only at launch.
- **Read-event audit logging** — mutations only.

## See also

- [[data-model-target]] — entity shape (relational sketch).
- [[migration-considerations]] — what to do about existing Notion data (now reframed by the "fresh start" decision).
- [[../concepts/payment-lifecycle]] — `Transaction.status` enum transitions.
- [[../concepts/billing-cycle]] — the four independent date axes.
- [[../../.claude/skills/add-transaction/SKILL.md|/add-transaction]] — verbatim-merchant rule the new app inherits.
