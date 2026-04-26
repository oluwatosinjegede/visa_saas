from dataclasses import dataclass
from typing import Any
from .models import VisaProgram, VisaRequirement


@dataclass
class EligibilityResult:
    eligibility_status: str
    score: int
    missing_requirements: list[str]
    risk_flags: list[str]
    recommended_next_steps: list[str]


class EligibilityEngine:
    @staticmethod
    def assess(user: Any, visa_program: VisaProgram, answers: dict[str, Any]) -> EligibilityResult:
        requirements = VisaRequirement.objects.filter(visa_program=visa_program, required=True)
        missing: list[str] = []

        for req in requirements:
            if not answers.get(req.code):
                missing.append(req.code)

        completed = max(0, requirements.count() - len(missing))
        score = int((completed / requirements.count()) * 100) if requirements.exists() else 100

        risk_flags = []
        if user.role == "APPLICANT" and score < visa_program.minimum_score:
            risk_flags.append("INSUFFICIENT_ELIGIBILITY_SCORE")

        status = "eligible" if score >= visa_program.minimum_score else "review_required"
        next_steps = [
            "Upload required documents",
            "Request consultant handoff",
        ] if status == "review_required" else ["Start visa application"]

        return EligibilityResult(
            eligibility_status=status,
            score=score,
            missing_requirements=missing,
            risk_flags=risk_flags,
            recommended_next_steps=next_steps,
        )
