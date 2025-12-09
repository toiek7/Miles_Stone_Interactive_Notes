import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from transcription.transcribe import transcribe_video
from classification.segment_classifier import classify_segments
from filtering.filter_segments import filter_segments
from grouping.group_segments import group_and_summarize

def pipeline_part1(work_id, video_path, video_objective, output_dir, logger=None):
    """
    Executes the first part of the video processing pipeline:
    1. Transcription
    2. Classification
    3. Filtering
    4. Grouping & Summarization

    Args:
        output_dir (str): Directory to save outputs.
        video_path (str): Path to the input video file.
        video_objective (str): Objective or goal of the video content.

    Returns:
        dict: Grouped and summarized data.
    """

    try:
        # Step 1: Transcription
        print("\n[1/10] Transcribing video...")
        logger.info("Step 1: Starting transcription")
        transcript_data = transcribe_video(str(video_path), work_id, output_dir)
        logger.info(f"Transcription complete. {len(transcript_data['segments'])} segments found.")
        
        # Step 2: Classification
        print("\n[2/10] Classifying segments...")
        logger.info("Step 2: Starting segment classification")
        classified_segments = classify_segments(transcript_data['segments'], logger)
        logger.info(f"Classification complete. {len(classified_segments)} segments classified.")
        
        # Step 3: Filtering
        print("\n[3/10] Filtering irrelevant segments...")
        logger.info("Step 3: Starting segment filtering")
        filtered_segments = filter_segments(classified_segments, logger)
        logger.info(f"Filtering complete. {len(filtered_segments)} segments remaining.")
        
        # Step 4: Grouping & Summarization
        print("\n[4/10] Grouping and summarizing segments...")
        logger.info("Step 4: Starting grouping and summarization")
        grouped_data = group_and_summarize(filtered_segments, video_objective, output_dir, logger)
        logger.info(f"Grouping complete. {len(grouped_data)} groups created.")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        print(f"\nERROR: Pipeline failed: {str(e)}")
        sys.exit(1)

    return video_path, video_objective, output_dir
