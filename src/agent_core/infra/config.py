# agent_core/infra/config.py
import os
from dataclasses import dataclass


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


def require_env(key: str) -> str:
    value = os.getenv(key)
    if value is None or value.strip() == "":
        raise ConfigError(f"Missing required environment variable: {key}")
    return value


def optional_env(key: str, default: str) -> str:
    return os.getenv(key, default)


@dataclass(frozen=True)
class AgentConfig:
    # Rollout / safety flags
    agent_planner_enabled: bool

    # LLM config
    agent_model: str

    @staticmethod
    def load() -> "AgentConfig":
        agent_planner_raw = require_env("AGENT_PLANNER")

        if agent_planner_raw not in {"0", "1"}:
            raise ConfigError("AGENT_PLANNER must be '0' or '1'")

        agent_model = optional_env(
            "AGENT_MODEL",
            "gpt-4o-mini",
        )

        return AgentConfig(
            agent_planner_enabled=(agent_planner_raw == "1"),
            agent_model=agent_model,
        )
