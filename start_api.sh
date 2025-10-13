#!/bin/bash
# Start FastAPI Backend and Scanner

echo "🚀 Starting Trading Signal System..."

# Start scanner in background
python run_all_scanners.py &
SCANNER_PID=$!
echo "✅ Scanner started (PID: $SCANNER_PID)"

# Start FastAPI
echo "🌐 Starting API server..."
uvicorn backend_api:app --host 0.0.0.0 --port 8000

