"""
Video cutting module using FFmpeg
"""

import subprocess
import sys
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.timestamp import timestamp_to_seconds


def cut_video_clip(input_video, start_time, end_time, output_path, logger=None):
    """
    Cut a video clip using FFmpeg
    
    Args:
        input_video: Path to input video
        start_time: Start timestamp (H:MM:SS)
        end_time: End timestamp (H:MM:SS)
        output_path: Output clip path
        logger: Logger instance
        
    Returns:
        bool: True if successful
    """
    try:
        # Convert timestamps to seconds for FFmpeg
        start_sec = timestamp_to_seconds(start_time)
        end_sec = timestamp_to_seconds(end_time)
        duration = end_sec - start_sec
        
        if duration <= 0:
            if logger:
                logger.warning(f"Invalid duration for clip: {start_time} to {end_time}")
            return False
        
        # Build FFmpeg command
        cmd = [
            'ffmpeg',
            '-i', input_video,
            '-ss', str(start_sec),
            '-t', str(duration),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', 'fast',
            '-crf', '23',
            '-y',  # Overwrite output
            output_path
        ]
        
        # Run FFmpeg
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            if logger:
                logger.debug(f"Created clip: {output_path}")
            return True
        else:
            if logger:
                logger.error(f"FFmpeg failed: {result.stderr}")
            return False
            
    except Exception as e:
        if logger:
            logger.error(f"Failed to cut clip: {e}")
        return False


def cut_video_clips(input_video, grouped_data, output_dir, logger=None):
    """
    Cut video into clips based on grouped segments
    
    Args:
        input_video: Path to input video
        grouped_data: List of grouped segments
        output_dir: Output directory
        logger: Logger instance
        
    Returns:
        Path: Path to clips directory
    """
    if logger:
        logger.info(f"Cutting video into {len(grouped_data)} clips")
    
    # Create clips directory
    clips_dir = Path(output_dir) / 'clips'
    clips_dir.mkdir(parents=True, exist_ok=True)
    
    successful_clips = []
    
    for group in tqdm(grouped_data, desc="Cutting video clips"):
        group_id = group['group_id']
        start_time = group['group_start_time']
        end_time = group['group_end_time']
        
        output_path = clips_dir / f"clip_{group_id}.mp4"
        
        success = cut_video_clip(
            input_video,
            start_time,
            end_time,
            str(output_path),
            logger
        )
        
        if success:
            successful_clips.append(output_path)
    
    if logger:
        logger.info(f"Successfully created {len(successful_clips)} clips")
        logger.info(f"Clips saved to: {clips_dir}")
    
    return clips_dir


def extract_keyframe(video_path, timestamp, output_path, logger=None):
    """
    Extract a single keyframe from video at specific timestamp
    
    Args:
        video_path: Path to video
        timestamp: Timestamp (H:MM:SS)
        output_path: Output image path
        logger: Logger instance
        
    Returns:
        bool: True if successful
    """
    try:
        seconds = timestamp_to_seconds(timestamp)
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', str(seconds),
            '-frames:v', '1',
            '-q:v', '2',
            '-y',
            output_path
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return result.returncode == 0
        
    except Exception as e:
        if logger:
            logger.error(f"Failed to extract keyframe: {e}")
        return False


def get_video_info(video_path):
    """
    Get video metadata using FFprobe
    
    Args:
        video_path: Path to video
        
    Returns:
        dict: Video metadata
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            import json
            return json.loads(result.stdout)
        else:
            return {}
            
    except Exception as e:
        print(f"Failed to get video info: {e}")
        return {}