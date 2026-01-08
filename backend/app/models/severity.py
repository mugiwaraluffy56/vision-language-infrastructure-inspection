from typing import Dict, List, Any

class SeverityEstimator:
    @staticmethod
    def estimate_severity(detection: Dict[str, Any], image_width: int, image_height: int) -> str:
        """
        Estimate severity based on bounding box size and type.
        Rules:
          - Crack: 
            - Length (max dim) < 10% image dim -> Low
            - Length < 30% -> Medium
            - Length >= 30% -> High
          - Corrosion:
            - Area < 5% -> Low
            - Area < 15% -> Medium
            - Area >= 15% -> High
          - Spalling:
            - Area < 5% -> Medium
            - Area >= 5% -> High
        """
        label = detection.get("label", "").lower()
        box = detection.get("box", [0, 0, 0, 0])
        x1, y1, x2, y2 = box
        
        width = x2 - x1
        height = y2 - y1
        area = width * height
        image_area = image_width * image_height
        max_dim = max(width, height)
        max_image_dim = max(image_width, image_height)
        
        # Avoid division by zero
        if image_area == 0:
            return "Unknown"

        rel_area = area / image_area
        rel_len = max_dim / max_image_dim

        if label == "crack":
            if rel_len < 0.10:
                return "Low"
            elif rel_len < 0.30:
                return "Medium"
            else:
                return "High"
        
        elif label == "corrosion":
            if rel_area < 0.05:
                return "Low"
            elif rel_area < 0.15:
                return "Medium"
            else:
                return "High"
        
        elif label == "spalling":
            if rel_area < 0.05:
                return "Medium"
            else:
                return "High"
        
        return "Low" # Default
