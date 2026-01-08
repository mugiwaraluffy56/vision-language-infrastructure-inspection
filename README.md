# Vision-Language Infrastructure Inspection System (MVP)

An AI-powered system that detects structural defects (Crack, Corrosion, Spalling) in infrastructure images and generates engineering-grade risk assessments using a Vision-Language Model.

## Features
- **Defect Detection**: Identifies cracks, corrosion, and spalling using YOLOv8.
- **Severity Assessment**: Logic-based severity classification (Low, Medium, High).
- **Automated Explanations**: Generates natural language risk explanations using BLIP-2 VLM.
- **Structured Output**: Returns a detailed JSON report.

## Tech Stack
- **Language**: Python
- **Backend Framework**: FastAPI
- **ML Models**: YOLOv8 (Detection), Salesforce/BLIP-2 (VLM)
- **Containerization**: (Optional) Docker ready

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server**
   ```bash
   uvicorn backend.app.main:app --reload
   ```

3. **Inspect an Image**
   ```bash
   curl -X POST -F "file=@path/to/image.jpg" http://localhost:8000/inspect
   ```

## API Endpoint
**POST /inspect**
- **Input**: `file` (Multipart form-data, image)
- **Output**: JSON object with detected defects, severity, and explanations.

## Example Output
```json
{
  "filename": "bridge_crack.jpg",
  "defects": [
    {
      "defect_type": "crack",
      "bounding_box": [100, 200, 150, 400],
      "severity": "High",
      "explanation": "Detected High severity crack. Structural integrity may be compromised...",
      "recommended_action": "Inspect and repair per code."
    }
  ]
}
```

## Note on Models
- **YOLOv8**: Uses standard weights. For strict classification of "Crack/Corrosion/Spalling", a custom trained model is recommended. In this MVP, we map/mock classes if standard weights are used.
- **VLM**: Uses `Salesforce/blip2-opt-2.7b`. It requires ~15GB system memory or a GPU. If memory is insufficient, the system will fall back to a mock mode.
