"""
JSON input/output utilities
"""

import json
from pathlib import Path


def save_json(data, filepath, indent=2):
    """
    Save data to JSON file
    
    Args:
        data: Data to save (dict, list, etc.)
        filepath: Path to save file
        indent: JSON indentation level
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_json(filepath):
    """
    Load data from JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Loaded data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_text(text, filepath):
    """
    Save text to file
    
    Args:
        text: Text content to save
        filepath: Path to save file
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)


def load_text(filepath):
    """
    Load text from file
    
    Args:
        filepath: Path to text file
        
    Returns:
        str: File content
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()