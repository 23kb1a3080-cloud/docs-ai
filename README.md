# DocMind AI – Self-Updating Developer Knowledge Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)

## 🎯 Project Overview

DocMind AI is an intelligent developer assistant that automatically generates, updates, and explains technical documentation from GitHub repositories. It transforms any codebase into a living knowledge system that continuously maintains documentation and helps developers understand projects instantly.

### 🎥 Demo
![DocMind AI Demo](https://via.placeholder.com/800x400?text=DocMind+AI+Demo)

### ⚡ Quick Links
- 📖 [Quick Start Guide](QUICKSTART.md) - Get running in 10 minutes
- 🏗️ [Architecture](docs/ARCHITECTURE.md) - System design
- 🚀 [Deployment Guide](docs/DEPLOYMENT.md) - Production setup
- 📚 [API Documentation](docs/API.md) - Complete API reference
- 🎯 [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) - 24-hour hackathon guide

## 🚀 Problem Statement

Developers rarely update documentation, resulting in:
- Outdated API documentation
- Onboarding confusion for new team members
- Poor project understanding
- Wasted time searching for information

## 💡 Solution

An AI-powered system that:
- Automatically generates comprehensive documentation
- Analyzes pull requests for documentation updates
- Provides intelligent Q&A about the codebase
- Visualizes system architecture
- Detects missing or outdated documentation

## ✨ Core Features

### 1. GitHub Repository Integration
- Connect any public GitHub repository
- Fetch and analyze repository structure
- Read and process codebase contents

### 2. AI Documentation Generator
Automatically generates:
- README and project overview
- Setup instructions
- Folder structure explanation
- API documentation
- Architecture explanation
- Tech stack summary
- Module descriptions

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
Repository chatbot that answers:
- "Explain authentication flow"
- "How does payment work?"
- "Where is login implemented?"
- "How do I run this project?"

### 6. Architecture Visualizer
Generates system architecture diagrams using Mermaid.js

### 7. Auto Documentation Updates
- Re-analyzes modified files
- Regenerates impacted documentation
- Maintains version history

## 🏗️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Shadcn/ui** - UI components
- **Mermaid.js** - Architecture visualization

### Backend
- **FastAPI** - Python web framework
- **Python 3.11+** - Backend language
- **Pydantic** - Data validation

### AI & RAG
- **OpenAI API / Gemini API** - LLM for generation
- **LangChain** - RAG framework
- **ChromaDB** - Vector database
- **Sentence Transformers** - Embeddings

### Database
- **PostgreSQL** - Primary database
- **SQLAlchemy** - ORM

### External APIs
- **GitHub API** - Repository integration

## 📁 Project Structure

```
docmind-ai/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities
│   │   ├── hooks/           # Custom hooks
│   │   └── types/           # TypeScript types
│   ├── public/              # Static assets
│   └── package.json
│
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── .env.example
│
├── docs/                    # Project documentation
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── DEPLOYMENT.md
│
└── README.md
```

## 🚀 Quick Start

### ⚡ One-Command Startup (Windows)

```bash
start.bat
```

This will:
1. Start backend server (http://localhost:8000)
2. Start frontend server (http://localhost:3000)
3. Open application in browser automatically

### Prerequisites
- Node.js 18+
- Python 3.10+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- Git

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/23kb1a3080-cloud/docs-ai.git
cd docs-ai
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements-minimal.txt
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
```

#### 4. Configuration
Edit `backend\.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

#### 5. Start Application
```bash
# Windows - One command
start.bat

# Or manually start both servers
# Terminal 1 - Backend
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Visit `http://localhost:3000`

### 📚 Documentation
- **[Quick Start](START_HERE.md)** - 3-step guide
- **[Single Localhost Guide](SINGLE_LOCALHOST_GUIDE.md)** - One-command startup
- **[Complete Setup](COMPLETE_SETUP.md)** - Detailed installation
- **[Status](STATUS.md)** - Current system status

## 📊 System Architecture

```mermaid
graph TB
    A[User] --> B[Next.js Frontend]
    B --> C[FastAPI Backend]
    C --> D[GitHub API]
    C --> E[OpenAI/Gemini API]
    C --> F[ChromaDB Vector Store]
    C --> G[PostgreSQL Database]
    E --> H[LangChain RAG Pipeline]
    F --> H
    H --> C
```

## 🎯 MVP Features (24-Hour Hackathon)

### Phase 1: Core Setup (4 hours)
- [ ] Project scaffolding
- [ ] Database setup
- [ ] GitHub API integration
- [ ] Basic UI layout

### Phase 2: Documentation Generation (8 hours)
- [ ] Repository analysis
- [ ] AI documentation generation
- [ ] Markdown rendering
- [ ] File tree visualization

### Phase 3: RAG Chat (6 hours)
- [ ] Document chunking
- [ ] Vector embeddings
- [ ] ChromaDB integration
- [ ] Chat interface

### Phase 4: Polish & Demo (6 hours)
- [ ] UI improvements
- [ ] Error handling
- [ ] Demo preparation
- [ ] Deployment

## 🔮 Future Scope

- **Multi-repository support** - Analyze multiple repos
- **Private repository access** - OAuth integration
- **Team collaboration** - Shared documentation workspaces
- **CI/CD integration** - Auto-update on deployments
- **Custom templates** - Organization-specific doc formats
- **Code quality metrics** - Technical debt analysis
- **API endpoint testing** - Auto-generate test cases
- **Slack/Discord integration** - Bot notifications
- **Version comparison** - Track documentation changes over time
- **Export options** - PDF, Confluence, Notion

## 🚀 Deployment

### Backend (Railway/Render)
```bash
# Deploy to Railway
railway up

# Or deploy to Render
# Connect GitHub repo and set environment variables
```

### Frontend (Vercel)
```bash
# Deploy to Vercel
vercel --prod

# Or connect GitHub repo in Vercel dashboard
```

### Database (Supabase/Neon)
- Use managed PostgreSQL service
- Update connection string in backend .env

## 📝 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/docmind
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for your hackathon or personal projects.

## 👥 Team

Built for hackathons by developers who care about documentation.

---

**Made with ❤️ for developers who hate outdated docs**
