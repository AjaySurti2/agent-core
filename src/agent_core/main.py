import logging

from agent_core.config.logging import setup_logging
from agent_core.core.simple_agent import SimpleAgent
#from agent_core.memory.file_memory import FileMemory
from agent_core.memory.in_memory import InMemoryMemory as FileMemory

def main():
    setup_logging(level="INFO")

    logging.getLogger("bootstrap").info("main() entered")

    memory = FileMemory()
    state = memory.load()

    agent = SimpleAgent(name="agent-core")
    state = agent.run(state)

    memory.save(state)


if __name__ == "__main__":
    main()

