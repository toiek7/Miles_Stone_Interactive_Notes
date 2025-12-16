# Instruction Video to Teaching Document Generator

A production-ready Python application that transforms instructional videos into structured, interactive teaching documents with embedded GIF demonstrations.

## 📋 Project Overview

This tool automates the process of converting video content into written tutorials. It uses a sophisticated pipeline of AI models and video processing tools to:

1.  **Transcribe** audio using Whisper.
2.  **Classify** video segments using local LLMs (Ollama).
3.  **Filter** out irrelevant content (greetings, fillers).
4.  **Group** related segments into logical steps.
5.  **Generate** a professional Markdown document using GPT-4.
6.  **Create** optimized GIFs for demonstrations to embed in the document.

## ✅ Prerequisites

Before running the project, ensure you have:
*   **Operating System**: Linux (Ubuntu/Debian) or macOS. (Windows users should use WSL2).
*   **Python 3.8+**
*   **Sudo Privileges**: The setup script may ask for your password to install system dependencies (ffmpeg, etc).

## 🚀 Easy Installation

We provide a fully automated setup script that handles:
*   Installing system dependencies (FFmpeg, Ollama).
*   Setting up the Python virtual environment.
*   Installing AI models.
*   Configuring the project environment.

1.  **Run the setup script**:
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

    > **Note**: This will install Ollama and download the required AI model (`phi3.5:3.8b`). It may take a few minutes depending on your internet connection.

2.  **Add API Keys**:
    The script creates a `.env` file. Open it and add your **OpenAI API Key**:
    ```bash
    nano .env
    # Set OPENAI_API_KEY=your_key_here
    ```

## 🏃 How to Run

Once setup is complete, you can run the project immediately:

1.  **Prepare your video**: Place your MP4 video file in the `data/` directory.

2.  **Run the CLI**:
    ```bash
    source venv/bin/activate
    python src/main_cli.py
    ```

3.  **Follow the prompts**: The CLI will guide you through the process.

## 📂 Output

The results will be generated in the `output/` directory, organized by timestamp:
```
output/work_YYYYMMDD_HHMMSS/
├── index.html          # Final interactive teaching document
├── document_raw.md     # Raw Markdown content
├── clips/              # Extracted video clips and GIFs
├── transcript.json     # Raw transcription data
└── pipeline.log        # Process execution log
```

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| **Setup Fails** | Ensure you have internet access and sudo privileges. Check the logs for specific error messages. |
| **Ollama Error** | Ensure Ollama server is running (`ollama serve`). The setup script tries to start it, but you may need to run it manually if it fails. |
| **OpenAI API Errors** | Check that `OPENAI_API_KEY` is set correctly in `.env` and has credits. |
| **Permission Denied** | Run `chmod +x setup.sh` to make the script executable. |

## 📚 Documentation
For deeper architectural details, file structure, and advanced configuration, please refer to the [project.md](project.md) file.
