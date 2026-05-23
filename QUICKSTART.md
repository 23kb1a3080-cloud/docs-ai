# DocMind AI - Quick Start Guide

Get DocMind AI running in 10 minutes! 🚀

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or use SQLite for testing)
- OpenAI API Key or Gemini API Key
- GitHub Personal Access Token

## Step 1: Clone & Setup (2 minutes)

```bash
# Clone the repository
git clone <your-repo-url>
cd docmind-ai

# Or if you're starting fresh, the files are already created
```

## Step 2: Backend Setup (4 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

**Edit `.env` file with your credentials:**

```env
# Minimum required for testing:
DATABASE_URL=sqlite:///./docmind.db
OPENAI_API_KEY=sk-your-key-here
GITHUB_TOKEN=ghp_your-token-here
CORS_ORIGINS=http://localhost:3000
```

**Start the backend:**

```bash
# Run the server
uvicorn app.main:app --reload --port 8000
```

✅ Backend running at http://localhost:8000
📚 API docs at http://localhost:8000/api/docs

## Step 3: Frontend Setup (4 minutes)

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
```

**Edit `.env.local`:**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Start the frontend:**

```bash
npm run dev
```

✅ Frontend running at http://localhost:3000

## Step 4: Test It Out! (2 minutes)

1. Open http://localhost:3000 in your browser
2. Enter a GitHub repository URL (try: `https://github.com/fastapi/fastapi`)
3. Click "Analyze"
4. Wait for analysis to complete
5. Generate documentation
6. Try the AI chat!

## Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com
2. Sign up / Log in
3. Go to API Keys section
4. Create new secret key
5. Copy and paste into `.env`

### GitHub Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (for private repos) or just `public_repo`
4. Generate and copy token
5. Paste into `.env`

### Gemini API Key (Alternative to OpenAI)
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Use in `.env` with `AI_PROVIDER=gemini`

## Troubleshooting

### Backend won't start

**Error: "No module named 'app'"**
```bash
# Make sure you're in the backend directory
cd backend
# And virtual environment is activated
```

**Error: "Database connection failed"**
```bash
# For quick testing, use SQLite:
DATABASE_URL=sqlite:///./docmind.db
```

### Frontend won't start

**Error: "Cannot find module"**
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

**Error: "API connection failed"**
- Make sure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in .env.local

### API Errors

**Error: "GitHub API rate limit"**
- Make sure GITHUB_TOKEN is set correctly
- Wait a few minutes and try again

**Error: "OpenAI API error"**
- Verify API key is correct
- Check you have credits/billing enabled
- Try with a smaller repository first

## What to Try

### Good Test Repositories
- Small: `https://github.com/tiangolo/fastapi`
- Medium: `https://github.com/vercel/next.js`
- Your own public repos!

### Features to Test
1. **Documentation Generation**
   - Click "Generate Docs"
   - Switch between README, API, Architecture tabs

2. **AI Chat**
   - Click "Show Chat"
   - Ask: "How does this project work?"
   - Ask: "Explain the authentication flow"

3. **File Explorer**
   - Browse repository files in left sidebar
   - Click on files to view content

## Next Steps

### For Development
- Read `docs/IMPLEMENTATION_PLAN.md` for detailed guide
- Check `docs/ARCHITECTURE.md` for system design
- See `docs/API.md` for API documentation

### For Deployment
- Follow `docs/DEPLOYMENT.md` for production setup
- Deploy backend to Railway/Render
- Deploy frontend to Vercel
- Use managed PostgreSQL (Supabase/Neon)

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Change port: `uvicorn app.main:app --port 8001` |
| Port 3000 already in use | Frontend will auto-suggest 3001 |
| Slow documentation generation | Normal for large repos, try smaller ones first |
| Chat not responding | Check backend logs, verify ChromaDB is working |
| CORS errors | Verify CORS_ORIGINS includes frontend URL |

## Development Tips

### Hot Reload
Both backend and frontend support hot reload:
- Backend: Changes auto-reload with `--reload` flag
- Frontend: Changes auto-refresh in browser

### Debugging
- Backend logs: Check terminal running uvicorn
- Frontend logs: Check browser console (F12)
- API testing: Use http://localhost:8000/api/docs

### Database Reset
```bash
# SQLite
rm docmind.db

# PostgreSQL
# Drop and recreate database
```

## Project Structure

```
docmind-ai/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── core/     # Config & database
│   │   ├── models/   # Database models
│   │   ├── schemas/  # Pydantic schemas
│   │   └── services/ # Business logic
│   └── requirements.txt
│
├── frontend/          # Next.js frontend
│   ├── src/
│   │   ├── app/      # Pages
│   │   ├── components/ # React components
│   │   └── lib/      # Utilities & API client
│   └── package.json
│
└── docs/             # Documentation
```

## Need Help?

- Check the `/docs` folder for detailed documentation
- Review API docs at http://localhost:8000/api/docs
- Check GitHub issues
- Review error logs in terminal

## Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can access both URLs in browser
- [ ] API docs load at /api/docs
- [ ] Can analyze a GitHub repository
- [ ] Documentation generates successfully
- [ ] Chat interface responds to questions

---

**You're all set!** 🎉

Start analyzing repositories and generating documentation with AI!
