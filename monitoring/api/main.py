"""
Main FastAPI application for brain tumor monitoring service.
"""

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .endpoints import init_monitor, router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Brain Tumor Monitoring Service",
    description="Monitoring and drift detection for brain tumor image classification",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize monitoring system
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    init_monitor(DATABASE_URL)
    logger.info("Monitoring system initialized successfully")
else:
    logger.error("DATABASE_URL environment variable is not set")

# Include monitoring routes
app.include_router(router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "brain-tumor-monitoring", "version": "1.0.0"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Brain Tumor Monitoring Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "dashboard": "/monitoring/dashboard",
            "drift_report": "/monitoring/drift-report",
            "feature_analysis": "/monitoring/feature-analysis",
            "data_quality": "/monitoring/data-quality",
        },
    }
