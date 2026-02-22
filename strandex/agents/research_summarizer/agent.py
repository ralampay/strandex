"""Agent that summarizes PDF research documents using a local LLM."""
from __future__ import annotations

from pathlib import Path

from strandex.tools.llama_runner import load_llama_from_env, llama_complete
from strandex.tools.pdf_reader import PdfReaderTool


class Agent:
    def __init__(self) -> None:
        self._pdf_tool = PdfReaderTool()

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
            prompt = (
                "You are a research assistant. Summarize the following text "
                "for concise research notes. Focus on key claims, evidence, "
                "and conclusions.\n\nText:\n"
                f"{chunk}\n\nSummary:\n"
            )
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
        prompt = (
            "You are a research assistant. Combine the notes into a clear "
            "summary with 3-6 bullet points plus a short paragraph overview.\n\n"
            "Notes:\n"
            f"{combined}\n\nSummary:\n"
        )
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

        llm = load_llama_from_env()
        chunks = self._chunk_text(text)
        summaries = self._summarize_chunks(llm, chunks)
        return self._summarize_final(llm, summaries)
