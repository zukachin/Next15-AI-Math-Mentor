from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def get_vectorstore():

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding
    )

    return vectordb