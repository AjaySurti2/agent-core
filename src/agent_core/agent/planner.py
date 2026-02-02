from typing import List, Dict, Any, TypedDict


class PlanStep(TypedDict):
    tool: str
    arguments: Dict[str, Any]


class ExecutionPlan(TypedDict):
    steps: List[PlanStep]

class SequentialPlanner:
    """
    Deterministic planner.
    Used for chaining tests.
    """

    def build_plan(self, user_input: str) -> ExecutionPlan:
        if "alpha then beta" in user_input.lower():
            return {
                "steps": [
                    {"tool": "tool_a", "arguments": {}},
                    {"tool": "tool_b", "arguments": {"x": 5}},
                ]
            }

        raise ValueError("Unable to build plan for input")

from typing import List
from agent_core.agent.planner import ExecutionPlan
from agent_core.agent.executor import ExecutionResult


class ChainExecutor:
    def __init__(self, tool_executor):
        self.tool_executor = tool_executor

    def execute_plan(self, plan: ExecutionPlan) -> List[ExecutionResult]:
        results: List[ExecutionResult] = []

        for step in plan["steps"]:
            result = self.tool_executor.execute(
                step["tool"],
                step.get("arguments", {}),
            )

            results.append(result)

            if not result["success"]:
                break  # stop chain on failure

        return results
