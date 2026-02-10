from typing import Dict, Any

from agent_core.llm.client import BaseLLMClient
from agent_core.tools.registry import ToolRegistry


class LLMPlanner:
    """
    Phase 22 — LLM Planner (Hardened)
    Converts user input into an executable plan using an LLM,
    with strict guardrails against hallucination.
    """

    def __init__(
        self,
        llm: BaseLLMClient,
        registry: ToolRegistry,
    ):
        self.llm = llm
        self.registry = registry

    # -------------------------
    # Public API
    # -------------------------

    def build_plan(self, user_input: str) -> Dict[str, Any]:
        prompt = self._build_prompt(user_input)

        plan = self.llm.complete_json(prompt)

        # Guardrail: explicit refusal
        if "error" in plan:
            raise ValueError("LLM unable to build plan")

        self._validate_plan(plan)

        return plan

    # -------------------------
    # Prompt Construction
    # -------------------------

    def _build_prompt(self, user_input: str) -> str:
        tools_description = []

        for tool in self.registry.list():
            tools_description.append(
                f"- {tool.name}: {tool.description}, "
                f"arguments={list(tool.input_schema.keys())}, "
                f"keywords={tool.keywords}"
            )

        tools_text = "\n".join(tools_description)

        return f"""
You are an execution planner.

Available tools:
{tools_text}

User request:
"{user_input}"

Rules:
- ONLY use the available tools listed above.
- ONLY return valid JSON.
- If the request is unclear, ambiguous, or cannot be mapped to tools,
  respond EXACTLY with:
  {{ "error": "UNABLE_TO_PLAN" }}
- If a tool requires arguments, infer reasonable values.
- All required arguments must be included.

Valid response format:
{{
  "steps": [
    {{
      "tool": "<tool_name>",
      "arguments": {{}}
    }}
  ]
}}
"""

    # -------------------------
    # Validation
    # -------------------------

    def _validate_plan(self, plan: Dict[str, Any]) -> None:
        if not isinstance(plan, dict):
            raise ValueError("Plan must be a JSON object")

        if "steps" not in plan:
            raise ValueError("Plan missing 'steps' key")

        if not isinstance(plan["steps"], list):
            raise ValueError("'steps' must be a list")

        if not plan["steps"]:
            raise ValueError("Plan contains no steps")

        for step in plan["steps"]:
            if "tool" not in step:
                raise ValueError("Each step must include 'tool'")

            if step["tool"] not in self.registry.names():
                raise ValueError(f"Unknown tool in plan: {step['tool']}")

            if "arguments" not in step:
                step["arguments"] = {}

            if not isinstance(step["arguments"], dict):
                raise ValueError("'arguments' must be a dict")

