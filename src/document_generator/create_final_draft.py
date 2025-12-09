"""
Final draft JSON creation module
Combines grouped data with GIF paths and relevance information
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.json_io import save_json


def create_final_draft_json(grouped_data, relevant_gifs, clips_dir, output_dir, logger=None):
    """
    Create final draft JSON with GIF paths and relevance information
    
    Args:
        grouped_data: List of grouped segments with summaries
        relevant_gifs: Dict mapping group_id to GIF path (only relevant ones)
        clips_dir: Directory containing clips and GIFs
        output_dir: Output directory for final_draft.json
        logger: Logger instance
        
    Returns:
        Path: Path to final_draft.json
    """
    if logger:
        logger.info("Creating final draft JSON with GIF information")
    
    clips_dir = Path(clips_dir)
    final_draft = []
    
    for group in grouped_data:
        group_id = group['group_id']
        
        # Get GIF path for this group
        gif_path = clips_dir / f"clip_{group_id}.gif"
        
        # Check if GIF exists and is relevant
        gif_exists = gif_path.exists()
        gif_is_relevant = group_id in relevant_gifs
        
        # Determine gif_relate status
        if not gif_exists:
            gif_relate = "No (GIF not found)"
            relative_gif_path = None
        elif gif_is_relevant:
            gif_relate = "Yes"
            # Use relative path for portability
            relative_gif_path = f"clips/clip_{group_id}.gif"
        else:
            gif_relate = "No"
            relative_gif_path = f"clips/clip_{group_id}.gif"
        
        # Build group segments list with segment_id
        group_segments = []
        for idx, segment in enumerate(group.get('group_segments', [])):
            group_segments.append({
                'segment_id': idx,
                'text': segment.get('text', '').strip()
            })
        
        # Build final draft entry
        draft_entry = {
            'group_id': group_id,
            'group_start_time': group['group_start_time'],
            'group_end_time': group['group_end_time'],
            'group_summary': group['group_summary'],
            'gif_path': relative_gif_path,
            'gif_relate': gif_relate,
            'group_segments': group_segments
        }
        
        final_draft.append(draft_entry)
        
        if logger:
            logger.debug(f"Group {group_id}: GIF exists={gif_exists}, relevant={gif_is_relevant}, status='{gif_relate}'")
    
    # Save final draft JSON
    output_file = Path(output_dir) / 'final_draft.json'
    save_json(final_draft, output_file)
    
    if logger:
        # Count statistics
        total_groups = len(final_draft)
        gifs_yes = sum(1 for entry in final_draft if entry['gif_relate'] == "Yes")
        gifs_no = sum(1 for entry in final_draft if entry['gif_relate'] == "No")
        gifs_missing = sum(1 for entry in final_draft if "not found" in entry['gif_relate'])
        
        logger.info(f"Final draft JSON created: {output_file}")
        logger.info(f"Statistics:")
        logger.info(f"  Total groups: {total_groups}")
        logger.info(f"  GIFs included (Yes): {gifs_yes}")
        logger.info(f"  GIFs excluded (No): {gifs_no}")
        logger.info(f"  GIFs missing: {gifs_missing}")
    
    return output_file


def final_json_to_readable_text(grouped_data):
    """
    Convert grouped JSON data into a clean readable text format.

    Args:
        grouped_data (list): List of grouped segment dictionaries

    Returns:
        str: Formatted text
    """
    output_lines = []

    for group in grouped_data:
        group_id = group.get("group_id")
        gif_relate = group.get("gif_relate", "Unknown")

        # Combine all text from the group_segments
        combined_text = " ".join(
            seg.get("text", "").strip() for seg in group.get("group_segments", [])
        )

        # Build section block
        section_text = (
            f"Section-{group_id + 1} (group_id: {group_id})\n"
            f"gif_relate: {gif_relate}\n"
            f"Text: {combined_text}\n"
        )

        output_lines.append(section_text)

    return "\n".join(output_lines)



def create_final_draft_with_enhanced_info(grouped_data, relevant_gifs, clips_dir, output_dir, logger=None):
    """
    Create final draft JSON with enhanced GIF information including analysis
    
    Args:
        grouped_data: List of grouped segments with summaries
        relevant_gifs: Dict mapping group_id to GIF path (only relevant ones)
        clips_dir: Directory containing clips and GIFs
        output_dir: Output directory for final_draft.json
        logger: Logger instance
        
    Returns:
        Path: Path to final_draft.json
    """
    if logger:
        logger.info("Creating enhanced final draft JSON with GIF analysis")
    
    clips_dir = Path(clips_dir)
    final_draft = []
    
    # Import GIF analysis function
    try:
        from cv_filter.filter_gif import analyze_gif_content
        has_analysis = True
    except ImportError:
        has_analysis = False
        if logger:
            logger.warning("GIF analysis not available, creating basic final draft")
    
    for group in grouped_data:
        group_id = group['group_id']
        
        # Get GIF path for this group
        gif_path = clips_dir / f"clip_{group_id}.gif"
        
        # Check if GIF exists and is relevant
        gif_exists = gif_path.exists()
        gif_is_relevant = group_id in relevant_gifs
        
        # Analyze GIF if available
        gif_analysis = None
        if gif_exists and has_analysis:
            gif_analysis = analyze_gif_content(str(gif_path))
        
        # Determine gif_relate status with reason
        if not gif_exists:
            gif_relate = "No"
            gif_reason = "GIF file not found"
            relative_gif_path = None
        elif gif_is_relevant:
            gif_relate = "Yes"
            gif_reason = "GIF is relevant to content"
            relative_gif_path = f"clips/clip_{group_id}.gif"
        else:
            gif_relate = "No"
            gif_reason = "GIF failed relevance check"
            relative_gif_path = f"clips/clip_{group_id}.gif"
        
        # Build group segments list with segment_id and timestamps
        group_segments = []
        for idx, segment in enumerate(group.get('group_segments', [])):
            segment_entry = {
                'segment_id': idx,
                'text': segment.get('text', '').strip()
            }
            
            # Add timestamps if available
            if 'start' in segment:
                segment_entry['start'] = segment['start']
            if 'end' in segment:
                segment_entry['end'] = segment['end']
            
            group_segments.append(segment_entry)
        
        # Build final draft entry
        draft_entry = {
            'group_id': group_id,
            'group_start_time': group['group_start_time'],
            'group_end_time': group['group_end_time'],
            'group_summary': group['group_summary'],
            'gif_path': relative_gif_path,
            'gif_relate': gif_relate,
            'gif_reason': gif_reason,
            'group_segments': group_segments
        }
        
        # Add GIF analysis if available
        if gif_analysis and gif_analysis.get('valid'):
            draft_entry['gif_analysis'] = {
                'has_motion': gif_analysis.get('has_motion', False),
                'avg_brightness': round(gif_analysis.get('avg_brightness', 0), 2),
                'avg_contrast': round(gif_analysis.get('avg_contrast', 0), 2)
            }
        
        final_draft.append(draft_entry)
        
        if logger:
            logger.debug(f"Group {group_id}: {gif_relate} - {gif_reason}")
    
    # Save final draft JSON
    output_file = Path(output_dir) / 'final_draft.json'
    save_json(final_draft, output_file)
    
    if logger:
        # Count statistics
        total_groups = len(final_draft)
        gifs_yes = sum(1 for entry in final_draft if entry['gif_relate'] == "Yes")
        gifs_no = sum(1 for entry in final_draft if entry['gif_relate'] == "No")
        
        logger.info(f"Enhanced final draft JSON created: {output_file}")
        logger.info(f"Statistics:")
        logger.info(f"  Total groups: {total_groups}")
        logger.info(f"  GIFs to include: {gifs_yes}")
        logger.info(f"  GIFs to exclude: {gifs_no}")
        logger.info(f"  Inclusion rate: {100 * gifs_yes / total_groups:.1f}%")
    
    return output_file


def validate_final_draft(final_draft_path, logger=None):
    """
    Validate the final draft JSON structure
    
    Args:
        final_draft_path: Path to final_draft.json
        logger: Logger instance
        
    Returns:
        bool: True if valid
    """
    from utils.json_io import load_json
    
    try:
        final_draft = load_json(final_draft_path)
        
        required_fields = [
            'group_id',
            'group_start_time',
            'group_end_time',
            'group_summary',
            'gif_path',
            'gif_relate',
            'group_segments'
        ]
        
        for idx, entry in enumerate(final_draft):
            # Check required fields
            for field in required_fields:
                if field not in entry:
                    if logger:
                        logger.error(f"Entry {idx}: Missing required field '{field}'")
                    return False
            
            # Check group_segments structure
            if not isinstance(entry['group_segments'], list):
                if logger:
                    logger.error(f"Entry {idx}: 'group_segments' must be a list")
                return False
            
            for seg_idx, segment in enumerate(entry['group_segments']):
                if 'segment_id' not in segment or 'text' not in segment:
                    if logger:
                        logger.error(f"Entry {idx}, Segment {seg_idx}: Missing 'segment_id' or 'text'")
                    return False
        
        if logger:
            logger.info(f"Final draft validation passed: {len(final_draft)} entries")
        
        return True
        
    except Exception as e:
        if logger:
            logger.error(f"Final draft validation failed: {e}")
        return False

