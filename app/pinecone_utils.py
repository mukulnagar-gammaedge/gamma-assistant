import os
from pinecone import Pinecone
import json

# Initialize Pinecone
def initialize_pinecone():
    """Initialize Pinecone client"""
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY environment variable not set")
    
    pc = Pinecone(api_key=api_key)
    return pc


def get_index():
    """Get or create Pinecone index"""
    pc = initialize_pinecone()
    index_name = os.getenv("PINECONE_INDEX_NAME", "ai-assistant")
    index = pc.Index(index_name)
    return index


def upsert_vectors(embeddings, chunks, batch_size=100):
    """
    Upsert vectors to Pinecone
    
    Args:
        embeddings: Numpy array of shape (n, 384)
        chunks: List of text chunks
        batch_size: Batch size for upsert
    """
    index = get_index()
    
    vectors_to_upsert = []
    for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
        # Convert embedding to list
        vector = embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
        
        # Create metadata with text chunk
        metadata = {
            "text": chunk,
            "chunk_index": i
        }
        
        # Create vector tuple format for Pinecone: (id, vector, metadata)
        vectors_to_upsert.append({
            "id": f"chunk_{i}",
            "values": vector,
            "metadata": metadata
        })
    
    # Upsert in batches
    for i in range(0, len(vectors_to_upsert), batch_size):
        batch = vectors_to_upsert[i:i + batch_size]
        index.upsert(vectors=batch)
    
    print(f"Upserted {len(vectors_to_upsert)} vectors to Pinecone")


def search_vectors(query_embedding, top_k=5, threshold=0.2):
    """
    Search for similar vectors in Pinecone
    
    Args:
        query_embedding: Query vector (384-dimensional)
        top_k: Number of top results to return
        threshold: Similarity threshold (0-1 scale)
    
    Returns:
        List of (text_chunk, similarity_score) tuples
    """
    index = get_index()
    
    # Convert to list if numpy array
    query_vector = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else list(query_embedding)
    
    # Search in Pinecone (returns similarity scores by default for cosine)
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    
    # Extract and filter results
    retrieved_chunks = []
    for match in results['matches']:
        score = match['score']  # Pinecone returns cosine similarity (0-1)
        
        if score >= threshold:
            text = match['metadata'].get('text', '')
            retrieved_chunks.append((text, score))
    
    return retrieved_chunks


def clear_index():
    """Clear all vectors from Pinecone index"""
    index = get_index()
    # Get index stats to know how many vectors to delete
    stats = index.describe_index_stats()
    total_vectors = stats['total_vector_count']
    
    if total_vectors > 0:
        # Delete all vectors using namespace (default namespace is "")
        index.delete(delete_all=True)
        print(f"Cleared {total_vectors} vectors from Pinecone index")


def get_index_stats():
    """Get statistics about the Pinecone index"""
    index = get_index()
    stats = index.describe_index_stats()
    return stats
