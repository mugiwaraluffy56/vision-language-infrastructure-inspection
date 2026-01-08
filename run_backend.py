#!/usr/bin/env python3
"""
Simple backend server runner script.
Starts the FastAPI application on http://localhost:8000
"""

import uvicorn
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    print("=" * 60)
    print("Infrastructure Inspection System - Backend")
    print("=" * 60)
    print("\nStarting FastAPI server...")
    print("API will be available at: http://localhost:8000")
    print("Documentation at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
