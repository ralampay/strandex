"""Utilities for extracting text from PDFs."""
from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


class PdfReaderTool:
    """Extract text from a PDF file."""

    def read(self, pdf_path: Path) -> str:
        reader = PdfReader(str(pdf_path))
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)
        return "\n".join(pages).strip()

    def metadata(self, pdf_path: Path) -> dict[str, str]:
        reader = PdfReader(str(pdf_path))
        info = reader.metadata or {}
        title = str(getattr(info, "title", "") or "")
        author = str(getattr(info, "author", "") or "")
        return {"title": title.strip(), "author": author.strip()}
