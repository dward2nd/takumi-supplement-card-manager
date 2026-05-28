"""Plain-text extraction from a (possibly password-encrypted) PDF.

deterministic + idempotent — same PDF + same password → same text.

Thin wrapper around `pdfplumber`. Bank statements vary wildly in layout
across issuers, so we deliberately stop at "text per page" and leave row
parsing to the caller (an AI agent reading the text, or a per-issuer
parser written later). Encryption is handled here via `password=`,
since several Thai bank statements arrive AES-encrypted with the
holder's national ID.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pdfplumber


@dataclass(frozen=True)
class PdfText:
    pages: list[str]

    @property
    def text(self) -> str:
        return "\n".join(self.pages)

    def joined(self, sep: str = "\n") -> str:
        out: list[str] = []
        for i, t in enumerate(self.pages, 1):
            out.append(f"===== Page {i} =====")
            out.append(t.rstrip())
        return sep.join(out)


def extract(pdf_path: str | Path, password: str | None = None) -> PdfText:
    """Read every page's text from a PDF and return them in order."""
    pages: list[str] = []
    with pdfplumber.open(str(pdf_path), password=password or "") as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return PdfText(pages=pages)
