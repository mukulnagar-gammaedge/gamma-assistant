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


def upsert_vectors(embeddings, chunks, batch_size=100, doc_id=None):
    """
    Upsert vectors to Pinecone
    
    Args:
        embeddings: Numpy array of shape (n, 384)
        chunks: List of text chunks
        batch_size: Batch size for upsert
        doc_id: Unique document identifier (prevents ID collisions across documents)
    """
    index = get_index()
    
    # Use doc_id to create unique chunk identifiers across multiple documents
    # This ensures documents don't overwrite each other
    if doc_id is None:
        doc_id = "doc"
    
    vectors_to_upsert = []
    for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
        # Convert embedding to list
        vector = embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
        
        # Create metadata with text chunk and document info
        metadata = {
            "text": chunk,
            "chunk_index": i,
            "document_id": doc_id
        }
        
        # Create unique chunk ID using document ID + chunk index
        # This prevents collisions when multiple documents are uploaded
        chunk_id = f"{doc_id}_chunk_{i}"
        
        # Create vector tuple format for Pinecone: (id, vector, metadata)
        vectors_to_upsert.append({
            "id": chunk_id,
            "values": vector,
            "metadata": metadata
        })
    
    # Upsert in batches
    for i in range(0, len(vectors_to_upsert), batch_size):
        batch = vectors_to_upsert[i:i + batch_size]
        index.upsert(vectors=batch)
    
    print(f"Upserted {len(vectors_to_upsert)} vectors to Pinecone (doc_id: {doc_id})")


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
    """
    ⚠️ WARNING: Clear ALL vectors from Pinecone index
    This removes all documents and cannot be undone!
    Use clear_document() to remove specific documents instead.
    """
    index = get_index()
    stats = index.describe_index_stats()
    total_vectors = stats['total_vector_count']
    
    if total_vectors > 0:
        index.delete(delete_all=True)
        print(f"⚠️  Cleared {total_vectors} vectors from Pinecone index")


def clear_document(doc_id):
    """
    Clear vectors for a specific document by doc_id
    Other documents remain untouched
    
    Args:
        doc_id: Document ID to clear (e.g., 'document_20250331_123456_abc12345')
    """
    index = get_index()
    
    # Delete all chunks matching this document ID
    try:
        # Pinecone requires delete by ID pattern match
        # We need to query and delete individually
        results = index.query(
            vector=[0] * 384,  # Dummy query to get stats
            top_k=10000,
            include_metadata=True
        )
        
        chunk_ids_to_delete = []
        for match in results.get('matches', []):
            metadata = match.get('metadata', {})
            if metadata.get('document_id') == doc_id:
                chunk_ids_to_delete.append(match['id'])
        
        if chunk_ids_to_delete:
            index.delete(ids=chunk_ids_to_delete)
            print(f"Deleted {len(chunk_ids_to_delete)} chunks for document: {doc_id}")
        else:
            print(f"No chunks found for document: {doc_id}")
            
    except Exception as e:
        print(f"Error clearing document {doc_id}: {e}")


def get_documents():
    """
    List all unique documents stored in Pinecone
    
    Returns:
        List of document IDs with chunk counts
    """
    index = get_index()
    
    try:
        results = index.query(
            vector=[0] * 384,  # Dummy query
            top_k=10000,
            include_metadata=True
        )
        
        documents = {}
        for match in results.get('matches', []):
            metadata = match.get('metadata', {})
            doc_id = metadata.get('document_id', 'unknown')
            documents[doc_id] = documents.get(doc_id, 0) + 1
        
        return documents
        
    except Exception as e:
        print(f"Error getting documents: {e}")
        return {}


def get_index_stats():
    """Get statistics about the Pinecone index"""
    index = get_index()
    stats = index.describe_index_stats()
    return stats
