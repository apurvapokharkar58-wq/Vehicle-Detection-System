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