"""
Teaching document generation using OpenAI
"""

import os
import json
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
from document_generator.create_final_draft import final_json_to_readable_text
from utils.json_io import save_text


def generate_teaching_document(grouped_data, video_objective, output_dir, logger=None):
    """
    Generate teaching document using OpenAI GPT-4
    
    Args:
        grouped_data: List of grouped segments with summaries
        video_objective: Video learning objective
        output_dir: Output directory
        logger: Logger instance
        
    Returns:
        Path: Path to generated document
    """
    if logger:
        logger.info("Generating teaching document with OpenAI")
    
    # Load .env file
    load_dotenv()   # <-- IMPORTANT

    # Initialize OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)
    
    # Prepare JSON structure description
    json_structure = """
    [
      {
        "group_id": 0,
        "group_start_time": "H:MM:SS",
        "group_end_time": "H:MM:SS",
        "group_summary": "Summary of this section",
        "group_segments": [
          {
            "start": "H:MM:SS",
            "end": "H:MM:SS",
            "text": "transcript text",
            "label": "explanation"
          }
        ]
      }
    ]
    """
    
    # Prepare full transcript text
    transcript_text = json.dumps(grouped_data, indent=2)
    
    # Build prompt
    prompt = f"""You are a professional teaching assistant. I have a video transcript in JSON format with timestamps.

JSON Structure:
{json_structure}

Full Transcript:
{transcript_text}

Video Objective: {video_objective}

Your task:
1. Analyze the transcript and identify the main teaching concepts and sections.
2. Create a well-structured teaching document with:
   - Clear numbered sections
   - Group timestamps: [H:MM:SS - H:MM:SS]
   - Subsection timestamps where relevant
   - Bullet points for key concepts
   - Sub-bullets with explanations
   - Clean, professional language
   - Code blocks where relevant (use markdown syntax)

3. Remove filler words and improve clarity.
4. Focus on teaching value and learning outcomes.
5. Use markdown formatting.
6. Make it comprehensive but concise.

Generate the teaching notes now."""

    try:
        if logger:
            logger.info("Sending request to OpenAI API...")
        
        response = client.chat.completions.create(
            model="gpt-5.1",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert teaching assistant who creates clear, structured educational documents from video transcripts."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        # Extract generated document
        document_content = response.choices[0].message.content
        
        # Save to file
        output_file = Path(output_dir) / 'document_raw.md'
        save_text(document_content, output_file)
        
        if logger:
            logger.info(f"Teaching document generated: {output_file}")
            logger.info(f"Document length: {len(document_content)} characters")
        
        return output_file
        
    except Exception as e:
        if logger:
            logger.error(f"Failed to generate document: {e}")
        raise


def generate_with_claude(grouped_data, video_objective, output_dir, logger=None):
    """
    Alternative: Generate teaching document using Anthropic Claude
    
    Args:
        grouped_data: List of grouped segments with summaries
        video_objective: Video learning objective
        output_dir: Output directory
        logger: Logger instance
        
    Returns:
        Path: Path to generated document
    """
    from anthropic import Anthropic
    
    if logger:
        logger.info("Generating teaching document with Claude")
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    client = Anthropic(api_key=api_key)
    
    # Prepare transcript
    transcript_text = json.dumps(grouped_data, indent=2)
    
    prompt = f"""Analyze this video transcript and create a comprehensive teaching document.

Video Objective: {video_objective}

Transcript Data:
{transcript_text}

Create a well-structured markdown document with:
- Clear sections with timestamps [H:MM:SS - H:MM:SS]
- Bullet points for key concepts
- Code examples where relevant
- Professional, clear language
- Focus on learning outcomes"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        document_content = message.content[0].text
        
        output_file = Path(output_dir) / 'document_raw.md'
        save_text(document_content, output_file)
        
        if logger:
            logger.info(f"Teaching document generated: {output_file}")
        
        return output_file
        
    except Exception as e:
        if logger:
            logger.error(f"Failed to generate document: {e}")
        raise


def generate_with_ollama(grouped_data, video_objective, output_dir, logger=None):
    """
    Alternative: Generate teaching document using Ollama (model: deepseek-r1:latest)

    Args:
        grouped_data: List of grouped segments with summaries
        video_objective: Video learning objective
        output_dir: Output directory
        logger: Logger instance
        
    Returns:
        Path: Path to generated document
    """
    import requests

    if logger:
        logger.info("Generating teaching document with Ollama (deepseek-r1:latest)")

    # Prepare JSON structure description (same as OpenAI version)
    json_structure = """
    [
      {
        "group_id": 0,
        "group_start_time": "H:MM:SS",
        "group_end_time": "H:MM:SS",
        "group_summary": "Summary of this section",
        "group_segments": [
          {
            "start": "H:MM:SS",
            "end": "H:MM:SS",
            "text": "transcript text",
            "label": "explanation"
          }
        ]
      }
    ]
    """

    # Prepare transcript
    transcript_text = json.dumps(grouped_data, indent=2)

    # Build full prompt (same as OpenAI version)
    prompt = f"""You are a professional teaching assistant. I have a video transcript in JSON format with timestamps.

JSON Structure:
{json_structure}

Full Transcript:
{transcript_text}

Video Objective: {video_objective}

Your task:
1. Analyze the transcript and identify the main teaching concepts and sections.
2. Create a well-structured teaching document with:
   - Clear numbered sections
   - Group timestamps: [H:MM:SS - H:MM:SS]
   - Subsection timestamps where relevant
   - Bullet points for key concepts
   - Sub-bullets with explanations
   - Clean, professional language
   - Code blocks where relevant (use markdown syntax)

3. Remove filler words and improve clarity.
4. Focus on teaching value and learning outcomes.
5. Use markdown formatting.
6. Make it comprehensive but concise.

Generate the teaching notes now."""

    # → Ollama API endpoint
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "deepseek-r1:latest",
        "prompt": prompt,
        "temperature": 0.3,
        "num_predict": 4000   # similar to max_tokens
    }

    try:
        if logger:
            logger.info("Sending request to Ollama...")

        response = requests.post(url, json=payload, stream=True)

        if response.status_code != 200:
            raise RuntimeError(f"Ollama generation failed: {response.text}")

        # DeepSeek returns streaming JSON chunks: we must concatenate `.response`
        document_content = ""

        for line in response.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                document_content += data["response"]

        # Save output
        output_file = Path(output_dir) / "document_raw.md"
        save_text(document_content, output_file)

        if logger:
            logger.info(f"Teaching document generated with Ollama: {output_file}")
            logger.info(f"Document length: {len(document_content)} characters")

        return output_file

    except Exception as e:
        if logger:
            logger.error(f"Failed to generate document using Ollama: {e}")
        raise


def generate_with_ollama_cloud(grouped_data, video_objective, output_dir, logger=None):
    """
    Alternative: Generate teaching document using Ollama Cloud (model: gpt-oss:120b-cloud)

    Args:
        grouped_data: List of grouped segments with summaries
        video_objective: Video learning objective
        output_dir: Output directory
        logger: Logger instance
        
    Returns:
        Path: Path to generated document
    """
    from ollama import Client

    # Initialize Ollama Cloud client
    client = Client()

    if logger:
        logger.info("Generating teaching document with Ollama Cloud (gpt-oss:120b-cloud)")

    # Convert Grouped JSON to Readable Text
    content_from_json = final_json_to_readable_text(grouped_data)

    # Build full prompt (same as OpenAI version)
    prompt = f"""
You are a professional teaching assistant. You will generate a structured teaching document based on segmented video transcript data.

Objective of this teaching note: {video_objective}

Below is the processed transcript content extracted from JSON:
{content_from_json}

Each section contains:
- group_id
- gif_relate (“Yes” or “No”)
- Combined transcript text from all segments in that group

==============================
IMPORTANT RULES AND OUTPUT FORMAT
==============================

1. SECTION STRUCTURE
For each group, create a clearly labeled section:

## Section {{group_num}}: <Descriptive Title>
(Choose a meaningful, academic title based on the text content.)

2. GIF HANDLING
- If gif_relate = "Yes":
    Insert a GIF placeholder immediately below the section title:
    {{GIF:<group_id>}}
- If gif_relate = "No":
    Do not include a placeholder.

3. CONTENT REQUIREMENTS
For each section, include:
- A concise introductory paragraph explaining the concept
- A “Key Concepts” bullet list with 3–6 well-structured points
- A concise deeper explanation (2–4 short paragraphs)
- Code blocks when appropriate (using ``` syntax)

4. WRITING STYLE
- Clear, professional, instructional tone
- Focus on educational clarity
- Remove filler text; improve grammar
- Use Markdown formatting consistently
- Ensure logical flow between sections

5. WHAT NOT TO DO
- Do not repeat the raw transcript word-for-word
- Do not invent content unrelated to the provided text
- Do not mention JSON or data structure
- Do not skip sections

==============================
EXAMPLE SNIPPET (REFERENCE)
==============================

## Section 1: Introduction to Machine Learning
{{GIF:0}}

Machine Learning enables computers to learn from data without being explicitly programmed.

### Key Concepts
- **Definition:** Systems improve with experience
- **Origin:** Term coined by Arthur Samuel in 1959
- **Applications:** Predictive models in modern software

(Continue with deeper explanation...)

==============================

Now generate the complete, polished **Markdown teaching document**, following all rules and using all sections from the transcript above.
"""


    try:
        if logger:
            logger.info("Sending request to Ollama Cloud...")

        # Call Ollama Clolud Chat
        response = client.chat(
            model='gpt-oss:120b-cloud',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
            options={
                'temperature': 0.3,
                'num_predict': 4000
            },
        )

        # Extract generated document
        document_content = response['message']['content']

        # Save output
        output_file = Path(output_dir) / "document_raw.md"
        save_text(document_content, output_file)

        if logger:
            logger.info(f"Teaching document generated with Ollama Cloud: {output_file}")
            logger.info(f"Document length: {len(document_content)} characters")

        return output_file

    except Exception as e:
        if logger:
            logger.error(f"Failed to generate document using Ollama Cloud: {e}")
        raise

