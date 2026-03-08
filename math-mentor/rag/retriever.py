from rag.vectorstore import get_vectorstore

def retrieve_context(query):

    vectordb = get_vectorstore()

    retriever = vectordb.as_retriever(search_kwargs={"k":3})

    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs])

    return context