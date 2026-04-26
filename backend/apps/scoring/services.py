import json
import os
from openai import OpenAI


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)


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