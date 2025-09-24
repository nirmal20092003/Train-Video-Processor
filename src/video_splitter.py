# src/video_splitter.py
import cv2
import os
import numpy as np
from utils import calculate_frame_similarity

def split_video_into_coaches(config):
    """
    Detects gaps between coaches using frame similarity and splits the video.
    """
    video_path = config['INPUT_VIDEO_PATH']
    output_dir = config['PROCESSED_VIDEO_DIR']
    train_number = config['TRAIN_NUMBER']
    threshold = config['SIMILARITY_THRESHOLD']

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define a vertical Region of Interest (ROI) in the center of the frame
    roi_x = int(width / 2) - 25
    roi_w = 50
    roi_rect = (roi_x, 0, roi_w, height)

    coach_segments = []
    coach_count = 0
    start_frame = 0
    is_in_gap = False
    
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read the first frame.")
        return []

    frame_num = 1
    while True:
        ret, current_frame = cap.read()
        if not ret:
            # End of video, save the last segment
            coach_segments.append({'start': start_frame, 'end': frame_num - 1})
            break

        similarity = calculate_frame_similarity(prev_frame, current_frame, roi_rect)

        # A sharp drop in similarity indicates a gap between coaches
        if similarity < threshold and not is_in_gap:
            is_in_gap = True
            end_frame = frame_num
            coach_segments.append({'start': start_frame, 'end': end_frame})
            start_frame = end_frame + 1

        # When similarity recovers, it means the next coach has entered the frame
        elif similarity >= threshold and is_in_gap:
            is_in_gap = False

        prev_frame = current_frame
        frame_num += 1

    print(f"Detected {len(coach_segments)} segments in the video.")
    
    # Now, save each segment as a separate video file
    coach_data = []
    for i, seg in enumerate(coach_segments, 1):
        coach_count = i
        coach_folder = os.path.join(output_dir, f"{train_number}_{coach_count}")
        os.makedirs(coach_folder, exist_ok=True)
        
        video_filename = f"{train_number}_{coach_count}.mp4"
        video_filepath = os.path.join(coach_folder, video_filename)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_filepath, fourcc, fps, (width, height))
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, seg['start'])
        for fn in range(seg['start'], seg['end'] + 1):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        out.release()

        print(f"Saved video for coach {coach_count} at {video_filepath}")
        coach_data.append({
            'id': coach_count,
            'folder': coach_folder,
            'video_path': video_filepath
        })

    cap.release()
    return coach_data