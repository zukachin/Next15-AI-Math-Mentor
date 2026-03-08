import os
import sys

# Fix the path error
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from rag.vectorstore import get_vectorstore

def retrieve_context(query):
    vectordb = get_vectorstore()
    
    # Check if we actually have data
    count = vectordb._collection.count()
    print(f"DEBUG: Vectorstore contains {count} documents.")

    if count == 0:
        print("WARNING: Vectorstore is empty! Check your chroma_db folder.")
        return ""

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    
    context = "\n".join([doc.page_content for doc in docs])
    return context

if __name__ == "__main__":
    # Test it
    print(retrieve_context("What is a dice problem?"))