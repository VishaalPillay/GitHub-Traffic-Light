from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from detector import detect_traffic_light_state

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect_traffic_light():
    """
    API endpoint for traffic light detection.
    
    Expects JSON data with 'image' field containing base64 encoded image.
    Returns JSON with 'status' and 'image' fields.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Extract base64 image data
        image_data = data['image']
        
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_data)
        
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Decode image using OpenCV
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Detect traffic light state
        detected_colors, annotated_frame = detect_traffic_light_state(frame)
        
        # Determine status message based on detected colors
        status = determine_status(detected_colors)
        
        # Encode annotated frame back to base64
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        annotated_image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Return JSON response
        return jsonify({
            'status': status,
            'image': annotated_image_base64,
            'detected_colors': detected_colors
        })
        
    except Exception as e:
        print(f"Error in detection: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def determine_status(detected_colors):
    """
    Determine the traffic light status based on detected colors.
    
    Args:
        detected_colors (list): List of detected colors
        
    Returns:
        str: Status message
    """
    if not detected_colors:
        return "NO LIGHT DETECTED"
    
    # Check for all three colors (test mode)
    if 'red' in detected_colors and 'yellow' in detected_colors and 'green' in detected_colors:
        return "TEST"
    
    # Priority order: Red > Yellow > Green
    if 'red' in detected_colors:
        return "STOP"
    elif 'yellow' in detected_colors:
        return "WAIT"
    elif 'green' in detected_colors:
        return "GO"
    
    return "NO LIGHT DETECTED"


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server error."""
    return jsonify({'error': 'Internal server error'}), 500

