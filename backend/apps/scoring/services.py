from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_application(profile, sop_text):
    if not os.getenv("OPENAI_API_KEY"):
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
                "content": "Return a JSON object with score, approval_probability, strengths, weaknesses, recommendations.",
            },
            {
                "role": "user",
                "content": f"Profile: age={profile.age}, country={profile.country}, education={profile.education_level}, experience={profile.work_experience}. SOP: {sop_text[:4000]}",
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content or "{}"

    try:
        return json.loads(content)
    except Exception:
        return {
            "score": 0,
            "approval_probability": "Unknown",
            "strengths": [],
            "weaknesses": ["AI parsing failed"],
            "recommendations": []
        }