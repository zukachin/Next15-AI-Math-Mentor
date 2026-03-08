import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


MEMORY_DIR = os.path.join("Backend", "math-mentor", "memory", "chroma_memory")
MEMORY_LOG_PATH = os.path.join("Backend", "math-mentor", "memory", "memory_log.jsonl")
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def _get_memory_store() -> Chroma:
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = Chroma(
        persist_directory=MEMORY_DIR,
        embedding_function=embedding,
        collection_name="math_mentor_memory",
    )
    return vectordb


def save_interaction(record: Dict[str, Any]) -> str:
    """
    Save a solved interaction into vector memory + append-only JSONL log.

    Expected record keys (not all mandatory, but recommended):
      - input_mode: "text" | "image" | "audio"
      - raw_input: original text or path
      - parsed_problem: dict from parser_agent
      - intent_routing: dict from intent_router_agent
      - rag_context: string with retrieved KB chunks
      - memory_context: string with reused examples
      - solution: string
      - explanation: string
      - verifier: dict with confidence/issues
      - user_feedback: "correct" | "incorrect" | "unknown"
      - user_comment: optional string
    """
    os.makedirs(os.path.dirname(MEMORY_LOG_PATH), exist_ok=True)
    os.makedirs(MEMORY_DIR, exist_ok=True)

    record_id = record.get("id") or str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    parsed = record.get("parsed_problem") or {}
    problem_text = parsed.get("problem_text") or record.get("raw_input") or ""

    text_for_embedding = "\n".join(
        [
            f"Problem: {problem_text}",
            f"Solution: {record.get('solution', '')}",
            f"Explanation: {record.get('explanation', '')}",
        ]
    )

    metadata = {
        "id": record_id,
        "timestamp": timestamp,
        "topic": parsed.get("topic", "unknown"),
        "input_mode": record.get("input_mode", "text"),
        "feedback": record.get("user_feedback", "unknown"),
        "verifier_confidence": (record.get("verifier") or {}).get("confidence"),
    }

    vectordb = _get_memory_store()
    vectordb.add_texts([text_for_embedding], metadatas=[metadata], ids=[record_id])
    vectordb.persist()

    log_entry = {
        "id": record_id,
        "timestamp": timestamp,
        **record,
    }

    with open(MEMORY_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return record_id


def get_memory_context(problem_text: str, k: int = 3) -> str:
    """
    Retrieve similar past problems/solutions as additional context for the solver.
    """
    if not os.path.isdir(MEMORY_DIR):
        return ""

    vectordb = _get_memory_store()
    try:
        docs = vectordb.similarity_search(problem_text, k=k)
    except Exception:
        return ""

    if not docs:
        return ""

    snippets: List[str] = []
    for doc in docs:
        topic = (doc.metadata or {}).get("topic", "unknown")
        snippets.append(f"[Past example | topic={topic}]\n{doc.page_content}")

    return "\n\n".join(snippets)

