from ultralytics import YOLO
from typing import List, Dict, Any
import numpy as np

class Detector:
    def __init__(self, model_path: str = "yolov8n.pt"):
        """
        Initialize the YOLOv8 detector.
        Args:
            model_path: Path to the YOLOv8 weights file.
                        Defaults to 'yolov8n.pt' (nano) for MVP which will auto-download.
        """
        self.model = YOLO(model_path)
        # Class mapping to ensure we stick to the 3 requested defect types
        # This is a bit of a hack for the MVP if we use standard weights,
        # but if we had a custom trained model, these indices would match.
        # For demonstration with standard COCO weights, we might not find 'crack', 'corrosion', 'spalling'.
        # So we will mock the return if it's standard weights, or expect the model to be trained.
        # ALLOWANCE: User said "Load pretrained weights (mock weights acceptable for MVP)"
        self.mock_mode = "yolov8" in model_path and "seg" not in model_path and "cls" not in model_path

    def detect(self, image_path: str, conf_threshold: float = 0.25) -> List[Dict[str, Any]]:
        """
        Run detection on an image.
        """
        results = self.model(image_path, conf=conf_threshold)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = box.conf[0].item()
                cls_id = int(box.cls[0].item())
                
                # In a real scenario, we map cls_id to 'crack', 'corrosion', 'spalling'.
                # For this MVP with generic weights, we might get random COCO classes.
                # We will FORCE map them for demonstration if it's not a custom model.
                if self.mock_mode:
                    # Randomly assign a defect type based on hash of coordinates for determinism
                    label_idx = int((x1 + y1) % 3)
                    labels = ["crack", "corrosion", "spalling"]
                    label = labels[label_idx]
                else:
                    label = self.model.names[cls_id]
                
                if label not in ["crack", "corrosion", "spalling"]:
                     # Fallback for generic models to valid types
                     label_idx = int((x1 + y1) % 3)
                     labels = ["crack", "corrosion", "spalling"]
                     label = labels[label_idx]

                detections.append({
                    "box": [float(x1), float(y1), float(x2), float(y2)],
                    "label": label,
                    "confidence": float(confidence)
                })
        
        return detections
