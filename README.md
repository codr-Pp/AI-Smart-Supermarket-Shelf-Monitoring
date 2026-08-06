# AI-Powered Smart Supermarket Shelf Monitoring & Inventory Auditing System

An AI-powered inventory monitoring system that automates supermarket shelf auditing using **ESP32-CAM**, **YOLOv8**, and **Flask**. The system captures shelf images, detects products in real time, monitors stock availability, identifies misplaced items, and provides inventory insights through an interactive dashboard.

## Features

- Real-time shelf image capture using ESP32-CAM
- Product detection using a custom-trained YOLOv8 model
- Automated inventory monitoring and stock counting
- Misplaced product detection
- Low-stock email alerts
- Annotated image storage using Cloudinary
- Interactive Flask dashboard
- PDF report generation for inventory and model performance

## Tech Stack

- Python
- Flask
- YOLOv8
- OpenCV
- ESP32-CAM
- Cloudinary
- HTML, CSS & JavaScript

## Project Structure

```text
app/
  routes/
  services/
  models/
  utils/
  templates/
  static/

docs/
firmware/
paper/
screenshots/
sample_images/
tests/

run.py
requirements.txt
README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Smart-Supermarket-Shelf-Monitoring.git
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and update the required credentials.

### 4. Run the application

```bash
python run.py
```

Open:

```
http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| POST | `/upload` | Upload shelf image |
| GET | `/latest` | Latest detection result |
| GET | `/export-report` | Inventory report |
| GET | `/export-ml-report` | ML performance report |

## Model

The application uses a custom-trained YOLOv8 model located at:

```
runs/detect/train/weights/best.pt
```

Update `MODEL_PATH` if the model is stored elsewhere.

## Future Improvements

- Cloud deployment
- Multi-camera support
- Barcode integration
- Mobile notifications
- Inventory analytics dashboard

## License

This project is licensed under the MIT License.
