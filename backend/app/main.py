"""
FastAPI main application for Infrastructure Inspection System.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.inspect import router as inspect_router


# Create FastAPI application
app = FastAPI(
    title="Infrastructure Inspection API",
    description="""
    Vision-Language Based Infrastructure Inspection System

    Detects and analyzes structural defects in infrastructure images:
    - Crack detection and analysis
    - Corrosion assessment
    - Spalling identification

    Uses YOLOv8 for detection and rule-based engineering analysis
    to generate professional inspection reports.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(inspect_router, prefix="/api", tags=["Inspection"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Infrastructure Inspection API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "inspect": "POST /api/inspect - Upload image for inspection",
            "health": "GET /api/health - Health check"
        }
    }


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("Infrastructure Inspection System - Starting Server")
    print("=" * 60)

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
