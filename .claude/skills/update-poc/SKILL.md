---
name: update-poc
description: Refresh the phase-2 PWA under `poc/` — either by syncing it to recent project changes (data model, concepts, schemas, formulas, repositories, promotions) since the POC was last committed, **or** by applying direct user feedback (with screenshots, UX critiques, feature requests). The skill prepares a structured **context brief** describing what the ideal POC should look like and then hands off to [[../frontend-design/SKILL.md|/frontend-design]] for the visual + code work. Use when the user runs `/update-poc`, attaches POC screenshots, asks to "refresh the POC", "sync the demo", or says "the docs changed — update the POC".
---

# update-poc

`/update-poc` is a **two-phase** skill driven by one of two **triggers**:

- **Doc-drift trigger** (`/update-poc` with no args): the user wants the POC re-synced against project changes since its last commit. The deterministic CLI surfaces the deltas; the agent triages them.
- **Direct-feedback trigger** (`/update-poc <feedback text>` and/or attached screenshots): the user has reviewed the running POC and is requesting specific UX, layout, or behavioural changes. The CLI is informational only here — the brief is composed from the feedback itself, not from a doc delta.

The two triggers share **phase B** (compose a brief, hand off to [[../frontend-design/SKILL.md|/frontend-design]]) but differ in **phase A** (how the brief is sourced).

The POC is the **phase-2 PWA**: a Vite + React + TypeScript app inside `poc/`, bun-managed, mobile-first, mock data only. It is a daily-use spend journal for three people — see [[../../docs/future-app/product-shape]] for the canonical product spec.

## Argument

Optional. When present, it's interpreted as direct user feedback on the running POC (with or without screenshots).

Invocation shape:

- `/update-poc` — doc-drift trigger.
- `/update-poc <feedback paragraph(s)>` — direct-feedback trigger. Screenshots attached to the message count as feedback artefacts.

## Phase A — sourcing the brief

### Doc-drift trigger (no args)

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

### Direct-feedback trigger (args present)

When the user invokes `/update-poc` with text and/or attached screenshots, the **CLI is informational only** — its `change_count` is just a tag-along signal. The brief is composed directly from:

1. The user's argument text — verbatim points, broken out one by one.
2. Any attached images — referenced by index ("Image #1 shows X").
3. The agent's knowledge of the current POC structure (file map, locked tokens, screens) so the brief lands as file-level deliverables in phase B.

If the CLI happens to surface doc deltas *in addition*, fold them into the brief as separate items — but don't let "the CLI returned 0" stop you from acting on the user's feedback.

> The two triggers are not mutually exclusive in practice. The user can absolutely give feedback *and* have unsynced doc deltas in the same run. Triage both.

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

3. **What needs to change** — depending on the trigger:
   - *Doc-drift trigger*: the triaged delta list from Phase A, each entry annotated with "screen + component to touch".
   - *Direct-feedback trigger*: the user's feedback re-stated as concrete change items, each annotated with "screen + component to touch" (e.g. "Card detail confusion → CardDetailScreen + CardFace: move overall vs cycle apart"). Quote the user's words; don't paraphrase to the point of losing intent.
   - *Both*: list both, kept visually distinct.

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

1. **Classify the trigger.** If the user supplied argument text or attached images, this is the **direct-feedback** trigger. Otherwise it's the **doc-drift** trigger.
2. **Run the survey script either way** — it's quick and the result feeds the *What needs to change* section of the brief:
   - Doc-drift trigger: `change_count: 0` → report "POC is in sync" and stop; otherwise triage.
   - Direct-feedback trigger: keep the result as informational input but don't stop on `change_count: 0`. The user's feedback IS the work.
3. **For doc-drift items:** for each watched-path change, `Read` the file, decide screen-impact per the heuristics above, and assemble a notes list keyed by "screen + component to touch".
4. **For direct-feedback items:** parse the user's argument into discrete change items (one per bullet/paragraph). Map each to "screen + component to touch" using the file map under *Aesthetic direction*. Quote the user's wording when it disambiguates intent.
5. **Cross-check structured data** when narrative docs are ambiguous. The structured source of truth lives in:
   - `scripts/repositories/cards/<slug>.yaml`
   - `scripts/repositories/promotions/<id>.yaml`
   - Live Notion via `mcp__notion__notion-fetch` (read-only) — only when neither narrative nor YAML answers the question.
6. **Compose the brief** with the six sections above.
7. **Invoke `/frontend-design`** with the brief. Wait for it to apply edits.
8. **Smoke-test via chrome-devtools-mcp**: launch `bun run dev` in `poc/`, navigate to the affected screen on a phone viewport (390×844), take a screenshot, check `list_console_messages` for errors. Stop the dev server when done.
9. **Report back** with three sections:
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
