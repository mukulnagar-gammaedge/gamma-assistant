# 📚 Internal Knowledge Assistant

A modern AI-powered RAG (Retrieval-Augmented Generation) application with authentication, document management, and real-time chat capabilities. Built with FastAPI backend and React frontend.

---

## 🎯 Project Overview

The **Internal Knowledge Assistant** is a sophisticated document-based Q&A system that allows users to:

- 🔐 **Authenticate** with secure token-based login/signup
- 📤 **Upload** documents (PDFs, TXT, DOCX)
- 🔍 **Search** through a vector database for relevant information
- 💬 **Chat** with an AI assistant that answers questions based on uploaded documents
- 👥 **Manage Users** with role-based access control (admin/user)
- ⚡ **Stream Responses** in real-time with WebSocket-like streaming

---

## 🏗️ Architecture

### Tech Stack

**Backend:**
- **FastAPI** - Modern Python web framework
- **SQLiteCloud** - Remote SQLite database for user management
- **FAISS** - Facebook's vector similarity search
- **Sentence Transformers** - Text embedding generation
- **OpenAI API** - LLM for answer generation
- **LangChain** - RAG orchestration

**Frontend:**
- **React 18** - UI component library
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** (implicitly used in styling)

**Infrastructure:**
- **Docker** - Containerization (backend only)
- **Pytest** - Testing framework
- **GitHub Actions** - CI/CD pipeline

### Project Structure

```
ai-assistant/
├── app/                           # FastAPI Backend
│   ├── main.py                   # Main application & endpoints
│   ├── auth.py                   # Authentication logic
│   ├── rag.py                    # RAG pipeline implementation
│   ├── retrieval.py              # Document retrieval system
│   ├── ingestion.py              # Document ingestion pipeline
│   ├── memory.py                 # Session memory management
│   ├── guardrails.py             # Safety guardrails
│   ├── evaluator.py              # Response evaluation
│   └── __pycache__/
│
├── frontend/                      # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth.jsx          # Login/Signup component
│   │   │   ├── Chat.jsx          # Chat interface
│   │   │   └── Message.jsx       # Message display
│   │   ├── image/
│   │   │   └── logo.jpeg         # App logo
│   │   ├── App.jsx               # Main app component
│   │   ├── App.css               # Global styles
│   │   └── main.jsx              # Entry point
│   ├── public/
│   ├── .env.development          # Dev environment variables
│   ├── .env.docker               # Docker environment variables
│   ├── Dockerfile                # Frontend container setup
│   ├── package.json              # Dependencies
│   ├── vite.config.js            # Vite configuration
│   └── index.html
│
├── tests/                         # Test Suite
│   ├── conftest.py               # Pytest configuration & fixtures
│   ├── test_main.py              # Main API tests
│   ├── test_auth.py              # Authentication tests
│   ├── __init__.py
│   └── README.md                 # Testing documentation
│
├── data/                          # Data Directory
│   ├── documents/                # Uploaded documents
│   └── vector_store/             # FAISS vector database
│       ├── index.faiss           # Vector index
│       └── chunks.npy            # Document embeddings
│
├── docker-compose.yml            # Docker Compose configuration (backend only)
├── Dockerfile.backend            # Backend container setup
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
├── SETUP.md                      # Setup instructions
├── BACKEND_DOCKER_SETUP.md       # Docker-specific setup
├── DOCKER_SETUP.md               # Original Docker documentation
├── README.md                     # This file
└── .env.example                  # Environment variables template
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 18+** (for frontend)
- **Docker & Docker Compose** (optional, for backend containerization)

### Option 1: Docker Backend + Local Frontend (Recommended)

```bash
# 1. Start Backend with Docker
docker-compose up -d

# 2. In a new terminal, start Frontend
cd frontend
npm install
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Run Everything Locally

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📋 Features

### Authentication System
- **Signup**: Create new user accounts with role assignment
- **Login**: Secure authentication with JWT-like tokens
- **Role-Based Access**: Admin and User roles with different permissions
- **Token Management**: Stateless token-based authorization

### Document Management
- **Upload**: Support for PDF, TXT, and DOCX formats
- **Ingestion**: Automatic document chunking and embedding
- **Vector Storage**: FAISS-based similarity search
- **Admin Only**: Only administrators can upload documents

### RAG Pipeline
- **Retrieval**: FAISS-based vector similarity search
- **Augmentation**: Context-aware prompt construction
- **Generation**: OpenAI API for intelligent responses
- **Streaming**: Real-time response streaming to frontend

### Chat Interface
- **Real-time Messaging**: Message history with streaming responses
- **User/AI Separation**: Clear distinction between user and AI messages
- **Session Memory**: Conversation context management
- **Typing Indicators**: Visual feedback during AI processing

### User Interface
- **Modern Design**: Orange, white, and black color scheme
- **Responsive**: Works on desktop, tablet, and mobile
- **Logo Integration**: Custom branded application
- **Smooth Animations**: Professional UX with transitions

