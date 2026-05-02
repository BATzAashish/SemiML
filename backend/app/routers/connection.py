"""
Connection Router - Test and system information endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.logging_config import logger

router = APIRouter(prefix="/api", tags=["Connection"])


@router.get("/connect")
async def test_connection():
    """
    Test endpoint for frontend to verify backend connection
    Returns system status and configuration
    """
    logger.info("Frontend connection test received")
    return {
        "status": "connected",
        "message": "Frontend successfully connected to SemiML Backend",
        "backend": {
            "name": "Hybrid Explainable ML Decision System",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        },
        "available_endpoints": {
            "health": "/health",
            "connection": "/api/connect",
            "system_info": "/api/system-info"
        }
    }


@router.get("/system-info")
async def get_system_info():
    """
    Get detailed system information
    Frontend can use this to display backend status
    """
    logger.info("System info requested")
    return {
        "system": {
            "name": "SemiML Backend",
            "version": "1.0.0",
            "status": "operational",
            "timestamp": datetime.now().isoformat()
        },
        "modules": {
            "module_1": {
                "name": "Project Foundation",
                "status": "active",
                "endpoints": [
                    "/health",
                    "/api/connect",
                    "/api/system-info"
                ]
            },
            "module_2": {
                "name": "Data Processing Layer",
                "status": "pending",
                "endpoints": []
            },
            "module_3_to_11": {
                "status": "pending"
            }
        },
        "tech_stack": [
            "FastAPI",
            "Pydantic",
            "Pandas",
            "Scikit-learn",
            "MLflow",
            "LangChain",
            "FAISS"
        ]
    }
