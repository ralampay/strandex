"""Shared agent configuration schema and loader."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AgentConfig:
    name: str = ""
    description: str = ""
    tools: list[str] = field(default_factory=list)
    prompts: dict[str, str] = field(default_factory=dict)


def load_agent_config(config_path: Path) -> AgentConfig:
    if not config_path.exists():
        return AgentConfig()

    try:
        with config_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError:
        return AgentConfig()

    tools = data.get("tools", [])
    if not isinstance(tools, list):
        tools = []

    prompts = data.get("prompts", {})
    if not isinstance(prompts, dict):
        prompts = {}

    return AgentConfig(
        name=str(data.get("name", "")),
        description=str(data.get("description", "")),
        tools=[str(tool) for tool in tools],
        prompts={str(key): str(value) for key, value in prompts.items()},
    )
