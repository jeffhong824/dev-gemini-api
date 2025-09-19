#!/usr/bin/env python3
"""
FastAPI server for Gemini Image Generation API

This script starts the FastAPI server with all image generation endpoints.
"""

import uvicorn
from api.main import app

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
