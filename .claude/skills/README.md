# Skills — responsibility map & boundaries

How the skills layer is organised, and the single-responsibility audit that guides where new behaviour belongs. (This file is an index — the skill loader only reads `<name>/SKILL.md`, so a top-level `README.md` here is documentation, not a skill.)

## Architecture

Each skill is `.claude/skills/<name>/SKILL.md` (the agent-facing contract) backed by a deterministic `scripts/python/<name>/cli.py`, with shared logic in `scripts/python/lib/*.py`.

**Rule of thumb: one user-facing task per skill.** Cross-skill behaviour is shared through `lib/` (e.g. `lib.transaction_write`, `lib.promotions`, `lib.payments`, `lib.bill_cycle`, `lib.bills`). A skill may *orchestrate* by delegating to another skill's lib — but it must not absorb that skill's job. Example: `/update-bill` records a payment on slip upload by **delegating** to `lib.payments` (the core behind `/record-payment`); it does not reimplement transaction-writing.

## The skills, by responsibility

**Write — Transactions DB**
- `add-transaction` — write charge rows (verbatim merchant, holder→DS routing, `Processed` default).
- `add-installment` — write the first `01/NN` term of a new installment plan.
- `populate-installment` — append the next `NN+1` term of in-progress plans to a cycle.
- `record-payment` — write the negative-amount **payment** row that offsets a cycle to zero. *(Split out of `/update-bill`, 2026-05-29.)*
- `post-cashback-credits` — write the cycle's cashback credit rows (UOB One).
- `update-transaction` — patch existing transaction rows.

**Write — Bills DB**
- `prepare-bill` — draft a `[DRAFT]` Bills row from the cycle's transactions.
- `update-bill` — patch a Bills row (`จ่ายแล้ว`, slip/statement files, Note, finalize). Delegates payment-row creation to `record-payment` on slip upload.

**Write — repositories**
- `add-promotion` / `update-promotion` — declare / patch promotion YAML.

**Read / preview (no mutation)**
- `classify-transaction` — preview the promo classification (`% cb`, multiplier, reason, Note) before writing. *(New, 2026-05-29.)*
- `fetch-transactions` — query transactions (+ optional aggregate summary).
- `summarize-overview` — per-holder portfolio table.
- `audit-bill` — diff a statement PDF against Notion for a cycle.
- `audit-transaction-dates` — flag BC/DD pairs that break the issuer pattern.

**Docs / tooling** — `update-docs`, `update-poc`, `show-poc`, `release`, `frontend-design`.

## Single-responsibility audit (2026-05-29)

Most skills are already single-purpose. The candidates where a second concern was bundled, with the verdict acted on / recommended:

| Skill | Bundled concern | Verdict | Status |
|-------|-----------------|---------|--------|
| `update-bill` | recording the payment ledger row alongside patching the Bills row | **Split** — payments belong in their own skill; `update-bill` delegates on slip upload | ✅ done → `record-payment` + `lib.payments` |
| 5 write skills | `auto_classify` (promo tiering) embedded as a flag with no preview | **Add a read-only preview** so classifications are inspectable before a write | ✅ done → `classify-transaction` |
| `prepare-bill` | auto-populates installments + checks cashback credits + auto-writes the Note inside "draft a bill" | **Keep, but surface** — this is deliberate orchestration; splitting would force two commands per bill. Improvement is to *report* what it populated, not extract it | open (recommended: surface) |
| `update-bill` | `finalize` (draft→final state) and `refresh_from_transactions` (recompute total) beyond "patch a field" | Defensible either way; small opt-in branches. Could become `finalize-bill` / `refresh-bill` if they grow | open (low priority) |
| `audit-bill` | ships `extract.py` (PDF→text) + `cli.py` (diff) as two steps | Extraction already lives in `lib.pdf_text`; formalise `extract-statement-pdf` only if another skill needs PDF text | open (low cost) |
| `post-cashback-credits` | crediting schedule hardcoded to UOB One | Extensibility refactor (read schedule from promotion YAML), not a split | defer until a 2nd card needs it |

## Principles for new behaviour

1. **One user-facing task per skill.** If a request spans two databases or two distinct operations, that's two skills (one may delegate to the other).
2. **Shared logic lives in `lib/`**, not duplicated across `cli.py` files. New cross-cutting logic → a `lib/` module first, then thin skill wrappers.
3. **Reads never mutate.** Preview/audit skills are read-only; they hand values to a write skill.
4. **Delegate, don't absorb.** Orchestration is fine (call another skill's lib); copying its responsibility in is not.
5. **Deterministic + idempotent scripts.** Re-running a write skill with the same spec must be safe (dedup / no-duplicate guards).
