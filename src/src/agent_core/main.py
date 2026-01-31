import asyncio
import logging
from agent_core.config.logging import setup_logging
from agent_core.core.async_simple_agent import AsyncSimpleAgent

def main():
    setup_logging(level="INFO")
    logging.getLogger("bootstrap").info("main() entered")

    agent = AsyncSimpleAgent(name="agent-core")
    asyncio.run(agent.run())

if __name__ == "__main__":
    main()
