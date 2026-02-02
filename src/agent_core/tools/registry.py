from typing import Dict, List
from agent_core.tools.base import BaseTool


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        if not isinstance(tool, BaseTool):
            raise TypeError("Only BaseTool instances can be registered")

        if not getattr(tool, "name", None):
            raise ValueError("Tool must define a non-empty 'name'")

        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")

        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered")
        return self._tools[name]

    def list(self) -> List[BaseTool]:
        return list(self._tools.values())

    def names(self) -> List[str]:
        return list(self._tools.keys())