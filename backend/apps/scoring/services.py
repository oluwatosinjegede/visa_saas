from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


import json

def analyze_application(profile, sop_text):
    response = client.chat.completions.create(...)

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "score": 0,
            "approval_probability": "Unknown",
            "strengths": [],
            "weaknesses": ["AI parsing failed"],
            "recommendations": []
        }