import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger
from utils.timestamp import generate_work_id
from pipeline_part1 import pipeline_part1
from pipeline_part2 import pipeline_part2

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

# Run pipeline part 1
logger.info("\n" + "=" * 70 + "\n")
logger.info("Running Pipeline Part 1")
video_path, video_objective, output_dir = pipeline_part1(work_id, video_path, video_objective, output_dir, logger)

# Run pipeline part 2
logger.info("\n" + "=" * 70 + "\n")
logger.info("Running Pipeline Part 2")
pipeline_part2(output_dir, video_path, video_objective, logger)

logger.info("=" * 70)
logger.info(f"Pipeline completed for work_id: {work_id}")
logger.info(f"All outputs saved in: {output_dir}")