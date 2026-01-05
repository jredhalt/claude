#!/bin/bash

# Skateskins Ad Generator - Start Script
# This script starts the FastAPI server

echo "================================================"
echo "   Skateskins Video & Ad Generator"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is not installed. Video generation will not work."
    echo "   Please install FFmpeg:"
    echo "   - Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "   - macOS: brew install ffmpeg"
    echo "   - Windows: Download from https://ffmpeg.org/download.html"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.dependencies_installed
else
    echo "✓ Dependencies already installed"
fi

# Create necessary directories
mkdir -p uploads/{broll,photos,inspiration}
mkdir -p output/{videos,static_ads}

echo ""
echo "================================================"
echo "🚀 Starting Skateskins Ad Generator..."
echo "================================================"
echo ""
echo "📍 Web Interface: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================"
echo ""

# Start the server
cd backend && python app.py
