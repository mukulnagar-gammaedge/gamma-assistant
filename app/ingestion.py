import os
from pypdf import PdfReader 
from app.onnx_embeddings import encode
from app.pinecone_utils import upsert_vectors
import uuid
from datetime import datetime

def read_pdf(file_path):
    reader = PdfReader(file_path)

    text=""

    for page in reader.pages:
        text += page.extract_text()+"\n"

    print(f"DEBUG: Extracted {len(text.strip())} characters from {file_path}")

    return text
    

def chunk_text(text, chunk_size=50, overlap=25):
    """
    Create overlapping chunks of text using sliding window approach
    
    Args:
        text: Input text to chunk
        chunk_size: Number of words per chunk (default: 50)
        overlap: Number of overlapping words between chunks (default: 25, i.e., 50% overlap)
    
    Returns:
        List of text chunks with context overlap
    
    Example:
        - Chunk 1: words 0-49
        - Chunk 2: words 25-74 (25 words overlap with Chunk 1)
        - Chunk 3: words 50-99 (25 words overlap with Chunk 2)
    """
    words = text.split()
    chunks = []
    step = chunk_size - overlap  # Step size determines overlap
    
    for i in range(0, len(words), step):
        # Get chunk from current position to chunk_size ahead
        chunk = " ".join(words[i:i+chunk_size])
        
        # Only add if chunk has meaningful content
        if chunk.strip():
            chunks.append(chunk)
        
        # If we've reached near the end, break to avoid tiny last chunks
        if i + chunk_size >= len(words):
            break
    
    print(f"Created {len(chunks)} overlapping chunks (size={chunk_size}, overlap={overlap})")
    return chunks

def create_embeddings(chunks):
    embeddings = encode(chunks)
    return embeddings


def store_vectors(chunks, embeddings, document_name="document"):
    """
    Store vectors in Pinecone WITHOUT clearing existing data
    
    Args:
        chunks: Text chunks to store
        embeddings: Embeddings for chunks
        document_name: Name of the source document (for metadata)
    """
    # Generate unique document ID using timestamp and UUID
    doc_id = f"{document_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
    
    # Include document name in metadata for tracking
    upsert_vectors(embeddings, chunks, doc_id=doc_id)
    print(f"Stored {len(chunks)} chunks from '{document_name}' in Pinecone (doc_id: {doc_id})")


def ingest_document(file_path):
    """
    Ingest PDF document and store in Pinecone
    
    Args:
        file_path: Path to PDF file
    """
    # Extract document name from file path
    document_name = os.path.splitext(os.path.basename(file_path))[0]
    
    text = read_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    store_vectors(chunks, embeddings, document_name=document_name)
    print(f"Ingestion complete for '{document_name}'")
