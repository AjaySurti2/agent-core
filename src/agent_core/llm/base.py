from abc import ABC, abstractmethod
from typing import Dict, Any


class LLMClient(ABC):
    """
    Provider-agnostic LLM interface.
    """

    @abstractmethod
    def plan(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns a planning decision dict:
        {
            "action": "run_tool" | "idle",
            "tool": "<tool_name>",
            "arguments": {}
        }
        """
        pass
