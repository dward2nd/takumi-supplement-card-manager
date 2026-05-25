---
name: show-poc
description: Open the POC PWA in an isolated Chrome window. Probes the Vite dev (5173) / preview (4173) ports and opens whichever responds; with `--auto`, starts `bun run dev` itself if no server is running. Use when the user runs `/show-poc`, asks to "open the POC", "show me the demo", or wants a browser window pointed at the local PWA without polluting their main Chrome profile.
---

# show-poc

Launches the POC PWA in a separate Chrome session whose profile lives outside the user's main Chrome — no extensions, no history, no cookies bleed-over.

This is the **human-facing** demo launcher. For in-conversation smoke testing the agent should use the `chrome-devtools` MCP directly; `/show-poc` is for handing a real window to the user.

## Argument

None. Optional flags below.

Invocation shape: `/show-poc` (no args), `/show-poc --auto` to let the skill start the dev server itself, or `/show-poc --fresh` when the previous Chrome profile is stale.

## Primary execution path — the deterministic script

`scripts/python/show-poc/cli.py` does the launch in one shot:

```sh
uv run scripts/python/show-poc/cli.py
```

What it does:

1. Probes `http://localhost:5173/` (Vite dev) and `http://localhost:4173/` (Vite preview). The first one that responds wins.
2. If neither responds and `--auto` is set, starts `bun run dev` from `poc/` in the background (log to `poc/.dev-server.log`) and waits up to 30s for the dev port to open.
3. Ensures the Chrome profile dir exists at `${TMPDIR:-/tmp}/takumi-poc-chrome-profile/` (wipes first if `--fresh`).
4. Runs `open -na "Google Chrome" --args --user-data-dir=<profile> --new-window <url>` — Chrome opens detached, control returns immediately.

Output: JSON envelope `{url, profile_dir, fresh, app, started_dev}` on stdout. `started_dev` carries the dev-server PID if the script spawned one (so the user can `kill <pid>` later).

Exits non-zero if:

- The platform isn't macOS.
- `Google Chrome.app` is missing from `/Applications`.
- `poc/package.json` is missing — the POC hasn't been authored.
- No server is responding and `--auto` wasn't passed. The error message includes the exact commands to start one.

### Flags

- `--auto`: start `bun run dev` in the background if nothing is responding. The dev server keeps running after the script exits; report the PID back so the user can kill it.
- `--fresh`: wipe the Chrome profile dir before launching. Use when the previous session got stuck or DevTools state interferes with the demo.
- `--profile-dir <path>`: override the profile location. Rarely needed.

## Procedure

1. Default: run the script with no flags. The user has likely already started `bun run dev` in another terminal.
2. If the user says "start it for me" / "open it from scratch" / "I haven't started anything", pass `--auto`.
3. Pass `--fresh` only when the user explicitly asks ("from scratch", "reset", "clear cache").
4. Read the JSON envelope and report the URL + profile dir back to the user — short. One or two lines. If `started_dev` is non-null, also surface the PID and remind the user how to stop it (`kill <pid>`).
5. If the script raises:
   - **No server + no `--auto`** → tell the user to either run `cd poc && bun run dev` in another terminal or re-invoke with `--auto`.
   - **Missing `poc/package.json`** → tell the user the POC project hasn't been authored yet; `/update-poc` won't help (it needs an existing baseline).
   - **Missing Chrome** → suggest the user opens the printed URL in whatever browser they have.
   - **Non-darwin platform** → same fallback: print the URL for them to open manually.

## Constraints

- **macOS only.** The `open` command is Apple-specific. Cross-platform support is out of scope.
- **Requires a running dev or preview server.** The POC is no longer a static `file://` page — it's a Vite-built PWA. `--auto` is the convenience escape hatch.
- **Does not rebuild the POC.** Use [[../update-poc/SKILL.md|/update-poc]] for syncing the POC to recent project changes.
- **Does not use the chrome-devtools MCP.** That MCP is for the agent's own browser interactions during a turn — `/show-poc` exists to give the human a real, persistent window.
- **Leaves the dev server running if it spawned one.** The user controls its lifecycle.

## Notes

- The profile dir is reused across invocations on purpose: faster startup, the user keeps their devtools panel layout. `--fresh` is the escape hatch.
- Multiple invocations open multiple Chrome windows in the same isolated profile. Closing them doesn't affect the user's main Chrome.
- Per the POC charter (memory `feedback-poc-charter`) the POC stack is **fixed** — Vite + React + TS + bun. If a doc change would force a stack swap, push back; that's a re-design, not an update.
