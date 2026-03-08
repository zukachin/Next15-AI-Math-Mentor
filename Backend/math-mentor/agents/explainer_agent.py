from config import model

def explain_solution(problem, solution):

    prompt = f"""
Explain the math solution clearly step by step for a student.

Problem:
{problem}

Solution:
{solution}


Return:
- short reasoning
- final answer clearly

Do NOT produce a long explanation.
"""

    response = model.generate_content(prompt)

    return response.text