"""
Video transcription module using Whisper
"""

import os
import sys
from pathlib import Path
import whisper
import torch

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.timestamp import seconds_to_timestamp
from utils.json_io import save_json


def get_video_duration(video_path):
    """
    Get video duration using ffprobe
    
    Args:
        video_path: Path to video file
        
    Returns:
        float: Duration in seconds
    """
    import subprocess
    
    try:
        result = subprocess.run(
            [
                'ffprobe', '-v', 'error', '-show_entries',
                'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Warning: Could not determine video duration: {e}")
        return 0


def transcribe_video(video_path, work_id, output_dir, model_name="base"):
    """
    Transcribe video using Whisper
    
    Args:
        video_path: Path to video file
        work_id: Unique work identifier
        output_dir: Output directory
        model_name: Whisper model size (tiny, base, small, medium, large)
        
    Returns:
        dict: Transcription data with segments
    """
    print(f"Loading Whisper model '{model_name}'...")
    
    # Check for CUDA
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load model
    model = whisper.load_model(model_name, device=device)
    
    print(f"Transcribing video: {video_path}")
    result = model.transcribe(
        video_path,
        verbose=True,
        word_timestamps=False
    )
    
    # Get video duration
    duration = get_video_duration(video_path)
    
    # Format segments
    segments = []
    for segment in result['segments']:
        segments.append({
            'start': seconds_to_timestamp(segment['start']),
            'end': seconds_to_timestamp(segment['end']),
            'text': segment['text'].strip()
        })
    
    # Build transcript data
    transcript_data = {
        'work_id': work_id,
        'video_path': video_path,
        'model': model_name,
        'duration': duration,
        'language': result.get('language', 'en'),
        'segments': segments
    }
    
    # Save to file
    output_file = Path(output_dir) / 'transcript.json'
    save_json(transcript_data, output_file)
    
    print(f"Transcription saved to: {output_file}")
    print(f"Total segments: {len(segments)}")
    
    return transcript_data


def transcribe_with_openai_api(video_path, work_id, output_dir):
    """
    Alternative: Transcribe using OpenAI Whisper API
    Requires OPENAI_API_KEY environment variable
    
    Args:
        video_path: Path to video file
        work_id: Unique work identifier
        output_dir: Output directory
        
    Returns:
        dict: Transcription data with segments
    """
    from openai import OpenAI
    
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print(f"Transcribing video with OpenAI API: {video_path}")
    
    with open(video_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
    
    # Get video duration
    duration = get_video_duration(video_path)
    
    # Format segments
    segments = []
    if hasattr(transcript, 'segments'):
        for segment in transcript.segments:
            segments.append({
                'start': seconds_to_timestamp(segment['start']),
                'end': seconds_to_timestamp(segment['end']),
                'text': segment['text'].strip()
            })
    else:
        # Fallback: single segment
        segments.append({
            'start': '0:00:00',
            'end': seconds_to_timestamp(duration),
            'text': transcript.text
        })
    
    # Build transcript data
    transcript_data = {
        'work_id': work_id,
        'video_path': video_path,
        'model': 'whisper-1',
        'duration': duration,
        'language': getattr(transcript, 'language', 'en'),
        'segments': segments
    }
    
    # Save to file
    output_file = Path(output_dir) / 'transcript.json'
    save_json(transcript_data, output_file)
    
    print(f"Transcription saved to: {output_file}")
    
    return transcript_data

