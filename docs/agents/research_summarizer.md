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
