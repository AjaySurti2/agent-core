from typing import Dict, Any

from agent_core.agent.router import BaseRouter, ToolDecision
from agent_core.tools.registry import ToolRegistry
from agent_core.llm.client import BaseLLMClient


class LLMRouter(BaseRouter):
    def __init__(
        self,
        llm: BaseLLMClient,
        registry: ToolRegistry,
        fallback_router: BaseRouter,
    ):
        self.llm = llm
        self.registry = registry
        self.fallback_router = fallback_router

    def route(self, user_input: str) -> ToolDecision:
        tools_payload = []

        for tool in self.registry.list():
            tools_payload.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.input_schema,
                }
            )

        prompt = f"""
User request:
{user_input}

Available tools (JSON):
{tools_payload}

Rules:
- Choose exactly ONE tool
- Respond ONLY with valid JSON
- No explanations

Response format:
{{
  "tool": "<tool_name>",
  "arguments": {{ }}
}}
"""

        try:
            decision = self.llm.complete_json(prompt)

            # Hard validation
            if not isinstance(decision, dict):
                raise ValueError("LLM response is not a dict")

            tool_name = decision.get("tool")
            if tool_name not in self.registry.names():
                raise ValueError(f"Unknown tool '{tool_name}'")

            if "arguments" not in decision:
                decision["arguments"] = {}

            return decision  # type: ignore

        except Exception:
            # ABSOLUTE RULE: routing must never crash
            return self.fallback_router.route(user_input)
