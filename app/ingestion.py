import os
import numpy as np 
from pypdf import PdfReader 
from sentence_transformers import SentenceTransformer
from app.pinecone_utils import upsert_vectors, clear_index


model = SentenceTransformer("all-MiniLM-L6-v2")

def read_pdf(file_path):
    reader = PdfReader(file_path)

    text=""

    for page in reader.pages:
        text += page.extract_text()+"\n"

    print(f"DEBUG: Extracted {len(text.strip())} characters from {file_path}")

    return text
    

def chunk_text(text, chunk_size=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def create_embeddings(chunks):
    embeddings = model.encode(chunks)
    return np.array(embeddings)


def store_vectors(chunks, embeddings):
    # Clear previous vectors and store new ones in Pinecone
    clear_index()
    upsert_vectors(embeddings, chunks)
    print("stored", len(chunks), "chunks in Pinecone")


def ingest_document(file_path):
    text = read_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    store_vectors(chunks, embeddings)
    print("ingestion complete")
