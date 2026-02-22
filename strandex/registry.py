"""Agent registry and loader."""
from __future__ import annotations

import importlib
import json
import pkgutil
from pathlib import Path

AGENTS_PATH = Path(__file__).parent / "agents"


def _load_agent_config(agent_name: str) -> dict:
    config_path = AGENTS_PATH / agent_name / "config.json"
    if not config_path.exists():
        return {}

    try:
        with config_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return {}


def list_agents() -> list[dict]:
    agents = [
        name
        for _, name, ispkg in pkgutil.iter_modules([str(AGENTS_PATH)])
        if ispkg
    ]
    return [
        {"name": name, "description": _load_agent_config(name).get("description")}
        for name in agents
    ]


def load_agent(agent_name: str):
    module_path = f"strandex.agents.{agent_name}.agent"
    module = importlib.import_module(module_path)
    return module.Agent()
