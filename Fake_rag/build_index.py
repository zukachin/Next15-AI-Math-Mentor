import os
import faiss
import numpy as np
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

knowledge_path = r'C:/Users/swethath/Desktop/Next15/Backend/math-mentor/rag/knowledge_base'

documents = []

for file in os.listdir(knowledge_path):
    with open(os.path.join(knowledge_path, file), "r", encoding="utf-8") as f:
        documents.append(f.read())

embeddings = []

for doc in documents:

    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=doc
    )

    embeddings.append(response.embeddings[0].values)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    r'C:/Users/swethath/Desktop/Next15/Backend/math-mentor/rag/math_index.faiss'
)

np.save(
    r'C:/Users/swethath/Desktop/Next15/Backend/math-mentor/rag/documents.npy',
    np.array(documents)
)

print("Index built successfully")