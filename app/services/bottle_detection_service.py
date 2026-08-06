from ultralytics import YOLO

# Load model once
model = YOLO("yolov8n.pt")

# Class mapping
CLASS_NAMES = {
    0: "campa",
    1: "other"
}

def detect_bottles(image_path):
    results = model(image_path)

    campa_count = 0
    other_count = 0

    for box in results[0].boxes:
        cls = int(box.cls[0])
        if cls == 0:
            campa_count += 1
        elif cls == 1:
            other_count += 1

    # Decision logic
    if other_count > 0:
        status = "MISPLACED BOTTLE"
        alert = "RED"
    elif campa_count <= 1:
        status = "LOW STOCK"
        alert = "ORANGE"
    else:
        status = "STOCK OK"
        alert = "GREEN"

    return {
        "campa": campa_count,
        "other": other_count,
        "status": status,
        "alert": alert
    }