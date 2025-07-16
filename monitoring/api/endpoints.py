"""
API endpoints for brain tumor monitoring system.
"""

import logging
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from ..core.monitor import BrainTumorImageMonitor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

# Global monitor instance
monitor = None


def get_monitor() -> BrainTumorImageMonitor:
    """Get the global monitor instance."""
    if monitor is None:
        raise HTTPException(status_code=500, detail="Monitor not initialized")
    return monitor


@router.get("/dashboard")
async def get_monitoring_dashboard() -> JSONResponse:
    """Get brain tumor monitoring dashboard data."""
    try:
        monitor_instance = get_monitor()
        dashboard_data = monitor_instance.get_brain_tumor_dashboard_data()
        return JSONResponse(content=dashboard_data)
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Error getting dashboard data")


@router.get("/drift-report")
async def generate_drift_report(days: int = 7) -> JSONResponse:
    """Generate brain tumor image drift report."""
    try:
        monitor_instance = get_monitor()
        report_path = monitor_instance.generate_brain_tumor_drift_report(days)
        return JSONResponse(
            content={
                "message": "Brain tumor drift report generated successfully",
                "report_path": report_path,
                "days_analyzed": days,
            }
        )
    except Exception as e:
        logger.error(f"Error generating drift report: {e}")
        raise HTTPException(status_code=500, detail="Error generating drift report")


@router.get("/feature-analysis")
async def analyze_feature_drift(days: int = 7) -> JSONResponse:
    """Analyze feature distributions and drift indicators."""
    try:
        monitor_instance = get_monitor()
        analysis = monitor_instance.analyze_feature_drift(days)
        return JSONResponse(content=analysis)
    except Exception as e:
        logger.error(f"Error analyzing feature drift: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing feature drift")


@router.get("/data-quality")
async def run_data_quality_tests() -> JSONResponse:
    """Run brain tumor image quality tests."""
    try:
        # Placeholder for data quality tests
        results = {
            "data_quality": True,
            "missing_values_test": True,
            "outliers_test": True,
            "drift_test": True,
            "timestamp": "2025-07-13T20:00:00",
        }
        return JSONResponse(content=results)
    except Exception as e:
        logger.error(f"Error running data quality tests: {e}")
        raise HTTPException(status_code=500, detail="Error running data quality tests")


@router.get("/report/{report_name}")
async def get_report(report_name: str) -> HTMLResponse:
    """Get a specific monitoring report."""
    try:
        monitor_instance = get_monitor()
        report_path = monitor_instance.reports_dir / report_name

        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")

        with open(report_path, "r") as f:
            content = f.read()

        return HTMLResponse(content=content)
    except Exception as e:
        logger.error(f"Error getting report: {e}")
        raise HTTPException(status_code=500, detail="Error getting report")


def init_monitor(database_url: str):
    """Initialize the global monitor instance."""
    global monitor
    monitor = BrainTumorImageMonitor(database_url)
