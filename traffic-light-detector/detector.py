"""
Traffic Light Detection Module

This module contains the core computer vision logic for detecting traffic lights
and determining their state using OpenCV and HSV color space analysis.
"""

import cv2
import numpy as np


def detect_traffic_light_state(frame):
    """
    Detect traffic light state from an input frame.
    
    Args:
        frame (numpy.ndarray): Input image frame as a NumPy array
        
    Returns:
        tuple: (detected_colors, annotated_frame)
            - detected_colors: List of detected colors ['red', 'yellow', 'green']
            - annotated_frame: Original frame with detection annotations
    """
    
    # Define HSV color ranges for traffic light colors
    # Red wraps around 0/180, so we need two ranges
    red_lower1 = np.array([0, 120, 70])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 120, 70])
    red_upper2 = np.array([180, 255, 255])
    
    # Yellow range
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    
    # Green range
    green_lower = np.array([40, 80, 80])
    green_upper = np.array([90, 255, 255])
    
    # Convert to grayscale and HSV
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=5,
        maxRadius=60
    )
    
    detected_colors = []
    annotated_frame = frame.copy()
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        for (x, y, r) in circles:
            # Create a mask for the circular region
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r, 255, -1)
            
            # Apply the mask to HSV image
            masked_hsv = cv2.bitwise_and(hsv, hsv, mask=mask)
            
            # Check for each color in the masked region
            color_counts = {}
            
            # Check for red (two ranges)
            red_mask1 = cv2.inRange(masked_hsv, red_lower1, red_upper1)
            red_mask2 = cv2.inRange(masked_hsv, red_lower2, red_upper2)
            red_mask = cv2.bitwise_or(red_mask1, red_mask2)
            color_counts['red'] = cv2.countNonZero(red_mask)
            
            # Check for yellow
            yellow_mask = cv2.inRange(masked_hsv, yellow_lower, yellow_upper)
            color_counts['yellow'] = cv2.countNonZero(yellow_mask)
            
            # Check for green
            green_mask = cv2.inRange(masked_hsv, green_lower, green_upper)
            color_counts['green'] = cv2.countNonZero(green_mask)
            
            # Find the dominant color (most non-zero pixels)
            if color_counts:
                dominant_color = max(color_counts, key=color_counts.get)
                
                # Only add if there's a significant amount of the color
                if color_counts[dominant_color] > 50:  # Threshold for minimum pixels
                    detected_colors.append(dominant_color)
                    
                    # Draw circle and label on annotated frame
                    color_bgr = get_color_bgr(dominant_color)
                    cv2.circle(annotated_frame, (x, y), r, color_bgr, 2)
                    cv2.putText(annotated_frame, dominant_color.upper(), 
                               (x - 20, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.6, color_bgr, 2)
    
    return detected_colors, annotated_frame


def get_color_bgr(color_name):
    """
    Get BGR color values for drawing annotations.
    
    Args:
        color_name (str): Color name ('red', 'yellow', 'green')
        
    Returns:
        tuple: BGR color values
    """
    color_map = {
        'red': (0, 0, 255),
        'yellow': (0, 255, 255),
        'green': (0, 255, 0)
    }
    return color_map.get(color_name, (255, 255, 255))  # Default to white
