import io
from typing import Tuple

import streamlit as st

from agents.parser_agent import parse_problem
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution
from agents.intent_router_agent import route_intent

from rag.retriever import retrieve_context
from memory.memory_store import get_memory_context, save_interaction
from config import model


st.title("AI Math Mentor")
st.caption("Multimodal math mentor with RAG, agents, HITL, and memory")


def extract_text_from_image(uploaded_file) -> Tuple[str, float]:
    """
    Use Gemini multimodal to perform OCR on the uploaded image.
    Returns (text, confidence in [0,1]).
    """
    bytes_data = uploaded_file.read()
    image = {
        "mime_type": uploaded_file.type,
        "data": bytes_data,
    }

    prompt = """
You are an OCR assistant for math problems.

Extract ONLY the math problem statement from this image.
Return STRICTLY valid JSON as:
{
  "text": "<extracted problem as plain text>",
  "confidence": <number between 0 and 1>
}
"""

    response = model.generate_content([prompt, image])
    text = response.text.strip().replace("```json", "").replace("```", "")
    try:
        import json

        data = json.loads(text)
        return data.get("text", ""), float(data.get("confidence", 0.6))
    except Exception:
        return "", 0.0


def transcribe_audio(uploaded_file) -> Tuple[str, float]:
    """
    Use Gemini multimodal to perform ASR on the uploaded audio.
    Returns (transcript, confidence in [0,1]).
    """
    bytes_data = uploaded_file.read()
    audio = {
        "mime_type": uploaded_file.type,
        "data": bytes_data,
    }

    prompt = """
You are an ASR assistant for math problems.

Transcribe the math question clearly in text form.
Handle phrases like "square root of", "raised to", "over", etc.

Return STRICTLY valid JSON as:
{
  "text": "<transcribed problem as plain text>",
  "confidence": <number between 0 and 1>
}
"""

    response = model.generate_content([prompt, audio])
    text = response.text.strip().replace("```json", "").replace("```", "")
    try:
        import json

        data = json.loads(text)
        return data.get("text", ""), float(data.get("confidence", 0.6))
    except Exception:
        return "", 0.0


st.sidebar.header("Input mode")
input_mode = st.sidebar.radio("Choose how to ask your question", ["Text", "Image", "Audio"])

raw_question = ""
input_confidence = 1.0

st.subheader("1. Provide your question")

uploaded_image = None
uploaded_audio = None

if input_mode == "Text":
    raw_question = st.text_area("Type your math question", height=120)

elif input_mode == "Image":
    uploaded_image = st.file_uploader("Upload a photo/screenshot (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        ocr_text, ocr_conf = extract_text_from_image(uploaded_image)
        input_confidence = ocr_conf
        st.markdown("**OCR extraction preview (you can edit):**")
        raw_question = st.text_area("Extracted text", value=ocr_text, height=120)
        if ocr_conf < 0.7:
            st.warning("OCR confidence is low. Please carefully review and edit the extracted text (HITL).")

elif input_mode == "Audio":
    uploaded_audio = st.file_uploader(
        "Upload or record audio (WAV/MP3/M4A/OGG)", type=["wav", "mp3", "m4a", "ogg"]
    )
    if uploaded_audio is not None:
        transcript, asr_conf = transcribe_audio(uploaded_audio)
        input_confidence = asr_conf
        st.markdown("**Transcript preview (you can edit):**")
        raw_question = st.text_area("Transcribed text", value=transcript, height=120)
        if asr_conf < 0.7:
            st.warning("ASR confidence is low. Please carefully review and edit the transcript (HITL).")


st.subheader("2. Solve the problem")

if st.button("Solve") and raw_question.strip():
    # Parser agent
    parsed = parse_problem(raw_question)
    st.markdown("**Parsed Problem**")
    st.json(parsed)

    if parsed.get("needs_clarification"):
        st.warning("Parser detected that the question may be incomplete or ambiguous (HITL).")

    # Intent router agent
    routing = route_intent(parsed)
    st.markdown("**Intent Router**")
    st.json(routing)

    problem_text = parsed.get("problem_text", raw_question)

    # Retrieve RAG context
    context = retrieve_context(problem_text)
    st.markdown("**Retrieved Knowledge (RAG context)**")
    st.write(context if context else "No relevant knowledge retrieved.")

    # Retrieve memory context
    memory_context = get_memory_context(problem_text)
    if memory_context:
        st.markdown("**Memory: similar past problems**")
        st.write(memory_context)

    # Solver agent
    combined_context = "\n\n".join(
        [
            "Knowledge base context:",
            context,
            "Memory context (similar solved problems):",
            memory_context,
        ]
    )
    solution = solve_problem(problem_text, combined_context)
    st.markdown("**Proposed Solution**")
    st.write(solution)

    # Verifier agent
    verification = verify_solution(problem_text, solution)
    st.markdown("**Verifier**")
    st.json(verification)

    verifier_conf = float(verification.get("confidence", 0.5))
    if verifier_conf < 0.7:
        st.error(
            "Verifier is not confident in this solution (HITL). "
            "Please review the steps and provide feedback below."
        )

    # Explainer agent
    explanation = explain_solution(problem_text, solution)
    st.markdown("**Student-friendly Explanation**")
    st.write(explanation)

    # Agent trace
    st.markdown("**Agent Trace**")
    trace = [
        "Parser Agent completed",
        "Intent Router Agent completed",
        "Retriever Agent completed",
        "Solver Agent completed",
        "Verifier Agent completed",
        "Explainer Agent completed",
    ]
    for t in trace:
        st.write("✅", t)

    # Feedback & memory storage (HITL + self-learning)
    st.subheader("3. Feedback (Human-in-the-loop)")
    feedback_choice = st.radio(
        "How was this answer?",
        ["Not decided yet", "✅ Correct", "❌ Incorrect"],
        index=0,
    )

    comment = ""
    if feedback_choice == "❌ Incorrect":
        comment = st.text_area("What was wrong? (optional but very helpful)", height=80)

    if st.button("Save to memory"):
        user_feedback = (
            "correct" if feedback_choice == "✅ Correct" else "incorrect" if feedback_choice == "❌ Incorrect" else "unknown"
        )

        record = {
            "input_mode": input_mode.lower(),
            "raw_input": raw_question,
            "parsed_problem": parsed,
            "intent_routing": routing,
            "rag_context": context,
            "memory_context": memory_context,
            "solution": solution,
            "explanation": explanation,
            "verifier": verification,
            "input_confidence": input_confidence,
            "user_feedback": user_feedback,
            "user_comment": comment,
        }

        _ = save_interaction(record)
        st.success("Interaction saved to memory. Future similar questions can reuse this solution pattern.")
