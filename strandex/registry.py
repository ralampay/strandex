"""Agent registry and loader."""
from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from .config import load_agent_config

AGENTS_PATH = Path(__file__).parent / "agents"


def _load_agent_config(agent_name: str) -> dict:
    config_path = AGENTS_PATH / agent_name / "config.json"
    config = load_agent_config(config_path)
    return {"name": config.name, "description": config.description}


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
