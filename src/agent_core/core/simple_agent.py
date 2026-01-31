import logging
from typing import Dict, Any

from agent_core.core.planner import Planner
from agent_core.tools.antigravity_tool import AntigravityTool


class SimpleAgent:
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)

        self.planner = Planner()
        self.tool_registry = {
            "antigravity": AntigravityTool()
        }

    def run(self, state: Dict[str, Any]):
        """
        Execute one planning + action cycle.
        """
        plan = self.planner.plan(state)

        action = plan.get("action")
        tool_name = plan.get("tool")
        reason = plan.get("reason")

        self.logger.info(
            f"Planner decision → action={action}, tool={tool_name}, reason={reason}"
        )

        if action == "run_tool" and tool_name in self.tool_registry:
            self.tool_registry[tool_name].run()

            # Update state (memory)
            state["task_count"] = state.get("task_count", 0) + 1

        elif action == "idle":
            self.logger.info("Planner chose to idle")

        else:
            self.logger.warning(f"Unknown planner action: {plan}")

        return state

