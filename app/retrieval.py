import numpy as np 
from sentence_transformers import CrossEncoder
from app.onnx_embeddings import encode
from app.pinecone_utils import search_vectors

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def embed_query(query):
    embedding = encode([query])
    return embedding[0]  # Return single embedding, not array


def search(query, top_k=5, threshold=0.2):
    query_vector = embed_query(query)
    
    # Search in Pinecone
    results = search_vectors(query_vector, top_k=top_k, threshold=threshold)
    
    # Convert to same format as before
    formatted_results = []
    for text, score in results:
        formatted_results.append({
            "text": text,
            "score": float(score)
        })
    
    return formatted_results




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