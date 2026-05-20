---
name: show-poc
description: Open the static POC at `poc/index.html` in an isolated Chrome window using a dedicated `--user-data-dir`. Use when the user runs `/show-poc`, asks to "open the POC", "show me the demo", or wants a browser window pointed at the local POC without polluting their main Chrome profile.
---

# show-poc

Launches `poc/index.html` in a separate Chrome session whose profile lives outside the user's main Chrome — no extensions, no history, no cookies bleed-over.

This is the **human-facing** demo launcher. For in-conversation smoke testing the agent should use the `chrome-devtools` MCP directly; `/show-poc` is for handing a real window to the user.

## Argument

None. Optional flags below.

Invocation shape: `/show-poc` (no args), or `/show-poc --fresh` when the previous profile is stale.

## Primary execution path — the deterministic script

`scripts/python/show-poc/cli.py` does the launch in one shot:

```sh
uv run scripts/python/show-poc/cli.py
```

What it does:

1. Resolves `<repo-root>/poc/index.html` and converts it to a `file://` URL.
2. Ensures the Chrome profile dir exists at `${TMPDIR:-/tmp}/takumi-poc-chrome-profile/` (wipes first if `--fresh`).
3. Runs `open -na "Google Chrome" --args --user-data-dir=<profile> --new-window <url>` — Chrome opens detached, control returns immediately.

Output: JSON envelope `{url, profile_dir, fresh, app}` on stdout.

Exits non-zero if:

- The platform isn't macOS.
- `Google Chrome.app` is missing from `/Applications`.
- `poc/index.html` is missing — most likely the POC hasn't been built yet.

### Flags

- `--fresh`: wipe the profile dir before launching. Use when the previous session got stuck, you want to clear caches, or DevTools state is interfering with the demo.
- `--profile-dir <path>`: override the profile location. Rarely needed.

## Procedure

1. Run the script with no flags by default. Pass `--fresh` only if the user explicitly asks ("from scratch", "reset", "clear cache").
2. Read the JSON envelope and report the URL + the profile dir back to the user — short. One or two lines.
3. If the script raises:
   - **Missing `poc/index.html`** → tell the user the POC doesn't exist yet and suggest `/update-poc` won't help here either (the POC must be authored first).
   - **Missing Chrome** → suggest the user opens the printed `file://` URL in whatever browser they have.
   - **Non-darwin platform** → same fallback: print the `file://` URL for them to open manually.

## Constraints

- **macOS only.** The `open` command is Apple-specific. Cross-platform support is out of scope.
- **Does not start a dev server.** The POC is static; `file://` is enough. Do not introduce one.
- **Does not rebuild the POC.** Use [[../update-poc/SKILL.md|/update-poc]] for syncing the POC to recent project changes.
- **Does not use the chrome-devtools MCP.** That MCP is for the agent's own browser interactions during a turn — `/show-poc` exists to give the human a real, persistent window.

## Notes

- The profile dir is reused across invocations on purpose: faster startup, the user keeps their devtools panel layout. `--fresh` is the escape hatch.
- Multiple invocations open multiple Chrome windows in the same isolated profile. Closing them doesn't affect the user's main Chrome.
- The POC charter ([[feedback-poc-charter]]) requires the POC to keep working from `file://`. If a doc change ever pulls the POC toward needing a server, push back — that's a charter violation.
