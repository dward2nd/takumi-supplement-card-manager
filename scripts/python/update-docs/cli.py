#!/usr/bin/env python3
"""update-docs — flag documentation files likely to be stale relative
to the current state of the codebase.

deterministic + idempotent: no writes, no network. Compares each doc's
"freshness time" against the freshness time of the files it references
(wikilinks + path code-spans) and a small set of global drift sources
(CLAUDE.md, .mcp.json). Emits a JSON envelope on stdout.

"Freshness time" of a file F:
  - If F appears in `git status --porcelain` (modified or untracked),
    use its filesystem mtime — the working tree is newer than HEAD.
  - Otherwise, use `git log -1 --format=%ct -- F` (commit time).
  - If neither is available (file doesn't exist), the ref is "broken".

Signal kinds (extend here AND in the SKILL.md "Signals" section when
new patterns are found in the field):

  - broken_wikilink     : [[X]] doesn't resolve to any markdown file
  - broken_path_ref     : `path/to/x.py` doesn't exist on disk
  - wikilink_target_newer : a [[X]] target is newer than the doc
  - path_ref_newer      : a `path/to/x` code-span target is newer than the doc
  - claudemd_newer      : CLAUDE.md is newer than the doc
  - mcp_config_newer    : .mcp.json is newer than the doc

Output shape — see `run()`. The CLI never edits docs; that is the
skill body's job.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import paths  # noqa: E402

DEFAULT_DOC_GLOBS: list[str] = [
    "docs/**/*.md",
    "CLAUDE.md",
    "README.md",
]

# Files whose freshness, if newer than a doc, suggests convention/config drift.
GLOBAL_DRIFT_SOURCES: list[tuple[str, str]] = [
    ("CLAUDE.md", "claudemd_newer"),
    (".mcp.json", "mcp_config_newer"),
]

# Wikilink: [[target]] or [[target|alias]]. Capture `target`. We later
# discard hits whose [[ falls inside a backtick code-span — those are
# prose examples (e.g. ``[[folder/note]]`` in an explanation sentence).
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")

# Path code-span: `something/with/slash.ext` — require a slash to avoid
# matching bare filenames like `package.json` mentioned as examples.
PATH_REF_RE = re.compile(r"`([^`\s]*/[^`\s]+\.[A-Za-z0-9]+)`")

# Detect backtick code-spans so wikilink hits inside them can be skipped.
# Matches both single-backtick spans and triple-backtick fences (greedy
# enough for typical docs; we only need to know whether a position is
# inside one, not to perfectly preserve span boundaries).
CODE_SPAN_RE = re.compile(r"```[\s\S]*?```|`[^`\n]+`")

# Files we never treat as a doc to scan (output of the skill, lockfiles, etc.)
SKIP_DOC_REL: set[str] = {
    "docs/_stale-review.md",
}


def _git(args: list[str], *, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=paths.REPO_ROOT,
        check=check,
        text=True,
        capture_output=True,
    )
    return (proc.stdout or "").rstrip("\n")


def _git_porcelain_paths() -> set[str]:
    """Return the set of repo-relative paths with uncommitted changes
    (modified, added, deleted, untracked, etc.). Rename targets are
    returned as the *new* path."""
    raw = _git(["status", "--porcelain"])
    dirty: set[str] = set()
    for line in raw.splitlines():
        if not line:
            continue
        # Format: XY <path>  OR  XY <old> -> <new>
        payload = line[3:]
        if " -> " in payload:
            payload = payload.split(" -> ", 1)[1]
        dirty.add(payload.strip())
    return dirty


def _git_last_commit_ts(rel: str) -> int | None:
    out = _git(["log", "-1", "--format=%ct", "--", rel], check=False)
    if not out.strip():
        return None
    try:
        return int(out.strip())
    except ValueError:
        return None


def _freshness(rel: str, dirty: set[str]) -> int | None:
    """Repo-relative path → freshness timestamp (epoch seconds), or
    None if the file doesn't exist on disk."""
    abs_path = paths.REPO_ROOT / rel
    if not abs_path.exists():
        return None
    if rel in dirty:
        try:
            return int(abs_path.stat().st_mtime)
        except OSError:
            return None
    ts = _git_last_commit_ts(rel)
    if ts is not None:
        return ts
    # Fall back to mtime if the file is tracked but has no history yet (shouldn't usually happen).
    try:
        return int(abs_path.stat().st_mtime)
    except OSError:
        return None


def _iter_docs(globs: list[str]) -> list[Path]:
    seen: dict[str, Path] = {}
    for pattern in globs:
        for p in paths.REPO_ROOT.glob(pattern):
            if not p.is_file():
                continue
            rel = p.relative_to(paths.REPO_ROOT).as_posix()
            if rel in SKIP_DOC_REL:
                continue
            seen[rel] = p
    return [seen[k] for k in sorted(seen.keys())]


