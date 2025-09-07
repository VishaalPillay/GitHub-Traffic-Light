/**
 * Traffic Light Detector - Frontend JavaScript
 * 
 * This script handles webcam access, file uploads, and communication
 * with the Flask backend for traffic light detection.
 */

// DOM Element References
const statusDisplay = document.getElementById('status-display');
const statusDescription = document.querySelector('.status-description');
const imageUpload = document.getElementById('imageUpload');
const startCamBtn = document.getElementById('startCam');
const stopCamBtn = document.getElementById('stopCam');
const webcam = document.getElementById('webcam');
const webcamPlaceholder = document.getElementById('webcam-placeholder');
const resultImage = document.getElementById('resultImage');
const resultPlaceholder = document.getElementById('result-placeholder');
const hiddenCanvas = document.getElementById('hiddenCanvas');

// Global variables
let stream = null;
let detectionInterval = null;
let isDetecting = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateStatus('READY', 'Upload an image or start your webcam to begin detection');
});

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    // File upload event listener
    imageUpload.addEventListener('change', handleFileUpload);
    
    // Webcam control event listeners
    startCamBtn.addEventListener('click', startWebcam);
    stopCamBtn.addEventListener('click', stopWebcam);
    
    // Handle page visibility change to stop detection when tab is not active
    document.addEventListener('visibilitychange', function() {
        if (document.hidden && isDetecting) {
            pauseDetection();
        } else if (!document.hidden && stream && !isDetecting) {
            resumeDetection();
        }
    });
}

/**
 * Handle file upload
 */
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file.');
        return;
    }
    
    // Validate file size (16MB limit)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size too large. Maximum size is 16MB.');
        return;
    }
    
    // Stop webcam if running
    if (stream) {
        stopWebcam();
    }
    
    // Read file and send to backend
    const reader = new FileReader();
    reader.onload = function(e) {
        sendFrameToBackend(e.target.result);
    };
    reader.readAsDataURL(file);
}

/**
 * Start webcam
 */
async function startWebcam() {
    try {
        updateStatus('INITIALIZING', 'Starting webcam...');
        
        // Request camera access
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'environment' // Use back camera if available
            }
        });
        
        // Set video source
        webcam.srcObject = stream;
        webcam.style.display = 'block';
        webcamPlaceholder.style.display = 'none';
        
        // Wait for video to be ready
        webcam.onloadedmetadata = function() {
            webcam.play();
            startDetection();
        };
        
        // Update UI
        startCamBtn.style.display = 'none';
        stopCamBtn.style.display = 'inline-block';
        
        updateStatus('DETECTING', 'Webcam active - detecting traffic lights...');
        
    } catch (error) {
        console.error('Error accessing webcam:', error);
        showError('Unable to access webcam. Please check permissions and try again.');
        updateStatus('ERROR', 'Webcam access failed');
    }
}

/**
 * Stop webcam
 */
function stopWebcam() {
    // Stop detection
    stopDetection();
    
    // Stop video stream
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    
    // Hide video and show placeholder
    webcam.style.display = 'none';
    webcamPlaceholder.style.display = 'block';
    resultImage.style.display = 'none';
    resultPlaceholder.style.display = 'block';
    
    // Update UI
    startCamBtn.style.display = 'inline-block';
    stopCamBtn.style.display = 'none';
    
    updateStatus('READY', 'Upload an image or start your webcam to begin detection');
}

/**
 * Start continuous detection
 */
function startDetection() {
    if (detectionInterval) return;
    
    isDetecting = true;
    detectionInterval = setInterval(() => {
        captureAndDetect();
    }, 200); // Detect every 200ms for smooth real-time experience
}

/**
 * Stop continuous detection
 */
function stopDetection() {
    if (detectionInterval) {
        clearInterval(detectionInterval);
        detectionInterval = null;
    }
    isDetecting = false;
}

/**
 * Pause detection (when tab is not active)
 */
function pauseDetection() {
    if (detectionInterval) {
        clearInterval(detectionInterval);
        detectionInterval = null;
    }
}

