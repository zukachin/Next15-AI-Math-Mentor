import json
from config import model

def parse_problem(question):

    prompt = f"""
You are a math parser.

Your job is to convert a math question into structured JSON.

Rules:
- Identify the topic correctly.
- Extract variables if present.
- Only mark needs_clarification=true if the question is incomplete.

Topics allowed:
algebra
calculus
probability
linear algebra

Question:
{question}

Return ONLY valid JSON.

Example:
{{
 "problem_text": "Find derivative of x^2 + 3x",
 "topic": "calculus",
 "variables": ["x"],
 "constraints": [],
 "needs_clarification": false
}}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown formatting if Gemini adds it
    text = text.replace("```json", "").replace("```", "")

    try:
        data = json.loads(text)
        return data
    except:
        return {
            "problem_text": question,
            "topic": "unknown",
            "variables": [],
            "constraints": [],
            "needs_clarification": True
        }