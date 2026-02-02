from typing import Any, Dict, TypedDict, Optional, List

from agent_core.tools.registry import ToolRegistry


# -----------------------------
# Execution Result Schema
# -----------------------------

class ExecutionResult(TypedDict):
    tool: str
    success: bool
    output: Optional[Any]
    error: Optional[str]


# -----------------------------
# Single Tool Executor (Phase 18)
# -----------------------------

class ToolExecutor:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> ExecutionResult:
        try:
            tool = self.registry.get(tool_name)

            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments must be a dict")

            result = tool.run(**arguments)

            return {
                "tool": tool_name,
                "success": True,
                "output": result,
                "error": None,
            }

        except Exception as e:
            return {
                "tool": tool_name,
                "success": False,
                "output": None,
                "error": str(e),
            }


# -----------------------------
# Chain Executor (Phase 19)
# -----------------------------

class ChainExecutor:
    def __init__(self, tool_executor: ToolExecutor):
        self.tool_executor = tool_executor

    def execute_plan(self, plan: Dict[str, Any]) -> List[ExecutionResult]:
        results: List[ExecutionResult] = []

        for step in plan.get("steps", []):
            result = self.tool_executor.execute(
                step["tool"],
                step.get("arguments", {}),
            )

            results.append(result)

            # Stop chain on first failure
            if not result["success"]:
                break

        return results
