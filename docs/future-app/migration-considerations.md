---
tags: [future, migration]
---

# Migration considerations: Notion → custom app

When phase 2 begins, the eight Notion databases described in this vault need to flow into the data model in [[data-model-target]]. This note captures what's likely to be tricky.

## Extraction shape

Notion's API yields each database as a paginated list of pages, each page being a `properties` dict. Per database:

- [[../databases/takumi-cards]] → `CardProduct` rows + `Card` rows (split per card-product)
- [[../databases/takumi-transactions]] → `Transaction` rows + populate `Category` from `หมวดหมู่`
- [[../databases/baiboon-cards]] / [[../databases/nuta-cards]] → `CardProduct` (dedup by name across the three universes) + `Card` rows
- [[../databases/baiboon-transactions]] / [[../databases/nuta-transactions]] → `Transaction` rows
- [[../databases/baiboon-bills]] / [[../databases/nuta-bills]] → `Bill` rows, but the `Card` SELECT must resolve to the corresponding `Card.id` by name-matching

## Hard problems

### 1. `PrimaryAccount` is not in Notion

No database represents the underlying primary account that a supplement card hangs off. The migration must **invent** primary accounts, probably by grouping cards: every `UOB Premier` card (Takumi's, Baiboon's, Nuta's) belongs to one underlying UOB Premier account.

Heuristic: if two `Card` rows in different people's universes share the same `Name`, they probably share an underlying primary account. Confirm with the user during migration.

### 2. Bills' `Card` is a SELECT — name-match resolution

Need a deterministic name-to-card-id lookup for each Bill row. The SELECT options are clean (no typos seen as of 2026-05-19), but verify before importing. A reconciliation script can pre-check that every `Bills.Card` SELECT value matches a `Cards.Name` row in the same person's universe.

### 3. Three formula triplets

`คะแนนที่ได้จริง`, `คะแนน unrealized`, `ยอดค้างชำระ` each exist in three databases. The bodies *might* be identical but probably aren't (Takumi has `×3` and no `÷4`; supplements have `÷4` and no `×3`). Decode all three sets ([[../formulas/points-realized]], [[../formulas/points-unrealized]], [[../formulas/outstanding-balance]]) and decide:

- **Option A**: replicate three engines in the app (one per person).
- **Option B**: unify into one engine driven by per-card config (multiplier table, gating rules).

Option B is the right end-state but requires confirming that the rules **can** be unified — i.e. that the differences are intentional UI conveniences rather than genuinely different reward maths.

### 4. Photos & PDFs

The Bills DB stores `ใบแจ้งยอด (PDF)` and `หลักฐานการชำระ` as Notion `file` properties. These are S3-backed URLs Notion serves. Migration must download and re-host (Notion file URLs expire).

### 5. The `Credit Return` semantic ambiguity

Open question (see [[data-model-target]] open questions): is a refunded transaction a *transition* or an *adjustment row*? Different answers imply different migration scripts. Ask the user.

### 6. Discontinued Takumi data

Takumi's own activity has reportedly been discontinued for some time — the data may be partial or stale. Decide with the user whether to migrate it as historical record or skip.

## Migration script characteristics

- One-shot, not deterministic-by-rerun (data lands in target DB with new IDs).
- Lives in `scripts/typescript/` or `scripts/python/` per the sandbox rules in `../../scripts/README.md` (outside this vault).
- Should produce an audit report: rows extracted per DB, rows loaded per target table, mismatches flagged.
- Should run against a **read-only** copy of Notion first (use the Notion API; don't mutate source).
