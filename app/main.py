from fastapi import FastAPI
from fastapi import Query, HTTPException 
from fastapi.responses import StreamingResponse
from app.rag import generate_answer_with_memory
from fastapi.middleware.cors import CORSMiddleware 
from app.auth import (
    authenticate_user,
    create_token,
    verify_token
)
from app.auth import create_user
from fastapi import UploadFile, File
from app.ingestion import ingest_document
import os

app = FastAPI(title="Internal Knowledge Assistant")



origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://delicate-hamster-232b1e.netlify.app",
]

# 3. Add the middleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows your frontend
    allow_credentials=True,
    allow_methods=["*"],              # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],              # Allows all headers
)
@app.get("/")
def root():
    return {"message": "API running"}

'''@app.get("/ask")
def ask(question: str = Query(...), session_id: str = Query(...), token:str = Query(...)):
    """
    Ask a question with streaming response
    """
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401)
    session_id = user["user_id"]
    generator = generate_answer_with_memory(session_id, question)
    return StreamingResponse(generator, media_type="text/plain")'''




@app.get("/ask")
def ask(question: str = Query(...), token: str = Query(...)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401)

    session_id = user["user_id"]      #
    generator = generate_answer_with_memory(session_id, question)
    return StreamingResponse(generator, media_type="text/plain")




@app.post("/login")

def login(username: str, password: str):

    user = authenticate_user(username, password)

    if not user:

        raise HTTPException(status_code=401)

    user_id, role = user

    token = create_token(user_id, role)

    return {

        "token": token,
        "role": role

    }





@app.post("/upload")

def upload_doc(

    file: UploadFile = File(...),
    token: str = ""

):

    user = verify_token(token)

    if not user:

        raise HTTPException(status_code=401)

    if user["role"] != "admin":

        raise HTTPException(status_code=403)

    # Create directory if it doesn't exist
    os.makedirs("data/documents", exist_ok=True)
    
    file_path = f"data/documents/{file.filename}"
    
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    try:
        ingest_document(file_path)
    finally:
        # Always delete PDF after ingestion
        if os.path.exists(file_path):
            os.remove(file_path)
    
    return {"status": "uploaded", "message": "PDF processed and stored in Pinecone"}

@app.post("/signup")
def signup(username: str, password: str):

    try:

        user_id = create_user(
            username,
            password,
            role="user"   # default role
        )

        return {

            "message": "user created",
            "user_id": user_id

        }

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="username already exists"
        )