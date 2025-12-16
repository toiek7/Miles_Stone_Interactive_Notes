from pathlib import Path
from utils.json_io import load_json
from video_processing.create_gif import convert_clips_to_gifs
from cv_filter.filter_gif import filter_gifs_by_relevance
from document_generator.create_final_draft import create_final_draft_json
from document_generator.generate_document import generate_with_ollama_cloud
from document_generator.build_html import build_final_html


def pipeline_part2(output_dir, video_objective, clips_dir, logger=None):
    output_dir = Path(output_dir)  # ensure it's a Path
    grouped_data = load_json(output_dir / "grouped.json")

    # Step 6: Convert to GIFs <<< Start here [Done]
    print("\n[6/10] Converting clips to GIFs...")
    gifs_output_dir, gifs_created = convert_clips_to_gifs(clips_dir, logger) 
    print(f"Created {len(gifs_created)} GIFs")
    print(f"GIFs saved to: {gifs_output_dir}")

    # Step 7: CV filtering <<<
    print("\n[7/10] Filtering GIFs by relevance...")
    relevant_gifs = filter_gifs_by_relevance(gifs_output_dir, grouped_data, logger, use_vision_model=True)  ## Change to use gifs_dir
    print(f"{len(relevant_gifs)} GIFs passed relevance check")

    ### Step 8:  Create final draft JSON with GIF information
    print("\n[8/10] Creating final draft JSON with GIF info...")
    final_draft_path = create_final_draft_json(grouped_data, relevant_gifs, gifs_output_dir, output_dir, logger)
    print(f"Final draft JSON created: {final_draft_path}")

    # Step 9: Generate teaching document << Need to change //This will send out the markdown with gif placeholders
    print("\n[9/10] Generating teaching document with gif placeholder...")
    # Load final draft data
    final_draft_data = load_json(final_draft_path)
    document_path = generate_with_ollama_cloud(final_draft_data, video_objective, output_dir, logger)
    print(f"Document generated: {document_path}")

    # Step 10: Build final HTML
    print("\n[10/10] Building final HTML document...")
    html_path = build_final_html(document_path, relevant_gifs, grouped_data, output_dir, logger)
    print(f"HTML document created: {html_path}")