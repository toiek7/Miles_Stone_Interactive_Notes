"""
Segment filtering module
"""

import re
import string


# Labels to filter out
IRRELEVANT_LABELS = {
    'greeting',
    'farewell',
    'noise',
    'filler',
    'off_topic'
}


def normalize_text(text):
    """
    Normalize text for duplicate detection
    
    Args:
        text: Text to normalize
        
    Returns:
        str: Normalized text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def is_duplicate(segment, seen_texts, threshold=0.9):
    """
    Check if segment is duplicate based on normalized text
    
    Args:
        segment: Segment dictionary
        seen_texts: Set of already seen normalized texts
        threshold: Similarity threshold (not implemented, exact match for now)
        
    Returns:
        bool: True if duplicate
    """
    normalized = normalize_text(segment.get('text', ''))
    
    if not normalized:
        return True
    
    if normalized in seen_texts:
        return True
    
    seen_texts.add(normalized)
    return False


def filter_segments(segments, logger=None):
    """
    Filter out irrelevant and duplicate segments
    
    Args:
        segments: List of classified segments
        logger: Logger instance
        
    Returns:
        list: Filtered segments
    """
    if logger:
        logger.info(f"Filtering {len(segments)} segments")
    
    filtered = []
    seen_texts = set()
    
    stats = {
        'total': len(segments),
        'irrelevant_label': 0,
        'duplicate': 0,
        'empty': 0,
        'kept': 0
    }
    
    for segment in segments:
        text = segment.get('text', '').strip()
        label = segment.get('label', '').lower()
        
        # Filter empty
        if not text:
            stats['empty'] += 1
            if logger:
                logger.debug(f"Filtered (empty): {segment}")
            continue
        
        # Filter irrelevant labels
        if label in IRRELEVANT_LABELS:
            stats['irrelevant_label'] += 1
            if logger:
                logger.debug(f"Filtered ({label}): {text[:50]}...")
            continue
        
        # Filter duplicates
        if is_duplicate(segment, seen_texts):
            stats['duplicate'] += 1
            if logger:
                logger.debug(f"Filtered (duplicate): {text[:50]}...")
            continue
        
        # Keep segment
        filtered.append(segment)
        stats['kept'] += 1
    
    if logger:
        logger.info("Filtering summary:")
        logger.info(f"  Total segments: {stats['total']}")
        logger.info(f"  Irrelevant labels: {stats['irrelevant_label']}")
        logger.info(f"  Duplicates: {stats['duplicate']}")
        logger.info(f"  Empty: {stats['empty']}")
        logger.info(f"  Kept: {stats['kept']}")
        logger.info(f"  Reduction: {100 * (1 - stats['kept'] / stats['total']):.1f}%")
    
    return filtered


def filter_by_length(segments, min_words=3, max_words=500):
    """
    Additional filter by segment length
    
    Args:
        segments: List of segments
        min_words: Minimum word count
        max_words: Maximum word count
        
    Returns:
        list: Filtered segments
    """
    filtered = []
    
    for segment in segments:
        text = segment.get('text', '')
        word_count = len(text.split())
        
        if min_words <= word_count <= max_words:
            filtered.append(segment)
    
    return filtered


def filter_by_keywords(segments, required_keywords=None, excluded_keywords=None):
    """
    Filter segments by keyword presence
    
    Args:
        segments: List of segments
        required_keywords: List of keywords that must be present (any)
        excluded_keywords: List of keywords that must NOT be present
        
    Returns:
        list: Filtered segments
    """
    filtered = []
    
    for segment in segments:
        text = segment.get('text', '').lower()
        
        # Check excluded keywords
        if excluded_keywords:
            if any(keyword.lower() in text for keyword in excluded_keywords):
                continue
        
        # Check required keywords
        if required_keywords:
            if not any(keyword.lower() in text for keyword in required_keywords):
                continue
        
        filtered.append(segment)
    
    return filtered

