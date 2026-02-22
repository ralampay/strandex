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
