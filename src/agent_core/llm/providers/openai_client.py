import os
import json
from typing import Dict, Any

from openai import OpenAI
from agent_core.llm.base import LLMClient


class OpenAIClient(LLMClient):

    def __init__(self):
        self.model = os.getenv("AGENT_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def plan(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = """
You are an AI planning agent.

Return ONLY valid JSON.

Available tool:
- antigravity → launches the Antigravity desktop app

Format:
{
  "action": "run_tool" | "idle",
  "tool": "antigravity",
  "arguments": {}
}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except Exception:
            return {"action": "idle", "reason": "invalid_llm_output"}
