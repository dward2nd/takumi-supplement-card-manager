"""Semantic-version parse + bump.

deterministic + idempotent — safe to re-run.

Pure functions, no I/O, easy to test in isolation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final


BUMP_TYPES: Final[tuple[str, ...]] = ("major", "minor", "patch")

_SEMVER_RE = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")


class InvalidVersion(ValueError):
    pass


class InvalidBumpType(ValueError):
    pass


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def parse(text: str) -> Version:
    m = _SEMVER_RE.match((text or "").strip())
    if not m:
        raise InvalidVersion(
            f"not a valid semver MAJOR.MINOR.PATCH: {text!r}"
        )
    return Version(int(m["major"]), int(m["minor"]), int(m["patch"]))


def bump(v: Version, kind: str) -> Version:
    if kind == "major":
        return Version(v.major + 1, 0, 0)
    if kind == "minor":
        return Version(v.major, v.minor + 1, 0)
    if kind == "patch":
        return Version(v.major, v.minor, v.patch + 1)
    raise InvalidBumpType(
        f"type must be one of {BUMP_TYPES}, got {kind!r}"
    )
