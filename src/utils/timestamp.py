"""
Timestamp utilities for work ID generation and time formatting
"""

from datetime import datetime


def generate_work_id():
    """
    Generate a unique work ID based on current timestamp
    
    Returns:
        str: Work ID in format YYYYMMDD_HHMMSS
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def seconds_to_timestamp(seconds):
    """
    Convert seconds to H:MM:SS format
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted timestamp
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    return f"{hours}:{minutes:02d}:{secs:02d}"


def timestamp_to_seconds(timestamp):
    """
    Convert H:MM:SS or MM:SS timestamp to seconds
    
    Args:
        timestamp (str): Timestamp string
        
    Returns:
        float: Time in seconds
    """
    parts = timestamp.split(':')
    
    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid timestamp format: {timestamp}")


def format_duration(seconds):
    """
    Format duration in a human-readable way
    
    Args:
        seconds (float): Duration in seconds
        
    Returns:
        str: Human-readable duration
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"
    
