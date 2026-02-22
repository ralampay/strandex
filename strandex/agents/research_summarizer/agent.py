"""Agent that summarizes PDF research documents using a local LLM."""
from __future__ import annotations

import json
from pathlib import Path

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from strandex.tools.llama_runner import load_llama_from_env, llama_complete
from strandex.tools.pdf_reader import PdfReaderTool


class Agent:
    def __init__(self) -> None:
        self._pdf_tool = PdfReaderTool()
        self._prompts = self._load_prompts()
        self._console = Console(stderr=True)

    def _load_prompts(self) -> dict[str, str]:
        config_path = Path(__file__).with_name("config.json")
        if not config_path.exists():
            return {}

        try:
            with config_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError:
            return {}

        prompts = data.get("prompts", {})
        if not isinstance(prompts, dict):
            return {}
        return {key: str(value) for key, value in prompts.items()}

    def _get_prompt(self, key: str, fallback: str) -> str:
        return self._prompts.get(key, fallback)

    def _guess_title_author(self, text: str) -> tuple[str, str]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        title = ""
        author = ""
        for line in lines[:6]:
            if not title and len(line) > 5:
                title = line
                continue
            lower = line.lower()
            if "author" in lower or "authors" in lower:
                author = line.replace("Authors:", "").replace("Author:", "").strip()
                break
            if not author and "," in line and len(line) < 120:
                author = line
        return title, author

    def _safe_filename(self, title: str) -> str:
        cleaned = []
        for char in title.strip():
            if char.isalnum():
                cleaned.append(char.lower())
            elif char in {" ", "-", "_"}:
                cleaned.append("-")
        slug = "".join(cleaned).strip("-")
        while "--" in slug:
            slug = slug.replace("--", "-")
        if not slug:
            return "output.md"
        return f"output-{slug[:80]}.md"

    def _write_output(
        self, output_path: Path, title: str, author: str, summary: str
    ) -> None:
        content = (
            f"# {title or 'Untitled'}\n\n"
            f"**Author(s):** {author or 'Unknown'}\n\n"
            "## Analysis\n\n"
            f"{summary}\n"
        )
        output_path.write_text(content, encoding="utf-8")

    def _chunk_text(self, text: str, chunk_size: int = 3000) -> list[str]:
        chunks = []
        start = 0
        length = len(text)
        while start < length:
            end = min(start + chunk_size, length)
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end
        return chunks

    def _summarize_chunks(self, llm, chunks: list[str]) -> list[str]:
        summaries = []
        for chunk in chunks:
            template = self._get_prompt(
                "chunk_summary",
                "You are a research assistant. Summarize the following text "
                "for concise research notes. Focus on key claims, evidence, "
                "and conclusions.\n\nText:\n{chunk}\n\nSummary:\n",
            )
            prompt = template.format(chunk=chunk)
            summary = llama_complete(
                llm,
                prompt,
                max_tokens=400,
                temperature=0.2,
                stop=["\n\nText:", "\n\nSummary:"],
            )
            summaries.append(summary)
        return summaries

    def _summarize_final(self, llm, summaries: list[str]) -> str:
        combined = "\n".join(summaries)
        template = self._get_prompt(
            "final_summary",
            "You are a research assistant. Combine the notes into a clear "
            "summary with 3-6 bullet points plus a short paragraph overview.\n\n"
            "Notes:\n{notes}\n\nSummary:\n",
        )
        prompt = template.format(notes=combined)
        return llama_complete(
            llm,
            prompt,
            max_tokens=500,
            temperature=0.2,
            stop=["\n\nNotes:", "\n\nSummary:"],
        )

    def run(self, prompt: str) -> str:
        pdf_path = Path(prompt).expanduser()
        if not pdf_path.exists():
            return f"PDF not found: {pdf_path}"
        if pdf_path.suffix.lower() != ".pdf":
            return "Input must be a .pdf file path."

        text = self._pdf_tool.read(pdf_path)
        if not text:
            return "No extractable text found in the PDF."

        metadata = self._pdf_tool.metadata(pdf_path)
        title = metadata.get("title", "")
        author = metadata.get("author", "")
        if not title or not author:
            guessed_title, guessed_author = self._guess_title_author(text)
            title = title or guessed_title
            author = author or guessed_author

        llm = load_llama_from_env()
        chunks = self._chunk_text(text)
        summaries: list[str] = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=self._console,
        ) as progress:
            task = progress.add_task("Summarizing chunk 1/1", total=len(chunks))
            for idx, chunk in enumerate(chunks, start=1):
                progress.update(
                    task, description=f"Summarizing chunk {idx}/{len(chunks)}"
                )
                summaries.append(self._summarize_chunks(llm, [chunk])[0])
                progress.advance(task)
            progress.update(task, description="Summarizing final report")
            final_summary = self._summarize_final(llm, summaries)

        output_path = Path.cwd() / self._safe_filename(title)
        self._write_output(output_path, title, author, final_summary)
        return final_summary
