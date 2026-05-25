---
name: update-poc
description: Sync the phase-2 PWA under `poc/` to significant project changes (data model, concepts, schemas, formulas, repositories, promotions) since the POC was last committed. The skill prepares a structured **context brief** describing what the ideal POC should look like and then hands off to [[../frontend-design/SKILL.md|/frontend-design]] for the visual + code work. Use when the user runs `/update-poc`, asks to "refresh the POC", "sync the demo", or says "the docs changed — update the POC".
---

# update-poc

`/update-poc` is a **two-phase** skill:

1. **Phase A — survey**: figure out which project changes since the last `poc/` commit are meaningful enough to ripple into the PWA, and synthesise a brief that describes the ideal target state.
2. **Phase B — design**: hand the brief to [[../frontend-design/SKILL.md|/frontend-design]] (with the project's POC constraints attached) and let it execute the visual + code changes inside `poc/` only.

The POC is the **phase-2 PWA**: a Vite + React + TypeScript app inside `poc/`, bun-managed, mobile-first, mock data only. It is a daily-use spend journal for three people — see [[../../docs/future-app/product-shape]] for the canonical product spec.

## Argument

None.

Invocation shape: `/update-poc`.

## Phase A — surveying changes

`scripts/python/update-poc/cli.py` enumerates "potentially significant" changes since the last commit that touched `poc/`:

```sh
uv run scripts/python/update-poc/cli.py
```

Output: a JSON envelope `{since_commit, poc_dir_exists, watched_paths, change_count, changes: [...]}`. If `since_commit` is `null`, the POC has never been committed — stop and ask the user to bootstrap with:

```sh
git add poc/ && git commit -m "Bootstrap POC baseline"
```

Do not auto-commit. After they commit, the next run computes a real delta.

If `change_count` is `0`, the POC is in sync; report "POC is in sync (baseline `<sha-short>`)" and stop — don't read docs, don't hand off to /frontend-design.

### Watched paths

| Path                              | Why it can ripple into the POC                                                          |
|-----------------------------------|------------------------------------------------------------------------------------------|
| `docs/future-app/`                | Canonical phase-2 product spec — anything here can reshape the UI.                       |
| `docs/databases/`                 | Notion schema. New fields / SELECT values that the POC must surface.                     |
| `docs/concepts/`                  | Cross-cutting rules (multipliers, billing cycle, payment lifecycle, promotions, etc.).   |
| `docs/promotions/`                | Per-promo narrative; structured data lives in `scripts/repositories/promotions/`.         |
| `docs/formulas/`                  | Notion formula decodings. Rarely UI-relevant on its own.                                 |
| `docs/people/`                    | Cardholder facts — names, roles, visibility rules.                                       |
| `docs/cards/`                     | Per-card narrative.                                                                      |
| `scripts/repositories/`           | Structured cards + promotions YAML. Drives the POC's mock data + classification preview. |
| `CLAUDE.md`                       | Top-level conventions.                                                                   |
| `.mcp.json`                       | Notion endpoint config (offline POC ⇒ rarely relevant; included for completeness).       |

### Triage heuristics

| Change                                                                  | Likely action on POC                                                                                                       |
|-------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| New entity / field in `docs/future-app/data-model-target.md`            | Add to the POC's `src/data/types.ts` and any seed-data file. Surface in a screen if user-visible.                            |
| New SELECT value in `docs/databases/*`                                  | Extend the seed in `src/data/` only if it materially affects display or the classification preview.                          |
| New rule in `docs/concepts/*` (e.g. a new payment-lifecycle state)      | Update the corresponding component — status pill, chip, tab, etc.                                                            |
| New promotion YAML in `scripts/repositories/promotions/`                | Mirror the promo into `src/data/promotions.ts` so the classification preview on Add Transaction stays current.               |
| New card YAML in `scripts/repositories/cards/`                          | Mirror the card into `src/data/cards.ts` with brand colours and a synthetic last-4.                                          |
| Formula change in `docs/formulas/*`                                     | Usually skip; the POC doesn't compute realized points. Apply only if the *inputs* (data model) shifted.                       |
| `CLAUDE.md` / `.mcp.json` change                                        | Almost always skip for the POC. Re-check the charter section below instead.                                                  |

## Phase B — handing off to `/frontend-design`

After triage, **invoke [[../frontend-design/SKILL.md|/frontend-design]]** with a structured brief. The brief is what makes the design skill effective in this codebase — it doesn't get to re-invent the world; it executes the project's conventions.

### The brief — what to pass

Always include these sections, written tersely:

1. **Project + audience** (one sentence). Pin from [[../../docs/future-app/product-shape]]:
   > A daily-use spend journal PWA for three people — Takumi (admin/primary), Baiboon, Nuta (supplement-card holders). Mobile-first, installable. Mock data only inside `poc/`.

2. **Phase-2 spec excerpts** that are load-bearing for this update. Cite the relevant section headings from [[../../docs/future-app/product-shape]] verbatim — don't paraphrase. Typical ones:
   - *Daily-use workflow* (action-first home, FAB to add transactions, mini-table entry, three flows: new / alias-matched / tap-to-reuse).
   - *Users & access model* (Takumi sees all; supplements see own + `PrimaryAccount` aggregates).
   - *Data model decisions* (`RewardRule` as JSON on `Transaction`, `PrimaryAccount` quotas, refund adjustment rows).

3. **What changed since `since_commit`** — the triaged list from Phase A, each entry annotated with "screen + component to touch".

4. **POC charter (non-negotiable)** — paste this block verbatim into the brief so /frontend-design doesn't drift:
   - Stack is fixed: **Vite + React + TypeScript + Tailwind v3 + Framer Motion + lucide-react + vite-plugin-pwa + bun**. No framework swaps in an update.
   - Everything stays inside `poc/`. No edits outside.
   - **Mock data only.** No network calls, no backend hits, no real card numbers or merchant strings. Illustrative values only.
   - The mobile container clamps to `max-w-md` (~448px) and centers on desktop — design is portrait-phone first.
   - **44px minimum touch targets** (use the `.tap` utility).
   - Safe-area-inset everywhere (use `.top-safe` / `.bottom-safe`).
   - **Typography is locked**: Fraunces (display, with italic), IBM Plex Sans Thai Looped (body), IBM Plex Mono (numerals, tabular figures). Don't introduce new fonts in a sync; that's a re-design, not an update.
   - **Colour palette is locked**: warm-dark default (`#0d0b08`), amber primary, teal for done, coral for danger. Don't introduce a new accent in a sync.
   - **Verbatim merchant strings** stay verbatim across the UI — never normalise.
   - **Thai field names** stay verbatim wherever shown (`ยอดชำระ`, `วันตัดรอบบิล`, `จ่ายแล้ว`).

5. **Aesthetic direction (already-committed)** — paste this one-liner so /frontend-design extends the look rather than reinventing it:
   > "Editorial journal" — typography-led, restrained colour, hero numerals in mono, generous spacing, asymmetric overlap on the display layer. Not a banking dashboard.

6. **Deliverables** — what the design skill should produce, file-by-file. Tie each change to a file in `poc/src/`. Examples:
   - "New `RewardRule` field → extend `src/data/types.ts` Transaction interface; surface in `TransactionRow` as a stacked-pill row."
   - "New 'rejected' payment-lifecycle state → add a `Pill` tone, render in `BillRow`."

### Invocation

Call the `frontend-design` skill via the Skill tool with the brief above as the argument. The handoff is the natural end of `/update-poc` — once /frontend-design returns, surface its summary back to the user and suggest [[../show-poc/SKILL.md|/show-poc]] to view the result.

## Procedure

1. **Run the survey script.** Read the JSON envelope.
2. **Handle the trivial cases** (no `since_commit` → bootstrap nudge; `change_count: 0` → "in sync" and stop).
3. **Triage**. For each watched-path change, `Read` the file, decide screen-impact per the heuristics above, and assemble a notes list keyed by "screen + component to touch".
4. **Cross-check structured data** when narrative docs are ambiguous. The structured source of truth lives in:
   - `scripts/repositories/cards/<slug>.yaml`
   - `scripts/repositories/promotions/<id>.yaml`
   - Live Notion via `mcp__notion__notion-fetch` (read-only) — only when neither narrative nor YAML answers the question.
5. **Compose the brief** with the six sections above.
6. **Invoke `/frontend-design`** with the brief. Wait for it to apply edits.
7. **Smoke-test via chrome-devtools-mcp**: launch `bun run dev` in `poc/`, navigate to the affected screen on a phone viewport (390×844), take a screenshot, check `list_console_messages` for errors. Stop the dev server when done.
8. **Report back** with three sections:
   - **Applied** — file + one-line reason per change.
   - **Skipped** — change + one-line reason the POC doesn't need it.
   - **Verified** — what was smoke-tested and the outcome (with screenshot path under `poc/.screenshots/`).
   Do **not** commit unless the user explicitly asks.

## Charter guardrails (non-negotiable, even when a doc change pulls toward them)

Pasted into the /frontend-design brief, repeated here for the agent's own awareness:

- **No framework swaps in a sync.** Stack changes are a re-build, not an update — discuss with the user first.
- **Mock data only.** No real PANs, no real bank-statement merchant strings, no real bill amounts.
- **No backend.** The PWA must work standalone in `bun run dev` / `bun run build`.
- **`poc/` is the boundary.** Don't edit anything outside it.
- **Service-worker hygiene.** Don't introduce data fetches inside the SW; the POC is offline by design.
- **Typography + palette are locked** (see *POC charter* in the brief).

If a doc change would force a charter violation (e.g. "add a real Notion fetch"), surface the conflict to the user instead of complying silently.

## What this skill does NOT do

- Does **not** invent features the docs don't justify.
- Does **not** auto-commit. The user reviews the diff. (Use [[../release/SKILL.md|/release]] when they're ready.)
- Does **not** update Notion. POC is read-only.
- Does **not** re-design from scratch. For ground-up re-builds (new aesthetic, new framework), invoke [[../frontend-design/SKILL.md|/frontend-design]] directly with a fresh brief.

Cross-reference [[../show-poc/SKILL.md|/show-poc]] — once updates are applied, suggest `/show-poc` to view the result in an isolated Chrome window.
