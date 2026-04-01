import numpy as np 
from app.onnx_embeddings import encode
from app.pinecone_utils import search_vectors
import requests
API_URL = "https://api.jina.ai/v1/rerank"
headers = {
    "Authorization": f"Bearer jina_4a70666e3cf14691a42658c24dc04bfa7j-dErPbiB0IH8DiLE1eaET9mJmf",
    "Content-Type": "application/json"
}

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
    if not results:
        return []

    payload = {
        "model": "jina-reranker-v3-base-en",  # or jina-reranker-v3-base-multilingual
        "query": query,
        "documents": [r["text"] for r in results]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()

    # Jina returns scores aligned with documents
    reranked = sorted(
        zip(results, data["scores"]),
        key=lambda x: x[1],
        reverse=True
    )

    return [r[0]["text"] for r in reranked[:top_k]]