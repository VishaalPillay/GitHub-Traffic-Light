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

## Project Structure

```
.
├── data/
│   ├── videos/
│   │   └── sample_video.mp4      # Place your input video files here
│   │
│   └── images/
│       └── test_image_01.png     # Place test images here
│
├── .gitignore                    # To exclude unnecessary files from Git
├── main.py                       # The main Python script with all the logic
├── README.md                     # Project description for GitHub
└── requirements.txt              # List of Python dependencies
```

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
# On Windows PowerShell
venv\Scripts\Activate
# On macOS/Linux
source venv/bin/activate
```

**3. Install Dependencies:**

```bash
pip install -r requirements.txt
```

-----

## Usage

1.  Open `main.py`.

2.  Configure the video source by modifying the `video_source` variable at the top of the file:

      - **For Webcam:**
        ```python
        video_source = 0
        ```
      - **For Video File (place your file in `data/videos/`):**
        ```python
        video_source = "data/videos/sample_video.mp4"
        ```

3.  Run the script from your terminal:

    ```bash
    python main.py
    ```

4.  A window will appear showing the video feed with the detections. Press the **'q'** key to close the window and terminate the program.
