"""
Pydantic schemas for inspection API request and response models.
"""

from pydantic import BaseModel, Field
from typing import List, Literal


SeverityLevel = Literal["Low", "Medium", "High"]


class BoundingBox(BaseModel):
    """Bounding box coordinates."""
    x1: float = Field(..., description="Top-left x coordinate")
    y1: float = Field(..., description="Top-left y coordinate")
    x2: float = Field(..., description="Bottom-right x coordinate")
    y2: float = Field(..., description="Bottom-right y coordinate")


class DefectDetection(BaseModel):
    """Single defect detection result."""
    defect_type: str = Field(..., description="Type of defect (crack, corrosion, spalling)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")
    severity: SeverityLevel = Field(..., description="Severity level")
    severity_reasoning: str = Field(..., description="Explanation for severity assessment")
    bounding_box: BoundingBox = Field(..., description="Defect location")
    explanation: str = Field(..., description="Engineering explanation of the defect")
    recommended_action: str = Field(..., description="Recommended maintenance or repair action")


class InspectionResponse(BaseModel):
    """Complete inspection report response."""
    status: str = Field(default="success", description="Inspection status")
    detections: List[DefectDetection] = Field(..., description="List of detected defects")
    total_defects: int = Field(..., description="Total number of defects detected")
    summary: str = Field(..., description="Overall inspection summary")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "total_defects": 1,
                "summary": "Inspection completed. 1 defect detected.",
                "detections": [
                    {
                        "defect_type": "crack",
                        "confidence": 0.89,
                        "severity": "High",
                        "severity_reasoning": "Long crack with significant extent",
                        "bounding_box": {
                            "x1": 120.5,
                            "y1": 80.3,
                            "x2": 450.2,
                            "y2": 95.7
                        },
                        "explanation": "Significant linear discontinuity detected in structural element...",
                        "recommended_action": "Conduct detailed structural evaluation including load capacity analysis..."
                    }
                ]
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    status: str = Field(default="error")
    message: str = Field(..., description="Error message")
    detail: str = Field(default="", description="Detailed error information")
