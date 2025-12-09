"""
Grouping and summarization module using Ollama with LLM-based grouping
"""

import json
import requests
import sys
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.json_io import save_json
from utils.timestamp import timestamp_to_seconds, seconds_to_timestamp


def check_segment_belongs_to_group(group_segments, next_segment, model="phi3.5:3.8b"):
    """
    Use LLM to check if next segment belongs to current group
    
    Args:
        group_segments: List of segments in current group
        next_segment: Next segment to check
        model: Ollama model to use
        
    Returns:
        bool: True if segment belongs to group, False otherwise
    """
    # Combine current group texts
    group_texts = '\n'.join([f"- {seg['text']}" for seg in group_segments])
    
    prompt = f"""You are analyzing transcript segments. Decide if the next segment belongs to the same topic as the current group.

Current group:
{group_texts}

Next segment:
{next_segment['text']}

Respond with ONLY "YES" or "NO". (No explanations)"""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.1,
                    'num_predict': 10
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['response'].strip().upper()
            # Check if response contains YES
            return 'YES' in answer
        else:
            # Default to YES if API fails to avoid breaking groups unnecessarily
            return True
            
    except Exception as e:
        print(f"Warning: Group check failed: {e}")
        return True


def summarize_group(segments, video_objective, model="phi3.5:3.8b"):
    """
    Generate summary for a completed group of segments
    
    Args:
        segments: List of segment dictionaries in the group
        video_objective: Video learning objective
        model: Ollama model to use
        
    Returns:
        str: Summary text (max 300 words)
    """
    # Skip summarization when only one segment in the group
    if len(segments) == 1:
        return segments[0]['text']
    
    # Combine segment texts
    combined_text = '\n'.join([f"[{seg['start']} - {seg['end']}] {seg['text']}" for seg in segments])
    
    prompt = f"""You are summarizing a section of an instructional video.

Video objective: {video_objective}

Section transcript:
{combined_text}

Summarize what this group of segments is about. Focus on the main topic, key concepts, and learning points.
Keep your summary under 300 words.

Summary:"""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.3,
                    'num_predict': 500
                }
            },
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result['response'].strip()
            return summary
        else:
            return "Summary generation failed."
            
    except Exception as e:
        print(f"Warning: Summary generation failed: {e}")
        return f"Section covering: {combined_text[:100]}..."


def group_segments_with_llm(segments, video_objective, model="phi3.5:3.8b", max_segments_per_group=15):
    """
    Group segments using LLM to check topic similarity sequentially
    
    Args:
        segments: List of filtered segments
        video_objective: Video learning objective
        model: Ollama model to use
        max_segments_per_group: Maximum segments per group (safety limit)
        
    Returns:
        list: List of groups with summaries
    """
    if not segments:
        return []
    
    grouped_data = []
    current_group = [segments[0]]  # Start with first segment
    group_id = 0
    
    print(f"Grouping {len(segments)} segments using LLM...")
    
    for i in tqdm(range(1, len(segments)), desc="Processing segments"):
        next_segment = segments[i]
        
        # Check if we should force a new group (safety limit)
        if len(current_group) >= max_segments_per_group:
            # Summarize and save current group
            summary = summarize_group(current_group, video_objective, model)
            grouped_data.append({
                'group_id': group_id,
                'group_start_time': current_group[0]['start'],
                'group_end_time': current_group[-1]['end'],
                'group_summary': summary,
                'group_segments': current_group
            })
            
            # Start new group
            current_group = [next_segment]
            group_id += 1
            continue
        
        # Ask LLM if next segment belongs to current group
        belongs = check_segment_belongs_to_group(current_group, next_segment, model)
        
        if belongs:
            # Add to current group
            current_group.append(next_segment)
        else:
            # Summarize and save current group
            summary = summarize_group(current_group, video_objective, model)
            grouped_data.append({
                'group_id': group_id,
                'group_start_time': current_group[0]['start'],
                'group_end_time': current_group[-1]['end'],
                'group_summary': summary,
                'group_segments': current_group
            })
            
            # Start new group with current segment
            current_group = [next_segment]
            group_id += 1
    
    # Don't forget the last group
    if current_group:
        summary = summarize_group(current_group, video_objective, model)
        grouped_data.append({
            'group_id': group_id,
            'group_start_time': current_group[0]['start'],
            'group_end_time': current_group[-1]['end'],
            'group_summary': summary,
            'group_segments': current_group
        })
    
    return grouped_data


def group_and_summarize(segments, video_objective, output_dir, logger=None, model="phi3.5:3.8b"):
    """
    Main function to group segments and generate summaries using LLM
    
    Args:
        segments: List of filtered segments
        video_objective: Video learning objective
        output_dir: Output directory
        logger: Logger instance
        model: Ollama model to use
        
    Returns:
        list: Grouped data with summaries
    """
    if logger:
        logger.info(f"Grouping {len(segments)} segments using LLM-based approach")
    
    # Group segments using LLM
    grouped_data = group_segments_with_llm(segments, video_objective, model)
    
    if logger:
        logger.info(f"Created {len(grouped_data)} groups")
        for group in grouped_data:
            logger.debug(f"Group {group['group_id']}: {len(group['group_segments'])} segments")
    
    # Save to file
    output_file = Path(output_dir) / 'grouped.json'
    save_json(grouped_data, output_file)
    
    if logger:
        logger.info(f"Grouped data saved to: {output_file}")
    
    return grouped_data


