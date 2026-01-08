# Quick Start Guide

## Step 1: Install Dependencies

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

## Step 2: Start Backend

```bash
python3 run_backend.py
```

You should see:
```
============================================================
Infrastructure Inspection System - Backend
============================================================

Starting FastAPI server...
API will be available at: http://localhost:8000
Documentation at: http://localhost:8000/docs
```

## Step 3: Start Frontend

Open a **new terminal** and run:

```bash
./run_frontend.sh
```

You should see:
```
  ➜  Local:   http://localhost:3000/
```

## Step 4: Open Application

Open your browser and go to:
```
http://localhost:3000
```

## Testing the API

You can test the API directly at:
```
http://localhost:8000/docs
```

Or use the test script:
```bash
python3 test_api.py
```

## Troubleshooting

### Port 8000 already in use

Kill the process using port 8000:
```bash
lsof -ti :8000 | xargs kill -9
```

Then restart the backend.

### Frontend won't start

Make sure you're in the project root directory, not the frontend directory:
```bash
./run_frontend.sh
```

### Module not found errors

Make sure you installed all dependencies:
```bash
pip3 install -r requirements.txt
```

## Quick Commands

**Check if backend is running:**
```bash
curl http://localhost:8000/api/health
```

**Check if frontend is running:**
```bash
curl http://localhost:3000
```

**Stop all servers:**
Press `Ctrl+C` in each terminal window
