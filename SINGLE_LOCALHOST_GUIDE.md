# 🚀 DocMind AI - Single Command Startup Guide

## ✅ Quick Start (One Command!)

### Windows Users

Simply double-click or run:
```bash
start.bat
```

This will:
1. ✅ Start the backend server (http://localhost:8000)
2. ✅ Start the frontend server (http://localhost:3000)
3. ✅ Open the application in your browser automatically
4. ✅ Show you both server windows

---

## 🎯 What Happens

When you run `start.bat`:

1. **Backend starts** on port 8000
   - FastAPI server with all APIs
   - SQLite database
   - AI services ready

2. **Frontend starts** on port 3000
   - Next.js React application
   - Connects to backend automatically
   - Modern UI ready

3. **Browser opens** automatically to http://localhost:3000

---

## 🔧 Configuration

### Before First Run

**IMPORTANT**: Add your OpenAI API key!

Edit `backend\.env`:
```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

---

## 🌐 Access Points

Once started, you can access:

| Service | URL | Description |
|---------|-----|-------------|
| **Main App** | http://localhost:3000 | Frontend UI |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/api/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/health | Server status |

---

## 🛑 Stopping the Servers

### Option 1: Using start.bat
Press any key in the `start.bat` window to stop all servers

### Option 2: Manual
Close both terminal windows:
- "DocMind AI - Backend"
- "DocMind AI - Frontend"

### Option 3: Task Manager
1. Open Task Manager (Ctrl+Shift+Esc)
2. Find and end:
   - `python.exe` (backend)
   - `node.exe` (frontend)

---

## 🔄 Restarting

Just run `start.bat` again!

---

## 📊 How It Works

```
┌─────────────────────────────────────────┐
│         start.bat (One Command)         │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│   Backend    │        │   Frontend   │
│  Port 8000   │◄───────│  Port 3000   │
│   FastAPI    │  API   │   Next.js    │
└──────────────┘        └──────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│   SQLite     │        │   Browser    │
│   Database   │        │ localhost:3000│
└──────────────┘        └──────────────┘
```

---

## 🧪 Testing After Startup

### 1. Check Backend
Open: http://localhost:8000/health

Expected response:
```json
{
  "status": "healthy",
  "app": "DocMind AI",
  "version": "1.0.0"
}
```

### 2. Check Frontend
Open: http://localhost:3000

Expected: DocMind AI landing page loads

### 3. Test Full Flow
1. Enter a GitHub URL: `https://github.com/fastapi/fastapi`
2. Click "Analyze"
3. Wait for analysis
4. View generated documentation

---

## 🛠️ Troubleshooting

### Problem: "Port already in use"

**Solution 1**: Stop other services using ports 8000 or 3000
```bash
# Check what's using port 8000
netstat -ano | findstr :8000

# Check what's using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Solution 2**: Change ports in configuration
- Backend: Edit `backend/app/main.py` (change port 8000)
- Frontend: Edit `frontend/package.json` (change port 3000)

### Problem: "Backend not starting"

**Causes**:
1. Virtual environment not activated
2. Dependencies not installed
3. Python not found

**Solutions**:
```bash
# Reinstall dependencies
cd backend
.\venv\Scripts\pip.exe install -r requirements-minimal.txt
```

### Problem: "Frontend not starting"

**Causes**:
1. Node modules not installed
2. npm not found

**Solutions**:
```bash
# Reinstall dependencies
cd frontend
npm install
```

### Problem: "OpenAI API error"

**Solution**: Add your API key to `backend\.env`
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

---

## 📁 File Structure

```
DocMind AI/
├── start.bat                    # ⭐ ONE-CLICK STARTUP
├── backend/
│   ├── .env                     # Configuration (add API key here)
│   ├── requirements-minimal.txt # Fast installation
│   └── app/                     # FastAPI application
├── frontend/
│   ├── package.json             # Frontend dependencies
│   └── src/                     # React/Next.js code
└── docs/                        # Documentation
```

---

## 🎨 Features Available

### ✅ Working Features
- GitHub repository analysis
- AI-powered documentation generation
- Pull request analysis
- Basic chat assistant
- File browsing
- Architecture diagrams
- Missing documentation detection

### 📊 API Endpoints
- Repository management
- Documentation generation
- Chat interface
- Pull request analysis
- Code analysis

---

## 💡 Usage Tips

1. **Start with small repos** - Faster analysis
2. **Use public repos** - No GitHub token needed
3. **Monitor costs** - Check OpenAI usage
4. **Keep servers running** - Don't close terminal windows
5. **Check logs** - Look at terminal output for errors

---

## 🔐 Security Notes

1. **Never commit `.env` files** - Contains API keys
2. **Keep API keys secret** - Don't share them
3. **Use environment variables** - For sensitive data
4. **Change SECRET_KEY** - In production
5. **Enable rate limiting** - For production use

---

## 📚 Additional Documentation

- **Complete Setup**: `COMPLETE_SETUP.md`
- **Status**: `STATUS.md`
- **Quick Start**: `START_HERE.md`
- **API Docs**: http://localhost:8000/api/docs

---

## 🎯 Example Workflow

1. **Start servers**: Run `start.bat`
2. **Wait 10 seconds**: Servers initialize
3. **Browser opens**: Automatically to localhost:3000
4. **Enter GitHub URL**: Try `https://github.com/fastapi/fastapi`
5. **Click Analyze**: Wait 30-60 seconds
6. **View Dashboard**: See repository analysis
7. **Generate Docs**: Click "Generate Documentation"
8. **View Results**: AI-generated documentation

---

## 🚀 Advanced: Manual Startup

If you prefer manual control:

### Terminal 1 - Backend
```bash
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

---

## ✅ Checklist Before Using

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] OpenAI API key added to `backend\.env`
- [ ] Ports 8000 and 3000 available
- [ ] Internet connection active

---

## 🎉 You're Ready!

Just run:
```bash
start.bat
```

And start building amazing documentation with AI! 🚀

---

**Need help?** Check `COMPLETE_SETUP.md` for detailed troubleshooting.
