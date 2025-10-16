#!/bin/bash
echo "Starting Railway deployment..."
echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"
echo "Starting FastAPI with uvicorn..."
uvicorn backend_api:app --host 0.0.0.0 --port $PORT --workers 1