# Traffic Light Detector

A real-time traffic light detection web application built with Flask, OpenCV, and computer vision techniques. The application can detect traffic light colors (Red, Yellow, Green) from uploaded images or live webcam feed and display corresponding status messages.

## Features

- **Real-time Detection**: Live webcam feed processing with continuous traffic light detection
- **Image Upload**: Upload static images for traffic light detection
- **Color Detection**: Accurate HSV-based color detection for Red, Yellow, and Green lights
- **Shape Detection**: Circular shape detection using HoughCircles for precise light identification
- **Modern UI**: Clean, responsive dark theme interface
- **Status Display**: Clear visual feedback with color-coded status messages
- **Cross-platform**: Works on Windows, macOS, and Linux

## Status Messages

- **STOP** - Red light detected
- **WAIT** - Yellow light detected  
- **GO** - Green light detected
- **TEST** - All three colors detected (test mode)
- **NO LIGHT DETECTED** - No traffic light found in the image

## Technology Stack

- **Backend**: Python 3.9+, Flask
- **Computer Vision**: OpenCV, NumPy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Image Processing**: HSV color space analysis, HoughCircles detection

## Installation

### Prerequisites

- Python 3.9 or higher
- Webcam (for live detection)
- Modern web browser with camera access support

### Setup

1. **Clone or download the project**
   ```bash
   cd traffic-light-detector
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### Webcam Detection
1. Click "Start Webcam" to begin live detection
2. Point your camera at a traffic light
3. The application will continuously detect and display the status
4. Click "Stop Webcam" to end the session

### Image Upload
1. Click "Choose Image File" to select an image
2. The application will process the image and display results
3. Uploaded images are processed once and results are shown

## Project Structure

```
traffic-light-detector/
├── app.py                 # Main Flask application
├── detector.py            # Computer vision detection logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Styling and responsive design
    └── js/
        └── script.js     # Frontend JavaScript functionality
```

## Technical Details

### Detection Algorithm

1. **Image Preprocessing**: Convert to grayscale and HSV color space
2. **Noise Reduction**: Apply Gaussian blur for better circle detection
3. **Shape Detection**: Use HoughCircles to detect circular traffic light shapes
4. **Color Analysis**: For each detected circle:
   - Create a circular mask
   - Apply HSV color range filtering
   - Count pixels for Red, Yellow, and Green
   - Determine dominant color based on pixel count
5. **Status Determination**: Map detected colors to traffic light states

### HSV Color Ranges

- **Red**: `(0,120,70)-(10,255,255)` and `(170,120,70)-(180,255,255)`
- **Yellow**: `(20,100,100)-(30,255,255)`
- **Green**: `(40,80,80)-(90,255,255)`

### API Endpoints

- `GET /` - Main application page
- `POST /detect` - Image processing endpoint
  - Input: JSON with base64 encoded image
  - Output: JSON with status and annotated image

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## Troubleshooting

### Webcam Issues
- Ensure camera permissions are granted
- Try refreshing the page
- Check if another application is using the camera

### Detection Issues
- Ensure good lighting conditions
- Traffic lights should be clearly visible
- Try different angles or distances
- Upload higher quality images

### Performance
- Close other applications using the camera
- Reduce browser tab count
- Ensure stable internet connection

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py
```

### Customizing Detection Parameters
Edit `detector.py` to adjust:
- HSV color ranges
- Circle detection parameters
- Minimum pixel thresholds
- Detection sensitivity

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Support

For issues or questions, please check the troubleshooting section or create an issue in the project repository.
