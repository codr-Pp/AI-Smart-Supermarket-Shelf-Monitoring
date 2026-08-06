from app.services.bottle_detector.yolo_detector import detect

def analyze_image(image_path):
    campa_count, non_campa_count = detect(image_path)

    alert = False
    if campa_count <= 1:
        alert = True

    return {
        "campa_count": campa_count,
        "non_campa_count": non_campa_count,
        "alert": alert
    }
