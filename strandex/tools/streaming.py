"""Streaming helpers for CLI output."""
from __future__ import annotations

import os
from typing import Iterable

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown


def stream_enabled() -> bool:
    return os.getenv("STRANDEX_STREAM", "1").lower() in {"1", "true", "yes", "on"}


def stream_markdown(tokens: Iterable[str], console: Console | None = None) -> str:
    """Render streaming Markdown in a Rich Live panel and return final text."""
    console = console or Console(stderr=True)
    collected: list[str] = []
    with Live(Markdown(""), console=console, refresh_per_second=8, transient=True) as live:
        for token in tokens:
            collected.append(token)
            live.update(Markdown("".join(collected)))
    return "".join(collected).strip()
