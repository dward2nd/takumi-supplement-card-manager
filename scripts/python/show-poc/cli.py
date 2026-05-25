#!/usr/bin/env python3
"""show-poc — open the POC PWA in an isolated Chrome window.

deterministic + idempotent (within a profile dir): re-running opens a
new Chrome window pointed at the dev / preview URL. The Chrome profile
lives at a stable temp path so caches and storage persist across
invocations unless --fresh is passed.

Full flow on `uv run scripts/python/show-poc/cli.py`:

  1. Probe http://localhost:5173/ (Vite dev) and http://localhost:4173/
     (Vite preview). The first one that responds wins.
  2. If neither responds and --auto is set, start `bun run dev`
     detached, wait until the port responds, then proceed.
  3. Ensure the Chrome profile dir exists (wipe first if --fresh).
  4. `open -na "Google Chrome" --args --user-data-dir=<profile>
     --new-window <url>` — Chrome opens detached.

If no server is running and --auto isn't set, the script prints the
exact commands the user should run in another terminal and exits with
a non-zero code.

macOS only. On other platforms the script raises with a helpful message.

Output: JSON envelope `{url, profile_dir, fresh, app, started_dev}` on stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import paths  # noqa: E402

CHROME_APP = "Google Chrome"
CHROME_APP_PATH = Path("/Applications/Google Chrome.app")
DEFAULT_PROFILE_DIR = Path(os.environ.get("TMPDIR", "/tmp")) / "takumi-poc-chrome-profile"
POC_DIR = paths.REPO_ROOT / "poc"
DEV_URL = "http://localhost:5173/"
PREVIEW_URL = "http://localhost:4173/"


def _port_alive(url: str, timeout: float = 0.5) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return 200 <= resp.status < 500
    except (urllib.error.URLError, socket.timeout, ConnectionError, TimeoutError):
        return False


def _wait_for(url: str, timeout: float = 30.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if _port_alive(url):
            return True
        time.sleep(0.25)
    return False


def _ensure_environment() -> None:
    if sys.platform != "darwin":
        raise RuntimeError(
            f"show-poc supports macOS only (saw sys.platform={sys.platform!r}). "
            f"Start the dev server yourself with `cd poc && bun run dev`, "
            f"then open {DEV_URL} in your browser."
        )
    if not CHROME_APP_PATH.exists():
        raise RuntimeError(
            f"{CHROME_APP_PATH} not found. Install Google Chrome or open {DEV_URL} manually."
        )
    if not (POC_DIR / "package.json").exists():
        raise RuntimeError(
            f"POC project not found at {POC_DIR} (expected {POC_DIR / 'package.json'}). "
            f"Initialise the POC first (see `feedback-poc-charter`)."
        )


def _start_dev_server() -> int:
    """Start `bun run dev` in the background, return the PID."""
    log = POC_DIR / ".dev-server.log"
    proc = subprocess.Popen(
        ["bun", "run", "dev"],
        cwd=POC_DIR,
        stdout=log.open("w"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    return proc.pid


def run(*, fresh: bool = False, profile_dir: Path = DEFAULT_PROFILE_DIR, auto_start: bool = False) -> dict:
    _ensure_environment()

    started_dev_pid: int | None = None
    url: str | None = None

    if _port_alive(DEV_URL):
        url = DEV_URL
    elif _port_alive(PREVIEW_URL):
        url = PREVIEW_URL
    elif auto_start:
        started_dev_pid = _start_dev_server()
        if not _wait_for(DEV_URL, timeout=30.0):
            raise RuntimeError(
                f"started `bun run dev` (pid {started_dev_pid}) but {DEV_URL} "
                f"never came up within 30s. Check `poc/.dev-server.log` for errors."
            )
        url = DEV_URL
    else:
        raise RuntimeError(
            "No POC server responding on the dev (5173) or preview (4173) port.\n"
            "Start one yourself, then re-run /show-poc:\n\n"
            "    cd poc && bun run dev          # for live HMR\n"
            "    # …or:\n"
            "    cd poc && bun run preview --host  # for the built bundle\n\n"
            "Alternatively, pass --auto to let /show-poc start `bun run dev` itself."
        )

    if fresh and profile_dir.exists():
        shutil.rmtree(profile_dir)
    profile_dir.mkdir(parents=True, exist_ok=True)

    args = [
        "open",
        "-na",
        CHROME_APP,
        "--args",
        f"--user-data-dir={profile_dir}",
        "--new-window",
        "--no-first-run",
        "--no-default-browser-check",
        url,
    ]
    subprocess.run(args, check=True)

    return {
        "url": url,
        "profile_dir": str(profile_dir),
        "fresh": fresh,
        "app": CHROME_APP,
        "started_dev": started_dev_pid,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--fresh",
        action="store_true",
        help="Wipe the Chrome profile dir before launching (clears cache, storage, devtools state).",
    )
    ap.add_argument(
        "--profile-dir",
        type=Path,
        default=DEFAULT_PROFILE_DIR,
        help=f"Chrome --user-data-dir (default: {DEFAULT_PROFILE_DIR}).",
    )
    ap.add_argument(
        "--auto",
        action="store_true",
        help="Start `bun run dev` in the background if no POC server is currently responding.",
    )
    args = ap.parse_args(argv)
    out = run(fresh=args.fresh, profile_dir=args.profile_dir, auto_start=args.auto)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
