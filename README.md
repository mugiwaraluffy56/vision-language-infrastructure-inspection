# Vision-Language Based Infrastructure Inspection System

An end-to-end AI system that detects structural defects from infrastructure images and explains their engineering significance using Vision-Language Models.

---

## 🚧 Problem Statement

Manual inspection of infrastructure such as bridges, buildings, and industrial facilities is:

- Time-consuming  
- Subjective and error-prone  
- Heavily dependent on expert availability  

Inspectors must visually identify defects and then manually prepare detailed inspection reports, which slows down maintenance decisions and increases operational risk.

---

## 💡 Solution Overview

This project presents an automated infrastructure inspection system that combines:

- Computer Vision for defect detection  
- Vision-Language Models (VLMs) for engineering-level explanations  
- Backend APIs for structured inspection reports  

The system takes an image as input, detects structural defects, evaluates their severity, and generates an inspection-style explanation suitable for engineering review.

---

## 🧠 System Architecture

Image Input  
↓  
Defect Detection (YOLOv8)  
↓  
Severity Assessment (Rule-Based)  
↓  
Vision-Language Reasoning (BLIP-2 / LLaVA)  
↓  
Structured Inspection Report  

---

## 🔍 Supported Defect Types (MVP)

The current implementation focuses on three common and high-impact defect categories:

1. **Cracks** – Structural or surface-level cracking in concrete or steel components  
2. **Corrosion** – Material degradation due to oxidation  
3. **Spalling** – Surface breaking or chipping of concrete  

---

## 🛠 Tech Stack

### Backend & Machine Learning
- Python  
- FastAPI  
- PyTorch  

### Computer Vision
- YOLOv8 – defect detection  
- SAM – optional segmentation  

### Vision-Language Models
- BLIP-2 or LLaVA  
- Prompted as a structural inspection engineer  

---

## 📥 Input

- A single image of infrastructure (bridge, beam, column, wall, or industrial surface)

---

## 📤 Output

The system produces a structured inspection result containing:

- Defect type  
- Bounding box location  
- Severity level (Low / Medium / High)  
- Engineering explanation  
- Recommended action  

### Example Output

Defect: Crack  
Location: Beam joint  
Severity: High  

Explanation:  
A longitudinal crack is detected near the beam joint, indicating potential fatigue stress concentration. Immediate monitoring and repair are recommended.

---

## 📄 Inspection Report Structure

Each inspection follows a consistent format:

1. Asset Type  
2. Detected Defects  
3. Severity Assessment  
4. Engineering Explanation  
5. Recommended Action  

This structure mirrors real-world inspection documentation used in engineering and infrastructure maintenance workflows.

---

## 🚀 How to Run (Development)

1. Clone the repository  
2. Install dependencies from `backend/requirements.txt`  
3. Start the FastAPI server using Uvicorn  

---

## 🎯 Project Scope (MVP)

- Single-image inspection  
- Three defect classes  
- Rule-based severity scoring  
- Vision-language explanation  
- JSON-based inspection report  

The scope is intentionally limited to ensure clarity, reliability, and real-world relevance.

---

## 🔮 Future Enhancements

- Video-based inspection  
- Defect progression tracking  
- Multi-defect severity aggregation  
- PDF inspection report generation  
- Integration with maintenance management systems  
- Deployment on edge devices or drones  

---

## 🏆 Use Cases

- Infrastructure inspection (bridges, buildings, industrial plants)  
- Preventive maintenance planning  
- Engineering audit support  
- Smart city monitoring systems  

---

## 📌 Project Status

In Progress (MVP Stage)  

This project is actively being developed as part of an applied AI and computer vision initiative.

---

## 📜 License

This project is licensed under the MIT License.
