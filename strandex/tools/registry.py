"""Tool registry for agents."""
from __future__ import annotations

from typing import Any, Callable

from .pdf_reader import PdfReaderTool


_TOOL_FACTORIES: dict[str, Callable[[], Any]] = {
    "pdf_reader": PdfReaderTool,
}


def list_tools() -> list[str]:
    return sorted(_TOOL_FACTORIES.keys())


def get_tool(name: str):
    try:
        factory = _TOOL_FACTORIES[name]
    except KeyError as exc:
        raise KeyError(f"Unknown tool: {name}") from exc
    return factory()
