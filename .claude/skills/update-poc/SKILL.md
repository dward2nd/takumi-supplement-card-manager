---
name: update-poc
description: Sync the static POC at `poc/` to significant project changes (data model, concepts, schemas, formulas) since the POC was last committed. Use when the user runs `/update-poc`, asks to "refresh the POC", "sync the demo", or says "the docs changed — update the POC".
---

# update-poc

Walks the project's documented changes since the last commit that touched `poc/` and applies the *relevant* ones to the POC's data, HTML, and JS. The POC is a living visual checkpoint of the future app — not a real product — so the bar for "should this drive a POC change" is **does it alter what the future app does or shows**.

The POC is governed by [[feedback-poc-charter]]: minimal static SPA, vanilla JS, no build step, mock data only. Do not violate that charter during an update.

## Argument

None.

Invocation shape: `/update-poc`.

## Primary execution path — the deterministic change-detector script

`scripts/python/update-poc/cli.py` is the only mechanical step:

```sh
uv run scripts/python/update-poc/cli.py
```

What it does:

1. Finds the most recent commit that touched `poc/` (`since`).
2. Runs `git log <since>..HEAD --name-status` restricted to watched paths.
3. Returns a JSON envelope:

   ```
   {
     "since_commit": "<sha or null>",
     "poc_dir_exists": true,
     "watched_paths": ["docs/future-app", "docs/databases", ...],
     "change_count": N,
     "changes": [
       {"path": "docs/future-app/data-model-target.md", "status": "M",
        "last_commit": "<sha>", "last_subject": "..."}
     ]
   }
   ```

If `since_commit` is `null`, the envelope carries a `note` asking the user to commit the current POC state first. Stop and surface that note; do not try to scan harder.

### Watched paths (changes here may justify a POC update)

- `docs/future-app/` — the canonical phase-2 target. Almost any change here matters.
- `docs/databases/` — Notion schema descriptions. New fields / new SELECT values.
- `docs/concepts/` — cross-cutting rules (multipliers, billing cycle, payment lifecycle, premium tier, network).
- `docs/formulas/` — Notion formula decodings.
- `docs/people/` — cardholder facts.
- `CLAUDE.md` — top-level conventions.
- `.mcp.json` — Notion endpoint config (rarely relevant to the POC, included for completeness).

### Flags

- `--path <p>` (repeatable): override the watched-path list. Defaults to the set above. Use when sweeping a non-standard directory like `docs/cards/` after card-by-card promotion.

## Procedure

1. **Run the script.** Read the JSON envelope. If `since_commit` is `null` the POC has never been committed — there's no baseline against which to compute a delta. Stop and surface the CLI's `note` to the user, then suggest the bootstrap command verbatim:

   ```sh
   git add poc/ && git commit -m "Bootstrap POC baseline"
   ```

   After they commit, the next `/update-poc` run will compute changes since that commit. Do **not** auto-commit on their behalf — that would violate the "user reviews the diff" rule below.
2. **Triage the change list.** For each entry, `Read` the file and decide: does this change affect what the POC demonstrates? Apply these heuristics:

   | Change                                                                  | Likely action on POC                                                                 |
   |-------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
   | New entity / property in `docs/future-app/data-model-target.md`        | Add to `poc/data.js`. Surface in `index.html`/`app.js` if user-visible.              |
   | New SELECT value in a `docs/databases/*` note                          | Add to mock data only if the value materially affects display or logic.              |
   | New rule in `docs/concepts/*` (e.g. a new payment lifecycle state)     | Update the corresponding render — status pill, chip, conditional view, etc.          |
   | Formula change in `docs/formulas/*`                                    | Usually skip. The POC does not compute realized points/cashback. Apply only if the *inputs* (i.e. the doc-side data model) changed. |
   | `CLAUDE.md` convention change                                          | Almost always skip for the POC itself. Re-check the charter and skill instructions instead. |
   | `.mcp.json` change                                                     | Skip. POC is offline.                                                                |

3. **Cross-check Notion when the docs are ambiguous.** Use `mcp__notion__notion-fetch` (read-only) to verify a property or SELECT exists in the live schema before adding it to mock data. The vault can drift; Notion is the source of truth for data.
4. **Apply edits to `poc/`.** Touch the minimum set of files:
   - `poc/data.js` — mock data.
   - `poc/index.html` — table columns, panel hints, summary cards.
   - `poc/app.js` — rendering and filtering logic.
   - `poc/styles.css` — only if a new chip/pill/status colour is introduced.
   Extend in place; do not restructure.
5. **Smoke-test via chrome-devtools MCP.** Open `file://<repo>/poc/index.html`, click through Takumi / Baiboon / Nuta, verify the new behaviour renders, capture `list_console_messages` for errors. Take a screenshot of any new visible affordance.
6. **Report back** with three sections:
   - **Applied** — file + one-line reason per change.
   - **Skipped** — change + one-line reason why the POC doesn't need it.
   - **Verified** — what you smoke-tested and the outcome.
   Do **not** commit unless the user explicitly asks.

## Charter guardrails (non-negotiable, even when a doc change pulls toward them)

- **No build step inside `poc/`.** No `package.json`, no bundler, no transpiler.
- **No network calls.** All data stays in `poc/data.js`. The POC must never call Notion or any backend.
- **`file://` must keep working.** No server-side dependencies, no paths that break under `file://`.
- **Mock data only.** Never paste real card numbers, real bank statement merchant strings, or real bill amounts. Illustrative values only.

If a doc change would force a charter violation (e.g. "add a real Notion fetch to the POC"), surface the conflict to the user instead of complying silently.

## What this skill does NOT do

- Does **not** invent features the docs don't justify.
- Does **not** auto-commit. The user reviews the diff. (Use [[../release/SKILL.md|/release]] when they're ready.)
- Does **not** update Notion. POC is read-only.
- Does **not** add a README to `poc/`. CLAUDE.md policy — docs go in `docs/`, not `poc/`.

Cross-reference [[../show-poc/SKILL.md|/show-poc]] — once updates are applied and smoke-tested, suggest `/show-poc` so the user can see the result in a real browser window.
