#!/bin/bash

# Setup script for Instruction Video to Teaching Document Generator

echo "====================================="
echo "  Video to Teaching Doc Generator"
echo "  Setup Script"
echo "====================================="
echo ""

# Create directory structure
echo "Creating directory structure..."
mkdir -p data
mkdir -p output
mkdir -p src/utils
mkdir -p src/transcription
mkdir -p src/classification
mkdir -p src/filtering
mkdir -p src/grouping
mkdir -p src/document_generator
mkdir -p src/video_processing
mkdir -p src/cv_filter

# Create __init__.py files
echo "Creating __init__.py files..."
touch src/__init__.py
touch src/utils/__init__.py
touch src/transcription/__init__.py
touch src/classification/__init__.py
touch src/filtering/__init__.py
touch src/grouping/__init__.py
touch src/document_generator/__init__.py
touch src/video_processing/__init__.py
touch src/cv_filter/__init__.py

# Create .gitkeep files
touch data/.gitkeep
touch output/.gitkeep

# Check Python version
echo ""
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check for system dependencies
echo ""
echo "Checking system dependencies..."

# Check FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg is installed"
    ffmpeg -version | head -n 1
else
    echo "✗ FFmpeg is NOT installed"
    echo "  Install with: sudo apt install ffmpeg (Ubuntu) or brew install ffmpeg (macOS)"
fi

# Check Ollama
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is installed"
    ollama --version
else
    echo "✗ Ollama is NOT installed"
    echo "  Install from: https://ollama.ai"
fi

# Check gifski
if command -v gifski &> /dev/null; then
    echo "✓ gifski is installed (optional)"
else
    echo "○ gifski is NOT installed (optional, for better GIF quality)"
    echo "  Install with: brew install gifski (macOS) or cargo install gifski"
fi

# Setup environment file
echo ""
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Please edit .env and add your API keys"
else
    echo "✓ .env file already exists"
fi

# Final instructions
echo ""
echo "====================================="
echo "  Setup Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys:"
echo "   - OPENAI_API_KEY (required)"
echo "   - ANTHROPIC_API_KEY (optional)"
echo ""
echo "2. Start Ollama:"
echo "   ollama serve"
echo ""
echo "3. Pull Ollama model:"
echo "   ollama pull phi3.5:3.8b"
echo ""
echo "4. Place your video in the data/ directory"
echo ""
echo "5. Run the pipeline:"
echo "   python src/main_cli.py"
echo ""
echo "For more information, see README.md"
echo ""