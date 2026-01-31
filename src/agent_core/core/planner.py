import json
import logging
from typing import Dict, Any

from agent_core.llm.client import LLMClient


class Planner:
    def __init__(self):
        self.logger = logging.getLogger("agent-core.planner")
        self.llm = LLMClient()

    def plan(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Uses an LLM to decide the next action.

        Returns:
        {
          "action": "run_tool",
          "tool": "antigravity",
          "reason": "startup sanity check"
        }
        """

        system_prompt = (
            "You are an autonomous agent planner. "
            "You must respond with ONLY valid JSON. "
            "Do not add explanations outside JSON."
        )

        user_prompt = f"""
Current agent state:
{json.dumps(state, indent=2)}

Decide the next action.

Allowed actions:
- run_tool
- idle

Allowed tools:
- antigravity

Response format (JSON only):
{{
  "action": "<action>",
  "tool": "<tool-or-null>",
  "reason": "<short reason>"
}}
"""

        response = self.llm.complete(
            system=system_prompt,
            user=user_prompt
        )

        self.logger.info(f"Planner raw response: {response}")

        plan = json.loads(response)
        return plan

