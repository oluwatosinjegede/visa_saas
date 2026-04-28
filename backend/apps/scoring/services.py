import json
import os
from typing import Any

from openai import OpenAI


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)

def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"yes", "true", "1"}
    return bool(value)


def _approval_band_from_refusal_probability(refusal_probability: float) -> str:
    success_probability = 100 - refusal_probability
    if success_probability >= 80:
        return "High"
    if success_probability >= 65:
        return "Moderate"
    if success_probability >= 50:
        return "Low"
    return "Very Low"


def _build_heuristic_prediction(score: float, refusal_risks: list[str]) -> dict[str, Any]:
    critical_terms = {
        "deportation",
        "overstay",
        "false documents",
        "misrepresentation",
        "previous visa refusal",
    }
    critical_hits = sum(1 for risk in refusal_risks if any(term in risk.lower() for term in critical_terms))
    refusal_probability = max(5.0, min(95.0, round((100 - score) + (critical_hits * 8), 2)))

    return {
        "refusal_probability": refusal_probability,
        "risk_category": "High" if refusal_probability >= 60 else "Medium" if refusal_probability >= 35 else "Low",
        "key_drivers": refusal_risks[:5],
        "narrative": "Heuristic fallback was used because AI refusal prediction is unavailable.",
    }


def predict_refusal_with_ai(questionnaire: dict[str, Any], refusal_risks: list[str], score: float):
    client = get_openai_client()

    if client is None:
        return _build_heuristic_prediction(score, refusal_risks)

    try:
        response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an immigration risk analyst. Return only JSON with keys: "
                    "refusal_probability (number 0-100), risk_category, key_drivers (array), narrative."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Base score: {score}. Preliminary refusal risks: {refusal_risks}. "
                    f"Questionnaire payload: {json.dumps(questionnaire)[:6000]}"
                ),
            },
        ],
    )

        content = response.choices[0].message.content or "{}"

        data = json.loads(content)
        refusal_probability = max(0.0, min(100.0, float(data.get("refusal_probability", 50))))
        key_drivers = data.get("key_drivers") if isinstance(data.get("key_drivers"), list) else refusal_risks[:5]
        return {
            "refusal_probability": round(refusal_probability, 2),
            "risk_category": data.get("risk_category") or ("High" if refusal_probability >= 60 else "Medium" if refusal_probability >= 35 else "Low"),
            "key_drivers": key_drivers,
            "narrative": data.get("narrative") or "AI-generated refusal prediction.",
        }
    except Exception:
        return _build_heuristic_prediction(score, refusal_risks)


