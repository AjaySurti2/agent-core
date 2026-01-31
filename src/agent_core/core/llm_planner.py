import json
import os
from typing import Dict, Any

from agent_core.core.planner import Planner


class LLMPlanner(Planner):
    def __init__(self):
        self.model = os.getenv("AGENT_MODEL", "gpt-4o-mini")

    def plan(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        TEMP deterministic logic (LLM-ready).
        Replace body with real LLM call later.
        """

        task_count = state.get("task_count", 0)

        if task_count < 3:
            return {
                "action": "run_tool",
                "tool": "antigravity",
                "reason": "periodic sanity check"
            }

        return {
            "action": "idle",
            "reason": "no action needed"
        }
