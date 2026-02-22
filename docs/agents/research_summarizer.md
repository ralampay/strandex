# research_summarizer

## Overview

Summarizes PDF research documents using a local GGUF model via `llama-cpp-python`.

## Syntax

```bash
python -m strandex run research_summarizer --input "/path/to/document.pdf"
```

## Tools

- `strandex/tools/pdf_reader.py`: Extracts text from PDF files.
- `strandex/tools/llama_runner.py`: Loads a local GGUF model and runs completions.

## Example Usage

```bash
STRANDEX_LLAMA_MODEL_PATH=/path/to/model.gguf \
python -m strandex run research_summarizer --input "/path/to/document.pdf"
```

By default, the agent writes `output-{title}.md` in the current working directory with the
paper title, author(s), and the generated analysis.

Suggested CPU-friendly models:
- `Phi-3.5-mini-instruct` (3.82B) in `Q4_K_M` for speed and lower heat.
- `Qwen2.5-7B-Instruct` in `Q4_K_M` or `Q5_K_M` for a balance of quality and speed.
- `Mistral-7B-Instruct v0.3` in `Q4_K_M` for reliable 7B performance.
