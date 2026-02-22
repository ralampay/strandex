"""Simple agent that says hello."""
from __future__ import annotations


class Agent:
    def run(self, prompt: str) -> str:
        return f"Hello from hello_agent! You said: {prompt}"
