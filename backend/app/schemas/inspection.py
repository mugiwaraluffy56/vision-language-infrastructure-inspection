from pydantic import BaseModel
from typing import List, Optional

class InspectionRequest(BaseModel):
    # For file uploads, we don't strictly need a Pydantic model for the body 
    # if we use UploadFile, but good to have for reference.
    pass

class DefectResult(BaseModel):
    defect_type: str
    bounding_box: List[float] # [x1, y1, x2, y2]
    severity: str
    explanation: str
    recommended_action: str

class InspectionResponse(BaseModel):
    filename: str
    defects: List[DefectResult]
