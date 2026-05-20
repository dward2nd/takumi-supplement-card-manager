#!/usr/bin/env python3
"""show-poc — open poc/index.html in an isolated Chrome window.

deterministic + idempotent (within a profile dir): re-running opens a
new Chrome window pointed at the same `file://` URL. The Chrome profile
lives at a stable temp path so caches and storage persist across
invocations unless --fresh is passed.

Full flow on `uv run scripts/python/show-poc/cli.py`:

  1. Resolve <repo-root>/poc/index.html and convert to a file:// URL.
  2. Ensure the profile dir exists (wipe first if --fresh).
  3. `open -na "Google Chrome" --args --user-data-dir=<profile> --new-window <url>`
     — launches Chrome detached. Control returns to the caller immediately.

The profile dir is intentionally separate from the user's main Chrome
so there's no cookie/extension/history bleed-over from the demo into
the user's regular browsing session.

macOS only. On other platforms the script raises with a helpful
message — the human can open the file directly.

Output: JSON envelope `{url, profile_dir, fresh, app}` on stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import paths  # noqa: E402

CHROME_APP = "Google Chrome"
CHROME_APP_PATH = Path("/Applications/Google Chrome.app")
DEFAULT_PROFILE_DIR = Path(os.environ.get("TMPDIR", "/tmp")) / "takumi-poc-chrome-profile"
POC_ENTRY = paths.REPO_ROOT / "poc" / "index.html"


def _ensure_environment() -> None:
    if sys.platform != "darwin":
        raise RuntimeError(
            f"show-poc supports macOS only (saw sys.platform={sys.platform!r}). "
            f"Open {POC_ENTRY} in your browser manually."
        )
    if not CHROME_APP_PATH.exists():
        raise RuntimeError(
            f"{CHROME_APP_PATH} not found. Install Google Chrome or invoke the POC manually."
        )
    if not POC_ENTRY.exists():
        raise RuntimeError(
            f"POC entry not found at {POC_ENTRY}. Initialise the POC first (see `feedback-poc-charter`)."
        )


def run(*, fresh: bool = False, profile_dir: Path = DEFAULT_PROFILE_DIR) -> dict:
    _ensure_environment()

    if fresh and profile_dir.exists():
        shutil.rmtree(profile_dir)
    profile_dir.mkdir(parents=True, exist_ok=True)

    url = POC_ENTRY.as_uri()  # file:///...
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
    args = ap.parse_args(argv)
    out = run(fresh=args.fresh, profile_dir=args.profile_dir)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
