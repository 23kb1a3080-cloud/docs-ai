#!/bin/bash

# DocMind AI - Setup Script
# This script helps you set up the project quickly

set -e

echo "🚀 DocMind AI - Setup Script"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js 18 or higher"
    exit 1
fi

echo -e "${GREEN}✓${NC} Node.js found: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} npm found: $(npm --version)"

echo ""
echo "📦 Setting up Backend..."
echo "================================"

# Backend setup
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${YELLOW}⚠${NC} Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Python dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠${NC} Please edit backend/.env with your API keys"
else
    echo -e "${YELLOW}⚠${NC} .env file already exists"
fi

cd ..

echo ""
echo "🎨 Setting up Frontend..."
echo "================================"

# Frontend setup
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install
echo -e "${GREEN}✓${NC} Node.js dependencies installed"

# Create .env.local file if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.example .env.local
    echo -e "${GREEN}✓${NC} .env.local created"
else
    echo -e "${YELLOW}⚠${NC} .env.local file already exists"
fi

cd ..

echo ""
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Configure API Keys:"
echo "   - Edit backend/.env with your:"
echo "     • OPENAI_API_KEY or GEMINI_API_KEY"
echo "     • GITHUB_TOKEN"
echo "     • DATABASE_URL (optional, defaults to SQLite)"
echo ""
echo "2. Start the Backend:"
echo "   cd backend"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3. Start the Frontend (in a new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open your browser:"
echo "   http://localhost:3000"
echo ""
echo "📚 Documentation:"
echo "   - Quick Start: QUICKSTART.md"
echo "   - Full Docs: docs/"
echo ""
echo "🎉 Happy coding!"
