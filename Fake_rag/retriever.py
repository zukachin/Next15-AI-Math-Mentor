# import faiss
# import numpy as np
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# index = faiss.read_index(r'C:\Users\swethath\Desktop\Next15\Backend\math-mentor\rag\math_index.faiss')

# documents = np.load(r'C:\Users\swethath\Desktop\Next15\Backend\math-mentor\rag\documents.npy', allow_pickle=True)

# def retrieve_context(query, k=2):

#     emb = genai.embed_content(
#         model="models/embedding-001",
#         content=query
#     )

#     query_vector = np.array([emb["embedding"]]).astype("float32")

#     distances, indices = index.search(query_vector, k)

#     results = []

#     for i in indices[0]:
#         results.append(documents[i])

#     return "\n".join(results)



import faiss
import numpy as np
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

index = faiss.read_index(r"C:\Users\swethath\Desktop\Next15\Backend\math-mentor\rag\math_index.faiss")

documents = np.load(r"C:\Users\swethath\Desktop\Next15\Backend\math-mentor\rag\documents.npy", allow_pickle=True)


def retrieve_context(query, k=3):

    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=query
    )

    query_vector = np.array([response.embeddings[0].values]).astype("float32")

    distances, indices = index.search(query_vector, k)

    results = [documents[i] for i in indices[0]]

    return "\n".join(results)