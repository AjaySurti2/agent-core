from typing import Dict, Any

from agent_core.core.planner import Planner
from agent_core.llm.factory import get_llm_client


class LLMPlanner(Planner):
    """
    Phase 24 — Pluggable LLM Planner

    Delegates planning decisions to a provider-agnostic LLM client.
    Provider is selected via:
        AGENT_LLM_PROVIDER=mock | openai | gemini
    """

    def __init__(self):
        self.client = get_llm_client()

    def plan(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        State-driven planning.

        Expected state:
        {
            "prompt": str,
            "task_count": int
        }
        """
        prompt = state.get("prompt", "")

        # Delegate decision-making to selected provider
        result = self.client.plan(prompt, state)

        # Safety guardrail: ensure minimal contract
        if not isinstance(result, dict):
            return {
                "action": "idle",
                "reason": "invalid llm response"
            }

        if "action" not in result:
            return {
                "action": "idle",
                "reason": "missing action from llm"
            }

        return result

