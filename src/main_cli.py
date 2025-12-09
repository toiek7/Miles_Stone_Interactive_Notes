#!/usr/bin/env python3
"""
Main CLI for Instruction Video to Teaching Document Generator
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger
from utils.timestamp import generate_work_id
from utils.json_io import load_json
from transcription.transcribe import transcribe_video
from classification.segment_classifier import classify_segments
from filtering.filter_segments import filter_segments
from grouping.group_segments import group_and_summarize
from video_processing.cut_video import cut_video_clips
from video_processing.create_gif import convert_clips_to_gifs
from cv_filter.filter_gif import filter_gifs_by_relevance
from document_generator.generate_document import generate_teaching_document, generate_with_ollama, generate_with_ollama_cloud
from document_generator.build_html import build_final_html
from document_generator.create_final_draft import create_final_draft_json


def main():
    """Main entry point for the CLI application"""
    
    print("=" * 70)
    print("  Instruction Video to Teaching Document Generator")
    print("=" * 70)
    print()
    
    # Get user inputs
    video_filename = input("Enter video filename (in /data directory): ").strip()
    video_path = Path("data") / video_filename
    
    if not video_path.exists():
        print(f"ERROR: Video file not found at {video_path}")
        sys.exit(1)
    
    video_objective = input("Enter video objective/desired learning outcome: ").strip()
    
    if not video_objective:
        print("ERROR: Video objective cannot be empty")
        sys.exit(1)
    
    # Generate work ID
    work_id = generate_work_id()
    output_dir = Path("output") / f"work_{work_id}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup logger
    logger = setup_logger(output_dir / "pipeline.log")
    
    logger.info("=" * 70)
    logger.info(f"Starting pipeline for work_id: {work_id}")
    logger.info(f"Video: {video_path}")
    logger.info(f"Objective: {video_objective}")
    logger.info("=" * 70)
    
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

        # Step 5: Cut video clips
        print("\n[5/10] Cutting video clips...")
        logger.info("Step 5: Cutting video clips")
        clips_dir = cut_video_clips(str(video_path), grouped_data, output_dir, logger)
        logger.info(f"Clips saved to: {clips_dir}")

        # Step 6: Convert to GIFs <<< Start here [Done]
        print("\n[6/10] Converting clips to GIFs...")
        logger.info("Step 6: Converting clips to GIFs")
        gifs_output_dir, gifs_created = convert_clips_to_gifs(clips_dir, logger) 
        logger.info(f"Created {len(gifs_created)} GIFs")
        logger.info(f"GIFs saved to: {gifs_output_dir}")

        # Step 7: CV filtering <<<
        print("\n[7/10] Filtering GIFs by relevance...")
        logger.info("Step 7: Filtering GIFs using computer vision")
        relevant_gifs = filter_gifs_by_relevance(gifs_output_dir, grouped_data, logger, use_vision_model=True)  ## Change to use gifs_dir
        logger.info(f"{len(relevant_gifs)} GIFs passed relevance check")

        ### Step 8:  Create final draft JSON with GIF information
        print("\n[8/10] Creating final draft JSON with GIF info...")
        logger.info("Step 8: Creating final draft JSON")
        final_draft_path = create_final_draft_json(grouped_data, relevant_gifs, gifs_output_dir, output_dir, logger)
        logger.info(f"Final draft JSON created: {final_draft_path}")

        # Step 9: Generate teaching document << Need to change //This will send out the markdown with gif placeholders
        print("\n[9/10] Generating teaching document with gif placeholder...")
        logger.info("Step 9: Generating teaching document with OLLAMA Cloud (gpt-oss:120b-cloud)")
        # Load final draft data
        final_draft_data = load_json(final_draft_path)
        document_path = generate_with_ollama_cloud(final_draft_data, video_objective, output_dir, logger)
        logger.info(f"Document generated: {document_path}")
        
        # Step 10: Build final HTML
        print("\n[10/10] Building final HTML document...")
        logger.info("Step 10: Building final HTML document")
        html_path = build_final_html(document_path, relevant_gifs, grouped_data, output_dir, logger)
        logger.info(f"HTML document created: {html_path}")
        
        print("\n" + "=" * 70)
        print("  PIPELINE COMPLETE!")
        print("=" * 70)
        print(f"\nWork ID: {work_id}")
        print(f"Output directory: {output_dir}")
        print(f"Final document: {html_path}")
        print("\nGenerated files:")
        print(f"  - Transcript: {output_dir}/transcript.json")
        print(f"  - Grouped data: {output_dir}/grouped.json")
        print(f"  - Raw document: {output_dir}/document_raw.md")
        print(f"  - Final HTML: {output_dir}/index.html")
        print(f"  - Video clips: {output_dir}/clips/")
        print()
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        print(f"\nERROR: Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
