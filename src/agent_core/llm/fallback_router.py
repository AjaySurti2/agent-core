class ProviderFallbackRouter:
    """
    Phase 24.4 — Provider Fallback Router

    Tries multiple providers in priority order until one succeeds.
    Adapts to different provider method names:
        - plan(prompt, state)
        - generate(prompt)
        - invoke(prompt)
    """

    def __init__(self, providers):
        if not providers:
            raise ValueError("ProviderFallbackRouter requires at least one provider")

        self.providers = providers

    def plan(self, prompt, state):
        """
        Main entrypoint used by LLMPlanner.
        """
        last_error = None

        for provider in self.providers:
            name = provider.__class__.__name__

            try:
                print(f"[Router] Trying {name}")

                # Preferred interface
                if hasattr(provider, "plan"):
                    result = provider.plan(prompt, state)

                # Fallback to generate()
                elif hasattr(provider, "generate"):
                    result = provider.generate(prompt)

                # Fallback to invoke()
                elif hasattr(provider, "invoke"):
                    result = provider.invoke(prompt)

                else:
                    raise RuntimeError(
                        f"{name} has no supported method (plan/generate/invoke)"
                    )

                # Validate non-empty result
                if result is not None and str(result).strip():
                    print(f"[Router] Success from {name}")
                    return result

                print(f"[Router] Empty result from {name}, trying next provider")

            except Exception as e:
                print(f"[Router] Failed {name}: {e}")
                last_error = e

        raise RuntimeError("All providers failed in fallback router") from last_error


