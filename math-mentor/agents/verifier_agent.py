import json
from config import model

def verify_solution(problem, solution):

    prompt = f"""
You are a math verifier.

Check if the solution is correct.

Problem:
{problem}

Solution:
{solution}

Return ONLY JSON:

{{
 "confidence": number between 0 and 1,
 "issues": "none or explanation"
}}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    text = text.replace("```json", "").replace("```", "")

    try:
        return json.loads(text)
    except:
        return {"confidence": 0.5, "issues": "verification failed"}