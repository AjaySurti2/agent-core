from typing import Dict, Any, TypedDict
from abc import ABC, abstractmethod

from agent_core.tools.registry import ToolRegistry


class ToolDecision(TypedDict):
    tool: str
    arguments: Dict[str, Any]


class BaseRouter(ABC):
    @abstractmethod
    def route(self, user_input: str) -> ToolDecision:
        pass


class KeywordRouter(BaseRouter):
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def route(self, user_input: str) -> ToolDecision:
        text = user_input.lower()

        for tool in self.registry.list():
            for keyword in getattr(tool, "keywords", []):
                if keyword.lower() in text:
                    return {
                        "tool": tool.name,
                        "arguments": {}
                    }

        raise ValueError("No suitable tool found for input")
