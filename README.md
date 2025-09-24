# Project: Train Video Processing and Analysis

This project provides an end-to-end pipeline to process a side-view video of a moving train. It automatically detects and counts the coaches, splits the video into individual clips for each coach, extracts keyframes for full coverage, and generates a detailed PDF report.

## Key Features Implemented

* *[span_0](start_span)Coach Counting & Video Splitting:* Automatically detects the gaps between coaches to count them and split the main video into separate segments[span_0](end_span).
* *[span_1](start_span)Structured Output:* Organizes the output into a clean folder structure, with a dedicated directory for each coach[span_1](end_span).
* *[span_2](start_span)[span_3](start_span)[span_4](start_span)File Naming Convention:* Adheres to the specified <train_number>_<counter> format for all generated files and folders[span_2](end_span)[span_3](end_span)[span_4](end_span).
* *[span_5](start_span)Minimal Frame Extraction:* Extracts a minimal set of frames from each coach's video to ensure full visual coverage without redundancy[span_5](end_span).
* *Component Detection Simulation:* Includes a module to annotate frames with bounding boxes for components like doors. [span_6](start_span)Note: This uses a simulated detector but is built to integrate a real model (e.g., YOLO) easily.[span_6](end_span)
* *[span_7](start_span)[span_8](start_span)PDF Report Generation:* Compiles all the data into a final, multi-page PDF report, starting with a summary table as requested[span_7](end_span)[span_8](end_span).

## Setup and Installation

1.  *Clone the repository or create the project structure as described.*

2.  *Create and activate a Python virtual environment:*
    bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    

3.  *Install the required dependencies:*
    bash
    pip install -r requirements.txt
    

## How to Run the Project

1.  Place your raw train video inside the input_video/ folder and name it Raw_video.mp4.

2.  Run the main script from the root directory of the project:
    bash
    python src/main.py
    

3.  The script will process the video and generate all the output files in the output/ directory.

## Assumptions and Limitations

* The camera is assumed to be stationary for the gap detection logic to work reliably.
* The train moves at a relatively consistent speed.
* The component detection for doors is *simulated*. To implement actual detection, a custom object detection model must be trained on an annotated dataset of train doors. The current code provides the framework for integrating such a model.
