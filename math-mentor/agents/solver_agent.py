from config import model

def solve_problem(problem, context):

    prompt = f"""
You are a math solver.

Problem:
{problem}

Relevant knowledge:
{context}

Solve step by step.
Return final answer clearly.
"""

    response = model.generate_content(prompt)

    return response.text