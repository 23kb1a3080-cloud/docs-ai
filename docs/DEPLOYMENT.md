# DocMind AI - Deployment Guide

## Quick Deployment (Production)

### Prerequisites
- GitHub account
- Vercel account (for frontend)
- Railway/Render account (for backend)
- Supabase/Neon account (for database)
- OpenAI or Gemini API key
- GitHub Personal Access Token

## Option 1: Railway + Vercel (Recommended)

### Step 1: Deploy Database (Supabase)

1. Go to [Supabase](https://supabase.com)
2. Create new project
3. Wait for database to provision
4. Copy connection string from Settings > Database
5. Format: `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`

### Step 2: Deploy Backend (Railway)

1. Go to [Railway](https://railway.app)
2. Click "New Project" > "Deploy from GitHub repo"
3. Select your repository
4. Choose `backend` as root directory
5. Add environment variables:

```env
DATABASE_URL=postgresql://...  # From Supabase
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
CORS_ORIGINS=https://your-frontend.vercel.app
SECRET_KEY=your-secret-key-here
CHROMA_PERSIST_DIRECTORY=/app/chroma_db
```

6. Add build command: `pip install -r requirements.txt`
7. Add start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
8. Deploy and copy the public URL

### Step 3: Deploy Frontend (Vercel)

1. Go to [Vercel](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Set root directory to `frontend`
5. Add environment variable:

```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

6. Deploy
7. Your app is live! 🎉

## Option 2: Render (All-in-One)

### Deploy Database
1. Create PostgreSQL database on Render
2. Copy internal connection string

### Deploy Backend
1. Create new Web Service
2. Connect GitHub repository
3. Settings:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables (same as Railway)
5. Deploy

### Deploy Frontend
1. Create new Static Site
2. Settings:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Publish Directory: `.next`
3. Add environment variables
4. Deploy

## Local Development Setup

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
# Required:
# - DATABASE_URL
# - OPENAI_API_KEY or GEMINI_API_KEY
# - GITHUB_TOKEN

# Run database migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/api/docs`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Edit .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Docker Deployment (Optional)

### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner

WORKDIR /app

COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: docmind
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/docmind
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      GITHUB_TOKEN: ${GITHUB_TOKEN}
    depends_on:
      - postgres
    volumes:
      - ./backend:/app
      - chroma_data:/app/chroma_db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
  chroma_data:
```

Run with:
```bash
docker-compose up -d
```

## Environment Variables Reference

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# AI Provider (choose one)
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
AI_PROVIDER=openai  # or "gemini"

# GitHub
GITHUB_TOKEN=ghp_...

# Application
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-min-32-chars

# CORS
CORS_ORIGINS=https://your-frontend.vercel.app,https://www.yourdomain.com

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db

# LLM Settings
LLM_MODEL=gpt-4-turbo-preview  # or gemini-pro
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4000
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## Database Setup

### Create Database Tables

```bash
cd backend

# Using Alembic (recommended)
alembic upgrade head

# Or using Python directly
python -c "from app.core.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Troubleshooting

### Backend Issues

**Database connection failed**
- Check DATABASE_URL format
- Ensure database is running
- Verify network access

**OpenAI API errors**
- Verify API key is valid
- Check API quota/billing
- Try with lower rate limits

**GitHub API rate limit**
- Use authenticated token
- Implement caching
- Reduce API calls

### Frontend Issues

**API connection failed**
- Check NEXT_PUBLIC_API_URL
- Verify CORS settings on backend
- Check network/firewall

**Build errors**
- Clear `.next` folder
- Delete `node_modules` and reinstall
- Check Node.js version (18+)

### Performance Issues

**Slow documentation generation**
- Use faster LLM model
- Reduce max tokens
- Implement caching

**High memory usage**
- Limit concurrent requests
- Reduce chunk size
- Use pagination

## Monitoring & Logging

### Backend Logging

Logs are output to stdout. Configure log aggregation:

**Railway**: Automatic log collection
**Render**: View in dashboard
**Docker**: `docker-compose logs -f backend`

### Error Tracking

Add Sentry for error tracking:

```bash
pip install sentry-sdk
```

In `app/main.py`:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment="production"
)
```

### Health Checks

Backend health endpoint: `GET /health`

```bash
curl https://your-backend.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "DocMind AI",
  "version": "1.0.0"
}
```

## Scaling Considerations

### Horizontal Scaling
- Deploy multiple backend instances
- Use load balancer
- Implement session affinity for chat

### Database Scaling
- Enable connection pooling
- Add read replicas
- Implement caching (Redis)

### Vector Database Scaling
- Migrate to Pinecone/Weaviate
- Implement sharding
- Use managed service

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Set strong SECRET_KEY
- [ ] Enable CORS only for your domain
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Add authentication (future)
- [ ] Regular dependency updates
- [ ] Database backups enabled

## Cost Estimation

### Free Tier (MVP)
- **Vercel**: Free for hobby projects
- **Railway**: $5/month credit (enough for small apps)
- **Supabase**: Free tier (500MB database)
- **OpenAI**: Pay per use (~$0.01-0.10 per request)
- **Total**: ~$10-20/month

### Production Scale
- **Vercel Pro**: $20/month
- **Railway**: $20-50/month
- **Database**: $25/month
- **OpenAI**: $50-200/month (depends on usage)
- **Total**: ~$115-295/month

## Backup & Recovery

### Database Backups
```bash
# Backup
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

### ChromaDB Backups
```bash
# Backup vector database
tar -czf chroma_backup.tar.gz chroma_db/

# Restore
tar -xzf chroma_backup.tar.gz
```

## Support & Resources

- **Documentation**: See `/docs` folder
- **API Docs**: `https://your-backend/api/docs`
- **Issues**: GitHub Issues
- **Community**: Discord/Slack (setup if needed)

---

**Deployment Complete!** 🚀

Your DocMind AI instance should now be live and ready to analyze repositories.
