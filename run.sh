#!/bin/bash

# Sales Performance Analysis API Startup Script

echo "Starting Sales Performance Analysis API..."

# Activate virtual environment
source venv/bin/activate

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo "Server stopped."