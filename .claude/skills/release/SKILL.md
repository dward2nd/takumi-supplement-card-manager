---
name: release
description: Cut a new release of this repo — bump VERSION (major/minor/patch), commit any unstaged/uncommitted changes, tag the commit, and push branch + tag to origin. Use when the user runs `/release <type>` or asks to cut a new version.
---

# release

Cuts a new repo release. This repo is in phase 1 (observation & research) — no built application yet — so a release here marks "the docs and scripts reached state X", not a binary artifact. Starting version is `0.0.1`; bumps follow semver from there.

## Argument

`type` (required): exactly one of `major`, `minor`, `patch`.

Invocation shape: `/release <type>`.

If the user invokes the skill without a type, or with anything else, **stop and ask**. Do not guess.

## Primary execution path — the deterministic script

`scripts/python/release/cli.py` does the entire flow in one shot:

```sh
uv run scripts/python/release/cli.py <type>
```

What it does, in order:

1. Reads `/VERSION` (repo root). Parses as semver. Errors if missing or malformed.
2. Bumps per `<type>`:
   - `major`: `X.Y.Z` → `(X+1).0.0`
   - `minor`: `X.Y.Z` → `X.(Y+1).0`
   - `patch`: `X.Y.Z` → `X.Y.(Z+1)`
3. Writes the new value to `/VERSION`.
4. `git add -A` — **all** currently unstaged/untracked changes ride along with the release commit. This is intentional: the user opted in at skill-design time. If they have work-in-progress they don't want bundled, they should stash it before invoking.
5. `git commit -m "release: v<next>"`.
6. `git tag -a v<next> -m "Release v<next>"` (annotated).
7. `git push origin <current-branch>`.
8. `git push origin v<next>` — pushes only the new tag, never `--tags`.

Output is a JSON envelope `{previous, next, type, version_file, commit, tag, actions: [...]}` on stdout.

### Flags

- `--dry-run`: write VERSION but skip every git op. Useful when verifying the bump math without polluting history.
- `--no-push`: do steps 1–6 only (commit + tag locally; user pushes manually later).
- `--no-tag`: skip tagging.
- `--no-commit`: only bump the file. Implies `--no-tag` and `--no-push` from the user's perspective even though they're independent flags.

For a normal release, **pass no flags**.

## Procedure

1. **Validate `type`.** Must be `major | minor | patch`. Reject anything else.
2. **Pre-flight `git status`.** Show the user what's about to be swept into the release commit. If anything looks accidental (e.g. a stray scratch file), surface it and confirm before running the script. The script itself will not pause for you.
3. **Run the script** with no flags (full flow). Pipe nothing — `type` is a positional CLI arg.
4. **Read the JSON envelope** and report back to the user:
   - The bump (`<previous> → <next>`).
   - The commit hash.
   - The tag name and that it was pushed.
   - Anything in `push_skipped` (e.g. no remote configured).
5. If the script raises:
   - **Tag already exists** → tell the user the version was bumped on disk but the tag step failed; they can either delete the tag and rerun, or pick a different bump type.
   - **Push rejected** (branch protection, no permission, etc.) → the local commit and tag exist; surface the git error verbatim and let the user decide.
   - **Pre-commit hook failed** → do **not** add `--no-verify`. Fix the underlying issue, then have the user re-run.

## Rollback

If the user wants to undo a release that hasn't been pushed yet:

- `git tag -d v<next>` — delete the local tag.
- `git reset --soft HEAD~1` — undo the commit, keep the staging intact so they can re-edit.
- `git restore VERSION` — revert the version file.

If it has already been pushed, undo is invasive (force-push to rewrite history, `git push --delete origin v<next>`) and should not be attempted without explicit user instruction.

## Notes

- The version in `scripts/python/pyproject.toml` is the Python sandbox's own version and is **independent** of the repo's release version. This skill does not touch it.
- If a CHANGELOG.md is added to the repo later, extend this skill to stamp it. Right now the only artifact is VERSION + the tag.
- All hard rules from the project ([[../add-transaction/SKILL.md]] style — verbatim, no normalization, no skipping hooks) apply by extension.
