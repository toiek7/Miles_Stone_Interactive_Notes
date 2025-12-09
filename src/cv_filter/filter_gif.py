"""
Computer vision filtering module for GIF relevance checking
"""

import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import requests
from tqdm import tqdm


def extract_gif_frames(gif_path, num_frames=5):
    """
    Extract sample frames from GIF
    
    Args:
        gif_path: Path to GIF file
        num_frames: Number of frames to extract
        
    Returns:
        list: List of PIL Images
    """
    try:
        gif = Image.open(gif_path)
        frames = []
        
        frame_count = gif.n_frames
        step = max(1, frame_count // num_frames)
        
        for i in range(0, frame_count, step):
            if len(frames) >= num_frames:
                break
            
            gif.seek(i)
            frames.append(gif.copy().convert('RGB'))
        
        return frames
        
    except Exception as e:
        print(f"Failed to extract frames from {gif_path}: {e}")
        return []


def check_visual_quality(gif_path, min_width=200, min_height=200):
    """
    Check if GIF meets minimum quality standards
    
    Args:
        gif_path: Path to GIF file
        min_width: Minimum width
        min_height: Minimum height
        
    Returns:
        bool: True if meets quality standards
    """
    try:
        gif = Image.open(gif_path)
        width, height = gif.size
        
        # Check dimensions
        if width < min_width or height < min_height:
            return False
        
        # Check if mostly blank/black
        frame = np.array(gif.convert('L'))
        mean_brightness = np.mean(frame)
        
        # Reject very dark images
        if mean_brightness < 10:
            return False
        
        return True
        
    except Exception as e:
        print(f"Quality check failed for {gif_path}: {e}")
        return False


def check_relevance_with_ollama(gif_path, summary, model="llava"):
    """
    Check if GIF content matches group summary using Ollama + LLaVA
    
    Args:
        gif_path: Path to GIF file
        summary: Group summary text
        model: Ollama vision model (llava, bakllava, etc.)
        
    Returns:
        tuple: (bool, str) - (is_relevant, explanation)
    """
    try:
        # Extract a representative frame
        frames = extract_gif_frames(gif_path, num_frames=1)
        if not frames:
            return False, "Could not extract frames"
        
        # Save frame temporarily
        temp_frame = Path(gif_path).parent / 'temp_frame.jpg'
        frames[0].save(temp_frame, 'JPEG')
        
        # Prepare prompt
        prompt = f"""Does this image show content related to: "{summary}"?

Answer with YES or NO, followed by a brief explanation."""

        # Call Ollama with vision model
        # Note: This requires Ollama with a vision model like llava
        with open(temp_frame, 'rb') as f:
            import base64
            image_b64 = base64.b64encode(f.read()).decode()
        
        #####
        # print(f"Sending request to Ollama for GIF {gif_path}...")
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'images': [image_b64],
                'stream': False
            },
            # timeout=60
        )
        
        # Clean up temp file
        temp_frame.unlink()
        
        if response.status_code == 200:
            result = response.json()
            answer = result['response'].strip().lower()
            
            is_relevant = answer.startswith('yes')
            #####
            # print(f"Ollama response for {gif_path}: {answer}")
            return is_relevant, answer
        else:
            #####
            # print(f"Ollama API error: {response.status_code} - {response.text}")
            return True, "API call failed, assuming relevant"
            
    except Exception as e:
        print(f"Relevance check failed: {e}")
        return True, f"Check failed: {e}"


def simple_relevance_check(gif_path, summary):
    """
    Simple heuristic-based relevance check (fallback)
    
    Args:
        gif_path: Path to GIF file
        summary: Group summary text
        
    Returns:
        tuple: (bool, str) - (is_relevant, explanation)
    """
    # For now, just check visual quality
    is_quality = check_visual_quality(gif_path)
    
    if not is_quality:
        return False, "Low visual quality"
    
    # Accept all quality GIFs in simple mode
    return True, "Quality check passed"


def filter_gifs_by_relevance(gifs_dir, grouped_data, logger=None, use_vision_model=False):
    """
    Filter GIFs based on relevance to group summaries
    
    Args:
        gifs_dir: Directory containing GIFs
        grouped_data: List of grouped segments with summaries
        logger: Logger instance
        use_vision_model: Whether to use vision model for checking
        
    Returns:
        dict: Map of group_id to GIF path (only relevant ones)
    """
    gifs_dir = Path(gifs_dir)
    
    if not gifs_dir.exists():
        if logger:
            logger.error(f"Gifs directory not found: {gifs_dir}")
        return {}
    
    relevant_gifs = {}
    
    if logger:
        logger.info(f"Filtering {len(grouped_data)} GIFs for relevance")
    
    for group in tqdm(grouped_data, desc="Filtering GIFs"):
        group_id = group['group_id']
        summary = group['group_summary']
        
        gif_path = gifs_dir / f"clip_{group_id}.gif"
        
        if not gif_path.exists():
            if logger:
                logger.warning(f"GIF not found: {gif_path}")
            continue
        
        # Check relevance
        if use_vision_model:
            #####
            print(f"Checking relevance for GIF {gif_path} using vision model...")
            is_relevant, explanation = check_relevance_with_ollama(gif_path, summary)
        else:
            #####
            print(f"Checking relevance for GIF {gif_path} using simple check...")
            is_relevant, explanation = simple_relevance_check(gif_path, summary)
        
        if logger:
            logger.debug(f"Group {group_id}: {is_relevant} - {explanation}")
        
        if is_relevant:
            relevant_gifs[group_id] = gif_path
    
    if logger:
        logger.info(f"Kept {len(relevant_gifs)} / {len(grouped_data)} GIFs")
    
    return relevant_gifs


def analyze_gif_content(gif_path):
    """
    Analyze GIF content using OpenCV
    
    Args:
        gif_path: Path to GIF file
        
    Returns:
        dict: Analysis results
    """
    try:
        frames = extract_gif_frames(gif_path, num_frames=10)
        
        if not frames:
            return {'valid': False}
        
        # Convert to numpy arrays
        frame_arrays = [np.array(f) for f in frames]
        
        # Calculate metrics
        brightnesses = [np.mean(f) for f in frame_arrays]
        contrasts = [np.std(f) for f in frame_arrays]
        
        # Detect motion (frame differences)
        motion_scores = []
        for i in range(len(frame_arrays) - 1):
            diff = np.abs(frame_arrays[i+1].astype(float) - frame_arrays[i].astype(float))
            motion_scores.append(np.mean(diff))
        
        return {
            'valid': True,
            'num_frames': len(frames),
            'avg_brightness': np.mean(brightnesses),
            'avg_contrast': np.mean(contrasts),
            'avg_motion': np.mean(motion_scores) if motion_scores else 0,
            'has_motion': np.mean(motion_scores) > 5 if motion_scores else False
        }
        
    except Exception as e:
        return {'valid': False, 'error': str(e)}
    
