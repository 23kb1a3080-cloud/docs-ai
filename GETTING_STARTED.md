# 🚀 Getting Started with DocMind AI

Welcome to DocMind AI! This guide will help you get up and running quickly.

## 📋 What You Have

A complete full-stack AI application with:
- ✅ **Backend**: FastAPI with AI integration
- ✅ **Frontend**: Next.js with modern UI
- ✅ **Database**: PostgreSQL/SQLite support
- ✅ **AI**: OpenAI/Gemini integration
- ✅ **RAG**: ChromaDB vector database
- ✅ **Documentation**: Complete guides

## 🎯 Choose Your Path

### Path 1: Quick Demo (10 minutes)
**Goal**: See the app running locally

1. **Run Setup Script**
   ```bash
   # Mac/Linux
   chmod +x setup.sh
   ./setup.sh
   
   # Windows
   setup.bat
   ```

2. **Add API Keys**
   - Edit `backend/.env`
   - Add your OpenAI/Gemini API key
   - Add your GitHub token

3. **Start Backend**
   ```bash
   cd backend
   source venv/bin/activate  # Windows: venv\Scripts\activate
   uvicorn app.main:app --reload
   ```

4. **Start Frontend** (new terminal)
   ```bash
   cd frontend
   npm run dev
   ```

5. **Visit**: http://localhost:3000

📖 **Detailed Guide**: See `QUICKSTART.md`

---

### Path 2: Understand First (30 minutes)
**Goal**: Learn the architecture before coding

1. **Read Documentation**
   - `README.md` - Project overview
   - `docs/ARCHITECTURE.md` - System design
   - `docs/API.md` - API reference

2. **Explore Code**
   - `backend/app/main.py` - Backend entry
   - `frontend/src/app/page.tsx` - Frontend entry
   - `backend/app/services/` - Core logic

3. **Then Follow Path 1**

📖 **Detailed Guide**: See `PROJECT_SUMMARY.md`

---

### Path 3: Deploy to Production (2 hours)
**Goal**: Get the app live on the internet

1. **Setup Accounts**
   - Vercel (frontend)
   - Railway/Render (backend)
   - Supabase (database)

2. **Deploy Backend**
   - Push to GitHub
   - Connect to Railway
   - Add environment variables
   - Deploy

3. **Deploy Frontend**
   - Connect to Vercel
   - Add backend URL
   - Deploy

4. **Test Live App**

📖 **Detailed Guide**: See `docs/DEPLOYMENT.md`

---

### Path 4: Hackathon Mode (24 hours)
**Goal**: Build MVP for demo

1. **Hour 0-4**: Setup & Core (Path 1)
2. **Hour 4-12**: AI Documentation
3. **Hour 12-18**: RAG Chat
4. **Hour 18-24**: Polish & Demo

📖 **Detailed Guide**: See `docs/IMPLEMENTATION_PLAN.md`

---

## 🔑 Required API Keys

### OpenAI API Key (Recommended)
1. Go to https://platform.openai.com
2. Sign up / Log in
3. Create API key
4. Add to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-...
   AI_PROVIDER=openai
   ```

### Gemini API Key (Alternative)
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Add to `backend/.env`:
   ```
   GEMINI_API_KEY=...
   AI_PROVIDER=gemini
   ```

### GitHub Token
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select `public_repo` scope
4. Add to `backend/.env`:
   ```
   GITHUB_TOKEN=ghp_...
   ```

## 📁 Project Structure

```
docmind-ai/
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   └── alembic/     # Database migrations
├── frontend/         # Next.js frontend
│   └── src/         # Source code
└── docs/            # Documentation
```

## 🎓 Learning Path

### Beginner
1. Start with `QUICKSTART.md`
2. Run the app locally
3. Try analyzing a repository
4. Explore the UI

### Intermediate
1. Read `docs/ARCHITECTURE.md`
2. Understand the data flow
3. Modify a component
4. Add a new feature

### Advanced
1. Read `docs/IMPLEMENTATION_PLAN.md`
2. Implement missing features
3. Optimize performance
4. Deploy to production

## 🛠️ Common Tasks

### Add a New API Endpoint
1. Create route in `backend/app/api/v1/`
2. Add service logic in `backend/app/services/`
3. Update schemas in `backend/app/schemas/`
4. Test at http://localhost:8000/api/docs

### Add a New UI Component
1. Create component in `frontend/src/components/`
2. Import in page
3. Style with Tailwind CSS
4. Test in browser

### Change AI Model
Edit `backend/.env`:
```env
# For GPT-4
LLM_MODEL=gpt-4-turbo-preview