def assess_questionnaire(questionnaire: dict[str, Any]) -> dict[str, Any]:
    score = 100.0
    refusal_risks: list[str] = []
    recommendations: list[str] = []
    critical_flags = 0

    if not _truthy(questionnaire.get("valid_passport")):
        score -= 35
        critical_flags += 1
        refusal_risks.append("No valid passport available.")
        recommendations.append("Renew or obtain a valid passport before visa submission.")

    if _truthy(questionnaire.get("has_overstay_history")):
        score -= 30
        critical_flags += 1
        refusal_risks.append("History of overstay identified.")
        recommendations.append("Provide a detailed legal explanation and evidence of compliance since the incident.")

    if _truthy(questionnaire.get("has_deportation_history")):
        score -= 40
        critical_flags += 1
        refusal_risks.append("Deportation/removal history increases inadmissibility concerns.")
        recommendations.append("Attach legal records and professional representation for prior deportation case.")

    if _truthy(questionnaire.get("has_previous_visa_refusal")):
        score -= 20
        refusal_risks.append("Previous visa refusal may impact credibility.")
        recommendations.append("Address prior refusal reasons directly with documentary evidence.")

    if _truthy(questionnaire.get("used_false_documents")):
        score -= 60
        critical_flags += 1
        refusal_risks.append("False documents disclosed.")
        recommendations.append("Do not re-submit until all records are corrected and legal counsel is engaged.")

    if _truthy(questionnaire.get("misrepresented_information")):
        score -= 60
        critical_flags += 1
        refusal_risks.append("Misrepresentation disclosed.")
        recommendations.append("Provide a corrective statement and legal guidance before filing again.")

    if not _truthy(questionnaire.get("trip_aligned_with_career")):
        score -= 15
        refusal_risks.append("Travel purpose appears inconsistent with education/career profile.")
        recommendations.append("Strengthen statement of purpose to show clear academic/career progression.")

    bank_balance = _safe_int(questionnaire.get("current_bank_balance"))
    monthly_inflow = _safe_int(questionnaire.get("average_monthly_inflow"))
    if bank_balance < 3000:
        score -= 15
        refusal_risks.append("Low available funds for travel plan.")
        recommendations.append("Improve available liquid balance and submit updated bank evidence.")
    if monthly_inflow < 500:
        score -= 10
        refusal_risks.append("Weak recurring income pattern.")
        recommendations.append("Show stable six-month income inflows aligned with declared occupation.")

    if _truthy(questionnaire.get("has_large_recent_deposits")) and not questionnaire.get("large_deposit_explanation"):
        score -= 15
        refusal_risks.append("Unexplained large recent deposits.")
        recommendations.append("Provide source-of-funds proof for all recent large deposits.")

    if not _truthy(questionnaire.get("has_tax_records")):
        score -= 8
        refusal_risks.append("Tax records unavailable.")
        recommendations.append("Add tax returns or equivalent fiscal records to support financial credibility.")

    if not _truthy(questionnaire.get("owns_property_home_country")):
        score -= 6
        refusal_risks.append("Limited property-based ties to home country.")

    if not _truthy(questionnaire.get("has_permanent_job_or_business")):
        score -= 10
        refusal_risks.append("Weak employment/business ties in home country.")

    if not _truthy(questionnaire.get("has_approved_leave")):
        score -= 6
        refusal_risks.append("No evidence of approved leave from current work.")

    if not _truthy(questionnaire.get("spouse_in_home_country")) and not _truthy(questionnaire.get("children_in_school_home_country")):
        score -= 5
        refusal_risks.append("Limited family-based return incentives identified.")

    if not _truthy(questionnaire.get("documents_verifiable")):
        score -= 20
        critical_flags += 1
        refusal_risks.append("Document verifiability concerns.")
        recommendations.append("Ensure all submitted records are verifiable and traceable to issuing authorities.")

    if _truthy(questionnaire.get("document_inconsistencies")):
        score -= 20
        critical_flags += 1
        refusal_risks.append("Inconsistencies across documents.")
        recommendations.append("Resolve inconsistencies across forms, financials, and supporting evidence.")

    purpose_text = str(questionnaire.get("purpose_explanation", "")).strip()
    if len(purpose_text) < 80:
        score -= 8
        refusal_risks.append("Purpose of travel explanation lacks detail.")
        recommendations.append("Provide a specific, evidence-backed purpose narrative.")

    statement_of_intent = str(questionnaire.get("statement_of_intent", "")).strip()
    if len(statement_of_intent) < 120:
        score -= 8
        refusal_risks.append("Statement of intent is underdeveloped.")
        recommendations.append("Expand your statement of intent with return strategy and long-term plan.")

    score = max(0.0, min(100.0, round(score, 2)))
    ai_refusal_prediction = predict_refusal_with_ai(questionnaire, refusal_risks, score)
    refusal_probability = float(ai_refusal_prediction.get("refusal_probability", 50))
    refusal_risk_level = ai_refusal_prediction.get("risk_category", "Medium")
    approval_probability = _approval_band_from_refusal_probability(refusal_probability)

    return {
        "score": score,
        "approval_probability": approval_probability,
        "refusal_risk_level": refusal_risk_level,
        "refusal_risks": refusal_risks,
        "recommendations": recommendations[:10],
        "ai_refusal_prediction": ai_refusal_prediction,
    }


def analyze_application(profile, sop_text):
    client = get_openai_client()

    if client is None:
        return {
            "score": 0,
            "approval_probability": "Unknown",
            "strengths": ["Profile received"],
            "weaknesses": ["OPENAI_API_KEY is not configured"],
            "recommendations": ["Set OPENAI_API_KEY to enable AI analysis"],
        }

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Return only valid JSON with these keys: "
                    "score, approval_probability, strengths, weaknesses, recommendations."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Profile: "
                    f"age={getattr(profile, 'age', None)}, "
                    f"country={getattr(profile, 'country', None)}, "
                    f"education={getattr(profile, 'education_level', None)}, "
                    f"experience={getattr(profile, 'work_experience', None)}. "
                    f"SOP: {(sop_text or '')[:4000]}"
                ),
            },
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "approval_probability": "Unknown",
            "strengths": [],
            "weaknesses": ["AI parsing failed"],
            "recommendations": [],
        }