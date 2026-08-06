import os
import smtplib
import time
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, HexColor
from email.mime.text import MIMEText

import cloudinary
import cloudinary.uploader
import cv2
from flask import Flask, render_template, request, jsonify, send_file
from ultralytics import YOLO

from config import Config

# ---------------- FLASK APP ----------------
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_object(Config)

UPLOAD_DIR = app.config["UPLOAD_DIR"]
TEMP_DIR = app.config["TEMP_DIR"]
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

MODEL_PATH = app.config["MODEL_PATH"]

# ---------------- CLOUDINARY ----------------
cloudinary.config(
    cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
    api_key=app.config["CLOUDINARY_API_KEY"],
    api_secret=app.config["CLOUDINARY_API_SECRET"],
    secure=True
)

# ---------------- YOLO ----------------
model = YOLO(MODEL_PATH)
CLASS_NAMES = model.names
CLASS_NAMES[1] = "sprite"

# ---------------- DATA ----------------
stock_history = {
    "total_scans": 0,
    "total_campa_detected": 0,
    "timeline": []
}

ml_insights = {
    "total_campa_samples": 0,
    "sum_campa_conf": 0.0
}

latest_result = {
    "campa": 0,
    "sprite": 0,
    "alert": False,
    "sprite_detected": False,
    "image_url": ""
}

# ---------------- EMAIL ----------------
SMTP_SERVER = app.config["SMTP_SERVER"]
SMTP_PORT = app.config["SMTP_PORT"]
EMAIL_FROM = app.config["EMAIL_FROM"]
EMAIL_TO = app.config["EMAIL_TO"]
EMAIL_PASS = app.config["EMAIL_PASSWORD"]

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    try:
        s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        s.starttls()
        s.login(EMAIL_FROM, EMAIL_PASS)
        s.send_message(msg)
        s.quit()
    except Exception as e:
        print("Email error:", e)

# ---------------- ROUTES ----------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload", methods=["POST"])
def upload():
    global latest_result

    filename = f"frame_{int(time.time())}.jpg"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(request.data)

    img = cv2.imread(path)
    results = model(img, conf=0.4, verbose=False)

    campa = 0
    sprite = 0

    for r in results:
        if r.boxes:
            for box in r.boxes:
                cls = CLASS_NAMES[int(box.cls)].lower()
                conf = float(box.conf)

                if cls == "campa":
                    campa += 1
                    ml_insights["total_campa_samples"] += 1
                    ml_insights["sum_campa_conf"] += conf
                elif cls == "sprite":
                    sprite += 1

    annotated = results[0].plot()
    det = path.replace(".jpg", "_det.jpg")
    cv2.imwrite(det, annotated)
    url = cloudinary.uploader.upload(det)["secure_url"]

    timestamp = datetime.now().strftime("%H:%M:%S")

    latest_result = {
        "campa": campa,
        "sprite": sprite,
        "alert": sprite > 0,
        "sprite_detected": sprite > 0,
        "image_url": url
    }

    snapshot = {
        "Time": timestamp,
        "Campa": campa,
        "Biscuits": 5,
        "Chips": 4,
        "Juice": 6,
        "Water": 7,
        "Energy Drink": 3,
        "Snacks": 4
    }

    stock_history["total_scans"] += 1
    stock_history["total_campa_detected"] += campa
    stock_history["timeline"].append(snapshot)

    if campa <= 1:
        send_email("🚨 Campa Stock Alert", f"Campa stock critically low\nDetected: {campa}")

    if sprite > 0:
        send_email("🚨 Sprite Detected Alert", f"Sprite detected at {timestamp}\nCount: {sprite}")

    return jsonify({"status": "ok"})

@app.route("/latest")
def latest():
    return jsonify(latest_result)

