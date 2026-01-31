from agent_core.core.base_agent import BaseAgent
from agent_core.tools.antigravity_tool import AntigravityTool

class WorkerAgent(BaseAgent):
    def __init__(self, name: str, memory):
        super().__init__(name)
        self.memory = memory
        self.tool = AntigravityTool()

    def start(self):
        self.log.info("worker started")

        count = self.memory.get("task_count") or 0
        count += 1
        self.memory.set("task_count", count)

        self.log.info(f"task_count = {count}")

        self.tool.run()

    def stop(self):
        self.log.info("worker stopped")
