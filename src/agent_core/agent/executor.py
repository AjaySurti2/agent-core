from typing import Any, Dict, TypedDict, Optional, List
from contextlib import contextmanager
import signal

from agent_core.tools.registry import ToolRegistry
from agent_core.agent.memory_manager import MemoryManager


# -----------------------------
# Execution Result Schema
# -----------------------------

class ExecutionResult(TypedDict):
    tool: str
    success: bool
    output: Optional[Any]
    error: Optional[str]


# -----------------------------
# Timeout Utilities (Phase 23.2)
# -----------------------------

class ToolTimeoutError(Exception):
    pass


@contextmanager
def time_limit(seconds: int):
    """
    Enforces a hard execution timeout.
    Linux / WSL-safe. Raises ToolTimeoutError.
    """
    def handler(signum, frame):
        raise ToolTimeoutError("Tool execution timed out")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)


# -----------------------------
# Single Tool Executor (Phase 18 → Hardened)
# -----------------------------

class ToolExecutor:
    """
    Executes a single tool safely.
    Never raises; always returns ExecutionResult.
    """

    DEFAULT_TIMEOUT_SECONDS = 10  # ⏱ production-safe default

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> ExecutionResult:
        try:
            tool = self.registry.get(tool_name)

            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments must be a dict")

            # ---- TIME-BOUND EXECUTION ----
            with time_limit(self.DEFAULT_TIMEOUT_SECONDS):
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
    """
    Executes a deterministic sequence of tool calls.
    Stops immediately on first failure.
    """

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


# -----------------------------
# Memory-Aware Chain Executor (Phase 20)
# -----------------------------

class MemoryAwareChainExecutor(ChainExecutor):
    """
    Executes a plan and records every execution result into memory.
    """

    def __init__(
        self,
        tool_executor: ToolExecutor,
        memory_manager: MemoryManager,
    ):
        super().__init__(tool_executor)
        self.memory_manager = memory_manager

    def execute_plan(self, plan: Dict[str, Any]) -> List[ExecutionResult]:
        results = super().execute_plan(plan)

        for record in results:
            self.memory_manager.record_execution(record)

        return results


