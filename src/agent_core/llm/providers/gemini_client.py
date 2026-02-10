import os
import json
import re
from typing import Dict, Any

from google import genai
from agent_core.llm.base import LLMClient


class GeminiClient(LLMClient):
    """
    Gemini planning client using google-genai SDK.
    Includes robust JSON extraction to handle extra text in responses.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=api_key)

        # Use model that exists in your account
        self.model = os.getenv("AGENT_MODEL", "gemini-2.5-flash")

    def plan(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = """
You are an AI planning agent.

Available tool:
- antigravity → launches the Antigravity desktop app

Return ONLY valid JSON.
Do NOT include explanation.
Do NOT include markdown.
Do NOT include extra text.

Format:
{
  "action": "run_tool" | "idle",
  "tool": "antigravity",
  "arguments": {}
}
"""

        full_prompt = f"{system_prompt}\n\nUser request:\n{prompt}"

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt
        )

        text = (response.text or "").strip()

        # --- Robust JSON extraction ---
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass

        # Safe fallback
        return {
            "action": "idle",
            "reason": "invalid_llm_output"
        }
