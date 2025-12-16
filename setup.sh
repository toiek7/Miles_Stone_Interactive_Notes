#!/bin/bash

# Setup script for Instruction Video to Teaching Document Generator
# This script automates the entire environment setup.

set -e  # Exit on error

echo "====================================="
echo "  Video to Teaching Doc Generator"
echo "  Automated Setup Script"
echo "====================================="
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect OS
OS_TYPE="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
fi

echo "Detected OS: $OS_TYPE"
echo ""

# --- 1. System Dependencies ---
echo "[1/4] Checking system dependencies..."

if [ "$OS_TYPE" == "linux" ]; then
    if ! command_exists ffmpeg; then
        echo "Installing FFmpeg..."
        sudo apt-get update && sudo apt-get install -y ffmpeg
    fi
    # gifski check
    if ! command_exists gifski; then
        echo "gifski not found. It is optional but recommended for better GIFs."
        echo "To install gifski on Linux, you typically need Rust/Cargo: 'cargo install gifski'"
    fi
elif [ "$OS_TYPE" == "macos" ]; then
    if ! command_exists ffmpeg; then
        echo "Installing FFmpeg..."
        brew install ffmpeg
    fi
    if ! command_exists gifski; then
        echo "Installing gifski..."
        brew install gifski
    fi
fi

# Ollama Check & Install
if ! command_exists ollama; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✓ Ollama is already installed"
fi

# --- 2. Python Environment ---
echo ""
echo "[2/4] Setting up Python environment..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

echo "Installing/Updating Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# --- 3. Environment Configuration ---
echo ""
echo "[3/4] Configuring environment..."
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: A .env file has been created."
    echo "⚠️  You MUST edit .env and add your OPENAI_API_KEY before running the project."
else
    echo "✓ .env file exists"
fi

# --- 4. Ollama Setup ---
echo ""
echo "[4/4] Setting up AI Models..."

# Check if Ollama server is running
if ! curl -s http://localhost:11434/api/tags >/dev/null; then
    echo "Starting Ollama server in background..."
    ollama serve &
    OLLAMA_PID=$!
    echo "Waiting for Ollama to start..."
    sleep 5
else
    echo "✓ Ollama server is running"
fi

echo "Pulling required model (phi3.5:3.8b)..."
echo "This may take a while depending on your internet connection."
ollama pull phi3.5:3.8b

echo "Most recently used model for generate_with_ollama_cloud is likely not local, skipping pull."

# --- Final Instructions ---
echo ""
echo "====================================="
echo "  🎉 Setup Complete!"
echo "====================================="
echo ""
echo "To run the project:"
echo "1.  Ensure you have added your API keys to the .env file."
echo "2.  Run the following commands:"
echo ""
echo "    source venv/bin/activate"
echo "    python src/main_cli.py"
echo ""