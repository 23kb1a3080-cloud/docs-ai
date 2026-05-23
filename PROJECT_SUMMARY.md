# DocMind AI - Project Summary

## 🎯 Project Overview

**DocMind AI** is a full-stack AI-powered developer assistant that automatically generates, updates, and explains technical documentation from GitHub repositories. It transforms any codebase into a living knowledge system.

### Problem Statement
Developers rarely update documentation, resulting in:
- Outdated API documentation
- Onboarding confusion for new team members
- Poor project understanding
- Wasted time searching for information

### Solution
An intelligent system that:
- Automatically generates comprehensive documentation
- Provides AI-powered Q&A about codebases
- Analyzes pull requests for documentation updates
- Detects missing or outdated documentation
- Visualizes system architecture

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 14 (React framework with App Router)
- TypeScript (Type safety)
- Tailwind CSS (Styling)
- React Query (Data fetching)
- Zustand (State management)

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Alembic (Migrations)

**AI & RAG:**
- OpenAI API / Gemini API (LLM)
- LangChain (RAG framework)
- ChromaDB (Vector database)
- Sentence Transformers (Embeddings)

**External APIs:**
- GitHub API (Repository integration)

### System Architecture

```
┌─────────────┐
│   Next.js   │  Frontend (Port 3000)
│   Frontend  │
└──────┬──────┘
       │
       │ HTTP/REST
       │
┌──────▼──────┐
│   FastAPI   │  Backend (Port 8000)
│   Backend   │
└──────┬──────┘
       │
       ├─────────────┐
       │             │
┌──────▼──────┐ ┌───▼────────┐
│  PostgreSQL │ │  ChromaDB  │
│  Database   │ │   Vector   │
└─────────────┘ └────────────┘
       │
       │
┌──────▼──────┐
│  GitHub API │
│  OpenAI API │
└─────────────┘
```

## 📁 Project Structure

```
docmind-ai/
├── backend/                    # FastAPI Backend
│   ├── alembic/               # Database migrations
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── repositories.py
│   │   │       ├── documentation.py
│   │   │       ├── pull_requests.py
│   │   │       ├── chat.py
│   │   │       └── analysis.py
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/            # Database models
│   │   │   ├── __init__.py
│   │   │   └── repository.py
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── repository.py
│   │   ├── services/          # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── github_service.py
│   │   │   ├── ai_service.py
│   │   │   └── rag_service.py
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── alembic.ini
│
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # App router pages
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx       # Landing page
│   │   │   ├── globals.css
│   │   │   └── dashboard/
│   │   │       └── [id]/
│   │   │           └── page.tsx
│   │   ├── components/        # React components
│   │   │   ├── providers.tsx
│   │   │   ├── markdown-viewer.tsx
│   │   │   ├── chat-interface.tsx
│   │   │   └── ui/            # UI components
│   │   │       ├── button.tsx
│   │   │       ├── input.tsx
│   │   │       └── card.tsx
│   │   └── lib/               # Utilities
│   │       ├── api.ts         # API client
│   │       ├── store.ts       # State management
│   │       └── utils.ts       # Helper functions
│   ├── public/                # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── postcss.config.js
│   └── .env.example
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md        # System architecture
│   ├── API.md                 # API documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── IMPLEMENTATION_PLAN.md # Development plan
│
├── README.md                   # Main readme
├── QUICKSTART.md              # Quick start guide
├── PROJECT_SUMMARY.md         # This file
└── .gitignore
```

## ✨ Core Features

### 1. GitHub Repository Integration
- Connect any public GitHub repository
- Fetch repository structure and files
- Analyze codebase contents
- Support for multiple programming languages

### 2. AI Documentation Generator
Automatically generates:
- **README**: Project overview, setup, usage
- **API Documentation**: Endpoints, parameters, responses
- **Architecture**: System design, components, data flow
- **Setup Instructions**: Installation and configuration

### 3. Pull Request Change Analyzer
- Detects changed files in PRs
- Compares previous and updated code
- Generates PR summaries
- Identifies affected modules
- Suggests documentation updates

### 4. Missing Documentation Detector
Identifies:
- Undocumented functions
- Undocumented APIs
- Missing comments
- Outdated sections
- Dead endpoints

### 5. Developer Q&A Assistant (RAG)
- Repository chatbot powered by RAG
- Semantic search across codebase
- Context-aware answers
- Source references
- Chat history

### 6. Architecture Visualizer
- Generates system architecture diagrams
- Uses Mermaid.js for visualization
- Identifies components and relationships
- Shows technology stack

### 7. Auto Documentation Updates
- Re-analyzes modified files
- Regenerates impacted documentation
- Maintains version history
- Tracks changes over time

## 🔌 API Endpoints

### Repositories
- `POST /api/v1/repositories/analyze` - Analyze repository
- `GET /api/v1/repositories/{id}` - Get repository details
- `GET /api/v1/repositories` - List repositories
- `GET /api/v1/repositories/{id}/structure` - Get file structure
- `GET /api/v1/repositories/{id}/files` - Get file content

### Documentation
- `POST /api/v1/documentation/generate` - Generate documentation
- `GET /api/v1/documentation/{repo_id}` - Get documentation
- `GET /api/v1/documentation/{repo_id}/list` - List all docs
- `PUT /api/v1/documentation/{id}` - Update documentation

