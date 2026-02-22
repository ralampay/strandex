"""Command-line interface for Strandex."""
from __future__ import annotations

import argparse

from dotenv import load_dotenv

from .registry import list_agents, load_agent


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="strandex")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List available agents")

    run_parser = subparsers.add_parser("run", help="Run an agent")
    run_parser.add_argument("agent_name", help="Name of the agent")
    run_parser.add_argument("--input", "-i", required=True, help="Input text")

    args = parser.parse_args()

    if args.command == "list":
        agents = list_agents()
        print("\nAvailable Agents:")
        for agent in agents:
            line = f" - {agent['name']}"
            if agent.get("description"):
                line += f": {agent['description']}"
            print(line)
        return 0

    if args.command == "run":
        agent = load_agent(args.agent_name)
        result = agent.run(args.input)
        print("\nResult:")
        print(result)
        return 0

    parser.print_help()
    return 1
