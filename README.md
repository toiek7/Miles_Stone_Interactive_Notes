# Instruction Video to Teaching Document Generator

A complete Python pipeline that converts instructional videos into structured teaching documents with embedded GIF demonstrations.

## Features

- **Video Transcription**: Automatic transcription using Whisper (local or API)
- **AI-Powered Classification**: Segment classification using Ollama
- **Smart Filtering**: Removes irrelevant content and duplicates
- **Semantic Grouping**: Groups related segments using LLM
- **Document Generation**: Creates structured teaching notes using GPT-4
- **Video Processing**: Cuts video into clips and converts to GIFs
- **CV Filtering**: Validates GIF relevance using computer vision
- **HTML Export**: Beautiful, responsive HTML output with embedded media

## Directory Structure

```
.
├── src/
│   ├── main_cli.py                    # Main CLI entry point
│   ├── transcription/
│   │   └── transcribe.py              # Whisper transcription
│   ├── classification/
│   │   └── segment_classifier.py      # Ollama classification
│   ├── filtering/
│   │   └── filter_segments.py         # Segment filtering
│   ├── grouping/
│   │   └── group_segments.py          # Grouping & summarization
│   ├── document_generator/
│   │   ├── generate_document.py       # OpenAI document generation
│   │   └── build_html.py              # HTML builder
│   ├── video_processing/
│   │   ├── cut_video.py               # FFmpeg video cutting
│   │   └── create_gif.py              # GIF conversion
│   ├── cv_filter/
│   │   └── filter_gif.py              # CV-based filtering
│   └── utils/
│       ├── timestamp.py               # Timestamp utilities
│       ├── json_io.py                 # JSON I/O
│       └── logger.py                  # Logging setup
├── data/                              # Place input videos here
├── output/                            # Generated outputs
├── requirements.txt
├── .env.example
└── README.md
```

## Prerequisites

### System Requirements

1. **Python 3.8+**
2. **FFmpeg** - Video processing
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   choco install ffmpeg
   ```

3. **Ollama** - Local LLM inference
   ```bash
   # Install from https://ollama.ai
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull required model
   ollama pull phi3.5:3.8b
   ```

4. **gifski** (optional, for better GIF quality)
   ```bash
   # macOS
   brew install gifski
   
   # Ubuntu/Debian
   cargo install gifski
   ```

### API Keys

- **OpenAI API Key**: Required for document generation and optional for Whisper transcription
- **Anthropic API Key**: Optional, for Claude-based document generation

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd video-to-teaching-doc
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Verify Ollama is running**
   ```bash
   ollama serve
   ```

## Usage

### Basic Usage

1. **Place your video in the `data/` directory**
   ```bash
   cp my_tutorial.mp4 data/
   ```

2. **Run the pipeline**
   ```bash
   python src/main_cli.py
   ```

3. **Follow the prompts**
   - Enter video filename (e.g., `my_tutorial.mp4`)
   - Enter video objective (e.g., "Learn Python basics")

4. **Find your output**
   ```
   output/work_YYYYMMDD_HHMMSS/
   ├── transcript.json         # Raw transcription
   ├── grouped.json           # Grouped segments
   ├── document_raw.md        # Generated markdown
   ├── index.html             # Final HTML document
   ├── clips/                 # Video clips and GIFs
   └── pipeline.log           # Execution log
   ```

### Advanced Usage

#### Using OpenAI Whisper API

Edit `src/main_cli.py` to use the API version:

```python
from transcription.transcribe import transcribe_with_openai_api

transcript_data = transcribe_with_openai_api(str(video_path), work_id, output_dir)
```

#### Customizing Classification Labels

Edit `src/classification/segment_classifier.py`:

```python
CLASSIFICATION_LABELS = [
    "introduction",
    "explanation",
    "demonstration",
    # Add your custom labels
]
```

#### Using Claude for Document Generation

Edit `src/main_cli.py`:

```python
from document_generator.generate_document import generate_with_claude

