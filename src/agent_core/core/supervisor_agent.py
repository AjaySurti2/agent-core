from agent_core.core.base_agent import BaseAgent
from agent_core.core.worker_agent import WorkerAgent
from agent_core.memory.file import FileMemory


class SupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__("supervisor")
        self.memory = FileMemory()
        self.workers = []

    def start(self):
        self.log.info("supervisor started")

        count = self.memory.get("task_count") or 0
        self.memory.set("task_count", count)

        worker = WorkerAgent(
            name="worker-1",
            memory=self.memory
        )
        self.workers.append(worker)

        for w in self.workers:
            w.start()

    def stop(self):
        self.log.info("supervisor stopping worker")
        for w in self.workers:
            w.stop()

