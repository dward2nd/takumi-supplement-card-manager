"""Thin wrapper around the official `notion-client` SDK.

deterministic + idempotent — safe to re-run.

One client per process. Loads NOTION_TOKEN from the nearest .env
(repo root in this project); a variable already in the environment wins,
which is how a cloud session (no .env in its fresh clone) supplies it.
Uses the 2025-09-03 multi-source API: queries hit
`data_sources/{id}/query` and page parents are typed `data_source_id`.
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from notion_client import Client

from . import paths

# Load .env from the repo root regardless of which CWD invoked the script.
load_dotenv(paths.ENV_FILE)


class NotionAuthError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client() -> Client:
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise NotionAuthError(
            "NOTION_TOKEN is not set. Add it to .env at the repo root, or, in a "
            "cloud session, as an environment variable in the cloud environment's settings."
        )
    return Client(auth=token)


def query_all(data_source_id: str, **query_kwargs) -> list[dict]:
    """Paginate POST /v1/data_sources/{id}/query until exhausted.

    Accepts the same kwargs as `client.data_sources.query` (filter, sorts, page_size).
    """
    client = get_client()
    results: list[dict] = []
    start_cursor: str | None = None
    while True:
        kwargs = dict(query_kwargs)
        if start_cursor:
            kwargs["start_cursor"] = start_cursor
        resp = client.data_sources.query(data_source_id=data_source_id, **kwargs)
        results.extend(resp.get("results", []))
        if not resp.get("has_more"):
            break
        start_cursor = resp.get("next_cursor")
    return results


def query_page(data_source_id: str, *, page_size: int = 100, **query_kwargs) -> list[dict]:
    """Single-page query (no pagination). Use when you know the cap fits in `page_size`."""
    client = get_client()
    resp = client.data_sources.query(
        data_source_id=data_source_id, page_size=page_size, **query_kwargs
    )
    return resp.get("results", [])


def create_page(data_source_id: str, properties: dict, *, icon: dict | None = None) -> dict:
    """Create a row under the given data source.

    Every row gets a page icon: `icon` when the caller passes one, otherwise
    whatever `lib.icons` picks for that data source (none for the Cards DBs).
    """
    if icon is None:
        from . import icons   # late: icons reads the Cards DBs through this module
        icon = icons.for_new_page(data_source_id, properties)
    client = get_client()
    return client.pages.create(
        parent={"type": "data_source_id", "data_source_id": data_source_id},
        properties=properties,
        **({"icon": icon} if icon else {}),
    )


def set_icon(page_id: str, icon: dict) -> dict:
    """Replace a page's icon."""
    client = get_client()
    return client.pages.update(page_id=page_id, icon=icon)


def set_cover(page_id: str, cover: dict) -> dict:
    """Replace a page's cover (e.g. `{"type": "file_upload", "file_upload": {"id": …}}`)."""
    client = get_client()
    return client.pages.update(page_id=page_id, cover=cover)


def archive_page(page_id: str) -> dict:
    """Soft-delete a page (idempotent — re-archiving is a no-op)."""
    client = get_client()
    return client.pages.update(page_id=page_id, archived=True)


def update_page_properties(page_id: str, properties: dict, *, icon: dict | None = None) -> dict:
    """Patch one or more property values on an existing page (and its icon, when given)."""
    client = get_client()
    return client.pages.update(page_id=page_id, properties=properties, **({"icon": icon} if icon else {}))


def get_page(page_id: str) -> dict:
    client = get_client()
    return client.pages.retrieve(page_id=page_id)
