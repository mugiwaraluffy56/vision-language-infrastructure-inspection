#!/bin/bash

# Infrastructure Inspection System - Quick Start Script

echo "=========================================="
echo "Infrastructure Inspection System"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies if needed
if [ ! -f "venv/installed.flag" ]; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
    touch venv/installed.flag
    echo "✓ Backend dependencies installed"
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    echo "✓ Frontend dependencies installed"
fi

echo ""
echo "=========================================="
echo "Starting servers..."
echo "=========================================="
echo ""

# Start backend in background
echo "Starting backend on http://localhost:8000"
python -m backend.app.main &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "Starting frontend on http://localhost:3000"
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "Servers running!"
echo "=========================================="
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "=========================================="

# Wait for interrupt
wait

# Cleanup
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
