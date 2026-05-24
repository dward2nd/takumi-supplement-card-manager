"""Notion file_upload helpers — create upload, send bytes, attach to pages.

deterministic + idempotent — safe to re-run. Upload objects are
short-lived (1 hour expiry) but uploading the same bytes twice is fine,
and attaching a file_upload by ID multiple times to the same property
is a no-op once Notion has materialized the file.

Notion's file-property updates are *replace* semantics: a `pages.update`
on a files property overwrites the whole list. To append, the existing
entries have to be re-included — and for already-internal files
(`type == "file"`), the signed URL expires, so we re-upload them from
the live URL before patching.

See https://developers.notion.com/reference/file-upload for the upload
lifecycle. We use the SDK to *create* the upload object (gives us the
id) but bypass it for the multipart POST — the SDK's `send` helper
serializes the file argument incorrectly.
"""

from __future__ import annotations

import mimetypes
import os
import pathlib
from typing import Any

import httpx

from . import notion_client


_API_BASE = "https://api.notion.com/v1"


def _auth_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
        "Notion-Version": "2025-09-03",
    }


def upload_file(
    path: str | pathlib.Path,
    *,
    filename: str | None = None,
    content_type: str | None = None,
) -> str:
    """Upload a local file to Notion. Returns the `file_upload` ID.

    `filename` defaults to the source file's basename; `content_type` is
    guessed from the extension if not provided.
    """
    p = pathlib.Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"no such file: {p}")

    name = filename or p.name
    ctype = content_type or mimetypes.guess_type(name)[0] or "application/octet-stream"

    client = notion_client.get_client()
    obj = client.file_uploads.create(filename=name, content_type=ctype)
    upload_id = obj["id"]

    with open(p, "rb") as fh:
        resp = httpx.post(
            f"{_API_BASE}/file_uploads/{upload_id}/send",
            headers=_auth_headers(),
            files={"file": (name, fh, ctype)},
            timeout=120.0,
        )
    resp.raise_for_status()
    status = resp.json().get("status")
    if status != "uploaded":
        raise RuntimeError(f"file_upload {upload_id!r} status={status!r}, expected 'uploaded'")
    return upload_id


def _refetch_internal_file(file_entry: dict, work_dir: pathlib.Path) -> tuple[str, str]:
    """Download a `type: file` entry's signed URL → local path. Returns (path, name)."""
    name = file_entry.get("name") or "preserved"
    url = file_entry["file"]["url"]
    dest = work_dir / name
    with httpx.stream("GET", url, timeout=120.0) as r:
        r.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in r.iter_bytes():
                fh.write(chunk)
    return str(dest), name


def append_files_to_page(
    page_id: str,
    property_name: str,
    new_files: list[str | pathlib.Path],
    *,
    work_dir: str | pathlib.Path = "/tmp",
) -> dict[str, Any]:
    """Append files to a page's files-property, preserving existing entries.

    For each existing entry:
      - `type == "file_upload"` (still pending materialization): re-pass by id.
      - `type == "external"`: re-pass the external URL.
      - `type == "file"` (already-internal, signed URL): re-download and
        re-upload as a new file_upload so the slot survives the replace.

    Returns the updated page object from Notion.
    """
    wd = pathlib.Path(work_dir)
    wd.mkdir(parents=True, exist_ok=True)

    page = notion_client.get_page(page_id)
    existing = page["properties"].get(property_name, {}).get("files", [])

    files_payload: list[dict] = []
    for f in existing:
        kind = f.get("type")
        if kind == "file_upload":
            files_payload.append(
                {"type": "file_upload", "file_upload": {"id": f["file_upload"]["id"]}, "name": f["name"]}
            )
        elif kind == "external":
            files_payload.append(
                {"type": "external", "external": {"url": f["external"]["url"]}, "name": f["name"]}
            )
        elif kind == "file":
            local, name = _refetch_internal_file(f, wd)
            uid = upload_file(local)
            files_payload.append(
                {"type": "file_upload", "file_upload": {"id": uid}, "name": name}
            )
        else:
            raise RuntimeError(f"unknown file entry type {kind!r} on {page_id} / {property_name}")

    for path in new_files:
        p = pathlib.Path(path)
        uid = upload_file(p)
        files_payload.append(
            {"type": "file_upload", "file_upload": {"id": uid}, "name": p.name}
        )

    return notion_client.update_page_properties(
        page_id, {property_name: {"files": files_payload}}
    )
