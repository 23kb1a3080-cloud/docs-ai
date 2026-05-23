# Installation Issue & Solution

## Problem
The full installation is taking too long due to:
1. Large dependencies (PyTorch ~2GB, onnxruntime ~13GB, transformers ~12MB)
2. Network connectivity issues
3. Dependency resolution conflicts

## Quick Solution Options

### Option 1: Install Core Dependencies Only (Recommended for Demo)

Create a minimal `requirements-minimal.txt`:

```txt
# Core FastAPI
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-dotenv==1.0.0

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9  # Or use sqlite

# GitHub
PyGithub==2.1.1

# AI (Choose ONE)
openai==1.10.0  # Simpler, faster
# OR google-generativeai==0.3.2

# Basic utilities
pydantic==2.5.3
httpx==0.26.0
```

Install with:
```bash
cd backend
.\venv\Scripts\pip.exe install fastapi uvicorn python-dotenv sqlalchemy psycopg2-binary PyGithub openai pydantic httpx python-multipart
```

### Option 2: Use SQLite Instead of PostgreSQL

Edit `backend/.env`:
```
DATABASE_URL=sqlite:///./docmind.db
```

### Option 3: Skip RAG Features Initially

Comment out RAG-related imports in:
- `backend/app/services/rag_service.py`
- `backend/app/api/v1/chat.py`

### Option 4: Run Frontend Only

The frontend can be developed independently:

```bash
cd frontend
npm install
npm run dev
```

## What Works Without Full Installation

✅ **With Minimal Install:**
- FastAPI server
- GitHub repository fetching
- Basic documentation generation (using OpenAI only)
- Database storage
- API endpoints

❌ **Requires Full Install:**
- RAG chat system (needs ChromaDB, sentence-transformers)
- Local embeddings (needs torch, transformers)
- Code analysis (needs tree-sitter)

## Recommended Approach for Demo

1. **Install minimal dependencies** (5 minutes)
2. **Use OpenAI API** for documentation generation
3. **Use SQLite** for database
4. **Skip RAG chat** initially
5. **Focus on core features**: Repository analysis + Doc generation

## Full Installation (When You Have Time)

The full installation will take 30-60 minutes due to large packages.

Run in background:
```bash
cd backend
.\venv\Scripts\pip.exe install -r requirements.txt
```

Let it run overnight or during a break.

## Alternative: Use Docker

Create `docker-compose.yml` and let Docker handle dependencies:
```bash
docker-compose up
```

This isolates the environment and handles all dependencies automatically.

---

**For immediate demo, use Option 1 (minimal install) + SQLite!**
