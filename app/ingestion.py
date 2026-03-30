import os
import numpy as np 
from pypdf import PdfReader 
from sentence_transformers import SentenceTransformer
import faiss


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
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, "data/vector_store/index.faiss")
    np.save("data/vector_store/chunks.npy", chunks)

    print("stored", len(chunks), "chunks")


def ingest_document(file_path):
    text = read_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    store_vectors(chunks, embeddings)
    print("ingestion complete")
