#!/usr/bin/env python3
"""Simple run script for the backend server."""

import os
import sys
import uvicorn

if __name__ == "__main__":
    # Set Python path
    os.environ['PYTHONPATH'] = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 Starting I2C AI Chatbot Backend...")
    print("📡 Server will be available at http://localhost:8000")
    print("📖 API documentation at http://localhost:8000/docs")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
