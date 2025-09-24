# src/component_detector.py
import cv2
import os
import random

def detect_components_on_frames(coach_data):
    """
    Simulates door detection on extracted frames.
    A real implementation would load a model (e.g., YOLO) here.
    """
    for coach in coach_data:
        frame_folder = coach.get('frame_folder')
        if not frame_folder or not os.path.exists(frame_folder):
            continue

        image_files = [f for f in os.listdir(frame_folder) if f.endswith('.jpg')]
        print(f"Annotating frames for coach {coach['id']}...")

        for image_name in image_files:
            image_path = os.path.join(frame_folder, image_name)
            image = cv2.imread(image_path)
            if image is None:
                continue

            # --- SIMULATED DETECTION ---
            # In a real scenario, you would run your model here:
            # results = model(image)
            # for box in results.xyxy[0]:
            #     x1, y1, x2, y2, conf, cls = box
            
            # For now, we draw a random box to simulate detection.
            h, w, _ = image.shape
            # Draw a box for a "door"
            x1, y1 = int(w * 0.4), int(h * 0.3)
            x2, y2 = int(w * 0.6), int(h * 0.8)
            
            # Randomly decide if the door is open or closed
            is_open = random.choice([True, False])
            
            if is_open:
                color = (0, 0, 255)  # Red for open
                label = "Door is open"
            else:
                color = (0, 255, 0)  # Green for closed
                label = "Door is closed"
            
            # Draw rectangle and label
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            
            # Save the annotated image, overwriting the original
            cv2.imwrite(image_path, image)
            
    print("Annotation simulation complete.")
    return coach_data