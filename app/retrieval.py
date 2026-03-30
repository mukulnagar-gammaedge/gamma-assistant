import numpy as np 
import faiss 
from sentence_transformers import SentenceTransformer

from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_vector_store():

    index = faiss.read_index("data/vector_store/index.faiss")

    chunks = np.load(
        "data/vector_store/chunks.npy",
        allow_pickle=True
    )
    return index, chunks

def embed_query(query):
    embedding = model.encode([query])
    return np.array(embedding)

def search(query, top_k=5, threshold=0.2):

    index, chunks = load_vector_store()

    query_vector = embed_query(query)

    distances, indices = index.search(query_vector, top_k)

    results = []

    for score, idx in zip(distances[0], indices[0]):

        if idx < 0:
            continue

        similarity = 1 / (1 + score)

        # include close-enough matches; exact match is not required
        if similarity >= threshold:

            results.append({

                "text": chunks[idx],
                "score": float(similarity)

            })

    return results




def rerank(query, results, top_k=3):
    if not results: return []

    pairs = []

    for r in results:

        pairs.append((query, r["text"]))

    scores = reranker.predict(pairs)

    ranked = sorted(

        zip(results, scores),

        key=lambda x: x[1],

        reverse=True

    )

    top_results = [

        r[0]["text"] for r in ranked[:top_k]

    ]

    return top_results