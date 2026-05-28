---
name: update-docs
description: Sweep `docs/`, `CLAUDE.md`, and `README.md` for staleness (broken wikilinks, broken path references, doc older than something it references, drift from CLAUDE.md / .mcp.json), then **apply the writes** for fixes that are unambiguous — and queue the rest at `docs/_stale-review.md` for human judgment. Use when the user runs `/update-docs`, asks to "fix stale docs", "sweep the vault for rot", or "bring the docs up to date with the code". Self-revising — extend this skill in place when new signal patterns appear.
---

# update-docs

Finds documentation files that are out of date relative to whatever else has moved in the repo, and fixes them. The vault is the project's persistent memory ([[../../CLAUDE.md]]), so when code, schemas, or conventions drift the docs need to follow — and waiting for humans to notice doesn't scale. This skill is both the sweeper and the writer.

Two outputs per run:

1. **Direct edits** to docs that have an unambiguous fix (e.g. a broken path reference whose intended target is obvious, a wikilink with one clear candidate).
2. A **review checklist** at `docs/_stale-review.md` for everything that needs human judgment (multi-candidate links, content-level drift, anything the skill can't confidently rewrite).

`CLAUDE.md` and `README.md` are in scope as edit targets too — they are docs, just at the repo root.

## Argument

None.

Invocation shape: `/update-docs`.

Optional override (rare): `--glob <pattern>` on the underlying CLI to scan a non-default file set.

## Primary execution path — the deterministic CLI

`scripts/python/update-docs/cli.py` is the only mechanical step:

```sh
uv run scripts/python/update-docs/cli.py
```

What it does:

1. Walks the doc set: `docs/**/*.md`, plus `CLAUDE.md` and `README.md`. Skips `docs/_stale-review.md` (it's the output, not an input).
2. Builds a freshness timestamp per file:
   - If the file is dirty in `git status` → use filesystem mtime.
   - Else → use `git log -1 --format=%ct` for that path.
3. For each doc, parses two reference kinds:
   - **Wikilinks** `[[target]]` / `[[target|alias]]` / `[[../rel/path]]` / `[[../folder/]]` (trailing slash = link to a directory). Obsidian's `[[x\|alias]]` table-escape is handled. Wikilinks that fall **inside a backtick code-span** are skipped — they're prose examples (e.g. `` `[[folder/note]]` `` in a syntax explanation), not real links. Folder wikilinks resolve when the directory exists, and never emit a `*_newer` signal (directory mtime is not a meaningful staleness driver).
   - **Path code-spans** with a `/` in them: `` `scripts/python/lib/notion_client.py` ``, `` `docs/concepts/cashback.md` ``. Bare filenames like `` `package.json` `` are intentionally ignored to avoid false positives on prose examples.
4. Emits a JSON envelope listing every doc with at least one signal. Signals are deduplicated within a doc.

### Signal kinds

Extend this table AND the `cli.py` source when new patterns surface — see *Self-revision contract* below.

| Kind                      | Meaning                                                              | Triage rule of thumb                                                          |
|---------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------|
| `broken_wikilink`         | `[[X]]` doesn't resolve to any markdown file (or, when `X` ends with `/`, to any directory) | **High priority** — fix or remove the link.                                   |
| `broken_path_ref`         | `` `path/to/x.py` `` doesn't exist on disk                           | **High priority** — usually a rename/move the doc didn't catch.               |
| `wikilink_target_newer`   | The wikilink target file is newer than this doc                      | Re-read the target; if it changed substantively, update this doc.             |
| `path_ref_newer`          | A path code-span target is newer than this doc                       | Same as above. Often the doc describes a script that has since been refactored. |
| `claudemd_newer`          | `CLAUDE.md` was touched after this doc                               | **Low priority alone.** Almost every old doc trips this. Only act on it if paired with another signal or if you can identify a specific convention that changed. |
| `mcp_config_newer`        | `.mcp.json` was touched after this doc                               | Rarely matters — only flags docs that pin an MCP endpoint or transport.       |

## Procedure

1. **Run the CLI.** Parse the JSON envelope.
2. **Triage candidates.** For each candidate, look at the signal mix:
   - Any `broken_*` → upgrade to **high** priority. Real rot.
   - Multiple non-`claudemd_newer` signals → **medium** priority.
   - Only `claudemd_newer` → **low** priority. Group these together in the checklist; they're a long tail.
   - `path_ref_newer` / `wikilink_target_newer` where the target is itself a stale-flagged doc → don't double-count; fix the upstream first.
3. **Read suspicious docs.** When in doubt, `Read` the doc and the referenced file to judge whether the signal reflects real drift or is benign (e.g. the doc still describes the right behaviour even though the code was reformatted). Skip whole-vault reading — only sample what you need.
4. **Cross-check Notion when the docs are about schema.** For a flagged `docs/databases/*.md`, optionally use `mcp__notion__notion-fetch` (read-only) to confirm the live schema still matches what the doc says. Only when signals don't already explain the staleness.
5. **Decide auto-fix vs queue.** Walk each signal through the *Auto-fix decision table* below. Auto-fixable items get an `Edit`/`Write` immediately. Everything else goes onto the review queue.
6. **Apply auto-fixes.** Use `Edit` with `replace_all=false` and full-surrounding-context strings — never blanket-replace. After each edit, re-read the surrounding paragraph to confirm the fix reads naturally. If it doesn't, revert and push the item to the review queue instead.
7. **Write `docs/_stale-review.md`.** Replace it in full; this file is regenerated each run. Use the *Output shape* below. Auto-fixed items go in a separate **Applied** section so the user can audit what changed.
8. **Report back inline** with four sections: **Applied** (what was edited and why), **High** (queued — broken links/refs the skill couldn't auto-fix), **Medium** (queued — multi-signal docs needing real review), **Low** (queued — `claudemd_newer`-only, count only). Mention the checklist file path. Do **not** commit; the user reviews the diff.

### Auto-fix decision table

A signal is **auto-fixable** only when all of these hold:

- The fix is local (one or two adjacent characters / one wikilink target string) — not a content rewrite.
- There is **exactly one** plausible new target on disk. Two or more candidates → human judgment, queue it.
- The fix doesn't change meaning, just the pointer. Rewording is never auto.

| Signal                  | Auto-fix policy                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `broken_wikilink`       | Auto-fix if there is **exactly one** existing markdown file whose stem either matches (ignoring case + punctuation) **or contains as a substring** the link's last path segment, and `Read` confirms the target is topical (the link's surrounding sentence makes sense with that target). The "contains" relaxation catches renames like `multipliers` → `points-and-multipliers`. Otherwise queue. |
| `broken_path_ref`       | Auto-fix if **exactly one** path on disk matches the broken ref's basename **and** lives under a sibling directory (typical rename: `scripts/python/foo.py` → `scripts/python/lib/foo.py`). Update the ref in place. Otherwise queue. |
| `wikilink_target_newer` / `path_ref_newer` | Never auto-fix — these signal **content** drift, which the skill cannot rewrite without judgment. Always queue. |
| `claudemd_newer`        | Never auto-fix — too vague a signal. Queue as Low.                                                                                                                              |
| `mcp_config_newer`      | Never auto-fix — `.mcp.json` rarely affects doc prose. Queue with a one-line "check if MCP endpoint pinning in this doc still matches `.mcp.json`".                              |

When in doubt, **queue rather than auto-fix.** A bad auto-fix that the human has to undo is worse than a queued item the human resolves in 10 seconds.

### Hard limits on writes

- Never delete a doc. Even if every reference to it is broken.
- Never edit `Name`-equivalent identifiers in docs (Thai field names, card titles, holder names). Verbatim is sacred ([[../../CLAUDE.md]]).
- Never edit `poc/*` — that's [[../update-poc/SKILL.md|/update-poc]]'s job.
- Never edit `.mcp.json` from this skill. If it's wrong, the user fixes it.
- Cap auto-fixes at 10 per run. Beyond that the run is probably wrong about the signal definition; queue the rest and stop.

## Output shape — `docs/_stale-review.md`

Single file, regenerated on every run. Four sections: **Applied** (write log of this run), **High** / **Medium** / **Low** (queue for the human). Use checkbox bullets so the user can tick items off as they resolve them.

```md
# Stale-doc review queue

Generated by `/update-docs` on <YYYY-MM-DD>. Run again to refresh.

Legend: ✏️ applied this run · 🔴 broken link/ref (queued) · 🟡 referenced file newer · ⚪ CLAUDE.md drift only.

## Applied

- ✏️ `docs/cards/uob-one.md` — replaced `[[../concepts/multipliers]]` with `[[../concepts/points-and-multipliers]]` (one matching target on disk).

## High

- [ ] 🔴 `docs/cards/_stubs.md` — wikilink `[[uob-premier]]` doesn't resolve. Promote `uob-premier.md` from stub when ready, or remove the link.

## Medium

- [ ] 🟡 `docs/concepts/cashback.md` — referenced `docs/future-app/data-model-target.md` is newer.

## Low

- [ ] ⚪ 18 docs flagged solely because `CLAUDE.md` was touched recently. Expand only if a convention you remember changing applies to one of them.
```

For each queued item, give a one-line *why* and (when known) a candidate fix the human can verify. For each Applied item, name the old and new value so the diff is auditable from the review file alone.

## Self-revision contract

This skill is expected to **grow** as the vault uncovers new patterns. When a run uncovers something the current procedure can't classify cleanly — for example a wikilink syntax not handled, a code reference style not covered (`` ` `` -less inline paths, callouts that name a file, etc.) — you must:

1. **Update `cli.py`** to capture the new pattern as a named signal kind. Keep signals deterministic; never include LLM-style guesses in the CLI.
2. **Update this SKILL.md**: add the new kind to the *Signal kinds* table with a one-line triage rule of thumb, and extend the *Procedure* if the new signal needs special handling.
3. Note the addition in the run report ("Added signal `X` because Y; see `_stale-review.md` for hits.").

Self-revision is **bounded**:

- Only extend when you have at least one concrete example from this run.
- Don't add signals that would require Notion / network access to evaluate — keep the CLI deterministic and offline. Schema-drift checks happen in the skill body (step 4), not the CLI.
- Don't add signals so noisy they'd flag most of the vault. If a signal's hit rate would exceed ~50% of docs, gate it behind a flag instead of making it default.

## Hard rules

### 1. Auto-fixes are narrow and reversible

Auto-fixes only swap a pointer (one wikilink target or one path-ref string) when there is exactly one plausible target on disk. Content rewrites, rewording, and "interpretive" updates are always queued for the human. See *Auto-fix decision table* and *Hard limits on writes*.

### 2. Don't commit

Never `git add`/`git commit` anything — neither the review file nor the doc edits. The user reviews the diff (a single `git diff` covers both kinds of change) and decides.

### 3. Respect the vault charter

Verbatim Thai field names ([[../../CLAUDE.md]]). When the review-file output mentions a Notion field by name, write it in Thai with an English gloss, same as everywhere else in the vault. The same rule applies to auto-fixes — never silently translate a Thai identifier while "fixing" a doc.

### 4. Don't recurse into `poc/`

`poc/` is not documentation. [[../update-poc/SKILL.md|/update-poc]] handles drift between docs and the POC. This skill handles drift inside the docs.

## What this skill does NOT do

- Does **not** rewrite doc *content* — only swaps unambiguous pointers (wikilink targets, path refs). Content drift goes to the review queue.
- Does **not** verify content against Notion automatically. Only on demand during triage.
- Does **not** check `scripts/` for stale docstrings — those live in code, not docs.
- Does **not** delete `docs/_stale-review.md` when the queue is empty. It rewrites the file with an "✅ nothing flagged" body (Applied section still listed) so the user can confirm the sweep ran.
- Does **not** auto-fix more than 10 items per run. The cap is a safety belt against a broken signal definition cascading.

Cross-reference [[../update-poc/SKILL.md|/update-poc]] (POC sync) and [[../release/SKILL.md|/release]] (cut a version after a doc-cleanup pass).
