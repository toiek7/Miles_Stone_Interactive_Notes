"""
Segment classification module using Ollama
"""

import json
import requests
from tqdm import tqdm


CLASSIFICATION_LABELS = [
    "introduction",
    "explanation",
    "demonstration",
    "code_example",
    "tip",
    "warning",
    "summary",
    "transition",
    "greeting",
    "farewell",
    "filler",
    "noise",
    "off_topic"
]


def classify_with_ollama(text, model="phi3.5:3.8b"):
    """
    Classify a text segment using Ollama
    
    Args:
        text: Text to classify
        model: Ollama model to use
        
    Returns:
        str: Classification label
    """
    prompt = f"""Classify the following transcript segment into ONE of these categories:
{', '.join(CLASSIFICATION_LABELS)}

Segment: "{text}"

Respond with ONLY the category name, nothing else."""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.1,
                    'num_predict': 20
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            label = result['response'].strip().lower()
            
            # Normalize label
            label = label.replace('"', '').replace("'", '').strip()
            
            # Validate label
            if label in CLASSIFICATION_LABELS:
                return label
            else:
                # Try to find closest match
                for valid_label in CLASSIFICATION_LABELS:
                    if valid_label in label or label in valid_label:
                        return valid_label
                
                # Default to explanation if can't match
                return "explanation"
        else:
            print(f"Warning: Ollama request failed with status {response.status_code}")
            return "explanation"
            
    except Exception as e:
        print(f"Warning: Classification failed for segment: {e}")
        return "explanation"


def classify_segments(segments, logger=None, model="phi3.5:3.8b", batch_size=1):
    """
    Classify all segments
    
    Args:
        segments: List of segment dictionaries
        logger: Logger instance
        model: Ollama model to use
        batch_size: Number of segments to classify at once (currently only 1 supported)
        
    Returns:
        list: Segments with added 'label' field
    """
    if logger:
        logger.info(f"Classifying {len(segments)} segments using Ollama model: {model}")
    
    classified_segments = []
    
    for segment in tqdm(segments, desc="Classifying segments"):
        text = segment.get('text', '')
        
        if not text.strip():
            label = "noise"
        elif len(text.split()) < 3:
            label = "filler"
        else:
            label = classify_with_ollama(text, model)
        
        segment_copy = segment.copy()
        segment_copy['label'] = label
        classified_segments.append(segment_copy)
        
        if logger:
            logger.debug(f"Segment: '{text[:50]}...' -> {label}")
    
    if logger:
        # Count labels
        label_counts = {}
        for seg in classified_segments:
            label = seg['label']
            label_counts[label] = label_counts.get(label, 0) + 1
        
        logger.info("Classification summary:")
        for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {label}: {count}")
    
    return classified_segments


def classify_batch_with_ollama(segments, model="phi3.5:3.8b"):
    """
    Classify multiple segments in one request (experimental)
    
    Args:
        segments: List of segment dictionaries
        model: Ollama model to use
        
    Returns:
        list: Classification labels
    """
    texts = [seg['text'] for seg in segments]
    
    prompt = f"""Classify each of these transcript segments into ONE of these categories:
{', '.join(CLASSIFICATION_LABELS)}

Segments:
{json.dumps(texts, indent=2)}

Respond with a JSON array of labels in the same order, like: ["label1", "label2", ...]"""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.1
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            labels_text = result['response'].strip()
            
            # Try to parse as JSON
            try:
                labels = json.loads(labels_text)
                if isinstance(labels, list) and len(labels) == len(segments):
                    return [l.lower().strip() for l in labels]
            except:
                pass
        
        # Fallback to individual classification
        return [classify_with_ollama(seg['text'], model) for seg in segments]
        
    except Exception as e:
        print(f"Batch classification failed: {e}")
        return [classify_with_ollama(seg['text'], model) for seg in segments]
    
