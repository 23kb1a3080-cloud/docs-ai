# ✅ DocMind AI - Complete Setup & Running Guide

## 🎉 Current Status: FULLY RUNNING

### ✅ Backend Server
- **Status**: Running
- **URL**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

### ✅ Frontend Server
- **Status**: Running  
- **URL**: http://localhost:3000
- **Framework**: Next.js 14

---

## 🚀 Quick Start (3 Steps)

### Step 1: Add Your OpenAI API Key

**CRITICAL**: The app won't work without this!

Edit `backend/.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### Step 2: Open the Application

Open your browser and go to:
```
http://localhost:3000
```

### Step 3: Analyze a Repository

1. Enter a GitHub repository URL (e.g., `https://github.com/fastapi/fastapi`)
2. Click "Analyze"
3. Wait for analysis to complete (30 seconds - 2 minutes depending on repo size)
4. View generated documentation!

---

## 📋 What's Installed & Working

### ✅ Core Features (Working Now)
- ✅ GitHub repository integration
- ✅ Repository structure analysis
- ✅ File content fetching
- ✅ AI-powered documentation generation
- ✅ Pull request analysis
- ✅ Basic chat interface
- ✅ SQLite database (no external DB needed)
- ✅ REST API with FastAPI
- ✅ Modern React/Next.js frontend

### ⚠️ Advanced Features (Disabled - Minimal Setup)
- ⚠️ RAG-powered chat (requires ChromaDB, sentence-transformers)
- ⚠️ Semantic code search with embeddings
- ⚠️ Advanced code analysis (requires tree-sitter)

---

## 🔧 Configuration Files

### Backend Configuration (`backend/.env`)

```env
# Database - Using SQLite (no setup needed)
DATABASE_URL=sqlite:///./docmind.db

# AI API Keys (REQUIRED!)
OPENAI_API_KEY=your-openai-key-here
AI_PROVIDER=openai

# GitHub (Optional - for private repos)
GITHUB_TOKEN=

# Application
APP_NAME=DocMind AI
APP_VERSION=1.0.0
DEBUG=True
LOG_LEVEL=INFO

# CORS (JSON array format)
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
CORS_ALLOW_CREDENTIALS=True

# Security
SECRET_KEY=dev-secret-key-change-in-production

# Documentation Generation
MAX_FILE_SIZE_MB=10
MAX_REPOSITORY_SIZE_MB=500

# LLM Settings
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4000

# Feature Flags
ENABLE_PR_ANALYSIS=True
ENABLE_WEBHOOKS=False
ENABLE_ARCHITECTURE_DIAGRAMS=True
```

### Frontend Configuration (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🧪 Testing the Application

### Test 1: Health Check

Open in browser or run:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "DocMind AI",
  "version": "1.0.0"
}
```

### Test 2: API Documentation

Open in browser:
```
http://localhost:8000/api/docs
```

You should see interactive Swagger UI with all API endpoints.

### Test 3: Analyze a Small Repository

1. Go to http://localhost:3000
2. Enter: `https://github.com/tiangolo/fastapi`
3. Click "Analyze"
4. Wait for completion
5. View generated documentation

### Test 4: Generate Documentation

After analyzing a repository:
1. Go to the dashboard
2. Click "Generate Documentation"
3. Select documentation types (README, API, Architecture)
4. View generated docs

---

## 📊 API Endpoints

### Repositories
- `POST /api/v1/repositories/analyze` - Analyze a GitHub repository
- `GET /api/v1/repositories` - List all repositories
- `GET /api/v1/repositories/{id}` - Get repository details
- `GET /api/v1/repositories/{id}/structure` - Get file structure
- `GET /api/v1/repositories/{id}/files?path=...` - Get file content
- `DELETE /api/v1/repositories/{id}` - Delete repository

### Documentation
- `POST /api/v1/documentation/generate` - Generate documentation
- `GET /api/v1/documentation/{repo_id}?type=...` - Get documentation
- `GET /api/v1/documentation/{repo_id}/list` - List all docs

### Pull Requests
- `POST /api/v1/prs/analyze` - Analyze a pull request
- `GET /api/v1/prs/{repo_id}` - List pull requests

### Chat
- `POST /api/v1/chat/sessions` - Create chat session
- `POST /api/v1/chat/sessions/{id}/messages` - Send message
- `GET /api/v1/chat/sessions/{id}/messages` - Get chat history

### Analysis
- `POST /api/v1/analysis/missing-docs` - Detect missing documentation
- `POST /api/v1/analysis/architecture` - Generate architecture diagram

---

## 🛠️ Troubleshooting

### Problem: "Failed to analyze repository"

**Solutions:**
1. Check if OpenAI API key is set in `backend/.env`
2. Verify the GitHub URL is correct and public
3. Check backend logs for detailed errors
4. Try a smaller repository first

### Problem: Backend not responding

