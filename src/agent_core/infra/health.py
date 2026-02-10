# agent_core/infra/health.py
from typing import Dict, Any

from agent_core import __version__
from agent_core.infra.config import AgentConfig


def health_check() -> Dict[str, Any]:
    """
    Lightweight readiness signal.
    No side effects.
    Safe for CI, Docker, and monitoring.
    """

    try:
        config = AgentConfig.load()
        planner_enabled = config.agent_planner_enabled
        model = config.agent_model
    except Exception:
        # Health should never crash
        planner_enabled = False
        model = "unknown"

    return {
        "status": "ok",
        "version": __version__,
        "planner_enabled": planner_enabled,
        "model": model,
        "memory": "in_memory",
        "tools": ["antigravity"],
    }