document_path = generate_with_claude(grouped_data, video_objective, output_dir, logger)
```

#### Enabling Vision-Based GIF Filtering

Edit `src/main_cli.py`:

```python
relevant_gifs = filter_gifs_by_relevance(clips_dir, grouped_data, logger, use_vision_model=True)
```

Note: Requires Ollama with LLaVA model:
```bash
ollama pull llava
```

## Pipeline Stages

### 1. Transcription
- Uses Whisper to transcribe audio to text
- Generates timestamped segments
- Outputs: `transcript.json`

### 2. Classification
- Classifies each segment using Ollama
- Labels: introduction, explanation, demonstration, code_example, tip, warning, etc.

### 3. Filtering
- Removes irrelevant segments (greetings, noise, fillers)
- Eliminates duplicates
- Filters by content quality

### 4. Grouping & Summarization
- Groups semantically related segments
- Generates summaries using Ollama
- Outputs: `grouped.json`

### 5. Document Generation
- Uses GPT-4 to create structured teaching notes
- Markdown format with proper formatting
- Outputs: `document_raw.md`

### 6. Video Processing
- Cuts video into clips based on groups
- Converts clips to GIFs
- Outputs: `clips/clip_*.mp4` and `clips/clip_*.gif`

### 7. CV Filtering
- Validates GIF relevance using computer vision
- Checks visual quality
- Optional: Uses vision models for content matching

### 8. HTML Generation
- Creates responsive HTML document
- Embeds GIFs into sections
- Professional styling
- Outputs: `index.html`

## Configuration

### Whisper Model Size
In `src/transcription/transcribe.py`:
- `tiny`: Fastest, least accurate
- `base`: Default, good balance
- `small`: Better accuracy
- `medium`: High accuracy
- `large`: Best accuracy, slowest

### Ollama Model
In `src/classification/segment_classifier.py` and `src/grouping/group_segments.py`:
- `phi3.5:3.8b`: Default
- `llama2`: Alternative
- `mistral`: Faster alternative

### GIF Settings
In `src/video_processing/create_gif.py`:
- `fps`: Frame rate (default: 10)
- `width`: Output width (default: 480)
- `quality`: Quality setting (default: 90)

## Troubleshooting

### "Ollama connection failed"
- Ensure Ollama is running: `ollama serve`
- Check port 11434 is accessible

### "FFmpeg not found"
- Install FFmpeg (see Prerequisites)
- Add to PATH

### "OpenAI API error"
- Verify API key in `.env`
- Check API quota/billing

### "Out of memory"
- Use smaller Whisper model
- Process shorter videos
- Reduce GIF quality/size

### "GIF creation failed"
- Install gifski for better results
- Falls back to FFmpeg automatically

## Performance Tips

1. **GPU Acceleration**: Install CUDA for faster Whisper transcription
2. **Batch Processing**: Modify code to process multiple videos
3. **Parallel Processing**: Use multiprocessing for GIF creation
4. **Model Selection**: Balance speed vs accuracy for your use case

## Output Examples

### transcript.json
```json
{
  "work_id": "20241207_143022",
  "video_path": "data/tutorial.mp4",
  "segments": [
    {
      "start": "0:00:00",
      "end": "0:00:06",
      "text": "Welcome to this Python tutorial"
    }
  ]
}
```

### grouped.json
```json
[
  {
    "group_id": 0,
    "group_start_time": "0:00:00",
    "group_end_time": "0:01:30",
    "group_summary": "Introduction to Python basics and setup",
    "group_segments": [...]
  }
]
```

### index.html
Beautiful, responsive HTML with:
- Structured sections
- Embedded GIFs
- Timestamps
- Professional styling

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## Acknowledgments

- OpenAI Whisper for transcription
- Ollama for local LLM inference
- FFmpeg for video processing
- gifski for high-quality GIFs
