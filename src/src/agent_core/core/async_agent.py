import asyncio
import logging
import signal
from agent_core.memory.in_memory import InMemoryMemory

class AsyncAgent:
    def __init__(self, name: str):
        self.name = name
        self.running = False
        self.logger = logging.getLogger(self.name)
        self.memory = InMemoryMemory()

    async def setup(self):
        pass

    async def step(self):
        raise NotImplementedError

    async def shutdown(self):
        self.logger.info("shutdown initiated")
        self.running = False

    def _handle_signal(self, signum, frame):
        self.logger.info(f"received signal {signum}")
        asyncio.create_task(self.shutdown())

    async def run(self):
        self.running = True

        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.shutdown()))
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self.shutdown()))

        await self.setup()
        self.logger.info("agent started")

        while self.running:
            await self.step()

        self.logger.info("agent stopped")
