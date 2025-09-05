import cv2
import numpy as np

# --- Configuration & Tuning Parameters ---
video_source = 0
FRAME_WIDTH = 800

# --- Circle Detection (Hough Transform) Parameters ---
# These are crucial for accuracy. Tune these carefully for your camera/environment.
HOUGH_DP = 1.2          # Inverse ratio of accumulator resolution.
HOUGH_MIN_DIST = 50    # Minimum distance between the centers of detected circles. Increased for less close detections.
HOUGH_PARAM1 = 150      # Upper threshold for the internal Canny edge detector. Increased for stronger edges.
HOUGH_PARAM2 = 40       # Accumulator threshold for center detection. Increased for more confident detections.
HOUGH_MIN_RADIUS = 10   # Minimum circle radius. Adjusted based on typical traffic light size in frame.
HOUGH_MAX_RADIUS = 70   # Maximum circle radius. Adjusted.

# --- Color Detection Parameters ---
# HSV color ranges (tuned for better distinction)
RED_LOWER1 = np.array([0, 150, 120])
RED_UPPER1 = np.array([10, 255, 255])
RED_LOWER2 = np.array([170, 150, 120])
RED_UPPER2 = np.array([180, 255, 255])
YELLOW_LOWER = np.array([20, 150, 120])
YELLOW_UPPER = np.array([35, 255, 255]) # Slightly wider hue for yellow
GREEN_LOWER = np.array([40, 100, 100])
GREEN_UPPER = np.array([90, 255, 255])

# New: Confidence thresholds for color, saturation, and value within detected circles
COLOR_PIXEL_THRESHOLD_RATIO = 0.3 # Minimum ratio of pixels of specific color within circle to total circle pixels
MIN_SATURATION = 100 # Minimum saturation value in HSV for a pixel to be considered "colored"
MIN_VALUE = 80       # Minimum brightness/value in HSV for a pixel to be considered "bright"

# Text display parameters
FONT = cv2.FONT_HERSHEY_SIMPLEX

# --- Helper Function for Robust Color Check ---
def get_dominant_color_in_circle(hsv_frame, center, radius):
    """
    Checks the dominant color within a circle's region, considering saturation and value.
    Returns "Red", "Yellow", "Green", or None.
    """
    # Create a circular mask for the region of interest
    mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, thickness=cv2.FILLED)

    # Extract the ROI using the mask
    masked_hsv = cv2.bitwise_and(hsv_frame, hsv_frame, mask=mask)

    # Filter by saturation and value to exclude dull/dark areas
    saturated_pixels_mask = cv2.inRange(masked_hsv, (0, MIN_SATURATION, MIN_VALUE), (180, 255, 255))
    
    # Apply median blur to the saturated pixels mask to clean it up
    saturated_pixels_mask = cv2.medianBlur(saturated_pixels_mask, 5)

    total_circle_pixels = cv2.countNonZero(mask)
    if total_circle_pixels == 0:
        return None, 0 # Avoid division by zero

    color_scores = {}

    # Check for red
    red_mask1 = cv2.inRange(masked_hsv, RED_LOWER1, RED_UPPER1)
    red_mask2 = cv2.inRange(masked_hsv, RED_LOWER2, RED_UPPER2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    red_pixels = cv2.countNonZero(cv2.bitwise_and(red_mask, saturated_pixels_mask))
    color_scores["Red"] = red_pixels / total_circle_pixels

    # Check for yellow
    yellow_mask = cv2.inRange(masked_hsv, YELLOW_LOWER, YELLOW_UPPER)
    yellow_pixels = cv2.countNonZero(cv2.bitwise_and(yellow_mask, saturated_pixels_mask))
    color_scores["Yellow"] = yellow_pixels / total_circle_pixels

    # Check for green
    green_mask = cv2.inRange(masked_hsv, GREEN_LOWER, GREEN_UPPER)
    green_pixels = cv2.countNonZero(cv2.bitwise_and(green_mask, saturated_pixels_mask))
    color_scores["Green"] = green_pixels / total_circle_pixels

    dominant_color = None
    max_ratio = 0
    for color, ratio in color_scores.items():
        if ratio > max_ratio and ratio >= COLOR_PIXEL_THRESHOLD_RATIO:
            max_ratio = ratio
            dominant_color = color
            
    return dominant_color, max_ratio

# --- Main Detection Logic ---
def detect_traffic_lights(frame):
    """
    Detects traffic lights by first finding circles, then validating their color and properties.
    """
    annotated_frame = frame.copy()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_gray = cv2.medianBlur(gray_frame, 5)

    # --- Stage 1: Detect Circles using Hough Circle Transform ---
    circles = cv2.HoughCircles(blurred_gray, cv2.HOUGH_GRADIENT,
                               dp=HOUGH_DP,
                               minDist=HOUGH_MIN_DIST,
                               param1=HOUGH_PARAM1,
                               param2=HOUGH_PARAM2,
                               minRadius=HOUGH_MIN_RADIUS,
                               maxRadius=HOUGH_MAX_RADIUS)
    
    red_detected, yellow_detected, green_detected = False, False, False

    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            
            # --- Stage 2: Robustly Validate Color within each detected circle ---
            dominant_color, confidence = get_dominant_color_in_circle(hsv_frame, center, radius)

            if dominant_color:
                color_bgr = (0, 0, 0) # Default
                if dominant_color == "Red":
                    color_bgr = (0, 0, 255)
                    red_detected = True
                elif dominant_color == "Yellow":
                    color_bgr = (0, 255, 255)
                    yellow_detected = True
                elif dominant_color == "Green":
                    color_bgr = (0, 255, 0)
                    green_detected = True
                
                # Draw the circle and label
                cv2.circle(annotated_frame, center, radius, color_bgr, 3)
                cv2.putText(annotated_frame, dominant_color, (center[0] - radius, center[1] - radius - 10), FONT, 0.7, color_bgr, 2)

    # --- Determine Overall State ---
    overall_state = None
    if red_detected and yellow_detected and green_detected:
        overall_state = "TEST"
    elif red_detected:
        overall_state = "STOP"
    elif yellow_detected:
        overall_state = "WAIT"
    elif green_detected:
        overall_state = "GO"
        
    return annotated_frame, overall_state

# --- Main Program Loop ---
def main():
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}.")
        return

    while True:
        ret, frame = cap.read()
        if not ret: 
            # If reading from a file, loop it
            if isinstance(video_source, str):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                print("Error reading frame from webcam.")
                break
        
        # Resize frame
        h, w, _ = frame.shape
        frame = cv2.resize(frame, (FRAME_WIDTH, int(FRAME_WIDTH * h / w)))

        annotated_frame, state = detect_traffic_lights(frame)
        
        # Display the overall state
        if state:
            (tw, th), _ = cv2.getTextSize(state, FONT, 1, 2)
            tx, ty = annotated_frame.shape[1] - tw - 20, th + 20
            cv2.rectangle(annotated_frame, (tx - 10, ty - th - 10), (tx + tw + 10, ty + 10), (0,0,0), -1)
            cv2.putText(annotated_frame, state, (tx, ty), FONT, 1, (255,255,255), 2, cv2.LINE_AA)

        cv2.imshow("Traffic Light Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()