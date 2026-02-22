"""Utilities for running local GGUF models via llama-cpp-python."""
from __future__ import annotations

import os
from typing import Sequence

try:
    from llama_cpp import Llama
except ImportError as exc:  # pragma: no cover - runtime dependency guard
    raise ImportError(
        "llama-cpp-python is required for llama_runner. Install it and try again."
    ) from exc


def load_llama_from_env() -> Llama:
    model_path = os.getenv("STRANDEX_LLAMA_MODEL_PATH")
    if not model_path:
        raise ValueError(
            "Set STRANDEX_LLAMA_MODEL_PATH to the local GGUF model file."
        )

    cpu_count = os.cpu_count() or 8
    default_threads = max(1, cpu_count - 2)
    n_ctx = int(os.getenv("STRANDEX_LLAMA_CTX", "4096"))
    n_threads = int(os.getenv("STRANDEX_LLAMA_THREADS", str(default_threads)))
    n_gpu_layers = int(os.getenv("STRANDEX_LLAMA_GPU_LAYERS", "0"))
    return Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_threads=n_threads,
        n_gpu_layers=n_gpu_layers,
    )


def llama_complete(
    llm: Llama,
    prompt: str,
    max_tokens: int,
    temperature: float = 0.2,
    stop: Sequence[str] | None = None,
) -> str:
    response = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=list(stop) if stop else None,
    )
    return response["choices"][0]["text"].strip()