---

## 🔐 API Endpoints

### Authentication

```http
POST /login?username=<username>&password=<password>
Response: { token: string, role: "admin" | "user" }

POST /signup?username=<username>&password=<password>
Response: { user_id: string, message: string }
```

### Chat

```http
GET /ask?question=<question>&token=<token>
Response: Streaming text response from AI

Requires: Valid authentication token
```

### Document Management

```http
POST /upload
Body: FormData with file and token
Headers: Authorization with token
Response: { status: "uploaded" }

Admin only endpoint
```

### Health Check

```http
GET /
Response: { message: "API running" }
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::TestAuthentication::test_login_valid_credentials

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app tests/
```

### Test Coverage

- **Authentication**: Login, signup, token generation
- **Authorization**: Role-based access control
- **API Endpoints**: Health checks, document uploads
- **Error Handling**: Invalid credentials, duplicate users

### Test Structure

```
tests/
├── conftest.py           # Shared fixtures & configuration
├── test_main.py          # Main API endpoint tests
├── test_auth.py          # Authentication & authorization tests
└── README.md             # Testing documentation
```

---

## 🐳 Docker Setup

### Backend Only (Default)

```bash
# Build backend image
docker-compose build

# Start backend
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop backend
docker-compose down
```

The frontend runs locally with hot reload enabled.

### Environment Variables

**Backend (.env):**
```env
PYTHONUNBUFFERED=1
API_HOST=0.0.0.0
API_PORT=8000
```

**Frontend (.env.development):**
```env
VITE_API_URL=http://localhost:8000
```

**Frontend (.env.docker):**
```env
VITE_API_URL=http://backend:8000
```

---

## 📊 Database

### User Database (SQLiteCloud)

- **Provider**: SQLiteCloud (remote SQLite)
- **Connection**: HTTPS-based API
- **Tables**: 
  - `users` - User accounts with hashed passwords

### Vector Store (FAISS)

- **Location**: `data/vector_store/`
- **Format**: 
  - `index.faiss` - Vector index
  - `chunks.npy` - Embeddings array
- **Model**: `all-MiniLM-L6-v2` (SBERT)

### Document Store

- **Location**: `data/documents/`
- **Formats**: PDF, TXT, DOCX
- **Processing**: Automatic chunking & embedding

---

## 🛠️ Development

### Local Setup

1. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
cd frontend && npm install
```

3. **Configure Environment**
```bash
cp .env.example .env
# Update with your OpenAI API key and other settings
```

4. **Run Locally**
```bash
# Backend
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm run dev
```

### Hot Reload

- **Backend**: Auto-reloads with uvicorn (--reload flag)
- **Frontend**: Auto-reloads with Vite dev server

### Code Quality

```bash
# Run tests
pytest -v

# Check coverage
pytest --cov=app tests/

# Lint Python code (if configured)
flake8 app/
```

---

## 📦 Dependencies

### Key Backend Packages

| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.135.2 | Web framework |
| Uvicorn | 0.42.0 | ASGI server |
| Pydantic | 2.12.5 | Data validation |
| OpenAI | 2.30.0 | LLM integration |
| sentence-transformers | 5.3.0 | Text embeddings |
| faiss-cpu | 1.13.2 | Vector search |
| sqlitecloud | 0.0.84 | Remote database |
| PyPDF | 6.9.2 | PDF processing |
| pytest | 9.0.2 | Testing framework |

### Key Frontend Packages

| Package | Version | Purpose |
|---------|---------|---------|
| React | 18.2.0 | UI framework |
| Vite | 4.3.9 | Build tool |

---

## 🔄 Workflow

### User Authentication Flow

```
1. User Signs Up
   ↓
2. Creates account (username/password hashed)
   ↓
3. User Logs In
   ↓
4. Credentials validated
   ↓
5. JWT token generated
   ↓
6. Token stored in browser localStorage
   ↓
7. Token sent with each API request
```

### Document Upload & Processing Flow

```
1. Admin uploads document
   ↓
2. File stored in data/documents/
   ↓
3. Document ingested (PDFLoader, TextLoader, etc.)
   ↓
4. Split into chunks
   ↓
5. Embeddings generated (SBERT)
   ↓
6. Vectors stored in FAISS index
   ↓
7. Ready for retrieval
```

### Chat & RAG Flow

```
1. User asks question
   ↓
2. Question embedded
   ↓
3. FAISS similarity search
   ↓
4. Top-k similar documents retrieved
   ↓
5. Prompt constructed with context
   ↓
6. OpenAI API called
   ↓
7. Response streamed to frontend
   ↓
