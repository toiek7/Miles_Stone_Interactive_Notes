from utils.json_io import load_json
from video_processing.cut_video import cut_video_clips
from video_processing.create_gif import convert_clips_to_gifs
from cv_filter.filter_gif import filter_gifs_by_relevance
from document_generator.create_final_draft import create_final_draft_json
from document_generator.generate_document import generate_with_ollama_cloud
from document_generator.build_html import build_final_html

# Change these paths as needed for testing
output_dir = "output/work_20251209_064431"
video_path = "data/100s_ml_explain.mp4"
video_objective = """
Machine Learning is the process of teaching a computer how perform a task with out explicitly programming it. The process feeds algorithms with large amounts of data to gradually improve predictive performance.
"""


grouped_data = load_json(output_dir + "/grouped.json")


# Step 5: Cut video clips
print("\n[5/10] Cutting video clips...")
clips_dir = cut_video_clips(str(video_path), grouped_data, output_dir, logger=None)
print(f"Clips saved to: {clips_dir}")

# Step 6: Convert to GIFs <<< Start here [Done]
print("\n[6/10] Converting clips to GIFs...")
gifs_output_dir, gifs_created = convert_clips_to_gifs(clips_dir, logger=None) 
print(f"Created {len(gifs_created)} GIFs")
print(f"GIFs saved to: {gifs_output_dir}")

# Step 7: CV filtering <<<
print("\n[7/10] Filtering GIFs by relevance...")
relevant_gifs = filter_gifs_by_relevance(gifs_output_dir, grouped_data, logger=None, use_vision_model=True)  ## Change to use gifs_dir
print(f"{len(relevant_gifs)} GIFs passed relevance check")

### Step 8:  Create final draft JSON with GIF information
print("\n[8/10] Creating final draft JSON with GIF info...")
final_draft_path = create_final_draft_json(grouped_data, relevant_gifs, gifs_output_dir, output_dir, logger=None)
print(f"Final draft JSON created: {final_draft_path}")

# Step 9: Generate teaching document << Need to change //This will send out the markdown with gif placeholders
print("\n[9/10] Generating teaching document with gif placeholder...")
# Load final draft data
final_draft_data = load_json(final_draft_path)
document_path = generate_with_ollama_cloud(final_draft_data, video_objective, output_dir, logger=None)
print(f"Document generated: {document_path}")

# Step 10: Build final HTML
print("\n[10/10] Building final HTML document...")
html_path = build_final_html(document_path, relevant_gifs, grouped_data, output_dir, logger=None)
print(f"HTML document created: {html_path}")