"""
GIF creation module using gifski or FFmpeg
"""

import subprocess
import shutil
from pathlib import Path
from tqdm import tqdm


def check_gifski_available():
    """
    Check if gifski is installed
    
    Returns:
        bool: True if gifski is available
    """
    return shutil.which('gifski') is not None


def convert_to_gif_gifski(video_path, output_path, fps=10, width=480, quality=90):
    """
    Convert video to GIF using gifski (high quality)
    
    Args:
        video_path: Path to input video
        output_path: Path to output GIF
        fps: Frames per second
        width: Output width in pixels
        quality: Quality (1-100)
        
    Returns:
        bool: True if successful
    """
    try:
        cmd = [
            'gifski',
            '--fps', str(fps),
            '--width', str(width),
            '--quality', str(quality),
            '--output', str(output_path),
            str(video_path)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"gifski conversion failed: {e}")
        return False


def convert_to_gif_ffmpeg(video_path, output_path, fps=10, width=480):
    """
    Convert video to GIF using FFmpeg (fallback)
    
    Args:
        video_path: Path to input video
        output_path: Path to output GIF
        fps: Frames per second
        width: Output width in pixels
        
    Returns:
        bool: True if successful
    """
    try:
        # Two-pass approach for better quality
        palette_path = str(Path(output_path).parent / 'palette.png')
        
        # Generate palette
        palette_cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', f'fps={fps},scale={width}:-1:flags=lanczos,palettegen',
            '-y',
            palette_path
        ]
        
        result = subprocess.run(
            palette_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            return False
        
        # Generate GIF
        gif_cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-i', palette_path,
            '-lavfi', f'fps={fps},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse',
            '-y',
            str(output_path)
        ]
        
        result = subprocess.run(
            gif_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Clean up palette
        try:
            Path(palette_path).unlink()
        except:
            pass
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"FFmpeg GIF conversion failed: {e}")
        return False


def convert_clip_to_gif(video_path, output_path, fps=10, width=480, logger=None):
    """
    Convert video clip to GIF, trying gifski first, then FFmpeg
    
    Args:
        video_path: Path to input video
        output_path: Path to output GIF
        fps: Frames per second
        width: Output width in pixels
        logger: Logger instance
        
    Returns:
        bool: True if successful
    """
    # Try gifski first (better quality)
    if check_gifski_available():
        if logger:
            logger.debug(f"Converting with gifski: {video_path}")
        success = convert_to_gif_gifski(video_path, output_path, fps, width)
        if success:
            return True
    
    # Fallback to FFmpeg
    if logger:
        logger.debug(f"Converting with FFmpeg: {video_path}")
    return convert_to_gif_ffmpeg(video_path, output_path, fps, width)


def convert_clips_to_gifs(clips_dir, fps=10, width=480, logger=None):
    """
    Convert all video clips in directory to GIFs
    
    Args:
        clips_dir: Directory containing video clips
        fps: Frames per second
        width: Output width in pixels
        logger: Logger instance
        
    Returns:
        list: List of created GIF paths
    """
    clips_dir = Path(clips_dir)
    gifs_output_dir = clips_dir.parent / "gifs"
    
    if not clips_dir.exists():
        if logger:
            logger.error(f"Clips directory not found: {clips_dir}")
        return []
    
    # Find all MP4 clips
    video_clips = sorted(clips_dir.glob('clip_*.mp4'))
    
    if logger:
        logger.info(f"Converting {len(video_clips)} clips to GIFs")
    
    created_gifs = []
    
    for video_path in tqdm(video_clips, desc="Creating GIFs"):

        # Create parallel GIF folder: output/.../gifs/
        gif_output_dir = video_path.parent.parent / "gifs"
        gif_output_dir.mkdir(parents=True, exist_ok=True)

        # Save GIF as output/.../gifs/clip_x.gif
        gif_path = gif_output_dir / (video_path.stem + ".gif")

        success = convert_clip_to_gif(
            video_path,
            gif_path,
            fps=fps,
            width=width,
            logger=logger
        )
        
        if success:
            created_gifs.append(gif_path)
            if logger:
                logger.debug(f"Created GIF: {gif_path}")
        else:
            if logger:
                logger.warning(f"Failed to create GIF: {gif_path}")
    
    if logger:
        logger.info(f"Successfully created {len(created_gifs)} GIFs")
    
    return gifs_output_dir, created_gifs


def optimize_gif(gif_path, logger=None):
    """
    Optimize GIF file size using gifsicle if available
    
    Args:
        gif_path: Path to GIF file
        logger: Logger instance
        
    Returns:
        bool: True if successful
    """
    if not shutil.which('gifsicle'):
        return False
    
    try:
        cmd = [
            'gifsicle',
            '-O3',
            '--colors', '256',
            '-i', str(gif_path),
            '-o', str(gif_path)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0 and logger:
            logger.debug(f"Optimized GIF: {gif_path}")
        
        return result.returncode == 0
        
    except Exception as e:
        if logger:
            logger.warning(f"GIF optimization failed: {e}")
        return False
    
    