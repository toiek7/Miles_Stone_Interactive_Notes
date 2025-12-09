"""
Logging utilities
"""

import logging
import sys
from pathlib import Path


def setup_logger(log_file=None, level=logging.INFO):
    """
    Setup application logger with console and file output
    
    Args:
        log_file: Path to log file (optional)
        level: Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger('video_to_doc')
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file provided)
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger():
    """
    Get the application logger
    
    Returns:
        logging.Logger: Application logger
    """
    return logging.getLogger('video_to_doc')