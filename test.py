# run once

'''from app.auth import init_db, create_user

init_db()

create_user("admin", "admin123", role="admin")

create_user("employee", "user123", role="user")

print("users created")'''


import requests
import os

API_URL = "https://api.jina.ai/v1/rerank"
headers = {
    "Authorization": f"Bearer jina_4a70666e3cf14691a42658c24dc04bfa7j-dErPbiB0IH8DiLE1eaET9mJmf",  # set locally in your shell
    "Content-Type": "application/json"
}

def test_rerank():
    query = "What is FastAPI?"
    documents = [
        "FastAPI is a modern web framework for Python.",
        "Django is a full-stack Python web framework.",
        "Flask is a lightweight Python web framework."
    ]

    payload = {
        "model": "jina-reranker-v3",
        "query": query,
        "documents": documents
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    print("Status:", response.status_code)
    print("Raw JSON:", response.json())

if __name__ == "__main__":
    test_rerank()
