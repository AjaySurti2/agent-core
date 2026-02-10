import logging
import os
from typing import Dict, Any

from agent_core.agent.executor import ToolExecutor, MemoryAwareChainExecutor
from agent_core.agent.planner import SequentialPlanner
from agent_core.agent.llm_planner import LLMPlanner
from agent_core.agent.memory_manager import MemoryManager
from agent_core.llm.client import LLMClient
from agent_core.memory.in_memory import InMemoryStore
from agent_core.tools.registry import ToolRegistry


class SimpleAgent:
    """
    Phase 22.3 — SimpleAgent with safe LLM planner rollout.

    Planner priority:
    1. LLMPlanner (if AGENT_PLANNER=llm)
    2. SequentialPlanner (fallback / default)
    """

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)

        # -------------------------
        # Tool registry
        # -------------------------
        self.registry = ToolRegistry()
        self._register_tools()

        # -------------------------
        # Memory
        # -------------------------
        self.memory_store = InMemoryStore()
        self.memory_manager = MemoryManager(self.memory_store)

        # -------------------------
        # Executor
        # -------------------------
        tool_executor = ToolExecutor(self.registry)
        self.executor = MemoryAwareChainExecutor(
            tool_executor=tool_executor,
            memory_manager=self.memory_manager,
        )

        # -------------------------
        # Planners
        # -------------------------
        self.rule_planner = SequentialPlanner()
        self.llm_planner = LLMPlanner(
            llm=LLMClient(),
            registry=self.registry,
        )

        self.active_planner = self._select_planner()

    # -------------------------
    # Planner selection
    # -------------------------
    def _select_planner(self):
        mode = os.getenv("AGENT_PLANNER", "rule").lower()

        if mode == "llm":
            self.logger.info("Planner mode: LLM")
            return self.llm_planner

        self.logger.info("Planner mode: rule-based")
        return self.rule_planner

    # -------------------------
    # Tool registration
    # -------------------------
    def _register_tools(self):
        # Import locally to avoid circular imports
        from agent_core.tools._validate_registry import ToolA, ToolB

        self.registry.register(ToolA())
        self.registry.register(ToolB())

    # -------------------------
    # Agent loop
    # -------------------------
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("Agent started. Type 'exit' or 'quit' to stop.")

        while True:
            user_input = input("\nUser> ").strip()

            if user_input.lower() in {"exit", "quit"}:
                break

            try:
                plan = self.active_planner.build_plan(user_input)
            except Exception:
                self.logger.exception(
                    "Planner failed, falling back to SequentialPlanner"
                )
                plan = self.rule_planner.build_plan(user_input)

            results = self.executor.execute_plan(plan)

            response = {
                "input": user_input,
                "steps": results,
                "memory": self.memory_manager.get_recent(),
            }

            print("\nAgent response:")
            print(response)

        return state