**Solutions:**
1. Check if backend is running: `curl http://localhost:8000/health`
2. Look at backend terminal for errors
3. Restart backend: Stop terminal and run:
   ```bash
   cd backend
   .\venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

### Problem: Frontend not loading

**Solutions:**
1. Check if frontend is running on port 3000
2. Clear browser cache
3. Restart frontend:
   ```bash
   cd frontend
   npm run dev
   ```

### Problem: CORS errors

**Solutions:**
1. Verify `CORS_ORIGINS` in `backend/.env` includes `http://localhost:3000`
2. Restart backend server
3. Clear browser cache

### Problem: "OpenAI API error"

**Solutions:**
1. Verify API key is correct in `backend/.env`
2. Check API key has credits: https://platform.openai.com/usage
3. Try using `gpt-3.5-turbo` instead of `gpt-4` (cheaper)

---

## 📦 Dependencies Installed

### Backend (Minimal Setup)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-dotenv==1.0.0
python-multipart==0.0.6
sqlalchemy==2.0.25
aiosqlite (for async SQLite)
PyGithub==2.1.1
openai==1.10.0
pydantic==2.5.3
pydantic-settings==2.1.0
httpx==0.26.0
markdown==3.5.2
```

### Frontend
```
next@14.1.0
react@18.2.0
typescript@5.3.3
tailwindcss@3.4.1
axios@1.6.5
zustand@4.5.0
lucide-react@0.316.0
```

---

## 🔄 Stopping the Servers

### Stop Backend
1. Find the terminal running the backend
2. Press `Ctrl+C`

### Stop Frontend
1. Find the terminal running the frontend
2. Press `Ctrl+C`

---

## 🚀 Restarting the Servers

### Start Backend
```bash
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd frontend
npm run dev
```

---

## 📈 Performance Tips

1. **Start with small repositories** (< 50 files) for faster analysis
2. **Use public repositories** to avoid GitHub authentication
3. **Monitor OpenAI API usage** to control costs
4. **Use gpt-3.5-turbo** for faster and cheaper responses
5. **Limit file size** in configuration to avoid timeouts

---

## 🎯 Example Repositories to Try

### Small & Fast (< 1 minute)
- `https://github.com/tiangolo/fastapi`
- `https://github.com/pallets/flask`
- `https://github.com/encode/httpx`

### Medium (1-3 minutes)
- `https://github.com/vercel/next.js`
- `https://github.com/facebook/react`
- `https://github.com/django/django`

### Large (3-5 minutes)
- `https://github.com/microsoft/vscode`
- `https://github.com/tensorflow/tensorflow`

---

## 🔐 Security Notes

1. **Never commit `.env` files** to version control
2. **Keep API keys secret** - don't share them
3. **Use environment variables** for sensitive data
4. **Change SECRET_KEY** in production
5. **Enable rate limiting** for production use

---

## 📚 Documentation Generated

The system generates:

### 1. README.md
- Project overview
- Installation instructions
- Usage guide
- Features list
- Contributing guidelines

### 2. API Documentation
- Endpoint descriptions
- Request/response formats
- Authentication details
- Error codes
- Usage examples

### 3. Architecture Documentation
- System overview
- Component breakdown
- Data flow diagrams
- Technology stack
- Design decisions
- Mermaid diagrams

### 4. Pull Request Analysis
- Change summary
- Affected modules
- Breaking changes detection
- Documentation update suggestions

---

## 🎨 UI Features

- **Dark mode** support
- **Responsive design** (mobile, tablet, desktop)
- **Real-time updates** during analysis
- **Syntax highlighting** for code
- **Markdown rendering** for documentation
- **Interactive chat** interface
- **File tree** navigation

---

## 💡 Usage Tips

1. **Analyze before generating docs** - Always analyze the repository first
2. **Use specific branches** - Specify branch name for accurate analysis
3. **Check file structure** - Review the file tree before generating docs
4. **Ask specific questions** - Be specific in chat for better answers
5. **Review generated docs** - Always review and edit generated documentation

---

## 🔮 Future Enhancements (Full Installation)

To enable advanced features, install full dependencies:

```bash
cd backend
.\venv\Scripts\pip.exe install -r requirements.txt
```

This enables:
- ✨ RAG-powered chat with repository context
- ✨ Semantic code search
- ✨ Advanced code analysis
- ✨ Embeddings and vector search
- ✨ Real-time code understanding

**Note**: Full installation takes 30-60 minutes due to large packages (PyTorch ~2GB).

---

## 📞 Support

If you encounter issues:

1. Check this guide first
2. Review backend logs for errors
3. Check browser console for frontend errors
4. Verify all configuration files
5. Ensure API keys are valid

---

## ✅ Checklist

Before using the application:

- [ ] Backend server is running (http://localhost:8000)
- [ ] Frontend server is running (http://localhost:3000)
- [ ] OpenAI API key is set in `backend/.env`
- [ ] Health check returns "healthy" status
- [ ] API docs are accessible
- [ ] Frontend loads without errors

---

**🎉 You're all set! Start analyzing repositories and generating documentation!**

**Open**: http://localhost:3000
