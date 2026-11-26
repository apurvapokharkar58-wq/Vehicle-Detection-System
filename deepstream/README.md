# NVIDIA DeepStream Integration

## Project Overview

This folder contains the planned NVIDIA DeepStream implementation for the Real-Time Vehicle Analytics Pipeline.

The goal is to process vehicle video streams using GPU-accelerated inference and tracking.

## Planned Pipeline

1. Video input through RTSP using MediaMTX.
2. Vehicle detection using a YOLO model with NVIDIA TensorRT.
3. Vehicle tracking using NvDCF or another supported tracker.
4. Vehicle colour classification.
5. Line-crossing detection and direction identification.
6. Vehicle event storage in PostgreSQL.
7. Analytics display through the project dashboard.

## Required Environment

- NVIDIA GPU
- Compatible NVIDIA driver and CUDA
- NVIDIA DeepStream SDK
- GStreamer
- TensorRT
- PostgreSQL

## Implementation Status

- MediaMTX RTSP ingestion: Prototype tested locally.
- YOLO vehicle detection and tracking: Implemented using Python and Ultralytics.
- Line-crossing detection: Implemented.
- Basic vehicle colour estimation: Implemented.
- PostgreSQL event storage: Implemented.
- Streamlit dashboard: Implemented.
- Native NVIDIA DeepStream pipeline: Pending compatible environment setup.

**Note:** The existing Python implementation is a working prototype. The native DeepStream pipeline has not yet been executed.