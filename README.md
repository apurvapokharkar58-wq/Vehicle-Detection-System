# 🚗 Vehicle Detection and Analytics System

A computer vision-based vehicle analytics application that detects, tracks, classifies, and counts vehicles in traffic videos using YOLO11, OpenCV, and ByteTrack. The system also estimates vehicle colors, detects line crossings, stores traffic events in PostgreSQL, and displays analytics through a web dashboard.

## 📌 Project Overview

The Vehicle Detection and Analytics System aims to provide automated traffic monitoring and vehicle analytics.

The application processes traffic videos, identifies vehicles, assigns tracking IDs, estimates vehicle colors, detects line-crossing events, and stores relevant information in a PostgreSQL database.

A custom web dashboard built using HTML, CSS, JavaScript, and Flask presents vehicle statistics, color analytics, recent events, and the annotated tracking video.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| YOLO11n | Vehicle detection |
| OpenCV | Video processing |
| ByteTrack | Multi-object tracking |
| NumPy | Image processing |
| Flask | Web application backend |
| HTML, CSS, JavaScript | Frontend dashboard |
| PostgreSQL | Event data storage |
| CSV | Analytics reports |
| MediaMTX | RTSP stream testing |
| Google Colab | NVIDIA GPU testing |
| Git and GitHub | Version control |

## ✨ Features

- Vehicle detection using YOLO11n.
- Vehicle tracking using ByteTrack.
- Vehicle classification into Car, Bike, Bus, and Truck.
- Unique vehicle counting.
- Line-crossing detection.
- Vehicle movement direction estimation (Up/Down).
- Basic vehicle color estimation using HSV color space.
- PostgreSQL storage of vehicle crossing events.
- CSV report generation.
- Custom responsive web dashboard.
- Vehicle analytics and color charts.
- Recent vehicle event history.
- Annotated vehicle tracking video playback.
- Periodic dashboard data refresh.

## 🏗️ Project Architecture

```text
              Traffic Video
                    |
                    v
              YOLO11 Detection
                    |
                    v
              ByteTrack Tracking
                    |
                    v
          Vehicle Color Estimation
                    |
                    v
           Line Crossing Detection
                    |
                    v
             PostgreSQL Database
                    |
                    v
              Flask Backend
                    |
                    v
          HTML / CSS / JavaScript
                    |
                    v
            Analytics Dashboard
```

MediaMTX RTSP ingestion was also tested separately as part of the video ingestion prototype. Integration of the RTSP stream into the native DeepStream pipeline remains pending.

## 📂 Project Structure

```text
Vehicle-Detection-System/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── deepstream/
│   ├── README.md
│   └── config/
│       └── pipeline.ini
│
├── videos/
│   └── Sample_Traffic.mp4
│
├── detect.py
├── color_classifier.py
├── database.py
├── web_app.py
├── dashboard.py
├── requirements.txt
├── vehicle_report.csv
├── line_crossing_events.csv
├── vehicle_color_results.csv
├── README.md
└── .gitignore
```

Note: Video files, model weights, virtual environments, and database credentials are excluded from the GitHub repository where appropriate.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/apurvapokharkar58-wq/Vehicle-Detection-System.git
```

```bash
cd Vehicle-Detection-System
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Add the Input Video

Create a `videos` folder and place your traffic video inside it.

The current detection script uses:

```text
videos/Sample_Traffic.mp4
```

### 5. Configure PostgreSQL

Install and start PostgreSQL.

Create a database named:

```sql
CREATE DATABASE vehicle_analytics;
```

Create the vehicle events table:

```sql
CREATE TABLE vehicle_events (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    direction VARCHAR(10) NOT NULL,
    color VARCHAR(30)
);
```

Create a `.env` file in the project root:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vehicle_analytics
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
```

Replace the password with your own PostgreSQL password. Do not upload `.env` to GitHub.

## ▶️ Running the Application

### 1. Run Vehicle Detection

```bash
python detect.py
```

This processes the input traffic video and generates detection, tracking, and analytics results.

### 2. Start the Web Dashboard

Open another terminal in the project directory, activate the virtual environment, and run:

```bash
python web_app