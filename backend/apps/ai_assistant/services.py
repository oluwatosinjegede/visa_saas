IMMIGRATION_DISCLAIMER = (
    "This platform provides general immigration guidance and decision-support only. "
    "It does not replace legal advice from a licensed immigration lawyer or regulated consultant."
)


class AIResponseService:
    @staticmethod
    def wrap_with_disclaimer(content: str) -> str:
        return f"{content}\n\n{IMMIGRATION_DISCLAIMER}"
