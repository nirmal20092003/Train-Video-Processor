# src/main.py
import os
from video_splitter import split_video_into_coaches
from frame_extractor import extract_frames_for_coverage
from component_detector import detect_components_on_frames
from report_generator import create_pdf_report

# --- Configuration ---
CONFIG = {
    'TRAIN_NUMBER': "12309",
    'INPUT_VIDEO_PATH': "input_video/Raw_video.mp4",
    'OUTPUT_DIR': "output",
    'PROCESSED_VIDEO_DIR': "output/Processed_Video",
    'FINAL_REPORT_DIR': "output/Final_Report",
    'PDF_REPORT_PATH': "output/Final_Report/Train_Coverage_Report.pdf",
    
    # --- Tuning Parameters ---
    # Lower this value if gaps are not detected; raise if normal motion is seen as a gap.
    'SIMILARITY_THRESHOLD': 0.2775, 
    # Number of frames to extract from each coach video for the report.
    'FRAMES_PER_COACH': 6 
}

def setup_directories():
    """Ensures all necessary output directories are created."""
    os.makedirs(CONFIG['PROCESSED_VIDEO_DIR'], exist_ok=True)
    os.makedirs(CONFIG['FINAL_REPORT_DIR'], exist_ok=True)

if __name__ == "__main__":
    print("Starting train video processing pipeline...")
    
    # 1. Create necessary directories
    setup_directories()

    # 2. Detect coaches and split the video
    print("\n--- Step 1: Splitting video into coach segments ---")
    coach_segments_data = split_video_into_coaches(CONFIG)
    if not coach_segments_data:
        print("Could not detect any coach segments. Exiting.")
        exit()

    # 3. Extract frames for coverage from each coach video
    print("\n--- Step 2: Extracting frames for coverage report ---")
    coach_segments_data = extract_frames_for_coverage(coach_segments_data, CONFIG)

    # 4. Simulate component detection and annotate frames
    print("\n--- Step 3: Annotating frames with component detection ---")
    coach_segments_data = detect_components_on_frames(coach_segments_data)
    
    # 5. Generate the final PDF report
    print("\n--- Step 4: Generating final PDF report ---")
    create_pdf_report(coach_segments_data, CONFIG)

    print("\n✅ Pipeline finished successfully!")