import asyncio
from agent_core.core.async_agent import AsyncAgent

class AsyncSimpleAgent(AsyncAgent):
    async def step(self):
        self.memory.add("async-heartbeat")
        self.logger.info(f"memory contents: {self.memory.get_all()}")
        await asyncio.sleep(3)
        await self.shutdown()
