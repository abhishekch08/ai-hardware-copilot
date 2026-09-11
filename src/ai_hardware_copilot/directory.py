"""Load and validate the compiled specialist directory."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import yaml

from .models import AgentConfig


class AgentDirectory:
    def __init__(self, agents: Iterable[AgentConfig]):
        self._agents: dict[str, AgentConfig] = {}
        for agent in agents:
            if agent.agent_id in self._agents:
                raise ValueError(f"duplicate agent_id: {agent.agent_id}")
            self._agents[agent.agent_id] = agent
        if not self._agents:
            raise ValueError("agent directory is empty")

    @classmethod
    def from_directory(cls, path: str | Path) -> "AgentDirectory":
        root = Path(path)
        agents: list[AgentConfig] = []
        for file_path in sorted(root.glob("*.yaml")):
            with file_path.open("r", encoding="utf-8") as handle:
                value = yaml.safe_load(handle)
            if not isinstance(value, dict):
                raise ValueError(f"{file_path} does not contain a mapping")
            agent = AgentConfig.from_dict(value)
            expected = f"{agent.agent_id}.yaml"
            if file_path.name != expected:
                raise ValueError(f"{file_path}: expected filename {expected}")
            agents.append(agent)
        return cls(agents)

    def __len__(self) -> int:
        return len(self._agents)

    def __iter__(self):
        return iter(self._agents.values())

    def get(self, agent_id: str) -> AgentConfig:
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise KeyError(f"unknown agent_id: {agent_id}") from exc

    @property
    def ids(self) -> set[str]:
        return set(self._agents)

    def in_domain(self, domain: str) -> list[AgentConfig]:
        return [agent for agent in self if domain in agent.domains]

