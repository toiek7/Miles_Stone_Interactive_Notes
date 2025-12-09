# Test on output/work_20251209_025156

from document_generator.build_html import build_final_html
from document_generator.generate_document import generate_with_ollama_cloud
from utils.json_io import load_json

final_draft_path = "output/work_20251209_025156/final_draft.json"
video_objective = ""
output_dir = "output/work_20251209_025156"

# Step 8: Generate teaching document using final draft
print("\n[8/9] Generating teaching document with GIF placeholders...")

# Load final draft data
final_draft_data = load_json(final_draft_path)

document_path = generate_with_ollama_cloud(
    final_draft_data,
    video_objective,
    output_dir,
    logger=None
)
print(f"Document generated: {document_path}")