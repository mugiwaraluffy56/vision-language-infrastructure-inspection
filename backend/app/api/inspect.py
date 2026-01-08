from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.services.inspection import inspection_service
from backend.app.schemas.inspection import InspectionResponse

router = APIRouter()

@router.post("/inspect", response_model=InspectionResponse)
async def inspect_image(file: UploadFile = File(...)):
    """
    Endpoint to inspect an infrastructure image.
    Accepts an image file, runs detection and VLM analysis,
    and returns a structured JSON report.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    contents = await file.read()
    
    try:
        response = await inspection_service.process_image(contents, file.filename)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
