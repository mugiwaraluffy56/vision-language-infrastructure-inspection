"""
Rule-based severity assessment for detected defects.
Assigns Low, Medium, or High severity based on defect characteristics.
"""

from typing import Literal, Dict, Any
from PIL import Image
import numpy as np


SeverityLevel = Literal["Low", "Medium", "High"]


class SeverityAssessor:
    """
    Rule-based severity assessment for infrastructure defects.

    Uses deterministic rules based on:
    - Defect size (area and dimensions)
    - Defect type
    - Relative size compared to image
    """

    def assess_severity(
        self,
        defect_type: str,
        bbox: list[float],
        image: Image.Image,
        confidence: float
    ) -> tuple[SeverityLevel, str]:
        """
        Assess severity of a detected defect.

        Args:
            defect_type: Type of defect (crack, corrosion, spalling)
            bbox: Bounding box [x1, y1, x2, y2]
            image: Original image for size comparison
            confidence: Detection confidence score

        Returns:
            Tuple of (severity_level, reasoning)
        """
        # Calculate defect dimensions
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        area = width * height

        # Get image dimensions for relative sizing
        img_width, img_height = image.size
        img_area = img_width * img_height

        # Relative metrics
        relative_area = area / img_area
        aspect_ratio = max(width, height) / min(width, height)

        # Assess based on defect type
        defect_type_lower = defect_type.lower()

        if defect_type_lower == "crack":
            return self._assess_crack(relative_area, width, height, aspect_ratio, confidence)
        elif defect_type_lower == "corrosion":
            return self._assess_corrosion(relative_area, area, confidence)
        elif defect_type_lower == "spalling":
            return self._assess_spalling(relative_area, area, confidence)
        else:
            return "Medium", "Unknown defect type, defaulting to Medium severity"

    def _assess_crack(
        self,
        relative_area: float,
        width: float,
        height: float,
        aspect_ratio: float,
        confidence: float
    ) -> tuple[SeverityLevel, str]:
        """
        Assess crack severity based on length and extent.

        Rules:
        - High: Long cracks (high aspect ratio) or large relative area
        - Medium: Moderate length/area
        - Low: Small, localized cracks
        """
        max_dimension = max(width, height)

        # High severity: Long cracks or wide coverage
        if aspect_ratio > 8 and relative_area > 0.05:
            return "High", "Long crack with significant extent, potential structural concern"
        elif relative_area > 0.15:
            return "High", "Large crack covering substantial area, requires immediate attention"
        elif max_dimension > 300 and aspect_ratio > 5:
            return "High", "Extensive linear crack, may indicate structural movement"

        # Medium severity: Moderate cracks
        elif relative_area > 0.03 or (aspect_ratio > 4 and max_dimension > 150):
            return "Medium", "Moderate crack requiring monitoring and potential repair"
        elif confidence > 0.8 and relative_area > 0.01:
            return "Medium", "Clearly visible crack, should be assessed by engineer"

        # Low severity: Small cracks
        else:
            return "Low", "Small localized crack, likely superficial but should be documented"

    def _assess_corrosion(
        self,
        relative_area: float,
        area: float,
        confidence: float
    ) -> tuple[SeverityLevel, str]:
        """
        Assess corrosion severity based on area and extent.

        Rules:
        - High: Deep/widespread corrosion indicating material loss
        - Medium: Moderate surface corrosion
        - Low: Minor surface oxidation
        """
        # High severity: Extensive corrosion
        if relative_area > 0.12:
            return "High", "Extensive corrosion with likely material degradation, immediate assessment needed"
        elif area > 50000 and confidence > 0.7:
            return "High", "Large corroded area indicating advanced deterioration"

        # Medium severity: Moderate corrosion
        elif relative_area > 0.04:
            return "Medium", "Moderate corrosion present, risk of progression if untreated"
        elif area > 15000:
            return "Medium", "Significant corroded area requiring remediation planning"

        # Low severity: Surface-level corrosion
        else:
            return "Low", "Surface-level corrosion detected, monitor for progression"

    def _assess_spalling(
        self,
        relative_area: float,
        area: float,
        confidence: float
    ) -> tuple[SeverityLevel, str]:
        """
        Assess spalling severity based on area and depth indicators.

        Rules:
        - High: Large spalling potentially exposing reinforcement
        - Medium: Moderate surface loss
        - Low: Minor surface spalling
        """
        # High severity: Large spalling areas
        if relative_area > 0.10:
            return "High", "Extensive spalling, possible reinforcement exposure, structural integrity at risk"
        elif area > 40000 and confidence > 0.75:
            return "High", "Large spalled region indicating concrete deterioration, urgent repair required"

        # Medium severity: Moderate spalling
        elif relative_area > 0.03:
            return "Medium", "Moderate spalling with material loss, repair recommended"
        elif area > 10000:
            return "Medium", "Significant surface spalling, assess for underlying damage"

        # Low severity: Minor spalling
        else:
            return "Low", "Minor surface spalling detected, document and monitor"
