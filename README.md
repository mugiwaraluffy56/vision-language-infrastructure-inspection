# Infrastructure Inspection System

AI-powered infrastructure defect detection and analysis system using computer vision and vision-language models.

## Overview

This system performs automated structural defect inspection on infrastructure images, detecting cracks, corrosion, and spalling with severity assessment and engineering-grade explanations.

### Key Features

- **Defect Detection**: YOLOv8-based detection of three defect types (crack, corrosion, spalling)
- **Severity Assessment**: Rule-based severity classification (Low, Medium, High)
- **Engineering Analysis**: Professional explanations and recommended actions
- **Clean Web Interface**: Minimal, modern React frontend
- **RESTful API**: FastAPI backend with automatic documentation

## System Architecture

```
Image Upload
    ↓
YOLOv8 Defect Detection
    ↓
Rule-Based Severity Assessment
    ↓
Vision-Language Explanation (Optional)
    ↓
Structured JSON Report
```

## Tech Stack

### Backend
- **Framework**: FastAPI
- **ML Framework**: PyTorch
- **Object Detection**: YOLOv8 (Ultralytics)
- **Vision-Language Model**: BLIP-2 (optional, rule-based by default)
- **Language**: Python 3.9+

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Pure CSS
- **HTTP Client**: Axios

## Project Structure

```
mhack/
├── backend/
│   └── app/
│       ├── api/
│       │   └── inspect.py          # API endpoints
│       ├── models/
│       │   ├── detector.py         # YOLOv8 detector
│       │   ├── severity.py         # Severity assessment
│       │   └── vlm.py              # Vision-Language Model
│       ├── schemas/
│       │   └── inspection.py       # Pydantic schemas
│       ├── services/
│       │   └── inspection.py       # Orchestration service
│       └── main.py                 # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.jsx     # Image upload component
│   │   │   └── InspectionReport.jsx # Report display
│   │   ├── App.jsx                 # Main app component
│   │   └── main.jsx                # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── models/                         # Model weights directory
├── data/                           # Sample images directory
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- pip and npm

### Backend Setup

1. **Navigate to project directory**:
```bash
cd mhack
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
# or with pip3
pip3 install -r requirements.txt
```

3. **YOLOv8 weights**:
The system will automatically download YOLOv8n weights on first startup.

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

## Running the Application

### Method 1: Using Run Scripts (Recommended)

**Start Backend:**
```bash
python3 run_backend.py
```

**Start Frontend** (in a new terminal):
```bash
./run_frontend.sh
```

### Method 2: Manual Start

**Start Backend Server:**

From the project root directory:
```bash
python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will start on `http://localhost:8000`

- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

**Start Frontend Development Server:**

In a new terminal, from the `frontend` directory:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

### Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

## Usage

### Web Interface

1. Open the application in your browser
2. Click or drag-and-drop an infrastructure image
3. Click "Analyze Image"
4. View the inspection report with detected defects

### API Usage

#### Inspect Image Endpoint

```bash
POST /api/inspect
```

**Request:**
```bash
curl -X POST "http://localhost:8000/api/inspect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/image.jpg"
```

**Response:**
```json
{
  "status": "success",
  "total_defects": 1,
  "summary": "Inspection completed. 1 defect detected...",
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
      "explanation": "Significant linear discontinuity detected...",
      "recommended_action": "Conduct detailed structural evaluation..."
    }
  ]
}
```

#### Health Check

```bash
GET /api/health
```

Returns service status.

## Configuration

### Enable Vision-Language Model

By default, the system uses fast rule-based explanations. To enable BLIP-2 VLM:

Edit `backend/app/api/inspect.py`:
```python
inspection_service = InspectionService(use_vlm=True)
```

**Note**: VLM requires significant memory and is slower. Recommended only for detailed analysis.

### Adjust Detection Confidence

Edit `backend/app/models/detector.py`:
```python
def __init__(self, model_path: str = None, confidence_threshold: float = 0.25):
```

Lower threshold = more detections (may include false positives)
Higher threshold = fewer detections (higher precision)

## Severity Assessment Rules

### Crack
- **High**: Long cracks, large relative area, high aspect ratio
- **Medium**: Moderate length/area, clear visibility
- **Low**: Small, localized cracks

### Corrosion
- **High**: Extensive area (>12% of image), deep material loss
- **Medium**: Moderate surface corrosion (4-12%)
- **Low**: Surface-level oxidation (<4%)

### Spalling
- **High**: Large spalling (>10%), potential reinforcement exposure
- **Medium**: Moderate surface loss (3-10%)
- **Low**: Minor surface spalling (<3%)

## Development

### Run Tests

```bash
# Backend tests (if available)
pytest

# Frontend tests
cd frontend
npm test
```

### Build for Production

**Backend:**
```bash
# Backend runs with uvicorn in production mode
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Limitations & Notes

### MVP Scope
- Single image processing (no video support)
- Three defect types only (crack, corrosion, spalling)
- No database persistence
- No user authentication
- Local deployment only

### Model Notes
- Uses pretrained YOLOv8n as placeholder
- Production deployment requires training on defect-specific dataset
- Rule-based severity is deterministic and configurable
- VLM explanations are optional (slower but more detailed)

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (requires 3.9+)
- Ensure virtual environment is activated
- Verify all dependencies installed: `pip install -r requirements.txt`

### Frontend won't start
- Check Node version: `node --version` (requires 18+)
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check if port 3000 is available

### Model download fails
- Check internet connection
- YOLOv8 downloads automatically from Ultralytics on first run
- Manually download from: https://github.com/ultralytics/assets/releases

### CORS errors
- Ensure backend is running on port 8000
- Check Vite proxy configuration in `frontend/vite.config.js`

## Future Enhancements

- [ ] Train custom YOLOv8 model on infrastructure defect dataset
- [ ] Add more defect types (delamination, efflorescence, etc.)
- [ ] Support batch image processing
- [ ] Database integration for report storage
- [ ] User authentication and project management
- [ ] Export reports as PDF
- [ ] Mobile app integration
- [ ] Real-time video analysis

## License

This project is an MVP for educational and demonstration purposes.

## Contact

For questions or issues, please refer to the project documentation.

---

**Built with:**
- FastAPI
- PyTorch
- YOLOv8
- React
- Vite

**Developed for infrastructure safety and inspection automation**
