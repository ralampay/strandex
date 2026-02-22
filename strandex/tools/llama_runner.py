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

    model_path = os.path.abspath(model_path)

    verbose_env = os.getenv("STRANDEX_LLAMA_VERBOSE", "0").lower()
    verbose = verbose_env in {"1", "true", "yes", "on"}
    cpu_count = os.cpu_count() or 8
    default_threads = max(1, cpu_count - 2)
    n_ctx = int(os.getenv("STRANDEX_LLAMA_CTX", "4096"))
    n_threads = int(os.getenv("STRANDEX_LLAMA_THREADS", str(default_threads)))
    n_gpu_layers = int(os.getenv("STRANDEX_LLAMA_GPU_LAYERS", "0"))
    llm = Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_threads=n_threads,
        n_gpu_layers=n_gpu_layers,
        verbose=verbose,
    )
    llm.model_path = model_path
    return llm


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


def llama_stream(
    llm: Llama,
    prompt: str,
    max_tokens: int,
    temperature: float = 0.2,
    stop: Sequence[str] | None = None,
):
    response = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=list(stop) if stop else None,
        stream=True,
    )
    for chunk in response:
        token = chunk["choices"][0].get("text", "")
        if token:
            yield token
