import time
from agent_core.core.agent import Agent

class SimpleAgent(Agent):
    def step(self):
        self.memory.add("heartbeat")
        self.logger.info(f"memory contents: {self.memory.get_all()}")
        time.sleep(3)
        self.shutdown()
