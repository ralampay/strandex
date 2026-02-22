# Strandex

A lightweight Python CLI for running modular agents.

## Setup

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

The CLI uses `rich` for spinners and styled logs.

## Environment Variables

This project uses dotenv files. Copy `.env.dist` to `.env` and update values.

## Research Summarizer Setup

This agent runs a local GGUF model with `llama-cpp-python` and reads PDFs with `pypdf`.

Required:
- Download a GGUF model file.
- Set the model path via `STRANDEX_LLAMA_MODEL_PATH`.

Optional tuning:
- `STRANDEX_LLAMA_CTX` (context length, default `4096`)
- `STRANDEX_LLAMA_THREADS` (CPU threads, default `CPU cores - 2`)
- `STRANDEX_LLAMA_GPU_LAYERS` (GPU offload layers, default `0`, CPU-first)
- `STRANDEX_LLAMA_VERBOSE` (set to `1` to enable llama-cpp-python logs)

CLI logging:
- `STRANDEX_LOG_LEVEL` (default `INFO`)
- `STRANDEX_RENDER_MARKDOWN` (default `1`)
- `STRANDEX_STREAM` (default `0`)

Suggested CPU-friendly models:
- `Phi-3.5-mini-instruct` (3.82B) in `Q4_K_M` for speed and lower heat.
- `Qwen2.5-7B-Instruct` in `Q4_K_M` or `Q5_K_M` for a balance of quality and speed.
- `Mistral-7B-Instruct v0.3` in `Q4_K_M` for reliable 7B performance.

Performance tips for laptops:
- Lower `STRANDEX_LLAMA_THREADS` to reduce heat.
- Reduce `STRANDEX_LLAMA_CTX` if you don’t need long context windows.

## Shared Tools

Reusable tools live in `strandex/tools` so new agents can share functionality:
- `strandex/tools/pdf_reader.py`: PDF text extraction.
- `strandex/tools/llama_runner.py`: Local GGUF loading and completion helpers.
- `strandex/tools/streaming.py`: Rich Live Markdown streaming helpers.

## Agent Docs

See `docs/agents/README.md` for the agent documentation index.

## Run an Agent

```bash
python -m strandex run hello_agent --input "some prompt"
```

```bash
STRANDEX_LLAMA_MODEL_PATH=/path/to/model.gguf \\
python -m strandex run research_summarizer --input "/path/to/document.pdf"
```

The research summarizer writes `output-{title}.md` in the current working directory with
the paper title, author(s), and the generated analysis.

## List Agents

```bash
python -m strandex list
