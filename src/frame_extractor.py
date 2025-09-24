# src/frame_extractor.py
import cv2
import os

def extract_frames_for_coverage(coach_data, config):
    """
    Extracts frames from each coach's video segment at a fixed interval.
    """
    train_number = config['TRAIN_NUMBER']
    frames_per_coach = config['FRAMES_PER_COACH']

    for coach in coach_data:
        video_path = coach['video_path']
        coach_id = coach['id']
        output_folder = os.path.join(coach['folder'], "annotated_frames")
        os.makedirs(output_folder, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Warning: Could not open {video_path} for frame extraction.")
            continue

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Calculate interval to get the desired number of frames
        interval = max(1, total_frames // frames_per_coach)

        frame_count = 0
        saved_frame_num = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % interval == 0:
                saved_frame_num += 1
                image_name = f"{train_number}_{coach_id}_{saved_frame_num}.jpg"
                image_path = os.path.join(output_folder, image_name)
                cv2.imwrite(image_path, frame)
            
            frame_count += 1
        
        cap.release()
        print(f"Extracted {saved_frame_num} frames for coach {coach_id}.")
        coach['frame_folder'] = output_folder
    
    return coach_data