/**
 * Resume detection (when tab becomes active)
 */
function resumeDetection() {
    if (stream && !detectionInterval) {
        detectionInterval = setInterval(() => {
            captureAndDetect();
        }, 200);
    }
}

/**
 * Capture frame from webcam and send for detection
 */
function captureAndDetect() {
    if (!webcam.videoWidth || !webcam.videoHeight) return;
    
    // Set canvas dimensions to match video
    hiddenCanvas.width = webcam.videoWidth;
    hiddenCanvas.height = webcam.videoHeight;
    
    // Draw current video frame to canvas
    const ctx = hiddenCanvas.getContext('2d');
    ctx.drawImage(webcam, 0, 0);
    
    // Convert to base64 and send to backend
    const base64Image = hiddenCanvas.toDataURL('image/jpeg', 0.8);
    sendFrameToBackend(base64Image);
}

/**
 * Send frame to backend for detection
 */
async function sendFrameToBackend(base64Image) {
    try {
        const response = await fetch('/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: base64Image
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        updateUI(data);
        
    } catch (error) {
        console.error('Error sending frame to backend:', error);
        showError('Error processing image. Please try again.');
    }
}

/**
 * Update UI with detection results
 */
function updateUI(data) {
    if (data.error) {
        showError(data.error);
        return;
    }
    
    // Update status display
    const status = data.status;
    updateStatus(status, getStatusDescription(status));
    
    // Update result image
    if (data.image) {
        resultImage.src = 'data:image/jpeg;base64,' + data.image;
        resultImage.style.display = 'block';
        resultPlaceholder.style.display = 'none';
    }
    
    // Log detected colors for debugging
    if (data.detected_colors) {
        console.log('Detected colors:', data.detected_colors);
    }
}

/**
 * Update status display with color coding
 */
function updateStatus(status, description) {
    statusDisplay.textContent = status;
    statusDescription.textContent = description;
    
    // Remove all status classes
    statusDisplay.className = '';
    
    // Add appropriate status class for styling
    const statusClass = status.toLowerCase().replace(/\s+/g, '-');
    statusDisplay.classList.add(statusClass);
    
    // Add loading animation for detecting state
    if (status === 'DETECTING') {
        statusDisplay.classList.add('loading');
    } else {
        statusDisplay.classList.remove('loading');
    }
}

/**
 * Get description for status
 */
function getStatusDescription(status) {
    const descriptions = {
        'STOP': 'Red light detected - Please stop',
        'WAIT': 'Yellow light detected - Please wait',
        'GO': 'Green light detected - Safe to proceed',
        'TEST': 'All three colors detected - Test mode',
        'NO LIGHT DETECTED': 'No traffic light detected in the image',
        'READY': 'Upload an image or start your webcam to begin detection',
        'DETECTING': 'Webcam active - detecting traffic lights...',
        'INITIALIZING': 'Starting webcam...',
        'ERROR': 'An error occurred'
    };
    
    return descriptions[status] || 'Unknown status';
}

/**
 * Show error message
 */
function showError(message) {
    console.error('Error:', message);
    
    // Create error element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    
    // Insert error after status section
    const statusSection = document.querySelector('.status-section');
    statusSection.insertAdjacentElement('afterend', errorDiv);
    
    // Remove error after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 5000);
    
    updateStatus('ERROR', 'An error occurred');
}

/**
 * Show success message
 */
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success';
    successDiv.textContent = message;
    
    const statusSection = document.querySelector('.status-section');
    statusSection.insertAdjacentElement('afterend', successDiv);
    
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.parentNode.removeChild(successDiv);
        }
    }, 3000);
}

// Handle window resize for responsive design
window.addEventListener('resize', function() {
    // Adjust canvas size if webcam is active
    if (stream && webcam.videoWidth && webcam.videoHeight) {
        hiddenCanvas.width = webcam.videoWidth;
        hiddenCanvas.height = webcam.videoHeight;
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    if (detectionInterval) {
        clearInterval(detectionInterval);
    }
});