def _resolve_wikilink(raw_target: str, doc_rel: str, doc_index: dict[str, str]) -> str | None:
    """Resolve a wikilink target to a repo-relative markdown path, or
    None if it cannot be resolved.

    Resolution order:
      1. If the target contains `/`, treat as a relative path from the doc.
      2. Otherwise, look up by basename in the global doc index.
    """
    # Obsidian escapes the pipe in table cells as `\|`, so a link like
    # `[[uob-one\|UOB One]]` captures `uob-one\` here. Strip the trailing slash.
    target = raw_target.strip().rstrip("\\")
    if not target:
        return None
    # Strip an optional explicit `.md` extension.
    if target.endswith(".md"):
        bare = target[:-3]
    else:
        bare = target

    if "/" in bare:
        doc_dir = Path(doc_rel).parent
        candidate = (doc_dir / f"{bare}.md").as_posix()
        # Normalize ../ segments.
        candidate = os.path.normpath(candidate).replace("\\", "/")
        abs_candidate = paths.REPO_ROOT / candidate
        if abs_candidate.exists():
            return candidate
        return None

    # Basename lookup.
    basename = bare.split("/")[-1]
    return doc_index.get(basename)


def _build_doc_index(docs: list[Path]) -> dict[str, str]:
    """basename (without `.md`) → repo-relative path. Last-wins on
    duplicates; the typical case is no duplicates."""
    out: dict[str, str] = {}
    for p in docs:
        rel = p.relative_to(paths.REPO_ROOT).as_posix()
        out[p.stem] = rel
    return out


def _resolve_path_ref(raw: str, doc_rel: str) -> str | None:
    """Resolve a code-span path reference to a repo-relative path."""
    target = raw.strip()
    if not target:
        return None
    if target.startswith("/"):
        # Absolute paths in docs are unusual — treat as repo-relative anyway.
        target = target.lstrip("/")
        candidate = target
    elif target.startswith(("./", "../")):
        doc_dir = Path(doc_rel).parent
        candidate = os.path.normpath((doc_dir / target).as_posix()).replace("\\", "/")
    else:
        candidate = target
    return candidate


def _scan_doc(
    doc_path: Path,
    doc_index: dict[str, str],
    dirty: set[str],
    global_sources: list[tuple[str, str, int | None]],
) -> list[dict]:
    rel = doc_path.relative_to(paths.REPO_ROOT).as_posix()
    doc_ts = _freshness(rel, dirty)
    text = doc_path.read_text(encoding="utf-8", errors="replace")

    # Index spans of backtick code-spans so wikilink hits inside them
    # (prose examples like ``[[folder/note]]``) are dropped.
    code_span_ranges = [(m.start(), m.end()) for m in CODE_SPAN_RE.finditer(text)]

    def _inside_code_span(pos: int) -> bool:
        for s, e in code_span_ranges:
            if s <= pos < e:
                return True
        return False

    signals: list[dict] = []
    seen_keys: set[tuple] = set()

    def _push(kind: str, **extra) -> None:
        key = (kind, extra.get("target"), extra.get("raw"))
        if key in seen_keys:
            return
        seen_keys.add(key)
        signals.append({"kind": kind, **extra})

    # Wikilinks
    for m in WIKILINK_RE.finditer(text):
        if _inside_code_span(m.start()):
            continue  # prose example, not a real link
        raw = m.group(1)
        resolved = _resolve_wikilink(raw, rel, doc_index)
        if resolved is None:
            _push("broken_wikilink", raw=raw)
            continue
        target_ts = _freshness(resolved, dirty)
        if target_ts is None:
            _push("broken_wikilink", raw=raw, target=resolved)
            continue
        if doc_ts is not None and target_ts > doc_ts:
            _push("wikilink_target_newer", raw=raw, target=resolved)

    # Path code-spans
    for m in PATH_REF_RE.finditer(text):
        raw = m.group(1)
        resolved = _resolve_path_ref(raw, rel)
        if resolved is None:
            continue
        # Skip self-references and obvious placeholders.
        if "<" in resolved or ">" in resolved:
            continue
        abs_resolved = paths.REPO_ROOT / resolved
        if not abs_resolved.exists():
            _push("broken_path_ref", raw=raw, target=resolved)
            continue
        target_ts = _freshness(resolved, dirty)
        if target_ts is None:
            continue
        if doc_ts is not None and target_ts > doc_ts:
            _push("path_ref_newer", raw=raw, target=resolved)

    # Global drift sources
    if doc_ts is not None:
        for src_rel, kind, src_ts in global_sources:
            if src_rel == rel:
                continue  # don't flag a global drift source against itself
            if src_ts is None:
                continue
            if src_ts > doc_ts:
                _push(kind, target=src_rel)

    return signals


def run(*, doc_globs: list[str]) -> dict:
    dirty = _git_porcelain_paths()
    docs = _iter_docs(doc_globs)
    doc_index = _build_doc_index(docs)
    global_sources: list[tuple[str, str, int | None]] = [
        (rel, kind, _freshness(rel, dirty)) for rel, kind in GLOBAL_DRIFT_SOURCES
    ]

    candidates: list[dict] = []
    for doc_path in docs:
        rel = doc_path.relative_to(paths.REPO_ROOT).as_posix()
        signals = _scan_doc(doc_path, doc_index, dirty, global_sources)
        if not signals:
            continue
        candidates.append(
            {
                "path": rel,
                "freshness": _freshness(rel, dirty),
                "dirty": rel in dirty,
                "signal_count": len(signals),
                "signals": signals,
            }
        )

    return {
        "scan_globs": doc_globs,
        "doc_count": len(docs),
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--glob",
        action="append",
        help=(
            "Override the doc glob list. Repeatable. Defaults to "
            f"{DEFAULT_DOC_GLOBS}."
        ),
    )
    args = ap.parse_args(argv)
    globs = args.glob if args.glob else list(DEFAULT_DOC_GLOBS)
    out = run(doc_globs=globs)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