### Chat
- `POST /api/v1/chat/sessions` - Create chat session
- `POST /api/v1/chat/sessions/{id}/messages` - Send message
- `GET /api/v1/chat/sessions/{id}/messages` - Get history
- `POST /api/v1/chat/search` - Search repository

### Pull Requests
- `POST /api/v1/prs/analyze` - Analyze pull request
- `GET /api/v1/prs/{repo_id}` - List pull requests

### Analysis
- `POST /api/v1/analysis/missing-docs` - Detect missing docs
- `POST /api/v1/analysis/architecture` - Generate architecture

## 💾 Database Schema

### Tables
- **repositories**: GitHub repository metadata
- **documentations**: Generated documentation
- **documentation_versions**: Version history
- **pull_requests**: PR analysis results
- **files**: Repository files
- **file_changes**: PR file changes
- **chat_sessions**: Chat sessions
- **chat_messages**: Chat messages

## 🚀 Getting Started

### Quick Start (10 minutes)

1. **Clone and setup:**
```bash
git clone <repo-url>
cd docmind-ai
```

2. **Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload
```

3. **Frontend:**
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

4. **Visit:** http://localhost:3000

### Required API Keys
- **OpenAI API Key** or **Gemini API Key**
- **GitHub Personal Access Token**

## 📊 Data Flow

### Repository Analysis Flow
1. User enters GitHub URL
2. Backend fetches repository metadata
3. Downloads file structure and contents
4. Stores in PostgreSQL database
5. Creates vector embeddings
6. Stores in ChromaDB
7. Returns analysis results

### Documentation Generation Flow
1. User requests documentation
2. Backend retrieves repository files
3. Sends to AI with structured prompts
4. AI generates markdown documentation
5. Stores in database with version
6. Returns to frontend for display

### Chat Flow
1. User asks question
2. Backend performs semantic search in ChromaDB
3. Retrieves relevant code chunks
4. Constructs prompt with context
5. Sends to AI for answer generation
6. Returns answer with source references

## 🎯 MVP Features (24-Hour Hackathon)

### Must-Have ✅
- [x] Repository analysis from GitHub URL
- [x] README generation
- [x] Basic chat interface
- [x] Markdown rendering
- [x] File tree display
- [x] Clean, modern UI

### Should-Have ✅
- [x] API documentation generation
- [x] Architecture diagrams
- [x] RAG-based Q&A with sources
- [x] Multiple documentation types
- [x] Dark mode support

### Nice-to-Have 🔄
- [ ] PR analysis
- [ ] Missing docs detection
- [ ] Real-time updates
- [ ] Export functionality
- [ ] Webhook integration

## 🔮 Future Enhancements

### Short-term (1-2 months)
- Private repository support (OAuth)
- Team collaboration features
- CI/CD integration
- Custom documentation templates
- Export to PDF/Confluence/Notion

### Long-term (3-6 months)
- Multi-repository workspaces
- Code quality metrics
- API endpoint testing
- Slack/Discord integration
- Version comparison
- Technical debt analysis

## 📈 Scalability

### Current (MVP)
- Single server deployment
- PostgreSQL database
- ChromaDB local storage
- Synchronous processing

### Future (Production)
- Load balanced servers
- Managed PostgreSQL (Supabase)
- Pinecone/Weaviate for vectors
- Background job queue (Celery)
- Redis caching
- CDN for static assets

## 🔒 Security

- HTTPS in production
- Environment variables for secrets
- CORS configuration
- Rate limiting
- Input validation
- SQL injection prevention (SQLAlchemy)

## 💰 Cost Estimation

### Development (Free Tier)
- Vercel: Free
- Railway: $5/month credit
- Supabase: Free tier
- OpenAI: Pay per use (~$0.01-0.10/request)
- **Total**: ~$10-20/month

### Production Scale
- Vercel Pro: $20/month
- Railway: $20-50/month
- Database: $25/month
- OpenAI: $50-200/month
- **Total**: ~$115-295/month

## 📚 Documentation

- **README.md**: Project overview and features
- **QUICKSTART.md**: 10-minute setup guide
- **docs/ARCHITECTURE.md**: System architecture
- **docs/API.md**: Complete API reference
- **docs/DEPLOYMENT.md**: Deployment instructions
- **docs/IMPLEMENTATION_PLAN.md**: 24-hour hackathon plan

## 🛠️ Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Git

### Tech Decisions

**Why Next.js?**
- Server-side rendering
- Great developer experience
- Easy deployment
- Built-in optimization

**Why FastAPI?**
- High performance (async)
- Automatic API docs
- Type safety
- Python AI ecosystem

**Why ChromaDB?**
- Simple setup for MVP
- Built-in embeddings
- Good for hackathons
- Can migrate to Pinecone later

**Why PostgreSQL?**
- Robust and reliable
- JSON support
- Vector extension (pgvector)
- Wide hosting support

## 🎓 Learning Resources

- FastAPI: https://fastapi.tiangolo.com
- Next.js: https://nextjs.org/docs
- LangChain: https://python.langchain.com
- ChromaDB: https://docs.trychroma.com
- GitHub API: https://docs.github.com/en/rest
- OpenAI API: https://platform.openai.com/docs

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License - Free to use for personal and commercial projects

## 👥 Team

Built for hackathons by developers who care about documentation.

---

**Made with ❤️ for developers who hate outdated docs**

For questions or support, check the documentation in `/docs` or open an issue on GitHub.
