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
                "status": "active",
                "endpoints": [
                    "/api/upload-dataset",
                    "/api/dataset/{dataset_id}",
                    "/api/datasets",
                    "/api/dataset/{dataset_id} (DELETE)"
                ]
            },
            "module_3": {
                "name": "Meta-Features Extraction",
                "status": "active",
                "endpoints": [
                    "/api/extract-meta-features/{dataset_id}",
                    "/api/meta-features/{dataset_id}",
                    "/api/data-preview/{dataset_id}",
                    "/api/dataset-summary/{dataset_id}",
                    "/api/compare-datasets"
                ]
            },
            "module_4": {
                "name": "Experience Retrieval",
                "status": "active",
                "endpoints": [
                    "/api/store-experience",
                    "/api/find-similar-datasets",
                    "/api/get-best-practices",
                    "/api/get-best-models",
                    "/api/search-experiences",
                    "/api/experience-statistics"
                ]
            },
            "module_5": {
                "name": "Decision Engine",
                "status": "active",
                "endpoints": [
                    "/api/decide-pipeline",
                    "/api/detect-problem-type",
                    "/api/analyze-characteristics",
                    "/api/get-pipeline-recommendations",
                    "/api/decision-history"
                ]
            },
            "module_6": {
                "name": "Pipeline Builder",
                "status": "active",
                "endpoints": [
                    "/api/build-pipeline"
                ]
            },
            "module_7": {
                "name": "Training & Optimization",
                "status": "active",
                "endpoints": [
                    "/api/train-pipeline",
                    "/api/training-runs"
                ]
            },
            "module_8": {
                "name": "Validation",
                "status": "active",
                "endpoints": [
                    "/api/validate-model",
                    "/api/validation-runs"
                ]
            },
            "module_9": {
                "name": "Explainability",
                "status": "active",
                "endpoints": [
                    "/api/explain-model",
                    "/api/explanations"
                ]
            },
            "module_10": {
                "name": "Decision Trace",
                "status": "active",
                "endpoints": [
                    "/api/decision-trace",
                    "/api/decision-trace/{trace_id}"
                ]
            },
            "module_11": {
                "name": "Feedback & Learning",
                "status": "active",
                "endpoints": [
                    "/api/feedback"
                ]
            },
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
