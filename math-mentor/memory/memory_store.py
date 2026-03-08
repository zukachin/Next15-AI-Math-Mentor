import os
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Dynamic Path Resolution ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_BASE = os.path.join(BASE_DIR, "math-mentor-data")
MEMORY_DIR = os.path.join(MEMORY_BASE, "memory", "chroma_memory")
MEMORY_LOG_PATH = os.path.join(MEMORY_BASE, "memory", "memory_log.jsonl")

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def _get_memory_store() -> Chroma:
    """Initializes the Vector DB with the specified embedding model."""
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    return Chroma(
        persist_directory=MEMORY_DIR,
        embedding_function=embedding,
        collection_name="math_mentor_memory",
    )

def save_interaction(record: Dict[str, Any]) -> str:
    """Saves a solved interaction into vector memory + append-only JSONL log."""
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(MEMORY_LOG_PATH), exist_ok=True)
    os.makedirs(MEMORY_DIR, exist_ok=True)

    record_id = record.get("id") or str(uuid.uuid4())
    # Note: Use timezone-aware UTC for modern standards
    timestamp = datetime.utcnow().isoformat() + "Z"

    parsed = record.get("parsed_problem") or {}
    problem_text = parsed.get("problem_text") or record.get("raw_input") or ""

    # Content to be indexed for semantic search
    text_for_embedding = f"Problem: {problem_text}\nSolution: {record.get('solution', '')}\nExplanation: {record.get('explanation', '')}"

    metadata = {
        "id": record_id,
        "timestamp": timestamp,
        "topic": str(parsed.get("topic", "unknown")), # Cast to string for Chroma
        "input_mode": str(record.get("input_mode", "text")),
        "feedback": str(record.get("user_feedback", "unknown")),
        "verifier_confidence": float((record.get("verifier") or {}).get("confidence", 0.0)),
    }

    # Save to Vector DB
    vectordb = _get_memory_store()
    vectordb.add_texts([text_for_embedding], metadatas=[metadata], ids=[record_id])
    # vectordb.persist() is no longer needed in newer versions

    # Save to Audit Log (JSONL)
    log_entry = {"id": record_id, "timestamp": timestamp, **record}
    with open(MEMORY_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return record_id

def get_memory_context(problem_text: str, k: int = 3) -> str:
    """Retrieve similar past interactions to provide context for the current problem."""
    # If the database directory doesn't exist yet, there is no context to provide
    if not os.path.exists(MEMORY_DIR) or not os.listdir(MEMORY_DIR):
        return ""

    try:
        vectordb = _get_memory_store()
        docs = vectordb.similarity_search(problem_text, k=k)
        
        if not docs:
            return ""

        snippets = []
        for doc in docs:
            topic = doc.metadata.get("topic", "unknown")
            snippets.append(f"[Past example | topic={topic}]\n{doc.page_content}")

        return "\n\n".join(snippets)
    except Exception as e:
        print(f"Memory retrieval error: {e}")
        return ""