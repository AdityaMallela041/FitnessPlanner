#!/bin/bash

# FitPlanner Startup Script
echo "🚀 Starting FitPlanner - LlamaIndex Edition"
echo "=========================================="

cd src

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example .env
    echo "✏️  Please edit .env file and add your API keys before continuing."
    read -p "Press Enter when you've added your API keys..."
fi

echo "🏃 Starting FastAPI server..."
echo "Server will be available at: http://localhost:5000"
echo "API docs will be available at: http://localhost:5000/docs"
echo ""
echo "In another terminal, run: streamlit run streamlit/streamlit_app.py"
echo "Streamlit app will be available at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the FastAPI server
python main.py
