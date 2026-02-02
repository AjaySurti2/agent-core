from typing import Any, Dict, List

from agent_core.agent.executor import MemoryAwareChainExecutor
from agent_core.agent.planner import SequentialPlanner
from agent_core.agent.router import BaseRouter
from agent_core.agent.memory_manager import MemoryManager


class Agent:
    """
    Full agent loop:
    route → plan → execute → store → respond
    """

    def __init__(
        self,
        router: BaseRouter,
        planner: SequentialPlanner,
        executor: MemoryAwareChainExecutor,
        memory_manager: MemoryManager,
    ):
        self.router = router
        self.planner = planner
        self.executor = executor
        self.memory_manager = memory_manager

    def run(self, user_input: str) -> Dict[str, Any]:
        # 1. Route (for now, routing influences planning implicitly)
        _ = self.router.route(user_input)

        # 2. Build execution plan
        plan = self.planner.build_plan(user_input)

        # 3. Execute plan (memory-aware)
        results = self.executor.execute_plan(plan)

        # 4. Prepare final response
        return {
            "input": user_input,
            "steps": results,
            "memory": self.memory_manager.get_recent(),
        }
