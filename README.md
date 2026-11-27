# Vehicle Detection and Counting System

## Project Overview
A Python-based computer vision project that detects, tracks, and counts vehicles in traffic videos using YOLO11 and OpenCV.

## Technologies Used
- Python
- OpenCV
- YOLO11 (Ultralytics)
- ByteTrack
- CSV

## Features
- Vehicle detection in traffic videos
- Vehicle tracking using ByteTrack
- Vehicle counting by category
- Video output with detection annotations
- CSV report generation

## How to Run

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Add your traffic video inside the videos folder.
5. Run:

   python detect.py

## Output Files
- tracking_output.mp4
- vehicle_report.csv

## Note
The YOLO11n pretrained model weights and traffic video are not included in this repository.

## GPU Testing Results (Google Colab)

The vehicle detection and tracking pipeline was tested using a free NVIDIA Tesla T4 GPU in Google Colab.

### Test Configuration
- GPU: NVIDIA Tesla T4
- Detection Model: YOLO11n
- Tracking Algorithm: ByteTrack
- Input Video: Sample_Traffic.mp4
- Image Size: 416
- Confidence Threshold: 0.35
- Frames Processed: 298

### Test Results

| Test | Result |
|---|---:|
| Vehicle detection | Successful |
| Vehicle tracking | Successful |
| Tracking IDs verified | Successful |
| Unique line crossings | 12 |
| Down crossings | 12 |
| Up crossings | 0 |

### Conclusion

The YOLO-based vehicle detection, ByteTrack tracking, unique vehicle counting, and line-crossing direction detection prototypes were successfully tested on an NVIDIA Tesla T4 GPU.

**Note:** Native NVIDIA DeepStream SDK integration is still pending. The GPU tests were performed using Ultralytics YOLO and ByteTrack.