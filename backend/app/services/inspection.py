from typing import List
from PIL import Image
import io
import time

from backend.app.models.detector import Detector
from backend.app.models.severity import SeverityEstimator
from backend.app.models.vlm import VLMClient
from backend.app.schemas.inspection import DefectResult, InspectionResponse

class InspectionService:
    def __init__(self):
        # Initialize models once
        self.detector = Detector() # defaults to yolov8n.pt
        self.severity_estimator = SeverityEstimator()
        self.vlm_client = VLMClient() 

    async def process_image(self, image_bytes: bytes, filename: str) -> InspectionResponse:
        # Load image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        width, height = image.size
        
        # Save temp file for YOLO (needs path usually, or we can adapt Det class)
        # Ultralytics can accept PIL image directly
        
        # 1. Detect
        # The detector wrapper was written to take a path, let's adjust it to take PIL or just save tmp.
        # Saving tmp is safer for consistency.
        tmp_path = f"data/{filename}_{int(time.time())}.jpg"
        image.save(tmp_path)
        
        detections = self.detector.detect(tmp_path)
        
        defect_results = []
        
        for det in detections:
            # 2. Estimate Severity
            severity = self.severity_estimator.estimate_severity(det, width, height)
            
            # 3. Crop for VLM
            x1, y1, x2, y2 = det["box"]
            # Add some padding?
            crop = image.crop((x1, y1, x2, y2))
            
            # 4. Generate Explanation
            explanation_text = self.vlm_client.generate_explanation(crop, det["label"], severity)
            
            # 5. Extract Reccomendation (simple splitting or prompt engineering)
            # For MVP, we pass the whole text as explanation and a generic action or split if possible.
            # The prompt asked for "risk and recommended action". 
            # We'll split simply if possible or put all in explanation.
            
            rec_action = "Inspect and repair per code."
            risk_explanation = explanation_text
            
            if "Recommendation:" in explanation_text:
                parts = explanation_text.split("Recommendation:")
                risk_explanation = parts[0].strip()
                rec_action = parts[1].strip()
            
            defect_results.append(DefectResult(
                defect_type=det["label"],
                bounding_box=det["box"],
                severity=severity,
                explanation=risk_explanation,
                recommended_action=rec_action
            ))
            
        return InspectionResponse(
            filename=filename,
            defects=defect_results
        )

# Global instance
inspection_service = InspectionService()
