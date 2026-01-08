"""
Inspection service orchestrating the complete defect detection pipeline.

Pipeline:
1. Image Input
2. YOLOv8 Defect Detection
3. Rule-based Severity Assessment
4. Vision-Language Model Explanation
5. Structured Report Generation
"""

from typing import List, Dict, Any
from PIL import Image
import io

from backend.app.models.detector import DefectDetector
from backend.app.models.severity import SeverityAssessor
from backend.app.models.vlm import VisionLanguageModel
from backend.app.schemas.inspection import (
    InspectionResponse,
    DefectDetection,
    BoundingBox
)


class InspectionService:
    """
    Orchestrates the end-to-end infrastructure inspection pipeline.
    """

    def __init__(
        self,
        detector_model_path: str = None,
        use_vlm: bool = False,
        vlm_model_name: str = "Salesforce/blip2-opt-2.7b"
    ):
        """
        Initialize the inspection service.

        Args:
            detector_model_path: Path to YOLOv8 model weights
            use_vlm: Whether to use Vision-Language Model (slower but more detailed)
            vlm_model_name: BLIP-2 model identifier
        """
        print("Initializing Inspection Service...")

        # Initialize detector
        self.detector = DefectDetector(model_path=detector_model_path)
        print("✓ Defect detector loaded")

        # Initialize severity assessor
        self.severity_assessor = SeverityAssessor()
        print("✓ Severity assessor initialized")

        # Initialize VLM if requested
        self.use_vlm = use_vlm
        if use_vlm:
            self.vlm = VisionLanguageModel(model_name=vlm_model_name)
            print("✓ Vision-Language Model loaded")
        else:
            self.vlm = VisionLanguageModel.__new__(VisionLanguageModel)
            print("✓ Using rule-based explanations (faster)")

        print("Inspection Service ready\n")

    async def inspect_image(self, image_bytes: bytes) -> InspectionResponse:
        """
        Perform complete inspection on an uploaded image.

        Args:
            image_bytes: Raw image bytes from upload

        Returns:
            InspectionResponse with all detected defects and analysis
        """
        # Load image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Step 1: Detect defects
        detections = self.detector.detect(image)

        if not detections:
            return InspectionResponse(
                status="success",
                detections=[],
                total_defects=0,
                summary="Inspection completed. No defects detected."
            )

        # Step 2-4: Process each detection
        processed_detections = []

        for detection in detections:
            processed = await self._process_detection(detection, image)
            processed_detections.append(processed)

        # Generate summary
        summary = self._generate_summary(processed_detections)

        return InspectionResponse(
            status="success",
            detections=processed_detections,
            total_defects=len(processed_detections),
            summary=summary
        )

    async def _process_detection(
        self,
        detection: Dict[str, Any],
        image: Image.Image
    ) -> DefectDetection:
        """
        Process a single detection through severity assessment and explanation.

        Args:
            detection: Raw detection from YOLOv8
            image: Original image

        Returns:
            Complete DefectDetection with all analysis
        """
        defect_type = detection["class_name"]
        bbox = detection["bbox"]
        confidence = detection["confidence"]

        # Step 2: Assess severity
        severity, severity_reasoning = self.severity_assessor.assess_severity(
            defect_type=defect_type,
            bbox=bbox,
            image=image,
            confidence=confidence
        )

        # Step 3: Generate explanation
        if self.use_vlm:
            # Crop defect region for VLM
            cropped_image = self.detector.crop_defect_region(image, bbox)

            # Generate VLM explanation
            vlm_output = self.vlm.generate_explanation(
                image=cropped_image,
                defect_type=defect_type,
                severity=severity
            )
            explanation = vlm_output["explanation"]
            recommended_action = vlm_output["recommended_action"]
        else:
            # Use rule-based explanation (faster, production-ready)
            simple_output = self.vlm.generate_simple_explanation(
                defect_type=defect_type,
                severity=severity
            )
            explanation = simple_output["explanation"]
            recommended_action = simple_output["recommended_action"]

        # Create structured response
        return DefectDetection(
            defect_type=defect_type,
            confidence=round(confidence, 3),
            severity=severity,
            severity_reasoning=severity_reasoning,
            bounding_box=BoundingBox(
                x1=bbox[0],
                y1=bbox[1],
                x2=bbox[2],
                y2=bbox[3]
            ),
            explanation=explanation,
            recommended_action=recommended_action
        )

    def _generate_summary(self, detections: List[DefectDetection]) -> str:
        """
        Generate overall inspection summary.

        Args:
            detections: List of processed detections

        Returns:
            Summary string
        """
        total = len(detections)

        if total == 0:
            return "Inspection completed. No defects detected."

        # Count by severity
        severity_counts = {"High": 0, "Medium": 0, "Low": 0}
        defect_counts = {}

        for detection in detections:
            severity_counts[detection.severity] += 1
            defect_type = detection.defect_type.capitalize()
            defect_counts[defect_type] = defect_counts.get(defect_type, 0) + 1

        # Build summary
        summary_parts = [f"Inspection completed. {total} defect{'s' if total > 1 else ''} detected."]

        # Add defect type breakdown
        defect_list = [f"{count} {dtype}{'s' if count > 1 else ''}"
                       for dtype, count in defect_counts.items()]
        summary_parts.append(f"Types: {', '.join(defect_list)}.")

        # Add severity breakdown
        severity_list = []
        for severity in ["High", "Medium", "Low"]:
            count = severity_counts[severity]
            if count > 0:
                severity_list.append(f"{count} {severity}")

        if severity_list:
            summary_parts.append(f"Severity: {', '.join(severity_list)}.")

        # Add urgency note if high severity present
        if severity_counts["High"] > 0:
            summary_parts.append("Immediate engineering assessment recommended for high severity defects.")

        return " ".join(summary_parts)
