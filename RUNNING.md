# DocMind AI - Running Guide

## ✅ Backend is Running!

Your backend server is now running at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

## Current Setup

### Backend (✅ Running)
- FastAPI server on port 8000
- SQLite database (docmind.db)
- Minimal dependencies installed
- OpenAI integration ready

### What's Working
✅ Core API endpoints
✅ GitHub repository integration
✅ Documentation generation (with OpenAI)
✅ Database models
✅ Health check endpoint

### What's Simplified for Demo
- Using SQLite instead of PostgreSQL
- Using keyword search instead of vector embeddings
- Minimal dependencies (no heavy ML libraries)
- In-memory RAG storage

## Next Steps

### 1. Add Your OpenAI API Key

Edit `backend/.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 2. Test the API

Visit the interactive API documentation:
```
http://localhost:8000/api/docs
```

Try the health check endpoint:
```
curl http://localhost:8000/health
```

### 3. Setup Frontend (Optional)

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on http://localhost:3000

## API Endpoints

### Repositories
- `POST /api/v1/repositories/analyze` - Analyze a GitHub repository
- `GET /api/v1/repositories` - List all repositories
- `GET /api/v1/repositories/{id}` - Get repository details
- `GET /api/v1/repositories/{id}/structure` - Get repository structure

### Documentation
- `POST /api/v1/documentation/generate` - Generate documentation
- `GET /api/v1/documentation/{repo_id}` - Get all documentation
- `GET /api/v1/documentation/{repo_id}/{doc_type}` - Get specific doc type

### Pull Requests
- `GET /api/v1/pull-requests/{repo_id}` - List pull requests
- `POST /api/v1/pull-requests/{repo_id}/{pr_number}/analyze` - Analyze PR

### Chat
- `POST /api/v1/chat/sessions` - Create chat session
- `POST /api/v1/chat/sessions/{session_id}/message` - Send message

### Analysis
- `POST /api/v1/analysis/detect-undocumented` - Detect undocumented code

## Example Usage

### Analyze a Repository

```bash
curl -X POST "http://localhost:8000/api/v1/repositories/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "github_url": "https://github.com/username/repo"
  }'
```

### Generate Documentation

```bash
curl -X POST "http://localhost:8000/api/v1/documentation/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "repository_id": "your-repo-id",
    "doc_types": ["readme", "api", "architecture"]
  }'
```

## Stopping the Server

The server is running in the background. To stop it:
1. Find the terminal/process running uvicorn
2. Press Ctrl+C

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Verify Python virtual environment is activated
- Check `.env` file exists in backend folder

### API returns errors
- Verify OpenAI API key is set in `.env`
- Check the server logs for detailed error messages
- Ensure database file has write permissions

### GitHub API rate limits
- Add a GitHub token to `.env` for higher rate limits:
  ```
  GITHUB_TOKEN=ghp_your_token_here
  ```

## Development

### Reload on Changes
The server is running with `--reload` flag, so it will automatically restart when you modify Python files.

### View Logs
Check the terminal where uvicorn is running for real-time logs.

### Database
SQLite database file: `backend/docmind.db`

To reset the database, simply delete this file and restart the server.

## Production Deployment

For production, see `docs/DEPLOYMENT.md` for:
- PostgreSQL setup
- Environment configuration
- Docker deployment
- Security best practices

---

**Status**: Backend Running ✅
**Next**: Add OpenAI API key and test endpoints!
