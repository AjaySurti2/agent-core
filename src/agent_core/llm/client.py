import os
import json
from abc import ABC, abstractmethod
from typing import Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

# Load existing .env (already used in previous stages)
load_dotenv()


class BaseLLMClient(ABC):
    @abstractmethod
    def complete_json(self, prompt: str) -> Dict[str, Any]:
        """
        Must return parsed JSON.
        Must raise if JSON is invalid.
        """
        pass


class LLMClient(BaseLLMClient):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY not found. "
                "Ensure .env is configured and loaded."
            )

        self.client = OpenAI(api_key=api_key)

    def complete_json(self, prompt: str) -> Dict[str, Any]:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a tool router.\n"
                        "Rules:\n"
                        "- Respond ONLY with valid JSON\n"
                        "- No markdown\n"
                        "- No explanations\n"
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.0,  # deterministic routing
        )

        content = response.choices[0].message.content.strip()

        # Defensive cleanup (LLMs sometimes do this)
        if content.startswith("```"):
            content = content.strip("`")
            if content.lower().startswith("json"):
                content = content[4:].strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"LLM returned invalid JSON:\n{content}"
            ) from e
