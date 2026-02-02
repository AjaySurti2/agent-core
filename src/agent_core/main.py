from agent_core.tools.registry import ToolRegistry
from agent_core.tools._validate_registry import ToolA, ToolB

from agent_core.agent.router import KeywordRouter
from agent_core.agent.planner import SequentialPlanner
from agent_core.agent.executor import ToolExecutor, MemoryAwareChainExecutor
from agent_core.agent.memory_manager import MemoryManager
from agent_core.memory.in_memory import InMemoryStore
from agent_core.agent.agent import Agent


def build_agent() -> Agent:
    """
    Composition root for the agent.
    Wires all components together.
    """

    # 1. Tool registry
    registry = ToolRegistry()
    registry.register(ToolA())
    registry.register(ToolB())

    # 2. Router (deterministic for now)
    router = KeywordRouter(registry)

    # 3. Planner (deterministic chaining)
    planner = SequentialPlanner()

    # 4. Executor + memory
    tool_executor = ToolExecutor(registry)
    memory_store = InMemoryStore()
    memory_manager = MemoryManager(memory_store)
    executor = MemoryAwareChainExecutor(tool_executor, memory_manager)

    # 5. Agent
    return Agent(
        router=router,
        planner=planner,
        executor=executor,
        memory_manager=memory_manager,
    )


def main():
    agent = build_agent()

    print("Agent started. Type 'exit' or 'quit' to stop.")

    while True:
        user_input = input("\nUser> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        response = agent.run(user_input)
        print("\nAgent response:")
        print(response)


if __name__ == "__main__":
    main()
