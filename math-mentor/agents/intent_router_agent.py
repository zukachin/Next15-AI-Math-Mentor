import json
from typing import Dict, Any

from config import model


def route_intent(parsed_problem: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify the problem and decide how it should be handled.

    Returns a JSON dict such as:
    {
      "topic": "algebra",
      "difficulty": "jee-standard",
      "problem_type": "numerical",
      "strategy": "rag+symbolic",
      "notes": "..."
    }
    """

    prompt = f"""
You are an intent routing agent for a JEE-style math mentor system.

You will receive a parsed math problem in JSON format. Your job is to:
- confirm or refine the topic (algebra, probability, calculus, linear algebra)
- guess a rough difficulty (easy, medium, hard, jee-standard)
- classify the problem type (conceptual, numerical, proof, optimization, equation-solving)
- suggest an ideal solution strategy label:
  - "rag-only" (pure retrieval and reasoning)
  - "rag+symbolic" (retrieval plus algebraic manipulations / calculus)
  - "formula-lookup" (direct application of formula)

Input (parsed problem JSON):
{json.dumps(parsed_problem, ensure_ascii=False)}

Return ONLY valid JSON with this exact shape:
{{
  "topic": "<one of: algebra | probability | calculus | linear algebra | unknown>",
  "difficulty": "<one of: easy | medium | hard | jee-standard>",
  "problem_type": "<one of: conceptual | numerical | proof | optimization | equation-solving>",
  "strategy": "<one of: rag-only | rag+symbolic | formula-lookup>",
  "notes": "short reasoning (max 2 sentences)"
}}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "")

    try:
        data = json.loads(text)
        return data
    except Exception:
        # Fallback: keep minimal but valid routing info
        return {
            "topic": parsed_problem.get("topic", "unknown"),
            "difficulty": "jee-standard",
            "problem_type": "numerical",
            "strategy": "rag+symbolic",
            "notes": "Fallback routing because intent router JSON parsing failed.",
        }

