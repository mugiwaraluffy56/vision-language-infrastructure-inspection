from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.inspect import router as inspect_router
import uvicorn

app = FastAPI(
    title="Vision-Language Infrastructure Inspection",
    description="MVP for detecting structural defects and generating engineering explanations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP, allow all. In prod, lock down to frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inspect_router, tags=["Inspection"])

@app.get("/")
def read_root():
    return {"message": "Infrastructure Inspection API is running. POST to /inspect to analyze images."}

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
