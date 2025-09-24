# src/utils.py
import cv2
from skimage.metrics import structural_similarity as ssim

def calculate_frame_similarity(frame1, frame2, roi_rect):
    """
    Calculates the Structural Similarity Index (SSIM) between two frames
    within a specific region of interest (ROI).
    """
    x, y, w, h = roi_rect
    
    # Extract the ROI from both frames
    roi1 = frame1[y:y+h, x:x+w]
    roi2 = frame2[y:y+h, x:x+w]
    
    # Convert ROIs to grayscale for SSIM calculation
    gray_roi1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
    gray_roi2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
    
    # Calculate SSIM
    score, _ = ssim(gray_roi1, gray_roi2, full=True)
    
    return score