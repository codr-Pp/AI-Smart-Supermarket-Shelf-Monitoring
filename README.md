# Intelligent Supermarket Shelf Monitoring System

AI-powered Flask backend for supermarket shelf monitoring, stock auditing, and misplaced-product alerting using YOLOv8, ESP32-CAM image uploads, Cloudinary image hosting, email alerts, and PDF report exports.

## Features

- Real-time image upload endpoint for ESP32-CAM frames
- YOLOv8-based Campa and Sprite bottle detection
- Low-stock and misplaced-product alerts
- Cloudinary upload for annotated detection images
- Dashboard for latest detection status
- PDF stock trend and ML performance reports

## Project Structure

```text
app/
  routes/      Flask route handlers
  services/    Detection and storage helper modules
  models/      Model-related adapters and future model code
  utils/       Shared utilities
  templates/   Flask templates
  static/      Static dashboard assets and generated visual outputs
docs/          Architecture and project documentation
screenshots/   UI screenshots for README/demo material
sample_images/ Sample inputs for demos and testing
paper/         Research paper or project report assets
tests/         Automated tests
```

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Configure environment variables.

```bash
copy .env.example .env
```

4. Run the application.

```bash
python run.py
```

The dashboard runs at `http://127.0.0.1:5000`.

## API Endpoints

- `GET /` - dashboard
- `POST /upload` - upload a raw camera frame for detection
- `GET /latest` - latest detection result as JSON
- `GET /export-report` - stock trend PDF report
- `GET /export-ml-report` - ML performance PDF report

## Model Assets

The current application loads the YOLO model from:

```text
runs/detect/train/weights/best.pt
```

Keep this file in place or set `MODEL_PATH` in your environment.

## Security Note

Before publishing publicly, rotate any previously committed API keys or app passwords. Runtime secrets should be stored in `.env` or deployment environment variables, never in source control.

## License

This project is licensed under the MIT License.
