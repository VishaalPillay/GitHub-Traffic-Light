-----

# Real-Time Traffic Light Detection System

This project is a real-time traffic light detection and classification system built using Python and OpenCV. The program processes video input from a live webcam or a file, identifies traffic lights, and classifies their state as red, yellow, or green. The detection is performed using color segmentation in the HSV color space, combined with shape and size filtering for improved accuracy.


-----

## Features

  - **Real-Time Detection:** Accurately detects and classifies traffic light states in real-time.
  - **Multiple Light Support:** Capable of handling and annotating multiple traffic lights within a single video frame.
  - **Flexible Input:** Processes video from both live webcams and pre-recorded video files.
  - **Robust Color Segmentation:** Uses the HSV color space for reliable color detection under varying lighting conditions.
  - **Noise Reduction:** Implements filtering based on object size and shape (circularity) to minimize false positives.
  - **Clear Visualization:** Overlays bounding boxes and color labels on the detected lights for clear and immediate feedback.

-----

## Tech Stack

  - **Python 3.x**
  - **OpenCV:** For all computer vision tasks, including video capture, image processing, and contour detection.
  - **NumPy:** For efficient numerical operations and array manipulation.

-----

## How It Works

The detection pipeline operates on each frame of the video stream and follows these steps:

1.  **Frame Capture:** Reads the video source frame by frame.
2.  **Preprocessing:** A Gaussian blur is applied to the frame to reduce noise and improve detection stability.
3.  **HSV Conversion:** The frame is converted from the BGR color space to HSV (Hue, Saturation, Value), which isolates color information more effectively than RGB.
4.  **Color Masking:** The HSV frame is segmented to create binary masks for red, yellow, and green colors based on predefined HSV ranges.
5.  **Contour Detection:** The system finds contours (i.e., outlines of continuous shapes) within each color mask.
6.  **Filtering & Validation:** Each contour is validated to ensure it resembles a traffic light. Contours that are too small or not sufficiently circular are discarded.
7.  **Visualization:** A bounding box and a corresponding color label are drawn on the original frame for each validated traffic light.

-----

## Setup and Installation

Follow these steps to get the project running on your local machine.

**1. Clone the Repository:**

```bash
git clone repolink
cd directory
```

**2. Create a Virtual Environment (Recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

**3. Install Dependencies:**
Create a file named `requirements.txt` with the following content:

```
opencv-python
numpy
```

Then, install the packages:

```bash
pip install -r requirements.txt
```

-----

## Usage

1.  Open the main Python script (e.g., `traffic_light_detector.py`).

2.  Configure the video source by modifying the `video_source` variable:

      - **For Webcam:**
        ```python
        video_source = 0
        ```
      - **For Video File:**
        ```python
        video_source = "path/to/your/video.mp4"
        ```

3.  Run the script from your terminal:

    ```bash
    python traffic_light_detector.py
    ```

4.  A window will appear showing the video feed with the detections. Press the **'q'** key to close the window and terminate the program.