# For GPT-3.5 (cheaper)
LLM_MODEL=gpt-3.5-turbo

# For Gemini
AI_PROVIDER=gemini
LLM_MODEL=gemini-pro
```

### Use Different Database
Edit `backend/.env`:
```env
# SQLite (development)
DATABASE_URL=sqlite:///./docmind.db

# PostgreSQL (production)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt

# Check .env file exists
ls backend/.env
```

### Frontend Won't Start
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules .next
npm install
```

### Database Errors
```bash
# Reset database (SQLite)
rm backend/*.db

# Run migrations
cd backend
alembic upgrade head
```

### API Key Errors
- Verify keys are correct in `.env`
- Check API quota/billing
- Try with a different model

## 📚 Documentation Index

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| `README.md` | Project overview | 5 min |
| `QUICKSTART.md` | Setup guide | 10 min |
| `PROJECT_SUMMARY.md` | Complete overview | 15 min |
| `FILE_STRUCTURE.md` | File organization | 5 min |
| `docs/ARCHITECTURE.md` | System design | 20 min |
| `docs/API.md` | API reference | 15 min |
| `docs/DEPLOYMENT.md` | Deploy guide | 30 min |
| `docs/IMPLEMENTATION_PLAN.md` | Dev timeline | 20 min |

## 🎯 Next Steps

### Just Starting?
1. ✅ Read this file
2. ⏭️ Follow `QUICKSTART.md`
3. ⏭️ Try the demo
4. ⏭️ Read `PROJECT_SUMMARY.md`

### Ready to Code?
1. ✅ App is running
2. ⏭️ Read `docs/ARCHITECTURE.md`
3. ⏭️ Explore the codebase
4. ⏭️ Make your first change

### Ready to Deploy?
1. ✅ App works locally
2. ⏭️ Read `docs/DEPLOYMENT.md`
3. ⏭️ Setup hosting accounts
4. ⏭️ Deploy!

### Building for Hackathon?
1. ✅ Team is ready
2. ⏭️ Read `docs/IMPLEMENTATION_PLAN.md`
3. ⏭️ Divide tasks
4. ⏭️ Start coding!

## 💡 Pro Tips

1. **Start Simple**: Use SQLite and GPT-3.5 for development
2. **Test Often**: Test each feature as you build
3. **Read Logs**: Check terminal output for errors
4. **Use API Docs**: Visit http://localhost:8000/api/docs
5. **Ask for Help**: Check documentation or open an issue

## 🎉 Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can access both in browser
- [ ] API docs load successfully
- [ ] Can analyze a GitHub repository
- [ ] Documentation generates
- [ ] Chat responds to questions

## 🤝 Need Help?

1. **Check Documentation**: See `/docs` folder
2. **Review Examples**: Try with known repositories
3. **Check Logs**: Look at terminal output
4. **Search Issues**: Check GitHub issues
5. **Ask Community**: Open a new issue

## 🌟 What's Next?

After getting started:
- Customize the UI
- Add new features
- Improve AI prompts
- Deploy to production
- Share with others!

---

**Ready to start?** Choose your path above and begin! 🚀

For the fastest start, run:
```bash
./setup.sh  # or setup.bat on Windows
```

Then follow the on-screen instructions.

**Happy coding!** 💻✨
