import os
from agent_core.llm.fallback_router import ProviderFallbackRouter


def get_llm_client(provider: str | None = None):
    """
    Factory for constructing LLM clients.

    Supported providers:
       
        - gemini
        - openai
        - mock
        - auto   (fallback chain Gemini → OpenAI → Mock)

    If provider is None:
        Read from ENV LLM_PROVIDER
        Default = auto
    """

    # Allow old calls: get_llm_client()
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "auto")

    provider = provider.lower()
    print(f"[Factory] Requested provider = {provider}")

    # -----------------------------
    # MOCK PROVIDER
    # -----------------------------
    if provider == "mock":
        from agent_core.llm.providers.mock import MockClient
        return MockClient()

    # -----------------------------
    # OPENAI PROVIDER
    # -----------------------------
    if provider == "openai":
        try:
            from agent_core.llm.providers.openai_client import OpenAIClient
            return OpenAIClient()
        except ImportError as e:
            raise RuntimeError(
                "OpenAI provider selected but openai_client.py missing "
                "or openai package not installed."
            ) from e

    # -----------------------------
    # GEMINI PROVIDER
    # -----------------------------
    if provider == "gemini":
        try:
            from agent_core.llm.providers.gemini_client import GeminiClient
            return GeminiClient()
        except ImportError as e:
            raise RuntimeError(
                "Gemini provider selected but gemini_client.py missing "
                "or google-generativeai not installed."
            ) from e

    # -----------------------------
    # AUTO FALLBACK MODE (Phase 24.4)
    # -----------------------------
    if provider == "auto":
        clients = []

        # Priority 1 — OpenAI
        try:
            from agent_core.llm.providers.openai_client import OpenAIClient
            clients.append(OpenAIClient())
        except Exception as e:
            print(f"[Factory] OpenAI unavailable: {e}")

        # Priority 2 — Gemini
        try:
            from agent_core.llm.providers.gemini_client import GeminiClient
            clients.append(GeminiClient())
        except Exception as e:
            print(f"[Factory] Gemini unavailable: {e}")

        # Priority 3 — Mock (guaranteed fallback)
        try:
            from agent_core.llm.providers.mock import MockClient
            clients.append(MockClient())
        except Exception as e:
            print(f"[Factory] Mock unavailable: {e}")

        if not clients:
            raise RuntimeError("No LLM providers could be initialized.")

        print("[Factory] Using AUTO fallback router")
        return ProviderFallbackRouter(clients)

    # -----------------------------
    # UNKNOWN PROVIDER
    # -----------------------------
    raise ValueError(
        f"Unsupported LLM provider: '{provider}'. "
        f"Valid options: mock | openai | gemini | auto"
    )


