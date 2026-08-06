from ultralytics import YOLO
import tempfile
import requests

model = YOLO("bottle_detector/weights/best.pt")

def detect_from_url(image_url):
    # Download image temporarily
    response = requests.get(image_url)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_file.write(response.content)
    temp_file.close()

    results = model(temp_file.name, conf=0.5)

    campa = 0
    non_campa = 0

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id].lower()

            if label == "campa":
                campa += 1
            else:
                non_campa += 1

    return campa, non_campa
    return campa_count, non_campa_count