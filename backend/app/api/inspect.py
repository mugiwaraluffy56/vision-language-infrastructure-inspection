"""
FastAPI endpoint for infrastructure inspection.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from backend.app.schemas.inspection import InspectionResponse, ErrorResponse
from backend.app.services.inspection import InspectionService


router = APIRouter()

# Initialize inspection service (singleton)
inspection_service = None


def get_inspection_service() -> InspectionService:
    """Get or create inspection service instance."""
    global inspection_service
    if inspection_service is None:
        # Initialize with rule-based explanations by default (faster)
        # Set use_vlm=True to enable BLIP-2 (slower but more detailed)
        inspection_service = InspectionService(use_vlm=False)
    return inspection_service


@router.post(
    "/inspect",
    response_model=InspectionResponse,
    responses={
        200: {"model": InspectionResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Inspect infrastructure image for defects",
    description="""
    Upload an infrastructure image to detect and analyze structural defects.

    The system will:
    1. Detect defects (cracks, corrosion, spalling)
    2. Assess severity (Low, Medium, High)
    3. Generate engineering explanations
    4. Provide recommended actions

    Accepts: JPEG, PNG images
    Returns: Structured inspection report in JSON format
    """
)
async def inspect_image(
    file: UploadFile = File(..., description="Infrastructure image to inspect")
):
    """
    Perform structural defect inspection on uploaded image.

    Args:
        file: Uploaded image file (JPEG, PNG)

    Returns:
        InspectionResponse with detected defects and analysis
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Please upload an image file."
        )

    try:
        # Read image bytes
        image_bytes = await file.read()

        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded"
            )

        # Get inspection service
        service = get_inspection_service()

        # Perform inspection
        result = await service.inspect_image(image_bytes)

        return result

    except HTTPException:
        raise
    except Exception as e:
        # Log error in production
        print(f"Inspection error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Inspection failed: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check endpoint",
    description="Check if the inspection service is running and ready"
)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Infrastructure Inspection API",
        "version": "1.0.0"
    }
