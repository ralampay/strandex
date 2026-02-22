"""Command-line interface for Strandex."""
from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from rich.markdown import Markdown

from .registry import list_agents, load_agent


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="strandex")
    parser.add_argument(
        "--log-level",
        default=os.getenv("STRANDEX_LOG_LEVEL", "INFO"),
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List available agents")

    run_parser = subparsers.add_parser("run", help="Run an agent")
    run_parser.add_argument("agent_name", help="Name of the agent")
    run_parser.add_argument("--input", "-i", required=True, help="Input text")

    args = parser.parse_args()

    log_level = str(args.log_level).upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    logger = logging.getLogger("strandex")
    console = Console(stderr=True)

    def _total_memory_gb() -> Optional[float]:
        try:
            page_size = os.sysconf("SC_PAGE_SIZE")
            phys_pages = os.sysconf("SC_PHYS_PAGES")
        except (AttributeError, ValueError):
            return None
        if not isinstance(page_size, int) or not isinstance(phys_pages, int):
            return None
        return (page_size * phys_pages) / (1024 ** 3)

    cpu_count = os.cpu_count() or 0
    mem_gb = _total_memory_gb()
    if mem_gb is None:
        logger.info("System capacity: %s CPU cores detected.", cpu_count)
    else:
        logger.info(
            "System capacity: %s CPU cores, %.1f GB RAM detected.",
            cpu_count,
            mem_gb,
        )

    model_path = os.getenv("STRANDEX_LLAMA_MODEL_PATH")
    if model_path:
        logger.info("LLM model: %s", os.path.abspath(model_path))

    if args.command == "list":
        logger.info("Listing available agents.")
        agents = list_agents()
        print("\nAvailable Agents:")
        for agent in agents:
            line = f" - {agent['name']}"
            if agent.get("description"):
                line += f": {agent['description']}"
            print(line)
        return 0

    if args.command == "run":
        with console.status(f"Loading agent '{args.agent_name}'...", spinner="dots"):
            agent = load_agent(args.agent_name)
        logger.info("Loaded agent '%s'.", args.agent_name)
        result = agent.run(args.input)
        logger.info("Completed agent '%s'.", args.agent_name)
        print("\nResult:")
        render_markdown = os.getenv("STRANDEX_RENDER_MARKDOWN", "1").lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        if render_markdown:
            console.print(Markdown(result))
        else:
            print(result)
        return 0

    parser.print_help()
    return 1
