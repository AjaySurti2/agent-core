from agent_core.core.llm_planner import LLMPlanner
from agent_core.memory.base import Memory
from agent_core.tools.antigravity_tool import AntigravityTool
import logging


class Supervisor:
    def __init__(self):
        self.logger = logging.getLogger("agent-core.supervisor")
        self.memory = Memory()
        self.planner = LLMPlanner()

    def run(self):
        state = self.memory.load()

        self.logger.info("supervisor started")

        plan = self.planner.plan(state)
        self.logger.info(f"plan decided: {plan}")

        if plan["action"] == "run_tool":
            tool = AntigravityTool()
            tool.run()

            state["task_count"] = state.get("task_count", 0) + 1
            self.memory.save(state)

        self.logger.info("supervisor stopping worker")
