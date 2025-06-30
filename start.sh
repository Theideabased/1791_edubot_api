#!/bin/bash

# EduBot API Startup Script

echo "🤖 Starting EduBot API..."
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating required directories..."
mkdir -p generated_pdfs
mkdir -p logs

# Check if API keys are set (optional warnings)
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY environment variable not set"
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Warning: GEMINI_API_KEY environment variable not set"
fi

if [ -z "$MISTRAL_API_KEY" ]; then
    echo "⚠️  Warning: MISTRAL_API_KEY environment variable not set"
fi

echo ""
echo "🚀 Starting EduBot API server..."
echo "================================"
echo "📍 URL: http://localhost:8000"
echo "📖 Docs: http://localhost:8000/docs"
echo "📚 ReDoc: http://localhost:8000/redoc"
echo "💾 Postman Collection: postman_collection.json"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

# Start the server
python main.py