8. Displayed in real-time
```

---

## 🚨 Error Handling

### Common Issues & Solutions

**CORS Error**
```
Error: Failed to load resource: net::ERR_CONNECTION_RESET
Solution: Ensure backend is running on http://localhost:8000
```

**Port Already in Use**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Database Locked**
```
Error: UNIQUE constraint failed: users.username
Solution: Tests use unique usernames with UUID suffix
```

**Module Not Found**
```
Error: ModuleNotFoundError: No module named 'app'
Solution: Run from project root directory with venv activated
```

---

## 📈 Performance

### Optimization Tips

1. **Frontend**
   - Vite production build: ~200KB gzipped
   - React lazy loading for code splitting

2. **Backend**
   - FAISS uses CPU-optimized search
   - Document chunking reduces embedding overhead
   - Token caching avoids re-authentication

3. **Database**
   - SQLiteCloud provides automatic scaling
   - FAISS index cached in memory for fast retrieval

---

## 🔒 Security

### Security Features

- ✅ Password hashing (SHA-256)
- ✅ Token-based authentication
- ✅ CORS protection
- ✅ Role-based access control
- ✅ SQL injection protection (parameterized queries)
- ✅ Admin-only endpoints for sensitive operations

### Best Practices

- Store sensitive credentials in environment variables
- Use HTTPS in production
- Rotate authentication tokens regularly
- Implement rate limiting for API endpoints
- Sanitize user inputs

---

## 📝 Environment Variables

Create a `.env` file:

```env
# Backend
PYTHONUNBUFFERED=1
API_HOST=0.0.0.0
API_PORT=8000

# OpenAI (add your key)
OPENAI_API_KEY=sk-...

# Database
DB_PATH=sqlitecloud://...

# Frontend
VITE_API_URL=http://localhost:8000
```

---

## 🤝 Contributing

### Development Workflow

1. Create feature branch
2. Make changes in isolated branch
3. Write tests for new features
4. Run `pytest` to validate
5. Submit pull request

### Code Style

- Follow PEP 8 for Python
- Use descriptive variable/function names
- Add docstrings to functions
- Keep functions small and focused

---

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Complete setup instructions
- **[BACKEND_DOCKER_SETUP.md](BACKEND_DOCKER_SETUP.md)** - Backend Docker guide
- **[tests/README.md](tests/README.md)** - Testing documentation
- **API Docs**: http://localhost:8000/docs (Swagger UI)

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `PYTHONUNBUFFERED=1`
- [ ] Use production ASGI server (Gunicorn)
- [ ] Enable HTTPS
- [ ] Set up environment variables
- [ ] Configure CORS for production domain
- [ ] Enable database backups
- [ ] Set up monitoring & logging
- [ ] Use reverse proxy (Nginx)
- [ ] Implement rate limiting
- [ ] Set up CI/CD pipeline

### Deployment Options

- **Cloud Platforms**: AWS, Google Cloud, Azure
- **Container Orchestration**: Kubernetes, Docker Swarm
- **Serverless**: AWS Lambda, Google Cloud Functions
- **VPS**: DigitalOcean, Linode, Vultr

---

## 📞 Support

### Getting Help

1. Check [tests/README.md](tests/README.md) for testing issues
2. Review API documentation at `/docs`
3. Check application logs for errors
4. Review setup guides for installation issues

### Troubleshooting

Run tests to verify setup:
```bash
pytest -v
```

Check backend logs:
```bash
docker-compose logs backend
```

Check frontend console (browser DevTools)

---

## 📄 License

This project is provided as-is for internal use.

---

## 🎉 Features Summary

| Feature | Status | Notes |
|---------|--------|-------|
| User Authentication | ✅ Complete | Token-based with role support |
| Document Upload | ✅ Complete | Admin-only, multiple formats |
| RAG Pipeline | ✅ Complete | FAISS + OpenAI integration |
| Real-time Chat | ✅ Complete | Streaming responses |
| Testing Suite | ✅ Complete | 8+ tests covering auth & API |
| Docker Support | ✅ Complete | Backend containerization |
| React Frontend | ✅ Complete | Modern UI with Vite |
| API Documentation | ✅ Complete | Swagger UI at /docs |
| Dark Theme | ✅ Complete | Orange, white, black scheme |

---

## 📅 Project Timeline

- **Phase 1**: Backend setup with FastAPI & authentication ✅
- **Phase 2**: Frontend development with React ✅
- **Phase 3**: RAG pipeline implementation ✅
- **Phase 4**: Docker containerization ✅
- **Phase 5**: Test suite development ✅
- **Phase 6**: Documentation & deployment guides ✅

---

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Audio input/output
- [ ] Advanced analytics dashboard
- [ ] Document version control
- [ ] Collaborative editing
- [ ] Export capabilities (PDF, DOCX)
- [ ] Advanced search filters
- [ ] User activity logging
- [ ] Rate limiting & quotas
- [ ] API key management

---

**Last Updated**: March 30, 2026  
**Version**: 1.0.0

For more information, visit the documentation files or check the API swagger at `/docs`.
