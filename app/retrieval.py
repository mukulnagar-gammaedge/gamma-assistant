import numpy as np 
from app.onnx_embeddings import encode
from app.pinecone_utils import search_vectors


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
    """Simple rerank - just return top results by their existing scores
    
    (Using TF-IDF embeddings, the initial ranking is already good)
    """
    if not results:
        return []
    
    # Sort by score and return top results
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    return [r["text"] for r in sorted_results[:top_k]]