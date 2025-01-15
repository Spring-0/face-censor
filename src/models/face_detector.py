from ultralytics import YOLO
from .base import DetectionModel

class YOLOFaceDetector(DetectionModel):
    def __init__(self, model_path="src/data/models/face_detection_model.pt"):
        self.model = YOLO(model_path)
        
    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]
        detections = []
        
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = box.conf[0].cpu().numpy()
            detections.append([int(x1), int(y1), int(x2), int(y2), conf])
        return detections