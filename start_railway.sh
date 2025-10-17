#!/bin/bash
echo "Starting Railway deployment..."
echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"
echo "Environment variables:"
printenv | grep -E "(PORT|SUPABASE_URL)" | head -10

echo "Installing requirements if needed..."
pip install -r requirements.txt

echo "Starting FastAPI with uvicorn..."
PORT=${PORT:-8000} uvicorn backend_api:app --host 0.0.0.0 --port $PORT --workers 1 --timeout-keep-alive 30