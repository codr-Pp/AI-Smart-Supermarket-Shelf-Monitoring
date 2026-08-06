# Architecture

## Overview

The backend is a Flask application that receives shelf images, runs YOLOv8 object detection, updates in-memory inventory metrics, uploads annotated images to Cloudinary, and exposes dashboard/report endpoints.

## Main Components

- `run.py` starts the local Flask server.
- `config.py` centralizes paths and integration settings.
- `app/routes/monitoring.py` contains the existing HTTP routes and detection/report workflow.
- `app/services/` contains helper services and legacy detector/storage modules.
- `app/templates/dashboard.html` renders the live monitoring dashboard.
- `app/static/` stores dashboard static files and existing generated visual assets.

## Request Flow

1. ESP32-CAM posts image bytes to `POST /upload`.
2. The image is written to `uploads/`.
3. YOLOv8 loads `runs/detect/train/weights/best.pt` and detects products.
4. The annotated image is saved beside the upload and sent to Cloudinary.
5. In-memory stock and ML insight counters are updated.
6. Alert email logic runs for low Campa stock or Sprite detection.
7. The dashboard polls `GET /latest` for the newest detection state.

## Persistence

The current app uses local files for images/reports and in-memory dictionaries for dashboard counters. Restarting the Flask process resets counters but keeps uploaded files.

## Deployment Notes

- Move secrets into environment variables or a deployment secret manager.
- Keep the YOLO weights available at `MODEL_PATH`.
- Do not commit generated runtime folders such as `temp/`, `temp_uploads/`, `runs_old/`, or virtual environments.