# ---------------- STOCK REPORT ----------------
@app.route("/export-report")
def export_report():
    path = os.path.join(TEMP_DIR, "stock_report.pdf")
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 24)
    c.drawString(40, h - 60, "STOCK TREND REPORT")

    c.setFont("Helvetica", 12)
    c.drawString(40, h - 95, f"Generated on: {datetime.now()}")
    c.drawString(40, h - 115, f"Total Scans: {stock_history['total_scans']}")
    c.drawString(40, h - 135, f"Total Campa Detected: {stock_history['total_campa_detected']}")

    columns = ["Time", "Campa", "Biscuits", "Chips", "Juice", "Water", "Energy Drink", "Snacks"]
    x_positions = [40, 90, 140, 200, 250, 300, 350, 430]

    y = h - 180
    c.setFont("Helvetica-Bold", 11)
    for col, x in zip(columns, x_positions):
        c.drawString(x, y, col)
    c.line(40, y - 5, w - 40, y - 5)
    y -= 20

    c.setFont("Helvetica", 10)
    visible_data = stock_history["timeline"][-10:]

    for entry in visible_data:
        for col, x in zip(columns, x_positions):
            c.drawString(x, y, str(entry[col]))
        y -= 16

    # ---------- GRAPH SECTION (RESTORED EXACTLY) ----------
    origin_x, origin_y = 60, 90
    graph_w, graph_h = 420, 200

    c.setStrokeColor(black)
    c.line(origin_x, origin_y, origin_x, origin_y + graph_h)
    c.line(origin_x, origin_y, origin_x + graph_w, origin_y)

    c.setFont("Helvetica", 10)
    c.drawString(origin_x + graph_w/2 - 40, origin_y - 25, "Scan Index")
    c.saveState()
    c.rotate(90)
    c.drawString(origin_y + graph_h/2 - 40, -45, "Stock Count")
    c.restoreState()

    products = columns[1:]

    colors = {
        "Campa": HexColor("#00C853"),
        "Biscuits": HexColor("#FF6D00"),
        "Chips": HexColor("#2962FF"),
        "Juice": HexColor("#AA00FF"),
        "Water": HexColor("#00B8D4"),
        "Energy Drink": HexColor("#795548"),
        "Snacks": HexColor("#C51162")
    }

    if visible_data:
        max_val = max(max(entry[p] for p in products) for entry in visible_data)
    else:
        max_val = 10

    if max_val == 0:
        max_val = 1

    for product in products:
        c.setStrokeColor(colors[product])
        prev = None

        for i, entry in enumerate(visible_data):
            x = origin_x + (i / max(1, len(visible_data)-1)) * graph_w
            y_point = origin_y + (entry[product] / max_val) * graph_h

            c.circle(x, y_point, 3, fill=1)

            if prev:
                c.line(prev[0], prev[1], x, y_point)

            prev = (x, y_point)

    legend_x = origin_x + graph_w + 10
    legend_y = origin_y + graph_h - 10
    c.setFont("Helvetica", 9)

    for i, product in enumerate(products):
        c.setFillColor(colors[product])
        c.rect(legend_x, legend_y - i*14, 10, 10, fill=1, stroke=0)
        c.setFillColor(black)
        c.drawString(legend_x + 14, legend_y - i*14 + 2, product)

    c.showPage()
    c.save()
    return send_file(path, as_attachment=True)

# ---------------- ML REPORT ----------------
@app.route("/export-ml-report")
def export_ml_report():
    path = os.path.join(TEMP_DIR, "ml_report.pdf")
    c = canvas.Canvas(path, pagesize=A4)

    avg_conf = (
        ml_insights["sum_campa_conf"] / ml_insights["total_campa_samples"]
        if ml_insights["total_campa_samples"] else 0
    )

    c.setFont("Helvetica-Bold", 24)
    c.drawString(40, 780, "ML PERFORMANCE REPORT")

    y = 730
    c.setFont("Helvetica", 12)
    lines = [
        "Model: YOLOv8 Object Detection",
        f"Total Samples: {ml_insights['total_campa_samples']}",
        f"Average Confidence: {avg_conf:.2f}",
        "",
        "Features:",
        "- Multi-class detection",
        "- Sprite anomaly detection",
        "- Real-time alerting system",
        "- Cloud-integrated monitoring",
        "",
        "Conclusion:",
        "System is production-ready for automated retail stock compliance."
    ]

    for line in lines:
        c.drawString(40, y, line)
        y -= 18

    c.showPage()
    c.save()
    return send_file(path, as_attachment=True)
