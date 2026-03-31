import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pickle

# Global vectorizer (fits on all documents seen)
_vectorizer = None
_fitted = False


def get_vectorizer():
    """Get or create TF-IDF vectorizer"""
    global _vectorizer, _fitted
    
    if _vectorizer is None:
        # Create sparse TF-IDF vectorizer with sublinear_tf for better semantic similarity
        # Use 384 dimensions to match Pinecone index (or will be padded to 384)
        _vectorizer = TfidfVectorizer(
            max_features=384,  # Match Pinecone index dimension
            lowercase=True,
            stop_words='english',
            norm='l2',  # L2 normalization for cosine similarity
            sublinear_tf=True
        )
        _fitted = False
    
    return _vectorizer


def encode(texts):
    """
    Encode texts to sparse embeddings using TF-IDF
    
    Lightweight, no torch/CUDA needed!
    Produces 384-dimensional vectors (matches Pinecone index)
    
    Args:
        texts: List of strings or single string
    
    Returns:
        Numpy array of embeddings (384-dimensional)
    """
    global _vectorizer, _fitted
    
    if isinstance(texts, str):
        texts = [texts]
    
    # Filter out very short/empty texts
    texts = [t.strip() for t in texts if t.strip() and len(t.strip()) > 3]
    
    if not texts:
        # Return dummy embedding if all texts are empty
        return np.ones((1, 384), dtype=np.float32) / np.sqrt(384)
    
    vectorizer = get_vectorizer()
    
    # If this is the first batch, fit the vectorizer
    if not _fitted:
        vectorizer.fit(texts)
        _fitted = True
        embeddings = vectorizer.transform(texts).toarray()
    else:
        # Use existing vocabulary
        embeddings = vectorizer.transform(texts).toarray()
    
    # Ensure embeddings are exactly 384 dimensions (Pinecone index dimension)
    if embeddings.shape[1] < 384:
        # Pad with zeros
        padding = np.zeros((embeddings.shape[0], 384 - embeddings.shape[1]))
        embeddings = np.hstack([embeddings, padding])
    elif embeddings.shape[1] > 384:
        # Truncate
        embeddings = embeddings[:, :384]
    
    # Avoid all-zero vectors: add small constant and renormalize
    epsilon = 1e-6
    embeddings = embeddings + epsilon
    
    # Renormalize to unit vectors
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1  # Avoid division by zero
    embeddings = embeddings / norms
    
    return embeddings.astype(np.float32)




