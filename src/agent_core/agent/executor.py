from typing import Any, Dict, TypedDict, Optional

from agent_core.tools.registry import ToolRegistry


class ExecutionResult(TypedDict):
    tool: str
    success: bool
    output: Optional[Any]
    error: Optional[str]


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
