"""
Connection Router - Test and system information endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel
from app.logging_config import logger

router = APIRouter(prefix="/api", tags=["Connection"])


class ChatMessage(BaseModel):
    message: str
    history: Optional[list] = None


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


# ===== UTILITY ENDPOINTS FOR FRONTEND =====

@router.get("/data-profile")
async def get_data_profile():
    """
    Get data profile/overview for dashboard
    Returns mock data for initial dashboard display
    """
    logger.info("Data profile requested")
    return {
        "status": "success",
        "data": {
            "rows": 18420,
            "columns": 36,
            "missingValues": 742,
            "target": "readmission_risk",
            "classes": 3,
            "missingValuesDetail": [
                {"name": "age", "value": 0.4},
                {"name": "lab_glucose", "value": 6.7},
                {"name": "medication", "value": 2.8},
                {"name": "visits", "value": 1.1}
            ]
        }
    }


@router.get("/pipeline")
async def get_pipeline():
    """
    Get current pipeline configuration
    Returns active pipeline for dashboard
    """
    logger.info("Pipeline data requested")
    return {
        "status": "success",
        "data": {
            "steps": [
                "Schema validation",
                "Missingness-aware imputation",
                "Robust scaling",
                "Mutual information feature selection",
                "Calibrated gradient boosting",
                "SHAP audit layer"
            ],
            "models": [
                {
                    "name": "Explainable Gradient Boosting",
                    "accuracy": 0.914,
                    "precision": 0.902,
                    "recall": 0.888,
                    "confidence": 0.93,
                    "selected": True
                },
                {
                    "name": "Random Forest + SHAP",
                    "accuracy": 0.891,
                    "precision": 0.874,
                    "recall": 0.861,
                    "confidence": 0.86
                }
            ]
        }
    }


@router.get("/evaluation")
async def get_evaluation():
    """
    Get model evaluation metrics
    Returns validation and performance metrics
    """
    logger.info("Evaluation data requested")
    return {
        "status": "success",
        "data": {
            "metrics": [
                {"metric": "Accuracy", "value": 0.914},
                {"metric": "F1 score", "value": 0.897},
                {"metric": "RMSE", "value": 0.284},
                {"metric": "AUC", "value": 0.941}
            ],
            "confusion": [
                [412, 34, 12],
                [28, 301, 26],
                [9, 31, 177]
            ]
        }
    }


@router.get("/explanations")
async def get_explanations():
    """
    Get model explanations and feature importance
    Returns SHAP and importance scores
    """
    logger.info("Explanations requested")
    return {
        "status": "success",
        "data": {
            "importance": [
                {"feature": "prior_admissions", "value": 0.32},
                {"feature": "lab_glucose", "value": 0.26},
                {"feature": "age", "value": 0.21},
                {"feature": "medication_count", "value": 0.16},
                {"feature": "visit_gap", "value": 0.12}
            ],
            "shap": [
                {"feature": "prior_admissions", "impact": 0.44},
                {"feature": "lab_glucose", "impact": 0.29},
                {"feature": "age", "impact": -0.18}
            ]
        }
    }


@router.post("/chat")
async def chat_with_assistant(chat_msg: ChatMessage):
    """
    Chat with AI assistant
    Provides explainability and recommendations
    """
    logger.info(f"Chat message received: {chat_msg.message[:50]}")
    
    is_why_question = "why" in chat_msg.message.lower()
    response_text = (
        "recall priority, calibrated confidence, and SHAP-compatible model structure"
        if is_why_question
        else "I would re-profile the dataset, compare drift, and update the pipeline confidence before replacing the selected model"
    )
    
    return {
        "status": "success",
        "message": f"The recommendation is driven by traceable constraints: {response_text}.",
        "role": "assistant"
    }


# ============================================================================
# Phase 5: Unified Experience Retrieval Endpoint
# ============================================================================

class ExperienceRetrievalRequest(BaseModel):
    """Request model for unified experience retrieval"""
    dataset_meta_features: Dict[str, Any]
    problem_type: Optional[str] = None
    top_k: int = 5


@router.post("/retrieve-experience")
async def retrieve_experience(request: ExperienceRetrievalRequest) -> Dict[str, Any]:
    """
    Unified endpoint for comprehensive experience retrieval
    
    Consolidates all experience-related data into a single endpoint:
    - Similar datasets from past projects
    - Best performing models on similar data
    - Recommended preprocessing approaches
    - ML best practices relevant to problem
    
    Args:
        request: Meta-features of current dataset and top_k count
        
    Returns:
        Consolidated experience data with similar datasets, best models, and practices
    """
    try:
        from app.modules.module_4_experience_retrieval.service import experience_retriever
        from app.modules.module_4_experience_retrieval.knowledge_ingestion import get_knowledge_base
        
        logger.info("Retrieving unified experience data")
        
        # Retrieve similar datasets
        similar_datasets = experience_retriever.find_similar_datasets(
            request.dataset_meta_features,
            top_k=request.top_k
        )
        
        # Get best models for similar datasets
        best_models = experience_retriever.get_best_models_for_dataset(
            request.dataset_meta_features,
            top_k=request.top_k
        )
        
        # Get best practices
        best_practices = experience_retriever.get_best_practices(
            request.dataset_meta_features
        )
        
        # Retrieve from knowledge base
        kb = get_knowledge_base()
        knowledge_results = []
        if kb:
            problem_desc = f"Dataset with {request.dataset_meta_features.get('num_rows', 'unknown')} rows, {request.dataset_meta_features.get('num_columns', 'unknown')} columns"
            knowledge_results = kb.retrieve(problem_desc, top_k=request.top_k)
        
        return {
            "status": "success",
            "summary": {
                "similar_datasets_count": len(similar_datasets),
                "recommended_models_count": len(best_models),
                "practices_count": len(best_practices) if isinstance(best_practices, list) else 1,
                "knowledge_items_count": len(knowledge_results),
            },
            "similar_datasets": similar_datasets,
            "recommended_models": best_models,
            "best_practices": best_practices,
            "knowledge_base_insights": knowledge_results,
            "confidence": {
                "dataset_similarity": 0.85 if similar_datasets else 0.0,
                "model_recommendation": 0.88 if best_models else 0.0,
                "practice_recommendation": 0.82 if best_practices else 0.0,
            }
        }
        
    except Exception as e:
        logger.error(f"Error retrieving experience: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
