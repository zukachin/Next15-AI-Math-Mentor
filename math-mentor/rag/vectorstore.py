import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# This stops the telemetry error from appearing
os.environ["ANONYMOUS_TELEMETRY"] = "False"

def get_vectorstore():
    # Use the ABSOLUTE path to avoid "0 documents" errors
    # This ensures it always finds the folder regardless of where you run the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    persist_dir = os.path.join(project_root, "chroma_db")
    
    os.makedirs(persist_dir, exist_ok=True)

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # MUST match the name used in ingest.py
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding,
        collection_name="math_mentor_knowledge_base" 
    )
    
    return vectordb