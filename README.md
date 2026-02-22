# Strandex

A lightweight Python CLI for running modular agents.

## Setup

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Environment Variables

This project uses dotenv files. Copy `.env.dist` to `.env` and update values.

## Research Summarizer Setup

This agent runs a local GGUF model with `llama-cpp-python` and reads PDFs with `pypdf`.

Required:
- Download a GGUF model file.
- Set the model path via `STRANDEX_LLAMA_MODEL_PATH`.

Optional tuning:
- `STRANDEX_LLAMA_CTX` (context length, default `4096`)
- `STRANDEX_LLAMA_THREADS` (CPU threads, default `8`)
- `STRANDEX_LLAMA_GPU_LAYERS` (GPU offload layers, default `0`)

## Shared Tools

Reusable tools live in `strandex/tools` so new agents can share functionality:
- `strandex/tools/pdf_reader.py`: PDF text extraction.
- `strandex/tools/llama_runner.py`: Local GGUF loading and completion helpers.

## Run an Agent

```bash
python -m strandex run hello_agent --input "some prompt"
```

```bash
STRANDEX_LLAMA_MODEL_PATH=/path/to/model.gguf \\
python -m strandex run research_summarizer --input "/path/to/document.pdf"
```

## List Agents

```bash
python -m strandex list
