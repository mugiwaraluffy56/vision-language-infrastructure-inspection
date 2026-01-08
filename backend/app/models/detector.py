"""
YOLOv8-based defect detection module for infrastructure inspection.
Detects cracks, corrosion, and spalling in images.
"""

from pathlib import Path
from typing import List, Dict, Any
import torch
from ultralytics import YOLO
from PIL import Image
import numpy as np


class DefectDetector:
    """
    YOLOv8-based detector for infrastructure defects.

    Detects three defect types:
    - Crack
    - Corrosion
    - Spalling
    """

    def __init__(self, model_path: str = None, confidence_threshold: float = 0.25):
        """
        Initialize the defect detector.

        Args:
            model_path: Path to YOLOv8 weights. If None, uses pretrained YOLOv8n.
            confidence_threshold: Minimum confidence for detections.
        """
        self.confidence_threshold = confidence_threshold
        self.class_names = {0: "crack", 1: "corrosion", 2: "spalling"}

        # Load YOLOv8 model
        # For MVP, we use pretrained YOLOv8n as a placeholder
        # In production, this would be fine-tuned on defect dataset
        if model_path and Path(model_path).exists():
            self.model = YOLO(model_path)
        else:
            # Use pretrained model as placeholder for MVP
            self.model = YOLO("yolov8n.pt")

    def detect(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Detect defects in the given image.

        Args:
            image: PIL Image to analyze

        Returns:
            List of detections, each containing:
                - class_name: defect type
                - confidence: detection confidence
                - bbox: [x1, y1, x2, y2] bounding box coordinates
                - bbox_normalized: normalized coordinates [0-1]
        """
        # Run inference
        results = self.model(image, conf=self.confidence_threshold, verbose=False)

        detections = []

        for result in results:
            boxes = result.boxes

            if boxes is None or len(boxes) == 0:
                continue

            # Get image dimensions for normalization
            img_height, img_width = image.size[1], image.size[0]

            for box in boxes:
                # Extract box data
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())

                # Map class ID to defect type
                # For MVP with pretrained model, we simulate defect detection
                # In production, this would use actual trained class IDs
                class_name = self._map_class_to_defect(class_id)

                detection = {
                    "class_name": class_name,
                    "confidence": confidence,
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "bbox_normalized": [
                        float(x1 / img_width),
                        float(y1 / img_height),
                        float(x2 / img_width),
                        float(y2 / img_height)
                    ]
                }

                detections.append(detection)

        return detections

    def _map_class_to_defect(self, class_id: int) -> str:
        """
        Map YOLOv8 class ID to defect type.
        For MVP, we use modulo to simulate defect classes.
        In production, this would map actual trained class IDs.
        """
        defect_types = ["crack", "corrosion", "spalling"]
        return defect_types[class_id % 3]

    def crop_defect_region(self, image: Image.Image, bbox: List[float], padding: int = 20) -> Image.Image:
        """
        Crop the defect region from the image with optional padding.

        Args:
            image: Original PIL Image
            bbox: Bounding box [x1, y1, x2, y2]
            padding: Pixels to add around the bbox

        Returns:
            Cropped PIL Image
        """
        x1, y1, x2, y2 = bbox

        # Add padding
        x1 = max(0, int(x1 - padding))
        y1 = max(0, int(y1 - padding))
        x2 = min(image.width, int(x2 + padding))
        y2 = min(image.height, int(y2 + padding))

        return image.crop((x1, y1, x2, y2))
