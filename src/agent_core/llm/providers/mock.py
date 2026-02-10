from typing import Dict, Any
from agent_core.llm.base import LLMClient


class MockLLMClient(LLMClient):
    """
    Deterministic provider for offline/dev usage.

    Always returns a predictable plan.
    Useful for:
    - Testing executor
    - CI environments
    - No-API-key setups
    - Fallback mode
    """

    def plan(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        task_count = context.get("task_count", 0)

        # Simple deterministic behavior
        if task_count < 3:
            return {
                "action": "run_tool",
                "tool": "antigravity",
                "arguments": {},
                "reason": "mock_decision"
            }

        return {
            "action": "idle",
            "reason": "mock_idle"
        }

