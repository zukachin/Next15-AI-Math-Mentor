import os
import sys


from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Ensure the parent directory (Backend/math-mentor) is on sys.path so we can import rag.vectorstore
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from rag.vectorstore import get_vectorstore


# Use the CURRENT_DIR we already defined to create an absolute path
KNOWLEDGE_BASE_DIR = os.path.join(CURRENT_DIR, "knowledge_base")
print(f"Using knowledge base directory: {KNOWLEDGE_BASE_DIR}")


def ingest_docs() -> None:
    """
    Ingest all markdown knowledge base files into the Chroma vector store.
    """
    if not os.path.isdir(KNOWLEDGE_BASE_DIR):
        raise FileNotFoundError(f"Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    all_chunks = []

    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if not filename.lower().endswith(".md"):
            continue

        path = os.path.join(KNOWLEDGE_BASE_DIR, filename)
        loader = TextLoader(path, encoding="utf-8")
        docs = loader.load()
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)

    if not all_chunks:
        raise RuntimeError("No markdown documents found to ingest in knowledge base directory.")

    vectordb = get_vectorstore()
    vectordb.add_documents(all_chunks)
    vectordb.persist()

    print(f"Ingested {len(all_chunks)} chunks from knowledge base.")


if __name__ == "__main__":
    ingest_docs()