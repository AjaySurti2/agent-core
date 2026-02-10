# agent_core/run.py
import sys

from agent_core.infra.logging import setup_logger
from agent_core.infra.config import AgentConfig, ConfigError
from agent_core.infra.health import health_check

from agent_core.core.llm_planner import LLMPlanner

from agent_core.tools.registry import ToolRegistry
from agent_core.tools.antigravity_tool import AntigravityTool
from agent_core.agent.executor import ToolExecutor, MemoryAwareChainExecutor
from agent_core.agent.memory_manager import MemoryManager
from agent_core.memory.in_memory import InMemoryStore

logger = setup_logger(__name__)


def main():
    # ------------------
    # CONFIG (FAIL FAST) — Phase 23.3
    # ------------------
    try:
        config = AgentConfig.load()
    except ConfigError as e:
        print(f"[CONFIG ERROR] {e}")
        sys.exit(1)

    # ------------------
    # HEALTH CHECK MODE — Phase 23.4
    # ------------------
    if "--health" in sys.argv:
        print(health_check())
        return

    # ------------------
    # NORMAL EXECUTION
    # ------------------
    if len(sys.argv) < 2:
        print("Usage: python -m agent_core.run '<prompt>'")
        sys.exit(1)

    prompt = sys.argv[1]
    logger.info("Agent run started")
    logger.info(f"Planner enabled: {config.agent_planner_enabled}")
    logger.info(f"Using model: {config.agent_model}")

    # ------------------
    # MEMORY
    # ------------------
    memory_store = InMemoryStore()
    memory_manager = MemoryManager(memory_store)

    # ------------------
    # TOOLS
    # ------------------
    registry = ToolRegistry()
    registry.register(AntigravityTool())

    tool_executor = ToolExecutor(registry)

    # ------------------
    # PLANNER
    # ------------------
    planner = LLMPlanner()

    state = {
        "prompt": prompt,
        "task_count": 0,
    }

    plan = planner.plan(state)
    logger.info(f"Plan generated: {plan}")

    # ------------------
    # EXECUTOR
    # ------------------
    executor = MemoryAwareChainExecutor(
        tool_executor=tool_executor,
        memory_manager=memory_manager,
    )

    if plan.get("action") == "run_tool":
        execution_plan = {
            "steps": [
                {
                    "tool": plan["tool"],
                    "arguments": {},
                }
            ]
        }
        results = executor.execute_plan(execution_plan)
        print(results)
    else:
        logger.info("Planner returned idle action")
        print(plan)

    logger.info("Agent run completed")


if __name__ == "__main__":
    main()

