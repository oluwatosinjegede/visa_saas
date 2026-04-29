import os

IMMIGRATION_DISCLAIMER = (
    "This platform provides general immigration guidance and decision-support only. "
    "It does not replace legal advice from a licensed immigration lawyer or regulated consultant."
)


class AIResponseService:
    @staticmethod
    def wrap_with_disclaimer(content: str) -> str:
        return f"{content}\n\n{IMMIGRATION_DISCLAIMER}"


class AIHealthService:
    @staticmethod
    def status() -> dict:
        api_key = os.getenv("OPENAI_API_KEY", "")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        fallback_model = os.getenv("OPENAI_FALLBACK_MODEL", "gpt-4.1-mini")
        return {
            "provider": "openai",
            "configured": bool(api_key),
            "model": model,
            "fallback_model": fallback_model,
            "api_key_source": "OPENAI_API_KEY",
        }